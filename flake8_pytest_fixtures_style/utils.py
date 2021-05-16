import ast
import os
from fnmatch import fnmatch
from typing import List

from flake8_pytest_style.utils import AnyFunctionDef, get_fixture_decorator, get_qualname


def is_test_file(file_path: str, patterns: List[str]) -> bool:
    file_name = os.path.basename(file_path)
    return any(fnmatch(file_name, pattern) for pattern in patterns)


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


def is_pytest_mark_usefixtures(node: AnyFunctionDef) -> bool:
    name = get_qualname(node)
    if name is None:
        return False
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
