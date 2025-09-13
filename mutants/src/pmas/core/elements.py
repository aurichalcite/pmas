"""
Base abstractions for web elements with common interaction patterns.
"""

import logging
import time
from abc import ABC
from typing import Any

from selenium.common.exceptions import (
    ElementNotInteractableException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from .errors import ElementNotFoundError, ElementNotInteractableError
from .locators import Locator

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


class BaseElement(ABC):
    """
    Abstract base class for all web element wrappers.
    Provides common functionality for element interaction with robust error handling.
    """

    def xǁBaseElementǁ__init____mutmut_orig(
        self, driver, locator: Locator, timeout: float = 10.0
    ) -> None:
        self.driver = driver
        self.locator = locator
        self.timeout = timeout
        self._element: WebElement | None = None

    def xǁBaseElementǁ__init____mutmut_1(
        self, driver, locator: Locator, timeout: float = 11.0
    ) -> None:
        self.driver = driver
        self.locator = locator
        self.timeout = timeout
        self._element: WebElement | None = None

    def xǁBaseElementǁ__init____mutmut_2(
        self, driver, locator: Locator, timeout: float = 10.0
    ) -> None:
        self.driver = None
        self.locator = locator
        self.timeout = timeout
        self._element: WebElement | None = None

    def xǁBaseElementǁ__init____mutmut_3(
        self, driver, locator: Locator, timeout: float = 10.0
    ) -> None:
        self.driver = driver
        self.locator = None
        self.timeout = timeout
        self._element: WebElement | None = None

    def xǁBaseElementǁ__init____mutmut_4(
        self, driver, locator: Locator, timeout: float = 10.0
    ) -> None:
        self.driver = driver
        self.locator = locator
        self.timeout = None
        self._element: WebElement | None = None

    def xǁBaseElementǁ__init____mutmut_5(
        self, driver, locator: Locator, timeout: float = 10.0
    ) -> None:
        self.driver = driver
        self.locator = locator
        self.timeout = timeout
        self._element: WebElement | None = ""

    xǁBaseElementǁ__init____mutmut_mutants: ClassVar[MutantDict] = {
        "xǁBaseElementǁ__init____mutmut_1": xǁBaseElementǁ__init____mutmut_1,
        "xǁBaseElementǁ__init____mutmut_2": xǁBaseElementǁ__init____mutmut_2,
        "xǁBaseElementǁ__init____mutmut_3": xǁBaseElementǁ__init____mutmut_3,
        "xǁBaseElementǁ__init____mutmut_4": xǁBaseElementǁ__init____mutmut_4,
        "xǁBaseElementǁ__init____mutmut_5": xǁBaseElementǁ__init____mutmut_5,
    }

    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁBaseElementǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁBaseElementǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    __init__.__signature__ = _mutmut_signature(xǁBaseElementǁ__init____mutmut_orig)
    xǁBaseElementǁ__init____mutmut_orig.__name__ = "xǁBaseElementǁ__init__"

    @property
    def element(self) -> WebElement:
        """Get the underlying WebElement, finding it if necessary."""
        if self._element is None or self._is_stale():
            self._element = self._find_element()
        return self._element

    def xǁBaseElementǁ_find_element__mutmut_orig(self) -> WebElement:
        """Find the element using the locator."""
        try:
            wait = WebDriverWait(self.driver, self.timeout)
            by, value = self.locator.selenium_locator
            element = wait.until(EC.presence_of_element_located((by, value)))
            logger.debug(f"Found element: {self.locator}")
            return element
        except TimeoutException as e:
            raise ElementNotFoundError(str(self.locator), self.timeout) from e

    def xǁBaseElementǁ_find_element__mutmut_1(self) -> WebElement:
        """Find the element using the locator."""
        try:
            wait = None
            by, value = self.locator.selenium_locator
            element = wait.until(EC.presence_of_element_located((by, value)))
            logger.debug(f"Found element: {self.locator}")
            return element
        except TimeoutException as e:
            raise ElementNotFoundError(str(self.locator), self.timeout) from e

    def xǁBaseElementǁ_find_element__mutmut_2(self) -> WebElement:
        """Find the element using the locator."""
        try:
            wait = WebDriverWait(None, self.timeout)
            by, value = self.locator.selenium_locator
            element = wait.until(EC.presence_of_element_located((by, value)))
            logger.debug(f"Found element: {self.locator}")
            return element
        except TimeoutException as e:
            raise ElementNotFoundError(str(self.locator), self.timeout) from e

    def xǁBaseElementǁ_find_element__mutmut_3(self) -> WebElement:
        """Find the element using the locator."""
        try:
            wait = WebDriverWait(self.driver, None)
            by, value = self.locator.selenium_locator
            element = wait.until(EC.presence_of_element_located((by, value)))
            logger.debug(f"Found element: {self.locator}")
            return element
        except TimeoutException as e:
            raise ElementNotFoundError(str(self.locator), self.timeout) from e

    def xǁBaseElementǁ_find_element__mutmut_4(self) -> WebElement:
        """Find the element using the locator."""
        try:
            wait = WebDriverWait(self.timeout)
            by, value = self.locator.selenium_locator
            element = wait.until(EC.presence_of_element_located((by, value)))
            logger.debug(f"Found element: {self.locator}")
            return element
        except TimeoutException as e:
            raise ElementNotFoundError(str(self.locator), self.timeout) from e

    def xǁBaseElementǁ_find_element__mutmut_5(self) -> WebElement:
        """Find the element using the locator."""
        try:
            wait = WebDriverWait(
                self.driver,
            )
            by, value = self.locator.selenium_locator
            element = wait.until(EC.presence_of_element_located((by, value)))
            logger.debug(f"Found element: {self.locator}")
            return element
        except TimeoutException as e:
            raise ElementNotFoundError(str(self.locator), self.timeout) from e

    def xǁBaseElementǁ_find_element__mutmut_6(self) -> WebElement:
        """Find the element using the locator."""
        try:
            wait = WebDriverWait(self.driver, self.timeout)
            by, value = None
            element = wait.until(EC.presence_of_element_located((by, value)))
            logger.debug(f"Found element: {self.locator}")
            return element
        except TimeoutException as e:
            raise ElementNotFoundError(str(self.locator), self.timeout) from e

    def xǁBaseElementǁ_find_element__mutmut_7(self) -> WebElement:
        """Find the element using the locator."""
        try:
            wait = WebDriverWait(self.driver, self.timeout)
            by, value = self.locator.selenium_locator
            element = None
            logger.debug(f"Found element: {self.locator}")
            return element
        except TimeoutException as e:
            raise ElementNotFoundError(str(self.locator), self.timeout) from e

    def xǁBaseElementǁ_find_element__mutmut_8(self) -> WebElement:
        """Find the element using the locator."""
        try:
            wait = WebDriverWait(self.driver, self.timeout)
            by, value = self.locator.selenium_locator
            element = wait.until(None)
            logger.debug(f"Found element: {self.locator}")
            return element
        except TimeoutException as e:
            raise ElementNotFoundError(str(self.locator), self.timeout) from e

    def xǁBaseElementǁ_find_element__mutmut_9(self) -> WebElement:
        """Find the element using the locator."""
        try:
            wait = WebDriverWait(self.driver, self.timeout)
            by, value = self.locator.selenium_locator
            element = wait.until(EC.presence_of_element_located(None))
            logger.debug(f"Found element: {self.locator}")
            return element
        except TimeoutException as e:
            raise ElementNotFoundError(str(self.locator), self.timeout) from e

    def xǁBaseElementǁ_find_element__mutmut_10(self) -> WebElement:
        """Find the element using the locator."""
        try:
            wait = WebDriverWait(self.driver, self.timeout)
            by, value = self.locator.selenium_locator
            element = wait.until(EC.presence_of_element_located((by, value)))
            logger.debug(None)
            return element
        except TimeoutException as e:
            raise ElementNotFoundError(str(self.locator), self.timeout) from e

    def xǁBaseElementǁ_find_element__mutmut_11(self) -> WebElement:
        """Find the element using the locator."""
        try:
            wait = WebDriverWait(self.driver, self.timeout)
            by, value = self.locator.selenium_locator
            element = wait.until(EC.presence_of_element_located((by, value)))
            logger.debug(f"Found element: {self.locator}")
            return element
        except TimeoutException as e:
            raise ElementNotFoundError(None, self.timeout) from e

    def xǁBaseElementǁ_find_element__mutmut_12(self) -> WebElement:
        """Find the element using the locator."""
        try:
            wait = WebDriverWait(self.driver, self.timeout)
            by, value = self.locator.selenium_locator
            element = wait.until(EC.presence_of_element_located((by, value)))
            logger.debug(f"Found element: {self.locator}")
            return element
        except TimeoutException as e:
            raise ElementNotFoundError(str(self.locator), None) from e

    def xǁBaseElementǁ_find_element__mutmut_13(self) -> WebElement:
        """Find the element using the locator."""
        try:
            wait = WebDriverWait(self.driver, self.timeout)
            by, value = self.locator.selenium_locator
            element = wait.until(EC.presence_of_element_located((by, value)))
            logger.debug(f"Found element: {self.locator}")
            return element
        except TimeoutException as e:
            raise ElementNotFoundError(self.timeout) from e

    def xǁBaseElementǁ_find_element__mutmut_14(self) -> WebElement:
        """Find the element using the locator."""
        try:
            wait = WebDriverWait(self.driver, self.timeout)
            by, value = self.locator.selenium_locator
            element = wait.until(EC.presence_of_element_located((by, value)))
            logger.debug(f"Found element: {self.locator}")
            return element
        except TimeoutException as e:
            raise ElementNotFoundError(
                str(self.locator),
            ) from e

    def xǁBaseElementǁ_find_element__mutmut_15(self) -> WebElement:
        """Find the element using the locator."""
        try:
            wait = WebDriverWait(self.driver, self.timeout)
            by, value = self.locator.selenium_locator
            element = wait.until(EC.presence_of_element_located((by, value)))
            logger.debug(f"Found element: {self.locator}")
            return element
        except TimeoutException as e:
            raise ElementNotFoundError(str(None), self.timeout) from e

    xǁBaseElementǁ_find_element__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁBaseElementǁ_find_element__mutmut_1": xǁBaseElementǁ_find_element__mutmut_1,
        "xǁBaseElementǁ_find_element__mutmut_2": xǁBaseElementǁ_find_element__mutmut_2,
        "xǁBaseElementǁ_find_element__mutmut_3": xǁBaseElementǁ_find_element__mutmut_3,
        "xǁBaseElementǁ_find_element__mutmut_4": xǁBaseElementǁ_find_element__mutmut_4,
        "xǁBaseElementǁ_find_element__mutmut_5": xǁBaseElementǁ_find_element__mutmut_5,
        "xǁBaseElementǁ_find_element__mutmut_6": xǁBaseElementǁ_find_element__mutmut_6,
        "xǁBaseElementǁ_find_element__mutmut_7": xǁBaseElementǁ_find_element__mutmut_7,
        "xǁBaseElementǁ_find_element__mutmut_8": xǁBaseElementǁ_find_element__mutmut_8,
        "xǁBaseElementǁ_find_element__mutmut_9": xǁBaseElementǁ_find_element__mutmut_9,
        "xǁBaseElementǁ_find_element__mutmut_10": xǁBaseElementǁ_find_element__mutmut_10,
        "xǁBaseElementǁ_find_element__mutmut_11": xǁBaseElementǁ_find_element__mutmut_11,
        "xǁBaseElementǁ_find_element__mutmut_12": xǁBaseElementǁ_find_element__mutmut_12,
        "xǁBaseElementǁ_find_element__mutmut_13": xǁBaseElementǁ_find_element__mutmut_13,
        "xǁBaseElementǁ_find_element__mutmut_14": xǁBaseElementǁ_find_element__mutmut_14,
        "xǁBaseElementǁ_find_element__mutmut_15": xǁBaseElementǁ_find_element__mutmut_15,
    }

    def _find_element(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁBaseElementǁ_find_element__mutmut_orig"),
            object.__getattribute__(
                self, "xǁBaseElementǁ_find_element__mutmut_mutants"
            ),
            args,
            kwargs,
            self,
        )
        return result

    _find_element.__signature__ = _mutmut_signature(
        xǁBaseElementǁ_find_element__mutmut_orig
    )
    xǁBaseElementǁ_find_element__mutmut_orig.__name__ = "xǁBaseElementǁ_find_element"

    def xǁBaseElementǁ_is_stale__mutmut_orig(self) -> bool:
        """Check if the current element reference is stale."""
        if self._element is None:
            return False
        try:
            # Accessing any property will raise StaleElementReferenceException if stale
            _ = self._element.tag_name
            return False
        except StaleElementReferenceException:
            return True

    def xǁBaseElementǁ_is_stale__mutmut_1(self) -> bool:
        """Check if the current element reference is stale."""
        if self._element is not None:
            return False
        try:
            # Accessing any property will raise StaleElementReferenceException if stale
            _ = self._element.tag_name
            return False
        except StaleElementReferenceException:
            return True

    def xǁBaseElementǁ_is_stale__mutmut_2(self) -> bool:
        """Check if the current element reference is stale."""
        if self._element is None:
            return True
        try:
            # Accessing any property will raise StaleElementReferenceException if stale
            _ = self._element.tag_name
            return False
        except StaleElementReferenceException:
            return True

    def xǁBaseElementǁ_is_stale__mutmut_3(self) -> bool:
        """Check if the current element reference is stale."""
        if self._element is None:
            return False
        try:
            # Accessing any property will raise StaleElementReferenceException if stale
            _ = None
            return False
        except StaleElementReferenceException:
            return True

    def xǁBaseElementǁ_is_stale__mutmut_4(self) -> bool:
        """Check if the current element reference is stale."""
        if self._element is None:
            return False
        try:
            # Accessing any property will raise StaleElementReferenceException if stale
            _ = self._element.tag_name
            return True
        except StaleElementReferenceException:
            return True

    def xǁBaseElementǁ_is_stale__mutmut_5(self) -> bool:
        """Check if the current element reference is stale."""
        if self._element is None:
            return False
        try:
            # Accessing any property will raise StaleElementReferenceException if stale
            _ = self._element.tag_name
            return False
        except StaleElementReferenceException:
            return False

    xǁBaseElementǁ_is_stale__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁBaseElementǁ_is_stale__mutmut_1": xǁBaseElementǁ_is_stale__mutmut_1,
        "xǁBaseElementǁ_is_stale__mutmut_2": xǁBaseElementǁ_is_stale__mutmut_2,
        "xǁBaseElementǁ_is_stale__mutmut_3": xǁBaseElementǁ_is_stale__mutmut_3,
        "xǁBaseElementǁ_is_stale__mutmut_4": xǁBaseElementǁ_is_stale__mutmut_4,
        "xǁBaseElementǁ_is_stale__mutmut_5": xǁBaseElementǁ_is_stale__mutmut_5,
    }

    def _is_stale(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁBaseElementǁ_is_stale__mutmut_orig"),
            object.__getattribute__(self, "xǁBaseElementǁ_is_stale__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    _is_stale.__signature__ = _mutmut_signature(xǁBaseElementǁ_is_stale__mutmut_orig)
    xǁBaseElementǁ_is_stale__mutmut_orig.__name__ = "xǁBaseElementǁ_is_stale"

    def xǁBaseElementǁwait_for_visible__mutmut_orig(
        self, timeout: float | None = None
    ) -> "BaseElement":
        """Wait for the element to be visible."""
        timeout = timeout or self.timeout
        try:
            wait = WebDriverWait(self.driver, timeout)
            by, value = self.locator.selenium_locator
            wait.until(EC.visibility_of_element_located((by, value)))
            return self
        except TimeoutException as e:
            raise ElementNotFoundError(f"{self.locator} (visible)", timeout) from e

    def xǁBaseElementǁwait_for_visible__mutmut_1(
        self, timeout: float | None = None
    ) -> "BaseElement":
        """Wait for the element to be visible."""
        timeout = None
        try:
            wait = WebDriverWait(self.driver, timeout)
            by, value = self.locator.selenium_locator
            wait.until(EC.visibility_of_element_located((by, value)))
            return self
        except TimeoutException as e:
            raise ElementNotFoundError(f"{self.locator} (visible)", timeout) from e

    def xǁBaseElementǁwait_for_visible__mutmut_2(
        self, timeout: float | None = None
    ) -> "BaseElement":
        """Wait for the element to be visible."""
        timeout = timeout and self.timeout
        try:
            wait = WebDriverWait(self.driver, timeout)
            by, value = self.locator.selenium_locator
            wait.until(EC.visibility_of_element_located((by, value)))
            return self
        except TimeoutException as e:
            raise ElementNotFoundError(f"{self.locator} (visible)", timeout) from e

    def xǁBaseElementǁwait_for_visible__mutmut_3(
        self, timeout: float | None = None
    ) -> "BaseElement":
        """Wait for the element to be visible."""
        timeout = timeout or self.timeout
        try:
            wait = None
            by, value = self.locator.selenium_locator
            wait.until(EC.visibility_of_element_located((by, value)))
            return self
        except TimeoutException as e:
            raise ElementNotFoundError(f"{self.locator} (visible)", timeout) from e

    def xǁBaseElementǁwait_for_visible__mutmut_4(
        self, timeout: float | None = None
    ) -> "BaseElement":
        """Wait for the element to be visible."""
        timeout = timeout or self.timeout
        try:
            wait = WebDriverWait(None, timeout)
            by, value = self.locator.selenium_locator
            wait.until(EC.visibility_of_element_located((by, value)))
            return self
        except TimeoutException as e:
            raise ElementNotFoundError(f"{self.locator} (visible)", timeout) from e

    def xǁBaseElementǁwait_for_visible__mutmut_5(
        self, timeout: float | None = None
    ) -> "BaseElement":
        """Wait for the element to be visible."""
        timeout = timeout or self.timeout
        try:
            wait = WebDriverWait(self.driver, None)
            by, value = self.locator.selenium_locator
            wait.until(EC.visibility_of_element_located((by, value)))
            return self
        except TimeoutException as e:
            raise ElementNotFoundError(f"{self.locator} (visible)", timeout) from e

    def xǁBaseElementǁwait_for_visible__mutmut_6(
        self, timeout: float | None = None
    ) -> "BaseElement":
        """Wait for the element to be visible."""
        timeout = timeout or self.timeout
        try:
            wait = WebDriverWait(timeout)
            by, value = self.locator.selenium_locator
            wait.until(EC.visibility_of_element_located((by, value)))
            return self
        except TimeoutException as e:
            raise ElementNotFoundError(f"{self.locator} (visible)", timeout) from e

    def xǁBaseElementǁwait_for_visible__mutmut_7(
        self, timeout: float | None = None
    ) -> "BaseElement":
        """Wait for the element to be visible."""
        timeout = timeout or self.timeout
        try:
            wait = WebDriverWait(
                self.driver,
            )
            by, value = self.locator.selenium_locator
            wait.until(EC.visibility_of_element_located((by, value)))
            return self
        except TimeoutException as e:
            raise ElementNotFoundError(f"{self.locator} (visible)", timeout) from e

    def xǁBaseElementǁwait_for_visible__mutmut_8(
        self, timeout: float | None = None
    ) -> "BaseElement":
        """Wait for the element to be visible."""
        timeout = timeout or self.timeout
        try:
            wait = WebDriverWait(self.driver, timeout)
            by, value = None
            wait.until(EC.visibility_of_element_located((by, value)))
            return self
        except TimeoutException as e:
            raise ElementNotFoundError(f"{self.locator} (visible)", timeout) from e

    def xǁBaseElementǁwait_for_visible__mutmut_9(
        self, timeout: float | None = None
    ) -> "BaseElement":
        """Wait for the element to be visible."""
        timeout = timeout or self.timeout
        try:
            wait = WebDriverWait(self.driver, timeout)
            by, value = self.locator.selenium_locator
            wait.until(None)
            return self
        except TimeoutException as e:
            raise ElementNotFoundError(f"{self.locator} (visible)", timeout) from e

    def xǁBaseElementǁwait_for_visible__mutmut_10(
        self, timeout: float | None = None
    ) -> "BaseElement":
        """Wait for the element to be visible."""
        timeout = timeout or self.timeout
        try:
            wait = WebDriverWait(self.driver, timeout)
            by, value = self.locator.selenium_locator
            wait.until(EC.visibility_of_element_located(None))
            return self
        except TimeoutException as e:
            raise ElementNotFoundError(f"{self.locator} (visible)", timeout) from e

    def xǁBaseElementǁwait_for_visible__mutmut_11(
        self, timeout: float | None = None
    ) -> "BaseElement":
        """Wait for the element to be visible."""
        timeout = timeout or self.timeout
        try:
            wait = WebDriverWait(self.driver, timeout)
            by, value = self.locator.selenium_locator
            wait.until(EC.visibility_of_element_located((by, value)))
            return self
        except TimeoutException as e:
            raise ElementNotFoundError(None, timeout) from e

    def xǁBaseElementǁwait_for_visible__mutmut_12(
        self, timeout: float | None = None
    ) -> "BaseElement":
        """Wait for the element to be visible."""
        timeout = timeout or self.timeout
        try:
            wait = WebDriverWait(self.driver, timeout)
            by, value = self.locator.selenium_locator
            wait.until(EC.visibility_of_element_located((by, value)))
            return self
        except TimeoutException as e:
            raise ElementNotFoundError(f"{self.locator} (visible)", None) from e

    def xǁBaseElementǁwait_for_visible__mutmut_13(
        self, timeout: float | None = None
    ) -> "BaseElement":
        """Wait for the element to be visible."""
        timeout = timeout or self.timeout
        try:
            wait = WebDriverWait(self.driver, timeout)
            by, value = self.locator.selenium_locator
            wait.until(EC.visibility_of_element_located((by, value)))
            return self
        except TimeoutException as e:
            raise ElementNotFoundError(timeout) from e

    def xǁBaseElementǁwait_for_visible__mutmut_14(
        self, timeout: float | None = None
    ) -> "BaseElement":
        """Wait for the element to be visible."""
        timeout = timeout or self.timeout
        try:
            wait = WebDriverWait(self.driver, timeout)
            by, value = self.locator.selenium_locator
            wait.until(EC.visibility_of_element_located((by, value)))
            return self
        except TimeoutException as e:
            raise ElementNotFoundError(
                f"{self.locator} (visible)",
            ) from e

    xǁBaseElementǁwait_for_visible__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁBaseElementǁwait_for_visible__mutmut_1": xǁBaseElementǁwait_for_visible__mutmut_1,
        "xǁBaseElementǁwait_for_visible__mutmut_2": xǁBaseElementǁwait_for_visible__mutmut_2,
        "xǁBaseElementǁwait_for_visible__mutmut_3": xǁBaseElementǁwait_for_visible__mutmut_3,
        "xǁBaseElementǁwait_for_visible__mutmut_4": xǁBaseElementǁwait_for_visible__mutmut_4,
        "xǁBaseElementǁwait_for_visible__mutmut_5": xǁBaseElementǁwait_for_visible__mutmut_5,
        "xǁBaseElementǁwait_for_visible__mutmut_6": xǁBaseElementǁwait_for_visible__mutmut_6,
        "xǁBaseElementǁwait_for_visible__mutmut_7": xǁBaseElementǁwait_for_visible__mutmut_7,
        "xǁBaseElementǁwait_for_visible__mutmut_8": xǁBaseElementǁwait_for_visible__mutmut_8,
        "xǁBaseElementǁwait_for_visible__mutmut_9": xǁBaseElementǁwait_for_visible__mutmut_9,
        "xǁBaseElementǁwait_for_visible__mutmut_10": xǁBaseElementǁwait_for_visible__mutmut_10,
        "xǁBaseElementǁwait_for_visible__mutmut_11": xǁBaseElementǁwait_for_visible__mutmut_11,
        "xǁBaseElementǁwait_for_visible__mutmut_12": xǁBaseElementǁwait_for_visible__mutmut_12,
        "xǁBaseElementǁwait_for_visible__mutmut_13": xǁBaseElementǁwait_for_visible__mutmut_13,
        "xǁBaseElementǁwait_for_visible__mutmut_14": xǁBaseElementǁwait_for_visible__mutmut_14,
    }

    def wait_for_visible(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(
                self, "xǁBaseElementǁwait_for_visible__mutmut_orig"
            ),
            object.__getattribute__(
                self, "xǁBaseElementǁwait_for_visible__mutmut_mutants"
            ),
            args,
            kwargs,
            self,
        )
        return result

    wait_for_visible.__signature__ = _mutmut_signature(
        xǁBaseElementǁwait_for_visible__mutmut_orig
    )
    xǁBaseElementǁwait_for_visible__mutmut_orig.__name__ = (
        "xǁBaseElementǁwait_for_visible"
    )

    def xǁBaseElementǁwait_for_clickable__mutmut_orig(
        self, timeout: float | None = None
    ) -> "BaseElement":
        """Wait for the element to be clickable."""
        timeout = timeout or self.timeout
        try:
            wait = WebDriverWait(self.driver, timeout)
            by, value = self.locator.selenium_locator
            wait.until(EC.element_to_be_clickable((by, value)))
            return self
        except TimeoutException as e:
            raise ElementNotFoundError(f"{self.locator} (clickable)", timeout) from e

    def xǁBaseElementǁwait_for_clickable__mutmut_1(
        self, timeout: float | None = None
    ) -> "BaseElement":
        """Wait for the element to be clickable."""
        timeout = None
        try:
            wait = WebDriverWait(self.driver, timeout)
            by, value = self.locator.selenium_locator
            wait.until(EC.element_to_be_clickable((by, value)))
            return self
        except TimeoutException as e:
            raise ElementNotFoundError(f"{self.locator} (clickable)", timeout) from e

    def xǁBaseElementǁwait_for_clickable__mutmut_2(
        self, timeout: float | None = None
    ) -> "BaseElement":
        """Wait for the element to be clickable."""
        timeout = timeout and self.timeout
        try:
            wait = WebDriverWait(self.driver, timeout)
            by, value = self.locator.selenium_locator
            wait.until(EC.element_to_be_clickable((by, value)))
            return self
        except TimeoutException as e:
            raise ElementNotFoundError(f"{self.locator} (clickable)", timeout) from e

    def xǁBaseElementǁwait_for_clickable__mutmut_3(
        self, timeout: float | None = None
    ) -> "BaseElement":
        """Wait for the element to be clickable."""
        timeout = timeout or self.timeout
        try:
            wait = None
            by, value = self.locator.selenium_locator
            wait.until(EC.element_to_be_clickable((by, value)))
            return self
        except TimeoutException as e:
            raise ElementNotFoundError(f"{self.locator} (clickable)", timeout) from e

    def xǁBaseElementǁwait_for_clickable__mutmut_4(
        self, timeout: float | None = None
    ) -> "BaseElement":
        """Wait for the element to be clickable."""
        timeout = timeout or self.timeout
        try:
            wait = WebDriverWait(None, timeout)
            by, value = self.locator.selenium_locator
            wait.until(EC.element_to_be_clickable((by, value)))
            return self
        except TimeoutException as e:
            raise ElementNotFoundError(f"{self.locator} (clickable)", timeout) from e

    def xǁBaseElementǁwait_for_clickable__mutmut_5(
        self, timeout: float | None = None
    ) -> "BaseElement":
        """Wait for the element to be clickable."""
        timeout = timeout or self.timeout
        try:
            wait = WebDriverWait(self.driver, None)
            by, value = self.locator.selenium_locator
            wait.until(EC.element_to_be_clickable((by, value)))
            return self
        except TimeoutException as e:
            raise ElementNotFoundError(f"{self.locator} (clickable)", timeout) from e

    def xǁBaseElementǁwait_for_clickable__mutmut_6(
        self, timeout: float | None = None
    ) -> "BaseElement":
        """Wait for the element to be clickable."""
        timeout = timeout or self.timeout
        try:
            wait = WebDriverWait(timeout)
            by, value = self.locator.selenium_locator
            wait.until(EC.element_to_be_clickable((by, value)))
            return self
        except TimeoutException as e:
            raise ElementNotFoundError(f"{self.locator} (clickable)", timeout) from e

    def xǁBaseElementǁwait_for_clickable__mutmut_7(
        self, timeout: float | None = None
    ) -> "BaseElement":
        """Wait for the element to be clickable."""
        timeout = timeout or self.timeout
        try:
            wait = WebDriverWait(
                self.driver,
            )
            by, value = self.locator.selenium_locator
            wait.until(EC.element_to_be_clickable((by, value)))
            return self
        except TimeoutException as e:
            raise ElementNotFoundError(f"{self.locator} (clickable)", timeout) from e

    def xǁBaseElementǁwait_for_clickable__mutmut_8(
        self, timeout: float | None = None
    ) -> "BaseElement":
        """Wait for the element to be clickable."""
        timeout = timeout or self.timeout
        try:
            wait = WebDriverWait(self.driver, timeout)
            by, value = None
            wait.until(EC.element_to_be_clickable((by, value)))
            return self
        except TimeoutException as e:
            raise ElementNotFoundError(f"{self.locator} (clickable)", timeout) from e

    def xǁBaseElementǁwait_for_clickable__mutmut_9(
        self, timeout: float | None = None
    ) -> "BaseElement":
        """Wait for the element to be clickable."""
        timeout = timeout or self.timeout
        try:
            wait = WebDriverWait(self.driver, timeout)
            by, value = self.locator.selenium_locator
            wait.until(None)
            return self
        except TimeoutException as e:
            raise ElementNotFoundError(f"{self.locator} (clickable)", timeout) from e

    def xǁBaseElementǁwait_for_clickable__mutmut_10(
        self, timeout: float | None = None
    ) -> "BaseElement":
        """Wait for the element to be clickable."""
        timeout = timeout or self.timeout
        try:
            wait = WebDriverWait(self.driver, timeout)
            by, value = self.locator.selenium_locator
            wait.until(EC.element_to_be_clickable(None))
            return self
        except TimeoutException as e:
            raise ElementNotFoundError(f"{self.locator} (clickable)", timeout) from e

    def xǁBaseElementǁwait_for_clickable__mutmut_11(
        self, timeout: float | None = None
    ) -> "BaseElement":
        """Wait for the element to be clickable."""
        timeout = timeout or self.timeout
        try:
            wait = WebDriverWait(self.driver, timeout)
            by, value = self.locator.selenium_locator
            wait.until(EC.element_to_be_clickable((by, value)))
            return self
        except TimeoutException as e:
            raise ElementNotFoundError(None, timeout) from e

    def xǁBaseElementǁwait_for_clickable__mutmut_12(
        self, timeout: float | None = None
    ) -> "BaseElement":
        """Wait for the element to be clickable."""
        timeout = timeout or self.timeout
        try:
            wait = WebDriverWait(self.driver, timeout)
            by, value = self.locator.selenium_locator
            wait.until(EC.element_to_be_clickable((by, value)))
            return self
        except TimeoutException as e:
            raise ElementNotFoundError(f"{self.locator} (clickable)", None) from e

    def xǁBaseElementǁwait_for_clickable__mutmut_13(
        self, timeout: float | None = None
    ) -> "BaseElement":
        """Wait for the element to be clickable."""
        timeout = timeout or self.timeout
        try:
            wait = WebDriverWait(self.driver, timeout)
            by, value = self.locator.selenium_locator
            wait.until(EC.element_to_be_clickable((by, value)))
            return self
        except TimeoutException as e:
            raise ElementNotFoundError(timeout) from e

    def xǁBaseElementǁwait_for_clickable__mutmut_14(
        self, timeout: float | None = None
    ) -> "BaseElement":
        """Wait for the element to be clickable."""
        timeout = timeout or self.timeout
        try:
            wait = WebDriverWait(self.driver, timeout)
            by, value = self.locator.selenium_locator
            wait.until(EC.element_to_be_clickable((by, value)))
            return self
        except TimeoutException as e:
            raise ElementNotFoundError(
                f"{self.locator} (clickable)",
            ) from e

    xǁBaseElementǁwait_for_clickable__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁBaseElementǁwait_for_clickable__mutmut_1": xǁBaseElementǁwait_for_clickable__mutmut_1,
        "xǁBaseElementǁwait_for_clickable__mutmut_2": xǁBaseElementǁwait_for_clickable__mutmut_2,
        "xǁBaseElementǁwait_for_clickable__mutmut_3": xǁBaseElementǁwait_for_clickable__mutmut_3,
        "xǁBaseElementǁwait_for_clickable__mutmut_4": xǁBaseElementǁwait_for_clickable__mutmut_4,
        "xǁBaseElementǁwait_for_clickable__mutmut_5": xǁBaseElementǁwait_for_clickable__mutmut_5,
        "xǁBaseElementǁwait_for_clickable__mutmut_6": xǁBaseElementǁwait_for_clickable__mutmut_6,
        "xǁBaseElementǁwait_for_clickable__mutmut_7": xǁBaseElementǁwait_for_clickable__mutmut_7,
        "xǁBaseElementǁwait_for_clickable__mutmut_8": xǁBaseElementǁwait_for_clickable__mutmut_8,
        "xǁBaseElementǁwait_for_clickable__mutmut_9": xǁBaseElementǁwait_for_clickable__mutmut_9,
        "xǁBaseElementǁwait_for_clickable__mutmut_10": xǁBaseElementǁwait_for_clickable__mutmut_10,
        "xǁBaseElementǁwait_for_clickable__mutmut_11": xǁBaseElementǁwait_for_clickable__mutmut_11,
        "xǁBaseElementǁwait_for_clickable__mutmut_12": xǁBaseElementǁwait_for_clickable__mutmut_12,
        "xǁBaseElementǁwait_for_clickable__mutmut_13": xǁBaseElementǁwait_for_clickable__mutmut_13,
        "xǁBaseElementǁwait_for_clickable__mutmut_14": xǁBaseElementǁwait_for_clickable__mutmut_14,
    }

    def wait_for_clickable(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(
                self, "xǁBaseElementǁwait_for_clickable__mutmut_orig"
            ),
            object.__getattribute__(
                self, "xǁBaseElementǁwait_for_clickable__mutmut_mutants"
            ),
            args,
            kwargs,
            self,
        )
        return result

    wait_for_clickable.__signature__ = _mutmut_signature(
        xǁBaseElementǁwait_for_clickable__mutmut_orig
    )
    xǁBaseElementǁwait_for_clickable__mutmut_orig.__name__ = (
        "xǁBaseElementǁwait_for_clickable"
    )

    def xǁBaseElementǁscroll_into_view__mutmut_orig(self) -> "BaseElement":
        """Scroll the element into view."""
        self.driver.execute_script("arguments[0].scrollIntoView(true);", self.element)
        time.sleep(0.1)  # Small delay for scroll to complete
        return self

    def xǁBaseElementǁscroll_into_view__mutmut_1(self) -> "BaseElement":
        """Scroll the element into view."""
        self.driver.execute_script(None, self.element)
        time.sleep(0.1)  # Small delay for scroll to complete
        return self

    def xǁBaseElementǁscroll_into_view__mutmut_2(self) -> "BaseElement":
        """Scroll the element into view."""
        self.driver.execute_script("arguments[0].scrollIntoView(true);", None)
        time.sleep(0.1)  # Small delay for scroll to complete
        return self

    def xǁBaseElementǁscroll_into_view__mutmut_3(self) -> "BaseElement":
        """Scroll the element into view."""
        self.driver.execute_script(self.element)
        time.sleep(0.1)  # Small delay for scroll to complete
        return self

    def xǁBaseElementǁscroll_into_view__mutmut_4(self) -> "BaseElement":
        """Scroll the element into view."""
        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
        )
        time.sleep(0.1)  # Small delay for scroll to complete
        return self

    def xǁBaseElementǁscroll_into_view__mutmut_5(self) -> "BaseElement":
        """Scroll the element into view."""
        self.driver.execute_script(
            "XXarguments[0].scrollIntoView(true);XX", self.element
        )
        time.sleep(0.1)  # Small delay for scroll to complete
        return self

    def xǁBaseElementǁscroll_into_view__mutmut_6(self) -> "BaseElement":
        """Scroll the element into view."""
        self.driver.execute_script("arguments[0].scrollintoview(true);", self.element)
        time.sleep(0.1)  # Small delay for scroll to complete
        return self

    def xǁBaseElementǁscroll_into_view__mutmut_7(self) -> "BaseElement":
        """Scroll the element into view."""
        self.driver.execute_script("ARGUMENTS[0].SCROLLINTOVIEW(TRUE);", self.element)
        time.sleep(0.1)  # Small delay for scroll to complete
        return self

    def xǁBaseElementǁscroll_into_view__mutmut_8(self) -> "BaseElement":
        """Scroll the element into view."""
        self.driver.execute_script("arguments[0].scrollIntoView(true);", self.element)
        time.sleep(None)  # Small delay for scroll to complete
        return self

    def xǁBaseElementǁscroll_into_view__mutmut_9(self) -> "BaseElement":
        """Scroll the element into view."""
        self.driver.execute_script("arguments[0].scrollIntoView(true);", self.element)
        time.sleep(1.1)  # Small delay for scroll to complete
        return self

    xǁBaseElementǁscroll_into_view__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁBaseElementǁscroll_into_view__mutmut_1": xǁBaseElementǁscroll_into_view__mutmut_1,
        "xǁBaseElementǁscroll_into_view__mutmut_2": xǁBaseElementǁscroll_into_view__mutmut_2,
        "xǁBaseElementǁscroll_into_view__mutmut_3": xǁBaseElementǁscroll_into_view__mutmut_3,
        "xǁBaseElementǁscroll_into_view__mutmut_4": xǁBaseElementǁscroll_into_view__mutmut_4,
        "xǁBaseElementǁscroll_into_view__mutmut_5": xǁBaseElementǁscroll_into_view__mutmut_5,
        "xǁBaseElementǁscroll_into_view__mutmut_6": xǁBaseElementǁscroll_into_view__mutmut_6,
        "xǁBaseElementǁscroll_into_view__mutmut_7": xǁBaseElementǁscroll_into_view__mutmut_7,
        "xǁBaseElementǁscroll_into_view__mutmut_8": xǁBaseElementǁscroll_into_view__mutmut_8,
        "xǁBaseElementǁscroll_into_view__mutmut_9": xǁBaseElementǁscroll_into_view__mutmut_9,
    }

    def scroll_into_view(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(
                self, "xǁBaseElementǁscroll_into_view__mutmut_orig"
            ),
            object.__getattribute__(
                self, "xǁBaseElementǁscroll_into_view__mutmut_mutants"
            ),
            args,
            kwargs,
            self,
        )
        return result

    scroll_into_view.__signature__ = _mutmut_signature(
        xǁBaseElementǁscroll_into_view__mutmut_orig
    )
    xǁBaseElementǁscroll_into_view__mutmut_orig.__name__ = (
        "xǁBaseElementǁscroll_into_view"
    )

    def xǁBaseElementǁhighlight__mutmut_orig(
        self, duration: float = 1.0
    ) -> "BaseElement":
        """Highlight the element for debugging purposes."""
        original_style = self.element.get_attribute("style")
        self.driver.execute_script(
            "arguments[0].style.border='3px solid red';", self.element
        )
        time.sleep(duration)
        self.driver.execute_script(
            f"arguments[0].style.border='{original_style}';", self.element
        )
        return self

    def xǁBaseElementǁhighlight__mutmut_1(self, duration: float = 2.0) -> "BaseElement":
        """Highlight the element for debugging purposes."""
        original_style = self.element.get_attribute("style")
        self.driver.execute_script(
            "arguments[0].style.border='3px solid red';", self.element
        )
        time.sleep(duration)
        self.driver.execute_script(
            f"arguments[0].style.border='{original_style}';", self.element
        )
        return self

    def xǁBaseElementǁhighlight__mutmut_2(self, duration: float = 1.0) -> "BaseElement":
        """Highlight the element for debugging purposes."""
        original_style = None
        self.driver.execute_script(
            "arguments[0].style.border='3px solid red';", self.element
        )
        time.sleep(duration)
        self.driver.execute_script(
            f"arguments[0].style.border='{original_style}';", self.element
        )
        return self

    def xǁBaseElementǁhighlight__mutmut_3(self, duration: float = 1.0) -> "BaseElement":
        """Highlight the element for debugging purposes."""
        original_style = self.element.get_attribute(None)
        self.driver.execute_script(
            "arguments[0].style.border='3px solid red';", self.element
        )
        time.sleep(duration)
        self.driver.execute_script(
            f"arguments[0].style.border='{original_style}';", self.element
        )
        return self

    def xǁBaseElementǁhighlight__mutmut_4(self, duration: float = 1.0) -> "BaseElement":
        """Highlight the element for debugging purposes."""
        original_style = self.element.get_attribute("XXstyleXX")
        self.driver.execute_script(
            "arguments[0].style.border='3px solid red';", self.element
        )
        time.sleep(duration)
        self.driver.execute_script(
            f"arguments[0].style.border='{original_style}';", self.element
        )
        return self

    def xǁBaseElementǁhighlight__mutmut_5(self, duration: float = 1.0) -> "BaseElement":
        """Highlight the element for debugging purposes."""
        original_style = self.element.get_attribute("STYLE")
        self.driver.execute_script(
            "arguments[0].style.border='3px solid red';", self.element
        )
        time.sleep(duration)
        self.driver.execute_script(
            f"arguments[0].style.border='{original_style}';", self.element
        )
        return self

    def xǁBaseElementǁhighlight__mutmut_6(self, duration: float = 1.0) -> "BaseElement":
        """Highlight the element for debugging purposes."""
        original_style = self.element.get_attribute("style")
        self.driver.execute_script(None, self.element)
        time.sleep(duration)
        self.driver.execute_script(
            f"arguments[0].style.border='{original_style}';", self.element
        )
        return self

    def xǁBaseElementǁhighlight__mutmut_7(self, duration: float = 1.0) -> "BaseElement":
        """Highlight the element for debugging purposes."""
        original_style = self.element.get_attribute("style")
        self.driver.execute_script("arguments[0].style.border='3px solid red';", None)
        time.sleep(duration)
        self.driver.execute_script(
            f"arguments[0].style.border='{original_style}';", self.element
        )
        return self

    def xǁBaseElementǁhighlight__mutmut_8(self, duration: float = 1.0) -> "BaseElement":
        """Highlight the element for debugging purposes."""
        original_style = self.element.get_attribute("style")
        self.driver.execute_script(self.element)
        time.sleep(duration)
        self.driver.execute_script(
            f"arguments[0].style.border='{original_style}';", self.element
        )
        return self

    def xǁBaseElementǁhighlight__mutmut_9(self, duration: float = 1.0) -> "BaseElement":
        """Highlight the element for debugging purposes."""
        original_style = self.element.get_attribute("style")
        self.driver.execute_script(
            "arguments[0].style.border='3px solid red';",
        )
        time.sleep(duration)
        self.driver.execute_script(
            f"arguments[0].style.border='{original_style}';", self.element
        )
        return self

    def xǁBaseElementǁhighlight__mutmut_10(
        self, duration: float = 1.0
    ) -> "BaseElement":
        """Highlight the element for debugging purposes."""
        original_style = self.element.get_attribute("style")
        self.driver.execute_script(
            "XXarguments[0].style.border='3px solid red';XX", self.element
        )
        time.sleep(duration)
        self.driver.execute_script(
            f"arguments[0].style.border='{original_style}';", self.element
        )
        return self

    def xǁBaseElementǁhighlight__mutmut_11(
        self, duration: float = 1.0
    ) -> "BaseElement":
        """Highlight the element for debugging purposes."""
        original_style = self.element.get_attribute("style")
        self.driver.execute_script(
            "ARGUMENTS[0].STYLE.BORDER='3PX SOLID RED';", self.element
        )
        time.sleep(duration)
        self.driver.execute_script(
            f"arguments[0].style.border='{original_style}';", self.element
        )
        return self

    def xǁBaseElementǁhighlight__mutmut_12(
        self, duration: float = 1.0
    ) -> "BaseElement":
        """Highlight the element for debugging purposes."""
        original_style = self.element.get_attribute("style")
        self.driver.execute_script(
            "arguments[0].style.border='3px solid red';", self.element
        )
        time.sleep(None)
        self.driver.execute_script(
            f"arguments[0].style.border='{original_style}';", self.element
        )
        return self

    def xǁBaseElementǁhighlight__mutmut_13(
        self, duration: float = 1.0
    ) -> "BaseElement":
        """Highlight the element for debugging purposes."""
        original_style = self.element.get_attribute("style")
        self.driver.execute_script(
            "arguments[0].style.border='3px solid red';", self.element
        )
        time.sleep(duration)
        self.driver.execute_script(None, self.element)
        return self

    def xǁBaseElementǁhighlight__mutmut_14(
        self, duration: float = 1.0
    ) -> "BaseElement":
        """Highlight the element for debugging purposes."""
        original_style = self.element.get_attribute("style")
        self.driver.execute_script(
            "arguments[0].style.border='3px solid red';", self.element
        )
        time.sleep(duration)
        self.driver.execute_script(
            f"arguments[0].style.border='{original_style}';", None
        )
        return self

    def xǁBaseElementǁhighlight__mutmut_15(
        self, duration: float = 1.0
    ) -> "BaseElement":
        """Highlight the element for debugging purposes."""
        original_style = self.element.get_attribute("style")
        self.driver.execute_script(
            "arguments[0].style.border='3px solid red';", self.element
        )
        time.sleep(duration)
        self.driver.execute_script(self.element)
        return self

    def xǁBaseElementǁhighlight__mutmut_16(
        self, duration: float = 1.0
    ) -> "BaseElement":
        """Highlight the element for debugging purposes."""
        original_style = self.element.get_attribute("style")
        self.driver.execute_script(
            "arguments[0].style.border='3px solid red';", self.element
        )
        time.sleep(duration)
        self.driver.execute_script(
            f"arguments[0].style.border='{original_style}';",
        )
        return self

    xǁBaseElementǁhighlight__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁBaseElementǁhighlight__mutmut_1": xǁBaseElementǁhighlight__mutmut_1,
        "xǁBaseElementǁhighlight__mutmut_2": xǁBaseElementǁhighlight__mutmut_2,
        "xǁBaseElementǁhighlight__mutmut_3": xǁBaseElementǁhighlight__mutmut_3,
        "xǁBaseElementǁhighlight__mutmut_4": xǁBaseElementǁhighlight__mutmut_4,
        "xǁBaseElementǁhighlight__mutmut_5": xǁBaseElementǁhighlight__mutmut_5,
        "xǁBaseElementǁhighlight__mutmut_6": xǁBaseElementǁhighlight__mutmut_6,
        "xǁBaseElementǁhighlight__mutmut_7": xǁBaseElementǁhighlight__mutmut_7,
        "xǁBaseElementǁhighlight__mutmut_8": xǁBaseElementǁhighlight__mutmut_8,
        "xǁBaseElementǁhighlight__mutmut_9": xǁBaseElementǁhighlight__mutmut_9,
        "xǁBaseElementǁhighlight__mutmut_10": xǁBaseElementǁhighlight__mutmut_10,
        "xǁBaseElementǁhighlight__mutmut_11": xǁBaseElementǁhighlight__mutmut_11,
        "xǁBaseElementǁhighlight__mutmut_12": xǁBaseElementǁhighlight__mutmut_12,
        "xǁBaseElementǁhighlight__mutmut_13": xǁBaseElementǁhighlight__mutmut_13,
        "xǁBaseElementǁhighlight__mutmut_14": xǁBaseElementǁhighlight__mutmut_14,
        "xǁBaseElementǁhighlight__mutmut_15": xǁBaseElementǁhighlight__mutmut_15,
        "xǁBaseElementǁhighlight__mutmut_16": xǁBaseElementǁhighlight__mutmut_16,
    }

    def highlight(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁBaseElementǁhighlight__mutmut_orig"),
            object.__getattribute__(self, "xǁBaseElementǁhighlight__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    highlight.__signature__ = _mutmut_signature(xǁBaseElementǁhighlight__mutmut_orig)
    xǁBaseElementǁhighlight__mutmut_orig.__name__ = "xǁBaseElementǁhighlight"

    @property
    def text(self) -> str:
        """Get the text content of the element."""
        return self.element.text

    @property
    def is_displayed(self) -> bool:
        """Check if the element is displayed."""
        try:
            return self.element.is_displayed()
        except StaleElementReferenceException:
            self._element = None
            return self.element.is_displayed()

    @property
    def is_enabled(self) -> bool:
        """Check if the element is enabled."""
        return self.element.is_enabled()

    def xǁBaseElementǁget_attribute__mutmut_orig(self, name: str) -> str | None:
        """Get an attribute value from the element."""
        return self.element.get_attribute(name)

    def xǁBaseElementǁget_attribute__mutmut_1(self, name: str) -> str | None:
        """Get an attribute value from the element."""
        return self.element.get_attribute(None)

    xǁBaseElementǁget_attribute__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁBaseElementǁget_attribute__mutmut_1": xǁBaseElementǁget_attribute__mutmut_1
    }

    def get_attribute(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁBaseElementǁget_attribute__mutmut_orig"),
            object.__getattribute__(
                self, "xǁBaseElementǁget_attribute__mutmut_mutants"
            ),
            args,
            kwargs,
            self,
        )
        return result

    get_attribute.__signature__ = _mutmut_signature(
        xǁBaseElementǁget_attribute__mutmut_orig
    )
    xǁBaseElementǁget_attribute__mutmut_orig.__name__ = "xǁBaseElementǁget_attribute"

    def xǁBaseElementǁget_property__mutmut_orig(self, name: str) -> Any:
        """Get a property value from the element."""
        return self.element.get_property(name)

    def xǁBaseElementǁget_property__mutmut_1(self, name: str) -> Any:
        """Get a property value from the element."""
        return self.element.get_property(None)

    xǁBaseElementǁget_property__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁBaseElementǁget_property__mutmut_1": xǁBaseElementǁget_property__mutmut_1
    }

    def get_property(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁBaseElementǁget_property__mutmut_orig"),
            object.__getattribute__(self, "xǁBaseElementǁget_property__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    get_property.__signature__ = _mutmut_signature(
        xǁBaseElementǁget_property__mutmut_orig
    )
    xǁBaseElementǁget_property__mutmut_orig.__name__ = "xǁBaseElementǁget_property"


class Clickable(BaseElement):
    """Base class for clickable elements like buttons and links."""

    def xǁClickableǁclick__mutmut_orig(self, force: bool = False) -> "Clickable":
        """
        Click the element.

        Args:
            force: If True, use JavaScript click instead of normal click
        """
        try:
            if force:
                self.driver.execute_script("arguments[0].click();", self.element)
            else:
                self.scroll_into_view()
                self.wait_for_clickable()
                self.element.click()
            logger.debug(f"Clicked element: {self.locator}")
            return self
        except ElementNotInteractableException as e:
            raise ElementNotInteractableError(str(self.locator), "click") from e

    def xǁClickableǁclick__mutmut_1(self, force: bool = True) -> "Clickable":
        """
        Click the element.

        Args:
            force: If True, use JavaScript click instead of normal click
        """
        try:
            if force:
                self.driver.execute_script("arguments[0].click();", self.element)
            else:
                self.scroll_into_view()
                self.wait_for_clickable()
                self.element.click()
            logger.debug(f"Clicked element: {self.locator}")
            return self
        except ElementNotInteractableException as e:
            raise ElementNotInteractableError(str(self.locator), "click") from e

    def xǁClickableǁclick__mutmut_2(self, force: bool = False) -> "Clickable":
        """
        Click the element.

        Args:
            force: If True, use JavaScript click instead of normal click
        """
        try:
            if force:
                self.driver.execute_script(None, self.element)
            else:
                self.scroll_into_view()
                self.wait_for_clickable()
                self.element.click()
            logger.debug(f"Clicked element: {self.locator}")
            return self
        except ElementNotInteractableException as e:
            raise ElementNotInteractableError(str(self.locator), "click") from e

    def xǁClickableǁclick__mutmut_3(self, force: bool = False) -> "Clickable":
        """
        Click the element.

        Args:
            force: If True, use JavaScript click instead of normal click
        """
        try:
            if force:
                self.driver.execute_script("arguments[0].click();", None)
            else:
                self.scroll_into_view()
                self.wait_for_clickable()
                self.element.click()
            logger.debug(f"Clicked element: {self.locator}")
            return self
        except ElementNotInteractableException as e:
            raise ElementNotInteractableError(str(self.locator), "click") from e

    def xǁClickableǁclick__mutmut_4(self, force: bool = False) -> "Clickable":
        """
        Click the element.

        Args:
            force: If True, use JavaScript click instead of normal click
        """
        try:
            if force:
                self.driver.execute_script(self.element)
            else:
                self.scroll_into_view()
                self.wait_for_clickable()
                self.element.click()
            logger.debug(f"Clicked element: {self.locator}")
            return self
        except ElementNotInteractableException as e:
            raise ElementNotInteractableError(str(self.locator), "click") from e

    def xǁClickableǁclick__mutmut_5(self, force: bool = False) -> "Clickable":
        """
        Click the element.

        Args:
            force: If True, use JavaScript click instead of normal click
        """
        try:
            if force:
                self.driver.execute_script(
                    "arguments[0].click();",
                )
            else:
                self.scroll_into_view()
                self.wait_for_clickable()
                self.element.click()
            logger.debug(f"Clicked element: {self.locator}")
            return self
        except ElementNotInteractableException as e:
            raise ElementNotInteractableError(str(self.locator), "click") from e

    def xǁClickableǁclick__mutmut_6(self, force: bool = False) -> "Clickable":
        """
        Click the element.

        Args:
            force: If True, use JavaScript click instead of normal click
        """
        try:
            if force:
                self.driver.execute_script("XXarguments[0].click();XX", self.element)
            else:
                self.scroll_into_view()
                self.wait_for_clickable()
                self.element.click()
            logger.debug(f"Clicked element: {self.locator}")
            return self
        except ElementNotInteractableException as e:
            raise ElementNotInteractableError(str(self.locator), "click") from e

    def xǁClickableǁclick__mutmut_7(self, force: bool = False) -> "Clickable":
        """
        Click the element.

        Args:
            force: If True, use JavaScript click instead of normal click
        """
        try:
            if force:
                self.driver.execute_script("ARGUMENTS[0].CLICK();", self.element)
            else:
                self.scroll_into_view()
                self.wait_for_clickable()
                self.element.click()
            logger.debug(f"Clicked element: {self.locator}")
            return self
        except ElementNotInteractableException as e:
            raise ElementNotInteractableError(str(self.locator), "click") from e

    def xǁClickableǁclick__mutmut_8(self, force: bool = False) -> "Clickable":
        """
        Click the element.

        Args:
            force: If True, use JavaScript click instead of normal click
        """
        try:
            if force:
                self.driver.execute_script("arguments[0].click();", self.element)
            else:
                self.scroll_into_view()
                self.wait_for_clickable()
                self.element.click()
            logger.debug(None)
            return self
        except ElementNotInteractableException as e:
            raise ElementNotInteractableError(str(self.locator), "click") from e

    def xǁClickableǁclick__mutmut_9(self, force: bool = False) -> "Clickable":
        """
        Click the element.

        Args:
            force: If True, use JavaScript click instead of normal click
        """
        try:
            if force:
                self.driver.execute_script("arguments[0].click();", self.element)
            else:
                self.scroll_into_view()
                self.wait_for_clickable()
                self.element.click()
            logger.debug(f"Clicked element: {self.locator}")
            return self
        except ElementNotInteractableException as e:
            raise ElementNotInteractableError(None, "click") from e

    def xǁClickableǁclick__mutmut_10(self, force: bool = False) -> "Clickable":
        """
        Click the element.

        Args:
            force: If True, use JavaScript click instead of normal click
        """
        try:
            if force:
                self.driver.execute_script("arguments[0].click();", self.element)
            else:
                self.scroll_into_view()
                self.wait_for_clickable()
                self.element.click()
            logger.debug(f"Clicked element: {self.locator}")
            return self
        except ElementNotInteractableException as e:
            raise ElementNotInteractableError(str(self.locator), None) from e

    def xǁClickableǁclick__mutmut_11(self, force: bool = False) -> "Clickable":
        """
        Click the element.

        Args:
            force: If True, use JavaScript click instead of normal click
        """
        try:
            if force:
                self.driver.execute_script("arguments[0].click();", self.element)
            else:
                self.scroll_into_view()
                self.wait_for_clickable()
                self.element.click()
            logger.debug(f"Clicked element: {self.locator}")
            return self
        except ElementNotInteractableException as e:
            raise ElementNotInteractableError("click") from e

    def xǁClickableǁclick__mutmut_12(self, force: bool = False) -> "Clickable":
        """
        Click the element.

        Args:
            force: If True, use JavaScript click instead of normal click
        """
        try:
            if force:
                self.driver.execute_script("arguments[0].click();", self.element)
            else:
                self.scroll_into_view()
                self.wait_for_clickable()
                self.element.click()
            logger.debug(f"Clicked element: {self.locator}")
            return self
        except ElementNotInteractableException as e:
            raise ElementNotInteractableError(
                str(self.locator),
            ) from e

    def xǁClickableǁclick__mutmut_13(self, force: bool = False) -> "Clickable":
        """
        Click the element.

        Args:
            force: If True, use JavaScript click instead of normal click
        """
        try:
            if force:
                self.driver.execute_script("arguments[0].click();", self.element)
            else:
                self.scroll_into_view()
                self.wait_for_clickable()
                self.element.click()
            logger.debug(f"Clicked element: {self.locator}")
            return self
        except ElementNotInteractableException as e:
            raise ElementNotInteractableError(str(None), "click") from e

    def xǁClickableǁclick__mutmut_14(self, force: bool = False) -> "Clickable":
        """
        Click the element.

        Args:
            force: If True, use JavaScript click instead of normal click
        """
        try:
            if force:
                self.driver.execute_script("arguments[0].click();", self.element)
            else:
                self.scroll_into_view()
                self.wait_for_clickable()
                self.element.click()
            logger.debug(f"Clicked element: {self.locator}")
            return self
        except ElementNotInteractableException as e:
            raise ElementNotInteractableError(str(self.locator), "XXclickXX") from e

    def xǁClickableǁclick__mutmut_15(self, force: bool = False) -> "Clickable":
        """
        Click the element.

        Args:
            force: If True, use JavaScript click instead of normal click
        """
        try:
            if force:
                self.driver.execute_script("arguments[0].click();", self.element)
            else:
                self.scroll_into_view()
                self.wait_for_clickable()
                self.element.click()
            logger.debug(f"Clicked element: {self.locator}")
            return self
        except ElementNotInteractableException as e:
            raise ElementNotInteractableError(str(self.locator), "CLICK") from e

    xǁClickableǁclick__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁClickableǁclick__mutmut_1": xǁClickableǁclick__mutmut_1,
        "xǁClickableǁclick__mutmut_2": xǁClickableǁclick__mutmut_2,
        "xǁClickableǁclick__mutmut_3": xǁClickableǁclick__mutmut_3,
        "xǁClickableǁclick__mutmut_4": xǁClickableǁclick__mutmut_4,
        "xǁClickableǁclick__mutmut_5": xǁClickableǁclick__mutmut_5,
        "xǁClickableǁclick__mutmut_6": xǁClickableǁclick__mutmut_6,
        "xǁClickableǁclick__mutmut_7": xǁClickableǁclick__mutmut_7,
        "xǁClickableǁclick__mutmut_8": xǁClickableǁclick__mutmut_8,
        "xǁClickableǁclick__mutmut_9": xǁClickableǁclick__mutmut_9,
        "xǁClickableǁclick__mutmut_10": xǁClickableǁclick__mutmut_10,
        "xǁClickableǁclick__mutmut_11": xǁClickableǁclick__mutmut_11,
        "xǁClickableǁclick__mutmut_12": xǁClickableǁclick__mutmut_12,
        "xǁClickableǁclick__mutmut_13": xǁClickableǁclick__mutmut_13,
        "xǁClickableǁclick__mutmut_14": xǁClickableǁclick__mutmut_14,
        "xǁClickableǁclick__mutmut_15": xǁClickableǁclick__mutmut_15,
    }

    def click(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁClickableǁclick__mutmut_orig"),
            object.__getattribute__(self, "xǁClickableǁclick__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    click.__signature__ = _mutmut_signature(xǁClickableǁclick__mutmut_orig)
    xǁClickableǁclick__mutmut_orig.__name__ = "xǁClickableǁclick"

    def xǁClickableǁdouble_click__mutmut_orig(self) -> "Clickable":
        """Double-click the element."""
        self.scroll_into_view()
        self.wait_for_clickable()
        ActionChains(self.driver).double_click(self.element).perform()
        logger.debug(f"Double-clicked element: {self.locator}")
        return self

    def xǁClickableǁdouble_click__mutmut_1(self) -> "Clickable":
        """Double-click the element."""
        self.scroll_into_view()
        self.wait_for_clickable()
        ActionChains(self.driver).double_click(None).perform()
        logger.debug(f"Double-clicked element: {self.locator}")
        return self

    def xǁClickableǁdouble_click__mutmut_2(self) -> "Clickable":
        """Double-click the element."""
        self.scroll_into_view()
        self.wait_for_clickable()
        ActionChains(None).double_click(self.element).perform()
        logger.debug(f"Double-clicked element: {self.locator}")
        return self

    def xǁClickableǁdouble_click__mutmut_3(self) -> "Clickable":
        """Double-click the element."""
        self.scroll_into_view()
        self.wait_for_clickable()
        ActionChains(self.driver).double_click(self.element).perform()
        logger.debug(None)
        return self

    xǁClickableǁdouble_click__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁClickableǁdouble_click__mutmut_1": xǁClickableǁdouble_click__mutmut_1,
        "xǁClickableǁdouble_click__mutmut_2": xǁClickableǁdouble_click__mutmut_2,
        "xǁClickableǁdouble_click__mutmut_3": xǁClickableǁdouble_click__mutmut_3,
    }

    def double_click(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁClickableǁdouble_click__mutmut_orig"),
            object.__getattribute__(self, "xǁClickableǁdouble_click__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    double_click.__signature__ = _mutmut_signature(
        xǁClickableǁdouble_click__mutmut_orig
    )
    xǁClickableǁdouble_click__mutmut_orig.__name__ = "xǁClickableǁdouble_click"

    def xǁClickableǁright_click__mutmut_orig(self) -> "Clickable":
        """Right-click the element."""
        self.scroll_into_view()
        self.wait_for_clickable()
        ActionChains(self.driver).context_click(self.element).perform()
        logger.debug(f"Right-clicked element: {self.locator}")
        return self

    def xǁClickableǁright_click__mutmut_1(self) -> "Clickable":
        """Right-click the element."""
        self.scroll_into_view()
        self.wait_for_clickable()
        ActionChains(self.driver).context_click(None).perform()
        logger.debug(f"Right-clicked element: {self.locator}")
        return self

    def xǁClickableǁright_click__mutmut_2(self) -> "Clickable":
        """Right-click the element."""
        self.scroll_into_view()
        self.wait_for_clickable()
        ActionChains(None).context_click(self.element).perform()
        logger.debug(f"Right-clicked element: {self.locator}")
        return self

    def xǁClickableǁright_click__mutmut_3(self) -> "Clickable":
        """Right-click the element."""
        self.scroll_into_view()
        self.wait_for_clickable()
        ActionChains(self.driver).context_click(self.element).perform()
        logger.debug(None)
        return self

    xǁClickableǁright_click__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁClickableǁright_click__mutmut_1": xǁClickableǁright_click__mutmut_1,
        "xǁClickableǁright_click__mutmut_2": xǁClickableǁright_click__mutmut_2,
        "xǁClickableǁright_click__mutmut_3": xǁClickableǁright_click__mutmut_3,
    }

    def right_click(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁClickableǁright_click__mutmut_orig"),
            object.__getattribute__(self, "xǁClickableǁright_click__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    right_click.__signature__ = _mutmut_signature(xǁClickableǁright_click__mutmut_orig)
    xǁClickableǁright_click__mutmut_orig.__name__ = "xǁClickableǁright_click"


class Button(Clickable):
    """Represents a button element."""

    pass


class Link(Clickable):
    """Represents a link element."""

    @property
    def href(self) -> str | None:
        """Get the href attribute of the link."""
        return self.get_attribute("href")


class TextInput(BaseElement):
    """Represents a text input field."""

    def xǁTextInputǁclear__mutmut_orig(self) -> "TextInput":
        """Clear the input field."""
        self.wait_for_visible()
        self.element.clear()
        logger.debug(f"Cleared input: {self.locator}")
        return self

    def xǁTextInputǁclear__mutmut_1(self) -> "TextInput":
        """Clear the input field."""
        self.wait_for_visible()
        self.element.clear()
        logger.debug(None)
        return self

    xǁTextInputǁclear__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁTextInputǁclear__mutmut_1": xǁTextInputǁclear__mutmut_1
    }

    def clear(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁTextInputǁclear__mutmut_orig"),
            object.__getattribute__(self, "xǁTextInputǁclear__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    clear.__signature__ = _mutmut_signature(xǁTextInputǁclear__mutmut_orig)
    xǁTextInputǁclear__mutmut_orig.__name__ = "xǁTextInputǁclear"

    def xǁTextInputǁtype_text__mutmut_orig(
        self, text: str, clear_first: bool = True
    ) -> "TextInput":
        """
        Type text into the input field.

        Args:
            text: Text to type
            clear_first: Whether to clear the field first
        """
        self.wait_for_visible()
        if clear_first:
            self.clear()
        self.element.send_keys(text)
        logger.debug(f"Typed '{text}' into input: {self.locator}")
        return self

    def xǁTextInputǁtype_text__mutmut_1(
        self, text: str, clear_first: bool = False
    ) -> "TextInput":
        """
        Type text into the input field.

        Args:
            text: Text to type
            clear_first: Whether to clear the field first
        """
        self.wait_for_visible()
        if clear_first:
            self.clear()
        self.element.send_keys(text)
        logger.debug(f"Typed '{text}' into input: {self.locator}")
        return self

    def xǁTextInputǁtype_text__mutmut_2(
        self, text: str, clear_first: bool = True
    ) -> "TextInput":
        """
        Type text into the input field.

        Args:
            text: Text to type
            clear_first: Whether to clear the field first
        """
        self.wait_for_visible()
        if clear_first:
            self.clear()
        self.element.send_keys(None)
        logger.debug(f"Typed '{text}' into input: {self.locator}")
        return self

    def xǁTextInputǁtype_text__mutmut_3(
        self, text: str, clear_first: bool = True
    ) -> "TextInput":
        """
        Type text into the input field.

        Args:
            text: Text to type
            clear_first: Whether to clear the field first
        """
        self.wait_for_visible()
        if clear_first:
            self.clear()
        self.element.send_keys(text)
        logger.debug(None)
        return self

    xǁTextInputǁtype_text__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁTextInputǁtype_text__mutmut_1": xǁTextInputǁtype_text__mutmut_1,
        "xǁTextInputǁtype_text__mutmut_2": xǁTextInputǁtype_text__mutmut_2,
        "xǁTextInputǁtype_text__mutmut_3": xǁTextInputǁtype_text__mutmut_3,
    }

    def type_text(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁTextInputǁtype_text__mutmut_orig"),
            object.__getattribute__(self, "xǁTextInputǁtype_text__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    type_text.__signature__ = _mutmut_signature(xǁTextInputǁtype_text__mutmut_orig)
    xǁTextInputǁtype_text__mutmut_orig.__name__ = "xǁTextInputǁtype_text"

    def xǁTextInputǁappend_text__mutmut_orig(self, text: str) -> "TextInput":
        """Append text to the existing content."""
        return self.type_text(text, clear_first=False)

    def xǁTextInputǁappend_text__mutmut_1(self, text: str) -> "TextInput":
        """Append text to the existing content."""
        return self.type_text(None, clear_first=False)

    def xǁTextInputǁappend_text__mutmut_2(self, text: str) -> "TextInput":
        """Append text to the existing content."""
        return self.type_text(text, clear_first=None)

    def xǁTextInputǁappend_text__mutmut_3(self, text: str) -> "TextInput":
        """Append text to the existing content."""
        return self.type_text(clear_first=False)

    def xǁTextInputǁappend_text__mutmut_4(self, text: str) -> "TextInput":
        """Append text to the existing content."""
        return self.type_text(
            text,
        )

    def xǁTextInputǁappend_text__mutmut_5(self, text: str) -> "TextInput":
        """Append text to the existing content."""
        return self.type_text(text, clear_first=True)

    xǁTextInputǁappend_text__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁTextInputǁappend_text__mutmut_1": xǁTextInputǁappend_text__mutmut_1,
        "xǁTextInputǁappend_text__mutmut_2": xǁTextInputǁappend_text__mutmut_2,
        "xǁTextInputǁappend_text__mutmut_3": xǁTextInputǁappend_text__mutmut_3,
        "xǁTextInputǁappend_text__mutmut_4": xǁTextInputǁappend_text__mutmut_4,
        "xǁTextInputǁappend_text__mutmut_5": xǁTextInputǁappend_text__mutmut_5,
    }

    def append_text(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁTextInputǁappend_text__mutmut_orig"),
            object.__getattribute__(self, "xǁTextInputǁappend_text__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    append_text.__signature__ = _mutmut_signature(xǁTextInputǁappend_text__mutmut_orig)
    xǁTextInputǁappend_text__mutmut_orig.__name__ = "xǁTextInputǁappend_text"

    def xǁTextInputǁpress_key__mutmut_orig(self, key: str) -> "TextInput":
        """Press a special key (e.g., Keys.ENTER, Keys.TAB)."""
        self.element.send_keys(key)
        logger.debug(f"Pressed key '{key}' in input: {self.locator}")
        return self

    def xǁTextInputǁpress_key__mutmut_1(self, key: str) -> "TextInput":
        """Press a special key (e.g., Keys.ENTER, Keys.TAB)."""
        self.element.send_keys(None)
        logger.debug(f"Pressed key '{key}' in input: {self.locator}")
        return self

    def xǁTextInputǁpress_key__mutmut_2(self, key: str) -> "TextInput":
        """Press a special key (e.g., Keys.ENTER, Keys.TAB)."""
        self.element.send_keys(key)
        logger.debug(None)
        return self

    xǁTextInputǁpress_key__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁTextInputǁpress_key__mutmut_1": xǁTextInputǁpress_key__mutmut_1,
        "xǁTextInputǁpress_key__mutmut_2": xǁTextInputǁpress_key__mutmut_2,
    }

    def press_key(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁTextInputǁpress_key__mutmut_orig"),
            object.__getattribute__(self, "xǁTextInputǁpress_key__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    press_key.__signature__ = _mutmut_signature(xǁTextInputǁpress_key__mutmut_orig)
    xǁTextInputǁpress_key__mutmut_orig.__name__ = "xǁTextInputǁpress_key"

    @property
    def value(self) -> str:
        """Get the current value of the input field."""
        return self.get_attribute("value") or ""


class Dropdown(BaseElement):
    """Represents a dropdown/select element."""

    @property
    def select(self) -> Select:
        """Get the Selenium Select object."""
        return Select(self.element)

    def xǁDropdownǁselect_by_text__mutmut_orig(self, text: str) -> "Dropdown":
        """Select an option by visible text."""
        self.wait_for_visible()
        self.select.select_by_visible_text(text)
        logger.debug(f"Selected '{text}' in dropdown: {self.locator}")
        return self

    def xǁDropdownǁselect_by_text__mutmut_1(self, text: str) -> "Dropdown":
        """Select an option by visible text."""
        self.wait_for_visible()
        self.select.select_by_visible_text(None)
        logger.debug(f"Selected '{text}' in dropdown: {self.locator}")
        return self

    def xǁDropdownǁselect_by_text__mutmut_2(self, text: str) -> "Dropdown":
        """Select an option by visible text."""
        self.wait_for_visible()
        self.select.select_by_visible_text(text)
        logger.debug(None)
        return self

    xǁDropdownǁselect_by_text__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁDropdownǁselect_by_text__mutmut_1": xǁDropdownǁselect_by_text__mutmut_1,
        "xǁDropdownǁselect_by_text__mutmut_2": xǁDropdownǁselect_by_text__mutmut_2,
    }

    def select_by_text(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁDropdownǁselect_by_text__mutmut_orig"),
            object.__getattribute__(self, "xǁDropdownǁselect_by_text__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    select_by_text.__signature__ = _mutmut_signature(
        xǁDropdownǁselect_by_text__mutmut_orig
    )
    xǁDropdownǁselect_by_text__mutmut_orig.__name__ = "xǁDropdownǁselect_by_text"

    def xǁDropdownǁselect_by_value__mutmut_orig(self, value: str) -> "Dropdown":
        """Select an option by value attribute."""
        self.wait_for_visible()
        self.select.select_by_value(value)
        logger.debug(f"Selected value '{value}' in dropdown: {self.locator}")
        return self

    def xǁDropdownǁselect_by_value__mutmut_1(self, value: str) -> "Dropdown":
        """Select an option by value attribute."""
        self.wait_for_visible()
        self.select.select_by_value(None)
        logger.debug(f"Selected value '{value}' in dropdown: {self.locator}")
        return self

    def xǁDropdownǁselect_by_value__mutmut_2(self, value: str) -> "Dropdown":
        """Select an option by value attribute."""
        self.wait_for_visible()
        self.select.select_by_value(value)
        logger.debug(None)
        return self

    xǁDropdownǁselect_by_value__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁDropdownǁselect_by_value__mutmut_1": xǁDropdownǁselect_by_value__mutmut_1,
        "xǁDropdownǁselect_by_value__mutmut_2": xǁDropdownǁselect_by_value__mutmut_2,
    }

    def select_by_value(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁDropdownǁselect_by_value__mutmut_orig"),
            object.__getattribute__(self, "xǁDropdownǁselect_by_value__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    select_by_value.__signature__ = _mutmut_signature(
        xǁDropdownǁselect_by_value__mutmut_orig
    )
    xǁDropdownǁselect_by_value__mutmut_orig.__name__ = "xǁDropdownǁselect_by_value"

    def xǁDropdownǁselect_by_index__mutmut_orig(self, index: int) -> "Dropdown":
        """Select an option by index."""
        self.wait_for_visible()
        self.select.select_by_index(index)
        logger.debug(f"Selected index {index} in dropdown: {self.locator}")
        return self

    def xǁDropdownǁselect_by_index__mutmut_1(self, index: int) -> "Dropdown":
        """Select an option by index."""
        self.wait_for_visible()
        self.select.select_by_index(None)
        logger.debug(f"Selected index {index} in dropdown: {self.locator}")
        return self

    def xǁDropdownǁselect_by_index__mutmut_2(self, index: int) -> "Dropdown":
        """Select an option by index."""
        self.wait_for_visible()
        self.select.select_by_index(index)
        logger.debug(None)
        return self

    xǁDropdownǁselect_by_index__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁDropdownǁselect_by_index__mutmut_1": xǁDropdownǁselect_by_index__mutmut_1,
        "xǁDropdownǁselect_by_index__mutmut_2": xǁDropdownǁselect_by_index__mutmut_2,
    }

    def select_by_index(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁDropdownǁselect_by_index__mutmut_orig"),
            object.__getattribute__(self, "xǁDropdownǁselect_by_index__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    select_by_index.__signature__ = _mutmut_signature(
        xǁDropdownǁselect_by_index__mutmut_orig
    )
    xǁDropdownǁselect_by_index__mutmut_orig.__name__ = "xǁDropdownǁselect_by_index"

    @property
    def selected_option_text(self) -> str:
        """Get the text of the currently selected option."""
        return self.select.first_selected_option.text

    @property
    def selected_option_value(self) -> str:
        """Get the value of the currently selected option."""
        return self.select.first_selected_option.get_attribute("value")

    @property
    def all_options_text(self) -> list[str]:
        """Get text of all available options."""
        return [option.text for option in self.select.options]


class Checkbox(BaseElement):
    """Represents a checkbox element."""

    def xǁCheckboxǁcheck__mutmut_orig(self) -> "Checkbox":
        """Check the checkbox if not already checked."""
        if not self.is_checked:
            self.scroll_into_view()
            self.wait_for_clickable()
            self.element.click()
            logger.debug(f"Checked checkbox: {self.locator}")
        return self

    def xǁCheckboxǁcheck__mutmut_1(self) -> "Checkbox":
        """Check the checkbox if not already checked."""
        if self.is_checked:
            self.scroll_into_view()
            self.wait_for_clickable()
            self.element.click()
            logger.debug(f"Checked checkbox: {self.locator}")
        return self

    def xǁCheckboxǁcheck__mutmut_2(self) -> "Checkbox":
        """Check the checkbox if not already checked."""
        if not self.is_checked:
            self.scroll_into_view()
            self.wait_for_clickable()
            self.element.click()
            logger.debug(None)
        return self

    xǁCheckboxǁcheck__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁCheckboxǁcheck__mutmut_1": xǁCheckboxǁcheck__mutmut_1,
        "xǁCheckboxǁcheck__mutmut_2": xǁCheckboxǁcheck__mutmut_2,
    }

    def check(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁCheckboxǁcheck__mutmut_orig"),
            object.__getattribute__(self, "xǁCheckboxǁcheck__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    check.__signature__ = _mutmut_signature(xǁCheckboxǁcheck__mutmut_orig)
    xǁCheckboxǁcheck__mutmut_orig.__name__ = "xǁCheckboxǁcheck"

    def xǁCheckboxǁuncheck__mutmut_orig(self) -> "Checkbox":
        """Uncheck the checkbox if currently checked."""
        if self.is_checked:
            self.scroll_into_view()
            self.wait_for_clickable()
            self.element.click()
            logger.debug(f"Unchecked checkbox: {self.locator}")
        return self

    def xǁCheckboxǁuncheck__mutmut_1(self) -> "Checkbox":
        """Uncheck the checkbox if currently checked."""
        if self.is_checked:
            self.scroll_into_view()
            self.wait_for_clickable()
            self.element.click()
            logger.debug(None)
        return self

    xǁCheckboxǁuncheck__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁCheckboxǁuncheck__mutmut_1": xǁCheckboxǁuncheck__mutmut_1
    }

    def uncheck(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁCheckboxǁuncheck__mutmut_orig"),
            object.__getattribute__(self, "xǁCheckboxǁuncheck__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    uncheck.__signature__ = _mutmut_signature(xǁCheckboxǁuncheck__mutmut_orig)
    xǁCheckboxǁuncheck__mutmut_orig.__name__ = "xǁCheckboxǁuncheck"

    def xǁCheckboxǁtoggle__mutmut_orig(self) -> "Checkbox":
        """Toggle the checkbox state."""
        self.scroll_into_view()
        self.wait_for_clickable()
        self.element.click()
        logger.debug(f"Toggled checkbox: {self.locator}")
        return self

    def xǁCheckboxǁtoggle__mutmut_1(self) -> "Checkbox":
        """Toggle the checkbox state."""
        self.scroll_into_view()
        self.wait_for_clickable()
        self.element.click()
        logger.debug(None)
        return self

    xǁCheckboxǁtoggle__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁCheckboxǁtoggle__mutmut_1": xǁCheckboxǁtoggle__mutmut_1
    }

    def toggle(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁCheckboxǁtoggle__mutmut_orig"),
            object.__getattribute__(self, "xǁCheckboxǁtoggle__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    toggle.__signature__ = _mutmut_signature(xǁCheckboxǁtoggle__mutmut_orig)
    xǁCheckboxǁtoggle__mutmut_orig.__name__ = "xǁCheckboxǁtoggle"

    @property
    def is_checked(self) -> bool:
        """Check if the checkbox is currently checked."""
        return self.element.is_selected()


class RadioButton(BaseElement):
    """Represents a radio button element."""

    def xǁRadioButtonǁselect__mutmut_orig(self) -> "RadioButton":
        """Select the radio button."""
        if not self.is_selected:
            self.scroll_into_view()
            self.wait_for_clickable()
            self.element.click()
            logger.debug(f"Selected radio button: {self.locator}")
        return self

    def xǁRadioButtonǁselect__mutmut_1(self) -> "RadioButton":
        """Select the radio button."""
        if self.is_selected:
            self.scroll_into_view()
            self.wait_for_clickable()
            self.element.click()
            logger.debug(f"Selected radio button: {self.locator}")
        return self

    def xǁRadioButtonǁselect__mutmut_2(self) -> "RadioButton":
        """Select the radio button."""
        if not self.is_selected:
            self.scroll_into_view()
            self.wait_for_clickable()
            self.element.click()
            logger.debug(None)
        return self

    xǁRadioButtonǁselect__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁRadioButtonǁselect__mutmut_1": xǁRadioButtonǁselect__mutmut_1,
        "xǁRadioButtonǁselect__mutmut_2": xǁRadioButtonǁselect__mutmut_2,
    }

    def select(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁRadioButtonǁselect__mutmut_orig"),
            object.__getattribute__(self, "xǁRadioButtonǁselect__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    select.__signature__ = _mutmut_signature(xǁRadioButtonǁselect__mutmut_orig)
    xǁRadioButtonǁselect__mutmut_orig.__name__ = "xǁRadioButtonǁselect"

    @property
    def is_selected(self) -> bool:
        """Check if the radio button is currently selected."""
        return self.element.is_selected()
