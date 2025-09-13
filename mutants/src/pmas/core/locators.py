"""
Typed locator system for web elements with modern Python patterns.
"""

from dataclasses import dataclass
from typing import Literal

from selenium.webdriver.common.by import By

# Type alias for locator strategies
LocatorStrategy = Literal[
    "id",
    "css",
    "xpath",
    "name",
    "class_name",
    "tag_name",
    "link_text",
    "partial_link_text",
]

# Mapping from our strategy names to Selenium By constants
STRATEGY_MAP = {
    "id": By.ID,
    "css": By.CSS_SELECTOR,
    "xpath": By.XPATH,
    "name": By.NAME,
    "class_name": By.CLASS_NAME,
    "tag_name": By.TAG_NAME,
    "link_text": By.LINK_TEXT,
    "partial_link_text": By.PARTIAL_LINK_TEXT,
}
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


@dataclass(frozen=True)
class Locator:
    """
    Immutable locator for web elements with type safety.

    Args:
        strategy: The locator strategy (id, css, xpath, etc.)
        value: The locator value/selector string
        description: Optional human-readable description for debugging

    Example:
        >>> login_button = Locator('id', 'login-btn', 'Login button')
        >>> username_field = Locator('css', 'input[name="username"]')
    """

    strategy: LocatorStrategy
    value: str
    description: str = ""

    def __post_init__(self) -> None:
        """Validate the locator strategy."""
        if self.strategy not in STRATEGY_MAP:
            raise ValueError(f"Invalid locator strategy: {self.strategy}")

    @property
    def selenium_by(self) -> str:
        """Get the Selenium By constant for this locator."""
        return STRATEGY_MAP[self.strategy]

    @property
    def selenium_locator(self) -> tuple[str, str]:
        """Get the (By, value) tuple for Selenium WebDriver methods."""
        return (self.selenium_by, self.value)

    def format(self, **kwargs: str | int) -> "Locator":
        """
        Create a new locator with formatted value using string interpolation.

        Args:
            **kwargs: Values to substitute in the locator value

        Returns:
            New Locator instance with formatted value

        Example:
            >>> template = Locator('xpath', '//button[@data-id="{button_id}"]')
            >>> specific = template.format(button_id='submit')
        """
        try:
            formatted_value = self.value.format(**kwargs)
            return Locator(
                strategy=self.strategy,
                value=formatted_value,
                description=self.description,
            )
        except KeyError as e:
            raise ValueError(f"Missing format parameter: {e}") from e

    def __str__(self) -> str:
        """String representation for debugging."""
        desc = f" ({self.description})" if self.description else ""
        return f"{self.strategy}='{self.value}'{desc}"


# Convenience factory functions for common locator types
def x_by_id__mutmut_orig(value: str, description: str = "") -> Locator:
    """Create an ID locator."""
    return Locator("id", value, description)


# Convenience factory functions for common locator types
def x_by_id__mutmut_1(value: str, description: str = "XXXX") -> Locator:
    """Create an ID locator."""
    return Locator("id", value, description)


# Convenience factory functions for common locator types
def x_by_id__mutmut_2(value: str, description: str = "") -> Locator:
    """Create an ID locator."""
    return Locator(None, value, description)


# Convenience factory functions for common locator types
def x_by_id__mutmut_3(value: str, description: str = "") -> Locator:
    """Create an ID locator."""
    return Locator("id", None, description)


# Convenience factory functions for common locator types
def x_by_id__mutmut_4(value: str, description: str = "") -> Locator:
    """Create an ID locator."""
    return Locator("id", value, None)


# Convenience factory functions for common locator types
def x_by_id__mutmut_5(value: str, description: str = "") -> Locator:
    """Create an ID locator."""
    return Locator(value, description)


# Convenience factory functions for common locator types
def x_by_id__mutmut_6(value: str, description: str = "") -> Locator:
    """Create an ID locator."""
    return Locator("id", description)


# Convenience factory functions for common locator types
def x_by_id__mutmut_7(value: str, description: str = "") -> Locator:
    """Create an ID locator."""
    return Locator(
        "id",
        value,
    )


