"""
Custom framework exceptions for better error handling and debugging.
"""

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


class FrameworkError(Exception):
    """Base exception for all framework-related errors."""

    def xǁFrameworkErrorǁ__init____mutmut_orig(
        self, message: str, cause: Exception | None = None
    ) -> None:
        super().__init__(message)
        self.cause = cause

    def xǁFrameworkErrorǁ__init____mutmut_1(
        self, message: str, cause: Exception | None = None
    ) -> None:
        super().__init__(None)
        self.cause = cause

    def xǁFrameworkErrorǁ__init____mutmut_2(
        self, message: str, cause: Exception | None = None
    ) -> None:
        super().__init__(message)
        self.cause = None

    xǁFrameworkErrorǁ__init____mutmut_mutants: ClassVar[MutantDict] = {
        "xǁFrameworkErrorǁ__init____mutmut_1": xǁFrameworkErrorǁ__init____mutmut_1,
        "xǁFrameworkErrorǁ__init____mutmut_2": xǁFrameworkErrorǁ__init____mutmut_2,
    }

    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁFrameworkErrorǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁFrameworkErrorǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    __init__.__signature__ = _mutmut_signature(xǁFrameworkErrorǁ__init____mutmut_orig)
    xǁFrameworkErrorǁ__init____mutmut_orig.__name__ = "xǁFrameworkErrorǁ__init__"


class ConfigurationError(FrameworkError):
    """Raised when there are configuration-related issues."""

    pass


class ElementNotFoundError(FrameworkError):
    """Raised when an element cannot be located on the page."""

    def xǁElementNotFoundErrorǁ__init____mutmut_orig(
        self, locator: str, timeout: float = 10.0, cause: Exception | None = None
    ) -> None:
        message = (
            f"Element not found using locator '{locator}' within {timeout} seconds"
        )
        super().__init__(message, cause)
        self.locator = locator
        self.timeout = timeout

    def xǁElementNotFoundErrorǁ__init____mutmut_1(
        self, locator: str, timeout: float = 11.0, cause: Exception | None = None
    ) -> None:
        message = (
            f"Element not found using locator '{locator}' within {timeout} seconds"
        )
        super().__init__(message, cause)
        self.locator = locator
        self.timeout = timeout

    def xǁElementNotFoundErrorǁ__init____mutmut_2(
        self, locator: str, timeout: float = 10.0, cause: Exception | None = None
    ) -> None:
        message = None
        super().__init__(message, cause)
        self.locator = locator
        self.timeout = timeout

    def xǁElementNotFoundErrorǁ__init____mutmut_3(
        self, locator: str, timeout: float = 10.0, cause: Exception | None = None
    ) -> None:
        message = (
            f"Element not found using locator '{locator}' within {timeout} seconds"
        )
        super().__init__(None, cause)
        self.locator = locator
        self.timeout = timeout

    def xǁElementNotFoundErrorǁ__init____mutmut_4(
        self, locator: str, timeout: float = 10.0, cause: Exception | None = None
    ) -> None:
        message = (
            f"Element not found using locator '{locator}' within {timeout} seconds"
        )
        super().__init__(message, None)
        self.locator = locator
        self.timeout = timeout

    def xǁElementNotFoundErrorǁ__init____mutmut_5(
        self, locator: str, timeout: float = 10.0, cause: Exception | None = None
    ) -> None:
        message = (
            f"Element not found using locator '{locator}' within {timeout} seconds"
        )
        super().__init__(cause)
        self.locator = locator
        self.timeout = timeout

    def xǁElementNotFoundErrorǁ__init____mutmut_6(
        self, locator: str, timeout: float = 10.0, cause: Exception | None = None
    ) -> None:
        message = (
            f"Element not found using locator '{locator}' within {timeout} seconds"
        )
        super().__init__(
            message,
        )
        self.locator = locator
        self.timeout = timeout

    def xǁElementNotFoundErrorǁ__init____mutmut_7(
        self, locator: str, timeout: float = 10.0, cause: Exception | None = None
    ) -> None:
        message = (
            f"Element not found using locator '{locator}' within {timeout} seconds"
        )
        super().__init__(message, cause)
        self.locator = None
        self.timeout = timeout

    def xǁElementNotFoundErrorǁ__init____mutmut_8(
        self, locator: str, timeout: float = 10.0, cause: Exception | None = None
    ) -> None:
        message = (
            f"Element not found using locator '{locator}' within {timeout} seconds"
        )
        super().__init__(message, cause)
        self.locator = locator
        self.timeout = None

    xǁElementNotFoundErrorǁ__init____mutmut_mutants: ClassVar[MutantDict] = {
        "xǁElementNotFoundErrorǁ__init____mutmut_1": xǁElementNotFoundErrorǁ__init____mutmut_1,
        "xǁElementNotFoundErrorǁ__init____mutmut_2": xǁElementNotFoundErrorǁ__init____mutmut_2,
        "xǁElementNotFoundErrorǁ__init____mutmut_3": xǁElementNotFoundErrorǁ__init____mutmut_3,
        "xǁElementNotFoundErrorǁ__init____mutmut_4": xǁElementNotFoundErrorǁ__init____mutmut_4,
        "xǁElementNotFoundErrorǁ__init____mutmut_5": xǁElementNotFoundErrorǁ__init____mutmut_5,
        "xǁElementNotFoundErrorǁ__init____mutmut_6": xǁElementNotFoundErrorǁ__init____mutmut_6,
        "xǁElementNotFoundErrorǁ__init____mutmut_7": xǁElementNotFoundErrorǁ__init____mutmut_7,
        "xǁElementNotFoundErrorǁ__init____mutmut_8": xǁElementNotFoundErrorǁ__init____mutmut_8,
    }

    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(
                self, "xǁElementNotFoundErrorǁ__init____mutmut_orig"
            ),
            object.__getattribute__(
                self, "xǁElementNotFoundErrorǁ__init____mutmut_mutants"
            ),
            args,
            kwargs,
            self,
        )
        return result

    __init__.__signature__ = _mutmut_signature(
        xǁElementNotFoundErrorǁ__init____mutmut_orig
    )
    xǁElementNotFoundErrorǁ__init____mutmut_orig.__name__ = (
        "xǁElementNotFoundErrorǁ__init__"
    )


