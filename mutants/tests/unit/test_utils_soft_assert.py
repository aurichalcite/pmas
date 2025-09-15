"""
Unit tests for PMAS SoftAssertions utility class.

This module tests the soft assertion functionality in complete isolation.
Tests cover:
- Basic assertion methods (assert_equal, assert_true, etc.)
- Context manager behavior and failure collection
- Fail-fast mode functionality
- Error message formatting and location tracking
- Multiple assertion scenarios and edge cases

All tests are hermetic with no external dependencies.
"""

import re

import pytest

# ASSUMPTION: Import PMAS SoftAssertions utility
from pmas.testing.assertions import AssertionFailure, SoftAssertions


class TestAssertionFailure:
    """Unit tests for AssertionFailure data class."""

    def test_assertion_failure_initialization(self):
        """Test AssertionFailure initialization with all parameters."""
        failure = AssertionFailure(
            message="Test failed",
            expected="expected_value",
            actual="actual_value",
            location="test_file.py:42",
        )

        assert failure.message == "Test failed"
        assert failure.expected == "expected_value"
        assert failure.actual == "actual_value"
        assert failure.location == "test_file.py:42"

    def test_assertion_failure_string_representation(self):
        """Test AssertionFailure string representation."""
        failure = AssertionFailure(
            message="Values should be equal",
            expected=10,
            actual=5,
            location="test.py:10",
        )

        failure_str = str(failure)
        assert "Values should be equal" in failure_str
        assert "Expected: 10" in failure_str
        assert "Actual: 5" in failure_str
        # Location is stored but not included in string representation
        assert failure.location == "test.py:10"

    def test_assertion_failure_without_expected_actual(self):
        """Test AssertionFailure with only message."""
        failure = AssertionFailure(
            message="Something went wrong", location="test.py:20"
        )

        failure_str = str(failure)
        assert "Something went wrong" in failure_str
        # Location is stored but not included in string representation
        assert failure.location == "test.py:20"
        # Should not contain Expected/Actual when not provided
        assert "Expected:" not in failure_str
        assert "Actual:" not in failure_str


