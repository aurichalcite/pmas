# PMAS Testing Guide

This document provides comprehensive guidance for running, maintaining, and extending the PMAS test suite. The test suite follows a three-layer architecture designed for speed, reliability, and maintainability.

## Table of Contents

- [Setup](#setup)
- [Test Categories](#test-categories)
- [Running Tests](#running-tests)
- [Environment Variables](#environment-variables)
- [Coverage Requirements](#coverage-requirements)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## Setup

### Prerequisites

- Python 3.11 or higher
- Chrome browser (for real browser tests)
- Git

### Development Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/aurichalcite/pmas.git
   cd pmas
   ```

2. **Install development dependencies:**
   ```bash
   # Using pip
   pip install -e ".[dev]"
   
   # Or using uv (recommended)
   uv sync --dev
   ```

3. **Verify installation:**
   ```bash
   pytest --version
   python -c "import pmas; print(pmas.__version__)"
   ```

### Required Development Dependencies

The test suite requires these additional packages (included in `[dev]` extras):

```
pytest>=7.0
pytest-cov>=4.0
pytest-xdist>=3.0
pytest-timeout>=2.0
selenium>=4.0
```

## Test Categories

The PMAS test suite implements exactly three distinct test layers:

### 1. Unit Tests (`@pytest.mark.unit`)

**Purpose:** Test individual components in complete isolation using mocks and fakes.

**Characteristics:**
- No external dependencies (no network, no filesystem I/O, no real browsers)
- Execute in milliseconds
- Use mocks and fakes exclusively
- Test single classes or functions

**Location:** `tests/unit/`

**Examples:**
- `test_core_config.py` - Config class validation and initialization
- `test_utils_soft_assert.py` - SoftAssertions utility functionality

### 2. Integration Tests (`@pytest.mark.integration`)

**Purpose:** Verify interaction between multiple internal PMAS components.

**Characteristics:**
- Use fakes for external systems (FakeWebDriver)
- No real browsers or network calls
- Test component interactions and workflows
- Fast execution (seconds, not minutes)

**Location:** `tests/integration/`

**Examples:**
- `test_adapter_login_flow.py` - Domain adapter integration with page objects

### 3. Real Browser Tests (`@pytest.mark.real_browser`)

**Purpose:** Minimal smoke tests validating PMAS integration with actual browser drivers.

**Characteristics:**
- Use actual headless browser drivers
- Must be explicitly enabled via environment variable
- Minimal operations only (not end-to-end tests)
- Confirm driver stack integration

**Location:** `tests/real_browser/`

**Examples:**
- `test_smoke_browser_init.py` - Basic browser control functionality

## Running Tests

### Quick Start

```bash
# Run all unit and integration tests (default)
pytest

# Run only unit tests
pytest -m unit

# Run only integration tests  
pytest -m integration

# Run with verbose output
pytest -v
```

### Running Real Browser Tests

Real browser tests are disabled by default and must be explicitly enabled:

```bash
# Enable real browser tests
export PMAS_RUN_REAL_BROWSER=1
pytest -m real_browser

# Run all tests including real browser tests
export PMAS_RUN_REAL_BROWSER=1
pytest
```

### Parallel Execution

For faster execution, use pytest-xdist:

```bash
# Run tests in parallel (auto-detect CPU cores)
pytest -n auto

# Run with specific number of workers
pytest -n 4

# Parallel execution with coverage
pytest -n auto --cov=src/pmas
```

### Test Selection Examples

```bash
# Run specific test file
pytest tests/unit/test_core_config.py

# Run specific test function
pytest tests/unit/test_core_config.py::TestConfig::test_config_default_initialization

# Run tests matching pattern
pytest -k "config"

# Run tests excluding slow ones
pytest -m "not slow"

# Run with maximum verbosity
pytest -vvv --tb=long
```

### Expected Output Examples

**Successful unit test run:**
```
$ pytest -m unit -v
========================= test session starts =========================
collected 45 items

tests/unit/test_core_config.py::TestBrowserConfig::test_browser_config_default_initialization PASSED
tests/unit/test_core_config.py::TestBrowserConfig::test_browser_config_with_valid_browsers[chrome] PASSED
tests/unit/test_utils_soft_assert.py::TestSoftAssertions::test_assert_equal_success PASSED
...

========================= 45 passed in 2.34s =========================
```

**Integration test run:**
```
$ pytest -m integration -v
========================= test session starts =========================
collected 12 items

tests/integration/test_adapter_login_flow.py::TestManufacturingLoginAdapterIntegration::test_login_as_production_planner_success PASSED
...

========================= 12 passed in 8.67s =========================
```

## Environment Variables

### Core Configuration

| Variable | Purpose | Default | Example |
|----------|---------|---------|---------|
| `PMAS_RUN_REAL_BROWSER` | Enable real browser tests | `unset` (disabled) | `1` |
| `PMAS_BROWSER_NAME` | Browser for real tests | `chrome` | `firefox` |
| `PMAS_TEST_TIMEOUT` | Default test timeout | `300` | `600` |

### CI/CD Configuration

```bash
# Typical CI environment setup
export PMAS_RUN_REAL_BROWSER=1
export PMAS_BROWSER_NAME=chrome
export PMAS_TEST_TIMEOUT=600
```

### Local Development

```bash
# Fast development cycle (unit + integration only)
unset PMAS_RUN_REAL_BROWSER

# Full test suite
export PMAS_RUN_REAL_BROWSER=1
```

## Coverage Requirements

### Running Coverage Analysis

```bash
# Generate coverage report
pytest --cov=src/pmas --cov-report=html --cov-report=term-missing

# Coverage with specific threshold
pytest --cov=src/pmas --cov-fail-under=80

# Coverage for specific test category
pytest -m unit --cov=src/pmas/config --cov-report=term-missing
```

### Coverage Thresholds

| Component | Minimum Coverage | Target Coverage |
|-----------|------------------|-----------------|
| Core modules | 90% | 95% |
| Domain adapters | 80% | 90% |
| Testing utilities | 95% | 98% |
| Overall project | 85% | 90% |

### Coverage Report Locations

- **HTML Report:** `htmlcov/index.html`
- **Terminal:** Displayed after test run
- **XML Report:** `coverage.xml` (for CI integration)

## Troubleshooting

### Common Issues

#### 1. Real Browser Tests Failing

**Symptoms:**
```
selenium.common.exceptions.WebDriverException: Message: 'chromedriver' executable needs to be in PATH
```

**Solutions:**
```bash
# Install ChromeDriver automatically
pip install webdriver-manager

# Or install manually (Ubuntu/Debian)
sudo apt-get install chromium-chromedriver

# Or use package manager (macOS)
brew install chromedriver
```

#### 2. Import Errors

**Symptoms:**
```
ModuleNotFoundError: No module named 'pmas'
```

**Solutions:**
```bash
# Ensure PMAS is installed in development mode
pip install -e .

# Verify Python path
python -c "import sys; print(sys.path)"

# Check installation
pip list | grep pmas
```

#### 3. Test Discovery Issues

**Symptoms:**
```
collected 0 items
```

**Solutions:**
```bash
# Verify test file naming (must start with test_)
ls tests/unit/test_*.py

# Check pytest configuration
pytest --collect-only

# Verify markers are registered
pytest --markers
```

#### 4. Slow Test Execution

**Symptoms:**
Tests taking longer than expected

**Solutions:**
```bash
# Use parallel execution
pytest -n auto

# Profile slow tests
pytest --durations=10

# Run only fast tests
pytest -m "unit or integration"
```

#### 5. Fake Driver Issues

**Symptoms:**
```
AttributeError: 'FakeWebDriver' object has no attribute 'some_method'
```

**Solutions:**
1. Check if method is implemented in `FakeWebDriver`
2. Add missing method to fake implementation
3. Verify test is using correct driver fixture

### Debug Mode

Enable debug mode for detailed troubleshooting:

```bash
# Enable debug logging
pytest --log-cli-level=DEBUG

# Capture stdout/stderr
pytest -s

# Drop into debugger on failure
pytest --pdb

# Stop on first failure
pytest -x
```

### Performance Debugging

```bash
# Profile test execution time
pytest --durations=0

# Memory usage profiling
pytest --profile

# Identify slow tests
pytest --durations=10 -v
```

## Contributing

### Adding New Tests

1. **Choose the correct test layer:**
   - Unit: Testing single components in isolation
   - Integration: Testing component interactions
   - Real Browser: Testing actual browser integration

2. **Follow naming conventions:**
   - File: `test_<component>_<functionality>.py`
   - Class: `Test<ComponentName>`
   - Method: `test_<component>_<scenario>_<expected_outcome>`

3. **Use appropriate fixtures:**
   - `pmas_config`: Test configuration
   - `fake_driver`: Mock WebDriver for unit/integration tests
   - `real_driver`: Actual WebDriver for smoke tests

### Test Quality Guidelines

1. **Isolation:** Each test should be runnable independently
2. **Determinism:** Tests must produce identical results on every run
3. **Speed:** Unit tests in milliseconds, integration tests in seconds
4. **Clarity:** Descriptive names and comprehensive docstrings
5. **Coverage:** Aim for high coverage with meaningful assertions

### Example Test Template

```python
"""
Module docstring explaining test purpose and scope.
"""

import pytest
from pmas import Config
from ..fakes.fake_webdriver import FakeWebDriver

class TestComponentName:
    """Test class for ComponentName functionality."""
    
    def test_component_scenario_expected_outcome(self, pmas_config: Config):
        """
        Test that ComponentName behaves correctly in specific scenario.
        
        Args:
            pmas_config: Test configuration fixture
        """
        # Arrange
        component = ComponentName(pmas_config)
        
        # Act
        result = component.do_something()
        
        # Assert
        assert result is not None
        assert result.property == expected_value
```

### Submitting Changes

1. Run full test suite: `pytest`
2. Check coverage: `pytest --cov=src/pmas --cov-fail-under=80`
3. Verify code style: `black . && isort .`
4. Update documentation if needed
5. Submit pull request with test results

For questions or issues, please refer to the project documentation or open an issue on GitHub.
