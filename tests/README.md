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
python -m pytest tests/accounts/
python -m pytest tests/invitations/
python -m pytest tests/companies/
python -m pytest tests/teams/
python -m pytest tests/reviews/
python -m pytest tests/perfecto/
```

To run tests with coverage report:

```bash
python -m pytest --cov=accounts --cov=invitations --cov=companies --cov=teams --cov=reviews --cov=perfecto --cov-report=term
```

## Test Organization

Tests are organized by application:

- `tests/accounts/` - Tests for the accounts app
  - `test_models.py` - Tests for user model
  - `test_forms.py` - Tests for authentication forms
  - `test_views.py` - Tests for authentication views
  - `test_urls.py` - Tests for authentication URLs

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

- `tests/teams/` - Tests for the teams app
  - `test_models.py` - Tests for team models
  - `test_forms.py` - Tests for team forms
  - `test_views.py` - Tests for team views
  - `test_urls.py` - Tests for team URLs

- `tests/reviews/` - Tests for the reviews app
  - `test_models.py` - Tests for review models
  - `test_forms.py` - Tests for review forms
  - `test_views.py` - Tests for review views
  - `test_urls.py` - Tests for review URLs

- `tests/perfecto/` - Tests for the core Perfecto project
  - `test_urls.py` - Tests for project URLs configuration
  - `test_settings.py` - Tests for project settings
  - `test_templates.py` - Tests for template rendering
  - `test_wsgi.py` - Tests for WSGI application
