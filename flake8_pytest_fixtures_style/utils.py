import ast
from fnmatch import fnmatch
from typing import List, Set

from flake8_pytest_style.utils import (
    AnyFunctionDef,
    extract_parametrize_call_args,
    get_fixture_decorator,
    get_qualname,
)


def is_test_function(name: str, patterns: List[str]) -> bool:
    for pattern in patterns:
        if name.startswith(pattern):
            return True

        # check that name looks like a glob-string before calling fnmatch
        # because this is called for every name in each collected module,
        # and fnmatch is somewhat expensive to call
        elif ('*' in pattern or '?' in pattern or '[' in pattern) and fnmatch(name, pattern):
            return True
    return False


def is_pytest_mark_usefixtures(node: ast.expr) -> bool:
    name = get_qualname(node)
    if name is None:
        return False  # pragma: no cover
    return name.startswith('pytest.mark.usefixtures')


def is_pytest_fixture_function(node: AnyFunctionDef) -> bool:
    return get_fixture_decorator(node) is not None


def is_function_returns_function(node: ast.FunctionDef) -> bool:
    return_name = [
        item.value.id
        for item in node.body
        if isinstance(item, ast.Return) and isinstance(item.value, ast.Name)
    ]
    if not return_name:
        return False
    return_name = return_name[0]

    for item in node.body:
        if isinstance(item, ast.FunctionDef) and item.name == return_name:
            return True

    return False


def get_variable_names(node: ast.AST) -> Set[str]:
    """
    Returns a set of variable names for given ast node.
    """
    return {node.id for node in ast.walk(node) if isinstance(node, ast.Name)}


def get_usefixtures_decorator_args(decorator: ast.Call) -> List[str]:
    """
    Returns a list of @pytest.mark.usefixtures(...) decorator args.
    """
    args = []

    for arg in decorator.args:
        if isinstance(arg, ast.Constant):
            args.append(arg.value)

    return args


def get_test_function_fixtures(function_node: AnyFunctionDef) -> List[str]:
    """
    Returns a set of fixtures passed into the test function as arguments.
    """
    return [arg.arg for arg in function_node.args.args]


def get_parametrize_decorator_args(decorator: ast.Call) -> List[str]:
    """
    Returns a list of @pytest.mark.parametrize(argnames, argvalues, *, ...) decorator argnames.

    If argnames represents a comma-separated string denoting one or more argument names,
    or a list/tuple of argument strings, returns a list of str.

    Otherwise, returns an empty list.
    """
    args: List[str] = []

    parametrize_args = extract_parametrize_call_args(decorator)
    if parametrize_args:
        argnames = parametrize_args.names
        if isinstance(argnames, ast.Constant):
            raw_args = [arg.strip() for arg in argnames.value.split(',')]
            args.extend(arg for arg in raw_args if arg)
        elif isinstance(argnames, (ast.List, ast.Tuple)):
            raw_args = [arg for arg in argnames.elts if isinstance(arg, ast.Constant)]
            args.extend(arg.value for arg in raw_args)

    return args
