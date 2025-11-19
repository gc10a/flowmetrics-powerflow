# Contributing to PowerFlow

Thank you for your interest in contributing to PowerFlow! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for all contributors.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:

- A clear, descriptive title
- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Your environment (OS, Python version, PowerFlow version)
- Code samples or error messages

### Suggesting Features

We welcome feature suggestions! Please create an issue with:

- A clear description of the feature
- Use cases and benefits
- Example code showing how it would work
- Any potential implementation considerations

### Submitting Pull Requests

1. **Fork the repository** and create a new branch from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Install development dependencies**:
   ```bash
   pip install -e ".[dev]"
   ```

3. **Make your changes** following our coding standards:
   - Follow PEP 8 style guidelines
   - Add type hints where applicable
   - Write docstrings for classes and functions
   - Keep functions focused and modular

4. **Add tests** for your changes:
   ```bash
   pytest tests/
   ```

5. **Run the code formatters**:
   ```bash
   black powerflow tests examples
   flake8 powerflow tests
   mypy powerflow
   ```

6. **Update documentation** if needed:
   - Update README.md if adding new features
   - Add docstrings to new code
   - Update examples if relevant

7. **Commit your changes** with clear commit messages:
   ```bash
   git commit -m "Add feature: description of your change"
   ```

8. **Push to your fork** and create a pull request:
   ```bash
   git push origin feature/your-feature-name
   ```

9. **Describe your changes** in the pull request:
   - What does this PR do?
   - Why is this change needed?
   - How has it been tested?
   - Any breaking changes?

## Development Setup

### Prerequisites

- Python 3.8 or higher
- pip
- git

### Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/flowmetrics/powerflow.git
   cd powerflow
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install in development mode:
   ```bash
   pip install -e ".[dev]"
   ```

4. Run tests to verify setup:
   ```bash
   pytest tests/
   ```

## Coding Standards

### Style Guide

- Follow [PEP 8](https://pep8.org/)
- Use [Black](https://black.readthedocs.io/) for code formatting (line length: 100)
- Use type hints for function arguments and return values
- Write clear, descriptive variable and function names

### Documentation

- All public classes and functions must have docstrings
- Use Google-style docstrings
- Include examples in docstrings where helpful

Example:
```python
def my_function(arg1: str, arg2: int) -> bool:
    """
    Brief description of what the function does.
    
    Args:
        arg1: Description of arg1
        arg2: Description of arg2
    
    Returns:
        Description of return value
    
    Example:
        >>> my_function("test", 42)
        True
    """
    pass
```

### Testing

- Write unit tests for all new features
- Aim for high test coverage (>80%)
- Use pytest for testing
- Mock external services (Salesforce, HubSpot, etc.)

Example test:
```python
def test_filter_transformer():
    """Test that FilterTransformer correctly filters records."""
    transformer = FilterTransformer(lambda x: x["value"] > 10)
    data = [{"value": 5}, {"value": 15}, {"value": 20}]
    result = transformer.transform(data)
    assert len(result) == 2
    assert result[0]["value"] == 15
```

## Adding New Integrations

When adding a new integration (e.g., a new CRM):

1. Create a new file in `powerflow/integrations/`
2. Implement a `Source` class that extends `DataSource`
3. Add tests in `tests/integrations/`
4. Update `powerflow/integrations/__init__.py`
5. Add example usage in `examples/`
6. Update README.md with the new integration
7. Add dependencies to `setup.py` extras_require

## Project Structure

```
powerflow/
├── powerflow/           # Main package
│   ├── __init__.py
│   ├── pipeline.py      # Core pipeline classes
│   ├── sources.py       # Data source implementations
│   ├── transformers.py  # Data transformer implementations
│   ├── destinations.py  # Data destination implementations
│   └── integrations/    # Third-party integrations
│       ├── __init__.py
│       ├── salesforce.py
│       └── hubspot.py
├── tests/              # Test suite
│   ├── test_pipeline.py
│   ├── test_sources.py
│   └── ...
├── examples/           # Example scripts
├── docs/              # Documentation
├── setup.py           # Package setup
└── README.md          # Project readme
```

## Release Process

Releases are handled by maintainers. The process:

1. Update version in `setup.py` and `powerflow/__init__.py`
2. Update CHANGELOG.md
3. Create a git tag
4. Push to GitHub
5. Publish to PyPI

## Questions?

If you have questions about contributing:

- Check existing [GitHub Discussions](https://github.com/flowmetrics/powerflow/discussions)
- Open a new discussion
- Contact the maintainers

## Recognition

Contributors will be recognized in:
- The README.md contributors section
- GitHub contributors page
- Release notes

Thank you for contributing to PowerFlow! 🎉