class ElementNotInteractableError(FrameworkError):
    """Raised when an element is found but cannot be interacted with."""

    def xǁElementNotInteractableErrorǁ__init____mutmut_orig(
        self, locator: str, action: str, cause: Exception | None = None
    ) -> None:
        message = f"Element '{locator}' is not interactable for action '{action}'"
        super().__init__(message, cause)
        self.locator = locator
        self.action = action

    def xǁElementNotInteractableErrorǁ__init____mutmut_1(
        self, locator: str, action: str, cause: Exception | None = None
    ) -> None:
        message = None
        super().__init__(message, cause)
        self.locator = locator
        self.action = action

    def xǁElementNotInteractableErrorǁ__init____mutmut_2(
        self, locator: str, action: str, cause: Exception | None = None
    ) -> None:
        message = f"Element '{locator}' is not interactable for action '{action}'"
        super().__init__(None, cause)
        self.locator = locator
        self.action = action

    def xǁElementNotInteractableErrorǁ__init____mutmut_3(
        self, locator: str, action: str, cause: Exception | None = None
    ) -> None:
        message = f"Element '{locator}' is not interactable for action '{action}'"
        super().__init__(message, None)
        self.locator = locator
        self.action = action

    def xǁElementNotInteractableErrorǁ__init____mutmut_4(
        self, locator: str, action: str, cause: Exception | None = None
    ) -> None:
        message = f"Element '{locator}' is not interactable for action '{action}'"
        super().__init__(cause)
        self.locator = locator
        self.action = action

    def xǁElementNotInteractableErrorǁ__init____mutmut_5(
        self, locator: str, action: str, cause: Exception | None = None
    ) -> None:
        message = f"Element '{locator}' is not interactable for action '{action}'"
        super().__init__(
            message,
        )
        self.locator = locator
        self.action = action

    def xǁElementNotInteractableErrorǁ__init____mutmut_6(
        self, locator: str, action: str, cause: Exception | None = None
    ) -> None:
        message = f"Element '{locator}' is not interactable for action '{action}'"
        super().__init__(message, cause)
        self.locator = None
        self.action = action

    def xǁElementNotInteractableErrorǁ__init____mutmut_7(
        self, locator: str, action: str, cause: Exception | None = None
    ) -> None:
        message = f"Element '{locator}' is not interactable for action '{action}'"
        super().__init__(message, cause)
        self.locator = locator
        self.action = None

    xǁElementNotInteractableErrorǁ__init____mutmut_mutants: ClassVar[MutantDict] = {
        "xǁElementNotInteractableErrorǁ__init____mutmut_1": xǁElementNotInteractableErrorǁ__init____mutmut_1,
        "xǁElementNotInteractableErrorǁ__init____mutmut_2": xǁElementNotInteractableErrorǁ__init____mutmut_2,
        "xǁElementNotInteractableErrorǁ__init____mutmut_3": xǁElementNotInteractableErrorǁ__init____mutmut_3,
        "xǁElementNotInteractableErrorǁ__init____mutmut_4": xǁElementNotInteractableErrorǁ__init____mutmut_4,
        "xǁElementNotInteractableErrorǁ__init____mutmut_5": xǁElementNotInteractableErrorǁ__init____mutmut_5,
        "xǁElementNotInteractableErrorǁ__init____mutmut_6": xǁElementNotInteractableErrorǁ__init____mutmut_6,
        "xǁElementNotInteractableErrorǁ__init____mutmut_7": xǁElementNotInteractableErrorǁ__init____mutmut_7,
    }

    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(
                self, "xǁElementNotInteractableErrorǁ__init____mutmut_orig"
            ),
            object.__getattribute__(
                self, "xǁElementNotInteractableErrorǁ__init____mutmut_mutants"
            ),
            args,
            kwargs,
            self,
        )
        return result

    __init__.__signature__ = _mutmut_signature(
        xǁElementNotInteractableErrorǁ__init____mutmut_orig
    )
    xǁElementNotInteractableErrorǁ__init____mutmut_orig.__name__ = (
        "xǁElementNotInteractableErrorǁ__init__"
    )