class TestSoftAssertions:
    """Unit tests for SoftAssertions context manager."""

    def test_soft_assertions_initialization_default(self):
        """Test SoftAssertions initialization with default parameters."""
        soft = SoftAssertions()

        assert soft.failures == []
        assert soft.fail_fast is False
        assert soft._in_context is False

    def test_soft_assertions_initialization_fail_fast(self):
        """Test SoftAssertions initialization with fail_fast=True."""
        soft = SoftAssertions(fail_fast=True)

        assert soft.fail_fast is True
        assert soft.failures == []

    def test_context_manager_entry_exit(self):
        """Test SoftAssertions context manager entry and exit."""
        soft = SoftAssertions()

        # Before entering context
        assert soft._in_context is False

        with soft as context_soft:
            # Inside context
            assert context_soft is soft
            assert soft._in_context is True

        # After exiting context (no failures)
        assert soft._in_context is False

    def test_context_manager_exit_with_failures_raises_assertion_error(self):
        """
        Test that context manager exit raises AssertionError when there are
        failures.
        """
        with pytest.raises(AssertionError) as exc_info:
            with SoftAssertions() as soft:
                soft.assert_equal(1, 2, "Numbers should be equal")
                soft.assert_true(False, "Should be true")

        # Verify the exception message contains failure information
        error_message = str(exc_info.value)
        assert "Soft assertion failures (2):" in error_message
        assert "Numbers should be equal" in error_message
        assert "Should be true" in error_message

    def test_assert_equal_success(self):
        """Test assert_equal with equal values (no failure)."""
        with SoftAssertions() as soft:
            soft.assert_equal(5, 5, "Numbers should be equal")
            soft.assert_equal("hello", "hello", "Strings should be equal")
            soft.assert_equal([1, 2, 3], [1, 2, 3], "Lists should be equal")

        # No failures should be recorded
        assert len(soft.failures) == 0

    def test_assert_equal_failure(self):
        """Test assert_equal with unequal values (failure recorded)."""
        with pytest.raises(AssertionError):
            with SoftAssertions() as soft:
                soft.assert_equal(5, 10, "Numbers should be equal")

        assert len(soft.failures) == 1
        failure = soft.failures[0]
        assert failure.message == "Numbers should be equal"
        assert failure.expected == 10
        assert failure.actual == 5

    def test_assert_true_success(self):
        """Test assert_true with truthy values (no failure)."""
        with SoftAssertions() as soft:
            soft.assert_true(True, "Should be true")
            soft.assert_true(1, "Should be truthy")
            soft.assert_true("non-empty", "Should be truthy")
            soft.assert_true([1], "Should be truthy")

        assert len(soft.failures) == 0

    def test_assert_true_failure(self):
        """Test assert_true with falsy values (failure recorded)."""
        with pytest.raises(AssertionError):
            with SoftAssertions() as soft:
                soft.assert_true(False, "Should be true")

        assert len(soft.failures) == 1
        failure = soft.failures[0]
        assert failure.message == "Should be true"
        assert failure.expected is True
        assert failure.actual is False

    def test_assert_false_success(self):
        """Test assert_false with falsy values (no failure)."""
        with SoftAssertions() as soft:
            soft.assert_false(False, "Should be false")
            soft.assert_false(0, "Should be falsy")
            soft.assert_false("", "Should be falsy")
            soft.assert_false([], "Should be falsy")

        assert len(soft.failures) == 0

    def test_assert_false_failure(self):
        """Test assert_false with truthy values (failure recorded)."""
        with pytest.raises(AssertionError):
            with SoftAssertions() as soft:
                soft.assert_false(True, "Should be false")

        assert len(soft.failures) == 1
        failure = soft.failures[0]
        assert failure.message == "Should be false"
        assert failure.expected is False
        assert failure.actual is True

    def test_assert_in_success(self):
        """Test assert_in with item in container (no failure)."""
        with SoftAssertions() as soft:
            soft.assert_in(5, [1, 2, 3, 4, 5], "Number should be in list")
            soft.assert_in("hello", "hello world", "Substring should be in string")
            soft.assert_in("key", {"key": "value"}, "Key should be in dict")

        assert len(soft.failures) == 0

    def test_assert_in_failure(self):
        """Test assert_in with item not in container (failure recorded)."""
        with pytest.raises(AssertionError):
            with SoftAssertions() as soft:
                soft.assert_in(10, [1, 2, 3], "Number should be in list")

        assert len(soft.failures) == 1
        failure = soft.failures[0]
        assert failure.message == "Number should be in list"
        assert failure.expected == "10 in [1, 2, 3]"
        assert failure.actual == "10 not in [1, 2, 3]"

    def test_assert_not_in_success(self):
        """Test assert_not_in with item not in container (no failure)."""
        with SoftAssertions() as soft:
            soft.assert_not_in(10, [1, 2, 3], "Number should not be in list")
            soft.assert_not_in(
                "xyz", "hello world", "Substring should not be in string"
            )

        assert len(soft.failures) == 0

    def test_assert_not_in_failure(self):
        """Test assert_not_in with item in container (failure recorded)."""
        with pytest.raises(AssertionError):
            with SoftAssertions() as soft:
                soft.assert_not_in(2, [1, 2, 3], "Number should not be in list")

        assert len(soft.failures) == 1
        failure = soft.failures[0]
        assert failure.message == "Number should not be in list"

    def test_assert_greater_success(self):
        """Test assert_greater with greater values (no failure)."""
        with SoftAssertions() as soft:
            soft.assert_greater(10, 5, "10 should be greater than 5")
            soft.assert_greater(1.5, 1.0, "1.5 should be greater than 1.0")

        assert len(soft.failures) == 0

    def test_assert_greater_failure(self):
        """Test assert_greater with non-greater values (failure recorded)."""
        with pytest.raises(AssertionError):
            with SoftAssertions() as soft:
                soft.assert_greater(5, 10, "5 should be greater than 10")

        assert len(soft.failures) == 1
        failure = soft.failures[0]
        assert failure.message == "5 should be greater than 10"
        assert failure.expected == "> 10"
        assert failure.actual == 5

    def test_assert_less_success(self):
        """Test assert_less with lesser values (no failure)."""
        with SoftAssertions() as soft:
            soft.assert_less(5, 10, "5 should be less than 10")
            soft.assert_less(1.0, 1.5, "1.0 should be less than 1.5")

        assert len(soft.failures) == 0

    def test_assert_less_failure(self):
        """Test assert_less with non-lesser values (failure recorded)."""
        with pytest.raises(AssertionError):
            with SoftAssertions() as soft:
                soft.assert_less(10, 5, "10 should be less than 5")

        assert len(soft.failures) == 1
        failure = soft.failures[0]
        assert failure.message == "10 should be less than 5"

    def test_multiple_failures_collected(self):
        """Test that multiple failures are collected and reported."""
        with pytest.raises(AssertionError) as exc_info:
            with SoftAssertions() as soft:
                soft.assert_equal(1, 2, "First failure")
                soft.assert_true(False, "Second failure")
                soft.assert_in(10, [1, 2, 3], "Third failure")

        # Verify all failures were collected
        assert len(soft.failures) == 3

        # Verify error message contains all failures
        error_message = str(exc_info.value)
        assert "Soft assertion failures (3):" in error_message
        assert "First failure" in error_message
        assert "Second failure" in error_message
        assert "Third failure" in error_message

    def test_fail_fast_mode_raises_immediately(self):
        """
        Test that fail_fast mode raises AssertionError immediately on first
        failure.
        """
        with pytest.raises(AssertionError) as exc_info:
            with SoftAssertions(fail_fast=True) as soft:
                soft.assert_equal(1, 2, "This should fail immediately")
                soft.assert_true(True, "This should not be reached")

        # Only one failure should be recorded
        assert len(soft.failures) == 1
        assert "This should fail immediately" in str(exc_info.value)

    def test_get_failure_summary_no_failures(self):
        """Test get_failure_summary with no failures."""
        soft = SoftAssertions()
        summary = soft.get_failure_summary()
        assert summary == "No failures"

    def test_get_failure_summary_with_failures(self):
        """Test get_failure_summary with multiple failures."""
        soft = SoftAssertions()

        # Manually add failures for testing
        soft.failures.append(AssertionFailure("First failure", location="test.py:1"))
        soft.failures.append(AssertionFailure("Second failure", location="test.py:2"))

        summary = soft.get_failure_summary()
        assert "2 failure(s)" in summary
        assert "1. First failure" in summary
        assert "2. Second failure" in summary

    @pytest.mark.parametrize(
        "values,expected_failures",
        [
            ([(1, 1), (2, 2), (3, 3)], 0),  # All equal
            ([(1, 2), (3, 3), (4, 4)], 1),  # One failure
            ([(1, 2), (3, 4), (5, 6)], 3),  # All failures
        ],
    )
    def test_parametrized_assertions(self, values: list[tuple], expected_failures: int):
        """Test soft assertions with parametrized data."""
        soft = SoftAssertions()

        try:
            with soft:
                for actual, expected in values:
                    soft.assert_equal(
                        actual, expected, f"{actual} should equal {expected}"
                    )
        except AssertionError:
            pass  # Expected when there are failures

        assert len(soft.failures) == expected_failures

    def test_location_tracking_in_failures(self):
        """Test that failure location is properly tracked."""
        with pytest.raises(AssertionError):
            with SoftAssertions() as soft:
                soft.assert_equal(1, 2, "Test failure")  # This line should be tracked

        failure = soft.failures[0]
        # Location should contain this file name and approximate line number
        assert "test_utils_soft_assert.py" in failure.location
        assert re.search(r":\d+$", failure.location)  # Should end with :line_number

    def test_assertion_without_context_manager_warning(self):
        """Test behavior when assertions are called outside context manager."""
        # ASSUMPTION: SoftAssertions might have different behavior outside context
        soft = SoftAssertions()

        # This should work but might behave differently
        soft.assert_equal(1, 1, "This should pass")
        assert len(soft.failures) == 0

        # This should add to failures but not raise immediately
        soft.assert_equal(1, 2, "This should fail")
        assert len(soft.failures) == 1
