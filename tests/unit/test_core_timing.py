"""
Comprehensive unit tests for timing utilities module.

This module tests the timing utilities with extensive mocking to ensure:
- Timer class functionality and error handling
- TimingResult data class behavior
- PerformanceTracker measurement collection
- Context manager timing operations
- Smart wait and exponential backoff functions
- Performance measurement and analysis
"""

from unittest.mock import Mock, call, patch

import pytest

from pmas.core.utils.timing import (
    PerformanceTracker,
    Timer,
    TimingResult,
    exponential_backoff_wait,
    smart_wait,
    time_operation,
)


class TestTimingResult:
    """Test TimingResult data class."""

    def test_init_when_all_parameters_provided_expects_correct_setup(self):
        """Test TimingResult initialization with all parameters."""
        result = TimingResult(
            name="test_operation", duration=1.234, start_time=1000.0, end_time=1001.234
        )

        assert result.name == "test_operation"
        assert result.duration == 1.234
        assert result.start_time == 1000.0
        assert result.end_time == 1001.234

    def test_str_representation_expects_formatted_output(self):
        """Test string representation includes name and formatted duration."""
        result = TimingResult(
            name="database_query",
            duration=2.5678,
            start_time=1000.0,
            end_time=1002.5678,
        )

        str_result = str(result)

        assert "database_query" in str_result
        assert "2.568s" in str_result  # Should be formatted to 3 decimal places


class TestTimer:
    """Test Timer class functionality."""

    def test_init_when_name_provided_expects_correct_setup(self):
        """Test Timer initialization with custom name."""
        timer = Timer("custom_timer")

        assert timer.name == "custom_timer"
        assert timer.start_time is None
        assert timer.end_time is None

    def test_init_when_no_name_expects_default(self):
        """Test Timer initialization with default name."""
        timer = Timer()

        assert timer.name == "Timer"

    @patch("pmas.core.utils.timing.time.time")
    def test_start_when_called_expects_start_time_set(self, mock_time):
        """Test start method sets start_time."""
        mock_time.return_value = 1000.0
        timer = Timer("test")

        result = timer.start()

        assert timer.start_time == 1000.0
        assert result == timer  # Should return self for chaining

    @patch("pmas.core.utils.timing.time.time")
    def test_stop_when_timer_started_expects_timing_result(self, mock_time):
        """Test stop method returns TimingResult when timer was started."""
        mock_time.side_effect = [1000.0, 1002.5]  # start, stop
        timer = Timer("test_operation")
        timer.start()

        result = timer.stop()

        assert isinstance(result, TimingResult)
        assert result.name == "test_operation"
        assert result.duration == 2.5
        assert result.start_time == 1000.0
        assert result.end_time == 1002.5
        assert timer.end_time == 1002.5

    def test_stop_when_timer_not_started_expects_value_error(self):
        """Test stop method raises ValueError when timer not started."""
        timer = Timer("test")

        with pytest.raises(ValueError) as exc_info:
            timer.stop()

        assert "Timer not started" in str(exc_info.value)

    @patch("pmas.core.utils.timing.time.time")
    def test_elapsed_when_timer_started_expects_current_duration(self, mock_time):
        """Test elapsed property returns current duration."""
        mock_time.side_effect = [1000.0, 1001.5]  # start, elapsed check
        timer = Timer("test")
        timer.start()

        elapsed = timer.elapsed

        assert elapsed == 1.5

    def test_elapsed_when_timer_not_started_expects_zero(self):
        """Test elapsed property returns 0 when timer not started."""
        timer = Timer("test")

        elapsed = timer.elapsed

        assert elapsed == 0.0


