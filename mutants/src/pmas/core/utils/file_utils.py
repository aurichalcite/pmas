"""
File and path utilities for the testing framework.
"""

import logging
import shutil
import tempfile
from pathlib import Path

logger = logging.getLogger(__name__)
from collections.abc import Callable
from inspect import signature as _mutmut_signature
from typing import Annotated, ClassVar

MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg=None):
    """Forward call to original or mutated function, depending on the environment"""
    import os

    mutant_under_test = os.environ["MUTANT_UNDER_TEST"]
    if mutant_under_test == "fail":
        from mutmut.__main__ import MutmutProgrammaticFailException

        raise MutmutProgrammaticFailException("Failed programmatically")
    elif mutant_under_test == "stats":
        from mutmut.__main__ import record_trampoline_hit

        record_trampoline_hit(orig.__module__ + "." + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + "." + orig.__name__ + "__mutmut_"
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition(".")[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


def x_ensure_directory__mutmut_orig(path: str | Path) -> Path:
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


def x_ensure_directory__mutmut_1(path: str | Path) -> Path:
    """
    Ensure a directory exists, creating it if necessary.

    Args:
        path: Directory path to ensure exists

    Returns:
        Path object for the directory
    """
    dir_path = None
    dir_path.mkdir(parents=True, exist_ok=True)
    logger.debug(f"Ensured directory exists: {dir_path}")
    return dir_path


def x_ensure_directory__mutmut_2(path: str | Path) -> Path:
    """
    Ensure a directory exists, creating it if necessary.

    Args:
        path: Directory path to ensure exists

    Returns:
        Path object for the directory
    """
    dir_path = Path(None)
    dir_path.mkdir(parents=True, exist_ok=True)
    logger.debug(f"Ensured directory exists: {dir_path}")
    return dir_path


def x_ensure_directory__mutmut_3(path: str | Path) -> Path:
    """
    Ensure a directory exists, creating it if necessary.

    Args:
        path: Directory path to ensure exists

    Returns:
        Path object for the directory
    """
    dir_path = Path(path)
    dir_path.mkdir(parents=None, exist_ok=True)
    logger.debug(f"Ensured directory exists: {dir_path}")
    return dir_path


def x_ensure_directory__mutmut_4(path: str | Path) -> Path:
    """
    Ensure a directory exists, creating it if necessary.

    Args:
        path: Directory path to ensure exists

    Returns:
        Path object for the directory
    """
    dir_path = Path(path)
    dir_path.mkdir(parents=True, exist_ok=None)
    logger.debug(f"Ensured directory exists: {dir_path}")
    return dir_path


def x_ensure_directory__mutmut_5(path: str | Path) -> Path:
    """
    Ensure a directory exists, creating it if necessary.

    Args:
        path: Directory path to ensure exists

    Returns:
        Path object for the directory
    """
    dir_path = Path(path)
    dir_path.mkdir(exist_ok=True)
    logger.debug(f"Ensured directory exists: {dir_path}")
    return dir_path


def x_ensure_directory__mutmut_6(path: str | Path) -> Path:
    """
    Ensure a directory exists, creating it if necessary.

    Args:
        path: Directory path to ensure exists

    Returns:
        Path object for the directory
    """
    dir_path = Path(path)
    dir_path.mkdir(
        parents=True,
    )
    logger.debug(f"Ensured directory exists: {dir_path}")
    return dir_path


def x_ensure_directory__mutmut_7(path: str | Path) -> Path:
    """
    Ensure a directory exists, creating it if necessary.

    Args:
        path: Directory path to ensure exists

    Returns:
        Path object for the directory
    """
    dir_path = Path(path)
    dir_path.mkdir(parents=False, exist_ok=True)
    logger.debug(f"Ensured directory exists: {dir_path}")
    return dir_path


def x_ensure_directory__mutmut_8(path: str | Path) -> Path:
    """
    Ensure a directory exists, creating it if necessary.

    Args:
        path: Directory path to ensure exists

    Returns:
        Path object for the directory
    """
    dir_path = Path(path)
    dir_path.mkdir(parents=True, exist_ok=False)
    logger.debug(f"Ensured directory exists: {dir_path}")
    return dir_path


def x_ensure_directory__mutmut_9(path: str | Path) -> Path:
    """
    Ensure a directory exists, creating it if necessary.

    Args:
        path: Directory path to ensure exists

    Returns:
        Path object for the directory
    """
    dir_path = Path(path)
    dir_path.mkdir(parents=True, exist_ok=True)
    logger.debug(None)
    return dir_path


x_ensure_directory__mutmut_mutants: ClassVar[MutantDict] = {
    "x_ensure_directory__mutmut_1": x_ensure_directory__mutmut_1,
    "x_ensure_directory__mutmut_2": x_ensure_directory__mutmut_2,
    "x_ensure_directory__mutmut_3": x_ensure_directory__mutmut_3,
    "x_ensure_directory__mutmut_4": x_ensure_directory__mutmut_4,
    "x_ensure_directory__mutmut_5": x_ensure_directory__mutmut_5,
    "x_ensure_directory__mutmut_6": x_ensure_directory__mutmut_6,
    "x_ensure_directory__mutmut_7": x_ensure_directory__mutmut_7,
    "x_ensure_directory__mutmut_8": x_ensure_directory__mutmut_8,
    "x_ensure_directory__mutmut_9": x_ensure_directory__mutmut_9,
}


def ensure_directory(*args, **kwargs):
    result = _mutmut_trampoline(
        x_ensure_directory__mutmut_orig,
        x_ensure_directory__mutmut_mutants,
        args,
        kwargs,
    )
    return result


ensure_directory.__signature__ = _mutmut_signature(x_ensure_directory__mutmut_orig)
x_ensure_directory__mutmut_orig.__name__ = "x_ensure_directory"


def x_clean_directory__mutmut_orig(
    path: str | Path, keep_directory: bool = True
) -> None:
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


def x_clean_directory__mutmut_1(path: str | Path, keep_directory: bool = False) -> None:
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


def x_clean_directory__mutmut_2(path: str | Path, keep_directory: bool = True) -> None:
    """
    Clean all contents from a directory.

    Args:
        path: Directory path to clean
        keep_directory: Whether to keep the directory itself
    """
    dir_path = None
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


def x_clean_directory__mutmut_3(path: str | Path, keep_directory: bool = True) -> None:
    """
    Clean all contents from a directory.

    Args:
        path: Directory path to clean
        keep_directory: Whether to keep the directory itself
    """
    dir_path = Path(None)
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


def x_clean_directory__mutmut_4(path: str | Path, keep_directory: bool = True) -> None:
    """
    Clean all contents from a directory.

    Args:
        path: Directory path to clean
        keep_directory: Whether to keep the directory itself
    """
    dir_path = Path(path)
    if dir_path.exists():
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


def x_clean_directory__mutmut_5(path: str | Path, keep_directory: bool = True) -> None:
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
        logger.debug(None)
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


def x_clean_directory__mutmut_6(path: str | Path, keep_directory: bool = True) -> None:
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
            shutil.rmtree(None)

    if not keep_directory:
        dir_path.rmdir()
        logger.debug(f"Removed directory: {dir_path}")
    else:
        logger.debug(f"Cleaned directory: {dir_path}")


def x_clean_directory__mutmut_7(path: str | Path, keep_directory: bool = True) -> None:
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

    if keep_directory:
        dir_path.rmdir()
        logger.debug(f"Removed directory: {dir_path}")
    else:
        logger.debug(f"Cleaned directory: {dir_path}")


def x_clean_directory__mutmut_8(path: str | Path, keep_directory: bool = True) -> None:
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
        logger.debug(None)
    else:
        logger.debug(f"Cleaned directory: {dir_path}")


def x_clean_directory__mutmut_9(path: str | Path, keep_directory: bool = True) -> None:
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
        logger.debug(None)


x_clean_directory__mutmut_mutants: ClassVar[MutantDict] = {
    "x_clean_directory__mutmut_1": x_clean_directory__mutmut_1,
    "x_clean_directory__mutmut_2": x_clean_directory__mutmut_2,
    "x_clean_directory__mutmut_3": x_clean_directory__mutmut_3,
    "x_clean_directory__mutmut_4": x_clean_directory__mutmut_4,
    "x_clean_directory__mutmut_5": x_clean_directory__mutmut_5,
    "x_clean_directory__mutmut_6": x_clean_directory__mutmut_6,
    "x_clean_directory__mutmut_7": x_clean_directory__mutmut_7,
    "x_clean_directory__mutmut_8": x_clean_directory__mutmut_8,
    "x_clean_directory__mutmut_9": x_clean_directory__mutmut_9,
}


def clean_directory(*args, **kwargs):
    result = _mutmut_trampoline(
        x_clean_directory__mutmut_orig, x_clean_directory__mutmut_mutants, args, kwargs
    )
    return result


clean_directory.__signature__ = _mutmut_signature(x_clean_directory__mutmut_orig)
x_clean_directory__mutmut_orig.__name__ = "x_clean_directory"


def x_copy_file__mutmut_orig(source: str | Path, destination: str | Path) -> Path:
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


def x_copy_file__mutmut_1(source: str | Path, destination: str | Path) -> Path:
    """
    Copy a file to a destination.

    Args:
        source: Source file path
        destination: Destination file path

    Returns:
        Path to the copied file
    """
    source_path = None
    dest_path = Path(destination)

    # Ensure destination directory exists
    dest_path.parent.mkdir(parents=True, exist_ok=True)

    shutil.copy2(source_path, dest_path)
    logger.debug(f"Copied file: {source_path} -> {dest_path}")
    return dest_path


def x_copy_file__mutmut_2(source: str | Path, destination: str | Path) -> Path:
    """
    Copy a file to a destination.

    Args:
        source: Source file path
        destination: Destination file path

    Returns:
        Path to the copied file
    """
    source_path = Path(None)
    dest_path = Path(destination)

    # Ensure destination directory exists
    dest_path.parent.mkdir(parents=True, exist_ok=True)

    shutil.copy2(source_path, dest_path)
    logger.debug(f"Copied file: {source_path} -> {dest_path}")
    return dest_path


def x_copy_file__mutmut_3(source: str | Path, destination: str | Path) -> Path:
    """
    Copy a file to a destination.

    Args:
        source: Source file path
        destination: Destination file path

    Returns:
        Path to the copied file
    """
    source_path = Path(source)
    dest_path = None

    # Ensure destination directory exists
    dest_path.parent.mkdir(parents=True, exist_ok=True)

    shutil.copy2(source_path, dest_path)
    logger.debug(f"Copied file: {source_path} -> {dest_path}")
    return dest_path


def x_copy_file__mutmut_4(source: str | Path, destination: str | Path) -> Path:
    """
    Copy a file to a destination.

    Args:
        source: Source file path
        destination: Destination file path

    Returns:
        Path to the copied file
    """
    source_path = Path(source)
    dest_path = Path(None)

    # Ensure destination directory exists
    dest_path.parent.mkdir(parents=True, exist_ok=True)

    shutil.copy2(source_path, dest_path)
    logger.debug(f"Copied file: {source_path} -> {dest_path}")
    return dest_path


def x_copy_file__mutmut_5(source: str | Path, destination: str | Path) -> Path:
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
    dest_path.parent.mkdir(parents=None, exist_ok=True)

    shutil.copy2(source_path, dest_path)
    logger.debug(f"Copied file: {source_path} -> {dest_path}")
    return dest_path


def x_copy_file__mutmut_6(source: str | Path, destination: str | Path) -> Path:
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
    dest_path.parent.mkdir(parents=True, exist_ok=None)

    shutil.copy2(source_path, dest_path)
    logger.debug(f"Copied file: {source_path} -> {dest_path}")
    return dest_path


def x_copy_file__mutmut_7(source: str | Path, destination: str | Path) -> Path:
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
    dest_path.parent.mkdir(exist_ok=True)

    shutil.copy2(source_path, dest_path)
    logger.debug(f"Copied file: {source_path} -> {dest_path}")
    return dest_path


def x_copy_file__mutmut_8(source: str | Path, destination: str | Path) -> Path:
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
    dest_path.parent.mkdir(
        parents=True,
    )

    shutil.copy2(source_path, dest_path)
    logger.debug(f"Copied file: {source_path} -> {dest_path}")
    return dest_path


def x_copy_file__mutmut_9(source: str | Path, destination: str | Path) -> Path:
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
    dest_path.parent.mkdir(parents=False, exist_ok=True)

    shutil.copy2(source_path, dest_path)
    logger.debug(f"Copied file: {source_path} -> {dest_path}")
    return dest_path


def x_copy_file__mutmut_10(source: str | Path, destination: str | Path) -> Path:
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
    dest_path.parent.mkdir(parents=True, exist_ok=False)

    shutil.copy2(source_path, dest_path)
    logger.debug(f"Copied file: {source_path} -> {dest_path}")
    return dest_path


def x_copy_file__mutmut_11(source: str | Path, destination: str | Path) -> Path:
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

    shutil.copy2(None, dest_path)
    logger.debug(f"Copied file: {source_path} -> {dest_path}")
    return dest_path


def x_copy_file__mutmut_12(source: str | Path, destination: str | Path) -> Path:
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

    shutil.copy2(source_path, None)
    logger.debug(f"Copied file: {source_path} -> {dest_path}")
    return dest_path


def x_copy_file__mutmut_13(source: str | Path, destination: str | Path) -> Path:
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

    shutil.copy2(dest_path)
    logger.debug(f"Copied file: {source_path} -> {dest_path}")
    return dest_path


def x_copy_file__mutmut_14(source: str | Path, destination: str | Path) -> Path:
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

    shutil.copy2(
        source_path,
    )
    logger.debug(f"Copied file: {source_path} -> {dest_path}")
    return dest_path


def x_copy_file__mutmut_15(source: str | Path, destination: str | Path) -> Path:
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
    logger.debug(None)
    return dest_path


x_copy_file__mutmut_mutants: ClassVar[MutantDict] = {
    "x_copy_file__mutmut_1": x_copy_file__mutmut_1,
    "x_copy_file__mutmut_2": x_copy_file__mutmut_2,
    "x_copy_file__mutmut_3": x_copy_file__mutmut_3,
    "x_copy_file__mutmut_4": x_copy_file__mutmut_4,
    "x_copy_file__mutmut_5": x_copy_file__mutmut_5,
    "x_copy_file__mutmut_6": x_copy_file__mutmut_6,
    "x_copy_file__mutmut_7": x_copy_file__mutmut_7,
    "x_copy_file__mutmut_8": x_copy_file__mutmut_8,
    "x_copy_file__mutmut_9": x_copy_file__mutmut_9,
    "x_copy_file__mutmut_10": x_copy_file__mutmut_10,
    "x_copy_file__mutmut_11": x_copy_file__mutmut_11,
    "x_copy_file__mutmut_12": x_copy_file__mutmut_12,
    "x_copy_file__mutmut_13": x_copy_file__mutmut_13,
    "x_copy_file__mutmut_14": x_copy_file__mutmut_14,
    "x_copy_file__mutmut_15": x_copy_file__mutmut_15,
}


def copy_file(*args, **kwargs):
    result = _mutmut_trampoline(
        x_copy_file__mutmut_orig, x_copy_file__mutmut_mutants, args, kwargs
    )
    return result


copy_file.__signature__ = _mutmut_signature(x_copy_file__mutmut_orig)
x_copy_file__mutmut_orig.__name__ = "x_copy_file"


def x_find_files__mutmut_orig(
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


def x_find_files__mutmut_1(
    directory: str | Path, pattern: str = "XX*XX", recursive: bool = True
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


def x_find_files__mutmut_2(
    directory: str | Path, pattern: str = "*", recursive: bool = False
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


def x_find_files__mutmut_3(
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
    dir_path = None
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


def x_find_files__mutmut_4(
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
    dir_path = Path(None)
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


def x_find_files__mutmut_5(
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
    if dir_path.exists():
        return []

    if recursive:
        files = list(dir_path.rglob(pattern))
    else:
        files = list(dir_path.glob(pattern))

    # Filter to only files (not directories)
    files = [f for f in files if f.is_file()]
    logger.debug(f"Found {len(files)} files matching '{pattern}' in {dir_path}")
    return files


def x_find_files__mutmut_6(
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
        files = None
    else:
        files = list(dir_path.glob(pattern))

    # Filter to only files (not directories)
    files = [f for f in files if f.is_file()]
    logger.debug(f"Found {len(files)} files matching '{pattern}' in {dir_path}")
    return files


def x_find_files__mutmut_7(
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
        files = list(None)
    else:
        files = list(dir_path.glob(pattern))

    # Filter to only files (not directories)
    files = [f for f in files if f.is_file()]
    logger.debug(f"Found {len(files)} files matching '{pattern}' in {dir_path}")
    return files


def x_find_files__mutmut_8(
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
        files = list(dir_path.rglob(None))
    else:
        files = list(dir_path.glob(pattern))

    # Filter to only files (not directories)
    files = [f for f in files if f.is_file()]
    logger.debug(f"Found {len(files)} files matching '{pattern}' in {dir_path}")
    return files


def x_find_files__mutmut_9(
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
        files = None

    # Filter to only files (not directories)
    files = [f for f in files if f.is_file()]
    logger.debug(f"Found {len(files)} files matching '{pattern}' in {dir_path}")
    return files


def x_find_files__mutmut_10(
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
        files = list(None)

    # Filter to only files (not directories)
    files = [f for f in files if f.is_file()]
    logger.debug(f"Found {len(files)} files matching '{pattern}' in {dir_path}")
    return files


def x_find_files__mutmut_11(
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
        files = list(dir_path.glob(None))

    # Filter to only files (not directories)
    files = [f for f in files if f.is_file()]
    logger.debug(f"Found {len(files)} files matching '{pattern}' in {dir_path}")
    return files


def x_find_files__mutmut_12(
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
    files = None
    logger.debug(f"Found {len(files)} files matching '{pattern}' in {dir_path}")
    return files


def x_find_files__mutmut_13(
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
    logger.debug(None)
    return files


x_find_files__mutmut_mutants: ClassVar[MutantDict] = {
    "x_find_files__mutmut_1": x_find_files__mutmut_1,
    "x_find_files__mutmut_2": x_find_files__mutmut_2,
    "x_find_files__mutmut_3": x_find_files__mutmut_3,
    "x_find_files__mutmut_4": x_find_files__mutmut_4,
    "x_find_files__mutmut_5": x_find_files__mutmut_5,
    "x_find_files__mutmut_6": x_find_files__mutmut_6,
    "x_find_files__mutmut_7": x_find_files__mutmut_7,
    "x_find_files__mutmut_8": x_find_files__mutmut_8,
    "x_find_files__mutmut_9": x_find_files__mutmut_9,
    "x_find_files__mutmut_10": x_find_files__mutmut_10,
    "x_find_files__mutmut_11": x_find_files__mutmut_11,
    "x_find_files__mutmut_12": x_find_files__mutmut_12,
    "x_find_files__mutmut_13": x_find_files__mutmut_13,
}


def find_files(*args, **kwargs):
    result = _mutmut_trampoline(
        x_find_files__mutmut_orig, x_find_files__mutmut_mutants, args, kwargs
    )
    return result


find_files.__signature__ = _mutmut_signature(x_find_files__mutmut_orig)
x_find_files__mutmut_orig.__name__ = "x_find_files"


def x_get_file_size__mutmut_orig(path: str | Path) -> int:
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


def x_get_file_size__mutmut_1(path: str | Path) -> int:
    """
    Get the size of a file in bytes.

    Args:
        path: File path

    Returns:
        File size in bytes
    """
    file_path = None
    if not file_path.exists():
        return 0
    return file_path.stat().st_size


def x_get_file_size__mutmut_2(path: str | Path) -> int:
    """
    Get the size of a file in bytes.

    Args:
        path: File path

    Returns:
        File size in bytes
    """
    file_path = Path(None)
    if not file_path.exists():
        return 0
    return file_path.stat().st_size


def x_get_file_size__mutmut_3(path: str | Path) -> int:
    """
    Get the size of a file in bytes.

    Args:
        path: File path

    Returns:
        File size in bytes
    """
    file_path = Path(path)
    if file_path.exists():
        return 0
    return file_path.stat().st_size


def x_get_file_size__mutmut_4(path: str | Path) -> int:
    """
    Get the size of a file in bytes.

    Args:
        path: File path

    Returns:
        File size in bytes
    """
    file_path = Path(path)
    if not file_path.exists():
        return 1
    return file_path.stat().st_size


x_get_file_size__mutmut_mutants: ClassVar[MutantDict] = {
    "x_get_file_size__mutmut_1": x_get_file_size__mutmut_1,
    "x_get_file_size__mutmut_2": x_get_file_size__mutmut_2,
    "x_get_file_size__mutmut_3": x_get_file_size__mutmut_3,
    "x_get_file_size__mutmut_4": x_get_file_size__mutmut_4,
}


def get_file_size(*args, **kwargs):
    result = _mutmut_trampoline(
        x_get_file_size__mutmut_orig, x_get_file_size__mutmut_mutants, args, kwargs
    )
    return result


get_file_size.__signature__ = _mutmut_signature(x_get_file_size__mutmut_orig)
x_get_file_size__mutmut_orig.__name__ = "x_get_file_size"


def x_is_file_empty__mutmut_orig(path: str | Path) -> bool:
    """
    Check if a file is empty.

    Args:
        path: File path

    Returns:
        True if file is empty or doesn't exist
    """
    return get_file_size(path) == 0


def x_is_file_empty__mutmut_1(path: str | Path) -> bool:
    """
    Check if a file is empty.

    Args:
        path: File path

    Returns:
        True if file is empty or doesn't exist
    """
    return get_file_size(None) == 0


def x_is_file_empty__mutmut_2(path: str | Path) -> bool:
    """
    Check if a file is empty.

    Args:
        path: File path

    Returns:
        True if file is empty or doesn't exist
    """
    return get_file_size(path) != 0


def x_is_file_empty__mutmut_3(path: str | Path) -> bool:
    """
    Check if a file is empty.

    Args:
        path: File path

    Returns:
        True if file is empty or doesn't exist
    """
    return get_file_size(path) == 1


x_is_file_empty__mutmut_mutants: ClassVar[MutantDict] = {
    "x_is_file_empty__mutmut_1": x_is_file_empty__mutmut_1,
    "x_is_file_empty__mutmut_2": x_is_file_empty__mutmut_2,
    "x_is_file_empty__mutmut_3": x_is_file_empty__mutmut_3,
}


def is_file_empty(*args, **kwargs):
    result = _mutmut_trampoline(
        x_is_file_empty__mutmut_orig, x_is_file_empty__mutmut_mutants, args, kwargs
    )
    return result


is_file_empty.__signature__ = _mutmut_signature(x_is_file_empty__mutmut_orig)
x_is_file_empty__mutmut_orig.__name__ = "x_is_file_empty"


def x_backup_file__mutmut_orig(
    path: str | Path, backup_suffix: str = ".bak"
) -> Path | None:
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


def x_backup_file__mutmut_1(
    path: str | Path, backup_suffix: str = "XX.bakXX"
) -> Path | None:
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


def x_backup_file__mutmut_2(
    path: str | Path, backup_suffix: str = ".BAK"
) -> Path | None:
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


def x_backup_file__mutmut_3(
    path: str | Path, backup_suffix: str = ".bak"
) -> Path | None:
    """
    Create a backup copy of a file.

    Args:
        path: File path to backup
        backup_suffix: Suffix to add to backup file

    Returns:
        Path to backup file, or None if original doesn't exist
    """
    file_path = None
    if not file_path.exists():
        return None

    backup_path = file_path.with_suffix(file_path.suffix + backup_suffix)
    shutil.copy2(file_path, backup_path)
    logger.debug(f"Created backup: {file_path} -> {backup_path}")
    return backup_path


def x_backup_file__mutmut_4(
    path: str | Path, backup_suffix: str = ".bak"
) -> Path | None:
    """
    Create a backup copy of a file.

    Args:
        path: File path to backup
        backup_suffix: Suffix to add to backup file

    Returns:
        Path to backup file, or None if original doesn't exist
    """
    file_path = Path(None)
    if not file_path.exists():
        return None

    backup_path = file_path.with_suffix(file_path.suffix + backup_suffix)
    shutil.copy2(file_path, backup_path)
    logger.debug(f"Created backup: {file_path} -> {backup_path}")
    return backup_path


def x_backup_file__mutmut_5(
    path: str | Path, backup_suffix: str = ".bak"
) -> Path | None:
    """
    Create a backup copy of a file.

    Args:
        path: File path to backup
        backup_suffix: Suffix to add to backup file

    Returns:
        Path to backup file, or None if original doesn't exist
    """
    file_path = Path(path)
    if file_path.exists():
        return None

    backup_path = file_path.with_suffix(file_path.suffix + backup_suffix)
    shutil.copy2(file_path, backup_path)
    logger.debug(f"Created backup: {file_path} -> {backup_path}")
    return backup_path


def x_backup_file__mutmut_6(
    path: str | Path, backup_suffix: str = ".bak"
) -> Path | None:
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

    backup_path = None
    shutil.copy2(file_path, backup_path)
    logger.debug(f"Created backup: {file_path} -> {backup_path}")
    return backup_path


def x_backup_file__mutmut_7(
    path: str | Path, backup_suffix: str = ".bak"
) -> Path | None:
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

    backup_path = file_path.with_suffix(None)
    shutil.copy2(file_path, backup_path)
    logger.debug(f"Created backup: {file_path} -> {backup_path}")
    return backup_path


def x_backup_file__mutmut_8(
    path: str | Path, backup_suffix: str = ".bak"
) -> Path | None:
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

    backup_path = file_path.with_suffix(file_path.suffix - backup_suffix)
    shutil.copy2(file_path, backup_path)
    logger.debug(f"Created backup: {file_path} -> {backup_path}")
    return backup_path


def x_backup_file__mutmut_9(
    path: str | Path, backup_suffix: str = ".bak"
) -> Path | None:
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
    shutil.copy2(None, backup_path)
    logger.debug(f"Created backup: {file_path} -> {backup_path}")
    return backup_path


def x_backup_file__mutmut_10(
    path: str | Path, backup_suffix: str = ".bak"
) -> Path | None:
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
    shutil.copy2(file_path, None)
    logger.debug(f"Created backup: {file_path} -> {backup_path}")
    return backup_path


def x_backup_file__mutmut_11(
    path: str | Path, backup_suffix: str = ".bak"
) -> Path | None:
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
    shutil.copy2(backup_path)
    logger.debug(f"Created backup: {file_path} -> {backup_path}")
    return backup_path


def x_backup_file__mutmut_12(
    path: str | Path, backup_suffix: str = ".bak"
) -> Path | None:
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
    shutil.copy2(
        file_path,
    )
    logger.debug(f"Created backup: {file_path} -> {backup_path}")
    return backup_path


def x_backup_file__mutmut_13(
    path: str | Path, backup_suffix: str = ".bak"
) -> Path | None:
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
    logger.debug(None)
    return backup_path


x_backup_file__mutmut_mutants: ClassVar[MutantDict] = {
    "x_backup_file__mutmut_1": x_backup_file__mutmut_1,
    "x_backup_file__mutmut_2": x_backup_file__mutmut_2,
    "x_backup_file__mutmut_3": x_backup_file__mutmut_3,
    "x_backup_file__mutmut_4": x_backup_file__mutmut_4,
    "x_backup_file__mutmut_5": x_backup_file__mutmut_5,
    "x_backup_file__mutmut_6": x_backup_file__mutmut_6,
    "x_backup_file__mutmut_7": x_backup_file__mutmut_7,
    "x_backup_file__mutmut_8": x_backup_file__mutmut_8,
    "x_backup_file__mutmut_9": x_backup_file__mutmut_9,
    "x_backup_file__mutmut_10": x_backup_file__mutmut_10,
    "x_backup_file__mutmut_11": x_backup_file__mutmut_11,
    "x_backup_file__mutmut_12": x_backup_file__mutmut_12,
    "x_backup_file__mutmut_13": x_backup_file__mutmut_13,
}


def backup_file(*args, **kwargs):
    result = _mutmut_trampoline(
        x_backup_file__mutmut_orig, x_backup_file__mutmut_mutants, args, kwargs
    )
    return result


backup_file.__signature__ = _mutmut_signature(x_backup_file__mutmut_orig)
x_backup_file__mutmut_orig.__name__ = "x_backup_file"


def x_safe_filename__mutmut_orig(filename: str, replacement: str = "_") -> str:
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


def x_safe_filename__mutmut_1(filename: str, replacement: str = "XX_XX") -> str:
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


def x_safe_filename__mutmut_2(filename: str, replacement: str = "_") -> str:
    """
    Make a filename safe for the filesystem by replacing invalid characters.

    Args:
        filename: Original filename
        replacement: Character to replace invalid characters with

    Returns:
        Safe filename
    """
    # Characters that are invalid in filenames on most systems
    invalid_chars = None
    safe_name = filename

    for char in invalid_chars:
        safe_name = safe_name.replace(char, replacement)

    # Remove leading/trailing whitespace and dots
    safe_name = safe_name.strip(". ")

    # Ensure it's not empty
    if not safe_name:
        safe_name = "unnamed"

    return safe_name


def x_safe_filename__mutmut_3(filename: str, replacement: str = "_") -> str:
    """
    Make a filename safe for the filesystem by replacing invalid characters.

    Args:
        filename: Original filename
        replacement: Character to replace invalid characters with

    Returns:
        Safe filename
    """
    # Characters that are invalid in filenames on most systems
    invalid_chars = 'XX<>:"/\\|?*XX'
    safe_name = filename

    for char in invalid_chars:
        safe_name = safe_name.replace(char, replacement)

    # Remove leading/trailing whitespace and dots
    safe_name = safe_name.strip(". ")

    # Ensure it's not empty
    if not safe_name:
        safe_name = "unnamed"

    return safe_name


def x_safe_filename__mutmut_4(filename: str, replacement: str = "_") -> str:
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
    safe_name = None

    for char in invalid_chars:
        safe_name = safe_name.replace(char, replacement)

    # Remove leading/trailing whitespace and dots
    safe_name = safe_name.strip(". ")

    # Ensure it's not empty
    if not safe_name:
        safe_name = "unnamed"

    return safe_name


def x_safe_filename__mutmut_5(filename: str, replacement: str = "_") -> str:
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
        safe_name = None

    # Remove leading/trailing whitespace and dots
    safe_name = safe_name.strip(". ")

    # Ensure it's not empty
    if not safe_name:
        safe_name = "unnamed"

    return safe_name


def x_safe_filename__mutmut_6(filename: str, replacement: str = "_") -> str:
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
        safe_name = safe_name.replace(None, replacement)

    # Remove leading/trailing whitespace and dots
    safe_name = safe_name.strip(". ")

    # Ensure it's not empty
    if not safe_name:
        safe_name = "unnamed"

    return safe_name


def x_safe_filename__mutmut_7(filename: str, replacement: str = "_") -> str:
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
        safe_name = safe_name.replace(char, None)

    # Remove leading/trailing whitespace and dots
    safe_name = safe_name.strip(". ")

    # Ensure it's not empty
    if not safe_name:
        safe_name = "unnamed"

    return safe_name


def x_safe_filename__mutmut_8(filename: str, replacement: str = "_") -> str:
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
        safe_name = safe_name.replace(replacement)

    # Remove leading/trailing whitespace and dots
    safe_name = safe_name.strip(". ")

    # Ensure it's not empty
    if not safe_name:
        safe_name = "unnamed"

    return safe_name


def x_safe_filename__mutmut_9(filename: str, replacement: str = "_") -> str:
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
        safe_name = safe_name.replace(
            char,
        )

    # Remove leading/trailing whitespace and dots
    safe_name = safe_name.strip(". ")

    # Ensure it's not empty
    if not safe_name:
        safe_name = "unnamed"

    return safe_name


def x_safe_filename__mutmut_10(filename: str, replacement: str = "_") -> str:
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
    safe_name = None

    # Ensure it's not empty
    if not safe_name:
        safe_name = "unnamed"

    return safe_name


def x_safe_filename__mutmut_11(filename: str, replacement: str = "_") -> str:
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
    safe_name = safe_name.strip(None)

    # Ensure it's not empty
    if not safe_name:
        safe_name = "unnamed"

    return safe_name


def x_safe_filename__mutmut_12(filename: str, replacement: str = "_") -> str:
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
    safe_name = safe_name.strip("XX. XX")

    # Ensure it's not empty
    if not safe_name:
        safe_name = "unnamed"

    return safe_name


def x_safe_filename__mutmut_13(filename: str, replacement: str = "_") -> str:
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
    if safe_name:
        safe_name = "unnamed"

    return safe_name


def x_safe_filename__mutmut_14(filename: str, replacement: str = "_") -> str:
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
        safe_name = None

    return safe_name


def x_safe_filename__mutmut_15(filename: str, replacement: str = "_") -> str:
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
        safe_name = "XXunnamedXX"

    return safe_name


def x_safe_filename__mutmut_16(filename: str, replacement: str = "_") -> str:
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
        safe_name = "UNNAMED"

    return safe_name


x_safe_filename__mutmut_mutants: ClassVar[MutantDict] = {
    "x_safe_filename__mutmut_1": x_safe_filename__mutmut_1,
    "x_safe_filename__mutmut_2": x_safe_filename__mutmut_2,
    "x_safe_filename__mutmut_3": x_safe_filename__mutmut_3,
    "x_safe_filename__mutmut_4": x_safe_filename__mutmut_4,
    "x_safe_filename__mutmut_5": x_safe_filename__mutmut_5,
    "x_safe_filename__mutmut_6": x_safe_filename__mutmut_6,
    "x_safe_filename__mutmut_7": x_safe_filename__mutmut_7,
    "x_safe_filename__mutmut_8": x_safe_filename__mutmut_8,
    "x_safe_filename__mutmut_9": x_safe_filename__mutmut_9,
    "x_safe_filename__mutmut_10": x_safe_filename__mutmut_10,
    "x_safe_filename__mutmut_11": x_safe_filename__mutmut_11,
    "x_safe_filename__mutmut_12": x_safe_filename__mutmut_12,
    "x_safe_filename__mutmut_13": x_safe_filename__mutmut_13,
    "x_safe_filename__mutmut_14": x_safe_filename__mutmut_14,
    "x_safe_filename__mutmut_15": x_safe_filename__mutmut_15,
    "x_safe_filename__mutmut_16": x_safe_filename__mutmut_16,
}


def safe_filename(*args, **kwargs):
    result = _mutmut_trampoline(
        x_safe_filename__mutmut_orig, x_safe_filename__mutmut_mutants, args, kwargs
    )
    return result


safe_filename.__signature__ = _mutmut_signature(x_safe_filename__mutmut_orig)
x_safe_filename__mutmut_orig.__name__ = "x_safe_filename"


def x_get_unique_filename__mutmut_orig(path: str | Path) -> Path:
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


def x_get_unique_filename__mutmut_1(path: str | Path) -> Path:
    """
    Get a unique filename by appending a number if the file already exists.

    Args:
        path: Desired file path

    Returns:
        Unique file path
    """
    file_path = None
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


def x_get_unique_filename__mutmut_2(path: str | Path) -> Path:
    """
    Get a unique filename by appending a number if the file already exists.

    Args:
        path: Desired file path

    Returns:
        Unique file path
    """
    file_path = Path(None)
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


def x_get_unique_filename__mutmut_3(path: str | Path) -> Path:
    """
    Get a unique filename by appending a number if the file already exists.

    Args:
        path: Desired file path

    Returns:
        Unique file path
    """
    file_path = Path(path)
    if file_path.exists():
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


def x_get_unique_filename__mutmut_4(path: str | Path) -> Path:
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

    stem = None
    suffix = file_path.suffix
    parent = file_path.parent

    counter = 1
    while True:
        new_name = f"{stem}_{counter}{suffix}"
        new_path = parent / new_name
        if not new_path.exists():
            return new_path
        counter += 1


def x_get_unique_filename__mutmut_5(path: str | Path) -> Path:
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
    suffix = None
    parent = file_path.parent

    counter = 1
    while True:
        new_name = f"{stem}_{counter}{suffix}"
        new_path = parent / new_name
        if not new_path.exists():
            return new_path
        counter += 1


def x_get_unique_filename__mutmut_6(path: str | Path) -> Path:
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
    parent = None

    counter = 1
    while True:
        new_name = f"{stem}_{counter}{suffix}"
        new_path = parent / new_name
        if not new_path.exists():
            return new_path
        counter += 1


def x_get_unique_filename__mutmut_7(path: str | Path) -> Path:
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

    counter = None
    while True:
        new_name = f"{stem}_{counter}{suffix}"
        new_path = parent / new_name
        if not new_path.exists():
            return new_path
        counter += 1


def x_get_unique_filename__mutmut_8(path: str | Path) -> Path:
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

    counter = 2
    while True:
        new_name = f"{stem}_{counter}{suffix}"
        new_path = parent / new_name
        if not new_path.exists():
            return new_path
        counter += 1


def x_get_unique_filename__mutmut_9(path: str | Path) -> Path:
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
    while False:
        new_name = f"{stem}_{counter}{suffix}"
        new_path = parent / new_name
        if not new_path.exists():
            return new_path
        counter += 1


def x_get_unique_filename__mutmut_10(path: str | Path) -> Path:
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
        new_name = None
        new_path = parent / new_name
        if not new_path.exists():
            return new_path
        counter += 1


def x_get_unique_filename__mutmut_11(path: str | Path) -> Path:
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
        new_path = None
        if not new_path.exists():
            return new_path
        counter += 1


def x_get_unique_filename__mutmut_12(path: str | Path) -> Path:
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
        new_path = parent * new_name
        if not new_path.exists():
            return new_path
        counter += 1


def x_get_unique_filename__mutmut_13(path: str | Path) -> Path:
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
        if new_path.exists():
            return new_path
        counter += 1


def x_get_unique_filename__mutmut_14(path: str | Path) -> Path:
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
        counter = 1


def x_get_unique_filename__mutmut_15(path: str | Path) -> Path:
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
        counter -= 1


def x_get_unique_filename__mutmut_16(path: str | Path) -> Path:
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
        counter += 2


x_get_unique_filename__mutmut_mutants: ClassVar[MutantDict] = {
    "x_get_unique_filename__mutmut_1": x_get_unique_filename__mutmut_1,
    "x_get_unique_filename__mutmut_2": x_get_unique_filename__mutmut_2,
    "x_get_unique_filename__mutmut_3": x_get_unique_filename__mutmut_3,
    "x_get_unique_filename__mutmut_4": x_get_unique_filename__mutmut_4,
    "x_get_unique_filename__mutmut_5": x_get_unique_filename__mutmut_5,
    "x_get_unique_filename__mutmut_6": x_get_unique_filename__mutmut_6,
    "x_get_unique_filename__mutmut_7": x_get_unique_filename__mutmut_7,
    "x_get_unique_filename__mutmut_8": x_get_unique_filename__mutmut_8,
    "x_get_unique_filename__mutmut_9": x_get_unique_filename__mutmut_9,
    "x_get_unique_filename__mutmut_10": x_get_unique_filename__mutmut_10,
    "x_get_unique_filename__mutmut_11": x_get_unique_filename__mutmut_11,
    "x_get_unique_filename__mutmut_12": x_get_unique_filename__mutmut_12,
    "x_get_unique_filename__mutmut_13": x_get_unique_filename__mutmut_13,
    "x_get_unique_filename__mutmut_14": x_get_unique_filename__mutmut_14,
    "x_get_unique_filename__mutmut_15": x_get_unique_filename__mutmut_15,
    "x_get_unique_filename__mutmut_16": x_get_unique_filename__mutmut_16,
}


def get_unique_filename(*args, **kwargs):
    result = _mutmut_trampoline(
        x_get_unique_filename__mutmut_orig,
        x_get_unique_filename__mutmut_mutants,
        args,
        kwargs,
    )
    return result


get_unique_filename.__signature__ = _mutmut_signature(
    x_get_unique_filename__mutmut_orig
)
x_get_unique_filename__mutmut_orig.__name__ = "x_get_unique_filename"


class TemporaryDirectory:
    """Context manager for creating and cleaning up temporary directories."""

    def xǁTemporaryDirectoryǁ__init____mutmut_orig(
        self, prefix: str = "pmas_test_", cleanup: bool = True
    ) -> None:
        self.prefix = prefix
        self.cleanup = cleanup
        self.path: Path | None = None

    def xǁTemporaryDirectoryǁ__init____mutmut_1(
        self, prefix: str = "XXpmas_test_XX", cleanup: bool = True
    ) -> None:
        self.prefix = prefix
        self.cleanup = cleanup
        self.path: Path | None = None

    def xǁTemporaryDirectoryǁ__init____mutmut_2(
        self, prefix: str = "PMAS_TEST_", cleanup: bool = True
    ) -> None:
        self.prefix = prefix
        self.cleanup = cleanup
        self.path: Path | None = None

    def xǁTemporaryDirectoryǁ__init____mutmut_3(
        self, prefix: str = "pmas_test_", cleanup: bool = False
    ) -> None:
        self.prefix = prefix
        self.cleanup = cleanup
        self.path: Path | None = None

    def xǁTemporaryDirectoryǁ__init____mutmut_4(
        self, prefix: str = "pmas_test_", cleanup: bool = True
    ) -> None:
        self.prefix = None
        self.cleanup = cleanup
        self.path: Path | None = None

    def xǁTemporaryDirectoryǁ__init____mutmut_5(
        self, prefix: str = "pmas_test_", cleanup: bool = True
    ) -> None:
        self.prefix = prefix
        self.cleanup = None
        self.path: Path | None = None

    def xǁTemporaryDirectoryǁ__init____mutmut_6(
        self, prefix: str = "pmas_test_", cleanup: bool = True
    ) -> None:
        self.prefix = prefix
        self.cleanup = cleanup
        self.path: Path | None = ""

    xǁTemporaryDirectoryǁ__init____mutmut_mutants: ClassVar[MutantDict] = {
        "xǁTemporaryDirectoryǁ__init____mutmut_1": xǁTemporaryDirectoryǁ__init____mutmut_1,
        "xǁTemporaryDirectoryǁ__init____mutmut_2": xǁTemporaryDirectoryǁ__init____mutmut_2,
        "xǁTemporaryDirectoryǁ__init____mutmut_3": xǁTemporaryDirectoryǁ__init____mutmut_3,
        "xǁTemporaryDirectoryǁ__init____mutmut_4": xǁTemporaryDirectoryǁ__init____mutmut_4,
        "xǁTemporaryDirectoryǁ__init____mutmut_5": xǁTemporaryDirectoryǁ__init____mutmut_5,
        "xǁTemporaryDirectoryǁ__init____mutmut_6": xǁTemporaryDirectoryǁ__init____mutmut_6,
    }

    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁTemporaryDirectoryǁ__init____mutmut_orig"),
            object.__getattribute__(
                self, "xǁTemporaryDirectoryǁ__init____mutmut_mutants"
            ),
            args,
            kwargs,
            self,
        )
        return result

    __init__.__signature__ = _mutmut_signature(
        xǁTemporaryDirectoryǁ__init____mutmut_orig
    )
    xǁTemporaryDirectoryǁ__init____mutmut_orig.__name__ = (
        "xǁTemporaryDirectoryǁ__init__"
    )

    def xǁTemporaryDirectoryǁ__enter____mutmut_orig(self) -> Path:
        self.path = Path(tempfile.mkdtemp(prefix=self.prefix))
        logger.debug(f"Created temporary directory: {self.path}")
        return self.path

    def xǁTemporaryDirectoryǁ__enter____mutmut_1(self) -> Path:
        self.path = None
        logger.debug(f"Created temporary directory: {self.path}")
        return self.path

    def xǁTemporaryDirectoryǁ__enter____mutmut_2(self) -> Path:
        self.path = Path(None)
        logger.debug(f"Created temporary directory: {self.path}")
        return self.path

    def xǁTemporaryDirectoryǁ__enter____mutmut_3(self) -> Path:
        self.path = Path(tempfile.mkdtemp(prefix=None))
        logger.debug(f"Created temporary directory: {self.path}")
        return self.path

    def xǁTemporaryDirectoryǁ__enter____mutmut_4(self) -> Path:
        self.path = Path(tempfile.mkdtemp(prefix=self.prefix))
        logger.debug(None)
        return self.path

    xǁTemporaryDirectoryǁ__enter____mutmut_mutants: ClassVar[MutantDict] = {
        "xǁTemporaryDirectoryǁ__enter____mutmut_1": xǁTemporaryDirectoryǁ__enter____mutmut_1,
        "xǁTemporaryDirectoryǁ__enter____mutmut_2": xǁTemporaryDirectoryǁ__enter____mutmut_2,
        "xǁTemporaryDirectoryǁ__enter____mutmut_3": xǁTemporaryDirectoryǁ__enter____mutmut_3,
        "xǁTemporaryDirectoryǁ__enter____mutmut_4": xǁTemporaryDirectoryǁ__enter____mutmut_4,
    }

    def __enter__(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(
                self, "xǁTemporaryDirectoryǁ__enter____mutmut_orig"
            ),
            object.__getattribute__(
                self, "xǁTemporaryDirectoryǁ__enter____mutmut_mutants"
            ),
            args,
            kwargs,
            self,
        )
        return result

    __enter__.__signature__ = _mutmut_signature(
        xǁTemporaryDirectoryǁ__enter____mutmut_orig
    )
    xǁTemporaryDirectoryǁ__enter____mutmut_orig.__name__ = (
        "xǁTemporaryDirectoryǁ__enter__"
    )

    def xǁTemporaryDirectoryǁ__exit____mutmut_orig(
        self, exc_type, exc_val, exc_tb
    ) -> None:
        if self.cleanup and self.path and self.path.exists():
            shutil.rmtree(self.path)
            logger.debug(f"Cleaned up temporary directory: {self.path}")

    def xǁTemporaryDirectoryǁ__exit____mutmut_1(
        self, exc_type, exc_val, exc_tb
    ) -> None:
        if self.cleanup and self.path or self.path.exists():
            shutil.rmtree(self.path)
            logger.debug(f"Cleaned up temporary directory: {self.path}")

    def xǁTemporaryDirectoryǁ__exit____mutmut_2(
        self, exc_type, exc_val, exc_tb
    ) -> None:
        if self.cleanup or self.path and self.path.exists():
            shutil.rmtree(self.path)
            logger.debug(f"Cleaned up temporary directory: {self.path}")

    def xǁTemporaryDirectoryǁ__exit____mutmut_3(
        self, exc_type, exc_val, exc_tb
    ) -> None:
        if self.cleanup and self.path and self.path.exists():
            shutil.rmtree(None)
            logger.debug(f"Cleaned up temporary directory: {self.path}")

    def xǁTemporaryDirectoryǁ__exit____mutmut_4(
        self, exc_type, exc_val, exc_tb
    ) -> None:
        if self.cleanup and self.path and self.path.exists():
            shutil.rmtree(self.path)
            logger.debug(None)

    xǁTemporaryDirectoryǁ__exit____mutmut_mutants: ClassVar[MutantDict] = {
        "xǁTemporaryDirectoryǁ__exit____mutmut_1": xǁTemporaryDirectoryǁ__exit____mutmut_1,
        "xǁTemporaryDirectoryǁ__exit____mutmut_2": xǁTemporaryDirectoryǁ__exit____mutmut_2,
        "xǁTemporaryDirectoryǁ__exit____mutmut_3": xǁTemporaryDirectoryǁ__exit____mutmut_3,
        "xǁTemporaryDirectoryǁ__exit____mutmut_4": xǁTemporaryDirectoryǁ__exit____mutmut_4,
    }

    def __exit__(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁTemporaryDirectoryǁ__exit____mutmut_orig"),
            object.__getattribute__(
                self, "xǁTemporaryDirectoryǁ__exit____mutmut_mutants"
            ),
            args,
            kwargs,
            self,
        )
        return result

    __exit__.__signature__ = _mutmut_signature(
        xǁTemporaryDirectoryǁ__exit____mutmut_orig
    )
    xǁTemporaryDirectoryǁ__exit____mutmut_orig.__name__ = (
        "xǁTemporaryDirectoryǁ__exit__"
    )


def x_read_file_lines__mutmut_orig(
    path: str | Path, encoding: str = "utf-8"
) -> list[str]:
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


def x_read_file_lines__mutmut_1(
    path: str | Path, encoding: str = "XXutf-8XX"
) -> list[str]:
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


def x_read_file_lines__mutmut_2(path: str | Path, encoding: str = "UTF-8") -> list[str]:
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


def x_read_file_lines__mutmut_3(path: str | Path, encoding: str = "utf-8") -> list[str]:
    """
    Read all lines from a file.

    Args:
        path: File path
        encoding: File encoding

    Returns:
        List of lines from the file
    """
    file_path = None
    try:
        with file_path.open("r", encoding=encoding) as f:
            return f.readlines()
    except FileNotFoundError:
        logger.warning(f"File not found: {file_path}")
        return []
    except UnicodeDecodeError as e:
        logger.error(f"Failed to decode file {file_path}: {e}")
        return []


def x_read_file_lines__mutmut_4(path: str | Path, encoding: str = "utf-8") -> list[str]:
    """
    Read all lines from a file.

    Args:
        path: File path
        encoding: File encoding

    Returns:
        List of lines from the file
    """
    file_path = Path(None)
    try:
        with file_path.open("r", encoding=encoding) as f:
            return f.readlines()
    except FileNotFoundError:
        logger.warning(f"File not found: {file_path}")
        return []
    except UnicodeDecodeError as e:
        logger.error(f"Failed to decode file {file_path}: {e}")
        return []


def x_read_file_lines__mutmut_5(path: str | Path, encoding: str = "utf-8") -> list[str]:
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
        with file_path.open(None, encoding=encoding) as f:
            return f.readlines()
    except FileNotFoundError:
        logger.warning(f"File not found: {file_path}")
        return []
    except UnicodeDecodeError as e:
        logger.error(f"Failed to decode file {file_path}: {e}")
        return []


def x_read_file_lines__mutmut_6(path: str | Path, encoding: str = "utf-8") -> list[str]:
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
        with file_path.open("r", encoding=None) as f:
            return f.readlines()
    except FileNotFoundError:
        logger.warning(f"File not found: {file_path}")
        return []
    except UnicodeDecodeError as e:
        logger.error(f"Failed to decode file {file_path}: {e}")
        return []


def x_read_file_lines__mutmut_7(path: str | Path, encoding: str = "utf-8") -> list[str]:
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
        with file_path.open(encoding=encoding) as f:
            return f.readlines()
    except FileNotFoundError:
        logger.warning(f"File not found: {file_path}")
        return []
    except UnicodeDecodeError as e:
        logger.error(f"Failed to decode file {file_path}: {e}")
        return []


def x_read_file_lines__mutmut_8(path: str | Path, encoding: str = "utf-8") -> list[str]:
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
        with file_path.open(
            "r",
        ) as f:
            return f.readlines()
    except FileNotFoundError:
        logger.warning(f"File not found: {file_path}")
        return []
    except UnicodeDecodeError as e:
        logger.error(f"Failed to decode file {file_path}: {e}")
        return []


def x_read_file_lines__mutmut_9(path: str | Path, encoding: str = "utf-8") -> list[str]:
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
        with file_path.open("XXrXX", encoding=encoding) as f:
            return f.readlines()
    except FileNotFoundError:
        logger.warning(f"File not found: {file_path}")
        return []
    except UnicodeDecodeError as e:
        logger.error(f"Failed to decode file {file_path}: {e}")
        return []


def x_read_file_lines__mutmut_10(
    path: str | Path, encoding: str = "utf-8"
) -> list[str]:
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
        with file_path.open("R", encoding=encoding) as f:
            return f.readlines()
    except FileNotFoundError:
        logger.warning(f"File not found: {file_path}")
        return []
    except UnicodeDecodeError as e:
        logger.error(f"Failed to decode file {file_path}: {e}")
        return []


def x_read_file_lines__mutmut_11(
    path: str | Path, encoding: str = "utf-8"
) -> list[str]:
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
        logger.warning(None)
        return []
    except UnicodeDecodeError as e:
        logger.error(f"Failed to decode file {file_path}: {e}")
        return []


def x_read_file_lines__mutmut_12(
    path: str | Path, encoding: str = "utf-8"
) -> list[str]:
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
    except UnicodeDecodeError:
        logger.error(None)
        return []


x_read_file_lines__mutmut_mutants: ClassVar[MutantDict] = {
    "x_read_file_lines__mutmut_1": x_read_file_lines__mutmut_1,
    "x_read_file_lines__mutmut_2": x_read_file_lines__mutmut_2,
    "x_read_file_lines__mutmut_3": x_read_file_lines__mutmut_3,
    "x_read_file_lines__mutmut_4": x_read_file_lines__mutmut_4,
    "x_read_file_lines__mutmut_5": x_read_file_lines__mutmut_5,
    "x_read_file_lines__mutmut_6": x_read_file_lines__mutmut_6,
    "x_read_file_lines__mutmut_7": x_read_file_lines__mutmut_7,
    "x_read_file_lines__mutmut_8": x_read_file_lines__mutmut_8,
    "x_read_file_lines__mutmut_9": x_read_file_lines__mutmut_9,
    "x_read_file_lines__mutmut_10": x_read_file_lines__mutmut_10,
    "x_read_file_lines__mutmut_11": x_read_file_lines__mutmut_11,
    "x_read_file_lines__mutmut_12": x_read_file_lines__mutmut_12,
}


def read_file_lines(*args, **kwargs):
    result = _mutmut_trampoline(
        x_read_file_lines__mutmut_orig, x_read_file_lines__mutmut_mutants, args, kwargs
    )
    return result


read_file_lines.__signature__ = _mutmut_signature(x_read_file_lines__mutmut_orig)
x_read_file_lines__mutmut_orig.__name__ = "x_read_file_lines"


def x_write_file_lines__mutmut_orig(
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


def x_write_file_lines__mutmut_1(
    path: str | Path, lines: list[str], encoding: str = "XXutf-8XX"
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


def x_write_file_lines__mutmut_2(
    path: str | Path, lines: list[str], encoding: str = "UTF-8"
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


def x_write_file_lines__mutmut_3(
    path: str | Path, lines: list[str], encoding: str = "utf-8"
) -> None:
    """
    Write lines to a file.

    Args:
        path: File path
        lines: Lines to write
        encoding: File encoding
    """
    file_path = None
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with file_path.open("w", encoding=encoding) as f:
        f.writelines(lines)

    logger.debug(f"Wrote {len(lines)} lines to {file_path}")


def x_write_file_lines__mutmut_4(
    path: str | Path, lines: list[str], encoding: str = "utf-8"
) -> None:
    """
    Write lines to a file.

    Args:
        path: File path
        lines: Lines to write
        encoding: File encoding
    """
    file_path = Path(None)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with file_path.open("w", encoding=encoding) as f:
        f.writelines(lines)

    logger.debug(f"Wrote {len(lines)} lines to {file_path}")


def x_write_file_lines__mutmut_5(
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
    file_path.parent.mkdir(parents=None, exist_ok=True)

    with file_path.open("w", encoding=encoding) as f:
        f.writelines(lines)

    logger.debug(f"Wrote {len(lines)} lines to {file_path}")


def x_write_file_lines__mutmut_6(
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
    file_path.parent.mkdir(parents=True, exist_ok=None)

    with file_path.open("w", encoding=encoding) as f:
        f.writelines(lines)

    logger.debug(f"Wrote {len(lines)} lines to {file_path}")


def x_write_file_lines__mutmut_7(
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
    file_path.parent.mkdir(exist_ok=True)

    with file_path.open("w", encoding=encoding) as f:
        f.writelines(lines)

    logger.debug(f"Wrote {len(lines)} lines to {file_path}")


def x_write_file_lines__mutmut_8(
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
    file_path.parent.mkdir(
        parents=True,
    )

    with file_path.open("w", encoding=encoding) as f:
        f.writelines(lines)

    logger.debug(f"Wrote {len(lines)} lines to {file_path}")


def x_write_file_lines__mutmut_9(
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
    file_path.parent.mkdir(parents=False, exist_ok=True)

    with file_path.open("w", encoding=encoding) as f:
        f.writelines(lines)

    logger.debug(f"Wrote {len(lines)} lines to {file_path}")


def x_write_file_lines__mutmut_10(
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
    file_path.parent.mkdir(parents=True, exist_ok=False)

    with file_path.open("w", encoding=encoding) as f:
        f.writelines(lines)

    logger.debug(f"Wrote {len(lines)} lines to {file_path}")


def x_write_file_lines__mutmut_11(
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

    with file_path.open(None, encoding=encoding) as f:
        f.writelines(lines)

    logger.debug(f"Wrote {len(lines)} lines to {file_path}")


def x_write_file_lines__mutmut_12(
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

    with file_path.open("w", encoding=None) as f:
        f.writelines(lines)

    logger.debug(f"Wrote {len(lines)} lines to {file_path}")


def x_write_file_lines__mutmut_13(
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

    with file_path.open(encoding=encoding) as f:
        f.writelines(lines)

    logger.debug(f"Wrote {len(lines)} lines to {file_path}")


def x_write_file_lines__mutmut_14(
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

    with file_path.open(
        "w",
    ) as f:
        f.writelines(lines)

    logger.debug(f"Wrote {len(lines)} lines to {file_path}")


def x_write_file_lines__mutmut_15(
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

    with file_path.open("XXwXX", encoding=encoding) as f:
        f.writelines(lines)

    logger.debug(f"Wrote {len(lines)} lines to {file_path}")


def x_write_file_lines__mutmut_16(
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

    with file_path.open("W", encoding=encoding) as f:
        f.writelines(lines)

    logger.debug(f"Wrote {len(lines)} lines to {file_path}")


def x_write_file_lines__mutmut_17(
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
        f.writelines(None)

    logger.debug(f"Wrote {len(lines)} lines to {file_path}")


def x_write_file_lines__mutmut_18(
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

    logger.debug(None)


x_write_file_lines__mutmut_mutants: ClassVar[MutantDict] = {
    "x_write_file_lines__mutmut_1": x_write_file_lines__mutmut_1,
    "x_write_file_lines__mutmut_2": x_write_file_lines__mutmut_2,
    "x_write_file_lines__mutmut_3": x_write_file_lines__mutmut_3,
    "x_write_file_lines__mutmut_4": x_write_file_lines__mutmut_4,
    "x_write_file_lines__mutmut_5": x_write_file_lines__mutmut_5,
    "x_write_file_lines__mutmut_6": x_write_file_lines__mutmut_6,
    "x_write_file_lines__mutmut_7": x_write_file_lines__mutmut_7,
    "x_write_file_lines__mutmut_8": x_write_file_lines__mutmut_8,
    "x_write_file_lines__mutmut_9": x_write_file_lines__mutmut_9,
    "x_write_file_lines__mutmut_10": x_write_file_lines__mutmut_10,
    "x_write_file_lines__mutmut_11": x_write_file_lines__mutmut_11,
    "x_write_file_lines__mutmut_12": x_write_file_lines__mutmut_12,
    "x_write_file_lines__mutmut_13": x_write_file_lines__mutmut_13,
    "x_write_file_lines__mutmut_14": x_write_file_lines__mutmut_14,
    "x_write_file_lines__mutmut_15": x_write_file_lines__mutmut_15,
    "x_write_file_lines__mutmut_16": x_write_file_lines__mutmut_16,
    "x_write_file_lines__mutmut_17": x_write_file_lines__mutmut_17,
    "x_write_file_lines__mutmut_18": x_write_file_lines__mutmut_18,
}


def write_file_lines(*args, **kwargs):
    result = _mutmut_trampoline(
        x_write_file_lines__mutmut_orig,
        x_write_file_lines__mutmut_mutants,
        args,
        kwargs,
    )
    return result


write_file_lines.__signature__ = _mutmut_signature(x_write_file_lines__mutmut_orig)
x_write_file_lines__mutmut_orig.__name__ = "x_write_file_lines"


def x_tail_file__mutmut_orig(path: str | Path, num_lines: int = 10) -> list[str]:
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


def x_tail_file__mutmut_1(path: str | Path, num_lines: int = 11) -> list[str]:
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


def x_tail_file__mutmut_2(path: str | Path, num_lines: int = 10) -> list[str]:
    """
    Get the last N lines from a file (like Unix tail command).

    Args:
        path: File path
        num_lines: Number of lines to return

    Returns:
        List of last N lines
    """
    lines = None
    return lines[-num_lines:] if lines else []


def x_tail_file__mutmut_3(path: str | Path, num_lines: int = 10) -> list[str]:
    """
    Get the last N lines from a file (like Unix tail command).

    Args:
        path: File path
        num_lines: Number of lines to return

    Returns:
        List of last N lines
    """
    lines = read_file_lines(None)
    return lines[-num_lines:] if lines else []


def x_tail_file__mutmut_4(path: str | Path, num_lines: int = 10) -> list[str]:
    """
    Get the last N lines from a file (like Unix tail command).

    Args:
        path: File path
        num_lines: Number of lines to return

    Returns:
        List of last N lines
    """
    lines = read_file_lines(path)
    return lines[+num_lines:] if lines else []


x_tail_file__mutmut_mutants: ClassVar[MutantDict] = {
    "x_tail_file__mutmut_1": x_tail_file__mutmut_1,
    "x_tail_file__mutmut_2": x_tail_file__mutmut_2,
    "x_tail_file__mutmut_3": x_tail_file__mutmut_3,
    "x_tail_file__mutmut_4": x_tail_file__mutmut_4,
}


def tail_file(*args, **kwargs):
    result = _mutmut_trampoline(
        x_tail_file__mutmut_orig, x_tail_file__mutmut_mutants, args, kwargs
    )
    return result


tail_file.__signature__ = _mutmut_signature(x_tail_file__mutmut_orig)
x_tail_file__mutmut_orig.__name__ = "x_tail_file"
