# SauceDemo Examples

This directory contains example tests demonstrating the PMAS framework capabilities using the [SauceDemo](https://www.saucedemo.com) application.

## Overview

The examples showcase:

- **Modern Page Object Pattern**: Clean, maintainable page objects using PMAS core components
- **Robust Element Interactions**: Type-safe element abstractions with built-in waits
- **Configuration Management**: Environment-specific configuration using TOML
- **Data-Driven Testing**: Parameterized tests with multiple scenarios
- **Soft Assertions**: Comprehensive validation without early test termination
- **Error Handling**: Graceful failure handling with detailed reporting

## Structure

```
demo_site/
├── pages/                  # Page object classes
│   ├── __init__.py
│   ├── login_page.py      # Login page object
│   ├── inventory_page.py  # Product inventory page
│   ├── cart_page.py       # Shopping cart page
│   └── checkout_page.py   # Checkout process pages
├── tests/                 # Test classes
│   ├── test_login.py      # Login functionality tests
│   └── test_shopping_workflow.py  # End-to-end shopping tests
├── pmas.toml             # PMAS configuration
└── README.md             # This file
```

## Page Objects

### LoginPage
Demonstrates:
- Form interaction with username/password fields
- Error message handling and validation
- Multiple user type support
- Credential management

### InventoryPage  
Demonstrates:
- Dynamic element location using templates
- List operations (getting all items)
- State management (cart item count)
- Navigation between pages
- Sorting and filtering

### CartPage
Demonstrates:
- Cart item management
- Price calculations
- Conditional logic (empty cart handling)
- Cross-page data consistency

### CheckoutPage
Demonstrates:
- Multi-step workflow handling
- Form validation
- Order summary verification
- Process completion confirmation

## Test Examples

### Login Tests (`test_login.py`)
- **Successful login scenarios**: Different user types
- **Validation testing**: Empty fields, invalid credentials
- **Error handling**: Locked out users, error message dismissal
- **Parameterized testing**: Multiple login scenarios in one test
- **Soft assertions**: Multiple validations without early termination

### Shopping Workflow Tests (`test_shopping_workflow.py`)
- **End-to-end workflows**: Complete shopping process from login to checkout
- **Cart management**: Adding/removing items, cart persistence
- **Inventory operations**: Sorting, item selection
- **Checkout process**: Form filling, validation, completion
- **Edge cases**: Empty cart, missing information, cancellation

## Running the Examples

### Prerequisites

1. **Install PMAS framework**:
   ```bash
   pip install -e .
   ```

2. **Install browser drivers**:
   ```bash
   # Chrome (recommended)
   pip install webdriver-manager
   
   # Or manually download ChromeDriver and add to PATH
   ```

### Running Tests

1. **Navigate to the examples directory**:
   ```bash
   cd src/pmas/examples/demo_site
   ```

2. **Run all tests**:
   ```bash
   pytest tests/ -v
   ```

3. **Run specific test file**:
   ```bash
   pytest tests/test_login.py -v
   pytest tests/test_shopping_workflow.py -v
   ```

4. **Run with different browsers**:
   ```bash
   # Firefox
   pytest tests/ -v --browser firefox
   
   # Edge
   pytest tests/ -v --browser edge
   
   # Headless mode
   pytest tests/ -v --headless
   ```

5. **Run with custom configuration**:
   ```bash
   pytest tests/ -v --config custom_pmas.toml
   ```

### Configuration Options

The `pmas.toml` file demonstrates various configuration options:

- **Environment settings**: Base URL, environment name
- **Browser configuration**: Browser type, window size, headless mode
- **Timeouts**: Page load, element wait, script execution
- **Test settings**: Default timeouts, failure capture
- **Logging**: Log levels, formats, file output
- **Reporting**: Screenshot and log directories

## Key Framework Features Demonstrated

### 1. Type-Safe Locators
```python
USERNAME_FIELD = by_id('user-name', 'Username input field')
PASSWORD_FIELD = by_id('password', 'Password input field')
```

### 2. Element Abstractions
```python
username_field = self.get_text_input(self.USERNAME_FIELD)
username_field.type_text(username)

login_button = self.get_button(self.LOGIN_BUTTON)
login_button.click()
```

### 3. Soft Assertions
```python
with SoftAssertions() as soft:
    soft.assert_true(login_page.verify_page_loaded(), "Login page should be loaded")
    soft.assert_true(username_field.is_displayed, "Username field should be visible")
    soft.assert_equal(username_field.get_attribute("placeholder"), "Username")
```

### 4. Parameterized Testing
```python
@pytest.mark.parametrize("username,password,should_succeed", [
    ("standard_user", "secret_sauce", True),
    ("locked_out_user", "secret_sauce", False),
    ("invalid_user", "secret_sauce", False),
])
def test_login_scenarios(self, driver, config, username, password, should_succeed):
    # Test implementation
```

### 5. Configuration-Driven Testing
```python
def test_successful_login(self, driver, config):
    login_page = SauceDemoLoginPage(driver, config.environment.base_url)
    # Test uses configuration for base URL, timeouts, etc.
```

## Best Practices Demonstrated

1. **Page Object Encapsulation**: Each page class encapsulates its own elements and behaviors
2. **Method Chaining**: Page methods return appropriate page objects for fluent interfaces
3. **Error Handling**: Graceful handling of expected and unexpected errors
4. **Wait Strategies**: Implicit and explicit waits for reliable element interactions
5. **Test Independence**: Each test can run independently without dependencies
6. **Data Separation**: Test data separated from test logic
7. **Logging**: Comprehensive logging for debugging and monitoring

## Extending the Examples

To add new test scenarios:

1. **Add new page objects** for additional pages
2. **Extend existing page objects** with new methods
3. **Create new test files** for different functional areas
4. **Add data files** for data-driven testing
5. **Customize configuration** for different environments

## Troubleshooting

### Common Issues

1. **Browser driver not found**:
   - Install webdriver-manager: `pip install webdriver-manager`
   - Or download driver manually and add to PATH

2. **Element not found errors**:
   - Check if page has loaded completely
   - Verify locator strategies are correct
   - Increase timeout values in configuration

3. **Test failures in headless mode**:
   - Some tests may behave differently in headless mode
   - Use `--headless false` to run with visible browser

4. **Slow test execution**:
   - Reduce timeout values for faster feedback
   - Use `--browser chrome` for better performance
   - Consider parallel execution with pytest-xdist

### Getting Help

- Check the main PMAS documentation
- Review the framework source code in `src/pmas/core/`
- Look at configuration examples in `src/pmas/config/`
- Examine other domain examples in `src/pmas/domains/`