class PageLoadError(FrameworkError):
    """Raised when a page fails to load properly."""

    def xǁPageLoadErrorǁ__init____mutmut_orig(
        self, expected_title: str, actual_title: str, url: str
    ) -> None:
        message = f"Page load failed. Expected title: '{expected_title}', got: '{actual_title}' at URL: {url}"
        super().__init__(message)
        self.expected_title = expected_title
        self.actual_title = actual_title
        self.url = url

    def xǁPageLoadErrorǁ__init____mutmut_1(
        self, expected_title: str, actual_title: str, url: str
    ) -> None:
        message = None
        super().__init__(message)
        self.expected_title = expected_title
        self.actual_title = actual_title
        self.url = url

    def xǁPageLoadErrorǁ__init____mutmut_2(
        self, expected_title: str, actual_title: str, url: str
    ) -> None:
        message = f"Page load failed. Expected title: '{expected_title}', got: '{actual_title}' at URL: {url}"
        super().__init__(None)
        self.expected_title = expected_title
        self.actual_title = actual_title
        self.url = url

    def xǁPageLoadErrorǁ__init____mutmut_3(
        self, expected_title: str, actual_title: str, url: str
    ) -> None:
        message = f"Page load failed. Expected title: '{expected_title}', got: '{actual_title}' at URL: {url}"
        super().__init__(message)
        self.expected_title = None
        self.actual_title = actual_title
        self.url = url

    def xǁPageLoadErrorǁ__init____mutmut_4(
        self, expected_title: str, actual_title: str, url: str
    ) -> None:
        message = f"Page load failed. Expected title: '{expected_title}', got: '{actual_title}' at URL: {url}"
        super().__init__(message)
        self.expected_title = expected_title
        self.actual_title = None
        self.url = url

    def xǁPageLoadErrorǁ__init____mutmut_5(
        self, expected_title: str, actual_title: str, url: str
    ) -> None:
        message = f"Page load failed. Expected title: '{expected_title}', got: '{actual_title}' at URL: {url}"
        super().__init__(message)
        self.expected_title = expected_title
        self.actual_title = actual_title
        self.url = None

    xǁPageLoadErrorǁ__init____mutmut_mutants: ClassVar[MutantDict] = {
        "xǁPageLoadErrorǁ__init____mutmut_1": xǁPageLoadErrorǁ__init____mutmut_1,
        "xǁPageLoadErrorǁ__init____mutmut_2": xǁPageLoadErrorǁ__init____mutmut_2,
        "xǁPageLoadErrorǁ__init____mutmut_3": xǁPageLoadErrorǁ__init____mutmut_3,
        "xǁPageLoadErrorǁ__init____mutmut_4": xǁPageLoadErrorǁ__init____mutmut_4,
        "xǁPageLoadErrorǁ__init____mutmut_5": xǁPageLoadErrorǁ__init____mutmut_5,
    }

    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁPageLoadErrorǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁPageLoadErrorǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    __init__.__signature__ = _mutmut_signature(xǁPageLoadErrorǁ__init____mutmut_orig)
    xǁPageLoadErrorǁ__init____mutmut_orig.__name__ = "xǁPageLoadErrorǁ__init__"


class DriverError(FrameworkError):
    """Raised when there are WebDriver-related issues."""

    pass


class ValidationError(FrameworkError):
    """Raised when validation fails."""

    pass
