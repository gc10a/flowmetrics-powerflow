.PHONY: help install install-dev test lint format clean run-examples

help:
	@echo "PowerFlow Development Commands"
	@echo "=============================="
	@echo "install        - Install package"
	@echo "install-dev    - Install with development dependencies"
	@echo "test          - Run tests"
	@echo "lint          - Run linters (flake8, mypy)"
	@echo "format        - Format code with black"
	@echo "clean         - Remove build artifacts"
	@echo "run-examples  - Run example pipelines"

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

test:
	pytest tests/ -v --cov=powerflow --cov-report=term-missing

lint:
	flake8 powerflow tests --max-line-length=100
	mypy powerflow --ignore-missing-imports

format:
	black powerflow tests examples

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

run-examples:
	python examples/basic_pipeline.py
	python examples/aggregation_pipeline.py

