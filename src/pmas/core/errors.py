"""
Custom framework exceptions for better error handling and debugging.
"""


class FrameworkError(Exception):
    """Base exception for all framework-related errors."""

    def __init__(self, message: str, cause: Exception | None = None) -> None:
        super().__init__(message)
        self.cause = cause


class ConfigurationError(FrameworkError):
    """Raised when there are configuration-related issues."""

    pass


class ElementNotFoundError(FrameworkError):
    """Raised when an element cannot be located on the page."""

    def __init__(
        self, locator: str, timeout: float = 10.0, cause: Exception | None = None
    ) -> None:
        message = (
            f"Element not found using locator '{locator}' within {timeout} seconds"
        )
        super().__init__(message, cause)
        self.locator = locator
        self.timeout = timeout


class ElementNotInteractableError(FrameworkError):
    """Raised when an element is found but cannot be interacted with."""

    def __init__(
        self, locator: str, action: str, cause: Exception | None = None
    ) -> None:
        message = f"Element '{locator}' is not interactable for action '{action}'"
        super().__init__(message, cause)
        self.locator = locator
        self.action = action


class PageLoadError(FrameworkError):
    """Raised when a page fails to load properly."""

    def __init__(self, expected_title: str, actual_title: str, url: str) -> None:
        message = (
            f"Page load failed. Expected title: '{expected_title}', "
            f"got: '{actual_title}' at URL: {url}"
        )
        super().__init__(message)
        self.expected_title = expected_title
        self.actual_title = actual_title
        self.url = url


class DriverError(FrameworkError):
    """Raised when there are WebDriver-related issues."""

    pass


class LoginError(FrameworkError):
    """Raised when a login attempt fails."""

    pass


class ValidationError(FrameworkError):
    """Raised when validation fails."""

    pass
