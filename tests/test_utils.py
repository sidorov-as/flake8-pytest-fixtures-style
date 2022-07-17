import ast
import textwrap
from typing import cast

import pytest

from flake8_pytest_fixtures_style.utils import (
    is_pytest_mark_usefixtures,
    is_test_function,
    is_pytest_fixture_function,
    is_function_returns_function, get_variable_names, get_usefixtures_decorator_args, get_test_function_fixtures,
    get_parametrize_decorator_args,
)


@pytest.mark.parametrize(
    ('name', 'patterns', 'expected'),
    [
        ('test_func', ['test_*'], True),
        ('test_func', ['test_'], True),
        ('not_a_test_func', ['test_*'], False),
    ],
)
def test__is_test_function(name, patterns, expected):
    assert is_test_function(name, patterns) == expected


@pytest.mark.parametrize(
    ('source', 'expected'),
    [
        (
            textwrap.dedent(
                """
                @pytest.mark.usefixtures('foo', 'bar')
                def test_function():
                    ...
                """
            ),
            True,
        ),
        (
            textwrap.dedent(
                """
                @pytest.mark.anything_else()
                def test_function():
                    ...
                """
            ),
            False,
        ),
    ],
)
def test__is_pytest_mark_usefixtures(source, expected):
    funcdef = cast(ast.FunctionDef, ast.parse(source).body[0])
    decorator = cast(ast.Call, funcdef.decorator_list[0])

    assert is_pytest_mark_usefixtures(decorator.func) == expected


@pytest.mark.parametrize(
    ('source', 'expected'),
    [
        (
            textwrap.dedent(
                """
                @pytest.fixture
                def fake_data():
                    return 42
                """
            ),
            True,
        ),
        (
            textwrap.dedent(
                """
                @pytest.fixture()
                def fake_data():
                    return 42
                """
            ),
            True,
        ),
        (
            textwrap.dedent(
                """
                @pytest.not_a_fixture()
                def invalid_fixture_function():
                    return 42
                """
            ),
            False,
        ),
    ],
)
def test__is_pytest_fixture_function(source, expected):
    funcdef = cast(ast.FunctionDef, ast.parse(source).body[0])

    assert is_pytest_fixture_function(funcdef) == expected


@pytest.mark.parametrize(
    ('source', 'expected'),
    [
        (
            textwrap.dedent(
                """
                @pytest.fixture()
                def fake_data_factory():
                    def with_params(**kwargs):
                        return {
                            'some-default-values': 42,
                            **kwargs
                        }
                        
                    return with_params
                """
            ),
            True,
        ),
        (
            textwrap.dedent(
                """
                @pytest.fixture()
                def fake_data_factory():
                    def inner_factory():
                        return {
                            'data': 42,
                        }
                        
                    return inner_factory()
                """
            ),
            False,
        ),
        (
            textwrap.dedent(
                """
                @pytest.fixture()
                def fake_data_factory():
                    some_setup()
                        
                """
            ),
            False,
        ),
    ],
    ids=['func-returns-func', 'func-returns-some-data', 'func-returns-nothing'],
)
def test__is_function_returns_function(source, expected):
    funcdef = cast(ast.FunctionDef, ast.parse(source).body[0])

    assert is_function_returns_function(funcdef) == expected


def test__get_variable_names():
    source = textwrap.dedent(
        """
        def test_some_action():
            x = 'foo'
            y = 'bar'
            expected = 'foobar'
            
            result = some_action(x, y)
            
            assert result == expected
        """
    )
    funcdef = cast(ast.FunctionDef, ast.parse(source).body[0])
    expected_variable_names = {'x', 'y', 'some_action', 'expected', 'result'}

    variable_names = get_variable_names(funcdef)

    assert variable_names == expected_variable_names


def test__get_usefixtures_decorator_args():
    source = textwrap.dedent(
        """
        @pytest.mark.usefixtures('fixture1', 'fixture2')
        def test_something():
            ...
        """
    )
    funcdef = cast(ast.FunctionDef, ast.parse(source).body[0])
    decorator = cast(ast.Call, funcdef.decorator_list[0])
    expected_used_fixtures = ['fixture1', 'fixture2']

    used_fixtures = get_usefixtures_decorator_args(decorator)

    assert used_fixtures == expected_used_fixtures


@pytest.mark.parametrize(
    ('source', 'expected'),
    [
        (
            textwrap.dedent(
                """
                @pytest.mark.parametrize('x, y', [(1, 2), (3, 4)])
                def test_something(x, y, yet_another_fixture):
                    ...
                """
            ),
            ['x', 'y', 'yet_another_fixture'],
        ),
        (
            textwrap.dedent(
                """
                def test_something(fixture):
                    ...
                """
            ),
            ['fixture'],
        ),
        (
                textwrap.dedent(
                    """
                    def test_something():
                        ...
                    """
                ),
                [],
        ),
    ],
    ids=['fixtures-and-parametrize', 'fixtures', 'no-fixtures']
)
def test__get_test_function_fixtures(source, expected):
    funcdef = cast(ast.FunctionDef, ast.parse(source).body[0])

    assert get_test_function_fixtures(funcdef) == expected


@pytest.mark.parametrize(
    ('source', 'expected_args'),
    [
        (
            textwrap.dedent(
                """
                @pytest.mark.parametrize('x, y', [(1, 2), (3, 4)])
                def test_something(x, y, yet_another_fixture):
                    ...
                """
            ),
            ['x', 'y'],
        ),
        (
            textwrap.dedent(
                """
                @pytest.mark.parametrize(['x', 'y'], [(1, 2), (3, 4)])
                def test_something(x, y, yet_another_fixture):
                    ...
                """
            ),
            ['x', 'y'],
        ),
        (
            textwrap.dedent(
                """
                @pytest.mark.parametrize(('x', 'y'), [(1, 2), (3, 4)])
                def test_something(x, y, yet_another_fixture):
                    ...
                """
            ),
            ['x', 'y'],
        ),
    ],
    ids=['argnames-str', 'argnames-list', 'argnames-tuple']
)
def test__get_parametrize_decorator_args(source, expected_args):
    funcdef = cast(ast.FunctionDef, ast.parse(source).body[0])
    decorator = cast(ast.Call, funcdef.decorator_list[0])

    assert get_parametrize_decorator_args(decorator) == expected_args
