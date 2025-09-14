"""
Soft assertion utilities for collecting multiple assertion failures.
"""

import logging
from collections.abc import Callable
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class AssertionFailure:
    """Represents a single assertion failure."""

    message: str
    expected: Any = None
    actual: Any = None
    location: str = ""

    def __str__(self) -> str:
        if self.expected is not None and self.actual is not None:
            return (
                f"{self.message}\n  Expected: {self.expected}\n  Actual: {self.actual}"
            )
        return self.message


class SoftAssertions:
    """
    Context manager for collecting multiple assertion failures.

    Allows tests to continue executing after assertion failures,
    collecting all failures and reporting them at the end.

    Example:
        with SoftAssertions() as soft:
            soft.assert_equal(actual, expected, "Values should be equal")
            soft.assert_true(condition, "Condition should be true")
            # Test continues even if assertions fail
        # All failures are reported here
    """

    def __init__(self, fail_fast: bool = False) -> None:
        self.failures: list[AssertionFailure] = []
        self.fail_fast = fail_fast
        self._in_context = False

    def __enter__(self) -> "SoftAssertions":
        self._in_context = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self._in_context = False
        if self.failures:
            failure_messages = [str(failure) for failure in self.failures]
            combined_message = (
                f"Soft assertion failures ({len(self.failures)}):\n"
                + "\n".join(
                    f"  {i + 1}. {msg}" for i, msg in enumerate(failure_messages)
                )
            )
            raise AssertionError(combined_message)

    def _add_failure(
        self, message: str, expected: Any = None, actual: Any = None
    ) -> None:
        """Add a failure to the collection."""
        import traceback

        # Get the calling location
        stack = traceback.extract_stack()
        # Find the first frame outside this module
        location = ""
        for frame in reversed(stack[:-1]):
            if not frame.filename.endswith("assertions.py"):
                location = f"{frame.filename}:{frame.lineno}"
                break

        failure = AssertionFailure(
            message=message, expected=expected, actual=actual, location=location
        )

        self.failures.append(failure)
        logger.warning(f"Soft assertion failure: {failure}")

        if self.fail_fast:
            raise AssertionError(str(failure))

    def assert_true(
        self, condition: bool, message: str = "Condition should be true"
    ) -> None:
        """Assert that a condition is true."""
        if not condition:
            self._add_failure(message, expected=True, actual=condition)

    def assert_false(
        self, condition: bool, message: str = "Condition should be false"
    ) -> None:
        """Assert that a condition is false."""
        if condition:
            self._add_failure(message, expected=False, actual=condition)

    def assert_equal(
        self, actual: Any, expected: Any, message: str = "Values should be equal"
    ) -> None:
        """Assert that two values are equal."""
        if actual != expected:
            self._add_failure(message, expected=expected, actual=actual)

    def assert_not_equal(
        self, actual: Any, expected: Any, message: str = "Values should not be equal"
    ) -> None:
        """Assert that two values are not equal."""
        if actual == expected:
            self._add_failure(message, expected=f"not {expected}", actual=actual)

    def assert_in(
        self, item: Any, container: Any, message: str = "Item should be in container"
    ) -> None:
        """Assert that an item is in a container."""
        if item not in container:
            self._add_failure(
                message,
                expected=f"{item} in {container}",
                actual=f"{item} not in {container}",
            )

    def assert_not_in(
        self,
        item: Any,
        container: Any,
        message: str = "Item should not be in container",
    ) -> None:
        """Assert that an item is not in a container."""
        if item in container:
            self._add_failure(
                message,
                expected=f"{item} not in {container}",
                actual=f"{item} in {container}",
            )

    def assert_is_none(self, value: Any, message: str = "Value should be None") -> None:
        """Assert that a value is None."""
        if value is not None:
            self._add_failure(message, expected=None, actual=value)

    def assert_is_not_none(
        self, value: Any, message: str = "Value should not be None"
    ) -> None:
        """Assert that a value is not None."""
        if value is None:
            self._add_failure(message, expected="not None", actual=None)

    def assert_greater(
        self, actual: Any, expected: Any, message: str = "Value should be greater"
    ) -> None:
        """Assert that actual > expected."""
        if not actual > expected:
            self._add_failure(message, expected=f"> {expected}", actual=actual)

    def assert_greater_equal(
        self,
        actual: Any,
        expected: Any,
        message: str = "Value should be greater or equal",
    ) -> None:
        """Assert that actual >= expected."""
        if not actual >= expected:
            self._add_failure(message, expected=f">= {expected}", actual=actual)

    def assert_less(
        self, actual: Any, expected: Any, message: str = "Value should be less"
    ) -> None:
        """Assert that actual < expected."""
        if not actual < expected:
            self._add_failure(message, expected=f"< {expected}", actual=actual)

    def assert_less_equal(
        self, actual: Any, expected: Any, message: str = "Value should be less or equal"
    ) -> None:
        """Assert that actual <= expected."""
        if not actual <= expected:
            self._add_failure(message, expected=f"<= {expected}", actual=actual)

    def assert_contains(
        self, text: str, substring: str, message: str = "Text should contain substring"
    ) -> None:
        """Assert that text contains a substring."""
        if substring not in text:
            self._add_failure(
                message,
                expected=f"'{substring}' in '{text}'",
                actual=f"'{substring}' not found",
            )

    def assert_not_contains(
        self,
        text: str,
        substring: str,
        message: str = "Text should not contain substring",
    ) -> None:
        """Assert that text does not contain a substring."""
        if substring in text:
            self._add_failure(
                message,
                expected=f"'{substring}' not in '{text}'",
                actual=f"'{substring}' found",
            )

    def assert_starts_with(
        self, text: str, prefix: str, message: str = "Text should start with prefix"
    ) -> None:
        """Assert that text starts with a prefix."""
        if not text.startswith(prefix):
            self._add_failure(
                message, expected=f"starts with '{prefix}'", actual=f"'{text}'"
            )

    def assert_ends_with(
        self, text: str, suffix: str, message: str = "Text should end with suffix"
    ) -> None:
        """Assert that text ends with a suffix."""
        if not text.endswith(suffix):
            self._add_failure(
                message, expected=f"ends with '{suffix}'", actual=f"'{text}'"
            )

    def assert_regex_match(
        self, text: str, pattern: str, message: str = "Text should match regex pattern"
    ) -> None:
        """Assert that text matches a regex pattern."""
        import re

        if not re.search(pattern, text):
            self._add_failure(
                message, expected=f"matches pattern '{pattern}'", actual=f"'{text}'"
            )

    def assert_length(
        self,
        container: Any,
        expected_length: int,
        message: str = "Container should have expected length",
    ) -> None:
        """Assert that a container has the expected length."""
        actual_length = len(container)
        if actual_length != expected_length:
            self._add_failure(message, expected=expected_length, actual=actual_length)

    def assert_empty(
        self, container: Any, message: str = "Container should be empty"
    ) -> None:
        """Assert that a container is empty."""
        if len(container) != 0:
            self._add_failure(
                message, expected="empty", actual=f"length {len(container)}"
            )

    def assert_not_empty(
        self, container: Any, message: str = "Container should not be empty"
    ) -> None:
        """Assert that a container is not empty."""
        if len(container) == 0:
            self._add_failure(message, expected="not empty", actual="empty")

    def assert_isinstance(
        self,
        obj: Any,
        expected_type: type,
        message: str = "Object should be of expected type",
    ) -> None:
        """Assert that an object is an instance of the expected type."""
        if not isinstance(obj, expected_type):
            self._add_failure(
                message, expected=expected_type.__name__, actual=type(obj).__name__
            )

    def assert_callable(
        self, obj: Any, message: str = "Object should be callable"
    ) -> None:
        """Assert that an object is callable."""
        if not callable(obj):
            self._add_failure(message, expected="callable", actual=type(obj).__name__)

    def assert_raises(
        self, expected_exception: type, func: Callable, *args, **kwargs
    ) -> None:
        """Assert that a function raises the expected exception."""
        try:
            func(*args, **kwargs)
            self._add_failure(
                f"Expected {expected_exception.__name__} to be raised",
                expected=expected_exception.__name__,
                actual="no exception",
            )
        except expected_exception:
            # Expected exception was raised
            pass
        except Exception as e:
            self._add_failure(
                f"Expected {expected_exception.__name__} but got {type(e).__name__}",
                expected=expected_exception.__name__,
                actual=type(e).__name__,
            )

    def custom_assert(
        self, condition: bool, message: str, expected: Any = None, actual: Any = None
    ) -> None:
        """Custom assertion with user-defined condition."""
        if not condition:
            self._add_failure(message, expected=expected, actual=actual)

    @property
    def has_failures(self) -> bool:
        """Check if there are any failures."""
        return len(self.failures) > 0

    @property
    def failure_count(self) -> int:
        """Get the number of failures."""
        return len(self.failures)

    def clear_failures(self) -> None:
        """Clear all recorded failures."""
        self.failures.clear()

    def get_failure_summary(self) -> str:
        """Get a summary of all failures."""
        if not self.failures:
            return "No failures"

        return f"{len(self.failures)} failure(s):\n" + "\n".join(
            f"  {i + 1}. {failure}" for i, failure in enumerate(self.failures)
        )


@contextmanager
def soft_assertions(fail_fast: bool = False):
    """Context manager for soft assertions."""
    soft = SoftAssertions(fail_fast=fail_fast)
    with soft:
        yield soft
