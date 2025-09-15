"""
Base page class providing common page operations and navigation patterns.
"""

import logging
import time
from abc import ABC, abstractmethod
from collections.abc import Callable
from inspect import signature as _mutmut_signature
from pathlib import Path
from typing import Annotated, Any, ClassVar, TypeVar

from selenium.common.exceptions import (
    TimeoutException,
)
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .elements import BaseElement, Button, Checkbox, Dropdown, RadioButton, TextInput
from .errors import ElementNotFoundError, PageLoadError
from .locators import Locator

logger = logging.getLogger(__name__)

# Type variable for page classes
PageType = TypeVar("PageType", bound="BasePage")


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


class BasePage(ABC):
    """
    Abstract base class for all page objects.
    Provides common functionality for page navigation, waits, and element interactions.
    """

    # Subclasses should override these
    url_path: str = ""
    expected_titles: list[str] = []

    def xǁBasePageǁ__init____mutmut_orig(
        self, driver, base_url: str = "", timeout: float = 10.0
    ) -> None:
        self.driver = driver
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._elements_cache: dict[str, BaseElement] = {}

    def xǁBasePageǁ__init____mutmut_1(
        self, driver, base_url: str = "XXXX", timeout: float = 10.0
    ) -> None:
        self.driver = driver
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._elements_cache: dict[str, BaseElement] = {}

    def xǁBasePageǁ__init____mutmut_2(
        self, driver, base_url: str = "", timeout: float = 11.0
    ) -> None:
        self.driver = driver
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._elements_cache: dict[str, BaseElement] = {}

    def xǁBasePageǁ__init____mutmut_3(
        self, driver, base_url: str = "", timeout: float = 10.0
    ) -> None:
        self.driver = None
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._elements_cache: dict[str, BaseElement] = {}

    def xǁBasePageǁ__init____mutmut_4(
        self, driver, base_url: str = "", timeout: float = 10.0
    ) -> None:
        self.driver = driver
        self.base_url = None
        self.timeout = timeout
        self._elements_cache: dict[str, BaseElement] = {}

    def xǁBasePageǁ__init____mutmut_5(
        self, driver, base_url: str = "", timeout: float = 10.0
    ) -> None:
        self.driver = driver
        self.base_url = base_url.rstrip(None)
        self.timeout = timeout
        self._elements_cache: dict[str, BaseElement] = {}

    def xǁBasePageǁ__init____mutmut_6(
        self, driver, base_url: str = "", timeout: float = 10.0
    ) -> None:
        self.driver = driver
        self.base_url = base_url.lstrip("/")
        self.timeout = timeout
        self._elements_cache: dict[str, BaseElement] = {}

    def xǁBasePageǁ__init____mutmut_7(
        self, driver, base_url: str = "", timeout: float = 10.0
    ) -> None:
        self.driver = driver
        self.base_url = base_url.rstrip("XX/XX")
        self.timeout = timeout
        self._elements_cache: dict[str, BaseElement] = {}

    def xǁBasePageǁ__init____mutmut_8(
        self, driver, base_url: str = "", timeout: float = 10.0
    ) -> None:
        self.driver = driver
        self.base_url = base_url.rstrip("/")
        self.timeout = None
        self._elements_cache: dict[str, BaseElement] = {}

    def xǁBasePageǁ__init____mutmut_9(
        self, driver, base_url: str = "", timeout: float = 10.0
    ) -> None:
        self.driver = driver
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._elements_cache: dict[str, BaseElement] = None

    xǁBasePageǁ__init____mutmut_mutants: ClassVar[MutantDict] = {
        "xǁBasePageǁ__init____mutmut_1": xǁBasePageǁ__init____mutmut_1,
        "xǁBasePageǁ__init____mutmut_2": xǁBasePageǁ__init____mutmut_2,
        "xǁBasePageǁ__init____mutmut_3": xǁBasePageǁ__init____mutmut_3,
        "xǁBasePageǁ__init____mutmut_4": xǁBasePageǁ__init____mutmut_4,
        "xǁBasePageǁ__init____mutmut_5": xǁBasePageǁ__init____mutmut_5,
        "xǁBasePageǁ__init____mutmut_6": xǁBasePageǁ__init____mutmut_6,
        "xǁBasePageǁ__init____mutmut_7": xǁBasePageǁ__init____mutmut_7,
        "xǁBasePageǁ__init____mutmut_8": xǁBasePageǁ__init____mutmut_8,
        "xǁBasePageǁ__init____mutmut_9": xǁBasePageǁ__init____mutmut_9,
    }

    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁBasePageǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁBasePageǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    __init__.__signature__ = _mutmut_signature(xǁBasePageǁ__init____mutmut_orig)
    xǁBasePageǁ__init____mutmut_orig.__name__ = "xǁBasePageǁ__init__"

    @property
    def url(self) -> str:
        """Get the full URL for this page."""
        if self.url_path:
            return f"{self.base_url}/{self.url_path.lstrip('/')}"
        return self.base_url

    @property
    def current_url(self) -> str:
        """Get the current browser URL."""
        return self.driver.current_url

    @property
    def title(self) -> str:
        """Get the current page title."""
        return self.driver.title

    def xǁBasePageǁnavigate_to__mutmut_orig(self, url: str | None = None) -> "BasePage":
        """
        Navigate to the page URL.

        Args:
            url: Optional URL to navigate to, defaults to self.url
        """
        target_url = url or self.url
        if not target_url:
            raise ValueError("No URL specified and page has no default URL")

        logger.info(f"Navigating to: {target_url}")
        self.driver.get(target_url)
        return self

    def xǁBasePageǁnavigate_to__mutmut_1(self, url: str | None = None) -> "BasePage":
        """
        Navigate to the page URL.

        Args:
            url: Optional URL to navigate to, defaults to self.url
        """
        target_url = None
        if not target_url:
            raise ValueError("No URL specified and page has no default URL")

        logger.info(f"Navigating to: {target_url}")
        self.driver.get(target_url)
        return self

    def xǁBasePageǁnavigate_to__mutmut_2(self, url: str | None = None) -> "BasePage":
        """
        Navigate to the page URL.

        Args:
            url: Optional URL to navigate to, defaults to self.url
        """
        target_url = url and self.url
        if not target_url:
            raise ValueError("No URL specified and page has no default URL")

        logger.info(f"Navigating to: {target_url}")
        self.driver.get(target_url)
        return self

    def xǁBasePageǁnavigate_to__mutmut_3(self, url: str | None = None) -> "BasePage":
        """
        Navigate to the page URL.

        Args:
            url: Optional URL to navigate to, defaults to self.url
        """
        target_url = url or self.url
        if target_url:
            raise ValueError("No URL specified and page has no default URL")

        logger.info(f"Navigating to: {target_url}")
        self.driver.get(target_url)
        return self

    def xǁBasePageǁnavigate_to__mutmut_4(self, url: str | None = None) -> "BasePage":
        """
        Navigate to the page URL.

        Args:
            url: Optional URL to navigate to, defaults to self.url
        """
        target_url = url or self.url
        if not target_url:
            raise ValueError(None)

        logger.info(f"Navigating to: {target_url}")
        self.driver.get(target_url)
        return self

    def xǁBasePageǁnavigate_to__mutmut_5(self, url: str | None = None) -> "BasePage":
        """
        Navigate to the page URL.

        Args:
            url: Optional URL to navigate to, defaults to self.url
        """
        target_url = url or self.url
        if not target_url:
            raise ValueError("XXNo URL specified and page has no default URLXX")

        logger.info(f"Navigating to: {target_url}")
        self.driver.get(target_url)
        return self

    def xǁBasePageǁnavigate_to__mutmut_6(self, url: str | None = None) -> "BasePage":
        """
        Navigate to the page URL.

        Args:
            url: Optional URL to navigate to, defaults to self.url
        """
        target_url = url or self.url
        if not target_url:
            raise ValueError("no url specified and page has no default url")

        logger.info(f"Navigating to: {target_url}")
        self.driver.get(target_url)
        return self

    def xǁBasePageǁnavigate_to__mutmut_7(self, url: str | None = None) -> "BasePage":
        """
        Navigate to the page URL.

        Args:
            url: Optional URL to navigate to, defaults to self.url
        """
        target_url = url or self.url
        if not target_url:
            raise ValueError("NO URL SPECIFIED AND PAGE HAS NO DEFAULT URL")

        logger.info(f"Navigating to: {target_url}")
        self.driver.get(target_url)
        return self

    def xǁBasePageǁnavigate_to__mutmut_8(self, url: str | None = None) -> "BasePage":
        """
        Navigate to the page URL.

        Args:
            url: Optional URL to navigate to, defaults to self.url
        """
        target_url = url or self.url
        if not target_url:
            raise ValueError("No URL specified and page has no default URL")

        logger.info(None)
        self.driver.get(target_url)
        return self

    def xǁBasePageǁnavigate_to__mutmut_9(self, url: str | None = None) -> "BasePage":
        """
        Navigate to the page URL.

        Args:
            url: Optional URL to navigate to, defaults to self.url
        """
        target_url = url or self.url
        if not target_url:
            raise ValueError("No URL specified and page has no default URL")

        logger.info(f"Navigating to: {target_url}")
        self.driver.get(None)
        return self

    xǁBasePageǁnavigate_to__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁBasePageǁnavigate_to__mutmut_1": xǁBasePageǁnavigate_to__mutmut_1,
        "xǁBasePageǁnavigate_to__mutmut_2": xǁBasePageǁnavigate_to__mutmut_2,
        "xǁBasePageǁnavigate_to__mutmut_3": xǁBasePageǁnavigate_to__mutmut_3,
        "xǁBasePageǁnavigate_to__mutmut_4": xǁBasePageǁnavigate_to__mutmut_4,
        "xǁBasePageǁnavigate_to__mutmut_5": xǁBasePageǁnavigate_to__mutmut_5,
        "xǁBasePageǁnavigate_to__mutmut_6": xǁBasePageǁnavigate_to__mutmut_6,
        "xǁBasePageǁnavigate_to__mutmut_7": xǁBasePageǁnavigate_to__mutmut_7,
        "xǁBasePageǁnavigate_to__mutmut_8": xǁBasePageǁnavigate_to__mutmut_8,
        "xǁBasePageǁnavigate_to__mutmut_9": xǁBasePageǁnavigate_to__mutmut_9,
    }

    def navigate_to(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁBasePageǁnavigate_to__mutmut_orig"),
            object.__getattribute__(self, "xǁBasePageǁnavigate_to__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    navigate_to.__signature__ = _mutmut_signature(xǁBasePageǁnavigate_to__mutmut_orig)
    xǁBasePageǁnavigate_to__mutmut_orig.__name__ = "xǁBasePageǁnavigate_to"

    def xǁBasePageǁwait_for_page_load__mutmut_orig(
        self, timeout: float | None = None
    ) -> "BasePage":
        """
        Wait for the page to load completely.
        Checks for expected titles if defined.
        """
        timeout = timeout or self.timeout

        if self.expected_titles:
            try:
                wait = WebDriverWait(self.driver, timeout)
                wait.until(
                    lambda driver: any(
                        title in driver.title for title in self.expected_titles
                    )
                )
                logger.debug(f"Page loaded with title: {self.title}")
            except TimeoutException:
                raise PageLoadError(
                    expected_title=str(self.expected_titles),
                    actual_title=self.title,
                    url=self.current_url,
                )

        # Wait for document ready state
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(
                lambda driver: driver.execute_script("return document.readyState")
                == "complete"
            )
        except TimeoutException:
            logger.warning("Page did not reach complete ready state within timeout")

        return self

    def xǁBasePageǁwait_for_page_load__mutmut_1(
        self, timeout: float | None = None
    ) -> "BasePage":
        """
        Wait for the page to load completely.
        Checks for expected titles if defined.
        """
        timeout = None

        if self.expected_titles:
            try:
                wait = WebDriverWait(self.driver, timeout)
                wait.until(
                    lambda driver: any(
                        title in driver.title for title in self.expected_titles
                    )
                )
                logger.debug(f"Page loaded with title: {self.title}")
            except TimeoutException:
                raise PageLoadError(
                    expected_title=str(self.expected_titles),
                    actual_title=self.title,
                    url=self.current_url,
                )

        # Wait for document ready state
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(
                lambda driver: driver.execute_script("return document.readyState")
                == "complete"
            )
        except TimeoutException:
            logger.warning("Page did not reach complete ready state within timeout")

        return self

    def xǁBasePageǁwait_for_page_load__mutmut_2(
        self, timeout: float | None = None
    ) -> "BasePage":
        """
        Wait for the page to load completely.
        Checks for expected titles if defined.
        """
        timeout = timeout and self.timeout

        if self.expected_titles:
            try:
                wait = WebDriverWait(self.driver, timeout)
                wait.until(
                    lambda driver: any(
                        title in driver.title for title in self.expected_titles
                    )
                )
                logger.debug(f"Page loaded with title: {self.title}")
            except TimeoutException:
                raise PageLoadError(
                    expected_title=str(self.expected_titles),
                    actual_title=self.title,
                    url=self.current_url,
                )

        # Wait for document ready state
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(
                lambda driver: driver.execute_script("return document.readyState")
                == "complete"
            )
        except TimeoutException:
            logger.warning("Page did not reach complete ready state within timeout")

        return self

    def xǁBasePageǁwait_for_page_load__mutmut_3(
        self, timeout: float | None = None
    ) -> "BasePage":
        """
        Wait for the page to load completely.
        Checks for expected titles if defined.
        """
        timeout = timeout or self.timeout

        if self.expected_titles:
            try:
                wait = None
                wait.until(
                    lambda driver: any(
                        title in driver.title for title in self.expected_titles
                    )
                )
                logger.debug(f"Page loaded with title: {self.title}")
            except TimeoutException:
                raise PageLoadError(
                    expected_title=str(self.expected_titles),
                    actual_title=self.title,
                    url=self.current_url,
                )

        # Wait for document ready state
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(
                lambda driver: driver.execute_script("return document.readyState")
                == "complete"
            )
        except TimeoutException:
            logger.warning("Page did not reach complete ready state within timeout")

        return self

    def xǁBasePageǁwait_for_page_load__mutmut_4(
        self, timeout: float | None = None
    ) -> "BasePage":
        """
        Wait for the page to load completely.
        Checks for expected titles if defined.
        """
        timeout = timeout or self.timeout

        if self.expected_titles:
            try:
                wait = WebDriverWait(None, timeout)
                wait.until(
                    lambda driver: any(
                        title in driver.title for title in self.expected_titles
                    )
                )
                logger.debug(f"Page loaded with title: {self.title}")
            except TimeoutException:
                raise PageLoadError(
                    expected_title=str(self.expected_titles),
                    actual_title=self.title,
                    url=self.current_url,
                )

        # Wait for document ready state
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(
                lambda driver: driver.execute_script("return document.readyState")
                == "complete"
            )
        except TimeoutException:
            logger.warning("Page did not reach complete ready state within timeout")

        return self

    def xǁBasePageǁwait_for_page_load__mutmut_5(
        self, timeout: float | None = None
    ) -> "BasePage":
        """
        Wait for the page to load completely.
        Checks for expected titles if defined.
        """
        timeout = timeout or self.timeout

        if self.expected_titles:
            try:
                wait = WebDriverWait(self.driver, None)
                wait.until(
                    lambda driver: any(
                        title in driver.title for title in self.expected_titles
                    )
                )
                logger.debug(f"Page loaded with title: {self.title}")
            except TimeoutException:
                raise PageLoadError(
                    expected_title=str(self.expected_titles),
                    actual_title=self.title,
                    url=self.current_url,
                )

        # Wait for document ready state
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(
                lambda driver: driver.execute_script("return document.readyState")
                == "complete"
            )
        except TimeoutException:
            logger.warning("Page did not reach complete ready state within timeout")

        return self

    def xǁBasePageǁwait_for_page_load__mutmut_6(
        self, timeout: float | None = None
    ) -> "BasePage":
        """
        Wait for the page to load completely.
        Checks for expected titles if defined.
        """
        timeout = timeout or self.timeout

        if self.expected_titles:
            try:
                wait = WebDriverWait(timeout)
                wait.until(
                    lambda driver: any(
                        title in driver.title for title in self.expected_titles
                    )
                )
                logger.debug(f"Page loaded with title: {self.title}")
            except TimeoutException:
                raise PageLoadError(
                    expected_title=str(self.expected_titles),
                    actual_title=self.title,
                    url=self.current_url,
                )

        # Wait for document ready state
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(
                lambda driver: driver.execute_script("return document.readyState")
                == "complete"
            )
        except TimeoutException:
            logger.warning("Page did not reach complete ready state within timeout")

        return self

    def xǁBasePageǁwait_for_page_load__mutmut_7(
        self, timeout: float | None = None
    ) -> "BasePage":
        """
        Wait for the page to load completely.
        Checks for expected titles if defined.
        """
        timeout = timeout or self.timeout

        if self.expected_titles:
            try:
                wait = WebDriverWait(
                    self.driver,
                )
                wait.until(
                    lambda driver: any(
                        title in driver.title for title in self.expected_titles
                    )
                )
                logger.debug(f"Page loaded with title: {self.title}")
            except TimeoutException:
                raise PageLoadError(
                    expected_title=str(self.expected_titles),
                    actual_title=self.title,
                    url=self.current_url,
                )

        # Wait for document ready state
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(
                lambda driver: driver.execute_script("return document.readyState")
                == "complete"
            )
        except TimeoutException:
            logger.warning("Page did not reach complete ready state within timeout")

        return self

    def xǁBasePageǁwait_for_page_load__mutmut_8(
        self, timeout: float | None = None
    ) -> "BasePage":
        """
        Wait for the page to load completely.
        Checks for expected titles if defined.
        """
        timeout = timeout or self.timeout

        if self.expected_titles:
            try:
                wait = WebDriverWait(self.driver, timeout)
                wait.until(None)
                logger.debug(f"Page loaded with title: {self.title}")
            except TimeoutException:
                raise PageLoadError(
                    expected_title=str(self.expected_titles),
                    actual_title=self.title,
                    url=self.current_url,
                )

        # Wait for document ready state
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(
                lambda driver: driver.execute_script("return document.readyState")
                == "complete"
            )
        except TimeoutException:
            logger.warning("Page did not reach complete ready state within timeout")

        return self

    def xǁBasePageǁwait_for_page_load__mutmut_9(
        self, timeout: float | None = None
    ) -> "BasePage":
        """
        Wait for the page to load completely.
        Checks for expected titles if defined.
        """
        timeout = timeout or self.timeout

        if self.expected_titles:
            try:
                wait = WebDriverWait(self.driver, timeout)
                wait.until(lambda driver: None)
                logger.debug(f"Page loaded with title: {self.title}")
            except TimeoutException:
                raise PageLoadError(
                    expected_title=str(self.expected_titles),
                    actual_title=self.title,
                    url=self.current_url,
                )

        # Wait for document ready state
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(
                lambda driver: driver.execute_script("return document.readyState")
                == "complete"
            )
        except TimeoutException:
            logger.warning("Page did not reach complete ready state within timeout")

        return self

    def xǁBasePageǁwait_for_page_load__mutmut_10(
        self, timeout: float | None = None
    ) -> "BasePage":
        """
        Wait for the page to load completely.
        Checks for expected titles if defined.
        """
        timeout = timeout or self.timeout

        if self.expected_titles:
            try:
                wait = WebDriverWait(self.driver, timeout)
                wait.until(lambda driver: any(None))
                logger.debug(f"Page loaded with title: {self.title}")
            except TimeoutException:
                raise PageLoadError(
                    expected_title=str(self.expected_titles),
                    actual_title=self.title,
                    url=self.current_url,
                )

        # Wait for document ready state
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(
                lambda driver: driver.execute_script("return document.readyState")
                == "complete"
            )
        except TimeoutException:
            logger.warning("Page did not reach complete ready state within timeout")

        return self

    def xǁBasePageǁwait_for_page_load__mutmut_11(
        self, timeout: float | None = None
    ) -> "BasePage":
        """
        Wait for the page to load completely.
        Checks for expected titles if defined.
        """
        timeout = timeout or self.timeout

        if self.expected_titles:
            try:
                wait = WebDriverWait(self.driver, timeout)
                wait.until(
                    lambda driver: any(
                        title not in driver.title for title in self.expected_titles
                    )
                )
                logger.debug(f"Page loaded with title: {self.title}")
            except TimeoutException:
                raise PageLoadError(
                    expected_title=str(self.expected_titles),
                    actual_title=self.title,
                    url=self.current_url,
                )

        # Wait for document ready state
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(
                lambda driver: driver.execute_script("return document.readyState")
                == "complete"
            )
        except TimeoutException:
            logger.warning("Page did not reach complete ready state within timeout")

        return self

    def xǁBasePageǁwait_for_page_load__mutmut_12(
        self, timeout: float | None = None
    ) -> "BasePage":
        """
        Wait for the page to load completely.
        Checks for expected titles if defined.
        """
        timeout = timeout or self.timeout

        if self.expected_titles:
            try:
                wait = WebDriverWait(self.driver, timeout)
                wait.until(
                    lambda driver: any(
                        title in driver.title for title in self.expected_titles
                    )
                )
                logger.debug(None)
            except TimeoutException:
                raise PageLoadError(
                    expected_title=str(self.expected_titles),
                    actual_title=self.title,
                    url=self.current_url,
                )

        # Wait for document ready state
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(
                lambda driver: driver.execute_script("return document.readyState")
                == "complete"
            )
        except TimeoutException:
            logger.warning("Page did not reach complete ready state within timeout")

        return self

    def xǁBasePageǁwait_for_page_load__mutmut_13(
        self, timeout: float | None = None
    ) -> "BasePage":
        """
        Wait for the page to load completely.
        Checks for expected titles if defined.
        """
        timeout = timeout or self.timeout

        if self.expected_titles:
            try:
                wait = WebDriverWait(self.driver, timeout)
                wait.until(
                    lambda driver: any(
                        title in driver.title for title in self.expected_titles
                    )
                )
                logger.debug(f"Page loaded with title: {self.title}")
            except TimeoutException:
                raise PageLoadError(
                    expected_title=None,
                    actual_title=self.title,
                    url=self.current_url,
                )

        # Wait for document ready state
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(
                lambda driver: driver.execute_script("return document.readyState")
                == "complete"
            )
        except TimeoutException:
            logger.warning("Page did not reach complete ready state within timeout")

        return self

    def xǁBasePageǁwait_for_page_load__mutmut_14(
        self, timeout: float | None = None
    ) -> "BasePage":
        """
        Wait for the page to load completely.
        Checks for expected titles if defined.
        """
        timeout = timeout or self.timeout

        if self.expected_titles:
            try:
                wait = WebDriverWait(self.driver, timeout)
                wait.until(
                    lambda driver: any(
                        title in driver.title for title in self.expected_titles
                    )
                )
                logger.debug(f"Page loaded with title: {self.title}")
            except TimeoutException:
                raise PageLoadError(
                    expected_title=str(self.expected_titles),
                    actual_title=None,
                    url=self.current_url,
                )

        # Wait for document ready state
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(
                lambda driver: driver.execute_script("return document.readyState")
                == "complete"
            )
        except TimeoutException:
            logger.warning("Page did not reach complete ready state within timeout")

        return self

    def xǁBasePageǁwait_for_page_load__mutmut_15(
        self, timeout: float | None = None
    ) -> "BasePage":
        """
        Wait for the page to load completely.
        Checks for expected titles if defined.
        """
        timeout = timeout or self.timeout

        if self.expected_titles:
            try:
                wait = WebDriverWait(self.driver, timeout)
                wait.until(
                    lambda driver: any(
                        title in driver.title for title in self.expected_titles
                    )
                )
                logger.debug(f"Page loaded with title: {self.title}")
            except TimeoutException:
                raise PageLoadError(
                    expected_title=str(self.expected_titles),
                    actual_title=self.title,
                    url=None,
                )

        # Wait for document ready state
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(
                lambda driver: driver.execute_script("return document.readyState")
                == "complete"
            )
        except TimeoutException:
            logger.warning("Page did not reach complete ready state within timeout")

        return self

    def xǁBasePageǁwait_for_page_load__mutmut_16(
        self, timeout: float | None = None
    ) -> "BasePage":
        """
        Wait for the page to load completely.
        Checks for expected titles if defined.
        """
        timeout = timeout or self.timeout

        if self.expected_titles:
            try:
                wait = WebDriverWait(self.driver, timeout)
                wait.until(
                    lambda driver: any(
                        title in driver.title for title in self.expected_titles
                    )
                )
                logger.debug(f"Page loaded with title: {self.title}")
            except TimeoutException:
                raise PageLoadError(
                    actual_title=self.title,
                    url=self.current_url,
                )

        # Wait for document ready state
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(
                lambda driver: driver.execute_script("return document.readyState")
                == "complete"
            )
        except TimeoutException:
            logger.warning("Page did not reach complete ready state within timeout")

        return self

    def xǁBasePageǁwait_for_page_load__mutmut_17(
        self, timeout: float | None = None
    ) -> "BasePage":
        """
        Wait for the page to load completely.
        Checks for expected titles if defined.
        """
        timeout = timeout or self.timeout

        if self.expected_titles:
            try:
                wait = WebDriverWait(self.driver, timeout)
                wait.until(
                    lambda driver: any(
                        title in driver.title for title in self.expected_titles
                    )
                )
                logger.debug(f"Page loaded with title: {self.title}")
            except TimeoutException:
                raise PageLoadError(
                    expected_title=str(self.expected_titles),
                    url=self.current_url,
                )

        # Wait for document ready state
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(
                lambda driver: driver.execute_script("return document.readyState")
                == "complete"
            )
        except TimeoutException:
            logger.warning("Page did not reach complete ready state within timeout")

        return self

    def xǁBasePageǁwait_for_page_load__mutmut_18(
        self, timeout: float | None = None
    ) -> "BasePage":
        """
        Wait for the page to load completely.
        Checks for expected titles if defined.
        """
        timeout = timeout or self.timeout

        if self.expected_titles:
            try:
                wait = WebDriverWait(self.driver, timeout)
                wait.until(
                    lambda driver: any(
                        title in driver.title for title in self.expected_titles
                    )
                )
                logger.debug(f"Page loaded with title: {self.title}")
            except TimeoutException:
                raise PageLoadError(
                    expected_title=str(self.expected_titles),
                    actual_title=self.title,
                )

        # Wait for document ready state
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(
                lambda driver: driver.execute_script("return document.readyState")
                == "complete"
            )
        except TimeoutException:
            logger.warning("Page did not reach complete ready state within timeout")

        return self

    def xǁBasePageǁwait_for_page_load__mutmut_19(
        self, timeout: float | None = None
    ) -> "BasePage":
        """
        Wait for the page to load completely.
        Checks for expected titles if defined.
        """
        timeout = timeout or self.timeout

        if self.expected_titles:
            try:
                wait = WebDriverWait(self.driver, timeout)
                wait.until(
                    lambda driver: any(
                        title in driver.title for title in self.expected_titles
                    )
                )
                logger.debug(f"Page loaded with title: {self.title}")
            except TimeoutException:
                raise PageLoadError(
                    expected_title=str(None),
                    actual_title=self.title,
                    url=self.current_url,
                )

        # Wait for document ready state
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(
                lambda driver: driver.execute_script("return document.readyState")
                == "complete"
            )
        except TimeoutException:
            logger.warning("Page did not reach complete ready state within timeout")

        return self

    def xǁBasePageǁwait_for_page_load__mutmut_20(
        self, timeout: float | None = None
    ) -> "BasePage":
        """
        Wait for the page to load completely.
        Checks for expected titles if defined.
        """
        timeout = timeout or self.timeout

        if self.expected_titles:
            try:
                wait = WebDriverWait(self.driver, timeout)
                wait.until(
                    lambda driver: any(
                        title in driver.title for title in self.expected_titles
                    )
                )
                logger.debug(f"Page loaded with title: {self.title}")
            except TimeoutException:
                raise PageLoadError(
                    expected_title=str(self.expected_titles),
                    actual_title=self.title,
                    url=self.current_url,
                )

        # Wait for document ready state
        try:
            wait = None
            wait.until(
                lambda driver: driver.execute_script("return document.readyState")
                == "complete"
            )
        except TimeoutException:
            logger.warning("Page did not reach complete ready state within timeout")

        return self

    def xǁBasePageǁwait_for_page_load__mutmut_21(
        self, timeout: float | None = None
    ) -> "BasePage":
        """
        Wait for the page to load completely.
        Checks for expected titles if defined.
        """
        timeout = timeout or self.timeout

        if self.expected_titles:
            try:
                wait = WebDriverWait(self.driver, timeout)
                wait.until(
                    lambda driver: any(
                        title in driver.title for title in self.expected_titles
                    )
                )
                logger.debug(f"Page loaded with title: {self.title}")
            except TimeoutException:
                raise PageLoadError(
                    expected_title=str(self.expected_titles),
                    actual_title=self.title,
                    url=self.current_url,
                )

        # Wait for document ready state
        try:
            wait = WebDriverWait(None, timeout)
            wait.until(
                lambda driver: driver.execute_script("return document.readyState")
                == "complete"
            )
        except TimeoutException:
            logger.warning("Page did not reach complete ready state within timeout")

        return self

    def xǁBasePageǁwait_for_page_load__mutmut_22(
        self, timeout: float | None = None
    ) -> "BasePage":
        """
        Wait for the page to load completely.
        Checks for expected titles if defined.
        """
        timeout = timeout or self.timeout

        if self.expected_titles:
            try:
                wait = WebDriverWait(self.driver, timeout)
                wait.until(
                    lambda driver: any(
                        title in driver.title for title in self.expected_titles
                    )
                )
                logger.debug(f"Page loaded with title: {self.title}")
            except TimeoutException:
                raise PageLoadError(
                    expected_title=str(self.expected_titles),
                    actual_title=self.title,
                    url=self.current_url,
                )

        # Wait for document ready state
        try:
            wait = WebDriverWait(self.driver, None)
            wait.until(
                lambda driver: driver.execute_script("return document.readyState")
                == "complete"
            )
        except TimeoutException:
            logger.warning("Page did not reach complete ready state within timeout")

        return self

    def xǁBasePageǁwait_for_page_load__mutmut_23(
        self, timeout: float | None = None
    ) -> "BasePage":
        """
        Wait for the page to load completely.
        Checks for expected titles if defined.
        """
        timeout = timeout or self.timeout

        if self.expected_titles:
            try:
                wait = WebDriverWait(self.driver, timeout)
                wait.until(
                    lambda driver: any(
                        title in driver.title for title in self.expected_titles
                    )
                )
                logger.debug(f"Page loaded with title: {self.title}")
            except TimeoutException:
                raise PageLoadError(
                    expected_title=str(self.expected_titles),
                    actual_title=self.title,
                    url=self.current_url,
                )

        # Wait for document ready state
        try:
            wait = WebDriverWait(timeout)
            wait.until(
                lambda driver: driver.execute_script("return document.readyState")
                == "complete"
            )
        except TimeoutException:
            logger.warning("Page did not reach complete ready state within timeout")

        return self

    def xǁBasePageǁwait_for_page_load__mutmut_24(
        self, timeout: float | None = None
    ) -> "BasePage":
        """
        Wait for the page to load completely.
        Checks for expected titles if defined.
        """
        timeout = timeout or self.timeout

        if self.expected_titles:
            try:
                wait = WebDriverWait(self.driver, timeout)
                wait.until(
                    lambda driver: any(
                        title in driver.title for title in self.expected_titles
                    )
                )
                logger.debug(f"Page loaded with title: {self.title}")
            except TimeoutException:
                raise PageLoadError(
                    expected_title=str(self.expected_titles),
                    actual_title=self.title,
                    url=self.current_url,
                )

        # Wait for document ready state
        try:
            wait = WebDriverWait(
                self.driver,
            )
            wait.until(
                lambda driver: driver.execute_script("return document.readyState")
                == "complete"
            )
        except TimeoutException:
            logger.warning("Page did not reach complete ready state within timeout")

        return self

    def xǁBasePageǁwait_for_page_load__mutmut_25(
        self, timeout: float | None = None
    ) -> "BasePage":
        """
        Wait for the page to load completely.
        Checks for expected titles if defined.
        """
        timeout = timeout or self.timeout

        if self.expected_titles:
            try:
                wait = WebDriverWait(self.driver, timeout)
                wait.until(
                    lambda driver: any(
                        title in driver.title for title in self.expected_titles
                    )
                )
                logger.debug(f"Page loaded with title: {self.title}")
            except TimeoutException:
                raise PageLoadError(
                    expected_title=str(self.expected_titles),
                    actual_title=self.title,
                    url=self.current_url,
                )

        # Wait for document ready state
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(None)
        except TimeoutException:
            logger.warning("Page did not reach complete ready state within timeout")

        return self

    def xǁBasePageǁwait_for_page_load__mutmut_26(
        self, timeout: float | None = None
    ) -> "BasePage":
        """
        Wait for the page to load completely.
        Checks for expected titles if defined.
        """
        timeout = timeout or self.timeout

        if self.expected_titles:
            try:
                wait = WebDriverWait(self.driver, timeout)
                wait.until(
                    lambda driver: any(
                        title in driver.title for title in self.expected_titles
                    )
                )
                logger.debug(f"Page loaded with title: {self.title}")
            except TimeoutException:
                raise PageLoadError(
                    expected_title=str(self.expected_titles),
                    actual_title=self.title,
                    url=self.current_url,
                )

        # Wait for document ready state
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(lambda driver: None)
        except TimeoutException:
            logger.warning("Page did not reach complete ready state within timeout")

        return self

    def xǁBasePageǁwait_for_page_load__mutmut_27(
        self, timeout: float | None = None
    ) -> "BasePage":
        """
        Wait for the page to load completely.
        Checks for expected titles if defined.
        """
        timeout = timeout or self.timeout

        if self.expected_titles:
            try:
                wait = WebDriverWait(self.driver, timeout)
                wait.until(
                    lambda driver: any(
                        title in driver.title for title in self.expected_titles
                    )
                )
                logger.debug(f"Page loaded with title: {self.title}")
            except TimeoutException:
                raise PageLoadError(
                    expected_title=str(self.expected_titles),
                    actual_title=self.title,
                    url=self.current_url,
                )

        # Wait for document ready state
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(lambda driver: driver.execute_script(None) == "complete")
        except TimeoutException:
            logger.warning("Page did not reach complete ready state within timeout")

        return self

    def xǁBasePageǁwait_for_page_load__mutmut_28(
        self, timeout: float | None = None
    ) -> "BasePage":
        """
        Wait for the page to load completely.
        Checks for expected titles if defined.
        """
        timeout = timeout or self.timeout

        if self.expected_titles:
            try:
                wait = WebDriverWait(self.driver, timeout)
                wait.until(
                    lambda driver: any(
                        title in driver.title for title in self.expected_titles
                    )
                )
                logger.debug(f"Page loaded with title: {self.title}")
            except TimeoutException:
                raise PageLoadError(
                    expected_title=str(self.expected_titles),
                    actual_title=self.title,
                    url=self.current_url,
                )

        # Wait for document ready state
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(
                lambda driver: driver.execute_script("XXreturn document.readyStateXX")
                == "complete"
            )
        except TimeoutException:
            logger.warning("Page did not reach complete ready state within timeout")

        return self

    def xǁBasePageǁwait_for_page_load__mutmut_29(
        self, timeout: float | None = None
    ) -> "BasePage":
        """
        Wait for the page to load completely.
        Checks for expected titles if defined.
        """
        timeout = timeout or self.timeout

        if self.expected_titles:
            try:
                wait = WebDriverWait(self.driver, timeout)
                wait.until(
                    lambda driver: any(
                        title in driver.title for title in self.expected_titles
                    )
                )
                logger.debug(f"Page loaded with title: {self.title}")
            except TimeoutException:
                raise PageLoadError(
                    expected_title=str(self.expected_titles),
                    actual_title=self.title,
                    url=self.current_url,
                )

        # Wait for document ready state
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(
                lambda driver: driver.execute_script("return document.readystate")
                == "complete"
            )
        except TimeoutException:
            logger.warning("Page did not reach complete ready state within timeout")

        return self

    def xǁBasePageǁwait_for_page_load__mutmut_30(
        self, timeout: float | None = None
    ) -> "BasePage":
        """
        Wait for the page to load completely.
        Checks for expected titles if defined.
        """
        timeout = timeout or self.timeout

        if self.expected_titles:
            try:
                wait = WebDriverWait(self.driver, timeout)
                wait.until(
                    lambda driver: any(
                        title in driver.title for title in self.expected_titles
                    )
                )
                logger.debug(f"Page loaded with title: {self.title}")
            except TimeoutException:
                raise PageLoadError(
                    expected_title=str(self.expected_titles),
                    actual_title=self.title,
                    url=self.current_url,
                )

        # Wait for document ready state
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(
                lambda driver: driver.execute_script("RETURN DOCUMENT.READYSTATE")
                == "complete"
            )
        except TimeoutException:
            logger.warning("Page did not reach complete ready state within timeout")

        return self

    def xǁBasePageǁwait_for_page_load__mutmut_31(
        self, timeout: float | None = None
    ) -> "BasePage":
        """
        Wait for the page to load completely.
        Checks for expected titles if defined.
        """
        timeout = timeout or self.timeout

        if self.expected_titles:
            try:
                wait = WebDriverWait(self.driver, timeout)
                wait.until(
                    lambda driver: any(
                        title in driver.title for title in self.expected_titles
                    )
                )
                logger.debug(f"Page loaded with title: {self.title}")
            except TimeoutException:
                raise PageLoadError(
                    expected_title=str(self.expected_titles),
                    actual_title=self.title,
                    url=self.current_url,
                )

        # Wait for document ready state
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(
                lambda driver: driver.execute_script("return document.readyState")
                != "complete"
            )
        except TimeoutException:
            logger.warning("Page did not reach complete ready state within timeout")

        return self

    def xǁBasePageǁwait_for_page_load__mutmut_32(
        self, timeout: float | None = None
    ) -> "BasePage":
        """
        Wait for the page to load completely.
        Checks for expected titles if defined.
        """
        timeout = timeout or self.timeout

        if self.expected_titles:
            try:
                wait = WebDriverWait(self.driver, timeout)
                wait.until(
                    lambda driver: any(
                        title in driver.title for title in self.expected_titles
                    )
                )
                logger.debug(f"Page loaded with title: {self.title}")
            except TimeoutException:
                raise PageLoadError(
                    expected_title=str(self.expected_titles),
                    actual_title=self.title,
                    url=self.current_url,
                )

        # Wait for document ready state
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(
                lambda driver: driver.execute_script("return document.readyState")
                == "XXcompleteXX"
            )
        except TimeoutException:
            logger.warning("Page did not reach complete ready state within timeout")

        return self

    def xǁBasePageǁwait_for_page_load__mutmut_33(
        self, timeout: float | None = None
    ) -> "BasePage":
        """
        Wait for the page to load completely.
        Checks for expected titles if defined.
        """
        timeout = timeout or self.timeout

        if self.expected_titles:
            try:
                wait = WebDriverWait(self.driver, timeout)
                wait.until(
                    lambda driver: any(
                        title in driver.title for title in self.expected_titles
                    )
                )
                logger.debug(f"Page loaded with title: {self.title}")
            except TimeoutException:
                raise PageLoadError(
                    expected_title=str(self.expected_titles),
                    actual_title=self.title,
                    url=self.current_url,
                )

        # Wait for document ready state
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(
                lambda driver: driver.execute_script("return document.readyState")
                == "COMPLETE"
            )
        except TimeoutException:
            logger.warning("Page did not reach complete ready state within timeout")

        return self

    def xǁBasePageǁwait_for_page_load__mutmut_34(
        self, timeout: float | None = None
    ) -> "BasePage":
        """
        Wait for the page to load completely.
        Checks for expected titles if defined.
        """
        timeout = timeout or self.timeout

        if self.expected_titles:
            try:
                wait = WebDriverWait(self.driver, timeout)
                wait.until(
                    lambda driver: any(
                        title in driver.title for title in self.expected_titles
                    )
                )
                logger.debug(f"Page loaded with title: {self.title}")
            except TimeoutException:
                raise PageLoadError(
                    expected_title=str(self.expected_titles),
                    actual_title=self.title,
                    url=self.current_url,
                )

        # Wait for document ready state
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(
                lambda driver: driver.execute_script("return document.readyState")
                == "complete"
            )
        except TimeoutException:
            logger.warning(None)

        return self

    def xǁBasePageǁwait_for_page_load__mutmut_35(
        self, timeout: float | None = None
    ) -> "BasePage":
        """
        Wait for the page to load completely.
        Checks for expected titles if defined.
        """
        timeout = timeout or self.timeout

        if self.expected_titles:
            try:
                wait = WebDriverWait(self.driver, timeout)
                wait.until(
                    lambda driver: any(
                        title in driver.title for title in self.expected_titles
                    )
                )
                logger.debug(f"Page loaded with title: {self.title}")
            except TimeoutException:
                raise PageLoadError(
                    expected_title=str(self.expected_titles),
                    actual_title=self.title,
                    url=self.current_url,
                )

        # Wait for document ready state
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(
                lambda driver: driver.execute_script("return document.readyState")
                == "complete"
            )
        except TimeoutException:
            logger.warning("XXPage did not reach complete ready state within timeoutXX")

        return self

    def xǁBasePageǁwait_for_page_load__mutmut_36(
        self, timeout: float | None = None
    ) -> "BasePage":
        """
        Wait for the page to load completely.
        Checks for expected titles if defined.
        """
        timeout = timeout or self.timeout

        if self.expected_titles:
            try:
                wait = WebDriverWait(self.driver, timeout)
                wait.until(
                    lambda driver: any(
                        title in driver.title for title in self.expected_titles
                    )
                )
                logger.debug(f"Page loaded with title: {self.title}")
            except TimeoutException:
                raise PageLoadError(
                    expected_title=str(self.expected_titles),
                    actual_title=self.title,
                    url=self.current_url,
                )

        # Wait for document ready state
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(
                lambda driver: driver.execute_script("return document.readyState")
                == "complete"
            )
        except TimeoutException:
            logger.warning("page did not reach complete ready state within timeout")

        return self

    def xǁBasePageǁwait_for_page_load__mutmut_37(
        self, timeout: float | None = None
    ) -> "BasePage":
        """
        Wait for the page to load completely.
        Checks for expected titles if defined.
        """
        timeout = timeout or self.timeout

        if self.expected_titles:
            try:
                wait = WebDriverWait(self.driver, timeout)
                wait.until(
                    lambda driver: any(
                        title in driver.title for title in self.expected_titles
                    )
                )
                logger.debug(f"Page loaded with title: {self.title}")
            except TimeoutException:
                raise PageLoadError(
                    expected_title=str(self.expected_titles),
                    actual_title=self.title,
                    url=self.current_url,
                )

        # Wait for document ready state
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(
                lambda driver: driver.execute_script("return document.readyState")
                == "complete"
            )
        except TimeoutException:
            logger.warning("PAGE DID NOT REACH COMPLETE READY STATE WITHIN TIMEOUT")

        return self

    xǁBasePageǁwait_for_page_load__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁBasePageǁwait_for_page_load__mutmut_1": (
            xǁBasePageǁwait_for_page_load__mutmut_1
        ),
        "xǁBasePageǁwait_for_page_load__mutmut_2": (
            xǁBasePageǁwait_for_page_load__mutmut_2
        ),
        "xǁBasePageǁwait_for_page_load__mutmut_3": (
            xǁBasePageǁwait_for_page_load__mutmut_3
        ),
        "xǁBasePageǁwait_for_page_load__mutmut_4": (
            xǁBasePageǁwait_for_page_load__mutmut_4
        ),
        "xǁBasePageǁwait_for_page_load__mutmut_5": (
            xǁBasePageǁwait_for_page_load__mutmut_5
        ),
        "xǁBasePageǁwait_for_page_load__mutmut_6": (
            xǁBasePageǁwait_for_page_load__mutmut_6
        ),
        "xǁBasePageǁwait_for_page_load__mutmut_7": (
            xǁBasePageǁwait_for_page_load__mutmut_7
        ),
        "xǁBasePageǁwait_for_page_load__mutmut_8": (
            xǁBasePageǁwait_for_page_load__mutmut_8
        ),
        "xǁBasePageǁwait_for_page_load__mutmut_9": (
            xǁBasePageǁwait_for_page_load__mutmut_9
        ),
        "xǁBasePageǁwait_for_page_load__mutmut_10": (
            xǁBasePageǁwait_for_page_load__mutmut_10
        ),
        "xǁBasePageǁwait_for_page_load__mutmut_11": (
            xǁBasePageǁwait_for_page_load__mutmut_11
        ),
        "xǁBasePageǁwait_for_page_load__mutmut_12": (
            xǁBasePageǁwait_for_page_load__mutmut_12
        ),
        "xǁBasePageǁwait_for_page_load__mutmut_13": (
            xǁBasePageǁwait_for_page_load__mutmut_13
        ),
        "xǁBasePageǁwait_for_page_load__mutmut_14": (
            xǁBasePageǁwait_for_page_load__mutmut_14
        ),
        "xǁBasePageǁwait_for_page_load__mutmut_15": (
            xǁBasePageǁwait_for_page_load__mutmut_15
        ),
        "xǁBasePageǁwait_for_page_load__mutmut_16": (
            xǁBasePageǁwait_for_page_load__mutmut_16
        ),
        "xǁBasePageǁwait_for_page_load__mutmut_17": (
            xǁBasePageǁwait_for_page_load__mutmut_17
        ),
        "xǁBasePageǁwait_for_page_load__mutmut_18": (
            xǁBasePageǁwait_for_page_load__mutmut_18
        ),
        "xǁBasePageǁwait_for_page_load__mutmut_19": (
            xǁBasePageǁwait_for_page_load__mutmut_19
        ),
        "xǁBasePageǁwait_for_page_load__mutmut_20": (
            xǁBasePageǁwait_for_page_load__mutmut_20
        ),
        "xǁBasePageǁwait_for_page_load__mutmut_21": (
            xǁBasePageǁwait_for_page_load__mutmut_21
        ),
        "xǁBasePageǁwait_for_page_load__mutmut_22": (
            xǁBasePageǁwait_for_page_load__mutmut_22
        ),
        "xǁBasePageǁwait_for_page_load__mutmut_23": (
            xǁBasePageǁwait_for_page_load__mutmut_23
        ),
        "xǁBasePageǁwait_for_page_load__mutmut_24": (
            xǁBasePageǁwait_for_page_load__mutmut_24
        ),
        "xǁBasePageǁwait_for_page_load__mutmut_25": (
            xǁBasePageǁwait_for_page_load__mutmut_25
        ),
        "xǁBasePageǁwait_for_page_load__mutmut_26": (
            xǁBasePageǁwait_for_page_load__mutmut_26
        ),
        "xǁBasePageǁwait_for_page_load__mutmut_27": (
            xǁBasePageǁwait_for_page_load__mutmut_27
        ),
        "xǁBasePageǁwait_for_page_load__mutmut_28": (
            xǁBasePageǁwait_for_page_load__mutmut_28
        ),
        "xǁBasePageǁwait_for_page_load__mutmut_29": (
            xǁBasePageǁwait_for_page_load__mutmut_29
        ),
        "xǁBasePageǁwait_for_page_load__mutmut_30": (
            xǁBasePageǁwait_for_page_load__mutmut_30
        ),
        "xǁBasePageǁwait_for_page_load__mutmut_31": (
            xǁBasePageǁwait_for_page_load__mutmut_31
        ),
        "xǁBasePageǁwait_for_page_load__mutmut_32": (
            xǁBasePageǁwait_for_page_load__mutmut_32
        ),
        "xǁBasePageǁwait_for_page_load__mutmut_33": (
            xǁBasePageǁwait_for_page_load__mutmut_33
        ),
        "xǁBasePageǁwait_for_page_load__mutmut_34": (
            xǁBasePageǁwait_for_page_load__mutmut_34
        ),
        "xǁBasePageǁwait_for_page_load__mutmut_35": (
            xǁBasePageǁwait_for_page_load__mutmut_35
        ),
        "xǁBasePageǁwait_for_page_load__mutmut_36": (
            xǁBasePageǁwait_for_page_load__mutmut_36
        ),
        "xǁBasePageǁwait_for_page_load__mutmut_37": (
            xǁBasePageǁwait_for_page_load__mutmut_37
        ),
    }

    def wait_for_page_load(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁBasePageǁwait_for_page_load__mutmut_orig"),
            object.__getattribute__(
                self, "xǁBasePageǁwait_for_page_load__mutmut_mutants"
            ),
            args,
            kwargs,
            self,
        )
        return result

    wait_for_page_load.__signature__ = _mutmut_signature(
        xǁBasePageǁwait_for_page_load__mutmut_orig
    )
    xǁBasePageǁwait_for_page_load__mutmut_orig.__name__ = (
        "xǁBasePageǁwait_for_page_load"
    )

    def xǁBasePageǁrefresh__mutmut_orig(self) -> "BasePage":
        """Refresh the current page."""
        logger.debug("Refreshing page")
        self.driver.refresh()
        return self.wait_for_page_load()

    def xǁBasePageǁrefresh__mutmut_1(self) -> "BasePage":
        """Refresh the current page."""
        logger.debug(None)
        self.driver.refresh()
        return self.wait_for_page_load()

    def xǁBasePageǁrefresh__mutmut_2(self) -> "BasePage":
        """Refresh the current page."""
        logger.debug("XXRefreshing pageXX")
        self.driver.refresh()
        return self.wait_for_page_load()

    def xǁBasePageǁrefresh__mutmut_3(self) -> "BasePage":
        """Refresh the current page."""
        logger.debug("refreshing page")
        self.driver.refresh()
        return self.wait_for_page_load()

    def xǁBasePageǁrefresh__mutmut_4(self) -> "BasePage":
        """Refresh the current page."""
        logger.debug("REFRESHING PAGE")
        self.driver.refresh()
        return self.wait_for_page_load()

    xǁBasePageǁrefresh__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁBasePageǁrefresh__mutmut_1": xǁBasePageǁrefresh__mutmut_1,
        "xǁBasePageǁrefresh__mutmut_2": xǁBasePageǁrefresh__mutmut_2,
        "xǁBasePageǁrefresh__mutmut_3": xǁBasePageǁrefresh__mutmut_3,
        "xǁBasePageǁrefresh__mutmut_4": xǁBasePageǁrefresh__mutmut_4,
    }

    def refresh(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁBasePageǁrefresh__mutmut_orig"),
            object.__getattribute__(self, "xǁBasePageǁrefresh__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    refresh.__signature__ = _mutmut_signature(xǁBasePageǁrefresh__mutmut_orig)
    xǁBasePageǁrefresh__mutmut_orig.__name__ = "xǁBasePageǁrefresh"

    def xǁBasePageǁgo_back__mutmut_orig(self) -> "BasePage":
        """Navigate back in browser history."""
        logger.debug("Navigating back")
        self.driver.back()
        return self

    def xǁBasePageǁgo_back__mutmut_1(self) -> "BasePage":
        """Navigate back in browser history."""
        logger.debug(None)
        self.driver.back()
        return self

    def xǁBasePageǁgo_back__mutmut_2(self) -> "BasePage":
        """Navigate back in browser history."""
        logger.debug("XXNavigating backXX")
        self.driver.back()
        return self

    def xǁBasePageǁgo_back__mutmut_3(self) -> "BasePage":
        """Navigate back in browser history."""
        logger.debug("navigating back")
        self.driver.back()
        return self

    def xǁBasePageǁgo_back__mutmut_4(self) -> "BasePage":
        """Navigate back in browser history."""
        logger.debug("NAVIGATING BACK")
        self.driver.back()
        return self

    xǁBasePageǁgo_back__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁBasePageǁgo_back__mutmut_1": xǁBasePageǁgo_back__mutmut_1,
        "xǁBasePageǁgo_back__mutmut_2": xǁBasePageǁgo_back__mutmut_2,
        "xǁBasePageǁgo_back__mutmut_3": xǁBasePageǁgo_back__mutmut_3,
        "xǁBasePageǁgo_back__mutmut_4": xǁBasePageǁgo_back__mutmut_4,
    }

    def go_back(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁBasePageǁgo_back__mutmut_orig"),
            object.__getattribute__(self, "xǁBasePageǁgo_back__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    go_back.__signature__ = _mutmut_signature(xǁBasePageǁgo_back__mutmut_orig)
    xǁBasePageǁgo_back__mutmut_orig.__name__ = "xǁBasePageǁgo_back"

    def xǁBasePageǁgo_forward__mutmut_orig(self) -> "BasePage":
        """Navigate forward in browser history."""
        logger.debug("Navigating forward")
        self.driver.forward()
        return self

    def xǁBasePageǁgo_forward__mutmut_1(self) -> "BasePage":
        """Navigate forward in browser history."""
        logger.debug(None)
        self.driver.forward()
        return self

    def xǁBasePageǁgo_forward__mutmut_2(self) -> "BasePage":
        """Navigate forward in browser history."""
        logger.debug("XXNavigating forwardXX")
        self.driver.forward()
        return self

    def xǁBasePageǁgo_forward__mutmut_3(self) -> "BasePage":
        """Navigate forward in browser history."""
        logger.debug("navigating forward")
        self.driver.forward()
        return self

    def xǁBasePageǁgo_forward__mutmut_4(self) -> "BasePage":
        """Navigate forward in browser history."""
        logger.debug("NAVIGATING FORWARD")
        self.driver.forward()
        return self

    xǁBasePageǁgo_forward__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁBasePageǁgo_forward__mutmut_1": xǁBasePageǁgo_forward__mutmut_1,
        "xǁBasePageǁgo_forward__mutmut_2": xǁBasePageǁgo_forward__mutmut_2,
        "xǁBasePageǁgo_forward__mutmut_3": xǁBasePageǁgo_forward__mutmut_3,
        "xǁBasePageǁgo_forward__mutmut_4": xǁBasePageǁgo_forward__mutmut_4,
    }

    def go_forward(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁBasePageǁgo_forward__mutmut_orig"),
            object.__getattribute__(self, "xǁBasePageǁgo_forward__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    go_forward.__signature__ = _mutmut_signature(xǁBasePageǁgo_forward__mutmut_orig)
    xǁBasePageǁgo_forward__mutmut_orig.__name__ = "xǁBasePageǁgo_forward"

    def xǁBasePageǁwait_for_element__mutmut_orig(
        self, locator: Locator, timeout: float | None = None
    ) -> BaseElement:
        """
        Wait for an element to be present and return it.

        Args:
            locator: Element locator
            timeout: Wait timeout, defaults to page timeout
        """
        timeout = timeout or self.timeout
        element = BaseElement(self.driver, locator, timeout)
        element.wait_for_visible()
        return element

    def xǁBasePageǁwait_for_element__mutmut_1(
        self, locator: Locator, timeout: float | None = None
    ) -> BaseElement:
        """
        Wait for an element to be present and return it.

        Args:
            locator: Element locator
            timeout: Wait timeout, defaults to page timeout
        """
        timeout = None
        element = BaseElement(self.driver, locator, timeout)
        element.wait_for_visible()
        return element

    def xǁBasePageǁwait_for_element__mutmut_2(
        self, locator: Locator, timeout: float | None = None
    ) -> BaseElement:
        """
        Wait for an element to be present and return it.

        Args:
            locator: Element locator
            timeout: Wait timeout, defaults to page timeout
        """
        timeout = timeout and self.timeout
        element = BaseElement(self.driver, locator, timeout)
        element.wait_for_visible()
        return element

    def xǁBasePageǁwait_for_element__mutmut_3(
        self, locator: Locator, timeout: float | None = None
    ) -> BaseElement:
        """
        Wait for an element to be present and return it.

        Args:
            locator: Element locator
            timeout: Wait timeout, defaults to page timeout
        """
        timeout = timeout or self.timeout
        element = None
        element.wait_for_visible()
        return element

    def xǁBasePageǁwait_for_element__mutmut_4(
        self, locator: Locator, timeout: float | None = None
    ) -> BaseElement:
        """
        Wait for an element to be present and return it.

        Args:
            locator: Element locator
            timeout: Wait timeout, defaults to page timeout
        """
        timeout = timeout or self.timeout
        element = BaseElement(None, locator, timeout)
        element.wait_for_visible()
        return element

    def xǁBasePageǁwait_for_element__mutmut_5(
        self, locator: Locator, timeout: float | None = None
    ) -> BaseElement:
        """
        Wait for an element to be present and return it.

        Args:
            locator: Element locator
            timeout: Wait timeout, defaults to page timeout
        """
        timeout = timeout or self.timeout
        element = BaseElement(self.driver, None, timeout)
        element.wait_for_visible()
        return element

    def xǁBasePageǁwait_for_element__mutmut_6(
        self, locator: Locator, timeout: float | None = None
    ) -> BaseElement:
        """
        Wait for an element to be present and return it.

        Args:
            locator: Element locator
            timeout: Wait timeout, defaults to page timeout
        """
        timeout = timeout or self.timeout
        element = BaseElement(self.driver, locator, None)
        element.wait_for_visible()
        return element

    def xǁBasePageǁwait_for_element__mutmut_7(
        self, locator: Locator, timeout: float | None = None
    ) -> BaseElement:
        """
        Wait for an element to be present and return it.

        Args:
            locator: Element locator
            timeout: Wait timeout, defaults to page timeout
        """
        timeout = timeout or self.timeout
        element = BaseElement(locator, timeout)
        element.wait_for_visible()
        return element

    def xǁBasePageǁwait_for_element__mutmut_8(
        self, locator: Locator, timeout: float | None = None
    ) -> BaseElement:
        """
        Wait for an element to be present and return it.

        Args:
            locator: Element locator
            timeout: Wait timeout, defaults to page timeout
        """
        timeout = timeout or self.timeout
        element = BaseElement(self.driver, timeout)
        element.wait_for_visible()
        return element

    def xǁBasePageǁwait_for_element__mutmut_9(
        self, locator: Locator, timeout: float | None = None
    ) -> BaseElement:
        """
        Wait for an element to be present and return it.

        Args:
            locator: Element locator
            timeout: Wait timeout, defaults to page timeout
        """
        timeout = timeout or self.timeout
        element = BaseElement(
            self.driver,
            locator,
        )
        element.wait_for_visible()
        return element

    xǁBasePageǁwait_for_element__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁBasePageǁwait_for_element__mutmut_1": xǁBasePageǁwait_for_element__mutmut_1,
        "xǁBasePageǁwait_for_element__mutmut_2": xǁBasePageǁwait_for_element__mutmut_2,
        "xǁBasePageǁwait_for_element__mutmut_3": xǁBasePageǁwait_for_element__mutmut_3,
        "xǁBasePageǁwait_for_element__mutmut_4": xǁBasePageǁwait_for_element__mutmut_4,
        "xǁBasePageǁwait_for_element__mutmut_5": xǁBasePageǁwait_for_element__mutmut_5,
        "xǁBasePageǁwait_for_element__mutmut_6": xǁBasePageǁwait_for_element__mutmut_6,
        "xǁBasePageǁwait_for_element__mutmut_7": xǁBasePageǁwait_for_element__mutmut_7,
        "xǁBasePageǁwait_for_element__mutmut_8": xǁBasePageǁwait_for_element__mutmut_8,
        "xǁBasePageǁwait_for_element__mutmut_9": xǁBasePageǁwait_for_element__mutmut_9,
    }

    def wait_for_element(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁBasePageǁwait_for_element__mutmut_orig"),
            object.__getattribute__(
                self, "xǁBasePageǁwait_for_element__mutmut_mutants"
            ),
            args,
            kwargs,
            self,
        )
        return result

    wait_for_element.__signature__ = _mutmut_signature(
        xǁBasePageǁwait_for_element__mutmut_orig
    )
    xǁBasePageǁwait_for_element__mutmut_orig.__name__ = "xǁBasePageǁwait_for_element"

    def xǁBasePageǁwait_for_elements__mutmut_orig(
        self, locator: Locator, timeout: float | None = None
    ) -> list[BaseElement]:
        """
        Wait for multiple elements and return them as a list.

        Args:
            locator: Element locator
            timeout: Wait timeout, defaults to page timeout
        """
        timeout = timeout or self.timeout
        try:
            wait = WebDriverWait(self.driver, timeout)
            by, value = locator.selenium_locator
            elements = wait.until(EC.presence_of_all_elements_located((by, value)))
            return [BaseElement(self.driver, locator, timeout) for _ in elements]
        except TimeoutException as e:
            raise ElementNotFoundError(str(locator), timeout) from e

    def xǁBasePageǁwait_for_elements__mutmut_1(
        self, locator: Locator, timeout: float | None = None
    ) -> list[BaseElement]:
        """
        Wait for multiple elements and return them as a list.

        Args:
            locator: Element locator
            timeout: Wait timeout, defaults to page timeout
        """
        timeout = None
        try:
            wait = WebDriverWait(self.driver, timeout)
            by, value = locator.selenium_locator
            elements = wait.until(EC.presence_of_all_elements_located((by, value)))
            return [BaseElement(self.driver, locator, timeout) for _ in elements]
        except TimeoutException as e:
            raise ElementNotFoundError(str(locator), timeout) from e

    def xǁBasePageǁwait_for_elements__mutmut_2(
        self, locator: Locator, timeout: float | None = None
    ) -> list[BaseElement]:
        """
        Wait for multiple elements and return them as a list.

        Args:
            locator: Element locator
            timeout: Wait timeout, defaults to page timeout
        """
        timeout = timeout and self.timeout
        try:
            wait = WebDriverWait(self.driver, timeout)
            by, value = locator.selenium_locator
            elements = wait.until(EC.presence_of_all_elements_located((by, value)))
            return [BaseElement(self.driver, locator, timeout) for _ in elements]
        except TimeoutException as e:
            raise ElementNotFoundError(str(locator), timeout) from e

    def xǁBasePageǁwait_for_elements__mutmut_3(
        self, locator: Locator, timeout: float | None = None
    ) -> list[BaseElement]:
        """
        Wait for multiple elements and return them as a list.

        Args:
            locator: Element locator
            timeout: Wait timeout, defaults to page timeout
        """
        timeout = timeout or self.timeout
        try:
            wait = None
            by, value = locator.selenium_locator
            elements = wait.until(EC.presence_of_all_elements_located((by, value)))
            return [BaseElement(self.driver, locator, timeout) for _ in elements]
        except TimeoutException as e:
            raise ElementNotFoundError(str(locator), timeout) from e

    def xǁBasePageǁwait_for_elements__mutmut_4(
        self, locator: Locator, timeout: float | None = None
    ) -> list[BaseElement]:
        """
        Wait for multiple elements and return them as a list.

        Args:
            locator: Element locator
            timeout: Wait timeout, defaults to page timeout
        """
        timeout = timeout or self.timeout
        try:
            wait = WebDriverWait(None, timeout)
            by, value = locator.selenium_locator
            elements = wait.until(EC.presence_of_all_elements_located((by, value)))
            return [BaseElement(self.driver, locator, timeout) for _ in elements]
        except TimeoutException as e:
            raise ElementNotFoundError(str(locator), timeout) from e

    def xǁBasePageǁwait_for_elements__mutmut_5(
        self, locator: Locator, timeout: float | None = None
    ) -> list[BaseElement]:
        """
        Wait for multiple elements and return them as a list.

        Args:
            locator: Element locator
            timeout: Wait timeout, defaults to page timeout
        """
        timeout = timeout or self.timeout
        try:
            wait = WebDriverWait(self.driver, None)
            by, value = locator.selenium_locator
            elements = wait.until(EC.presence_of_all_elements_located((by, value)))
            return [BaseElement(self.driver, locator, timeout) for _ in elements]
        except TimeoutException as e:
            raise ElementNotFoundError(str(locator), timeout) from e

    def xǁBasePageǁwait_for_elements__mutmut_6(
        self, locator: Locator, timeout: float | None = None
    ) -> list[BaseElement]:
        """
        Wait for multiple elements and return them as a list.

        Args:
            locator: Element locator
            timeout: Wait timeout, defaults to page timeout
        """
        timeout = timeout or self.timeout
        try:
            wait = WebDriverWait(timeout)
            by, value = locator.selenium_locator
            elements = wait.until(EC.presence_of_all_elements_located((by, value)))
            return [BaseElement(self.driver, locator, timeout) for _ in elements]
        except TimeoutException as e:
            raise ElementNotFoundError(str(locator), timeout) from e

    def xǁBasePageǁwait_for_elements__mutmut_7(
        self, locator: Locator, timeout: float | None = None
    ) -> list[BaseElement]:
        """
        Wait for multiple elements and return them as a list.

        Args:
            locator: Element locator
            timeout: Wait timeout, defaults to page timeout
        """
        timeout = timeout or self.timeout
        try:
            wait = WebDriverWait(
                self.driver,
            )
            by, value = locator.selenium_locator
            elements = wait.until(EC.presence_of_all_elements_located((by, value)))
            return [BaseElement(self.driver, locator, timeout) for _ in elements]
        except TimeoutException as e:
            raise ElementNotFoundError(str(locator), timeout) from e

    def xǁBasePageǁwait_for_elements__mutmut_8(
        self, locator: Locator, timeout: float | None = None
    ) -> list[BaseElement]:
        """
        Wait for multiple elements and return them as a list.

        Args:
            locator: Element locator
            timeout: Wait timeout, defaults to page timeout
        """
        timeout = timeout or self.timeout
        try:
            wait = WebDriverWait(self.driver, timeout)
            by, value = None
            elements = wait.until(EC.presence_of_all_elements_located((by, value)))
            return [BaseElement(self.driver, locator, timeout) for _ in elements]
        except TimeoutException as e:
            raise ElementNotFoundError(str(locator), timeout) from e

    def xǁBasePageǁwait_for_elements__mutmut_9(
        self, locator: Locator, timeout: float | None = None
    ) -> list[BaseElement]:
        """
        Wait for multiple elements and return them as a list.

        Args:
            locator: Element locator
            timeout: Wait timeout, defaults to page timeout
        """
        timeout = timeout or self.timeout
        try:
            _wait = WebDriverWait(self.driver, timeout)
            by, value = locator.selenium_locator
            elements = None
            return [BaseElement(self.driver, locator, timeout) for _ in elements]
        except TimeoutException as e:
            raise ElementNotFoundError(str(locator), timeout) from e

    def xǁBasePageǁwait_for_elements__mutmut_10(
        self, locator: Locator, timeout: float | None = None
    ) -> list[BaseElement]:
        """
        Wait for multiple elements and return them as a list.

        Args:
            locator: Element locator
            timeout: Wait timeout, defaults to page timeout
        """
        timeout = timeout or self.timeout
        try:
            wait = WebDriverWait(self.driver, timeout)
            by, value = locator.selenium_locator
            elements = wait.until(None)
            return [BaseElement(self.driver, locator, timeout) for _ in elements]
        except TimeoutException as e:
            raise ElementNotFoundError(str(locator), timeout) from e

    def xǁBasePageǁwait_for_elements__mutmut_11(
        self, locator: Locator, timeout: float | None = None
    ) -> list[BaseElement]:
        """
        Wait for multiple elements and return them as a list.

        Args:
            locator: Element locator
            timeout: Wait timeout, defaults to page timeout
        """
        timeout = timeout or self.timeout
        try:
            wait = WebDriverWait(self.driver, timeout)
            by, value = locator.selenium_locator
            elements = wait.until(EC.presence_of_all_elements_located(None))
            return [BaseElement(self.driver, locator, timeout) for _ in elements]
        except TimeoutException as e:
            raise ElementNotFoundError(str(locator), timeout) from e

    def xǁBasePageǁwait_for_elements__mutmut_12(
        self, locator: Locator, timeout: float | None = None
    ) -> list[BaseElement]:
        """
        Wait for multiple elements and return them as a list.

        Args:
            locator: Element locator
            timeout: Wait timeout, defaults to page timeout
        """
        timeout = timeout or self.timeout
        try:
            wait = WebDriverWait(self.driver, timeout)
            by, value = locator.selenium_locator
            elements = wait.until(EC.presence_of_all_elements_located((by, value)))
            return [BaseElement(None, locator, timeout) for _ in elements]
        except TimeoutException as e:
            raise ElementNotFoundError(str(locator), timeout) from e

    def xǁBasePageǁwait_for_elements__mutmut_13(
        self, locator: Locator, timeout: float | None = None
    ) -> list[BaseElement]:
        """
        Wait for multiple elements and return them as a list.

        Args:
            locator: Element locator
            timeout: Wait timeout, defaults to page timeout
        """
        timeout = timeout or self.timeout
        try:
            wait = WebDriverWait(self.driver, timeout)
            by, value = locator.selenium_locator
            elements = wait.until(EC.presence_of_all_elements_located((by, value)))
            return [BaseElement(self.driver, None, timeout) for _ in elements]
        except TimeoutException as e:
            raise ElementNotFoundError(str(locator), timeout) from e

    def xǁBasePageǁwait_for_elements__mutmut_14(
        self, locator: Locator, timeout: float | None = None
    ) -> list[BaseElement]:
        """
        Wait for multiple elements and return them as a list.

        Args:
            locator: Element locator
            timeout: Wait timeout, defaults to page timeout
        """
        timeout = timeout or self.timeout
        try:
            wait = WebDriverWait(self.driver, timeout)
            by, value = locator.selenium_locator
            elements = wait.until(EC.presence_of_all_elements_located((by, value)))
            return [BaseElement(self.driver, locator, None) for _ in elements]
        except TimeoutException as e:
            raise ElementNotFoundError(str(locator), timeout) from e

    def xǁBasePageǁwait_for_elements__mutmut_15(
        self, locator: Locator, timeout: float | None = None
    ) -> list[BaseElement]:
        """
        Wait for multiple elements and return them as a list.

        Args:
            locator: Element locator
            timeout: Wait timeout, defaults to page timeout
        """
        timeout = timeout or self.timeout
        try:
            wait = WebDriverWait(self.driver, timeout)
            by, value = locator.selenium_locator
            elements = wait.until(EC.presence_of_all_elements_located((by, value)))
            return [BaseElement(locator, timeout) for _ in elements]
        except TimeoutException as e:
            raise ElementNotFoundError(str(locator), timeout) from e

    def xǁBasePageǁwait_for_elements__mutmut_16(
        self, locator: Locator, timeout: float | None = None
    ) -> list[BaseElement]:
        """
        Wait for multiple elements and return them as a list.

        Args:
            locator: Element locator
            timeout: Wait timeout, defaults to page timeout
        """
        timeout = timeout or self.timeout
        try:
            wait = WebDriverWait(self.driver, timeout)
            by, value = locator.selenium_locator
            elements = wait.until(EC.presence_of_all_elements_located((by, value)))
            return [BaseElement(self.driver, timeout) for _ in elements]
        except TimeoutException as e:
            raise ElementNotFoundError(str(locator), timeout) from e

    def xǁBasePageǁwait_for_elements__mutmut_17(
        self, locator: Locator, timeout: float | None = None
    ) -> list[BaseElement]:
        """
        Wait for multiple elements and return them as a list.

        Args:
            locator: Element locator
            timeout: Wait timeout, defaults to page timeout
        """
        timeout = timeout or self.timeout
        try:
            wait = WebDriverWait(self.driver, timeout)
            by, value = locator.selenium_locator
            elements = wait.until(EC.presence_of_all_elements_located((by, value)))
            return [
                BaseElement(
                    self.driver,
                    locator,
                )
                for _ in elements
            ]
        except TimeoutException as e:
            raise ElementNotFoundError(str(locator), timeout) from e

    def xǁBasePageǁwait_for_elements__mutmut_18(
        self, locator: Locator, timeout: float | None = None
    ) -> list[BaseElement]:
        """
        Wait for multiple elements and return them as a list.

        Args:
            locator: Element locator
            timeout: Wait timeout, defaults to page timeout
        """
        timeout = timeout or self.timeout
        try:
            wait = WebDriverWait(self.driver, timeout)
            by, value = locator.selenium_locator
            elements = wait.until(EC.presence_of_all_elements_located((by, value)))
            return [BaseElement(self.driver, locator, timeout) for _ in elements]
        except TimeoutException as e:
            raise ElementNotFoundError(None, timeout) from e

    def xǁBasePageǁwait_for_elements__mutmut_19(
        self, locator: Locator, timeout: float | None = None
    ) -> list[BaseElement]:
        """
        Wait for multiple elements and return them as a list.

        Args:
            locator: Element locator
            timeout: Wait timeout, defaults to page timeout
        """
        timeout = timeout or self.timeout
        try:
            wait = WebDriverWait(self.driver, timeout)
            by, value = locator.selenium_locator
            elements = wait.until(EC.presence_of_all_elements_located((by, value)))
            return [BaseElement(self.driver, locator, timeout) for _ in elements]
        except TimeoutException as e:
            raise ElementNotFoundError(str(locator), None) from e

    def xǁBasePageǁwait_for_elements__mutmut_20(
        self, locator: Locator, timeout: float | None = None
    ) -> list[BaseElement]:
        """
        Wait for multiple elements and return them as a list.

        Args:
            locator: Element locator
            timeout: Wait timeout, defaults to page timeout
        """
        timeout = timeout or self.timeout
        try:
            wait = WebDriverWait(self.driver, timeout)
            by, value = locator.selenium_locator
            elements = wait.until(EC.presence_of_all_elements_located((by, value)))
            return [BaseElement(self.driver, locator, timeout) for _ in elements]
        except TimeoutException as e:
            raise ElementNotFoundError(timeout) from e

    def xǁBasePageǁwait_for_elements__mutmut_21(
        self, locator: Locator, timeout: float | None = None
    ) -> list[BaseElement]:
        """
        Wait for multiple elements and return them as a list.

        Args:
            locator: Element locator
            timeout: Wait timeout, defaults to page timeout
        """
        timeout = timeout or self.timeout
        try:
            wait = WebDriverWait(self.driver, timeout)
            by, value = locator.selenium_locator
            elements = wait.until(EC.presence_of_all_elements_located((by, value)))
            return [BaseElement(self.driver, locator, timeout) for _ in elements]
        except TimeoutException as e:
            raise ElementNotFoundError(
                str(locator),
            ) from e

    def xǁBasePageǁwait_for_elements__mutmut_22(
        self, locator: Locator, timeout: float | None = None
    ) -> list[BaseElement]:
        """
        Wait for multiple elements and return them as a list.

        Args:
            locator: Element locator
            timeout: Wait timeout, defaults to page timeout
        """
        timeout = timeout or self.timeout
        try:
            wait = WebDriverWait(self.driver, timeout)
            by, value = locator.selenium_locator
            elements = wait.until(EC.presence_of_all_elements_located((by, value)))
            return [BaseElement(self.driver, locator, timeout) for _ in elements]
        except TimeoutException as e:
            raise ElementNotFoundError(str(None), timeout) from e

    xǁBasePageǁwait_for_elements__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁBasePageǁwait_for_elements__mutmut_1": (
            xǁBasePageǁwait_for_elements__mutmut_1
        ),
        "xǁBasePageǁwait_for_elements__mutmut_2": (
            xǁBasePageǁwait_for_elements__mutmut_2
        ),
        "xǁBasePageǁwait_for_elements__mutmut_3": (
            xǁBasePageǁwait_for_elements__mutmut_3
        ),
        "xǁBasePageǁwait_for_elements__mutmut_4": (
            xǁBasePageǁwait_for_elements__mutmut_4
        ),
        "xǁBasePageǁwait_for_elements__mutmut_5": (
            xǁBasePageǁwait_for_elements__mutmut_5
        ),
        "xǁBasePageǁwait_for_elements__mutmut_6": (
            xǁBasePageǁwait_for_elements__mutmut_6
        ),
        "xǁBasePageǁwait_for_elements__mutmut_7": (
            xǁBasePageǁwait_for_elements__mutmut_7
        ),
        "xǁBasePageǁwait_for_elements__mutmut_8": (
            xǁBasePageǁwait_for_elements__mutmut_8
        ),
        "xǁBasePageǁwait_for_elements__mutmut_9": (
            xǁBasePageǁwait_for_elements__mutmut_9
        ),
        "xǁBasePageǁwait_for_elements__mutmut_10": (
            xǁBasePageǁwait_for_elements__mutmut_10
        ),
        "xǁBasePageǁwait_for_elements__mutmut_11": (
            xǁBasePageǁwait_for_elements__mutmut_11
        ),
        "xǁBasePageǁwait_for_elements__mutmut_12": (
            xǁBasePageǁwait_for_elements__mutmut_12
        ),
        "xǁBasePageǁwait_for_elements__mutmut_13": (
            xǁBasePageǁwait_for_elements__mutmut_13
        ),
        "xǁBasePageǁwait_for_elements__mutmut_14": (
            xǁBasePageǁwait_for_elements__mutmut_14
        ),
        "xǁBasePageǁwait_for_elements__mutmut_15": (
            xǁBasePageǁwait_for_elements__mutmut_15
        ),
        "xǁBasePageǁwait_for_elements__mutmut_16": (
            xǁBasePageǁwait_for_elements__mutmut_16
        ),
        "xǁBasePageǁwait_for_elements__mutmut_17": (
            xǁBasePageǁwait_for_elements__mutmut_17
        ),
        "xǁBasePageǁwait_for_elements__mutmut_18": (
            xǁBasePageǁwait_for_elements__mutmut_18
        ),
        "xǁBasePageǁwait_for_elements__mutmut_19": (
            xǁBasePageǁwait_for_elements__mutmut_19
        ),
        "xǁBasePageǁwait_for_elements__mutmut_20": (
            xǁBasePageǁwait_for_elements__mutmut_20
        ),
        "xǁBasePageǁwait_for_elements__mutmut_21": (
            xǁBasePageǁwait_for_elements__mutmut_21
        ),
        "xǁBasePageǁwait_for_elements__mutmut_22": (
            xǁBasePageǁwait_for_elements__mutmut_22
        ),
    }

    def wait_for_elements(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁBasePageǁwait_for_elements__mutmut_orig"),
            object.__getattribute__(
                self, "xǁBasePageǁwait_for_elements__mutmut_mutants"
            ),
            args,
            kwargs,
            self,
        )
        return result

    wait_for_elements.__signature__ = _mutmut_signature(
        xǁBasePageǁwait_for_elements__mutmut_orig
    )
    xǁBasePageǁwait_for_elements__mutmut_orig.__name__ = "xǁBasePageǁwait_for_elements"

    def xǁBasePageǁis_element_present__mutmut_orig(self, locator: Locator) -> bool:
        """Check if an element is present on the page."""
        try:
            by, value = locator.selenium_locator
            self.driver.find_element(by, value)
            return True
        except:
            return False

    def xǁBasePageǁis_element_present__mutmut_1(self, locator: Locator) -> bool:
        """Check if an element is present on the page."""
        try:
            by, value = None
            self.driver.find_element(by, value)
            return True
        except:
            return False

    def xǁBasePageǁis_element_present__mutmut_2(self, locator: Locator) -> bool:
        """Check if an element is present on the page."""
        try:
            by, value = locator.selenium_locator
            self.driver.find_element(None, value)
            return True
        except:
            return False

    def xǁBasePageǁis_element_present__mutmut_3(self, locator: Locator) -> bool:
        """Check if an element is present on the page."""
        try:
            by, value = locator.selenium_locator
            self.driver.find_element(by, None)
            return True
        except:
            return False

    def xǁBasePageǁis_element_present__mutmut_4(self, locator: Locator) -> bool:
        """Check if an element is present on the page."""
        try:
            by, value = locator.selenium_locator
            self.driver.find_element(value)
            return True
        except:
            return False

    def xǁBasePageǁis_element_present__mutmut_5(self, locator: Locator) -> bool:
        """Check if an element is present on the page."""
        try:
            by, value = locator.selenium_locator
            self.driver.find_element(
                by,
            )
            return True
        except:
            return False

    def xǁBasePageǁis_element_present__mutmut_6(self, locator: Locator) -> bool:
        """Check if an element is present on the page."""
        try:
            by, value = locator.selenium_locator
            self.driver.find_element(by, value)
            return False
        except:
            return False

    def xǁBasePageǁis_element_present__mutmut_7(self, locator: Locator) -> bool:
        """Check if an element is present on the page."""
        try:
            by, value = locator.selenium_locator
            self.driver.find_element(by, value)
            return True
        except:
            return True

    xǁBasePageǁis_element_present__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁBasePageǁis_element_present__mutmut_1": (
            xǁBasePageǁis_element_present__mutmut_1
        ),
        "xǁBasePageǁis_element_present__mutmut_2": (
            xǁBasePageǁis_element_present__mutmut_2
        ),
        "xǁBasePageǁis_element_present__mutmut_3": (
            xǁBasePageǁis_element_present__mutmut_3
        ),
        "xǁBasePageǁis_element_present__mutmut_4": (
            xǁBasePageǁis_element_present__mutmut_4
        ),
        "xǁBasePageǁis_element_present__mutmut_5": (
            xǁBasePageǁis_element_present__mutmut_5
        ),
        "xǁBasePageǁis_element_present__mutmut_6": (
            xǁBasePageǁis_element_present__mutmut_6
        ),
        "xǁBasePageǁis_element_present__mutmut_7": (
            xǁBasePageǁis_element_present__mutmut_7
        ),
    }

    def is_element_present(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁBasePageǁis_element_present__mutmut_orig"),
            object.__getattribute__(
                self, "xǁBasePageǁis_element_present__mutmut_mutants"
            ),
            args,
            kwargs,
            self,
        )
        return result

    is_element_present.__signature__ = _mutmut_signature(
        xǁBasePageǁis_element_present__mutmut_orig
    )
    xǁBasePageǁis_element_present__mutmut_orig.__name__ = (
        "xǁBasePageǁis_element_present"
    )

    def xǁBasePageǁis_element_visible__mutmut_orig(self, locator: Locator) -> bool:
        """Check if an element is visible on the page."""
        try:
            element = BaseElement(self.driver, locator, 1.0)  # Short timeout
            return element.is_displayed
        except:
            return False

    def xǁBasePageǁis_element_visible__mutmut_1(self, locator: Locator) -> bool:
        """Check if an element is visible on the page."""
        try:
            element = None  # Short timeout
            return element.is_displayed
        except:
            return False

    def xǁBasePageǁis_element_visible__mutmut_2(self, locator: Locator) -> bool:
        """Check if an element is visible on the page."""
        try:
            element = BaseElement(None, locator, 1.0)  # Short timeout
            return element.is_displayed
        except:
            return False

    def xǁBasePageǁis_element_visible__mutmut_3(self, locator: Locator) -> bool:
        """Check if an element is visible on the page."""
        try:
            element = BaseElement(self.driver, None, 1.0)  # Short timeout
            return element.is_displayed
        except:
            return False

    def xǁBasePageǁis_element_visible__mutmut_4(self, locator: Locator) -> bool:
        """Check if an element is visible on the page."""
        try:
            element = BaseElement(self.driver, locator, None)  # Short timeout
            return element.is_displayed
        except:
            return False

    def xǁBasePageǁis_element_visible__mutmut_5(self, locator: Locator) -> bool:
        """Check if an element is visible on the page."""
        try:
            element = BaseElement(locator, 1.0)  # Short timeout
            return element.is_displayed
        except:
            return False

    def xǁBasePageǁis_element_visible__mutmut_6(self, locator: Locator) -> bool:
        """Check if an element is visible on the page."""
        try:
            element = BaseElement(self.driver, 1.0)  # Short timeout
            return element.is_displayed
        except:
            return False

    def xǁBasePageǁis_element_visible__mutmut_7(self, locator: Locator) -> bool:
        """Check if an element is visible on the page."""
        try:
            element = BaseElement(
                self.driver,
                locator,
            )  # Short timeout
            return element.is_displayed
        except:
            return False

    def xǁBasePageǁis_element_visible__mutmut_8(self, locator: Locator) -> bool:
        """Check if an element is visible on the page."""
        try:
            element = BaseElement(self.driver, locator, 2.0)  # Short timeout
            return element.is_displayed
        except:
            return False

    def xǁBasePageǁis_element_visible__mutmut_9(self, locator: Locator) -> bool:
        """Check if an element is visible on the page."""
        try:
            element = BaseElement(self.driver, locator, 1.0)  # Short timeout
            return element.is_displayed
        except:
            return True

    xǁBasePageǁis_element_visible__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁBasePageǁis_element_visible__mutmut_1": (
            xǁBasePageǁis_element_visible__mutmut_1
        ),
        "xǁBasePageǁis_element_visible__mutmut_2": (
            xǁBasePageǁis_element_visible__mutmut_2
        ),
        "xǁBasePageǁis_element_visible__mutmut_3": (
            xǁBasePageǁis_element_visible__mutmut_3
        ),
        "xǁBasePageǁis_element_visible__mutmut_4": (
            xǁBasePageǁis_element_visible__mutmut_4
        ),
        "xǁBasePageǁis_element_visible__mutmut_5": (
            xǁBasePageǁis_element_visible__mutmut_5
        ),
        "xǁBasePageǁis_element_visible__mutmut_6": (
            xǁBasePageǁis_element_visible__mutmut_6
        ),
        "xǁBasePageǁis_element_visible__mutmut_7": (
            xǁBasePageǁis_element_visible__mutmut_7
        ),
        "xǁBasePageǁis_element_visible__mutmut_8": (
            xǁBasePageǁis_element_visible__mutmut_8
        ),
        "xǁBasePageǁis_element_visible__mutmut_9": (
            xǁBasePageǁis_element_visible__mutmut_9
        ),
    }

    def is_element_visible(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁBasePageǁis_element_visible__mutmut_orig"),
            object.__getattribute__(
                self, "xǁBasePageǁis_element_visible__mutmut_mutants"
            ),
            args,
            kwargs,
            self,
        )
        return result

    is_element_visible.__signature__ = _mutmut_signature(
        xǁBasePageǁis_element_visible__mutmut_orig
    )
    xǁBasePageǁis_element_visible__mutmut_orig.__name__ = (
        "xǁBasePageǁis_element_visible"
    )

    def xǁBasePageǁget_button__mutmut_orig(self, locator: Locator) -> Button:
        """Get a button element."""
        return Button(self.driver, locator, self.timeout)

    def xǁBasePageǁget_button__mutmut_1(self, locator: Locator) -> Button:
        """Get a button element."""
        return Button(None, locator, self.timeout)

    def xǁBasePageǁget_button__mutmut_2(self, locator: Locator) -> Button:
        """Get a button element."""
        return Button(self.driver, None, self.timeout)

    def xǁBasePageǁget_button__mutmut_3(self, locator: Locator) -> Button:
        """Get a button element."""
        return Button(self.driver, locator, None)

    def xǁBasePageǁget_button__mutmut_4(self, locator: Locator) -> Button:
        """Get a button element."""
        return Button(locator, self.timeout)

    def xǁBasePageǁget_button__mutmut_5(self, locator: Locator) -> Button:
        """Get a button element."""
        return Button(self.driver, self.timeout)

    def xǁBasePageǁget_button__mutmut_6(self, locator: Locator) -> Button:
        """Get a button element."""
        return Button(
            self.driver,
            locator,
        )

    xǁBasePageǁget_button__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁBasePageǁget_button__mutmut_1": xǁBasePageǁget_button__mutmut_1,
        "xǁBasePageǁget_button__mutmut_2": xǁBasePageǁget_button__mutmut_2,
        "xǁBasePageǁget_button__mutmut_3": xǁBasePageǁget_button__mutmut_3,
        "xǁBasePageǁget_button__mutmut_4": xǁBasePageǁget_button__mutmut_4,
        "xǁBasePageǁget_button__mutmut_5": xǁBasePageǁget_button__mutmut_5,
        "xǁBasePageǁget_button__mutmut_6": xǁBasePageǁget_button__mutmut_6,
    }

    def get_button(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁBasePageǁget_button__mutmut_orig"),
            object.__getattribute__(self, "xǁBasePageǁget_button__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    get_button.__signature__ = _mutmut_signature(xǁBasePageǁget_button__mutmut_orig)
    xǁBasePageǁget_button__mutmut_orig.__name__ = "xǁBasePageǁget_button"

    def xǁBasePageǁget_text_input__mutmut_orig(self, locator: Locator) -> TextInput:
        """Get a text input element."""
        return TextInput(self.driver, locator, self.timeout)

    def xǁBasePageǁget_text_input__mutmut_1(self, locator: Locator) -> TextInput:
        """Get a text input element."""
        return TextInput(None, locator, self.timeout)

    def xǁBasePageǁget_text_input__mutmut_2(self, locator: Locator) -> TextInput:
        """Get a text input element."""
        return TextInput(self.driver, None, self.timeout)

    def xǁBasePageǁget_text_input__mutmut_3(self, locator: Locator) -> TextInput:
        """Get a text input element."""
        return TextInput(self.driver, locator, None)

    def xǁBasePageǁget_text_input__mutmut_4(self, locator: Locator) -> TextInput:
        """Get a text input element."""
        return TextInput(locator, self.timeout)

    def xǁBasePageǁget_text_input__mutmut_5(self, locator: Locator) -> TextInput:
        """Get a text input element."""
        return TextInput(self.driver, self.timeout)

    def xǁBasePageǁget_text_input__mutmut_6(self, locator: Locator) -> TextInput:
        """Get a text input element."""
        return TextInput(
            self.driver,
            locator,
        )

    xǁBasePageǁget_text_input__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁBasePageǁget_text_input__mutmut_1": xǁBasePageǁget_text_input__mutmut_1,
        "xǁBasePageǁget_text_input__mutmut_2": xǁBasePageǁget_text_input__mutmut_2,
        "xǁBasePageǁget_text_input__mutmut_3": xǁBasePageǁget_text_input__mutmut_3,
        "xǁBasePageǁget_text_input__mutmut_4": xǁBasePageǁget_text_input__mutmut_4,
        "xǁBasePageǁget_text_input__mutmut_5": xǁBasePageǁget_text_input__mutmut_5,
        "xǁBasePageǁget_text_input__mutmut_6": xǁBasePageǁget_text_input__mutmut_6,
    }

    def get_text_input(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁBasePageǁget_text_input__mutmut_orig"),
            object.__getattribute__(self, "xǁBasePageǁget_text_input__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    get_text_input.__signature__ = _mutmut_signature(
        xǁBasePageǁget_text_input__mutmut_orig
    )
    xǁBasePageǁget_text_input__mutmut_orig.__name__ = "xǁBasePageǁget_text_input"

    def xǁBasePageǁget_dropdown__mutmut_orig(self, locator: Locator) -> Dropdown:
        """Get a dropdown element."""
        return Dropdown(self.driver, locator, self.timeout)

    def xǁBasePageǁget_dropdown__mutmut_1(self, locator: Locator) -> Dropdown:
        """Get a dropdown element."""
        return Dropdown(None, locator, self.timeout)

    def xǁBasePageǁget_dropdown__mutmut_2(self, locator: Locator) -> Dropdown:
        """Get a dropdown element."""
        return Dropdown(self.driver, None, self.timeout)

    def xǁBasePageǁget_dropdown__mutmut_3(self, locator: Locator) -> Dropdown:
        """Get a dropdown element."""
        return Dropdown(self.driver, locator, None)

    def xǁBasePageǁget_dropdown__mutmut_4(self, locator: Locator) -> Dropdown:
        """Get a dropdown element."""
        return Dropdown(locator, self.timeout)

    def xǁBasePageǁget_dropdown__mutmut_5(self, locator: Locator) -> Dropdown:
        """Get a dropdown element."""
        return Dropdown(self.driver, self.timeout)

    def xǁBasePageǁget_dropdown__mutmut_6(self, locator: Locator) -> Dropdown:
        """Get a dropdown element."""
        return Dropdown(
            self.driver,
            locator,
        )

    xǁBasePageǁget_dropdown__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁBasePageǁget_dropdown__mutmut_1": xǁBasePageǁget_dropdown__mutmut_1,
        "xǁBasePageǁget_dropdown__mutmut_2": xǁBasePageǁget_dropdown__mutmut_2,
        "xǁBasePageǁget_dropdown__mutmut_3": xǁBasePageǁget_dropdown__mutmut_3,
        "xǁBasePageǁget_dropdown__mutmut_4": xǁBasePageǁget_dropdown__mutmut_4,
        "xǁBasePageǁget_dropdown__mutmut_5": xǁBasePageǁget_dropdown__mutmut_5,
        "xǁBasePageǁget_dropdown__mutmut_6": xǁBasePageǁget_dropdown__mutmut_6,
    }

    def get_dropdown(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁBasePageǁget_dropdown__mutmut_orig"),
            object.__getattribute__(self, "xǁBasePageǁget_dropdown__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    get_dropdown.__signature__ = _mutmut_signature(xǁBasePageǁget_dropdown__mutmut_orig)
    xǁBasePageǁget_dropdown__mutmut_orig.__name__ = "xǁBasePageǁget_dropdown"

    def xǁBasePageǁget_checkbox__mutmut_orig(self, locator: Locator) -> Checkbox:
        """Get a checkbox element."""
        return Checkbox(self.driver, locator, self.timeout)

    def xǁBasePageǁget_checkbox__mutmut_1(self, locator: Locator) -> Checkbox:
        """Get a checkbox element."""
        return Checkbox(None, locator, self.timeout)

    def xǁBasePageǁget_checkbox__mutmut_2(self, locator: Locator) -> Checkbox:
        """Get a checkbox element."""
        return Checkbox(self.driver, None, self.timeout)

    def xǁBasePageǁget_checkbox__mutmut_3(self, locator: Locator) -> Checkbox:
        """Get a checkbox element."""
        return Checkbox(self.driver, locator, None)

    def xǁBasePageǁget_checkbox__mutmut_4(self, locator: Locator) -> Checkbox:
        """Get a checkbox element."""
        return Checkbox(locator, self.timeout)

    def xǁBasePageǁget_checkbox__mutmut_5(self, locator: Locator) -> Checkbox:
        """Get a checkbox element."""
        return Checkbox(self.driver, self.timeout)

    def xǁBasePageǁget_checkbox__mutmut_6(self, locator: Locator) -> Checkbox:
        """Get a checkbox element."""
        return Checkbox(
            self.driver,
            locator,
        )

    xǁBasePageǁget_checkbox__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁBasePageǁget_checkbox__mutmut_1": xǁBasePageǁget_checkbox__mutmut_1,
        "xǁBasePageǁget_checkbox__mutmut_2": xǁBasePageǁget_checkbox__mutmut_2,
        "xǁBasePageǁget_checkbox__mutmut_3": xǁBasePageǁget_checkbox__mutmut_3,
        "xǁBasePageǁget_checkbox__mutmut_4": xǁBasePageǁget_checkbox__mutmut_4,
        "xǁBasePageǁget_checkbox__mutmut_5": xǁBasePageǁget_checkbox__mutmut_5,
        "xǁBasePageǁget_checkbox__mutmut_6": xǁBasePageǁget_checkbox__mutmut_6,
    }

    def get_checkbox(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁBasePageǁget_checkbox__mutmut_orig"),
            object.__getattribute__(self, "xǁBasePageǁget_checkbox__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    get_checkbox.__signature__ = _mutmut_signature(xǁBasePageǁget_checkbox__mutmut_orig)
    xǁBasePageǁget_checkbox__mutmut_orig.__name__ = "xǁBasePageǁget_checkbox"

    def xǁBasePageǁget_radio_button__mutmut_orig(self, locator: Locator) -> RadioButton:
        """Get a radio button element."""
        return RadioButton(self.driver, locator, self.timeout)

    def xǁBasePageǁget_radio_button__mutmut_1(self, locator: Locator) -> RadioButton:
        """Get a radio button element."""
        return RadioButton(None, locator, self.timeout)

    def xǁBasePageǁget_radio_button__mutmut_2(self, locator: Locator) -> RadioButton:
        """Get a radio button element."""
        return RadioButton(self.driver, None, self.timeout)

    def xǁBasePageǁget_radio_button__mutmut_3(self, locator: Locator) -> RadioButton:
        """Get a radio button element."""
        return RadioButton(self.driver, locator, None)

    def xǁBasePageǁget_radio_button__mutmut_4(self, locator: Locator) -> RadioButton:
        """Get a radio button element."""
        return RadioButton(locator, self.timeout)

    def xǁBasePageǁget_radio_button__mutmut_5(self, locator: Locator) -> RadioButton:
        """Get a radio button element."""
        return RadioButton(self.driver, self.timeout)

    def xǁBasePageǁget_radio_button__mutmut_6(self, locator: Locator) -> RadioButton:
        """Get a radio button element."""
        return RadioButton(
            self.driver,
            locator,
        )

    xǁBasePageǁget_radio_button__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁBasePageǁget_radio_button__mutmut_1": xǁBasePageǁget_radio_button__mutmut_1,
        "xǁBasePageǁget_radio_button__mutmut_2": xǁBasePageǁget_radio_button__mutmut_2,
        "xǁBasePageǁget_radio_button__mutmut_3": xǁBasePageǁget_radio_button__mutmut_3,
        "xǁBasePageǁget_radio_button__mutmut_4": xǁBasePageǁget_radio_button__mutmut_4,
        "xǁBasePageǁget_radio_button__mutmut_5": xǁBasePageǁget_radio_button__mutmut_5,
        "xǁBasePageǁget_radio_button__mutmut_6": xǁBasePageǁget_radio_button__mutmut_6,
    }

    def get_radio_button(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁBasePageǁget_radio_button__mutmut_orig"),
            object.__getattribute__(
                self, "xǁBasePageǁget_radio_button__mutmut_mutants"
            ),
            args,
            kwargs,
            self,
        )
        return result

    get_radio_button.__signature__ = _mutmut_signature(
        xǁBasePageǁget_radio_button__mutmut_orig
    )
    xǁBasePageǁget_radio_button__mutmut_orig.__name__ = "xǁBasePageǁget_radio_button"

    def xǁBasePageǁexecute_script__mutmut_orig(self, script: str, *args) -> Any:
        """Execute JavaScript in the browser."""
        return self.driver.execute_script(script, *args)

    def xǁBasePageǁexecute_script__mutmut_1(self, script: str, *args) -> Any:
        """Execute JavaScript in the browser."""
        return self.driver.execute_script(None, *args)

    def xǁBasePageǁexecute_script__mutmut_2(self, script: str, *args) -> Any:
        """Execute JavaScript in the browser."""
        return self.driver.execute_script(*args)

    def xǁBasePageǁexecute_script__mutmut_3(self, script: str, *args) -> Any:
        """Execute JavaScript in the browser."""
        return self.driver.execute_script(
            script,
        )

    xǁBasePageǁexecute_script__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁBasePageǁexecute_script__mutmut_1": xǁBasePageǁexecute_script__mutmut_1,
        "xǁBasePageǁexecute_script__mutmut_2": xǁBasePageǁexecute_script__mutmut_2,
        "xǁBasePageǁexecute_script__mutmut_3": xǁBasePageǁexecute_script__mutmut_3,
    }

    def execute_script(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁBasePageǁexecute_script__mutmut_orig"),
            object.__getattribute__(self, "xǁBasePageǁexecute_script__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    execute_script.__signature__ = _mutmut_signature(
        xǁBasePageǁexecute_script__mutmut_orig
    )
    xǁBasePageǁexecute_script__mutmut_orig.__name__ = "xǁBasePageǁexecute_script"

    def xǁBasePageǁscroll_to_top__mutmut_orig(self) -> "BasePage":
        """Scroll to the top of the page."""
        self.execute_script("window.scrollTo(0, 0);")
        return self

    def xǁBasePageǁscroll_to_top__mutmut_1(self) -> "BasePage":
        """Scroll to the top of the page."""
        self.execute_script(None)
        return self

    def xǁBasePageǁscroll_to_top__mutmut_2(self) -> "BasePage":
        """Scroll to the top of the page."""
        self.execute_script("XXwindow.scrollTo(0, 0);XX")
        return self

    def xǁBasePageǁscroll_to_top__mutmut_3(self) -> "BasePage":
        """Scroll to the top of the page."""
        self.execute_script("window.scrollto(0, 0);")
        return self

    def xǁBasePageǁscroll_to_top__mutmut_4(self) -> "BasePage":
        """Scroll to the top of the page."""
        self.execute_script("WINDOW.SCROLLTO(0, 0);")
        return self

    xǁBasePageǁscroll_to_top__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁBasePageǁscroll_to_top__mutmut_1": xǁBasePageǁscroll_to_top__mutmut_1,
        "xǁBasePageǁscroll_to_top__mutmut_2": xǁBasePageǁscroll_to_top__mutmut_2,
        "xǁBasePageǁscroll_to_top__mutmut_3": xǁBasePageǁscroll_to_top__mutmut_3,
        "xǁBasePageǁscroll_to_top__mutmut_4": xǁBasePageǁscroll_to_top__mutmut_4,
    }

    def scroll_to_top(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁBasePageǁscroll_to_top__mutmut_orig"),
            object.__getattribute__(self, "xǁBasePageǁscroll_to_top__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    scroll_to_top.__signature__ = _mutmut_signature(
        xǁBasePageǁscroll_to_top__mutmut_orig
    )
    xǁBasePageǁscroll_to_top__mutmut_orig.__name__ = "xǁBasePageǁscroll_to_top"

    def xǁBasePageǁscroll_to_bottom__mutmut_orig(self) -> "BasePage":
        """Scroll to the bottom of the page."""
        self.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        return self

    def xǁBasePageǁscroll_to_bottom__mutmut_1(self) -> "BasePage":
        """Scroll to the bottom of the page."""
        self.execute_script(None)
        return self

    def xǁBasePageǁscroll_to_bottom__mutmut_2(self) -> "BasePage":
        """Scroll to the bottom of the page."""
        self.execute_script("XXwindow.scrollTo(0, document.body.scrollHeight);XX")
        return self

    def xǁBasePageǁscroll_to_bottom__mutmut_3(self) -> "BasePage":
        """Scroll to the bottom of the page."""
        self.execute_script("window.scrollto(0, document.body.scrollheight);")
        return self

    def xǁBasePageǁscroll_to_bottom__mutmut_4(self) -> "BasePage":
        """Scroll to the bottom of the page."""
        self.execute_script("WINDOW.SCROLLTO(0, DOCUMENT.BODY.SCROLLHEIGHT);")
        return self

    xǁBasePageǁscroll_to_bottom__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁBasePageǁscroll_to_bottom__mutmut_1": xǁBasePageǁscroll_to_bottom__mutmut_1,
        "xǁBasePageǁscroll_to_bottom__mutmut_2": xǁBasePageǁscroll_to_bottom__mutmut_2,
        "xǁBasePageǁscroll_to_bottom__mutmut_3": xǁBasePageǁscroll_to_bottom__mutmut_3,
        "xǁBasePageǁscroll_to_bottom__mutmut_4": xǁBasePageǁscroll_to_bottom__mutmut_4,
    }

    def scroll_to_bottom(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁBasePageǁscroll_to_bottom__mutmut_orig"),
            object.__getattribute__(
                self, "xǁBasePageǁscroll_to_bottom__mutmut_mutants"
            ),
            args,
            kwargs,
            self,
        )
        return result

    scroll_to_bottom.__signature__ = _mutmut_signature(
        xǁBasePageǁscroll_to_bottom__mutmut_orig
    )
    xǁBasePageǁscroll_to_bottom__mutmut_orig.__name__ = "xǁBasePageǁscroll_to_bottom"

    def xǁBasePageǁtake_screenshot__mutmut_orig(
        self, filename: str | Path | None = None
    ) -> Path:
        """
        Take a screenshot of the current page.

        Args:
            filename: Optional filename, defaults to timestamp-based name

        Returns:
            Path to the saved screenshot
        """
        if filename is None:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"

        screenshot_path = Path(filename)
        if not screenshot_path.is_absolute():
            screenshot_path = Path.cwd() / "screenshots" / screenshot_path

        # Ensure directory exists
        screenshot_path.parent.mkdir(parents=True, exist_ok=True)

        success = self.driver.get_screenshot_as_file(str(screenshot_path))
        if success:
            logger.info(f"Screenshot saved: {screenshot_path}")
        else:
            logger.error(f"Failed to save screenshot: {screenshot_path}")

        return screenshot_path

    def xǁBasePageǁtake_screenshot__mutmut_1(
        self, filename: str | Path | None = None
    ) -> Path:
        """
        Take a screenshot of the current page.

        Args:
            filename: Optional filename, defaults to timestamp-based name

        Returns:
            Path to the saved screenshot
        """
        if filename is not None:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"

        screenshot_path = Path(filename)
        if not screenshot_path.is_absolute():
            screenshot_path = Path.cwd() / "screenshots" / screenshot_path

        # Ensure directory exists
        screenshot_path.parent.mkdir(parents=True, exist_ok=True)

        success = self.driver.get_screenshot_as_file(str(screenshot_path))
        if success:
            logger.info(f"Screenshot saved: {screenshot_path}")
        else:
            logger.error(f"Failed to save screenshot: {screenshot_path}")

        return screenshot_path

    def xǁBasePageǁtake_screenshot__mutmut_2(
        self, filename: str | Path | None = None
    ) -> Path:
        """
        Take a screenshot of the current page.

        Args:
            filename: Optional filename, defaults to timestamp-based name

        Returns:
            Path to the saved screenshot
        """
        if filename is None:
            timestamp = None
            filename = f"screenshot_{timestamp}.png"

        screenshot_path = Path(filename)
        if not screenshot_path.is_absolute():
            screenshot_path = Path.cwd() / "screenshots" / screenshot_path

        # Ensure directory exists
        screenshot_path.parent.mkdir(parents=True, exist_ok=True)

        success = self.driver.get_screenshot_as_file(str(screenshot_path))
        if success:
            logger.info(f"Screenshot saved: {screenshot_path}")
        else:
            logger.error(f"Failed to save screenshot: {screenshot_path}")

        return screenshot_path

    def xǁBasePageǁtake_screenshot__mutmut_3(
        self, filename: str | Path | None = None
    ) -> Path:
        """
        Take a screenshot of the current page.

        Args:
            filename: Optional filename, defaults to timestamp-based name

        Returns:
            Path to the saved screenshot
        """
        if filename is None:
            timestamp = time.strftime(None)
            filename = f"screenshot_{timestamp}.png"

        screenshot_path = Path(filename)
        if not screenshot_path.is_absolute():
            screenshot_path = Path.cwd() / "screenshots" / screenshot_path

        # Ensure directory exists
        screenshot_path.parent.mkdir(parents=True, exist_ok=True)

        success = self.driver.get_screenshot_as_file(str(screenshot_path))
        if success:
            logger.info(f"Screenshot saved: {screenshot_path}")
        else:
            logger.error(f"Failed to save screenshot: {screenshot_path}")

        return screenshot_path

    def xǁBasePageǁtake_screenshot__mutmut_4(
        self, filename: str | Path | None = None
    ) -> Path:
        """
        Take a screenshot of the current page.

        Args:
            filename: Optional filename, defaults to timestamp-based name

        Returns:
            Path to the saved screenshot
        """
        if filename is None:
            timestamp = time.strftime("XX%Y%m%d_%H%M%SXX")
            filename = f"screenshot_{timestamp}.png"

        screenshot_path = Path(filename)
        if not screenshot_path.is_absolute():
            screenshot_path = Path.cwd() / "screenshots" / screenshot_path

        # Ensure directory exists
        screenshot_path.parent.mkdir(parents=True, exist_ok=True)

        success = self.driver.get_screenshot_as_file(str(screenshot_path))
        if success:
            logger.info(f"Screenshot saved: {screenshot_path}")
        else:
            logger.error(f"Failed to save screenshot: {screenshot_path}")

        return screenshot_path

    def xǁBasePageǁtake_screenshot__mutmut_5(
        self, filename: str | Path | None = None
    ) -> Path:
        """
        Take a screenshot of the current page.

        Args:
            filename: Optional filename, defaults to timestamp-based name

        Returns:
            Path to the saved screenshot
        """
        if filename is None:
            timestamp = time.strftime("%y%m%d_%h%m%s")
            filename = f"screenshot_{timestamp}.png"

        screenshot_path = Path(filename)
        if not screenshot_path.is_absolute():
            screenshot_path = Path.cwd() / "screenshots" / screenshot_path

        # Ensure directory exists
        screenshot_path.parent.mkdir(parents=True, exist_ok=True)

        success = self.driver.get_screenshot_as_file(str(screenshot_path))
        if success:
            logger.info(f"Screenshot saved: {screenshot_path}")
        else:
            logger.error(f"Failed to save screenshot: {screenshot_path}")

        return screenshot_path

    def xǁBasePageǁtake_screenshot__mutmut_6(
        self, filename: str | Path | None = None
    ) -> Path:
        """
        Take a screenshot of the current page.

        Args:
            filename: Optional filename, defaults to timestamp-based name

        Returns:
            Path to the saved screenshot
        """
        if filename is None:
            timestamp = time.strftime("%Y%M%D_%H%M%S")
            filename = f"screenshot_{timestamp}.png"

        screenshot_path = Path(filename)
        if not screenshot_path.is_absolute():
            screenshot_path = Path.cwd() / "screenshots" / screenshot_path

        # Ensure directory exists
        screenshot_path.parent.mkdir(parents=True, exist_ok=True)

        success = self.driver.get_screenshot_as_file(str(screenshot_path))
        if success:
            logger.info(f"Screenshot saved: {screenshot_path}")
        else:
            logger.error(f"Failed to save screenshot: {screenshot_path}")

        return screenshot_path

    def xǁBasePageǁtake_screenshot__mutmut_7(
        self, filename: str | Path | None = None
    ) -> Path:
        """
        Take a screenshot of the current page.

        Args:
            filename: Optional filename, defaults to timestamp-based name

        Returns:
            Path to the saved screenshot
        """
        if filename is None:
            _timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = None

        screenshot_path = Path(filename)
        if not screenshot_path.is_absolute():
            screenshot_path = Path.cwd() / "screenshots" / screenshot_path

        # Ensure directory exists
        screenshot_path.parent.mkdir(parents=True, exist_ok=True)

        success = self.driver.get_screenshot_as_file(str(screenshot_path))
        if success:
            logger.info(f"Screenshot saved: {screenshot_path}")
        else:
            logger.error(f"Failed to save screenshot: {screenshot_path}")

        return screenshot_path

    def xǁBasePageǁtake_screenshot__mutmut_8(
        self, filename: str | Path | None = None
    ) -> Path:
        """
        Take a screenshot of the current page.

        Args:
            filename: Optional filename, defaults to timestamp-based name

        Returns:
            Path to the saved screenshot
        """
        if filename is None:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"

        screenshot_path = None
        if not screenshot_path.is_absolute():
            screenshot_path = Path.cwd() / "screenshots" / screenshot_path

        # Ensure directory exists
        screenshot_path.parent.mkdir(parents=True, exist_ok=True)

        success = self.driver.get_screenshot_as_file(str(screenshot_path))
        if success:
            logger.info(f"Screenshot saved: {screenshot_path}")
        else:
            logger.error(f"Failed to save screenshot: {screenshot_path}")

        return screenshot_path

    def xǁBasePageǁtake_screenshot__mutmut_9(
        self, filename: str | Path | None = None
    ) -> Path:
        """
        Take a screenshot of the current page.

        Args:
            filename: Optional filename, defaults to timestamp-based name

        Returns:
            Path to the saved screenshot
        """
        if filename is None:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"

        screenshot_path = Path(None)
        if not screenshot_path.is_absolute():
            screenshot_path = Path.cwd() / "screenshots" / screenshot_path

        # Ensure directory exists
        screenshot_path.parent.mkdir(parents=True, exist_ok=True)

        success = self.driver.get_screenshot_as_file(str(screenshot_path))
        if success:
            logger.info(f"Screenshot saved: {screenshot_path}")
        else:
            logger.error(f"Failed to save screenshot: {screenshot_path}")

        return screenshot_path

    def xǁBasePageǁtake_screenshot__mutmut_10(
        self, filename: str | Path | None = None
    ) -> Path:
        """
        Take a screenshot of the current page.

        Args:
            filename: Optional filename, defaults to timestamp-based name

        Returns:
            Path to the saved screenshot
        """
        if filename is None:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"

        screenshot_path = Path(filename)
        if screenshot_path.is_absolute():
            screenshot_path = Path.cwd() / "screenshots" / screenshot_path

        # Ensure directory exists
        screenshot_path.parent.mkdir(parents=True, exist_ok=True)

        success = self.driver.get_screenshot_as_file(str(screenshot_path))
        if success:
            logger.info(f"Screenshot saved: {screenshot_path}")
        else:
            logger.error(f"Failed to save screenshot: {screenshot_path}")

        return screenshot_path

    def xǁBasePageǁtake_screenshot__mutmut_11(
        self, filename: str | Path | None = None
    ) -> Path:
        """
        Take a screenshot of the current page.

        Args:
            filename: Optional filename, defaults to timestamp-based name

        Returns:
            Path to the saved screenshot
        """
        if filename is None:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"

        screenshot_path = Path(filename)
        if not screenshot_path.is_absolute():
            screenshot_path = None

        # Ensure directory exists
        screenshot_path.parent.mkdir(parents=True, exist_ok=True)

        success = self.driver.get_screenshot_as_file(str(screenshot_path))
        if success:
            logger.info(f"Screenshot saved: {screenshot_path}")
        else:
            logger.error(f"Failed to save screenshot: {screenshot_path}")

        return screenshot_path

    def xǁBasePageǁtake_screenshot__mutmut_12(
        self, filename: str | Path | None = None
    ) -> Path:
        """
        Take a screenshot of the current page.

        Args:
            filename: Optional filename, defaults to timestamp-based name

        Returns:
            Path to the saved screenshot
        """
        if filename is None:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"

        screenshot_path = Path(filename)
        if not screenshot_path.is_absolute():
            screenshot_path = Path.cwd() / "screenshots" * screenshot_path

        # Ensure directory exists
        screenshot_path.parent.mkdir(parents=True, exist_ok=True)

        success = self.driver.get_screenshot_as_file(str(screenshot_path))
        if success:
            logger.info(f"Screenshot saved: {screenshot_path}")
        else:
            logger.error(f"Failed to save screenshot: {screenshot_path}")

        return screenshot_path

    def xǁBasePageǁtake_screenshot__mutmut_13(
        self, filename: str | Path | None = None
    ) -> Path:
        """
        Take a screenshot of the current page.

        Args:
            filename: Optional filename, defaults to timestamp-based name

        Returns:
            Path to the saved screenshot
        """
        if filename is None:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"

        screenshot_path = Path(filename)
        if not screenshot_path.is_absolute():
            screenshot_path = Path.cwd() * "screenshots" / screenshot_path

        # Ensure directory exists
        screenshot_path.parent.mkdir(parents=True, exist_ok=True)

        success = self.driver.get_screenshot_as_file(str(screenshot_path))
        if success:
            logger.info(f"Screenshot saved: {screenshot_path}")
        else:
            logger.error(f"Failed to save screenshot: {screenshot_path}")

        return screenshot_path

    def xǁBasePageǁtake_screenshot__mutmut_14(
        self, filename: str | Path | None = None
    ) -> Path:
        """
        Take a screenshot of the current page.

        Args:
            filename: Optional filename, defaults to timestamp-based name

        Returns:
            Path to the saved screenshot
        """
        if filename is None:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"

        screenshot_path = Path(filename)
        if not screenshot_path.is_absolute():
            screenshot_path = Path.cwd() / "XXscreenshotsXX" / screenshot_path

        # Ensure directory exists
        screenshot_path.parent.mkdir(parents=True, exist_ok=True)

        success = self.driver.get_screenshot_as_file(str(screenshot_path))
        if success:
            logger.info(f"Screenshot saved: {screenshot_path}")
        else:
            logger.error(f"Failed to save screenshot: {screenshot_path}")

        return screenshot_path

    def xǁBasePageǁtake_screenshot__mutmut_15(
        self, filename: str | Path | None = None
    ) -> Path:
        """
        Take a screenshot of the current page.

        Args:
            filename: Optional filename, defaults to timestamp-based name

        Returns:
            Path to the saved screenshot
        """
        if filename is None:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"

        screenshot_path = Path(filename)
        if not screenshot_path.is_absolute():
            screenshot_path = Path.cwd() / "SCREENSHOTS" / screenshot_path

        # Ensure directory exists
        screenshot_path.parent.mkdir(parents=True, exist_ok=True)

        success = self.driver.get_screenshot_as_file(str(screenshot_path))
        if success:
            logger.info(f"Screenshot saved: {screenshot_path}")
        else:
            logger.error(f"Failed to save screenshot: {screenshot_path}")

        return screenshot_path

    def xǁBasePageǁtake_screenshot__mutmut_16(
        self, filename: str | Path | None = None
    ) -> Path:
        """
        Take a screenshot of the current page.

        Args:
            filename: Optional filename, defaults to timestamp-based name

        Returns:
            Path to the saved screenshot
        """
        if filename is None:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"

        screenshot_path = Path(filename)
        if not screenshot_path.is_absolute():
            screenshot_path = Path.cwd() / "screenshots" / screenshot_path

        # Ensure directory exists
        screenshot_path.parent.mkdir(parents=None, exist_ok=True)

        success = self.driver.get_screenshot_as_file(str(screenshot_path))
        if success:
            logger.info(f"Screenshot saved: {screenshot_path}")
        else:
            logger.error(f"Failed to save screenshot: {screenshot_path}")

        return screenshot_path

    def xǁBasePageǁtake_screenshot__mutmut_17(
        self, filename: str | Path | None = None
    ) -> Path:
        """
        Take a screenshot of the current page.

        Args:
            filename: Optional filename, defaults to timestamp-based name

        Returns:
            Path to the saved screenshot
        """
        if filename is None:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"

        screenshot_path = Path(filename)
        if not screenshot_path.is_absolute():
            screenshot_path = Path.cwd() / "screenshots" / screenshot_path

        # Ensure directory exists
        screenshot_path.parent.mkdir(parents=True, exist_ok=None)

        success = self.driver.get_screenshot_as_file(str(screenshot_path))
        if success:
            logger.info(f"Screenshot saved: {screenshot_path}")
        else:
            logger.error(f"Failed to save screenshot: {screenshot_path}")

        return screenshot_path

    def xǁBasePageǁtake_screenshot__mutmut_18(
        self, filename: str | Path | None = None
    ) -> Path:
        """
        Take a screenshot of the current page.

        Args:
            filename: Optional filename, defaults to timestamp-based name

        Returns:
            Path to the saved screenshot
        """
        if filename is None:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"

        screenshot_path = Path(filename)
        if not screenshot_path.is_absolute():
            screenshot_path = Path.cwd() / "screenshots" / screenshot_path

        # Ensure directory exists
        screenshot_path.parent.mkdir(exist_ok=True)

        success = self.driver.get_screenshot_as_file(str(screenshot_path))
        if success:
            logger.info(f"Screenshot saved: {screenshot_path}")
        else:
            logger.error(f"Failed to save screenshot: {screenshot_path}")

        return screenshot_path

    def xǁBasePageǁtake_screenshot__mutmut_19(
        self, filename: str | Path | None = None
    ) -> Path:
        """
        Take a screenshot of the current page.

        Args:
            filename: Optional filename, defaults to timestamp-based name

        Returns:
            Path to the saved screenshot
        """
        if filename is None:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"

        screenshot_path = Path(filename)
        if not screenshot_path.is_absolute():
            screenshot_path = Path.cwd() / "screenshots" / screenshot_path

        # Ensure directory exists
        screenshot_path.parent.mkdir(
            parents=True,
        )

        success = self.driver.get_screenshot_as_file(str(screenshot_path))
        if success:
            logger.info(f"Screenshot saved: {screenshot_path}")
        else:
            logger.error(f"Failed to save screenshot: {screenshot_path}")

        return screenshot_path

    def xǁBasePageǁtake_screenshot__mutmut_20(
        self, filename: str | Path | None = None
    ) -> Path:
        """
        Take a screenshot of the current page.

        Args:
            filename: Optional filename, defaults to timestamp-based name

        Returns:
            Path to the saved screenshot
        """
        if filename is None:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"

        screenshot_path = Path(filename)
        if not screenshot_path.is_absolute():
            screenshot_path = Path.cwd() / "screenshots" / screenshot_path

        # Ensure directory exists
        screenshot_path.parent.mkdir(parents=False, exist_ok=True)

        success = self.driver.get_screenshot_as_file(str(screenshot_path))
        if success:
            logger.info(f"Screenshot saved: {screenshot_path}")
        else:
            logger.error(f"Failed to save screenshot: {screenshot_path}")

        return screenshot_path

    def xǁBasePageǁtake_screenshot__mutmut_21(
        self, filename: str | Path | None = None
    ) -> Path:
        """
        Take a screenshot of the current page.

        Args:
            filename: Optional filename, defaults to timestamp-based name

        Returns:
            Path to the saved screenshot
        """
        if filename is None:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"

        screenshot_path = Path(filename)
        if not screenshot_path.is_absolute():
            screenshot_path = Path.cwd() / "screenshots" / screenshot_path

        # Ensure directory exists
        screenshot_path.parent.mkdir(parents=True, exist_ok=False)

        success = self.driver.get_screenshot_as_file(str(screenshot_path))
        if success:
            logger.info(f"Screenshot saved: {screenshot_path}")
        else:
            logger.error(f"Failed to save screenshot: {screenshot_path}")

        return screenshot_path

    def xǁBasePageǁtake_screenshot__mutmut_22(
        self, filename: str | Path | None = None
    ) -> Path:
        """
        Take a screenshot of the current page.

        Args:
            filename: Optional filename, defaults to timestamp-based name

        Returns:
            Path to the saved screenshot
        """
        if filename is None:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"

        screenshot_path = Path(filename)
        if not screenshot_path.is_absolute():
            screenshot_path = Path.cwd() / "screenshots" / screenshot_path

        # Ensure directory exists
        screenshot_path.parent.mkdir(parents=True, exist_ok=True)

        success = None
        if success:
            logger.info(f"Screenshot saved: {screenshot_path}")
        else:
            logger.error(f"Failed to save screenshot: {screenshot_path}")

        return screenshot_path

    def xǁBasePageǁtake_screenshot__mutmut_23(
        self, filename: str | Path | None = None
    ) -> Path:
        """
        Take a screenshot of the current page.

        Args:
            filename: Optional filename, defaults to timestamp-based name

        Returns:
            Path to the saved screenshot
        """
        if filename is None:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"

        screenshot_path = Path(filename)
        if not screenshot_path.is_absolute():
            screenshot_path = Path.cwd() / "screenshots" / screenshot_path

        # Ensure directory exists
        screenshot_path.parent.mkdir(parents=True, exist_ok=True)

        success = self.driver.get_screenshot_as_file(None)
        if success:
            logger.info(f"Screenshot saved: {screenshot_path}")
        else:
            logger.error(f"Failed to save screenshot: {screenshot_path}")

        return screenshot_path

    def xǁBasePageǁtake_screenshot__mutmut_24(
        self, filename: str | Path | None = None
    ) -> Path:
        """
        Take a screenshot of the current page.

        Args:
            filename: Optional filename, defaults to timestamp-based name

        Returns:
            Path to the saved screenshot
        """
        if filename is None:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"

        screenshot_path = Path(filename)
        if not screenshot_path.is_absolute():
            screenshot_path = Path.cwd() / "screenshots" / screenshot_path

        # Ensure directory exists
        screenshot_path.parent.mkdir(parents=True, exist_ok=True)

        success = self.driver.get_screenshot_as_file(str(None))
        if success:
            logger.info(f"Screenshot saved: {screenshot_path}")
        else:
            logger.error(f"Failed to save screenshot: {screenshot_path}")

        return screenshot_path

    def xǁBasePageǁtake_screenshot__mutmut_25(
        self, filename: str | Path | None = None
    ) -> Path:
        """
        Take a screenshot of the current page.

        Args:
            filename: Optional filename, defaults to timestamp-based name

        Returns:
            Path to the saved screenshot
        """
        if filename is None:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"

        screenshot_path = Path(filename)
        if not screenshot_path.is_absolute():
            screenshot_path = Path.cwd() / "screenshots" / screenshot_path

        # Ensure directory exists
        screenshot_path.parent.mkdir(parents=True, exist_ok=True)

        success = self.driver.get_screenshot_as_file(str(screenshot_path))
        if success:
            logger.info(None)
        else:
            logger.error(f"Failed to save screenshot: {screenshot_path}")

        return screenshot_path

    def xǁBasePageǁtake_screenshot__mutmut_26(
        self, filename: str | Path | None = None
    ) -> Path:
        """
        Take a screenshot of the current page.

        Args:
            filename: Optional filename, defaults to timestamp-based name

        Returns:
            Path to the saved screenshot
        """
        if filename is None:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"

        screenshot_path = Path(filename)
        if not screenshot_path.is_absolute():
            screenshot_path = Path.cwd() / "screenshots" / screenshot_path

        # Ensure directory exists
        screenshot_path.parent.mkdir(parents=True, exist_ok=True)

        success = self.driver.get_screenshot_as_file(str(screenshot_path))
        if success:
            logger.info(f"Screenshot saved: {screenshot_path}")
        else:
            logger.error(None)

        return screenshot_path

    xǁBasePageǁtake_screenshot__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁBasePageǁtake_screenshot__mutmut_1": xǁBasePageǁtake_screenshot__mutmut_1,
        "xǁBasePageǁtake_screenshot__mutmut_2": xǁBasePageǁtake_screenshot__mutmut_2,
        "xǁBasePageǁtake_screenshot__mutmut_3": xǁBasePageǁtake_screenshot__mutmut_3,
        "xǁBasePageǁtake_screenshot__mutmut_4": xǁBasePageǁtake_screenshot__mutmut_4,
        "xǁBasePageǁtake_screenshot__mutmut_5": xǁBasePageǁtake_screenshot__mutmut_5,
        "xǁBasePageǁtake_screenshot__mutmut_6": xǁBasePageǁtake_screenshot__mutmut_6,
        "xǁBasePageǁtake_screenshot__mutmut_7": xǁBasePageǁtake_screenshot__mutmut_7,
        "xǁBasePageǁtake_screenshot__mutmut_8": xǁBasePageǁtake_screenshot__mutmut_8,
        "xǁBasePageǁtake_screenshot__mutmut_9": xǁBasePageǁtake_screenshot__mutmut_9,
        "xǁBasePageǁtake_screenshot__mutmut_10": xǁBasePageǁtake_screenshot__mutmut_10,
        "xǁBasePageǁtake_screenshot__mutmut_11": xǁBasePageǁtake_screenshot__mutmut_11,
        "xǁBasePageǁtake_screenshot__mutmut_12": xǁBasePageǁtake_screenshot__mutmut_12,
        "xǁBasePageǁtake_screenshot__mutmut_13": xǁBasePageǁtake_screenshot__mutmut_13,
        "xǁBasePageǁtake_screenshot__mutmut_14": xǁBasePageǁtake_screenshot__mutmut_14,
        "xǁBasePageǁtake_screenshot__mutmut_15": xǁBasePageǁtake_screenshot__mutmut_15,
        "xǁBasePageǁtake_screenshot__mutmut_16": xǁBasePageǁtake_screenshot__mutmut_16,
        "xǁBasePageǁtake_screenshot__mutmut_17": xǁBasePageǁtake_screenshot__mutmut_17,
        "xǁBasePageǁtake_screenshot__mutmut_18": xǁBasePageǁtake_screenshot__mutmut_18,
        "xǁBasePageǁtake_screenshot__mutmut_19": xǁBasePageǁtake_screenshot__mutmut_19,
        "xǁBasePageǁtake_screenshot__mutmut_20": xǁBasePageǁtake_screenshot__mutmut_20,
        "xǁBasePageǁtake_screenshot__mutmut_21": xǁBasePageǁtake_screenshot__mutmut_21,
        "xǁBasePageǁtake_screenshot__mutmut_22": xǁBasePageǁtake_screenshot__mutmut_22,
        "xǁBasePageǁtake_screenshot__mutmut_23": xǁBasePageǁtake_screenshot__mutmut_23,
        "xǁBasePageǁtake_screenshot__mutmut_24": xǁBasePageǁtake_screenshot__mutmut_24,
        "xǁBasePageǁtake_screenshot__mutmut_25": xǁBasePageǁtake_screenshot__mutmut_25,
        "xǁBasePageǁtake_screenshot__mutmut_26": xǁBasePageǁtake_screenshot__mutmut_26,
    }

    def take_screenshot(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁBasePageǁtake_screenshot__mutmut_orig"),
            object.__getattribute__(self, "xǁBasePageǁtake_screenshot__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    take_screenshot.__signature__ = _mutmut_signature(
        xǁBasePageǁtake_screenshot__mutmut_orig
    )
    xǁBasePageǁtake_screenshot__mutmut_orig.__name__ = "xǁBasePageǁtake_screenshot"

    def xǁBasePageǁhandle_alert__mutmut_orig(
        self, accept: bool = True, timeout: float = 5.0
    ) -> str | None:
        """
        Handle JavaScript alerts.

        Args:
            accept: Whether to accept (True) or dismiss (False) the alert
            timeout: How long to wait for alert to appear

        Returns:
            Alert text if alert was present, None otherwise
        """
        try:
            wait = WebDriverWait(self.driver, timeout)
            alert = wait.until(EC.alert_is_present())
            alert_text = alert.text

            if accept:
                alert.accept()
                logger.debug(f"Accepted alert: {alert_text}")
            else:
                alert.dismiss()
                logger.debug(f"Dismissed alert: {alert_text}")

            return alert_text
        except TimeoutException:
            return None

    def xǁBasePageǁhandle_alert__mutmut_1(
        self, accept: bool = False, timeout: float = 5.0
    ) -> str | None:
        """
        Handle JavaScript alerts.

        Args:
            accept: Whether to accept (True) or dismiss (False) the alert
            timeout: How long to wait for alert to appear

        Returns:
            Alert text if alert was present, None otherwise
        """
        try:
            wait = WebDriverWait(self.driver, timeout)
            alert = wait.until(EC.alert_is_present())
            alert_text = alert.text

            if accept:
                alert.accept()
                logger.debug(f"Accepted alert: {alert_text}")
            else:
                alert.dismiss()
                logger.debug(f"Dismissed alert: {alert_text}")

            return alert_text
        except TimeoutException:
            return None

    def xǁBasePageǁhandle_alert__mutmut_2(
        self, accept: bool = True, timeout: float = 6.0
    ) -> str | None:
        """
        Handle JavaScript alerts.

        Args:
            accept: Whether to accept (True) or dismiss (False) the alert
            timeout: How long to wait for alert to appear

        Returns:
            Alert text if alert was present, None otherwise
        """
        try:
            wait = WebDriverWait(self.driver, timeout)
            alert = wait.until(EC.alert_is_present())
            alert_text = alert.text

            if accept:
                alert.accept()
                logger.debug(f"Accepted alert: {alert_text}")
            else:
                alert.dismiss()
                logger.debug(f"Dismissed alert: {alert_text}")

            return alert_text
        except TimeoutException:
            return None

    def xǁBasePageǁhandle_alert__mutmut_3(
        self, accept: bool = True, timeout: float = 5.0
    ) -> str | None:
        """
        Handle JavaScript alerts.

        Args:
            accept: Whether to accept (True) or dismiss (False) the alert
            timeout: How long to wait for alert to appear

        Returns:
            Alert text if alert was present, None otherwise
        """
        try:
            wait = None
            alert = wait.until(EC.alert_is_present())
            alert_text = alert.text

            if accept:
                alert.accept()
                logger.debug(f"Accepted alert: {alert_text}")
            else:
                alert.dismiss()
                logger.debug(f"Dismissed alert: {alert_text}")

            return alert_text
        except TimeoutException:
            return None

    def xǁBasePageǁhandle_alert__mutmut_4(
        self, accept: bool = True, timeout: float = 5.0
    ) -> str | None:
        """
        Handle JavaScript alerts.

        Args:
            accept: Whether to accept (True) or dismiss (False) the alert
            timeout: How long to wait for alert to appear

        Returns:
            Alert text if alert was present, None otherwise
        """
        try:
            wait = WebDriverWait(None, timeout)
            alert = wait.until(EC.alert_is_present())
            alert_text = alert.text

            if accept:
                alert.accept()
                logger.debug(f"Accepted alert: {alert_text}")
            else:
                alert.dismiss()
                logger.debug(f"Dismissed alert: {alert_text}")

            return alert_text
        except TimeoutException:
            return None

    def xǁBasePageǁhandle_alert__mutmut_5(
        self, accept: bool = True, timeout: float = 5.0
    ) -> str | None:
        """
        Handle JavaScript alerts.

        Args:
            accept: Whether to accept (True) or dismiss (False) the alert
            timeout: How long to wait for alert to appear

        Returns:
            Alert text if alert was present, None otherwise
        """
        try:
            wait = WebDriverWait(self.driver, None)
            alert = wait.until(EC.alert_is_present())
            alert_text = alert.text

            if accept:
                alert.accept()
                logger.debug(f"Accepted alert: {alert_text}")
            else:
                alert.dismiss()
                logger.debug(f"Dismissed alert: {alert_text}")

            return alert_text
        except TimeoutException:
            return None

    def xǁBasePageǁhandle_alert__mutmut_6(
        self, accept: bool = True, timeout: float = 5.0
    ) -> str | None:
        """
        Handle JavaScript alerts.

        Args:
            accept: Whether to accept (True) or dismiss (False) the alert
            timeout: How long to wait for alert to appear

        Returns:
            Alert text if alert was present, None otherwise
        """
        try:
            wait = WebDriverWait(timeout)
            alert = wait.until(EC.alert_is_present())
            alert_text = alert.text

            if accept:
                alert.accept()
                logger.debug(f"Accepted alert: {alert_text}")
            else:
                alert.dismiss()
                logger.debug(f"Dismissed alert: {alert_text}")

            return alert_text
        except TimeoutException:
            return None

    def xǁBasePageǁhandle_alert__mutmut_7(
        self, accept: bool = True, timeout: float = 5.0
    ) -> str | None:
        """
        Handle JavaScript alerts.

        Args:
            accept: Whether to accept (True) or dismiss (False) the alert
            timeout: How long to wait for alert to appear

        Returns:
            Alert text if alert was present, None otherwise
        """
        try:
            wait = WebDriverWait(
                self.driver,
            )
            alert = wait.until(EC.alert_is_present())
            alert_text = alert.text

            if accept:
                alert.accept()
                logger.debug(f"Accepted alert: {alert_text}")
            else:
                alert.dismiss()
                logger.debug(f"Dismissed alert: {alert_text}")

            return alert_text
        except TimeoutException:
            return None

    def xǁBasePageǁhandle_alert__mutmut_8(
        self, accept: bool = True, timeout: float = 5.0
    ) -> str | None:
        """
        Handle JavaScript alerts.

        Args:
            accept: Whether to accept (True) or dismiss (False) the alert
            timeout: How long to wait for alert to appear

        Returns:
            Alert text if alert was present, None otherwise
        """
        try:
            _wait = WebDriverWait(self.driver, timeout)
            alert = None
            alert_text = alert.text

            if accept:
                alert.accept()
                logger.debug(f"Accepted alert: {alert_text}")
            else:
                alert.dismiss()
                logger.debug(f"Dismissed alert: {alert_text}")

            return alert_text
        except TimeoutException:
            return None

    def xǁBasePageǁhandle_alert__mutmut_9(
        self, accept: bool = True, timeout: float = 5.0
    ) -> str | None:
        """
        Handle JavaScript alerts.

        Args:
            accept: Whether to accept (True) or dismiss (False) the alert
            timeout: How long to wait for alert to appear

        Returns:
            Alert text if alert was present, None otherwise
        """
        try:
            wait = WebDriverWait(self.driver, timeout)
            alert = wait.until(None)
            alert_text = alert.text

            if accept:
                alert.accept()
                logger.debug(f"Accepted alert: {alert_text}")
            else:
                alert.dismiss()
                logger.debug(f"Dismissed alert: {alert_text}")

            return alert_text
        except TimeoutException:
            return None

    def xǁBasePageǁhandle_alert__mutmut_10(
        self, accept: bool = True, timeout: float = 5.0
    ) -> str | None:
        """
        Handle JavaScript alerts.

        Args:
            accept: Whether to accept (True) or dismiss (False) the alert
            timeout: How long to wait for alert to appear

        Returns:
            Alert text if alert was present, None otherwise
        """
        try:
            wait = WebDriverWait(self.driver, timeout)
            alert = wait.until(EC.alert_is_present())
            alert_text = None

            if accept:
                alert.accept()
                logger.debug(f"Accepted alert: {alert_text}")
            else:
                alert.dismiss()
                logger.debug(f"Dismissed alert: {alert_text}")

            return alert_text
        except TimeoutException:
            return None

    def xǁBasePageǁhandle_alert__mutmut_11(
        self, accept: bool = True, timeout: float = 5.0
    ) -> str | None:
        """
        Handle JavaScript alerts.

        Args:
            accept: Whether to accept (True) or dismiss (False) the alert
            timeout: How long to wait for alert to appear

        Returns:
            Alert text if alert was present, None otherwise
        """
        try:
            wait = WebDriverWait(self.driver, timeout)
            alert = wait.until(EC.alert_is_present())
            alert_text = alert.text

            if accept:
                alert.accept()
                logger.debug(None)
            else:
                alert.dismiss()
                logger.debug(f"Dismissed alert: {alert_text}")

            return alert_text
        except TimeoutException:
            return None

    def xǁBasePageǁhandle_alert__mutmut_12(
        self, accept: bool = True, timeout: float = 5.0
    ) -> str | None:
        """
        Handle JavaScript alerts.

        Args:
            accept: Whether to accept (True) or dismiss (False) the alert
            timeout: How long to wait for alert to appear

        Returns:
            Alert text if alert was present, None otherwise
        """
        try:
            wait = WebDriverWait(self.driver, timeout)
            alert = wait.until(EC.alert_is_present())
            alert_text = alert.text

            if accept:
                alert.accept()
                logger.debug(f"Accepted alert: {alert_text}")
            else:
                alert.dismiss()
                logger.debug(None)

            return alert_text
        except TimeoutException:
            return None

    xǁBasePageǁhandle_alert__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁBasePageǁhandle_alert__mutmut_1": xǁBasePageǁhandle_alert__mutmut_1,
        "xǁBasePageǁhandle_alert__mutmut_2": xǁBasePageǁhandle_alert__mutmut_2,
        "xǁBasePageǁhandle_alert__mutmut_3": xǁBasePageǁhandle_alert__mutmut_3,
        "xǁBasePageǁhandle_alert__mutmut_4": xǁBasePageǁhandle_alert__mutmut_4,
        "xǁBasePageǁhandle_alert__mutmut_5": xǁBasePageǁhandle_alert__mutmut_5,
        "xǁBasePageǁhandle_alert__mutmut_6": xǁBasePageǁhandle_alert__mutmut_6,
        "xǁBasePageǁhandle_alert__mutmut_7": xǁBasePageǁhandle_alert__mutmut_7,
        "xǁBasePageǁhandle_alert__mutmut_8": xǁBasePageǁhandle_alert__mutmut_8,
        "xǁBasePageǁhandle_alert__mutmut_9": xǁBasePageǁhandle_alert__mutmut_9,
        "xǁBasePageǁhandle_alert__mutmut_10": xǁBasePageǁhandle_alert__mutmut_10,
        "xǁBasePageǁhandle_alert__mutmut_11": xǁBasePageǁhandle_alert__mutmut_11,
        "xǁBasePageǁhandle_alert__mutmut_12": xǁBasePageǁhandle_alert__mutmut_12,
    }

    def handle_alert(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁBasePageǁhandle_alert__mutmut_orig"),
            object.__getattribute__(self, "xǁBasePageǁhandle_alert__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    handle_alert.__signature__ = _mutmut_signature(xǁBasePageǁhandle_alert__mutmut_orig)
    xǁBasePageǁhandle_alert__mutmut_orig.__name__ = "xǁBasePageǁhandle_alert"

    def xǁBasePageǁswitch_to_window__mutmut_orig(
        self, window_handle: str
    ) -> "BasePage":
        """Switch to a specific browser window."""
        self.driver.switch_to.window(window_handle)
        logger.debug(f"Switched to window: {window_handle}")
        return self

    def xǁBasePageǁswitch_to_window__mutmut_1(self, window_handle: str) -> "BasePage":
        """Switch to a specific browser window."""
        self.driver.switch_to.window(None)
        logger.debug(f"Switched to window: {window_handle}")
        return self

    def xǁBasePageǁswitch_to_window__mutmut_2(self, window_handle: str) -> "BasePage":
        """Switch to a specific browser window."""
        self.driver.switch_to.window(window_handle)
        logger.debug(None)
        return self

    xǁBasePageǁswitch_to_window__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁBasePageǁswitch_to_window__mutmut_1": xǁBasePageǁswitch_to_window__mutmut_1,
        "xǁBasePageǁswitch_to_window__mutmut_2": xǁBasePageǁswitch_to_window__mutmut_2,
    }

    def switch_to_window(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁBasePageǁswitch_to_window__mutmut_orig"),
            object.__getattribute__(
                self, "xǁBasePageǁswitch_to_window__mutmut_mutants"
            ),
            args,
            kwargs,
            self,
        )
        return result

    switch_to_window.__signature__ = _mutmut_signature(
        xǁBasePageǁswitch_to_window__mutmut_orig
    )
    xǁBasePageǁswitch_to_window__mutmut_orig.__name__ = "xǁBasePageǁswitch_to_window"

    def xǁBasePageǁswitch_to_new_window__mutmut_orig(self) -> "BasePage":
        """Switch to the most recently opened window."""
        all_windows = self.driver.window_handles
        if len(all_windows) > 1:
            self.driver.switch_to.window(all_windows[-1])
            logger.debug("Switched to new window")
        return self

    def xǁBasePageǁswitch_to_new_window__mutmut_1(self) -> "BasePage":
        """Switch to the most recently opened window."""
        all_windows = None
        if len(all_windows) > 1:
            self.driver.switch_to.window(all_windows[-1])
            logger.debug("Switched to new window")
        return self

    def xǁBasePageǁswitch_to_new_window__mutmut_2(self) -> "BasePage":
        """Switch to the most recently opened window."""
        all_windows = self.driver.window_handles
        if len(all_windows) >= 1:
            self.driver.switch_to.window(all_windows[-1])
            logger.debug("Switched to new window")
        return self

    def xǁBasePageǁswitch_to_new_window__mutmut_3(self) -> "BasePage":
        """Switch to the most recently opened window."""
        all_windows = self.driver.window_handles
        if len(all_windows) > 2:
            self.driver.switch_to.window(all_windows[-1])
            logger.debug("Switched to new window")
        return self

    def xǁBasePageǁswitch_to_new_window__mutmut_4(self) -> "BasePage":
        """Switch to the most recently opened window."""
        all_windows = self.driver.window_handles
        if len(all_windows) > 1:
            self.driver.switch_to.window(None)
            logger.debug("Switched to new window")
        return self

    def xǁBasePageǁswitch_to_new_window__mutmut_5(self) -> "BasePage":
        """Switch to the most recently opened window."""
        all_windows = self.driver.window_handles
        if len(all_windows) > 1:
            self.driver.switch_to.window(all_windows[+1])
            logger.debug("Switched to new window")
        return self

    def xǁBasePageǁswitch_to_new_window__mutmut_6(self) -> "BasePage":
        """Switch to the most recently opened window."""
        all_windows = self.driver.window_handles
        if len(all_windows) > 1:
            self.driver.switch_to.window(all_windows[-2])
            logger.debug("Switched to new window")
        return self

    def xǁBasePageǁswitch_to_new_window__mutmut_7(self) -> "BasePage":
        """Switch to the most recently opened window."""
        all_windows = self.driver.window_handles
        if len(all_windows) > 1:
            self.driver.switch_to.window(all_windows[-1])
            logger.debug(None)
        return self

    def xǁBasePageǁswitch_to_new_window__mutmut_8(self) -> "BasePage":
        """Switch to the most recently opened window."""
        all_windows = self.driver.window_handles
        if len(all_windows) > 1:
            self.driver.switch_to.window(all_windows[-1])
            logger.debug("XXSwitched to new windowXX")
        return self

    def xǁBasePageǁswitch_to_new_window__mutmut_9(self) -> "BasePage":
        """Switch to the most recently opened window."""
        all_windows = self.driver.window_handles
        if len(all_windows) > 1:
            self.driver.switch_to.window(all_windows[-1])
            logger.debug("switched to new window")
        return self

    def xǁBasePageǁswitch_to_new_window__mutmut_10(self) -> "BasePage":
        """Switch to the most recently opened window."""
        all_windows = self.driver.window_handles
        if len(all_windows) > 1:
            self.driver.switch_to.window(all_windows[-1])
            logger.debug("SWITCHED TO NEW WINDOW")
        return self

    xǁBasePageǁswitch_to_new_window__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁBasePageǁswitch_to_new_window__mutmut_1": (
            xǁBasePageǁswitch_to_new_window__mutmut_1
        ),
        "xǁBasePageǁswitch_to_new_window__mutmut_2": (
            xǁBasePageǁswitch_to_new_window__mutmut_2
        ),
        "xǁBasePageǁswitch_to_new_window__mutmut_3": (
            xǁBasePageǁswitch_to_new_window__mutmut_3
        ),
        "xǁBasePageǁswitch_to_new_window__mutmut_4": (
            xǁBasePageǁswitch_to_new_window__mutmut_4
        ),
        "xǁBasePageǁswitch_to_new_window__mutmut_5": (
            xǁBasePageǁswitch_to_new_window__mutmut_5
        ),
        "xǁBasePageǁswitch_to_new_window__mutmut_6": (
            xǁBasePageǁswitch_to_new_window__mutmut_6
        ),
        "xǁBasePageǁswitch_to_new_window__mutmut_7": (
            xǁBasePageǁswitch_to_new_window__mutmut_7
        ),
        "xǁBasePageǁswitch_to_new_window__mutmut_8": (
            xǁBasePageǁswitch_to_new_window__mutmut_8
        ),
        "xǁBasePageǁswitch_to_new_window__mutmut_9": (
            xǁBasePageǁswitch_to_new_window__mutmut_9
        ),
        "xǁBasePageǁswitch_to_new_window__mutmut_10": (
            xǁBasePageǁswitch_to_new_window__mutmut_10
        ),
    }

    def switch_to_new_window(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(
                self, "xǁBasePageǁswitch_to_new_window__mutmut_orig"
            ),
            object.__getattribute__(
                self, "xǁBasePageǁswitch_to_new_window__mutmut_mutants"
            ),
            args,
            kwargs,
            self,
        )
        return result

    switch_to_new_window.__signature__ = _mutmut_signature(
        xǁBasePageǁswitch_to_new_window__mutmut_orig
    )
    xǁBasePageǁswitch_to_new_window__mutmut_orig.__name__ = (
        "xǁBasePageǁswitch_to_new_window"
    )

    def xǁBasePageǁclose_current_window__mutmut_orig(self) -> "BasePage":
        """Close the current window and switch to the previous one."""
        all_windows = self.driver.window_handles
        if len(all_windows) > 1:
            self.driver.close()
            self.driver.switch_to.window(all_windows[-2])
            logger.debug("Closed current window")
        return self

    def xǁBasePageǁclose_current_window__mutmut_1(self) -> "BasePage":
        """Close the current window and switch to the previous one."""
        all_windows = None
        if len(all_windows) > 1:
            self.driver.close()
            self.driver.switch_to.window(all_windows[-2])
            logger.debug("Closed current window")
        return self

    def xǁBasePageǁclose_current_window__mutmut_2(self) -> "BasePage":
        """Close the current window and switch to the previous one."""
        all_windows = self.driver.window_handles
        if len(all_windows) >= 1:
            self.driver.close()
            self.driver.switch_to.window(all_windows[-2])
            logger.debug("Closed current window")
        return self

    def xǁBasePageǁclose_current_window__mutmut_3(self) -> "BasePage":
        """Close the current window and switch to the previous one."""
        all_windows = self.driver.window_handles
        if len(all_windows) > 2:
            self.driver.close()
            self.driver.switch_to.window(all_windows[-2])
            logger.debug("Closed current window")
        return self

    def xǁBasePageǁclose_current_window__mutmut_4(self) -> "BasePage":
        """Close the current window and switch to the previous one."""
        all_windows = self.driver.window_handles
        if len(all_windows) > 1:
            self.driver.close()
            self.driver.switch_to.window(None)
            logger.debug("Closed current window")
        return self

    def xǁBasePageǁclose_current_window__mutmut_5(self) -> "BasePage":
        """Close the current window and switch to the previous one."""
        all_windows = self.driver.window_handles
        if len(all_windows) > 1:
            self.driver.close()
            self.driver.switch_to.window(all_windows[+2])
            logger.debug("Closed current window")
        return self

    def xǁBasePageǁclose_current_window__mutmut_6(self) -> "BasePage":
        """Close the current window and switch to the previous one."""
        all_windows = self.driver.window_handles
        if len(all_windows) > 1:
            self.driver.close()
            self.driver.switch_to.window(all_windows[-3])
            logger.debug("Closed current window")
        return self

    def xǁBasePageǁclose_current_window__mutmut_7(self) -> "BasePage":
        """Close the current window and switch to the previous one."""
        all_windows = self.driver.window_handles
        if len(all_windows) > 1:
            self.driver.close()
            self.driver.switch_to.window(all_windows[-2])
            logger.debug(None)
        return self

    def xǁBasePageǁclose_current_window__mutmut_8(self) -> "BasePage":
        """Close the current window and switch to the previous one."""
        all_windows = self.driver.window_handles
        if len(all_windows) > 1:
            self.driver.close()
            self.driver.switch_to.window(all_windows[-2])
            logger.debug("XXClosed current windowXX")
        return self

    def xǁBasePageǁclose_current_window__mutmut_9(self) -> "BasePage":
        """Close the current window and switch to the previous one."""
        all_windows = self.driver.window_handles
        if len(all_windows) > 1:
            self.driver.close()
            self.driver.switch_to.window(all_windows[-2])
            logger.debug("closed current window")
        return self

    def xǁBasePageǁclose_current_window__mutmut_10(self) -> "BasePage":
        """Close the current window and switch to the previous one."""
        all_windows = self.driver.window_handles
        if len(all_windows) > 1:
            self.driver.close()
            self.driver.switch_to.window(all_windows[-2])
            logger.debug("CLOSED CURRENT WINDOW")
        return self

    xǁBasePageǁclose_current_window__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁBasePageǁclose_current_window__mutmut_1": (
            xǁBasePageǁclose_current_window__mutmut_1
        ),
        "xǁBasePageǁclose_current_window__mutmut_2": (
            xǁBasePageǁclose_current_window__mutmut_2
        ),
        "xǁBasePageǁclose_current_window__mutmut_3": (
            xǁBasePageǁclose_current_window__mutmut_3
        ),
        "xǁBasePageǁclose_current_window__mutmut_4": (
            xǁBasePageǁclose_current_window__mutmut_4
        ),
        "xǁBasePageǁclose_current_window__mutmut_5": (
            xǁBasePageǁclose_current_window__mutmut_5
        ),
        "xǁBasePageǁclose_current_window__mutmut_6": (
            xǁBasePageǁclose_current_window__mutmut_6
        ),
        "xǁBasePageǁclose_current_window__mutmut_7": (
            xǁBasePageǁclose_current_window__mutmut_7
        ),
        "xǁBasePageǁclose_current_window__mutmut_8": (
            xǁBasePageǁclose_current_window__mutmut_8
        ),
        "xǁBasePageǁclose_current_window__mutmut_9": (
            xǁBasePageǁclose_current_window__mutmut_9
        ),
        "xǁBasePageǁclose_current_window__mutmut_10": (
            xǁBasePageǁclose_current_window__mutmut_10
        ),
    }

    def close_current_window(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(
                self, "xǁBasePageǁclose_current_window__mutmut_orig"
            ),
            object.__getattribute__(
                self, "xǁBasePageǁclose_current_window__mutmut_mutants"
            ),
            args,
            kwargs,
            self,
        )
        return result

    close_current_window.__signature__ = _mutmut_signature(
        xǁBasePageǁclose_current_window__mutmut_orig
    )
    xǁBasePageǁclose_current_window__mutmut_orig.__name__ = (
        "xǁBasePageǁclose_current_window"
    )

    @abstractmethod
    def verify_page_loaded(self) -> bool:
        """
        Verify that the page has loaded correctly.
        Subclasses should implement this method to check page-specific elements.
        """
        pass

    def __str__(self) -> str:
        """String representation of the page."""
        return f"{self.__class__.__name__}(url={self.url}, title={self.title})"