class TestTimeOperationContextManager:
    """Test time_operation context manager."""

    @patch("pmas.core.utils.timing.time.time")
    def test_time_operation_when_successful_expects_timer_yielded(self, mock_time):
        """Test time_operation context manager yields timer and measures time."""
        mock_time.side_effect = [1000.0, 1002.0]  # start, stop

        with time_operation("test_operation") as timer:
            assert isinstance(timer, Timer)
            assert timer.name == "test_operation"
            assert timer.start_time == 1000.0

    @patch("pmas.core.utils.timing.time.time")
    def test_time_operation_when_exception_expects_timer_still_stopped(self, mock_time):
        """Test time_operation stops timer even when exception occurs."""
        mock_time.side_effect = [1000.0, 1001.0]  # start, stop

        with pytest.raises(ValueError):
            with time_operation("failing_operation") as timer:
                raise ValueError("Test exception")

        # Timer should still be stopped despite exception
        assert timer.end_time == 1001.0


class TestPerformanceTracker:
    """Test PerformanceTracker class functionality."""

    def test_init_expects_empty_state(self):
        """Test PerformanceTracker initialization."""
        tracker = PerformanceTracker()

        assert tracker.measurements == []
        assert tracker.active_timers == {}

    @patch("pmas.core.utils.timing.time.time")
    def test_start_timer_when_new_name_expects_timer_created(self, mock_time):
        """Test start_timer creates and starts new timer."""
        mock_time.return_value = 1000.0
        tracker = PerformanceTracker()

        timer = tracker.start_timer("operation1")

        assert isinstance(timer, Timer)
        assert timer.name == "operation1"
        assert timer.start_time == 1000.0
        assert "operation1" in tracker.active_timers

    @patch("pmas.core.utils.timing.time.time")
    def test_start_timer_when_name_exists_expects_previous_stopped(self, mock_time):
        """Test start_timer stops previous timer with same name."""
        mock_time.side_effect = [1000.0, 1001.0, 1002.0]  # start1, stop1, start2
        tracker = PerformanceTracker()

        timer1 = tracker.start_timer("operation")
        timer2 = tracker.start_timer("operation")  # Should stop timer1

        assert len(tracker.measurements) == 1
        assert tracker.measurements[0].name == "operation"
        assert tracker.measurements[0].duration == 1.0
        assert tracker.active_timers["operation"] == timer2

    @patch("pmas.core.utils.timing.time.time")
    def test_stop_timer_when_timer_exists_expects_measurement_recorded(self, mock_time):
        """Test stop_timer records measurement."""
        mock_time.side_effect = [1000.0, 1002.5]  # start, stop
        tracker = PerformanceTracker()
        tracker.start_timer("operation")

        result = tracker.stop_timer("operation")

        assert isinstance(result, TimingResult)
        assert result.name == "operation"
        assert result.duration == 2.5
        assert len(tracker.measurements) == 1
        assert tracker.measurements[0] == result
        assert "operation" not in tracker.active_timers

    def test_stop_timer_when_timer_not_exists_expects_none(self):
        """Test stop_timer returns None for non-existent timer."""
        tracker = PerformanceTracker()

        result = tracker.stop_timer("nonexistent")

        assert result is None
        assert len(tracker.measurements) == 0

    def test_get_measurements_when_no_filter_expects_all_measurements(self):
        """Test get_measurements returns all measurements without filter."""
        tracker = PerformanceTracker()
        measurement1 = TimingResult("op1", 1.0, 1000.0, 1001.0)
        measurement2 = TimingResult("op2", 2.0, 1002.0, 1004.0)
        tracker.measurements = [measurement1, measurement2]

        result = tracker.get_measurements()

        assert len(result) == 2
        assert result == [measurement1, measurement2]
        assert result is not tracker.measurements  # Should be a copy

    def test_get_measurements_when_filter_applied_expects_filtered_results(self):
        """Test get_measurements filters by name."""
        tracker = PerformanceTracker()
        measurement1 = TimingResult("database_query", 1.0, 1000.0, 1001.0)
        measurement2 = TimingResult("api_call", 2.0, 1002.0, 1004.0)
        measurement3 = TimingResult("database_update", 1.5, 1005.0, 1006.5)
        tracker.measurements = [measurement1, measurement2, measurement3]

        result = tracker.get_measurements("database")

        assert len(result) == 2
        assert measurement1 in result
        assert measurement3 in result
        assert measurement2 not in result

    def test_get_average_duration_when_measurements_exist_expects_correct_average(self):
        """Test get_average_duration calculates correct average."""
        tracker = PerformanceTracker()
        tracker.measurements = [
            TimingResult("op1", 1.0, 1000.0, 1001.0),
            TimingResult("op2", 3.0, 1002.0, 1005.0),
            TimingResult("op3", 2.0, 1006.0, 1008.0),
        ]

        average = tracker.get_average_duration()

        assert average == 2.0  # (1.0 + 3.0 + 2.0) / 3

    def test_get_average_duration_when_no_measurements_expects_zero(self):
        """Test get_average_duration returns 0 when no measurements."""
        tracker = PerformanceTracker()

        average = tracker.get_average_duration()

        assert average == 0.0

    def test_get_total_duration_when_measurements_exist_expects_sum(self):
        """Test get_total_duration calculates correct sum."""
        tracker = PerformanceTracker()
        tracker.measurements = [
            TimingResult("op1", 1.5, 1000.0, 1001.5),
            TimingResult("op2", 2.5, 1002.0, 1004.5),
            TimingResult("op3", 1.0, 1005.0, 1006.0),
        ]

        total = tracker.get_total_duration()

        assert total == 5.0  # 1.5 + 2.5 + 1.0

    def test_clear_when_called_expects_all_data_cleared(self):
        """Test clear method removes all measurements and active timers."""
        tracker = PerformanceTracker()
        tracker.measurements = [TimingResult("op1", 1.0, 1000.0, 1001.0)]
        tracker.active_timers = {"active": Timer("active")}

        tracker.clear()

        assert tracker.measurements == []
        assert tracker.active_timers == {}

    def test_summary_when_no_measurements_expects_no_measurements_message(self):
        """Test summary returns appropriate message when no measurements."""
        tracker = PerformanceTracker()

        summary = tracker.summary()

        assert "No measurements recorded" in summary

    def test_summary_when_measurements_exist_expects_formatted_summary(self):
        """Test summary returns formatted performance summary."""
        tracker = PerformanceTracker()
        tracker.measurements = [
            TimingResult("operation1", 1.5, 1000.0, 1001.5),
            TimingResult("operation2", 2.5, 1002.0, 1004.5),
        ]

        summary = tracker.summary()

        assert "Performance Summary:" in summary
        assert "operation1: 1.500s" in summary
        assert "operation2: 2.500s" in summary
        assert "Total: 4.000s" in summary
        assert "Average: 2.000s" in summary
        assert "Count: 2" in summary


