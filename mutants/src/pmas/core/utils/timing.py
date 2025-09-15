"""
Timing utilities for performance measurement and delays.
"""

import logging
import time
from collections.abc import Callable
from contextlib import contextmanager
from dataclasses import dataclass
from inspect import signature as _mutmut_signature
from typing import Annotated, ClassVar

logger = logging.getLogger(__name__)


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

    def xǁTimerǁ__init____mutmut_orig(self, name: str = "Timer") -> None:
        self.name = name
        self.start_time: float | None = None
        self.end_time: float | None = None

    def xǁTimerǁ__init____mutmut_1(self, name: str = "XXTimerXX") -> None:
        self.name = name
        self.start_time: float | None = None
        self.end_time: float | None = None

    def xǁTimerǁ__init____mutmut_2(self, name: str = "timer") -> None:
        self.name = name
        self.start_time: float | None = None
        self.end_time: float | None = None

    def xǁTimerǁ__init____mutmut_3(self, name: str = "TIMER") -> None:
        self.name = name
        self.start_time: float | None = None
        self.end_time: float | None = None

    def xǁTimerǁ__init____mutmut_4(self, name: str = "Timer") -> None:
        self.name = None
        self.start_time: float | None = None
        self.end_time: float | None = None

    def xǁTimerǁ__init____mutmut_5(self, name: str = "Timer") -> None:
        self.name = name
        self.start_time: float | None = ""
        self.end_time: float | None = None

    def xǁTimerǁ__init____mutmut_6(self, name: str = "Timer") -> None:
        self.name = name
        self.start_time: float | None = None
        self.end_time: float | None = ""

    xǁTimerǁ__init____mutmut_mutants: ClassVar[MutantDict] = {
        "xǁTimerǁ__init____mutmut_1": xǁTimerǁ__init____mutmut_1,
        "xǁTimerǁ__init____mutmut_2": xǁTimerǁ__init____mutmut_2,
        "xǁTimerǁ__init____mutmut_3": xǁTimerǁ__init____mutmut_3,
        "xǁTimerǁ__init____mutmut_4": xǁTimerǁ__init____mutmut_4,
        "xǁTimerǁ__init____mutmut_5": xǁTimerǁ__init____mutmut_5,
        "xǁTimerǁ__init____mutmut_6": xǁTimerǁ__init____mutmut_6,
    }

    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁTimerǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁTimerǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    __init__.__signature__ = _mutmut_signature(xǁTimerǁ__init____mutmut_orig)
    xǁTimerǁ__init____mutmut_orig.__name__ = "xǁTimerǁ__init__"

    def xǁTimerǁstart__mutmut_orig(self) -> "Timer":
        """Start the timer."""
        self.start_time = time.time()
        logger.debug(f"Started timer: {self.name}")
        return self

    def xǁTimerǁstart__mutmut_1(self) -> "Timer":
        """Start the timer."""
        self.start_time = None
        logger.debug(f"Started timer: {self.name}")
        return self

    def xǁTimerǁstart__mutmut_2(self) -> "Timer":
        """Start the timer."""
        self.start_time = time.time()
        logger.debug(None)
        return self

    xǁTimerǁstart__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁTimerǁstart__mutmut_1": xǁTimerǁstart__mutmut_1,
        "xǁTimerǁstart__mutmut_2": xǁTimerǁstart__mutmut_2,
    }

    def start(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁTimerǁstart__mutmut_orig"),
            object.__getattribute__(self, "xǁTimerǁstart__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    start.__signature__ = _mutmut_signature(xǁTimerǁstart__mutmut_orig)
    xǁTimerǁstart__mutmut_orig.__name__ = "xǁTimerǁstart"

    def xǁTimerǁstop__mutmut_orig(self) -> TimingResult:
        """Stop the timer and return the result."""
        if self.start_time is None:
            raise ValueError("Timer not started")

        self.end_time = time.time()
        _duration = self.end_time - self.start_time

        result = TimingResult(
            name=self.name,
            duration=duration,
            start_time=self.start_time,
            end_time=self.end_time,
        )

        logger.debug(f"Stopped timer: {result}")
        return result

    def xǁTimerǁstop__mutmut_1(self) -> TimingResult:
        """Stop the timer and return the result."""
        if self.start_time is not None:
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

    def xǁTimerǁstop__mutmut_2(self) -> TimingResult:
        """Stop the timer and return the result."""
        if self.start_time is None:
            raise ValueError(None)

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

    def xǁTimerǁstop__mutmut_3(self) -> TimingResult:
        """Stop the timer and return the result."""
        if self.start_time is None:
            raise ValueError("XXTimer not startedXX")

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

    def xǁTimerǁstop__mutmut_4(self) -> TimingResult:
        """Stop the timer and return the result."""
        if self.start_time is None:
            raise ValueError("timer not started")

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

    def xǁTimerǁstop__mutmut_5(self) -> TimingResult:
        """Stop the timer and return the result."""
        if self.start_time is None:
            raise ValueError("TIMER NOT STARTED")

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

    def xǁTimerǁstop__mutmut_6(self) -> TimingResult:
        """Stop the timer and return the result."""
        if self.start_time is None:
            raise ValueError("Timer not started")

        self.end_time = None
        duration = self.end_time - self.start_time

        result = TimingResult(
            name=self.name,
            duration=duration,
            start_time=self.start_time,
            end_time=self.end_time,
        )

        logger.debug(f"Stopped timer: {result}")
        return result

    def xǁTimerǁstop__mutmut_7(self) -> TimingResult:
        """Stop the timer and return the result."""
        if self.start_time is None:
            raise ValueError("Timer not started")

        self.end_time = time.time()
        duration = None

        result = TimingResult(
            name=self.name,
            duration=duration,
            start_time=self.start_time,
            end_time=self.end_time,
        )

        logger.debug(f"Stopped timer: {result}")
        return result

    def xǁTimerǁstop__mutmut_8(self) -> TimingResult:
        """Stop the timer and return the result."""
        if self.start_time is None:
            raise ValueError("Timer not started")

        self.end_time = time.time()
        duration = self.end_time + self.start_time

        result = TimingResult(
            name=self.name,
            duration=duration,
            start_time=self.start_time,
            end_time=self.end_time,
        )

        logger.debug(f"Stopped timer: {result}")
        return result

    def xǁTimerǁstop__mutmut_9(self) -> TimingResult:
        """Stop the timer and return the result."""
        if self.start_time is None:
            raise ValueError("Timer not started")

        self.end_time = time.time()
        _duration = self.end_time - self.start_time

        result = None

        logger.debug(f"Stopped timer: {result}")
        return result

    def xǁTimerǁstop__mutmut_10(self) -> TimingResult:
        """Stop the timer and return the result."""
        if self.start_time is None:
            raise ValueError("Timer not started")

        self.end_time = time.time()
        duration = self.end_time - self.start_time

        result = TimingResult(
            name=None,
            duration=duration,
            start_time=self.start_time,
            end_time=self.end_time,
        )

        logger.debug(f"Stopped timer: {result}")
        return result

    def xǁTimerǁstop__mutmut_11(self) -> TimingResult:
        """Stop the timer and return the result."""
        if self.start_time is None:
            raise ValueError("Timer not started")

        self.end_time = time.time()
        duration = self.end_time - self.start_time

        result = TimingResult(
            name=self.name,
            duration=None,
            start_time=self.start_time,
            end_time=self.end_time,
        )

        logger.debug(f"Stopped timer: {result}")
        return result

    def xǁTimerǁstop__mutmut_12(self) -> TimingResult:
        """Stop the timer and return the result."""
        if self.start_time is None:
            raise ValueError("Timer not started")

        self.end_time = time.time()
        duration = self.end_time - self.start_time

        result = TimingResult(
            name=self.name,
            duration=duration,
            start_time=None,
            end_time=self.end_time,
        )

        logger.debug(f"Stopped timer: {result}")
        return result

    def xǁTimerǁstop__mutmut_13(self) -> TimingResult:
        """Stop the timer and return the result."""
        if self.start_time is None:
            raise ValueError("Timer not started")

        self.end_time = time.time()
        duration = self.end_time - self.start_time

        result = TimingResult(
            name=self.name,
            duration=duration,
            start_time=self.start_time,
            end_time=None,
        )

        logger.debug(f"Stopped timer: {result}")
        return result

    def xǁTimerǁstop__mutmut_14(self) -> TimingResult:
        """Stop the timer and return the result."""
        if self.start_time is None:
            raise ValueError("Timer not started")

        self.end_time = time.time()
        duration = self.end_time - self.start_time

        result = TimingResult(
            duration=duration,
            start_time=self.start_time,
            end_time=self.end_time,
        )

        logger.debug(f"Stopped timer: {result}")
        return result

    def xǁTimerǁstop__mutmut_15(self) -> TimingResult:
        """Stop the timer and return the result."""
        if self.start_time is None:
            raise ValueError("Timer not started")

        self.end_time = time.time()
        duration = self.end_time - self.start_time

        result = TimingResult(
            name=self.name,
            start_time=self.start_time,
            end_time=self.end_time,
        )

        logger.debug(f"Stopped timer: {result}")
        return result

    def xǁTimerǁstop__mutmut_16(self) -> TimingResult:
        """Stop the timer and return the result."""
        if self.start_time is None:
            raise ValueError("Timer not started")

        self.end_time = time.time()
        duration = self.end_time - self.start_time

        result = TimingResult(
            name=self.name,
            duration=duration,
            end_time=self.end_time,
        )

        logger.debug(f"Stopped timer: {result}")
        return result

    def xǁTimerǁstop__mutmut_17(self) -> TimingResult:
        """Stop the timer and return the result."""
        if self.start_time is None:
            raise ValueError("Timer not started")

        self.end_time = time.time()
        duration = self.end_time - self.start_time

        result = TimingResult(
            name=self.name,
            duration=duration,
            start_time=self.start_time,
        )

        logger.debug(f"Stopped timer: {result}")
        return result

    def xǁTimerǁstop__mutmut_18(self) -> TimingResult:
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

        logger.debug(None)
        return result

    xǁTimerǁstop__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁTimerǁstop__mutmut_1": xǁTimerǁstop__mutmut_1,
        "xǁTimerǁstop__mutmut_2": xǁTimerǁstop__mutmut_2,
        "xǁTimerǁstop__mutmut_3": xǁTimerǁstop__mutmut_3,
        "xǁTimerǁstop__mutmut_4": xǁTimerǁstop__mutmut_4,
        "xǁTimerǁstop__mutmut_5": xǁTimerǁstop__mutmut_5,
        "xǁTimerǁstop__mutmut_6": xǁTimerǁstop__mutmut_6,
        "xǁTimerǁstop__mutmut_7": xǁTimerǁstop__mutmut_7,
        "xǁTimerǁstop__mutmut_8": xǁTimerǁstop__mutmut_8,
        "xǁTimerǁstop__mutmut_9": xǁTimerǁstop__mutmut_9,
        "xǁTimerǁstop__mutmut_10": xǁTimerǁstop__mutmut_10,
        "xǁTimerǁstop__mutmut_11": xǁTimerǁstop__mutmut_11,
        "xǁTimerǁstop__mutmut_12": xǁTimerǁstop__mutmut_12,
        "xǁTimerǁstop__mutmut_13": xǁTimerǁstop__mutmut_13,
        "xǁTimerǁstop__mutmut_14": xǁTimerǁstop__mutmut_14,
        "xǁTimerǁstop__mutmut_15": xǁTimerǁstop__mutmut_15,
        "xǁTimerǁstop__mutmut_16": xǁTimerǁstop__mutmut_16,
        "xǁTimerǁstop__mutmut_17": xǁTimerǁstop__mutmut_17,
        "xǁTimerǁstop__mutmut_18": xǁTimerǁstop__mutmut_18,
    }

    def stop(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁTimerǁstop__mutmut_orig"),
            object.__getattribute__(self, "xǁTimerǁstop__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    stop.__signature__ = _mutmut_signature(xǁTimerǁstop__mutmut_orig)
    xǁTimerǁstop__mutmut_orig.__name__ = "xǁTimerǁstop"

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

    def xǁPerformanceTrackerǁ__init____mutmut_orig(self) -> None:
        self.measurements: list[TimingResult] = []
        self.active_timers: dict[str, Timer] = {}

    def xǁPerformanceTrackerǁ__init____mutmut_1(self) -> None:
        self.measurements: list[TimingResult] = None
        self.active_timers: dict[str, Timer] = {}

    def xǁPerformanceTrackerǁ__init____mutmut_2(self) -> None:
        self.measurements: list[TimingResult] = []
        self.active_timers: dict[str, Timer] = None

    xǁPerformanceTrackerǁ__init____mutmut_mutants: ClassVar[MutantDict] = {
        "xǁPerformanceTrackerǁ__init____mutmut_1": (
            xǁPerformanceTrackerǁ__init____mutmut_1
        ),
        "xǁPerformanceTrackerǁ__init____mutmut_2": (
            xǁPerformanceTrackerǁ__init____mutmut_2
        ),
    }

    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁPerformanceTrackerǁ__init____mutmut_orig"),
            object.__getattribute__(
                self, "xǁPerformanceTrackerǁ__init____mutmut_mutants"
            ),
            args,
            kwargs,
            self,
        )
        return result

    __init__.__signature__ = _mutmut_signature(
        xǁPerformanceTrackerǁ__init____mutmut_orig
    )
    xǁPerformanceTrackerǁ__init____mutmut_orig.__name__ = (
        "xǁPerformanceTrackerǁ__init__"
    )

    def xǁPerformanceTrackerǁstart_timer__mutmut_orig(self, name: str) -> Timer:
        """Start a named timer."""
        if name in self.active_timers:
            logger.warning(f"Timer '{name}' already active, stopping previous")
            self.stop_timer(name)

        timer = Timer(name)
        timer.start()
        self.active_timers[name] = timer
        return timer

    def xǁPerformanceTrackerǁstart_timer__mutmut_1(self, name: str) -> Timer:
        """Start a named timer."""
        if name not in self.active_timers:
            logger.warning(f"Timer '{name}' already active, stopping previous")
            self.stop_timer(name)

        timer = Timer(name)
        timer.start()
        self.active_timers[name] = timer
        return timer

    def xǁPerformanceTrackerǁstart_timer__mutmut_2(self, name: str) -> Timer:
        """Start a named timer."""
        if name in self.active_timers:
            logger.warning(None)
            self.stop_timer(name)

        timer = Timer(name)
        timer.start()
        self.active_timers[name] = timer
        return timer

    def xǁPerformanceTrackerǁstart_timer__mutmut_3(self, name: str) -> Timer:
        """Start a named timer."""
        if name in self.active_timers:
            logger.warning(f"Timer '{name}' already active, stopping previous")
            self.stop_timer(None)

        timer = Timer(name)
        timer.start()
        self.active_timers[name] = timer
        return timer

    def xǁPerformanceTrackerǁstart_timer__mutmut_4(self, name: str) -> Timer:
        """Start a named timer."""
        if name in self.active_timers:
            logger.warning(f"Timer '{name}' already active, stopping previous")
            self.stop_timer(name)

        timer = None
        timer.start()
        self.active_timers[name] = timer
        return timer

    def xǁPerformanceTrackerǁstart_timer__mutmut_5(self, name: str) -> Timer:
        """Start a named timer."""
        if name in self.active_timers:
            logger.warning(f"Timer '{name}' already active, stopping previous")
            self.stop_timer(name)

        timer = Timer(None)
        timer.start()
        self.active_timers[name] = timer
        return timer

    def xǁPerformanceTrackerǁstart_timer__mutmut_6(self, name: str) -> Timer:
        """Start a named timer."""
        if name in self.active_timers:
            logger.warning(f"Timer '{name}' already active, stopping previous")
            self.stop_timer(name)

        timer = Timer(name)
        timer.start()
        self.active_timers[name] = None
        return timer

    xǁPerformanceTrackerǁstart_timer__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁPerformanceTrackerǁstart_timer__mutmut_1": (
            xǁPerformanceTrackerǁstart_timer__mutmut_1
        ),
        "xǁPerformanceTrackerǁstart_timer__mutmut_2": (
            xǁPerformanceTrackerǁstart_timer__mutmut_2
        ),
        "xǁPerformanceTrackerǁstart_timer__mutmut_3": (
            xǁPerformanceTrackerǁstart_timer__mutmut_3
        ),
        "xǁPerformanceTrackerǁstart_timer__mutmut_4": (
            xǁPerformanceTrackerǁstart_timer__mutmut_4
        ),
        "xǁPerformanceTrackerǁstart_timer__mutmut_5": (
            xǁPerformanceTrackerǁstart_timer__mutmut_5
        ),
        "xǁPerformanceTrackerǁstart_timer__mutmut_6": (
            xǁPerformanceTrackerǁstart_timer__mutmut_6
        ),
    }

    def start_timer(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(
                self, "xǁPerformanceTrackerǁstart_timer__mutmut_orig"
            ),
            object.__getattribute__(
                self, "xǁPerformanceTrackerǁstart_timer__mutmut_mutants"
            ),
            args,
            kwargs,
            self,
        )
        return result

    start_timer.__signature__ = _mutmut_signature(
        xǁPerformanceTrackerǁstart_timer__mutmut_orig
    )
    xǁPerformanceTrackerǁstart_timer__mutmut_orig.__name__ = (
        "xǁPerformanceTrackerǁstart_timer"
    )

    def xǁPerformanceTrackerǁstop_timer__mutmut_orig(
        self, name: str
    ) -> TimingResult | None:
        """Stop a named timer and record the result."""
        timer = self.active_timers.pop(name, None)
        if timer is None:
            logger.warning(f"No active timer named '{name}'")
            return None

        result = timer.stop()
        self.measurements.append(result)
        return result

    def xǁPerformanceTrackerǁstop_timer__mutmut_1(
        self, name: str
    ) -> TimingResult | None:
        """Stop a named timer and record the result."""
        timer = None
        if timer is None:
            logger.warning(f"No active timer named '{name}'")
            return None

        result = timer.stop()
        self.measurements.append(result)
        return result

    def xǁPerformanceTrackerǁstop_timer__mutmut_2(
        self, name: str
    ) -> TimingResult | None:
        """Stop a named timer and record the result."""
        timer = self.active_timers.pop(None, None)
        if timer is None:
            logger.warning(f"No active timer named '{name}'")
            return None

        result = timer.stop()
        self.measurements.append(result)
        return result

    def xǁPerformanceTrackerǁstop_timer__mutmut_3(
        self, name: str
    ) -> TimingResult | None:
        """Stop a named timer and record the result."""
        timer = self.active_timers.pop(None)
        if timer is None:
            logger.warning(f"No active timer named '{name}'")
            return None

        result = timer.stop()
        self.measurements.append(result)
        return result

    def xǁPerformanceTrackerǁstop_timer__mutmut_4(
        self, name: str
    ) -> TimingResult | None:
        """Stop a named timer and record the result."""
        timer = self.active_timers.pop(
            name,
        )
        if timer is None:
            logger.warning(f"No active timer named '{name}'")
            return None

        result = timer.stop()
        self.measurements.append(result)
        return result

    def xǁPerformanceTrackerǁstop_timer__mutmut_5(
        self, name: str
    ) -> TimingResult | None:
        """Stop a named timer and record the result."""
        timer = self.active_timers.pop(name, None)
        if timer is not None:
            logger.warning(f"No active timer named '{name}'")
            return None

        result = timer.stop()
        self.measurements.append(result)
        return result

    def xǁPerformanceTrackerǁstop_timer__mutmut_6(
        self, name: str
    ) -> TimingResult | None:
        """Stop a named timer and record the result."""
        timer = self.active_timers.pop(name, None)
        if timer is None:
            logger.warning(None)
            return None

        result = timer.stop()
        self.measurements.append(result)
        return result

    def xǁPerformanceTrackerǁstop_timer__mutmut_7(
        self, name: str
    ) -> TimingResult | None:
        """Stop a named timer and record the result."""
        timer = self.active_timers.pop(name, None)
        if timer is None:
            logger.warning(f"No active timer named '{name}'")
            return None

        result = None
        self.measurements.append(result)
        return result

    def xǁPerformanceTrackerǁstop_timer__mutmut_8(
        self, name: str
    ) -> TimingResult | None:
        """Stop a named timer and record the result."""
        timer = self.active_timers.pop(name, None)
        if timer is None:
            logger.warning(f"No active timer named '{name}'")
            return None

        result = timer.stop()
        self.measurements.append(None)
        return result

    xǁPerformanceTrackerǁstop_timer__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁPerformanceTrackerǁstop_timer__mutmut_1": (
            xǁPerformanceTrackerǁstop_timer__mutmut_1
        ),
        "xǁPerformanceTrackerǁstop_timer__mutmut_2": (
            xǁPerformanceTrackerǁstop_timer__mutmut_2
        ),
        "xǁPerformanceTrackerǁstop_timer__mutmut_3": (
            xǁPerformanceTrackerǁstop_timer__mutmut_3
        ),
        "xǁPerformanceTrackerǁstop_timer__mutmut_4": (
            xǁPerformanceTrackerǁstop_timer__mutmut_4
        ),
        "xǁPerformanceTrackerǁstop_timer__mutmut_5": (
            xǁPerformanceTrackerǁstop_timer__mutmut_5
        ),
        "xǁPerformanceTrackerǁstop_timer__mutmut_6": (
            xǁPerformanceTrackerǁstop_timer__mutmut_6
        ),
        "xǁPerformanceTrackerǁstop_timer__mutmut_7": (
            xǁPerformanceTrackerǁstop_timer__mutmut_7
        ),
        "xǁPerformanceTrackerǁstop_timer__mutmut_8": (
            xǁPerformanceTrackerǁstop_timer__mutmut_8
        ),
    }

    def stop_timer(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(
                self, "xǁPerformanceTrackerǁstop_timer__mutmut_orig"
            ),
            object.__getattribute__(
                self, "xǁPerformanceTrackerǁstop_timer__mutmut_mutants"
            ),
            args,
            kwargs,
            self,
        )
        return result

    stop_timer.__signature__ = _mutmut_signature(
        xǁPerformanceTrackerǁstop_timer__mutmut_orig
    )
    xǁPerformanceTrackerǁstop_timer__mutmut_orig.__name__ = (
        "xǁPerformanceTrackerǁstop_timer"
    )

    def xǁPerformanceTrackerǁget_measurements__mutmut_orig(
        self, name_filter: str | None = None
    ) -> list[TimingResult]:
        """Get all measurements, optionally filtered by name."""
        if name_filter is None:
            return self.measurements.copy()
        return [m for m in self.measurements if name_filter in m.name]

    def xǁPerformanceTrackerǁget_measurements__mutmut_1(
        self, name_filter: str | None = None
    ) -> list[TimingResult]:
        """Get all measurements, optionally filtered by name."""
        if name_filter is not None:
            return self.measurements.copy()
        return [m for m in self.measurements if name_filter in m.name]

    def xǁPerformanceTrackerǁget_measurements__mutmut_2(
        self, name_filter: str | None = None
    ) -> list[TimingResult]:
        """Get all measurements, optionally filtered by name."""
        if name_filter is None:
            return self.measurements.copy()
        return [m for m in self.measurements if name_filter not in m.name]

    xǁPerformanceTrackerǁget_measurements__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁPerformanceTrackerǁget_measurements__mutmut_1": (
            xǁPerformanceTrackerǁget_measurements__mutmut_1
        ),
        "xǁPerformanceTrackerǁget_measurements__mutmut_2": (
            xǁPerformanceTrackerǁget_measurements__mutmut_2
        ),
    }

    def get_measurements(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(
                self, "xǁPerformanceTrackerǁget_measurements__mutmut_orig"
            ),
            object.__getattribute__(
                self, "xǁPerformanceTrackerǁget_measurements__mutmut_mutants"
            ),
            args,
            kwargs,
            self,
        )
        return result

    get_measurements.__signature__ = _mutmut_signature(
        xǁPerformanceTrackerǁget_measurements__mutmut_orig
    )
    xǁPerformanceTrackerǁget_measurements__mutmut_orig.__name__ = (
        "xǁPerformanceTrackerǁget_measurements"
    )

    def xǁPerformanceTrackerǁget_average_duration__mutmut_orig(
        self, name_filter: str | None = None
    ) -> float:
        """Get average duration for measurements."""
        measurements = self.get_measurements(name_filter)
        if not measurements:
            return 0.0
        return sum(m.duration for m in measurements) / len(measurements)

    def xǁPerformanceTrackerǁget_average_duration__mutmut_1(
        self, name_filter: str | None = None
    ) -> float:
        """Get average duration for measurements."""
        measurements = None
        if not measurements:
            return 0.0
        return sum(m.duration for m in measurements) / len(measurements)

    def xǁPerformanceTrackerǁget_average_duration__mutmut_2(
        self, name_filter: str | None = None
    ) -> float:
        """Get average duration for measurements."""
        measurements = self.get_measurements(None)
        if not measurements:
            return 0.0
        return sum(m.duration for m in measurements) / len(measurements)

    def xǁPerformanceTrackerǁget_average_duration__mutmut_3(
        self, name_filter: str | None = None
    ) -> float:
        """Get average duration for measurements."""
        measurements = self.get_measurements(name_filter)
        if measurements:
            return 0.0
        return sum(m.duration for m in measurements) / len(measurements)

    def xǁPerformanceTrackerǁget_average_duration__mutmut_4(
        self, name_filter: str | None = None
    ) -> float:
        """Get average duration for measurements."""
        measurements = self.get_measurements(name_filter)
        if not measurements:
            return 1.0
        return sum(m.duration for m in measurements) / len(measurements)

    def xǁPerformanceTrackerǁget_average_duration__mutmut_5(
        self, name_filter: str | None = None
    ) -> float:
        """Get average duration for measurements."""
        measurements = self.get_measurements(name_filter)
        if not measurements:
            return 0.0
        return sum(m.duration for m in measurements) * len(measurements)

    def xǁPerformanceTrackerǁget_average_duration__mutmut_6(
        self, name_filter: str | None = None
    ) -> float:
        """Get average duration for measurements."""
        measurements = self.get_measurements(name_filter)
        if not measurements:
            return 0.0
        return sum(None) / len(measurements)

    xǁPerformanceTrackerǁget_average_duration__mutmut_mutants: ClassVar[
        MutantDict
    ] = {
        "xǁPerformanceTrackerǁget_average_duration__mutmut_1": (
            xǁPerformanceTrackerǁget_average_duration__mutmut_1
        ),
        "xǁPerformanceTrackerǁget_average_duration__mutmut_2": (
            xǁPerformanceTrackerǁget_average_duration__mutmut_2
        ),
        "xǁPerformanceTrackerǁget_average_duration__mutmut_3": (
            xǁPerformanceTrackerǁget_average_duration__mutmut_3
        ),
        "xǁPerformanceTrackerǁget_average_duration__mutmut_4": (
            xǁPerformanceTrackerǁget_average_duration__mutmut_4
        ),
        "xǁPerformanceTrackerǁget_average_duration__mutmut_5": (
            xǁPerformanceTrackerǁget_average_duration__mutmut_5
        ),
        "xǁPerformanceTrackerǁget_average_duration__mutmut_6": (
            xǁPerformanceTrackerǁget_average_duration__mutmut_6
        ),
    }

    def get_average_duration(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(
                self, "xǁPerformanceTrackerǁget_average_duration__mutmut_orig"
            ),
            object.__getattribute__(
                self, "xǁPerformanceTrackerǁget_average_duration__mutmut_mutants"
            ),
            args,
            kwargs,
            self,
        )
        return result

    get_average_duration.__signature__ = _mutmut_signature(
        xǁPerformanceTrackerǁget_average_duration__mutmut_orig
    )
    xǁPerformanceTrackerǁget_average_duration__mutmut_orig.__name__ = (
        "xǁPerformanceTrackerǁget_average_duration"
    )

    def xǁPerformanceTrackerǁget_total_duration__mutmut_orig(
        self, name_filter: str | None = None
    ) -> float:
        """Get total duration for measurements."""
        measurements = self.get_measurements(name_filter)
        return sum(m.duration for m in measurements)

    def xǁPerformanceTrackerǁget_total_duration__mutmut_1(
        self, name_filter: str | None = None
    ) -> float:
        """Get total duration for measurements."""
        measurements = None
        return sum(m.duration for m in measurements)

    def xǁPerformanceTrackerǁget_total_duration__mutmut_2(
        self, name_filter: str | None = None
    ) -> float:
        """Get total duration for measurements."""
        measurements = self.get_measurements(None)
        return sum(m.duration for m in measurements)

    def xǁPerformanceTrackerǁget_total_duration__mutmut_3(
        self, name_filter: str | None = None
    ) -> float:
        """Get total duration for measurements."""
        _measurements = self.get_measurements(name_filter)
        return sum(None)

    xǁPerformanceTrackerǁget_total_duration__mutmut_mutants: ClassVar[
        MutantDict
    ] = {
        "xǁPerformanceTrackerǁget_total_duration__mutmut_1": (
            xǁPerformanceTrackerǁget_total_duration__mutmut_1
        ),
        "xǁPerformanceTrackerǁget_total_duration__mutmut_2": (
            xǁPerformanceTrackerǁget_total_duration__mutmut_2
        ),
        "xǁPerformanceTrackerǁget_total_duration__mutmut_3": (
            xǁPerformanceTrackerǁget_total_duration__mutmut_3
        ),
    }

    def get_total_duration(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(
                self, "xǁPerformanceTrackerǁget_total_duration__mutmut_orig"
            ),
            object.__getattribute__(
                self, "xǁPerformanceTrackerǁget_total_duration__mutmut_mutants"
            ),
            args,
            kwargs,
            self,
        )
        return result

    get_total_duration.__signature__ = _mutmut_signature(
        xǁPerformanceTrackerǁget_total_duration__mutmut_orig
    )
    xǁPerformanceTrackerǁget_total_duration__mutmut_orig.__name__ = (
        "xǁPerformanceTrackerǁget_total_duration"
    )

    def clear(self) -> None:
        """Clear all measurements and stop active timers."""
        self.measurements.clear()
        self.active_timers.clear()

    def xǁPerformanceTrackerǁsummary__mutmut_orig(self) -> str:
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

    def xǁPerformanceTrackerǁsummary__mutmut_1(self) -> str:
        """Get a summary of all measurements."""
        if self.measurements:
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

    def xǁPerformanceTrackerǁsummary__mutmut_2(self) -> str:
        """Get a summary of all measurements."""
        if not self.measurements:
            return "XXNo measurements recordedXX"

        lines = ["Performance Summary:"]
        lines.append("-" * 40)

        for measurement in self.measurements:
            lines.append(f"  {measurement}")

        lines.append("-" * 40)
        lines.append(f"  Total: {self.get_total_duration():.3f}s")
        lines.append(f"  Average: {self.get_average_duration():.3f}s")
        lines.append(f"  Count: {len(self.measurements)}")

        return "\n".join(lines)

    def xǁPerformanceTrackerǁsummary__mutmut_3(self) -> str:
        """Get a summary of all measurements."""
        if not self.measurements:
            return "no measurements recorded"

        lines = ["Performance Summary:"]
        lines.append("-" * 40)

        for measurement in self.measurements:
            lines.append(f"  {measurement}")

        lines.append("-" * 40)
        lines.append(f"  Total: {self.get_total_duration():.3f}s")
        lines.append(f"  Average: {self.get_average_duration():.3f}s")
        lines.append(f"  Count: {len(self.measurements)}")

        return "\n".join(lines)

    def xǁPerformanceTrackerǁsummary__mutmut_4(self) -> str:
        """Get a summary of all measurements."""
        if not self.measurements:
            return "NO MEASUREMENTS RECORDED"

        lines = ["Performance Summary:"]
        lines.append("-" * 40)

        for measurement in self.measurements:
            lines.append(f"  {measurement}")

        lines.append("-" * 40)
        lines.append(f"  Total: {self.get_total_duration():.3f}s")
        lines.append(f"  Average: {self.get_average_duration():.3f}s")
        lines.append(f"  Count: {len(self.measurements)}")

        return "\n".join(lines)

    def xǁPerformanceTrackerǁsummary__mutmut_5(self) -> str:
        """Get a summary of all measurements."""
        if not self.measurements:
            return "No measurements recorded"

        lines = None
        lines.append("-" * 40)

        for measurement in self.measurements:
            lines.append(f"  {measurement}")

        lines.append("-" * 40)
        lines.append(f"  Total: {self.get_total_duration():.3f}s")
        lines.append(f"  Average: {self.get_average_duration():.3f}s")
        lines.append(f"  Count: {len(self.measurements)}")

        return "\n".join(lines)

    def xǁPerformanceTrackerǁsummary__mutmut_6(self) -> str:
        """Get a summary of all measurements."""
        if not self.measurements:
            return "No measurements recorded"

        lines = ["XXPerformance Summary:XX"]
        lines.append("-" * 40)

        for measurement in self.measurements:
            lines.append(f"  {measurement}")

        lines.append("-" * 40)
        lines.append(f"  Total: {self.get_total_duration():.3f}s")
        lines.append(f"  Average: {self.get_average_duration():.3f}s")
        lines.append(f"  Count: {len(self.measurements)}")

        return "\n".join(lines)

    def xǁPerformanceTrackerǁsummary__mutmut_7(self) -> str:
        """Get a summary of all measurements."""
        if not self.measurements:
            return "No measurements recorded"

        lines = ["performance summary:"]
        lines.append("-" * 40)

        for measurement in self.measurements:
            lines.append(f"  {measurement}")

        lines.append("-" * 40)
        lines.append(f"  Total: {self.get_total_duration():.3f}s")
        lines.append(f"  Average: {self.get_average_duration():.3f}s")
        lines.append(f"  Count: {len(self.measurements)}")

        return "\n".join(lines)

    def xǁPerformanceTrackerǁsummary__mutmut_8(self) -> str:
        """Get a summary of all measurements."""
        if not self.measurements:
            return "No measurements recorded"

        lines = ["PERFORMANCE SUMMARY:"]
        lines.append("-" * 40)

        for measurement in self.measurements:
            lines.append(f"  {measurement}")

        lines.append("-" * 40)
        lines.append(f"  Total: {self.get_total_duration():.3f}s")
        lines.append(f"  Average: {self.get_average_duration():.3f}s")
        lines.append(f"  Count: {len(self.measurements)}")

        return "\n".join(lines)

    def xǁPerformanceTrackerǁsummary__mutmut_9(self) -> str:
        """Get a summary of all measurements."""
        if not self.measurements:
            return "No measurements recorded"

        lines = ["Performance Summary:"]
        lines.append(None)

        for measurement in self.measurements:
            lines.append(f"  {measurement}")

        lines.append("-" * 40)
        lines.append(f"  Total: {self.get_total_duration():.3f}s")
        lines.append(f"  Average: {self.get_average_duration():.3f}s")
        lines.append(f"  Count: {len(self.measurements)}")

        return "\n".join(lines)

    def xǁPerformanceTrackerǁsummary__mutmut_10(self) -> str:
        """Get a summary of all measurements."""
        if not self.measurements:
            return "No measurements recorded"

        lines = ["Performance Summary:"]
        lines.append("-" / 40)

        for measurement in self.measurements:
            lines.append(f"  {measurement}")

        lines.append("-" * 40)
        lines.append(f"  Total: {self.get_total_duration():.3f}s")
        lines.append(f"  Average: {self.get_average_duration():.3f}s")
        lines.append(f"  Count: {len(self.measurements)}")

        return "\n".join(lines)

    def xǁPerformanceTrackerǁsummary__mutmut_11(self) -> str:
        """Get a summary of all measurements."""
        if not self.measurements:
            return "No measurements recorded"

        lines = ["Performance Summary:"]
        lines.append("XX-XX" * 40)

        for measurement in self.measurements:
            lines.append(f"  {measurement}")

        lines.append("-" * 40)
        lines.append(f"  Total: {self.get_total_duration():.3f}s")
        lines.append(f"  Average: {self.get_average_duration():.3f}s")
        lines.append(f"  Count: {len(self.measurements)}")

        return "\n".join(lines)

    def xǁPerformanceTrackerǁsummary__mutmut_12(self) -> str:
        """Get a summary of all measurements."""
        if not self.measurements:
            return "No measurements recorded"

        lines = ["Performance Summary:"]
        lines.append("-" * 41)

        for measurement in self.measurements:
            lines.append(f"  {measurement}")

        lines.append("-" * 40)
        lines.append(f"  Total: {self.get_total_duration():.3f}s")
        lines.append(f"  Average: {self.get_average_duration():.3f}s")
        lines.append(f"  Count: {len(self.measurements)}")

        return "\n".join(lines)

    def xǁPerformanceTrackerǁsummary__mutmut_13(self) -> str:
        """Get a summary of all measurements."""
        if not self.measurements:
            return "No measurements recorded"

        lines = ["Performance Summary:"]
        lines.append("-" * 40)

        for measurement in self.measurements:
            lines.append(None)

        lines.append("-" * 40)
        lines.append(f"  Total: {self.get_total_duration():.3f}s")
        lines.append(f"  Average: {self.get_average_duration():.3f}s")
        lines.append(f"  Count: {len(self.measurements)}")

        return "\n".join(lines)

    def xǁPerformanceTrackerǁsummary__mutmut_14(self) -> str:
        """Get a summary of all measurements."""
        if not self.measurements:
            return "No measurements recorded"

        lines = ["Performance Summary:"]
        lines.append("-" * 40)

        for measurement in self.measurements:
            lines.append(f"  {measurement}")

        lines.append(None)
        lines.append(f"  Total: {self.get_total_duration():.3f}s")
        lines.append(f"  Average: {self.get_average_duration():.3f}s")
        lines.append(f"  Count: {len(self.measurements)}")

        return "\n".join(lines)

    def xǁPerformanceTrackerǁsummary__mutmut_15(self) -> str:
        """Get a summary of all measurements."""
        if not self.measurements:
            return "No measurements recorded"

        lines = ["Performance Summary:"]
        lines.append("-" * 40)

        for measurement in self.measurements:
            lines.append(f"  {measurement}")

        lines.append("-" / 40)
        lines.append(f"  Total: {self.get_total_duration():.3f}s")
        lines.append(f"  Average: {self.get_average_duration():.3f}s")
        lines.append(f"  Count: {len(self.measurements)}")

        return "\n".join(lines)

    def xǁPerformanceTrackerǁsummary__mutmut_16(self) -> str:
        """Get a summary of all measurements."""
        if not self.measurements:
            return "No measurements recorded"

        lines = ["Performance Summary:"]
        lines.append("-" * 40)

        for measurement in self.measurements:
            lines.append(f"  {measurement}")

        lines.append("XX-XX" * 40)
        lines.append(f"  Total: {self.get_total_duration():.3f}s")
        lines.append(f"  Average: {self.get_average_duration():.3f}s")
        lines.append(f"  Count: {len(self.measurements)}")

        return "\n".join(lines)

    def xǁPerformanceTrackerǁsummary__mutmut_17(self) -> str:
        """Get a summary of all measurements."""
        if not self.measurements:
            return "No measurements recorded"

        lines = ["Performance Summary:"]
        lines.append("-" * 40)

        for measurement in self.measurements:
            lines.append(f"  {measurement}")

        lines.append("-" * 41)
        lines.append(f"  Total: {self.get_total_duration():.3f}s")
        lines.append(f"  Average: {self.get_average_duration():.3f}s")
        lines.append(f"  Count: {len(self.measurements)}")

        return "\n".join(lines)

    def xǁPerformanceTrackerǁsummary__mutmut_18(self) -> str:
        """Get a summary of all measurements."""
        if not self.measurements:
            return "No measurements recorded"

        lines = ["Performance Summary:"]
        lines.append("-" * 40)

        for measurement in self.measurements:
            lines.append(f"  {measurement}")

        lines.append("-" * 40)
        lines.append(None)
        lines.append(f"  Average: {self.get_average_duration():.3f}s")
        lines.append(f"  Count: {len(self.measurements)}")

        return "\n".join(lines)

    def xǁPerformanceTrackerǁsummary__mutmut_19(self) -> str:
        """Get a summary of all measurements."""
        if not self.measurements:
            return "No measurements recorded"

        lines = ["Performance Summary:"]
        lines.append("-" * 40)

        for measurement in self.measurements:
            lines.append(f"  {measurement}")

        lines.append("-" * 40)
        lines.append(f"  Total: {self.get_total_duration():.3f}s")
        lines.append(None)
        lines.append(f"  Count: {len(self.measurements)}")

        return "\n".join(lines)

    def xǁPerformanceTrackerǁsummary__mutmut_20(self) -> str:
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
        lines.append(None)

        return "\n".join(lines)

    def xǁPerformanceTrackerǁsummary__mutmut_21(self) -> str:
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

        return "\n".join(None)

    def xǁPerformanceTrackerǁsummary__mutmut_22(self) -> str:
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

        return "XX\nXX".join(lines)

    xǁPerformanceTrackerǁsummary__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁPerformanceTrackerǁsummary__mutmut_1": (
            xǁPerformanceTrackerǁsummary__mutmut_1
        ),
        "xǁPerformanceTrackerǁsummary__mutmut_2": (
            xǁPerformanceTrackerǁsummary__mutmut_2
        ),
        "xǁPerformanceTrackerǁsummary__mutmut_3": (
            xǁPerformanceTrackerǁsummary__mutmut_3
        ),
        "xǁPerformanceTrackerǁsummary__mutmut_4": (
            xǁPerformanceTrackerǁsummary__mutmut_4
        ),
        "xǁPerformanceTrackerǁsummary__mutmut_5": (
            xǁPerformanceTrackerǁsummary__mutmut_5
        ),
        "xǁPerformanceTrackerǁsummary__mutmut_6": (
            xǁPerformanceTrackerǁsummary__mutmut_6
        ),
        "xǁPerformanceTrackerǁsummary__mutmut_7": (
            xǁPerformanceTrackerǁsummary__mutmut_7
        ),
        "xǁPerformanceTrackerǁsummary__mutmut_8": (
            xǁPerformanceTrackerǁsummary__mutmut_8
        ),
        "xǁPerformanceTrackerǁsummary__mutmut_9": (
            xǁPerformanceTrackerǁsummary__mutmut_9
        ),
        "xǁPerformanceTrackerǁsummary__mutmut_10": (
            xǁPerformanceTrackerǁsummary__mutmut_10
        ),
        "xǁPerformanceTrackerǁsummary__mutmut_11": (
            xǁPerformanceTrackerǁsummary__mutmut_11
        ),
        "xǁPerformanceTrackerǁsummary__mutmut_12": (
            xǁPerformanceTrackerǁsummary__mutmut_12
        ),
        "xǁPerformanceTrackerǁsummary__mutmut_13": (
            xǁPerformanceTrackerǁsummary__mutmut_13
        ),
        "xǁPerformanceTrackerǁsummary__mutmut_14": (
            xǁPerformanceTrackerǁsummary__mutmut_14
        ),
        "xǁPerformanceTrackerǁsummary__mutmut_15": (
            xǁPerformanceTrackerǁsummary__mutmut_15
        ),
        "xǁPerformanceTrackerǁsummary__mutmut_16": (
            xǁPerformanceTrackerǁsummary__mutmut_16
        ),
        "xǁPerformanceTrackerǁsummary__mutmut_17": (
            xǁPerformanceTrackerǁsummary__mutmut_17
        ),
        "xǁPerformanceTrackerǁsummary__mutmut_18": (
            xǁPerformanceTrackerǁsummary__mutmut_18
        ),
        "xǁPerformanceTrackerǁsummary__mutmut_19": (
            xǁPerformanceTrackerǁsummary__mutmut_19
        ),
        "xǁPerformanceTrackerǁsummary__mutmut_20": (
            xǁPerformanceTrackerǁsummary__mutmut_20
        ),
        "xǁPerformanceTrackerǁsummary__mutmut_21": (
            xǁPerformanceTrackerǁsummary__mutmut_21
        ),
        "xǁPerformanceTrackerǁsummary__mutmut_22": (
            xǁPerformanceTrackerǁsummary__mutmut_22
        ),
    }

    def summary(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁPerformanceTrackerǁsummary__mutmut_orig"),
            object.__getattribute__(
                self, "xǁPerformanceTrackerǁsummary__mutmut_mutants"
            ),
            args,
            kwargs,
            self,
        )
        return result

    summary.__signature__ = _mutmut_signature(xǁPerformanceTrackerǁsummary__mutmut_orig)
    xǁPerformanceTrackerǁsummary__mutmut_orig.__name__ = "xǁPerformanceTrackerǁsummary"


