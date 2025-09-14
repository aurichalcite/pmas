"""
Timing utilities for performance measurement and delays.
"""

import logging
import time
from contextlib import contextmanager
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class TimingResult:
    """Result of a timing measurement."""

    name: str
    duration: float
    start_time: float
    end_time: float

    def __str__(self) -> str:
        return f"{self.name}: {self.duration:.3f}s"


class Timer:
    """Simple timer for measuring execution time."""

    def __init__(self, name: str = "Timer") -> None:
        self.name = name
        self.start_time: float | None = None
        self.end_time: float | None = None

    def start(self) -> "Timer":
        """Start the timer."""
        self.start_time = time.time()
        logger.debug(f"Started timer: {self.name}")
        return self

    def stop(self) -> TimingResult:
        """Stop the timer and return the result."""
        if self.start_time is None:
            raise ValueError("Timer not started")

        self.end_time = time.time()
        duration = self.end_time - self.start_time

        result = TimingResult(
            name=self.name,
            duration=duration,
            start_time=self.start_time,
            end_time=self.end_time,
        )

        logger.debug(f"Stopped timer: {result}")
        return result

    @property
    def elapsed(self) -> float:
        """Get elapsed time without stopping the timer."""
        if self.start_time is None:
            return 0.0
        return time.time() - self.start_time


@contextmanager
def time_operation(name: str = "Operation"):
    """Context manager for timing operations."""
    timer = Timer(name)
    timer.start()
    try:
        yield timer
    finally:
        result = timer.stop()
        logger.info(f"Timed operation: {result}")


class PerformanceTracker:
    """Track multiple timing measurements for performance analysis."""

    def __init__(self) -> None:
        self.measurements: list[TimingResult] = []
        self.active_timers: dict[str, Timer] = {}

    def start_timer(self, name: str) -> Timer:
        """Start a named timer."""
        if name in self.active_timers:
            logger.warning(f"Timer '{name}' already active, stopping previous")
            self.stop_timer(name)

        timer = Timer(name)
        timer.start()
        self.active_timers[name] = timer
        return timer

    def stop_timer(self, name: str) -> TimingResult | None:
        """Stop a named timer and record the result."""
        timer = self.active_timers.pop(name, None)
        if timer is None:
            logger.warning(f"No active timer named '{name}'")
            return None

        result = timer.stop()
        self.measurements.append(result)
        return result

    def get_measurements(self, name_filter: str | None = None) -> list[TimingResult]:
        """Get all measurements, optionally filtered by name."""
        if name_filter is None:
            return self.measurements.copy()
        return [m for m in self.measurements if name_filter in m.name]

    def get_average_duration(self, name_filter: str | None = None) -> float:
        """Get average duration for measurements."""
        measurements = self.get_measurements(name_filter)
        if not measurements:
            return 0.0
        return sum(m.duration for m in measurements) / len(measurements)

    def get_total_duration(self, name_filter: str | None = None) -> float:
        """Get total duration for measurements."""
        measurements = self.get_measurements(name_filter)
        return sum(m.duration for m in measurements)

    def clear(self) -> None:
        """Clear all measurements and stop active timers."""
        self.measurements.clear()
        self.active_timers.clear()

    def summary(self) -> str:
        """Get a summary of all measurements."""
        if not self.measurements:
            return "No measurements recorded"

        lines = ["Performance Summary:"]
        lines.append("-" * 40)

        for measurement in self.measurements:
            lines.append(f"  {measurement}")

        lines.append("-" * 40)
        lines.append(f"  Total: {self.get_total_duration():.3f}s")
        lines.append(f"  Average: {self.get_average_duration():.3f}s")
        lines.append(f"  Count: {len(self.measurements)}")

        return "\n".join(lines)


def smart_wait(
    condition_func,
    timeout: float = 10.0,
    poll_frequency: float = 0.5,
    error_message: str = "Condition not met within timeout",
) -> bool:
    """
    Smart wait function that polls a condition until it's true or timeout.

    Args:
        condition_func: Function that returns True when condition is met
        timeout: Maximum time to wait in seconds
        poll_frequency: How often to check the condition in seconds
        error_message: Error message if timeout is reached

    Returns:
        True if condition was met, False if timeout

    Raises:
        TimeoutError: If timeout is reached and condition not met
    """
    start_time = time.time()

    while time.time() - start_time < timeout:
        try:
            if condition_func():
                return True
        except Exception as e:
            logger.debug(f"Condition check failed: {e}")

        time.sleep(poll_frequency)

    raise TimeoutError(f"{error_message} (timeout: {timeout}s)")


def exponential_backoff_wait(
    condition_func,
    max_attempts: int = 5,
    base_delay: float = 1.0,
    max_delay: float = 30.0,
    backoff_factor: float = 2.0,
) -> bool:
    """
    Wait with exponential backoff between attempts.

    Args:
        condition_func: Function that returns True when condition is met
        max_attempts: Maximum number of attempts
        base_delay: Initial delay between attempts
        max_delay: Maximum delay between attempts
        backoff_factor: Factor to multiply delay by each attempt

    Returns:
        True if condition was met, False if all attempts failed
    """
    delay = base_delay

    for attempt in range(max_attempts):
        try:
            if condition_func():
                return True
        except Exception as e:
            logger.debug(f"Attempt {attempt + 1} failed: {e}")

        if attempt < max_attempts - 1:  # Don't wait after last attempt
            actual_delay = min(delay, max_delay)
            logger.debug(f"Waiting {actual_delay}s before attempt {attempt + 2}")
            time.sleep(actual_delay)
            delay *= backoff_factor

    return False