# Convenience factory functions for common locator types
def x_by_id__mutmut_8(value: str, description: str = "") -> Locator:
    """Create an ID locator."""
    return Locator("XXidXX", value, description)


# Convenience factory functions for common locator types
def x_by_id__mutmut_9(value: str, description: str = "") -> Locator:
    """Create an ID locator."""
    return Locator("ID", value, description)


x_by_id__mutmut_mutants: ClassVar[MutantDict] = {
    "x_by_id__mutmut_1": x_by_id__mutmut_1,
    "x_by_id__mutmut_2": x_by_id__mutmut_2,
    "x_by_id__mutmut_3": x_by_id__mutmut_3,
    "x_by_id__mutmut_4": x_by_id__mutmut_4,
    "x_by_id__mutmut_5": x_by_id__mutmut_5,
    "x_by_id__mutmut_6": x_by_id__mutmut_6,
    "x_by_id__mutmut_7": x_by_id__mutmut_7,
    "x_by_id__mutmut_8": x_by_id__mutmut_8,
    "x_by_id__mutmut_9": x_by_id__mutmut_9,
}


def by_id(*args, **kwargs):
    result = _mutmut_trampoline(
        x_by_id__mutmut_orig, x_by_id__mutmut_mutants, args, kwargs
    )
    return result


by_id.__signature__ = _mutmut_signature(x_by_id__mutmut_orig)
x_by_id__mutmut_orig.__name__ = "x_by_id"


def x_by_css__mutmut_orig(value: str, description: str = "") -> Locator:
    """Create a CSS selector locator."""
    return Locator("css", value, description)


def x_by_css__mutmut_1(value: str, description: str = "XXXX") -> Locator:
    """Create a CSS selector locator."""
    return Locator("css", value, description)


def x_by_css__mutmut_2(value: str, description: str = "") -> Locator:
    """Create a CSS selector locator."""
    return Locator(None, value, description)


def x_by_css__mutmut_3(value: str, description: str = "") -> Locator:
    """Create a CSS selector locator."""
    return Locator("css", None, description)


def x_by_css__mutmut_4(value: str, description: str = "") -> Locator:
    """Create a CSS selector locator."""
    return Locator("css", value, None)


def x_by_css__mutmut_5(value: str, description: str = "") -> Locator:
    """Create a CSS selector locator."""
    return Locator(value, description)


def x_by_css__mutmut_6(value: str, description: str = "") -> Locator:
    """Create a CSS selector locator."""
    return Locator("css", description)


def x_by_css__mutmut_7(value: str, description: str = "") -> Locator:
    """Create a CSS selector locator."""
    return Locator(
        "css",
        value,
    )


def x_by_css__mutmut_8(value: str, description: str = "") -> Locator:
    """Create a CSS selector locator."""
    return Locator("XXcssXX", value, description)


def x_by_css__mutmut_9(value: str, description: str = "") -> Locator:
    """Create a CSS selector locator."""
    return Locator("CSS", value, description)


x_by_css__mutmut_mutants: ClassVar[MutantDict] = {
    "x_by_css__mutmut_1": x_by_css__mutmut_1,
    "x_by_css__mutmut_2": x_by_css__mutmut_2,
    "x_by_css__mutmut_3": x_by_css__mutmut_3,
    "x_by_css__mutmut_4": x_by_css__mutmut_4,
    "x_by_css__mutmut_5": x_by_css__mutmut_5,
    "x_by_css__mutmut_6": x_by_css__mutmut_6,
    "x_by_css__mutmut_7": x_by_css__mutmut_7,
    "x_by_css__mutmut_8": x_by_css__mutmut_8,
    "x_by_css__mutmut_9": x_by_css__mutmut_9,
}


def by_css(*args, **kwargs):
    result = _mutmut_trampoline(
        x_by_css__mutmut_orig, x_by_css__mutmut_mutants, args, kwargs
    )
    return result


by_css.__signature__ = _mutmut_signature(x_by_css__mutmut_orig)
x_by_css__mutmut_orig.__name__ = "x_by_css"


