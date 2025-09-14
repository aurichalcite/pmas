"""
File and path utilities for the testing framework.
"""

import logging
import shutil
import tempfile
from pathlib import Path

logger = logging.getLogger(__name__)


def ensure_directory(path: str | Path) -> Path:
    """
    Ensure a directory exists, creating it if necessary.

    Args:
        path: Directory path to ensure exists

    Returns:
        Path object for the directory
    """
    dir_path = Path(path)
    dir_path.mkdir(parents=True, exist_ok=True)
    logger.debug(f"Ensured directory exists: {dir_path}")
    return dir_path


def clean_directory(path: str | Path, keep_directory: bool = True) -> None:
    """
    Clean all contents from a directory.

    Args:
        path: Directory path to clean
        keep_directory: Whether to keep the directory itself
    """
    dir_path = Path(path)
    if not dir_path.exists():
        return

    if dir_path.is_file():
        dir_path.unlink()
        logger.debug(f"Removed file: {dir_path}")
        return

    for item in dir_path.iterdir():
        if item.is_file():
            item.unlink()
        elif item.is_dir():
            shutil.rmtree(item)

    if not keep_directory:
        dir_path.rmdir()
        logger.debug(f"Removed directory: {dir_path}")
    else:
        logger.debug(f"Cleaned directory: {dir_path}")


def copy_file(source: str | Path, destination: str | Path) -> Path:
    """
    Copy a file to a destination.

    Args:
        source: Source file path
        destination: Destination file path

    Returns:
        Path to the copied file
    """
    source_path = Path(source)
    dest_path = Path(destination)

    # Ensure destination directory exists
    dest_path.parent.mkdir(parents=True, exist_ok=True)

    shutil.copy2(source_path, dest_path)
    logger.debug(f"Copied file: {source_path} -> {dest_path}")
    return dest_path


def find_files(
    directory: str | Path, pattern: str = "*", recursive: bool = True
) -> list[Path]:
    """
    Find files matching a pattern in a directory.

    Args:
        directory: Directory to search in
        pattern: Glob pattern to match
        recursive: Whether to search recursively

    Returns:
        List of matching file paths
    """
    dir_path = Path(directory)
    if not dir_path.exists():
        return []

    if recursive:
        files = list(dir_path.rglob(pattern))
    else:
        files = list(dir_path.glob(pattern))

    # Filter to only files (not directories)
    files = [f for f in files if f.is_file()]
    logger.debug(f"Found {len(files)} files matching '{pattern}' in {dir_path}")
    return files


def get_file_size(path: str | Path) -> int:
    """
    Get the size of a file in bytes.

    Args:
        path: File path

    Returns:
        File size in bytes
    """
    file_path = Path(path)
    if not file_path.exists():
        return 0
    return file_path.stat().st_size


def is_file_empty(path: str | Path) -> bool:
    """
    Check if a file is empty.

    Args:
        path: File path

    Returns:
        True if file is empty or doesn't exist
    """
    return get_file_size(path) == 0


def backup_file(path: str | Path, backup_suffix: str = ".bak") -> Path | None:
    """
    Create a backup copy of a file.

    Args:
        path: File path to backup
        backup_suffix: Suffix to add to backup file

    Returns:
        Path to backup file, or None if original doesn't exist
    """
    file_path = Path(path)
    if not file_path.exists():
        return None

    backup_path = file_path.with_suffix(file_path.suffix + backup_suffix)
    shutil.copy2(file_path, backup_path)
    logger.debug(f"Created backup: {file_path} -> {backup_path}")
    return backup_path


def safe_filename(filename: str, replacement: str = "_") -> str:
    """
    Make a filename safe for the filesystem by replacing invalid characters.

    Args:
        filename: Original filename
        replacement: Character to replace invalid characters with

    Returns:
        Safe filename
    """
    # Characters that are invalid in filenames on most systems
    invalid_chars = '<>:"/\\|?*'
    safe_name = filename

    for char in invalid_chars:
        safe_name = safe_name.replace(char, replacement)

    # Remove leading/trailing whitespace and dots
    safe_name = safe_name.strip(". ")

    # Ensure it's not empty
    if not safe_name:
        safe_name = "unnamed"

    return safe_name


def get_unique_filename(path: str | Path) -> Path:
    """
    Get a unique filename by appending a number if the file already exists.

    Args:
        path: Desired file path

    Returns:
        Unique file path
    """
    file_path = Path(path)
    if not file_path.exists():
        return file_path

    stem = file_path.stem
    suffix = file_path.suffix
    parent = file_path.parent

    counter = 1
    while True:
        new_name = f"{stem}_{counter}{suffix}"
        new_path = parent / new_name
        if not new_path.exists():
            return new_path
        counter += 1


class TemporaryDirectory:
    """Context manager for creating and cleaning up temporary directories."""

    def __init__(self, prefix: str = "pmas_test_", cleanup: bool = True) -> None:
        self.prefix = prefix
        self.cleanup = cleanup
        self.path: Path | None = None

    def __enter__(self) -> Path:
        self.path = Path(tempfile.mkdtemp(prefix=self.prefix))
        logger.debug(f"Created temporary directory: {self.path}")
        return self.path

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self.cleanup and self.path and self.path.exists():
            shutil.rmtree(self.path)
            logger.debug(f"Cleaned up temporary directory: {self.path}")


def read_file_lines(path: str | Path, encoding: str = "utf-8") -> list[str]:
    """
    Read all lines from a file.

    Args:
        path: File path
        encoding: File encoding

    Returns:
        List of lines from the file
    """
    file_path = Path(path)
    try:
        with file_path.open("r", encoding=encoding) as f:
            return f.readlines()
    except FileNotFoundError:
        logger.warning(f"File not found: {file_path}")
        return []
    except UnicodeDecodeError as e:
        logger.error(f"Failed to decode file {file_path}: {e}")
        return []


def write_file_lines(
    path: str | Path, lines: list[str], encoding: str = "utf-8"
) -> None:
    """
    Write lines to a file.

    Args:
        path: File path
        lines: Lines to write
        encoding: File encoding
    """
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with file_path.open("w", encoding=encoding) as f:
        f.writelines(lines)

    logger.debug(f"Wrote {len(lines)} lines to {file_path}")


def tail_file(path: str | Path, num_lines: int = 10) -> list[str]:
    """
    Get the last N lines from a file (like Unix tail command).

    Args:
        path: File path
        num_lines: Number of lines to return

    Returns:
        List of last N lines
    """
    lines = read_file_lines(path)
    return lines[-num_lines:] if lines else []
