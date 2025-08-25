# Project variables
PACKAGE=src/litemon
TESTS=tests

# Default target: run all checks
all: install format lint test coverage

## Install development dependencies
install:
	pip install -e .[dev]

## Run tests only
test:
	pytest $(TESTS)

## Run tests with coverage
coverage:
	pytest --cov=$(PACKAGE) --cov-report=term-missing

## Lint the code using ruff (fast linter)
lint:
	ruff check $(PACKAGE) $(TESTS)

## Automatically format code using ruff
format:
	ruff format $(PACKAGE) $(TESTS)

## Remove Python cache and coverage files
clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.pyo' -delete
	rm -rf .pytest_cache .coverage htmlcov

## Run everything: format, lint, tests, and coverage
check: format lint test coverage