def x_smart_wait__mutmut_orig(
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


def x_smart_wait__mutmut_1(
    condition_func,
    timeout: float = 11.0,
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


def x_smart_wait__mutmut_2(
    condition_func,
    timeout: float = 10.0,
    poll_frequency: float = 1.5,
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


def x_smart_wait__mutmut_3(
    condition_func,
    timeout: float = 10.0,
    poll_frequency: float = 0.5,
    error_message: str = "XXCondition not met within timeoutXX",
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


def x_smart_wait__mutmut_4(
    condition_func,
    timeout: float = 10.0,
    poll_frequency: float = 0.5,
    error_message: str = "condition not met within timeout",
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


def x_smart_wait__mutmut_5(
    condition_func,
    timeout: float = 10.0,
    poll_frequency: float = 0.5,
    error_message: str = "CONDITION NOT MET WITHIN TIMEOUT",
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


def x_smart_wait__mutmut_6(
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
    start_time = None

    while time.time() - start_time < timeout:
        try:
            if condition_func():
                return True
        except Exception as e:
            logger.debug(f"Condition check failed: {e}")

        time.sleep(poll_frequency)

    raise TimeoutError(f"{error_message} (timeout: {timeout}s)")


def x_smart_wait__mutmut_7(
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

    while time.time() + start_time < timeout:
        try:
            if condition_func():
                return True
        except Exception as e:
            logger.debug(f"Condition check failed: {e}")

        time.sleep(poll_frequency)

    raise TimeoutError(f"{error_message} (timeout: {timeout}s)")


def x_smart_wait__mutmut_8(
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

    while time.time() - start_time <= timeout:
        try:
            if condition_func():
                return True
        except Exception as e:
            logger.debug(f"Condition check failed: {e}")

        time.sleep(poll_frequency)

    raise TimeoutError(f"{error_message} (timeout: {timeout}s)")


def x_smart_wait__mutmut_9(
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
                return False
        except Exception as e:
            logger.debug(f"Condition check failed: {e}")

        time.sleep(poll_frequency)

    raise TimeoutError(f"{error_message} (timeout: {timeout}s)")


def x_smart_wait__mutmut_10(
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
        except Exception:
            logger.debug(None)

        time.sleep(poll_frequency)

    raise TimeoutError(f"{error_message} (timeout: {timeout}s)")


def x_smart_wait__mutmut_11(
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

        time.sleep(None)

    raise TimeoutError(f"{error_message} (timeout: {timeout}s)")


def x_smart_wait__mutmut_12(
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

    raise TimeoutError(None)


x_smart_wait__mutmut_mutants: ClassVar[MutantDict] = {
    "x_smart_wait__mutmut_1": x_smart_wait__mutmut_1,
    "x_smart_wait__mutmut_2": x_smart_wait__mutmut_2,
    "x_smart_wait__mutmut_3": x_smart_wait__mutmut_3,
    "x_smart_wait__mutmut_4": x_smart_wait__mutmut_4,
    "x_smart_wait__mutmut_5": x_smart_wait__mutmut_5,
    "x_smart_wait__mutmut_6": x_smart_wait__mutmut_6,
    "x_smart_wait__mutmut_7": x_smart_wait__mutmut_7,
    "x_smart_wait__mutmut_8": x_smart_wait__mutmut_8,
    "x_smart_wait__mutmut_9": x_smart_wait__mutmut_9,
    "x_smart_wait__mutmut_10": x_smart_wait__mutmut_10,
    "x_smart_wait__mutmut_11": x_smart_wait__mutmut_11,
    "x_smart_wait__mutmut_12": x_smart_wait__mutmut_12,
}


def smart_wait(*args, **kwargs):
    result = _mutmut_trampoline(
        x_smart_wait__mutmut_orig, x_smart_wait__mutmut_mutants, args, kwargs
    )
    return result


smart_wait.__signature__ = _mutmut_signature(x_smart_wait__mutmut_orig)
x_smart_wait__mutmut_orig.__name__ = "x_smart_wait"


def x_exponential_backoff_wait__mutmut_orig(
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


def x_exponential_backoff_wait__mutmut_1(
    condition_func,
    max_attempts: int = 6,
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


def x_exponential_backoff_wait__mutmut_2(
    condition_func,
    max_attempts: int = 5,
    base_delay: float = 2.0,
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


def x_exponential_backoff_wait__mutmut_3(
    condition_func,
    max_attempts: int = 5,
    base_delay: float = 1.0,
    max_delay: float = 31.0,
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


def x_exponential_backoff_wait__mutmut_4(
    condition_func,
    max_attempts: int = 5,
    base_delay: float = 1.0,
    max_delay: float = 30.0,
    backoff_factor: float = 3.0,
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


def x_exponential_backoff_wait__mutmut_5(
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
    delay = None

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


def x_exponential_backoff_wait__mutmut_6(
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

    for attempt in range(None):
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


def x_exponential_backoff_wait__mutmut_7(
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
                return False
        except Exception as e:
            logger.debug(f"Attempt {attempt + 1} failed: {e}")

        if attempt < max_attempts - 1:  # Don't wait after last attempt
            actual_delay = min(delay, max_delay)
            logger.debug(f"Waiting {actual_delay}s before attempt {attempt + 2}")
            time.sleep(actual_delay)
            delay *= backoff_factor

    return False


def x_exponential_backoff_wait__mutmut_8(
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
        except Exception:
            logger.debug(None)

        if attempt < max_attempts - 1:  # Don't wait after last attempt
            actual_delay = min(delay, max_delay)
            logger.debug(f"Waiting {actual_delay}s before attempt {attempt + 2}")
            time.sleep(actual_delay)
            delay *= backoff_factor

    return False


def x_exponential_backoff_wait__mutmut_9(
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
            logger.debug(f"Attempt {attempt - 1} failed: {e}")

        if attempt < max_attempts - 1:  # Don't wait after last attempt
            actual_delay = min(delay, max_delay)
            logger.debug(f"Waiting {actual_delay}s before attempt {attempt + 2}")
            time.sleep(actual_delay)
            delay *= backoff_factor

    return False


def x_exponential_backoff_wait__mutmut_10(
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
            logger.debug(f"Attempt {attempt + 2} failed: {e}")

        if attempt < max_attempts - 1:  # Don't wait after last attempt
            actual_delay = min(delay, max_delay)
            logger.debug(f"Waiting {actual_delay}s before attempt {attempt + 2}")
            time.sleep(actual_delay)
            delay *= backoff_factor

    return False


def x_exponential_backoff_wait__mutmut_11(
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

        if attempt <= max_attempts - 1:  # Don't wait after last attempt
            actual_delay = min(delay, max_delay)
            logger.debug(f"Waiting {actual_delay}s before attempt {attempt + 2}")
            time.sleep(actual_delay)
            delay *= backoff_factor

    return False


def x_exponential_backoff_wait__mutmut_12(
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

        if attempt < max_attempts + 1:  # Don't wait after last attempt
            actual_delay = min(delay, max_delay)
            logger.debug(f"Waiting {actual_delay}s before attempt {attempt + 2}")
            time.sleep(actual_delay)
            delay *= backoff_factor

    return False


def x_exponential_backoff_wait__mutmut_13(
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

        if attempt < max_attempts - 2:  # Don't wait after last attempt
            actual_delay = min(delay, max_delay)
            logger.debug(f"Waiting {actual_delay}s before attempt {attempt + 2}")
            time.sleep(actual_delay)
            delay *= backoff_factor

    return False


def x_exponential_backoff_wait__mutmut_14(
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
            actual_delay = None
            logger.debug(f"Waiting {actual_delay}s before attempt {attempt + 2}")
            time.sleep(actual_delay)
            delay *= backoff_factor

    return False


def x_exponential_backoff_wait__mutmut_15(
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
            actual_delay = min(None, max_delay)
            logger.debug(f"Waiting {actual_delay}s before attempt {attempt + 2}")
            time.sleep(actual_delay)
            delay *= backoff_factor

    return False


def x_exponential_backoff_wait__mutmut_16(
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
            actual_delay = min(delay, None)
            logger.debug(f"Waiting {actual_delay}s before attempt {attempt + 2}")
            time.sleep(actual_delay)
            delay *= backoff_factor

    return False


def x_exponential_backoff_wait__mutmut_17(
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
            actual_delay = min(max_delay)
            logger.debug(f"Waiting {actual_delay}s before attempt {attempt + 2}")
            time.sleep(actual_delay)
            delay *= backoff_factor

    return False


def x_exponential_backoff_wait__mutmut_18(
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
            actual_delay = min(
                delay,
            )
            logger.debug(f"Waiting {actual_delay}s before attempt {attempt + 2}")
            time.sleep(actual_delay)
            delay *= backoff_factor

    return False


def x_exponential_backoff_wait__mutmut_19(
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
            logger.debug(None)
            time.sleep(actual_delay)
            delay *= backoff_factor

    return False


def x_exponential_backoff_wait__mutmut_20(
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
            logger.debug(f"Waiting {actual_delay}s before attempt {attempt - 2}")
            time.sleep(actual_delay)
            delay *= backoff_factor

    return False


def x_exponential_backoff_wait__mutmut_21(
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
            logger.debug(f"Waiting {actual_delay}s before attempt {attempt + 3}")
            time.sleep(actual_delay)
            delay *= backoff_factor

    return False


def x_exponential_backoff_wait__mutmut_22(
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
            time.sleep(None)
            delay *= backoff_factor

    return False


def x_exponential_backoff_wait__mutmut_23(
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
            delay = backoff_factor

    return False


def x_exponential_backoff_wait__mutmut_24(
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
            delay /= backoff_factor

    return False


def x_exponential_backoff_wait__mutmut_25(
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

    return True


x_exponential_backoff_wait__mutmut_mutants: ClassVar[MutantDict] = {
    "x_exponential_backoff_wait__mutmut_1": x_exponential_backoff_wait__mutmut_1,
    "x_exponential_backoff_wait__mutmut_2": x_exponential_backoff_wait__mutmut_2,
    "x_exponential_backoff_wait__mutmut_3": x_exponential_backoff_wait__mutmut_3,
    "x_exponential_backoff_wait__mutmut_4": x_exponential_backoff_wait__mutmut_4,
    "x_exponential_backoff_wait__mutmut_5": x_exponential_backoff_wait__mutmut_5,
    "x_exponential_backoff_wait__mutmut_6": x_exponential_backoff_wait__mutmut_6,
    "x_exponential_backoff_wait__mutmut_7": x_exponential_backoff_wait__mutmut_7,
    "x_exponential_backoff_wait__mutmut_8": x_exponential_backoff_wait__mutmut_8,
    "x_exponential_backoff_wait__mutmut_9": x_exponential_backoff_wait__mutmut_9,
    "x_exponential_backoff_wait__mutmut_10": x_exponential_backoff_wait__mutmut_10,
    "x_exponential_backoff_wait__mutmut_11": x_exponential_backoff_wait__mutmut_11,
    "x_exponential_backoff_wait__mutmut_12": x_exponential_backoff_wait__mutmut_12,
    "x_exponential_backoff_wait__mutmut_13": x_exponential_backoff_wait__mutmut_13,
    "x_exponential_backoff_wait__mutmut_14": x_exponential_backoff_wait__mutmut_14,
    "x_exponential_backoff_wait__mutmut_15": x_exponential_backoff_wait__mutmut_15,
    "x_exponential_backoff_wait__mutmut_16": x_exponential_backoff_wait__mutmut_16,
    "x_exponential_backoff_wait__mutmut_17": x_exponential_backoff_wait__mutmut_17,
    "x_exponential_backoff_wait__mutmut_18": x_exponential_backoff_wait__mutmut_18,
    "x_exponential_backoff_wait__mutmut_19": x_exponential_backoff_wait__mutmut_19,
    "x_exponential_backoff_wait__mutmut_20": x_exponential_backoff_wait__mutmut_20,
    "x_exponential_backoff_wait__mutmut_21": x_exponential_backoff_wait__mutmut_21,
    "x_exponential_backoff_wait__mutmut_22": x_exponential_backoff_wait__mutmut_22,
    "x_exponential_backoff_wait__mutmut_23": x_exponential_backoff_wait__mutmut_23,
    "x_exponential_backoff_wait__mutmut_24": x_exponential_backoff_wait__mutmut_24,
    "x_exponential_backoff_wait__mutmut_25": x_exponential_backoff_wait__mutmut_25,
}


def exponential_backoff_wait(*args, **kwargs):
    result = _mutmut_trampoline(
        x_exponential_backoff_wait__mutmut_orig,
        x_exponential_backoff_wait__mutmut_mutants,
        args,
        kwargs,
    )
    return result


exponential_backoff_wait.__signature__ = _mutmut_signature(
    x_exponential_backoff_wait__mutmut_orig
)
x_exponential_backoff_wait__mutmut_orig.__name__ = "x_exponential_backoff_wait"