def x_by_xpath__mutmut_orig(value: str, description: str = "") -> Locator:
    """Create an XPath locator."""
    return Locator("xpath", value, description)


def x_by_xpath__mutmut_1(value: str, description: str = "XXXX") -> Locator:
    """Create an XPath locator."""
    return Locator("xpath", value, description)


def x_by_xpath__mutmut_2(value: str, description: str = "") -> Locator:
    """Create an XPath locator."""
    return Locator(None, value, description)


def x_by_xpath__mutmut_3(value: str, description: str = "") -> Locator:
    """Create an XPath locator."""
    return Locator("xpath", None, description)


def x_by_xpath__mutmut_4(value: str, description: str = "") -> Locator:
    """Create an XPath locator."""
    return Locator("xpath", value, None)


def x_by_xpath__mutmut_5(value: str, description: str = "") -> Locator:
    """Create an XPath locator."""
    return Locator(value, description)


def x_by_xpath__mutmut_6(value: str, description: str = "") -> Locator:
    """Create an XPath locator."""
    return Locator("xpath", description)


def x_by_xpath__mutmut_7(value: str, description: str = "") -> Locator:
    """Create an XPath locator."""
    return Locator(
        "xpath",
        value,
    )


def x_by_xpath__mutmut_8(value: str, description: str = "") -> Locator:
    """Create an XPath locator."""
    return Locator("XXxpathXX", value, description)


def x_by_xpath__mutmut_9(value: str, description: str = "") -> Locator:
    """Create an XPath locator."""
    return Locator("XPATH", value, description)


x_by_xpath__mutmut_mutants: ClassVar[MutantDict] = {
    "x_by_xpath__mutmut_1": x_by_xpath__mutmut_1,
    "x_by_xpath__mutmut_2": x_by_xpath__mutmut_2,
    "x_by_xpath__mutmut_3": x_by_xpath__mutmut_3,
    "x_by_xpath__mutmut_4": x_by_xpath__mutmut_4,
    "x_by_xpath__mutmut_5": x_by_xpath__mutmut_5,
    "x_by_xpath__mutmut_6": x_by_xpath__mutmut_6,
    "x_by_xpath__mutmut_7": x_by_xpath__mutmut_7,
    "x_by_xpath__mutmut_8": x_by_xpath__mutmut_8,
    "x_by_xpath__mutmut_9": x_by_xpath__mutmut_9,
}


def by_xpath(*args, **kwargs):
    result = _mutmut_trampoline(
        x_by_xpath__mutmut_orig, x_by_xpath__mutmut_mutants, args, kwargs
    )
    return result


by_xpath.__signature__ = _mutmut_signature(x_by_xpath__mutmut_orig)
x_by_xpath__mutmut_orig.__name__ = "x_by_xpath"


def x_by_name__mutmut_orig(value: str, description: str = "") -> Locator:
    """Create a name attribute locator."""
    return Locator("name", value, description)


def x_by_name__mutmut_1(value: str, description: str = "XXXX") -> Locator:
    """Create a name attribute locator."""
    return Locator("name", value, description)


def x_by_name__mutmut_2(value: str, description: str = "") -> Locator:
    """Create a name attribute locator."""
    return Locator(None, value, description)


def x_by_name__mutmut_3(value: str, description: str = "") -> Locator:
    """Create a name attribute locator."""
    return Locator("name", None, description)


def x_by_name__mutmut_4(value: str, description: str = "") -> Locator:
    """Create a name attribute locator."""
    return Locator("name", value, None)


def x_by_name__mutmut_5(value: str, description: str = "") -> Locator:
    """Create a name attribute locator."""
    return Locator(value, description)


def x_by_name__mutmut_6(value: str, description: str = "") -> Locator:
    """Create a name attribute locator."""
    return Locator("name", description)


def x_by_name__mutmut_7(value: str, description: str = "") -> Locator:
    """Create a name attribute locator."""
    return Locator(
        "name",
        value,
    )


def x_by_name__mutmut_8(value: str, description: str = "") -> Locator:
    """Create a name attribute locator."""
    return Locator("XXnameXX", value, description)


def x_by_name__mutmut_9(value: str, description: str = "") -> Locator:
    """Create a name attribute locator."""
    return Locator("NAME", value, description)