class TestSmartWait:
    """Test smart_wait function."""

    @patch("pmas.core.utils.timing.time.time")
    @patch("pmas.core.utils.timing.time.sleep")
    def test_smart_wait_when_condition_met_immediately_expects_true(
        self, mock_sleep, mock_time
    ):
        """Test smart_wait returns True when condition is met immediately."""
        mock_time.side_effect = [1000.0, 1000.0]  # start, first check
        condition = Mock(return_value=True)

        result = smart_wait(condition, timeout=5.0, poll_frequency=0.5)

        assert result is True
        condition.assert_called_once()
        mock_sleep.assert_not_called()

    @patch("pmas.core.utils.timing.time.time")
    @patch("pmas.core.utils.timing.time.sleep")
    def test_smart_wait_when_condition_met_after_retries_expects_true(
        self, mock_sleep, mock_time
    ):
        """Test smart_wait returns True when condition is met after retries."""
        mock_time.side_effect = [1000.0, 1000.5, 1001.0]  # start, check1, check2
        condition = Mock(side_effect=[False, True])

        result = smart_wait(condition, timeout=5.0, poll_frequency=0.5)

        assert result is True
        assert condition.call_count == 2
        mock_sleep.assert_called_once_with(0.5)

    @patch("pmas.core.utils.timing.time.time")
    @patch("pmas.core.utils.timing.time.sleep")
    def test_smart_wait_when_timeout_reached_expects_timeout_error(
        self, mock_sleep, mock_time
    ):
        """Test smart_wait raises TimeoutError when timeout is reached."""
        mock_time.side_effect = [1000.0, 1005.1]  # start, timeout check
        condition = Mock(return_value=False)

        with pytest.raises(TimeoutError) as exc_info:
            smart_wait(condition, timeout=5.0, poll_frequency=0.5)

        assert "Condition not met within timeout" in str(exc_info.value)
        assert "(timeout: 5.0s)" in str(exc_info.value)

    @patch("pmas.core.utils.timing.time.time")
    @patch("pmas.core.utils.timing.time.sleep")
    def test_smart_wait_when_condition_raises_exception_expects_continued_polling(
        self, mock_sleep, mock_time
    ):
        """Test smart_wait continues polling when condition function raises exception."""
        mock_time.side_effect = [1000.0, 1000.5, 1001.0]  # start, check1, check2
        condition = Mock(side_effect=[Exception("Test error"), True])

        result = smart_wait(condition, timeout=5.0, poll_frequency=0.5)

        assert result is True
        assert condition.call_count == 2


