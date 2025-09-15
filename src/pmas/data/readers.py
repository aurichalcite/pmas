"""
Data readers for various file formats to support data-driven testing.
"""

import csv
import json
import logging
from collections.abc import Callable, Iterator
from pathlib import Path
from typing import Any

import yaml

from ..core.errors import ValidationError

logger = logging.getLogger(__name__)


def load_csv(
    file_path: str | Path,
    delimiter: str = ",",
    has_header: bool = True,
    encoding: str = "utf-8",
) -> list[dict[str, Any]]:
    """
    Load data from a CSV file.

    Args:
        file_path: Path to the CSV file
        delimiter: CSV delimiter character
        has_header: Whether the first row contains headers
        encoding: File encoding

    Returns:
        List of dictionaries representing rows

    Raises:
        ValidationError: If file cannot be read or parsed
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise ValidationError(f"CSV file not found: {file_path}")

    try:
        data = []
        with open(file_path, encoding=encoding, newline="") as csvfile:
            if has_header:
                reader = csv.DictReader(csvfile, delimiter=delimiter)
                for _row_num, row in enumerate(
                    reader, start=2
                ):  # Start at 2 because header is row 1
                    # Convert empty strings to None and try to convert numeric values
                    processed_row = {}
                    for key, value in row.items():
                        if value == "":
                            processed_row[key] = None
                        else:
                            processed_row[key] = _convert_value(value)
                    data.append(processed_row)
            else:
                reader = csv.reader(csvfile, delimiter=delimiter)
                headers = [f"column_{i}" for i in range(len(next(reader)))]
                csvfile.seek(0)  # Reset to beginning

                for _row_num, row in enumerate(reader, start=1):
                    processed_row = {}
                    for i, value in enumerate(row):
                        key = headers[i] if i < len(headers) else f"column_{i}"
                        processed_row[key] = (
                            _convert_value(value) if value != "" else None
                        )
                    data.append(processed_row)

        logger.debug(f"Loaded {len(data)} rows from CSV: {file_path}")
        return data

    except Exception as e:
        raise ValidationError(f"Failed to load CSV file {file_path}: {e}") from e


def load_json(
    file_path: str | Path, encoding: str = "utf-8"
) -> list[dict[str, Any]] | dict[str, Any]:
    """
    Load data from a JSON file.

    Args:
        file_path: Path to the JSON file
        encoding: File encoding

    Returns:
        Parsed JSON data (list or dictionary)

    Raises:
        ValidationError: If file cannot be read or parsed
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise ValidationError(f"JSON file not found: {file_path}")

    try:
        with open(file_path, encoding=encoding) as jsonfile:
            data = json.load(jsonfile)

        logger.debug(f"Loaded JSON data from: {file_path}")
        return data

    except json.JSONDecodeError as e:
        raise ValidationError(f"Invalid JSON in file {file_path}: {e}") from e
    except Exception as e:
        raise ValidationError(f"Failed to load JSON file {file_path}: {e}") from e