x_by_name__mutmut_mutants: ClassVar[MutantDict] = {
    "x_by_name__mutmut_1": x_by_name__mutmut_1,
    "x_by_name__mutmut_2": x_by_name__mutmut_2,
    "x_by_name__mutmut_3": x_by_name__mutmut_3,
    "x_by_name__mutmut_4": x_by_name__mutmut_4,
    "x_by_name__mutmut_5": x_by_name__mutmut_5,
    "x_by_name__mutmut_6": x_by_name__mutmut_6,
    "x_by_name__mutmut_7": x_by_name__mutmut_7,
    "x_by_name__mutmut_8": x_by_name__mutmut_8,
    "x_by_name__mutmut_9": x_by_name__mutmut_9,
}


def by_name(*args, **kwargs):
    result = _mutmut_trampoline(
        x_by_name__mutmut_orig, x_by_name__mutmut_mutants, args, kwargs
    )
    return result


by_name.__signature__ = _mutmut_signature(x_by_name__mutmut_orig)
x_by_name__mutmut_orig.__name__ = "x_by_name"


def x_by_class__mutmut_orig(value: str, description: str = "") -> Locator:
    """Create a class name locator."""
    return Locator("class_name", value, description)


def x_by_class__mutmut_1(value: str, description: str = "XXXX") -> Locator:
    """Create a class name locator."""
    return Locator("class_name", value, description)


def x_by_class__mutmut_2(value: str, description: str = "") -> Locator:
    """Create a class name locator."""
    return Locator(None, value, description)


def x_by_class__mutmut_3(value: str, description: str = "") -> Locator:
    """Create a class name locator."""
    return Locator("class_name", None, description)


def x_by_class__mutmut_4(value: str, description: str = "") -> Locator:
    """Create a class name locator."""
    return Locator("class_name", value, None)


def x_by_class__mutmut_5(value: str, description: str = "") -> Locator:
    """Create a class name locator."""
    return Locator(value, description)


def x_by_class__mutmut_6(value: str, description: str = "") -> Locator:
    """Create a class name locator."""
    return Locator("class_name", description)


def x_by_class__mutmut_7(value: str, description: str = "") -> Locator:
    """Create a class name locator."""
    return Locator(
        "class_name",
        value,
    )


def x_by_class__mutmut_8(value: str, description: str = "") -> Locator:
    """Create a class name locator."""
    return Locator("XXclass_nameXX", value, description)


def x_by_class__mutmut_9(value: str, description: str = "") -> Locator:
    """Create a class name locator."""
    return Locator("CLASS_NAME", value, description)


x_by_class__mutmut_mutants: ClassVar[MutantDict] = {
    "x_by_class__mutmut_1": x_by_class__mutmut_1,
    "x_by_class__mutmut_2": x_by_class__mutmut_2,
    "x_by_class__mutmut_3": x_by_class__mutmut_3,
    "x_by_class__mutmut_4": x_by_class__mutmut_4,
    "x_by_class__mutmut_5": x_by_class__mutmut_5,
    "x_by_class__mutmut_6": x_by_class__mutmut_6,
    "x_by_class__mutmut_7": x_by_class__mutmut_7,
    "x_by_class__mutmut_8": x_by_class__mutmut_8,
    "x_by_class__mutmut_9": x_by_class__mutmut_9,
}


def by_class(*args, **kwargs):
    result = _mutmut_trampoline(
        x_by_class__mutmut_orig, x_by_class__mutmut_mutants, args, kwargs
    )
    return result


by_class.__signature__ = _mutmut_signature(x_by_class__mutmut_orig)
x_by_class__mutmut_orig.__name__ = "x_by_class"


def x_by_tag__mutmut_orig(value: str, description: str = "") -> Locator:
    """Create a tag name locator."""
    return Locator("tag_name", value, description)


def x_by_tag__mutmut_1(value: str, description: str = "XXXX") -> Locator:
    """Create a tag name locator."""
    return Locator("tag_name", value, description)


def x_by_tag__mutmut_2(value: str, description: str = "") -> Locator:
    """Create a tag name locator."""
    return Locator(None, value, description)