class TestExponentialBackoffWait:
    """Test exponential_backoff_wait function."""

    @patch("pmas.core.utils.timing.time.sleep")
    def test_exponential_backoff_wait_when_condition_met_immediately_expects_true(
        self, mock_sleep
    ):
        """Test exponential backoff returns True when condition is met immediately."""
        condition = Mock(return_value=True)

        result = exponential_backoff_wait(condition, max_attempts=3)

        assert result is True
        condition.assert_called_once()
        mock_sleep.assert_not_called()

    @patch("pmas.core.utils.timing.time.sleep")
    def test_exponential_backoff_wait_when_condition_met_after_retries_expects_true(
        self, mock_sleep
    ):
        """Test exponential backoff with successful retry."""
        condition = Mock(side_effect=[False, False, True])

        result = exponential_backoff_wait(
            condition, max_attempts=3, base_delay=1.0, backoff_factor=2.0
        )

        assert result is True
        assert condition.call_count == 3
        # Should sleep 1.0s after first attempt, 2.0s after second
        expected_calls = [Mock(1.0), Mock(2.0)]
        mock_sleep.assert_has_calls([call(1.0), call(2.0)])

    @patch("pmas.core.utils.timing.time.sleep")
    def test_exponential_backoff_wait_when_max_delay_reached_expects_capped_delay(
        self, mock_sleep
    ):
        """Test exponential backoff respects max_delay."""
        condition = Mock(side_effect=[False, False, False, True])

        result = exponential_backoff_wait(
            condition, max_attempts=4, base_delay=5.0, max_delay=8.0, backoff_factor=2.0
        )

        assert result is True
        # Delays should be: 5.0, 8.0 (capped), 8.0 (capped)
        expected_calls = [call(5.0), call(8.0), call(8.0)]
        mock_sleep.assert_has_calls(expected_calls)

    def test_exponential_backoff_wait_when_all_attempts_fail_expects_false(self):
        """Test exponential backoff returns False when all attempts fail."""
        condition = Mock(return_value=False)

        result = exponential_backoff_wait(condition, max_attempts=3)

        assert result is False
        assert condition.call_count == 3

    @patch("pmas.core.utils.timing.time.sleep")
    def test_exponential_backoff_wait_when_condition_raises_exception_expects_continued(
        self, mock_sleep
    ):
        """Test exponential backoff continues when condition raises exception."""
        condition = Mock(side_effect=[Exception("Error"), False, True])

        result = exponential_backoff_wait(condition, max_attempts=3, base_delay=0.1)

        assert result is True
        assert condition.call_count == 3