def load_yaml(
    file_path: str | Path, encoding: str = "utf-8"
) -> list[dict[str, Any]] | dict[str, Any]:
    """
    Load data from a YAML file.

    Args:
        file_path: Path to the YAML file
        encoding: File encoding

    Returns:
        Parsed YAML data (list or dictionary)

    Raises:
        ValidationError: If file cannot be read or parsed
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise ValidationError(f"YAML file not found: {file_path}")

    try:
        with open(file_path, encoding=encoding) as yamlfile:
            data = yaml.safe_load(yamlfile)

        logger.debug(f"Loaded YAML data from: {file_path}")
        return data

    except yaml.YAMLError as e:
        raise ValidationError(f"Invalid YAML in file {file_path}: {e}") from e
    except Exception as e:
        raise ValidationError(f"Failed to load YAML file {file_path}: {e}") from e


def _convert_value(value: str) -> Any:
    """
    Convert string value to appropriate Python type.

    Args:
        value: String value to convert

    Returns:
        Converted value (int, float, bool, or original string)
    """
    if not isinstance(value, str):
        return value

    # Try boolean conversion first
    if value.lower() in ("true", "false"):
        return value.lower() == "true"

    # Try integer conversion
    try:
        if "." not in value and "e" not in value.lower():
            return int(value)
    except ValueError:
        pass

    # Try float conversion
    try:
        return float(value)
    except ValueError:
        pass

    # Return as string
    return value


def load_test_data(
    file_path: str | Path, file_format: str | None = None
) -> list[dict[str, Any]]:
    """
    Load test data from a file, auto-detecting format if not specified.

    Args:
        file_path: Path to the data file
        file_format: File format ('csv', 'json', 'yaml'), auto-detected if None

    Returns:
        List of test data dictionaries

    Raises:
        ValidationError: If file format is unsupported or file cannot be loaded
    """
    file_path = Path(file_path)

    if file_format is None:
        file_format = file_path.suffix.lower().lstrip(".")

    if file_format == "csv":
        return load_csv(file_path)
    elif file_format in ("json", "js"):
        data = load_json(file_path)
        # Ensure we return a list
        if isinstance(data, dict):
            return [data]
        elif isinstance(data, list):
            return data
        else:
            raise ValidationError(
                f"JSON file must contain a list or dictionary: {file_path}"
            )
    elif file_format in ("yaml", "yml"):
        data = load_yaml(file_path)
        # Ensure we return a list
        if isinstance(data, dict):
            return [data]
        elif isinstance(data, list):
            return data
        else:
            raise ValidationError(
                f"YAML file must contain a list or dictionary: {file_path}"
            )
    else:
        raise ValidationError(f"Unsupported file format: {file_format}")


def parametrize_from_file(
    file_path: str | Path,
    id_field: str | None = None,
    filter_func: Callable | None = None,
) -> list[tuple[str, dict[str, Any]]]:
    """
    Load test data for pytest parametrization.

    Args:
        file_path: Path to the data file
        id_field: Field to use for test IDs (defaults to row index)
        filter_func: Optional function to filter test data

    Returns:
        List of (test_id, test_data) tuples for pytest.mark.parametrize
    """
    data = load_test_data(file_path)

    if filter_func:
        data = [item for item in data if filter_func(item)]

    parametrized_data = []
    for i, item in enumerate(data):
        if id_field and id_field in item:
            test_id = str(item[id_field])
        else:
            test_id = f"data_{i}"

        parametrized_data.append((test_id, item))

    logger.debug(f"Prepared {len(parametrized_data)} test cases from: {file_path}")
    return parametrized_data


def get_test_data_iterator(
    file_path: str | Path, chunk_size: int = 100
) -> Iterator[list[dict[str, Any]]]:
    """
    Get an iterator for large test data files to avoid loading everything into memory.

    Args:
        file_path: Path to the data file
        chunk_size: Number of records to load at a time

    Yields:
        Chunks of test data
    """
    file_path = Path(file_path)
    file_format = file_path.suffix.lower().lstrip(".")

    if file_format == "csv":
        yield from _csv_iterator(file_path, chunk_size)
    else:
        # For JSON/YAML, load all data and chunk it
        data = load_test_data(file_path)
        for i in range(0, len(data), chunk_size):
            yield data[i : i + chunk_size]


def _csv_iterator(file_path: Path, chunk_size: int) -> Iterator[list[dict[str, Any]]]:
    """Iterator for CSV files to process in chunks."""
    try:
        with open(file_path, encoding="utf-8", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            chunk = []

            for row in reader:
                # Process row
                processed_row = {}
                for key, value in row.items():
                    if value == "":
                        processed_row[key] = None
                    else:
                        processed_row[key] = _convert_value(value)

                chunk.append(processed_row)

                if len(chunk) >= chunk_size:
                    yield chunk
                    chunk = []

            # Yield remaining data
            if chunk:
                yield chunk

    except Exception as e:
        raise ValidationError(f"Failed to iterate CSV file {file_path}: {e}") from e


class DataProvider:
    """
    Data provider class for managing test data from multiple sources.
    """

    def __init__(self, data_dir: str | Path = "test_data") -> None:
        self.data_dir = Path(data_dir)
        self._cache: dict[str, list[dict[str, Any]]] = {}

    def get_data(
        self, filename: str, use_cache: bool = True, filter_func: Callable | None = None
    ) -> list[dict[str, Any]]:
        """
        Get test data from a file.

        Args:
            filename: Name of the data file
            use_cache: Whether to use cached data
            filter_func: Optional function to filter data

        Returns:
            List of test data dictionaries
        """
        file_path = self.data_dir / filename
        cache_key = str(file_path)

        if use_cache and cache_key in self._cache:
            data = self._cache[cache_key]
        else:
            data = load_test_data(file_path)
            if use_cache:
                self._cache[cache_key] = data

        if filter_func:
            data = [item for item in data if filter_func(item)]

        return data

    def get_parametrized_data(
        self,
        filename: str,
        id_field: str | None = None,
        filter_func: Callable | None = None,
    ) -> list[tuple[str, dict[str, Any]]]:
        """Get parametrized test data for pytest."""
        data = self.get_data(filename, filter_func=filter_func)

        parametrized_data = []
        for i, item in enumerate(data):
            if id_field and id_field in item:
                test_id = str(item[id_field])
            else:
                test_id = f"data_{i}"

            parametrized_data.append((test_id, item))

        return parametrized_data

    def clear_cache(self) -> None:
        """Clear the data cache."""
        self._cache.clear()

    def list_data_files(self) -> list[Path]:
        """List all data files in the data directory."""
        if not self.data_dir.exists():
            return []

        supported_extensions = {".csv", ".json", ".yaml", ".yml"}
        return [
            f
            for f in self.data_dir.iterdir()
            if f.is_file() and f.suffix.lower() in supported_extensions
        ]


# Convenience functions for pytest parametrization
def pytest_param_from_csv(file_path: str | Path, **kwargs) -> list:
    """Create pytest parameters from CSV file."""
    import pytest

    data = parametrize_from_file(file_path, **kwargs)
    return [pytest.param(item[1], id=item[0]) for item in data]


def pytest_param_from_json(file_path: str | Path, **kwargs) -> list:
    """Create pytest parameters from JSON file."""
    import pytest

    data = parametrize_from_file(file_path, **kwargs)
    return [pytest.param(item[1], id=item[0]) for item in data]


def pytest_param_from_yaml(file_path: str | Path, **kwargs) -> list:
    """Create pytest parameters from YAML file."""
    import pytest

    data = parametrize_from_file(file_path, **kwargs)
    return [pytest.param(item[1], id=item[0]) for item in data]
