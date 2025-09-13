# PMAS - Python Modern Automation Suite

[![CI](https://github.com/aurichalcite/pmas/workflows/CI/badge.svg)](https://github.com/aurichalcite/pmas/actions)
[![Security](https://github.com/aurichalcite/pmas/workflows/Security/badge.svg)](https://github.com/aurichalcite/pmas/actions)
[![PyPI version](https://badge.fury.io/py/pmas.svg)](https://badge.fury.io/py/pmas)
[![Python versions](https://img.shields.io/pypi/pyversions/pmas.svg)](https://pypi.org/project/pmas/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A modern, reusable, domain-agnostic Web UI testing framework built on Python 3.11+ and Selenium 4+. PMAS provides a clean architecture that separates core testing logic from domain-specific application logic, making it easy to create maintainable and scalable test suites.

## 🚀 Key Features

### **Modern Architecture**
- **Domain-Agnostic Core**: Clean separation between framework and domain logic
- **Type-Safe**: Full type hints and mypy support for better IDE experience
- **Protocol-Based**: Flexible interfaces that hide implementation details
- **Dependency Injection**: Configurable components for easy testing and extension

### **Developer Experience**
- **Python 3.11+**: Modern Python features and performance improvements
- **Selenium 4+**: Latest WebDriver capabilities with enhanced stability
- **Rich Configuration**: TOML files, environment variables, and CLI arguments
- **Comprehensive Logging**: Structured logging with configurable levels and formats

### **Testing Capabilities**
- **pytest Integration**: Native fixtures, parametrization, and reporting
- **Soft Assertions**: Continue test execution after assertion failures
- **Data-Driven Testing**: Built-in CSV, JSON, and YAML data readers
- **Cross-Browser Support**: Chrome, Firefox, Edge with local and remote execution
- **Failure Artifacts**: Automatic screenshot and log capture on failures

### **Domain Support**
- **Aviation Domain**: Flight planning, weather, and aviation-specific workflows
- **Manufacturing Domain**: Production planning, quality control, and manufacturing workflows
- **Extensible**: Easy to add new domains with provided patterns and examples

## 📦 Installation

### Requirements
- Python 3.11 or higher
- Chrome, Firefox, or Edge browser
- WebDriver (automatically managed with webdriver-manager)

### Install from PyPI
```bash
pip install pmas
```

### Install from Source
```bash
git clone https://github.com/aurichalcite/pmas.git
cd pmas
pip install -e .
```

### Development Installation
```bash
git clone https://github.com/aurichalcite/pmas.git
cd pmas
pip install -e ".[dev]"
```

## 🏃‍♂️ Quick Start

### 1. Basic Page Object
```python
from pmas import BasePage, by_id, by_class_name

class LoginPage(BasePage):
    # Define locators with type safety
    USERNAME_FIELD = by_id('username', 'Username input field')
    PASSWORD_FIELD = by_id('password', 'Password input field')
    LOGIN_BUTTON = by_class_name('login-btn', 'Login button')

    def login(self, username: str, password: str):
        # Type-safe element interactions
        username_field = self.get_text_input(self.USERNAME_FIELD)
        password_field = self.get_text_input(self.PASSWORD_FIELD)
        login_button = self.get_button(self.LOGIN_BUTTON)

        username_field.type_text(username)
        password_field.type_text(password)
        login_button.click()
```

### 2. Configuration-Driven Test
```python
import pytest
from pmas import Config, DriverFactory
from pmas.testing import SoftAssertions

def test_login_functionality(config: Config):
    # Framework handles driver creation and cleanup
    with DriverFactory.create_driver(config.browser) as driver:
        login_page = LoginPage(driver, config.environment.base_url)
        login_page.navigate_to()

        # Soft assertions continue test execution after failures
        with SoftAssertions() as soft:
            soft.assert_true(login_page.verify_page_loaded())
            login_page.login("testuser", "testpass")
            soft.assert_true("dashboard" in driver.current_url)
```

### 3. Data-Driven Testing
```python
from pmas.data import parametrize_from_csv

@parametrize_from_csv("test_data/login_scenarios.csv")
def test_login_scenarios(config, driver, username, password, expected_result):
    login_page = LoginPage(driver, config.environment.base_url)
    login_page.navigate_to()

    if expected_result == "success":
        login_page.login(username, password)
        assert "dashboard" in driver.current_url
    else:
        with pytest.raises(Exception):
            login_page.login(username, password)
```

## ⚙️ Configuration

PMAS uses a layered configuration system with the following precedence:
1. Command-line arguments (highest priority)
2. Environment variables
3. TOML configuration files
4. Default values (lowest priority)

### Example `pmas.toml`
```toml
[environment]
base_url = "https://your-app.com"
name = "staging"

[browser]
name = "chrome"
headless = false
window_size = [1920, 1080]

[test]
default_timeout = 10.0
screenshot_on_failure = true
soft_assertions = true

[logging]
level = "INFO"
file_path = "logs/pmas.log"
```

### Environment Variables
```bash
export PMAS_BROWSER_NAME=firefox
export PMAS_BROWSER_HEADLESS=true
export PMAS_TEST_DEFAULT_TIMEOUT=30
```

### Command Line
```bash
pytest --browser chrome --headless --timeout 20
```

## 🏗️ Architecture

PMAS follows a layered architecture that promotes separation of concerns and maintainability:

```
┌─────────────────────────────────────────────────────────────┐
│                     Domain Layer                            │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐  │
│  │   Aviation      │  │   Manufacturing     │  │   Custom    │  │
│  │   Domain        │  │   Domain        │  │   Domain    │  │
│  └─────────────────┘  └─────────────────┘  └─────────────┘  │
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│                    Testing Layer                            │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐  │
│  │   Fixtures      │  │   Assertions    │  │   Reporting │  │
│  └─────────────────┘  └─────────────────┘  └─────────────┘  │
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│                     Core Layer                              │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐  │
│  │   Page Objects  │  │   Elements      │  │   Locators  │  │
│  └─────────────────┘  └─────────────────┘  └─────────────┘  │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐  │
│  │   Driver        │  │   Config        │  │   Data      │  │
│  └─────────────────┘  └─────────────────┘  └─────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Core Components

- **Driver Factory**: WebDriver creation and management with protocol-based interfaces
- **Page Objects**: Base classes for creating maintainable page representations
- **Element Abstractions**: Type-safe wrappers for common web elements
- **Locator System**: Flexible element location with built-in descriptions
- **Configuration**: Multi-source configuration with validation and type safety

### Domain Adapters

- **Aviation**: Flight planning, weather briefings, and aviation workflows
- **Manufacturing**: Production planning, quality control, and manufacturing processes
- **Extensible**: Template and patterns for creating new domain adapters

## 📚 Examples

### SauceDemo Examples
Complete working examples using the SauceDemo application:

```bash
cd src/pmas/examples/demo_site
pytest tests/ -v
```

Features demonstrated:
- Login workflows with different user types
- Shopping cart management
- End-to-end purchase flows
- Data-driven testing with multiple scenarios
- Error handling and validation

### Domain Examples

#### Aviation Domain
```python
from pmas.domains.aviation import AviationLoginAdapter, FlightPlanAdapter

# Login and create flight plan
login_adapter = AviationLoginAdapter(driver, config)
flight_adapter = FlightPlanAdapter(driver, config)

# Login as flight coordinator
page = login_adapter.login_as_flight_coordinator()

# Create flight plan
flight_data = FlightPlanData(
    tail_number="N123AB",
    departure="KJFK",
    arrival="KLAX",
    departure_time="14:00",
    passengers=4
)
result = flight_adapter.create_flight_plan(flight_data)
```

#### Manufacturing Domain
```python
from pmas.domains.manufacturing import ManufacturingLoginAdapter, ProductionOrderAdapter

# Login and create production order
login_adapter = ManufacturingLoginAdapter(driver, config)
production_adapter = ProductionOrderAdapter(driver, config)

# Login as production planner
page = login_adapter.login_as_production_planner()

# Create production order
order_data = ProductionOrderData(
    production_line_id="CNC-001",
    source_factory="FAC01",
    destination_warehouse="WAR01",
    order_quantity=100,
    material_type="WOOD"
)
result = production_adapter.create_production_order(order_data)
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with specific browser
pytest --browser firefox

# Run in headless mode
pytest --headless

# Run with custom configuration
pytest --config custom_pmas.toml

# Run specific test categories
pytest -m "not slow"  # Skip slow tests
pytest -m "smoke"     # Run only smoke tests
```

### Test Organization

```
tests/
├── unit/                   # Unit tests for framework components
├── integration/            # Integration tests with real browsers
├── examples/              # Example application tests
└── conftest.py           # Shared pytest configuration
```

### Writing Tests

```python
import pytest
from pmas.testing import SoftAssertions

class TestUserWorkflow:
    def test_complete_user_journey(self, driver, config):
        """Test complete user workflow with soft assertions."""
        with SoftAssertions() as soft:
            # Multiple assertions that don't stop test execution
            soft.assert_true(condition1, "Step 1 should pass")
            soft.assert_equal(actual, expected, "Step 2 validation")
            soft.assert_contains(text, "error", "Error message check")

    @pytest.mark.parametrize("browser", ["chrome", "firefox"])
    def test_cross_browser_compatibility(self, browser, config):
        """Test across multiple browsers."""
        # Test implementation
        pass
```

## 🔧 Development

### Setting Up Development Environment

```bash
# Clone repository
git clone https://github.com/aurichalcite/pmas.git
cd pmas

# Install with development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Run tests
pytest tests/

# Run linting
ruff check src/ tests/
ruff format src/ tests/

# Run type checking
mypy src/
```

### Project Structure

```
pmas/
├── src/pmas/              # Main package
│   ├── core/             # Core framework components
│   ├── config/           # Configuration system
│   ├── testing/          # Testing utilities
│   ├── data/             # Data-driven testing
│   ├── domains/          # Domain-specific adapters
│   └── examples/         # Example implementations
├── tests/                # Test suite
├── docs/                 # Documentation
├── .github/              # GitHub workflows and templates
├── pyproject.toml        # Project configuration
└── README.md            # This file
```

### Contributing

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** with tests and documentation
4. **Run the test suite**: `pytest`
5. **Run linting**: `ruff check . && ruff format .`
6. **Commit your changes**: `git commit -m 'Add amazing feature'`
7. **Push to the branch**: `git push origin feature/amazing-feature`
8. **Open a Pull Request**

### Code Quality

- **Type Hints**: All public APIs must have type hints
- **Documentation**: Public methods require docstrings
- **Testing**: New features require tests with >90% coverage
- **Linting**: Code must pass ruff checks
- **Formatting**: Code must be formatted with ruff

## 📖 Documentation

- **[API Reference](docs/api/)**: Complete API documentation
- **[User Guide](docs/guide/)**: Step-by-step tutorials and guides
- **[Domain Guide](docs/domains/)**: Creating custom domain adapters
- **[Migration Guide](docs/migration/)**: Upgrading from legacy frameworks
- **[Examples](src/pmas/examples/)**: Working code examples

## 🚀 Migration from Legacy Framework

PMAS provides migration utilities and backward compatibility shims for existing test suites:

### Automated Migration
```bash
# Run migration tool
python -m pmas.migration.migrate_legacy --source legacy_tests/ --target new_tests/

# Validate migration
python -m pmas.migration.validate --path new_tests/
```

### Manual Migration Steps
1. **Update imports**: Replace legacy imports with PMAS equivalents
2. **Convert page objects**: Use new base classes and locator system
3. **Update configuration**: Convert to TOML-based configuration
4. **Modernize tests**: Use pytest fixtures and soft assertions

See the [Migration Guide](docs/migration/README.md) for detailed instructions.

## 🤝 Community

- **GitHub Issues**: [Report bugs and request features](https://github.com/aurichalcite/pmas/issues)
- **Discussions**: [Ask questions and share ideas](https://github.com/aurichalcite/pmas/discussions)
- **Contributing**: [Contribution guidelines](CONTRIBUTING.md)
- **Code of Conduct**: [Community standards](CODE_OF_CONDUCT.md)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Selenium Project**: For providing the WebDriver foundation
- **pytest**: For the excellent testing framework
- **Community Contributors**: For feedback, bug reports, and contributions

---

**PMAS** - Making Web UI testing modern, maintainable, and enjoyable! 🎉
| ==AIRPORT = %RED%Loc.text%ENDCOLOR%(%GREEN%By.ID%ENDCOLOR%, %BLUE%"Airport"%ENDCOLOR%)==  | *%RED%Text input box%ENDCOLOR%* %GREEN%by id%ENDCOLOR% %BLUE%"Airport"%ENDCOLOR% | =ALIAS.AIRPORT= |
| ==RADIO = %RED%Loc.radio%ENDCOLOR%(%GREEN%By.NAME%ENDCOLOR%, %BLUE%"sat_radio"%ENDCOLOR%)==  | *%RED%radio%ENDCOLOR%* %GREEN%by name%ENDCOLOR% %BLUE%"sat_radio"%ENDCOLOR% | =ALIAS.RADIO= |
| ==ERROR = %RED%Loc.asset%ENDCOLOR%(%GREEN%By.CLASS_NAME%ENDCOLOR%, %BLUE%"warning"%ENDCOLOR%)== | *%RED%asset%ENDCOLOR%* %GREEN%by name of CSS class%ENDCOLOR% %BLUE%"warning"%ENDCOLOR% | =ALIAS.ERROR= |

Or, submit button located by a fancy CSS (2 levels deep from the Id):

==SUBMIT = %RED%Loc.asset%ENDCOLOR%(%GREEN%By.CSS_SELECTOR%ENDCOLOR%, %BLUE%"#arinc_messenger_form > div.message_submit > button" %ENDCOLOR%)==

---+ Locators: use in code

| =&lt;pageobject>.fill({ALIAS.AIRPORT:'KJFK'})= | fill alias AIRPORT with value ='JFK'= |
| =&lt;pageobject>.click(ALIAS.SUMBIT)= | click on button with alias =SUBMIT= |
| =&lt;pageobject>.wait_until_stale(ALIAS.SUBMIT)= | wait until button SUBMIT gets stale |

---+ Locators: Data types

*Locator Datatypes:*

   * 3 simple data types: Loc.text(), Loc.radio(), Loc.checkbox(),
   * 3 types of dropdown: Loc.dropdown(), Loc,droptext(), Loc.dropsend()
   * Loc.asset() - if you just need to find the element (not filling any value), like button or error message.

   * See ==page/base_loc.py== for all options for *%RED%data type%ENDCOLOR%*.
   * See ==page/base_elements.py== to see how ==fill()== uses data types (will click on assets)

---+ Locators: dynamic elements

Define *pattern for dynamic locator* with parameter %RED%%s%ENDCOLOR% (a checkbox):

==DYNAMIC = Locators(dict( %GREEN%SELECT%ENDCOLOR%=Loc.checkbox(By.ID, 'select_%RED%%s%ENDCOLOR%') ))==

Create dynamic locator according to pattern:

==dynamic_element=%BLUE%Loc.make%ENDCOLOR%(%GREEN%DYNAMIC.SELECT%ENDCOLOR%, %RED%recall%ENDCOLOR%)==

Optional: Dynamic locators might be stored in separate object (not ALIAS), because are used differently.

---+ Locators: dynamic elements example

Create list of checkbox locators from pattern and recall numbers, then fill them:
<verbatim>
DYNAMIC = Locators(dict(
   SELECT=Loc.checkbox(By.ID, 'select_%s'), # add recall later
))
checkboxes = odict()
for recall in recalls:  
    checkboxes[Loc.make(DYNAMIC.SELECT, recall)] = True
self.fill(checkboxes)</verbatim>


---+ Locate-By strategies

In order of preference:

By.ID > By.NAME > By.CSS_SELECTOR >  By.TAG_NAME > By.XPATH


   * By.LINK_TEXT > By.PARTIAL_LINK_TEXT > By.CLASS_NAME - are possible, but *[[https://blog.mozilla.org/webqa/2012/07/12/how-to-webdriverwait/][waiting for attributes]] %RED%is not reliable%ENDCOLOR%*
   *  *Waiting for a new node to be present is safer than waiting for an existing one to have changed* (attribute, text, class etc). Change relies on the element being stable inside !WebDriver’s element cache.

   * [[http://sauceio.com/index.php/tag/css-selectors/][XPATH should be avoided]]: use CSS_SELECTOR instead - [[http://www.w3schools.com/cssref/css_selectors.asp][reference]]

---+ Selenium !WebDriver in ARINC Direct

1) [[SeleniumStackWindows][Install]] Selenium on your Windows desktop - or use pre-configured VM

2) Client code is already installed on devbox:
   * Centos System libraries: =/usr/lib/python2.6/site-packages/selenium=
   * Arch System libraries: =/usr/lib/python2.6/site-packages/selenium2=
   * Tests and pageobjects: =adc_test/webdriver=

   * ==%RED%se2%ENDCOLOR%==  (in =test_tools= ) sets aliases: ==%RED%se2p%ENDCOLOR%== to pageobjects, ==%RED%se2t%ENDCOLOR%== to tests, etc
   * %FIXME% another one is in =/adc_test/scripts= - need to settle on one

---+ Required reading

   * SeleniumTests101 - detailed explanation of locators, basic operations and example of use
   * in =page= directory (pageobjects):
      * =base_elements, base_page, common_page=
   * In =webdrivertests= directory (test examples):
      * =base_test, test_Login, test_Alerts, cmp_TxtWeather_PROD.py=
   * Advanced magic: =prod_fpl.py=
      * reads a JSON copy of FPL from PROD, creates locator/value pairs to file exactly same plan in SAT

---+ More info

   * [[Selenium]] - main page for Selenium in SQA wiki
   * SeleniumTests101 - how to write test, with examples
   * SeleniumPageObject - what this design pattern is, why it is good fit
   * SeleniumWait - how to wait correctly (wrappers in =base_elements= page)
      * Hint: avoid =sleep()= if you can, use different =ExpectedConditions=
   * SeleniumTips - best practices, tricks to solve common problems
   * WritingSeleniumTests

%SLIDESHOWEND%

%CTOC%

---+ Main design pattern: Pageobject

   * *Test* ask pageobject to perform actions and makes assertion on the results.
   * [[SeleniumPageObject][Pageobject ]] - provides services for test, but hides details (like locators) and makes few assertions.
      * only asserting page invariants (independent of any data), like: Is page title correct? Was date widget pre-filled with current date?
      * separate test (business) logic (*%RED%WHAT+WHY%ENDCOLOR%*) from page interaction (*%RED%HOW%ENDCOLOR%*)
   * *You're Doing It Wrong* if you have locators or !WebDriver APIs in your tests
      * You *can* start with locators and assets in test as a quick-and-dirty shortcut, but when (not if) you want to reuse functionality, you will have to refactor it to a !PageObject anyway
   * pageobjects live in =adc_test/webdriver/page= directory, use ==se2p==
   * result of navigation is another pageobject (new page)
   * [[SeleniumWait][Waiting is tricky]] (but mostly hidden in =base_page=). Selenium has powerful helper class !ExpectedConditions (EC).
   * Complicated pages (like Create FPL) might have more than one pageobject .py file, to separate locators for different accordions.

---+ Basic terminology (internal, my own):

See [[Selenium101][Selenium 101 presentation]] - in colors. *Especially slides 11-18*.
   * *Alias* - name of locator in code. Collection of alias objects can have any name, ALIAS is used for consistency.
   * *Locator Data Types* - rough equivalent of HTML input data types.
   * *Locating strategy* (BY.ID, By.NAME, By.CSS_SELECTOR, ...)
      * Avoid XPATH, it is flaky (unreliable, works on and off), brittle (easy to break with trivial design change) and slow.
      * Avoid [[https://blog.mozilla.org/webqa/2012/07/12/how-to-webdriverwait/][wait on attributes like class, text]]
   * *Argument* (string for locating strategy)

 
---+ Declare aliases

%SUMMARY%Declare alias collection:
   * ALIAS - for static locators  %ENDSUMM%

Alias names are in uppercase because they are "constants".

==Loc.asset== is something we can locate, maybe to check for presence/visibility, click or read text out of it, but cannot be used in =fill()= to input data.

<verbatim>
# page.tankering.py
from page.base_page import BasePage, By, Loc, Locators
ALIAS = Locators(dict(
   BEGIN_FUEL =Loc.text(By.ID, 'current_fob'),
   ERROR      =Loc.asset(By.CLASS_NAME, 'error-message'),
   MULTIPAGE  =Loc.asset(By.ID, 'page_links'),
   NEXT_BUTTON=Loc.asset(By.ID, 'computeButton'),
   TAIL_NUMBER=Loc.droptext(By.ID, "tail_number"),
))</verbatim>

---+ Fill widgets with values

%SUMMARY%Fill tail number and date%ENDSUMM%

<verbatim>self.fill({ALIAS.TAIL_NUMBER:tail, ALIAS.DATE_FROM:from_date})
</verbatim>

---+ Check for optional widget, find and click

%SUMMARY%
   * Check if "multipage" is present,
   * click on "show all" button to show all pages.
%ENDSUMM%

=are_present()= does not wait, but returns empty list if located element is not present.

<verbatim>multipage = self.are_present(ALIAS.MULTIPAGE)
if multipage and multipage[0].is_displayed():
       self.click(ALIAS.SHOW_ALL)
</verbatim>

---+ Create and use dynamic elements
%SUMMARY%
   * PREFIX - collection of aliases for dynamically generated locators (by adding recall).
   * Loop over provided parameter (list of recalls),
   * create locators (checkboxes) for requested recalls, and
   * click on those dynamically generated checkbox locators
%ENDSUMM%

Having two collections is just safe programming (ALIAS can be used as-is, PREFIX needs a parameter to create dynamic locator), see example later.

<verbatim>
PREFIX = Locators(dict(
   SELECT=Loc.checkbox(By.ID, 'select_%s'), # checkbox to select recall number
))
checkboxes = odict()
for recall in recalls:
    # create new locator from prefix and recall number
    checkboxes[Loc.make(PREFIX.SELECT, recall)] = True
self.fill(checkboxes, log=False)
</verbatim>

---+ Example test: File flight plan
%SUMMARY%File flight between two given airports one hour from now - like needed for Alerts

=data.flight_plan= is helper module to build flight plans
   * =simple_flight()= builds input params to fill flight for tail, from/to
   * =departure()= builds departure date and time
%ENDSUMM%
<verbatim>
def file_plan(self, fpl_page, ap_from, ap_to):
    fpl_page.enter_plan(data.flight_plan.simple_flight(ARGS.tail, ap_from, ap_to))
    fpl_page.enter_departure(data.flight_plan.departure(0, False)) # today hour from now
    ncfpl_page = fpl_page.submit_plan() # opens popup compute_fpl page
    fpl_page.to_popup_window()
    self.assert_page(ncfpl_page, 'NewComputedFlightPlan')
    ncfpl_page.file_fpl(ARGS.tail, finish_filing=True) # finish without WB/perf
</verbatim>

Then, cleanup/close popups, check that recall on Filing Status page is filled.
<verbatim>
    fpl_page.wait_close_popups() # force closing ALL popups
    fpl_page.check_title() # check all popups were closed, back in FPL page
    print 'check filled recall number [%s] in Filing Status' % ncfpl_page.recall
    fstat_page = fpl_page.goto_tab(tab.FPL_FILING_STATUS)
    self.assert_page(fstat_page, 'Filing Status')
    fstat_page.check_recall_filed(ARGS.tail, ncfpl_page.recall, True)
    print 'filled OK'
    return fstat_page, ncfpl_page.recall
</verbatim>

---+ Utility methods for !PageObject
   * see =base_page= and =base_elements= for full list
   * most methods log the performed action, unless silenced by ==log=False==
   * =tprint()= - prints message in format like log
   * =voodoo()= - mark sleep which should be eventually replaced by properly waiting for something. Total of all voodoo waits is reported.

   * ==se2== sets up environment, see [[Selenium101]] slide 13

---+ Tests

   * tests live in =adc_test/webdriver/webdrivertests= directory, use ==se2t==
   * Tests are based on =BaseTest= in  =base_test.py= which is based on unittest.TestCase
   * Every =test_xx()= method starts fresh new browser instance with new profile (no cache), which can take from ~10 sec (Chrome) to ~30 sec (FF). So often every test has only a single =test_xx()= "golden path" through the test.
   * Also, temp files from profiles are left behind in temp directory (needs occasional cleanup).
   * Browser can be closed or left open (configuration param). Open browser makes easier debugging but *will* leak RAM. Selenium will close old browser instances but not clear RAM, so I got used to close browsers windows I do not need anymore.
   * For flexibility, I often add commandline parameters, populating global ARGS using  =argparse.ArgumentParser= in =parse_args()=
   * Different parts of functionality can be tested in several =try_xx()= called from the main =test_xx()= - and each can be commented/uncommented quickly to bypass parts to be skipped. !E2E test are *slow* so when developing, you want quickly comment/uncomment running different parts.

---+ Good examples
   * =test_Login.py= - basic login
      * advanced: =test_scenario()=: make valid/invalid logins multiple times, to test lockout on bad login, and expiration of such lockout
   * =test_CreateFPL.py= - file random flight plan in USA
   * =test_Alerts.py= - If no recall is provided on commandline, will file FPL and use that to check alerts. For repeated runs, you can reuse recall for substantial time saving.
   * =test_Tankering.py= - advanced example (showcase of power of !Webdriver over !FitNesse):
      * use lists and dictionaries literals to define parameters of test scenarios
      * pick one scenario, create connected flight plans, and pickle resulting recall numbers, print generated pickle name
      * In following runs, unpickle recalls, fill tankering page.
