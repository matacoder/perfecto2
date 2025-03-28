# Tests for Perfecto Application

This directory contains tests for the Perfecto application.

## Running Tests

To run all tests:

```bash
./run_perfecto.sh --test
```

Or directly using pytest:

```bash
python -m pytest
```

To run tests for specific applications:

```bash
python -m pytest tests/invitations/
python -m pytest tests/companies/
```

To run tests with coverage report:

```bash
python -m pytest --cov=invitations --cov=companies --cov-report=term
```

## Test Organization

Tests are organized by application:

- `tests/invitations/` - Tests for the invitations app
  - `test_models.py` - Tests for invitation models
  - `test_forms.py` - Tests for invitation forms
  - `test_views.py` - Tests for invitation views
  - `test_urls.py` - Tests for invitation URLs

- `tests/companies/` - Tests for the companies app
  - `test_models.py` - Tests for company models
  - `test_forms.py` - Tests for company forms
  - `test_views.py` - Tests for company views
  - `test_urls.py` - Tests for company URLs
