"""
Comprehensive unit tests for data readers module.

This module tests the data reading functionality with extensive mocking to ensure:
- CSV, JSON, and YAML file loading
- Data type conversion and validation
- Error handling for missing/invalid files
- Test data parameterization
- Data provider class functionality
- Iterator-based data loading for large files
"""

import json
from io import StringIO
from pathlib import Path
from unittest.mock import Mock, mock_open, patch

import pytest

from pmas.core.errors import ValidationError
from pmas.data.readers import (
    DataProvider,
    _convert_value,
    load_csv,
    load_json,
    load_test_data,
    load_yaml,
    parametrize_from_file,
)


class TestValueConversion:
    """Test the _convert_value helper function."""

    @pytest.mark.parametrize(
        "input_value, expected_output",
        [
            ("true", True),
            ("True", True),
            ("TRUE", True),
            ("false", False),
            ("False", False),
            ("FALSE", False),
            ("123", 123),
            ("0", 0),
            ("-456", -456),
            ("3.14", 3.14),
            ("0.0", 0.0),
            ("-2.5", -2.5),
            ("1.23e4", 12300.0),
            ("hello", "hello"),
            ("", ""),
            ("123.456.789", "123.456.789"),  # Invalid number format
        ],
    )
    def test_convert_value_when_various_inputs_expects_correct_types(
        self, input_value, expected_output
    ):
        """Test _convert_value handles various input types correctly."""
        result = _convert_value(input_value)
        assert result == expected_output
        assert isinstance(result, type(expected_output))

    def test_convert_value_when_non_string_input_expects_unchanged(self):
        """Test _convert_value returns non-string inputs unchanged."""
        inputs = [123, 3.14, True, None, [], {}]
        for input_value in inputs:
            result = _convert_value(input_value)
            assert result is input_value


class TestCSVLoader:
    """Test CSV file loading functionality."""

    @patch("pmas.data.readers.Path")
    @patch("builtins.open", new_callable=mock_open)
    def test_load_csv_when_valid_file_with_header_expects_correct_data(
        self, mock_file, mock_path
    ):
        """Test loading CSV file with header row."""
        # Setup mock
        mock_path_instance = Mock()
        mock_path.return_value = mock_path_instance
        mock_path_instance.exists.return_value = True

        csv_content = "name,age,active\nJohn,25,true\nJane,30,false\n"
        mock_file.return_value = StringIO(csv_content)

        result = load_csv("test.csv")

        expected = [
            {"name": "John", "age": 25, "active": True},
            {"name": "Jane", "age": 30, "active": False},
        ]
        assert result == expected

    @patch("pmas.data.readers.Path")
    @patch("builtins.open", new_callable=mock_open)
    def test_load_csv_when_no_header_expects_generated_column_names(
        self, mock_file, mock_path
    ):
        """Test loading CSV file without header row."""
        mock_path_instance = Mock()
        mock_path.return_value = mock_path_instance
        mock_path_instance.exists.return_value = True

        csv_content = "John,25,true\nJane,30,false\n"
        mock_file.return_value = StringIO(csv_content)

        result = load_csv("test.csv", has_header=False)

        expected = [
            {"column_0": "John", "column_1": 25, "column_2": True},
            {"column_0": "Jane", "column_1": 30, "column_2": False},
        ]
        assert result == expected

    @patch("pmas.data.readers.Path")
    @patch("builtins.open", new_callable=mock_open)
    def test_load_csv_when_empty_values_expects_none(self, mock_file, mock_path):
        """Test that empty CSV values are converted to None."""
        mock_path_instance = Mock()
        mock_path.return_value = mock_path_instance
        mock_path_instance.exists.return_value = True

        csv_content = "name,age,email\nJohn,,john@example.com\n,25,\n"
        mock_file.return_value = StringIO(csv_content)

        result = load_csv("test.csv")

        expected = [
            {"name": "John", "age": None, "email": "john@example.com"},
            {"name": None, "age": 25, "email": None},
        ]
        assert result == expected

    @patch("pmas.data.readers.Path")
    def test_load_csv_when_file_not_found_expects_validation_error(self, mock_path):
        """Test that missing CSV file raises ValidationError."""
        mock_path_instance = Mock()
        mock_path.return_value = mock_path_instance
        mock_path_instance.exists.return_value = False

        with pytest.raises(ValidationError) as exc_info:
            load_csv("missing.csv")

        assert "CSV file not found" in str(exc_info.value)

    @patch("pmas.data.readers.Path")
    @patch("builtins.open", new_callable=mock_open)
    def test_load_csv_when_custom_delimiter_expects_correct_parsing(
        self, mock_file, mock_path
    ):
        """Test CSV loading with custom delimiter."""
        mock_path_instance = Mock()
        mock_path.return_value = mock_path_instance
        mock_path_instance.exists.return_value = True

        csv_content = "name;age;active\nJohn;25;true\nJane;30;false\n"
        mock_file.return_value = StringIO(csv_content)

        result = load_csv("test.csv", delimiter=";")

        expected = [
            {"name": "John", "age": 25, "active": True},
            {"name": "Jane", "age": 30, "active": False},
        ]
        assert result == expected