def x_by_tag__mutmut_3(value: str, description: str = "") -> Locator:
    """Create a tag name locator."""
    return Locator("tag_name", None, description)


def x_by_tag__mutmut_4(value: str, description: str = "") -> Locator:
    """Create a tag name locator."""
    return Locator("tag_name", value, None)


def x_by_tag__mutmut_5(value: str, description: str = "") -> Locator:
    """Create a tag name locator."""
    return Locator(value, description)


def x_by_tag__mutmut_6(value: str, description: str = "") -> Locator:
    """Create a tag name locator."""
    return Locator("tag_name", description)


def x_by_tag__mutmut_7(value: str, description: str = "") -> Locator:
    """Create a tag name locator."""
    return Locator(
        "tag_name",
        value,
    )


def x_by_tag__mutmut_8(value: str, description: str = "") -> Locator:
    """Create a tag name locator."""
    return Locator("XXtag_nameXX", value, description)


def x_by_tag__mutmut_9(value: str, description: str = "") -> Locator:
    """Create a tag name locator."""
    return Locator("TAG_NAME", value, description)


x_by_tag__mutmut_mutants: ClassVar[MutantDict] = {
    "x_by_tag__mutmut_1": x_by_tag__mutmut_1,
    "x_by_tag__mutmut_2": x_by_tag__mutmut_2,
    "x_by_tag__mutmut_3": x_by_tag__mutmut_3,
    "x_by_tag__mutmut_4": x_by_tag__mutmut_4,
    "x_by_tag__mutmut_5": x_by_tag__mutmut_5,
    "x_by_tag__mutmut_6": x_by_tag__mutmut_6,
    "x_by_tag__mutmut_7": x_by_tag__mutmut_7,
    "x_by_tag__mutmut_8": x_by_tag__mutmut_8,
    "x_by_tag__mutmut_9": x_by_tag__mutmut_9,
}


def by_tag(*args, **kwargs):
    result = _mutmut_trampoline(
        x_by_tag__mutmut_orig, x_by_tag__mutmut_mutants, args, kwargs
    )
    return result


by_tag.__signature__ = _mutmut_signature(x_by_tag__mutmut_orig)
x_by_tag__mutmut_orig.__name__ = "x_by_tag"


def x_by_link_text__mutmut_orig(value: str, description: str = "") -> Locator:
    """Create a link text locator."""
    return Locator("link_text", value, description)


def x_by_link_text__mutmut_1(value: str, description: str = "XXXX") -> Locator:
    """Create a link text locator."""
    return Locator("link_text", value, description)


def x_by_link_text__mutmut_2(value: str, description: str = "") -> Locator:
    """Create a link text locator."""
    return Locator(None, value, description)


def x_by_link_text__mutmut_3(value: str, description: str = "") -> Locator:
    """Create a link text locator."""
    return Locator("link_text", None, description)


def x_by_link_text__mutmut_4(value: str, description: str = "") -> Locator:
    """Create a link text locator."""
    return Locator("link_text", value, None)


def x_by_link_text__mutmut_5(value: str, description: str = "") -> Locator:
    """Create a link text locator."""
    return Locator(value, description)


def x_by_link_text__mutmut_6(value: str, description: str = "") -> Locator:
    """Create a link text locator."""
    return Locator("link_text", description)


def x_by_link_text__mutmut_7(value: str, description: str = "") -> Locator:
    """Create a link text locator."""
    return Locator(
        "link_text",
        value,
    )


def x_by_link_text__mutmut_8(value: str, description: str = "") -> Locator:
    """Create a link text locator."""
    return Locator("XXlink_textXX", value, description)


def x_by_link_text__mutmut_9(value: str, description: str = "") -> Locator:
    """Create a link text locator."""
    return Locator("LINK_TEXT", value, description)


