## Project Overview

PMAS (Python Modern Automation Suite) is a modern, reusable Web UI testing framework built on Python 3.11+ and Selenium 4+. It provides a clean architecture separating core testing logic from domain-specific application logic through a layered architecture with domain adapters, testing utilities, and core components.

## Essential Commands

### Development Setup
```bash
# Install development dependencies
uv pip install -e ".[dev]"
```

### Running Tests
```bash
# Run all unit and integration tests (default, fast)
uv run pytest

# Run specific test categories
uv run pytest -m unit              # Unit tests only
uv run pytest -m integration        # Integration tests only

# Run real browser tests (requires explicit enablement)
export PMAS_RUN_REAL_BROWSER=1
uv run pytest -m real_browser

# Run tests with coverage
uv run pytest --cov=src/pmas --cov-report=term-missing

# Run tests in parallel
uv run pytest -n auto

# Run specific test file
uv run pytest tests/unit/test_core_config.py
```

### Code Quality
```bash
# Run linting
uv run ruff check src/ tests/
uv run ruff format src/ tests/

# Run type checking
uv run mypy src/
```

## Architecture Overview

The codebase follows a three-layer architecture that requires understanding the interaction between multiple components:

### Core Layer (`src/pmas/core/`)
- **Driver Factory Pattern**: WebDriver creation uses protocol-based interfaces hiding Selenium implementation details. The factory creates drivers based on configuration, managing browser lifecycle automatically.
- **Page Object Model**: Base classes in `base_page.py` provide common functionality. Pages inherit from `BasePage` and define locators as class attributes using the custom `Loc` system.
- **Element Abstractions**: Type-safe wrappers for web elements with automatic waits and error handling. Elements are accessed through specialized getters that return typed interfaces.
- **Locator System**: Custom locator definitions using `Loc.text()`, `Loc.dropdown()`, etc. with built-in descriptions for better debugging.

### Domain Layer (`src/pmas/domains/`)
- **Adapter Pattern**: Each domain (aviation, manufacturing) has adapters that orchestrate workflows using page objects. Adapters abstract complex multi-page operations into simple method calls.
- **Page Inheritance**: Domain-specific pages inherit from base pages and add domain logic. For example, `BaseManufacturingPage` extends `BasePage` with manufacturing-specific utilities.

### Testing Layer (`src/pmas/testing/`)
- **Soft Assertions**: Allow tests to continue after failures, collecting all failures for comprehensive reporting. Used via context managers: `with SoftAssertions() as soft:`.
- **Three-Tier Testing Strategy**:
  - Unit tests use `FakeWebDriver` for complete isolation
  - Integration tests verify component interactions with fakes
  - Real browser tests are minimal smoke tests for driver integration

### Configuration System (`src/pmas/config/`)
- **Layered Configuration**: Command-line args > Environment vars > TOML files > Defaults
- **Type-Safe Config**: Uses Pydantic models for validation and type safety
- **Environment-Specific**: Different configs for local development vs CI/CD

## Test Organization

### Test Fixtures (`tests/conftest.py`)
- `pmas_config`: Provides test configuration
- `fake_driver`: Mock WebDriver for unit/integration tests
- Real driver fixtures require `PMAS_RUN_REAL_BROWSER=1`

### Fake Implementation (`tests/fakes/`)
- `FakeWebDriver`: Simulates Selenium WebDriver for fast, deterministic tests
- Implements all driver methods used by the framework
- Tracks interactions for verification in tests

## Key Design Patterns

### Locator Declaration Pattern
Pages declare locators as class attributes using the custom `Loc` system which provides type safety and descriptions. This separates element location from interaction logic.

### Adapter Pattern for Domains
Domain adapters orchestrate complex workflows spanning multiple pages, hiding implementation details from tests. This allows tests to express business logic without WebDriver details.

### Protocol-Based Interfaces
Core components use Python protocols to define interfaces, allowing flexible implementations while maintaining type safety. This enables easy testing with fakes and future extensibility.

## Important Notes

- The framework uses modern Python features (3.11+) extensively - type hints, protocols, and dataclasses are used throughout
- Real browser tests are intentionally minimal - most testing should use unit and integration tests with fakes
- The codebase prioritizes type safety - all public APIs have type hints enforced by mypy
- Domain separation is strict - core framework has no knowledge of specific domains
- Test categories are enforced - tests must be properly marked with pytest markers