class TestJSONLoader:
    """Test JSON file loading functionality."""

    @patch("pmas.data.readers.Path")
    @patch("builtins.open", new_callable=mock_open)
    def test_load_json_when_valid_file_expects_parsed_data(self, mock_file, mock_path):
        """Test loading valid JSON file."""
        mock_path_instance = Mock()
        mock_path.return_value = mock_path_instance
        mock_path_instance.exists.return_value = True

        json_data = {
            "users": [{"name": "John", "age": 25}, {"name": "Jane", "age": 30}]
        }
        mock_file.return_value = StringIO(json.dumps(json_data))

        result = load_json("test.json")

        assert result == json_data

    @patch("pmas.data.readers.Path")
    def test_load_json_when_file_not_found_expects_validation_error(self, mock_path):
        """Test that missing JSON file raises ValidationError."""
        mock_path_instance = Mock()
        mock_path.return_value = mock_path_instance
        mock_path_instance.exists.return_value = False

        with pytest.raises(ValidationError) as exc_info:
            load_json("missing.json")

        assert "JSON file not found" in str(exc_info.value)

    @patch("pmas.data.readers.Path")
    @patch("builtins.open", new_callable=mock_open)
    def test_load_json_when_invalid_json_expects_validation_error(
        self, mock_file, mock_path
    ):
        """Test that invalid JSON raises ValidationError."""
        mock_path_instance = Mock()
        mock_path.return_value = mock_path_instance
        mock_path_instance.exists.return_value = True

        mock_file.return_value = StringIO('{"invalid": json}')

        with pytest.raises(ValidationError) as exc_info:
            load_json("invalid.json")

        assert "Invalid JSON" in str(exc_info.value)


class TestYAMLLoader:
    """Test YAML file loading functionality."""

    @patch("pmas.data.readers.Path")
    @patch("builtins.open", new_callable=mock_open)
    def test_load_yaml_when_valid_file_expects_parsed_data(self, mock_file, mock_path):
        """Test loading valid YAML file."""
        mock_path_instance = Mock()
        mock_path.return_value = mock_path_instance
        mock_path_instance.exists.return_value = True

        yaml_content = """
        users:
          - name: John
            age: 25
          - name: Jane
            age: 30
        """
        mock_file.return_value = StringIO(yaml_content)

        result = load_yaml("test.yaml")

        expected = {"users": [{"name": "John", "age": 25}, {"name": "Jane", "age": 30}]}
        assert result == expected

    @patch("pmas.data.readers.Path")
    def test_load_yaml_when_file_not_found_expects_validation_error(self, mock_path):
        """Test that missing YAML file raises ValidationError."""
        mock_path_instance = Mock()
        mock_path.return_value = mock_path_instance
        mock_path_instance.exists.return_value = False

        with pytest.raises(ValidationError) as exc_info:
            load_yaml("missing.yaml")

        assert "YAML file not found" in str(exc_info.value)

    @patch("pmas.data.readers.Path")
    @patch("builtins.open", new_callable=mock_open)
    def test_load_yaml_when_invalid_yaml_expects_validation_error(
        self, mock_file, mock_path
    ):
        """Test that invalid YAML raises ValidationError."""
        mock_path_instance = Mock()
        mock_path.return_value = mock_path_instance
        mock_path_instance.exists.return_value = True

        mock_file.return_value = StringIO("invalid: yaml: content: [")

        with pytest.raises(ValidationError) as exc_info:
            load_yaml("invalid.yaml")

        assert "Invalid YAML" in str(exc_info.value)


