import ast

from flake8_pytest_fixtures_style.utils import is_test_function, is_pytest_mark_usefixtures

import pytest


@pytest.mark.parametrize(
    ('name', 'patterns', 'expected'),
    [
        (
            'test_func',
            ['test_*'],
            True
        ),
        (
            'test_func',
            ['test_'],
            True
        ),
        (
            'not_a_test_func',
            ['test_*'],
            False
        ),
    ]
)
def test_is_test_function(name, patterns, expected):
    assert is_test_function(name, patterns) == expected

