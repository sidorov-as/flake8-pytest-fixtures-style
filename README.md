# flake8-pytest-fixtures-style

[![Build Status](https://travis-ci.com/sidorov-as/flake8-pytest-fixtures-style.svg?branch=main)](https://travis-ci.org/sidorov-as/flake8-pytest-fixtures-style)
[![Maintainability](https://api.codeclimate.com/v1/badges/705e9a1c834a48e1d05c/maintainability)](https://codeclimate.com/github/sidorov-as/flake8-pytest-fixtures-style/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/705e9a1c834a48e1d05c/test_coverage)](https://codeclimate.com/github/sidorov-as/flake8-pytest-fixtures-style/test_coverage)
[![PyPI version](https://badge.fury.io/py/flake8-pytest-fixtures-style.svg?)](https://badge.fury.io/py/flake8-pytest-fixtures-style)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/flake8-pytest-fixtures-style)

A flake8 extension that checks pytest fixtures.

## Installation

```terminal
pip install flake8-pytest-fixtures-style
```

## Usage

```terminal
$ flake8 text.py
text.py:2:5: PF001: pytest fixture "your_func_name" returning another fixture must be suffixed with "_factory"
```

## Error codes

| Error code |                     Description   |
|:----------:|:---------------------------------:|
|   [PF001](docs/codes/PF001.md)   | fixture `factories` must be suffixed with "_factory" |
|   [PF002](docs/codes/PF002.md)   | fixtures unused in test function body must be specified via a `@pytest.mark.usefixtures(...)` |