x_by_link_text__mutmut_mutants: ClassVar[MutantDict] = {
    "x_by_link_text__mutmut_1": x_by_link_text__mutmut_1,
    "x_by_link_text__mutmut_2": x_by_link_text__mutmut_2,
    "x_by_link_text__mutmut_3": x_by_link_text__mutmut_3,
    "x_by_link_text__mutmut_4": x_by_link_text__mutmut_4,
    "x_by_link_text__mutmut_5": x_by_link_text__mutmut_5,
    "x_by_link_text__mutmut_6": x_by_link_text__mutmut_6,
    "x_by_link_text__mutmut_7": x_by_link_text__mutmut_7,
    "x_by_link_text__mutmut_8": x_by_link_text__mutmut_8,
    "x_by_link_text__mutmut_9": x_by_link_text__mutmut_9,
}


def by_link_text(*args, **kwargs):
    result = _mutmut_trampoline(
        x_by_link_text__mutmut_orig, x_by_link_text__mutmut_mutants, args, kwargs
    )
    return result


by_link_text.__signature__ = _mutmut_signature(x_by_link_text__mutmut_orig)
x_by_link_text__mutmut_orig.__name__ = "x_by_link_text"


def x_by_partial_link_text__mutmut_orig(value: str, description: str = "") -> Locator:
    """Create a partial link text locator."""
    return Locator("partial_link_text", value, description)


def x_by_partial_link_text__mutmut_1(value: str, description: str = "XXXX") -> Locator:
    """Create a partial link text locator."""
    return Locator("partial_link_text", value, description)


def x_by_partial_link_text__mutmut_2(value: str, description: str = "") -> Locator:
    """Create a partial link text locator."""
    return Locator(None, value, description)


def x_by_partial_link_text__mutmut_3(value: str, description: str = "") -> Locator:
    """Create a partial link text locator."""
    return Locator("partial_link_text", None, description)


def x_by_partial_link_text__mutmut_4(value: str, description: str = "") -> Locator:
    """Create a partial link text locator."""
    return Locator("partial_link_text", value, None)


def x_by_partial_link_text__mutmut_5(value: str, description: str = "") -> Locator:
    """Create a partial link text locator."""
    return Locator(value, description)


def x_by_partial_link_text__mutmut_6(value: str, description: str = "") -> Locator:
    """Create a partial link text locator."""
    return Locator("partial_link_text", description)


def x_by_partial_link_text__mutmut_7(value: str, description: str = "") -> Locator:
    """Create a partial link text locator."""
    return Locator(
        "partial_link_text",
        value,
    )


def x_by_partial_link_text__mutmut_8(value: str, description: str = "") -> Locator:
    """Create a partial link text locator."""
    return Locator("XXpartial_link_textXX", value, description)


def x_by_partial_link_text__mutmut_9(value: str, description: str = "") -> Locator:
    """Create a partial link text locator."""
    return Locator("PARTIAL_LINK_TEXT", value, description)


x_by_partial_link_text__mutmut_mutants: ClassVar[MutantDict] = {
    "x_by_partial_link_text__mutmut_1": x_by_partial_link_text__mutmut_1,
    "x_by_partial_link_text__mutmut_2": x_by_partial_link_text__mutmut_2,
    "x_by_partial_link_text__mutmut_3": x_by_partial_link_text__mutmut_3,
    "x_by_partial_link_text__mutmut_4": x_by_partial_link_text__mutmut_4,
    "x_by_partial_link_text__mutmut_5": x_by_partial_link_text__mutmut_5,
    "x_by_partial_link_text__mutmut_6": x_by_partial_link_text__mutmut_6,
    "x_by_partial_link_text__mutmut_7": x_by_partial_link_text__mutmut_7,
    "x_by_partial_link_text__mutmut_8": x_by_partial_link_text__mutmut_8,
    "x_by_partial_link_text__mutmut_9": x_by_partial_link_text__mutmut_9,
}


def by_partial_link_text(*args, **kwargs):
    result = _mutmut_trampoline(
        x_by_partial_link_text__mutmut_orig,
        x_by_partial_link_text__mutmut_mutants,
        args,
        kwargs,
    )
    return result


by_partial_link_text.__signature__ = _mutmut_signature(
    x_by_partial_link_text__mutmut_orig
)
x_by_partial_link_text__mutmut_orig.__name__ = "x_by_partial_link_text"
