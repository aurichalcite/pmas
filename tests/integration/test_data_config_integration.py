"""
Integration tests for PMAS data loading and configuration workflows.

This module tests the interaction between configuration loading, data readers,
and test execution workflows. Tests cover:
- Configuration loading from files and environment
- Data provider integration with test parametrization
- Cross-module data flow and validation
- Error handling in data loading workflows
- Configuration-driven test data management

Uses temporary files and mock environments for deterministic testing.
No external dependencies or network calls.
"""

import json
import tempfile
from pathlib import Path
from typing import Any

import pytest
import yaml

from pmas import Config
from pmas.core.errors import ValidationError
from pmas.data.readers import (
    DataProvider,
    _convert_value,
    load_test_data,
    parametrize_from_file,
)


@pytest.mark.integration
class TestDataConfigurationIntegration:
    """Integration tests for data loading and configuration workflows."""

    @pytest.fixture
    def temp_data_dir(self) -> Path:
        """Create temporary directory with test data files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            data_dir = Path(temp_dir)

            # Create test CSV file
            csv_file = data_dir / "test_users.csv"
            csv_file.write_text(
                "username,password,role,active\n"
                "admin,admin123,administrator,true\n"
                "user1,pass123,user,true\n"
                "user2,pass456,user,false\n"
            )

            # Create test JSON file
            json_file = data_dir / "test_config.json"
            json_data = [
                {"environment": "dev", "timeout": 5, "retries": 3},
                {"environment": "staging", "timeout": 10, "retries": 2},
                {"environment": "prod", "timeout": 15, "retries": 1},
            ]
            json_file.write_text(json.dumps(json_data, indent=2))

            # Create test YAML file
            yaml_file = data_dir / "test_scenarios.yaml"
            yaml_data = [
                {
                    "scenario": "login_success",
                    "expected_result": "dashboard",
                    "priority": 1,
                },
                {
                    "scenario": "login_failure",
                    "expected_result": "error",
                    "priority": 2,
                },
                {"scenario": "logout", "expected_result": "login_page", "priority": 1},
            ]
            yaml_file.write_text(yaml.dump(yaml_data))

            yield data_dir

    @pytest.fixture
    def test_config(self) -> Config:
        """Provide test configuration for integration tests."""
        config = Config()
        config.environment.name = "integration_test"
        config.test.default_timeout = 10.0
        config.test.retry_count = 2
        return config

    def test_data_provider_configuration_integration(
        self, temp_data_dir: Path, test_config: Config
    ):
        """Test DataProvider integration with configuration settings."""
        # Initialize DataProvider with configuration-driven data directory
        data_provider = DataProvider(temp_data_dir)

        # Test CSV data loading with configuration
        csv_data = data_provider.get_data("test_users.csv")

        # Verify data structure and types
        assert len(csv_data) == 3
        assert all(isinstance(row, dict) for row in csv_data)
        assert csv_data[0]["username"] == "admin"
        assert csv_data[0]["active"] is True  # Should be converted from string

        # Test JSON data loading
        json_data = data_provider.get_data("test_config.json")
        assert len(json_data) == 3
        assert json_data[0]["environment"] == "dev"
        assert json_data[0]["timeout"] == 5

        # Test YAML data loading
        yaml_data = data_provider.get_data("test_scenarios.yaml")
        assert len(yaml_data) == 3
        assert yaml_data[0]["scenario"] == "login_success"
        assert yaml_data[0]["priority"] == 1

    def test_configuration_driven_data_filtering(
        self, temp_data_dir: Path, test_config: Config
    ):
        """Test data filtering based on configuration settings."""
        data_provider = DataProvider(temp_data_dir)

        # Test filtering active users only
        def active_users_filter(item: dict[str, Any]) -> bool:
            return item.get("active", False) is True

        active_users = data_provider.get_data(
            "test_users.csv", filter_func=active_users_filter
        )

        assert len(active_users) == 2  # admin and user1
        assert all(user["active"] is True for user in active_users)

        # Test filtering by environment
        def dev_config_filter(item: dict[str, Any]) -> bool:
            return item.get("environment") == "dev"

        dev_configs = data_provider.get_data(
            "test_config.json", filter_func=dev_config_filter
        )

        assert len(dev_configs) == 1
        assert dev_configs[0]["environment"] == "dev"

    def test_parametrize_from_file_integration(self, temp_data_dir: Path):
        """Test pytest parametrization integration with file data."""
        csv_file = temp_data_dir / "test_users.csv"

        # Test parametrization with ID field
        parametrized_data = parametrize_from_file(csv_file, id_field="username")

        # Verify parametrization structure
        assert len(parametrized_data) == 3

        # Check first parametrized item (tuple of test_id, test_data)
        first_item = parametrized_data[0]
        assert isinstance(first_item, tuple)
        assert len(first_item) == 2

        test_id, test_data = first_item
        assert test_id == "admin"

        # Verify data content
        assert test_data["username"] == "admin"
        assert test_data["role"] == "administrator"

    def test_cross_format_data_consistency(self, temp_data_dir: Path):
        """Test data consistency across different file formats."""
        # Create equivalent data in different formats
        test_data = [
            {"name": "test1", "value": 100, "enabled": True},
            {"name": "test2", "value": 200, "enabled": False},
        ]

        # Write as JSON
        json_file = temp_data_dir / "consistency_test.json"
        json_file.write_text(json.dumps(test_data))

        # Write as YAML
        yaml_file = temp_data_dir / "consistency_test.yaml"
        yaml_file.write_text(yaml.dump(test_data))

        # Write as CSV
        csv_file = temp_data_dir / "consistency_test.csv"
        csv_file.write_text("name,value,enabled\ntest1,100,true\ntest2,200,false\n")

        # Load data from all formats
        json_data = load_test_data(json_file)
        yaml_data = load_test_data(yaml_file)
        csv_data = load_test_data(csv_file)

        # Verify consistency
        assert len(json_data) == len(yaml_data) == len(csv_data) == 2

        # Verify data equivalence (accounting for type conversion)
        for i in range(2):
            assert json_data[i]["name"] == yaml_data[i]["name"] == csv_data[i]["name"]
            assert (
                json_data[i]["value"] == yaml_data[i]["value"] == csv_data[i]["value"]
            )
            assert (
                json_data[i]["enabled"]
                == yaml_data[i]["enabled"]
                == csv_data[i]["enabled"]
            )

    def test_configuration_error_handling_integration(self, temp_data_dir: Path):
        """Test error handling across configuration and data loading."""
        data_provider = DataProvider(temp_data_dir)

        # Test file not found error
        with pytest.raises(ValidationError):
            data_provider.get_data("nonexistent_file.csv")

        # Test invalid file format
        invalid_file = temp_data_dir / "invalid.txt"
        invalid_file.write_text("This is not valid data")

        with pytest.raises(ValidationError):
            load_test_data(invalid_file)

        # Test malformed JSON
        bad_json_file = temp_data_dir / "bad.json"
        bad_json_file.write_text('{"invalid": json}')

        with pytest.raises(ValidationError):
            load_test_data(bad_json_file)

    def test_data_caching_integration(self, temp_data_dir: Path):
        """Test data caching behavior in integration scenarios."""
        data_provider = DataProvider(temp_data_dir)

        # First load should cache data
        data1 = data_provider.get_data("test_users.csv", use_cache=True)

        # Second load should use cache
        data2 = data_provider.get_data("test_users.csv", use_cache=True)

        # Should be the same object reference (cached)
        assert data1 is data2

        # Third load without cache should be different object
        data3 = data_provider.get_data("test_users.csv", use_cache=False)
        assert data3 is not data1
        assert data3 == data1  # Same content, different object

        # Clear cache and verify
        data_provider.clear_cache()
        data4 = data_provider.get_data("test_users.csv", use_cache=True)
        assert data4 is not data1  # New object after cache clear

    def test_environment_configuration_integration(self, temp_data_dir: Path):
        """Test environment-specific configuration integration."""
        # Create environment-specific config files
        dev_config = temp_data_dir / "dev_config.json"
        dev_config.write_text(
            json.dumps({"database_url": "dev.db", "debug": True, "timeout": 5})
        )

        prod_config = temp_data_dir / "prod_config.json"
        prod_config.write_text(
            json.dumps({"database_url": "prod.db", "debug": False, "timeout": 30})
        )

        data_provider = DataProvider(temp_data_dir)

        # Test environment-specific data loading
        dev_data = data_provider.get_data("dev_config.json")
        prod_data = data_provider.get_data("prod_config.json")

        assert dev_data[0]["debug"] is True
        assert prod_data[0]["debug"] is False
        assert dev_data[0]["timeout"] == 5
        assert prod_data[0]["timeout"] == 30

    def test_value_conversion_integration(self):
        """Test value conversion integration across data types."""
        # Test boolean conversion
        assert _convert_value("true") is True
        assert _convert_value("false") is False
        assert _convert_value("TRUE") is True

        # Test numeric conversion
        assert _convert_value("123") == 123
        assert _convert_value("45.67") == 45.67
        assert _convert_value("-89") == -89

        # Test string preservation
        assert _convert_value("hello") == "hello"
        assert _convert_value("123abc") == "123abc"

    def test_large_dataset_handling_integration(self, temp_data_dir: Path):
        """Test integration with larger datasets."""
        # Create larger CSV file
        large_csv = temp_data_dir / "large_dataset.csv"
        csv_content = "id,name,value,category\n"

        # Generate 100 rows of test data
        for i in range(100):
            csv_content += f"{i},user_{i},{i * 10},category_{i % 5}\n"

        large_csv.write_text(csv_content)

        data_provider = DataProvider(temp_data_dir)

        # Test loading large dataset
        large_data = data_provider.get_data("large_dataset.csv")

        assert len(large_data) == 100
        assert large_data[0]["id"] == 0
        assert large_data[99]["id"] == 99

        # Test filtering large dataset
        def category_0_filter(item: dict[str, Any]) -> bool:
            return item["category"] == "category_0"

        filtered_data = data_provider.get_data(
            "large_dataset.csv", filter_func=category_0_filter
        )

        # Should have 20 items (every 5th item: 0, 5, 10, ..., 95)
        assert len(filtered_data) == 20
        assert all(item["category"] == "category_0" for item in filtered_data)

    def test_configuration_validation_integration(
        self, temp_data_dir: Path, test_config: Config
    ):
        """Test configuration validation in integration context."""
        # Test valid configuration
        assert test_config.environment.name == "integration_test"
        assert test_config.test.default_timeout == 10.0

        # Test configuration with data provider
        data_provider = DataProvider(temp_data_dir)

        # Use configuration values in data operations
        def timeout_based_filter(item: dict[str, Any]) -> bool:
            return item.get("timeout", 0) <= test_config.test.default_timeout

        config_data = data_provider.get_data(
            "test_config.json", filter_func=timeout_based_filter
        )

        # Should filter based on config timeout
        assert len(config_data) == 2  # dev (5) and staging (10), not prod (15)
        assert all(
            item["timeout"] <= test_config.test.default_timeout for item in config_data
        )