class TestLoadTestData:
    """Test the load_test_data function with format auto-detection."""

    @patch("pmas.data.readers.load_csv")
    def test_load_test_data_when_csv_file_expects_csv_loader_called(
        self, mock_load_csv
    ):
        """Test that CSV files are handled by CSV loader."""
        mock_load_csv.return_value = [{"test": "data"}]

        result = load_test_data("test.csv")

        mock_load_csv.assert_called_once()
        assert result == [{"test": "data"}]

    @patch("pmas.data.readers.load_json")
    def test_load_test_data_when_json_dict_expects_list_conversion(
        self, mock_load_json
    ):
        """Test that JSON dict is converted to list."""
        mock_load_json.return_value = {"test": "data"}

        result = load_test_data("test.json")

        assert result == [{"test": "data"}]

    @patch("pmas.data.readers.load_json")
    def test_load_test_data_when_json_list_expects_unchanged(self, mock_load_json):
        """Test that JSON list is returned unchanged."""
        mock_load_json.return_value = [{"test": "data1"}, {"test": "data2"}]

        result = load_test_data("test.json")

        assert result == [{"test": "data1"}, {"test": "data2"}]

    @patch("pmas.data.readers.load_yaml")
    def test_load_test_data_when_yaml_file_expects_yaml_loader_called(
        self, mock_load_yaml
    ):
        """Test that YAML files are handled by YAML loader."""
        mock_load_yaml.return_value = [{"test": "data"}]

        result = load_test_data("test.yml")

        mock_load_yaml.assert_called_once()
        assert result == [{"test": "data"}]

    def test_load_test_data_when_unsupported_format_expects_validation_error(self):
        """Test that unsupported file format raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            load_test_data("test.xml")

        assert "Unsupported file format: xml" in str(exc_info.value)

    @patch("pmas.data.readers.load_json")
    def test_load_test_data_when_explicit_format_expects_format_used(
        self, mock_load_json
    ):
        """Test that explicit format parameter is used."""
        mock_load_json.return_value = [{"test": "data"}]

        load_test_data("test.txt", file_format="json")

        mock_load_json.assert_called_once()


class TestParametrizeFromFile:
    """Test parametrization functionality for pytest."""

    @patch("pmas.data.readers.load_test_data")
    def test_parametrize_from_file_when_no_id_field_expects_indexed_ids(
        self, mock_load_test_data
    ):
        """Test parametrization with auto-generated IDs."""
        mock_load_test_data.return_value = [
            {"name": "test1", "value": 1},
            {"name": "test2", "value": 2},
        ]

        result = parametrize_from_file("test.csv")

        expected = [
            ("data_0", {"name": "test1", "value": 1}),
            ("data_1", {"name": "test2", "value": 2}),
        ]
        assert result == expected

    @patch("pmas.data.readers.load_test_data")
    def test_parametrize_from_file_when_id_field_specified_expects_field_used(
        self, mock_load_test_data
    ):
        """Test parametrization with specified ID field."""
        mock_load_test_data.return_value = [
            {"test_id": "login_valid", "username": "user1"},
            {"test_id": "login_invalid", "username": "user2"},
        ]

        result = parametrize_from_file("test.csv", id_field="test_id")

        expected = [
            ("login_valid", {"test_id": "login_valid", "username": "user1"}),
            ("login_invalid", {"test_id": "login_invalid", "username": "user2"}),
        ]
        assert result == expected

    @patch("pmas.data.readers.load_test_data")
    def test_parametrize_from_file_when_filter_func_expects_filtered_data(
        self, mock_load_test_data
    ):
        """Test parametrization with filter function."""
        mock_load_test_data.return_value = [
            {"name": "test1", "enabled": True},
            {"name": "test2", "enabled": False},
            {"name": "test3", "enabled": True},
        ]

        def filter_func(item):
            return item["enabled"]
        result = parametrize_from_file("test.csv", filter_func=filter_func)

        expected = [
            ("data_0", {"name": "test1", "enabled": True}),
            ("data_1", {"name": "test3", "enabled": True}),
        ]
        assert result == expected


class TestDataProvider:
    """Test DataProvider class functionality."""

    def test_init_when_data_dir_provided_expects_correct_setup(self):
        """Test DataProvider initialization."""
        provider = DataProvider("custom_data")

        assert provider.data_dir == Path("custom_data")
        assert provider._cache == {}

    @patch("pmas.data.readers.load_test_data")
    def test_get_data_when_first_call_expects_data_loaded_and_cached(
        self, mock_load_test_data
    ):
        """Test that data is loaded and cached on first call."""
        mock_load_test_data.return_value = [{"test": "data"}]
        provider = DataProvider("test_data")

        result = provider.get_data("test.csv")

        assert result == [{"test": "data"}]
        mock_load_test_data.assert_called_once()
        # Check cache
        cache_key = str(Path("test_data") / "test.csv")
        assert provider._cache[cache_key] == [{"test": "data"}]

    @patch("pmas.data.readers.load_test_data")
    def test_get_data_when_cached_expects_cache_used(self, mock_load_test_data):
        """Test that cached data is used on subsequent calls."""
        provider = DataProvider("test_data")
        cache_key = str(Path("test_data") / "test.csv")
        provider._cache[cache_key] = [{"cached": "data"}]

        result = provider.get_data("test.csv")

        assert result == [{"cached": "data"}]
        mock_load_test_data.assert_not_called()

    @patch("pmas.data.readers.load_test_data")
    def test_get_data_when_cache_disabled_expects_fresh_load(self, mock_load_test_data):
        """Test that cache can be bypassed."""
        mock_load_test_data.return_value = [{"fresh": "data"}]
        provider = DataProvider("test_data")
        cache_key = str(Path("test_data") / "test.csv")
        provider._cache[cache_key] = [{"cached": "data"}]

        result = provider.get_data("test.csv", use_cache=False)

        assert result == [{"fresh": "data"}]
        mock_load_test_data.assert_called_once()

    def test_clear_cache_when_called_expects_cache_empty(self):
        """Test cache clearing functionality."""
        provider = DataProvider("test_data")
        provider._cache["test"] = [{"data": "value"}]

        provider.clear_cache()

        assert provider._cache == {}

    @patch("pathlib.Path.exists")
    @patch("pathlib.Path.iterdir")
    def test_list_data_files_when_files_exist_expects_supported_files_only(
        self, mock_iterdir, mock_exists
    ):
        """Test listing of supported data files."""
        mock_exists.return_value = True

        # Mock files
        mock_files = [
            Mock(is_file=Mock(return_value=True), suffix=".csv"),
            Mock(is_file=Mock(return_value=True), suffix=".json"),
            Mock(is_file=Mock(return_value=True), suffix=".yaml"),
            Mock(is_file=Mock(return_value=True), suffix=".txt"),  # Unsupported
            Mock(is_file=Mock(return_value=False), suffix=".csv"),  # Directory
        ]
        mock_iterdir.return_value = mock_files

        provider = DataProvider("test_data")
        result = provider.list_data_files()

        # Should return only supported file types that are actual files
        assert len(result) == 3


class TestDataReadersBranchCoverage:
    """Test specific conditional branches to improve branch coverage."""

    @patch("pmas.data.readers.load_json")
    def test_load_test_data_when_json_invalid_type_expects_validation_error(
        self, mock_load_json
    ):
        """Test JSON with invalid type (not dict or list) raises ValidationError."""
        mock_load_json.return_value = "invalid_type"  # String instead of dict/list

        with pytest.raises(ValidationError) as exc_info:
            load_test_data("test.json")

        assert "JSON file must contain a list or dictionary" in str(exc_info.value)

    @patch("pmas.data.readers.load_yaml")
    def test_load_test_data_when_yaml_invalid_type_expects_validation_error(
        self, mock_load_yaml
    ):
        """Test YAML with invalid type (not dict or list) raises ValidationError."""
        mock_load_yaml.return_value = 42  # Integer instead of dict/list

        with pytest.raises(ValidationError) as exc_info:
            load_test_data("test.yaml")

        assert "YAML file must contain a list or dictionary" in str(exc_info.value)

    @patch("pmas.data.readers.load_yaml")
    def test_load_test_data_when_yaml_dict_expects_list_conversion(
        self, mock_load_yaml
    ):
        """Test that YAML dict is converted to list."""
        mock_load_yaml.return_value = {"test": "data"}

        result = load_test_data("test.yaml")

        assert result == [{"test": "data"}]

    @patch("pmas.data.readers.load_yaml")
    def test_load_test_data_when_yaml_list_expects_unchanged(self, mock_load_yaml):
        """Test that YAML list is returned unchanged."""
        mock_load_yaml.return_value = [{"test": "data1"}, {"test": "data2"}]

        result = load_test_data("test.yaml")

        assert result == [{"test": "data1"}, {"test": "data2"}]

    @patch("pmas.data.readers.load_test_data")
    def test_get_data_when_filter_func_provided_expects_filtered_results(
        self, mock_load_test_data
    ):
        """Test DataProvider.get_data with filter function."""
        mock_load_test_data.return_value = [
            {"name": "test1", "active": True},
            {"name": "test2", "active": False},
            {"name": "test3", "active": True},
        ]

        provider = DataProvider("test_data")
        def filter_func(item):
            return item["active"]

        result = provider.get_data("test.csv", filter_func=filter_func)

        expected = [
            {"name": "test1", "active": True},
            {"name": "test3", "active": True},
        ]
        assert result == expected

    @patch("pmas.data.readers.load_test_data")
    def test_get_data_when_no_filter_func_expects_unfiltered_results(
        self, mock_load_test_data
    ):
        """Test DataProvider.get_data without filter function."""
        mock_load_test_data.return_value = [
            {"name": "test1", "active": True},
            {"name": "test2", "active": False},
        ]

        provider = DataProvider("test_data")

        result = provider.get_data("test.csv", filter_func=None)

        expected = [
            {"name": "test1", "active": True},
            {"name": "test2", "active": False},
        ]
        assert result == expected
