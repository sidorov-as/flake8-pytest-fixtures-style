import ast
from typing import Set

from flake8_plugin_utils import Visitor
from flake8_pytest_style.utils import AnyFunctionDef, is_parametrize_call

from flake8_pytest_fixtures_style.config import Config
from flake8_pytest_fixtures_style.errors import FixtureFactoryNameError, UnusedFixtureError
from flake8_pytest_fixtures_style.utils import (
    get_parametrize_decorator_args,
    get_test_function_fixtures,
    get_usefixtures_decorator_args,
    get_variable_names,
    is_function_returns_function,
    is_pytest_fixture_function,
    is_pytest_mark_usefixtures,
    is_test_function,
)


class FixtureFactoryVisitor(Visitor[Config]):
    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:  # noqa: CCE001
        if is_pytest_fixture_function(node):
            if is_function_returns_function(node):
                self._check_fixture_factory_name(node)

    visit_AsyncFunctionDef = visit_FunctionDef  # noqa: CCE001

    def _check_fixture_factory_name(self, fixture: AnyFunctionDef):
        """Checks for PF001."""
        func_name = fixture.name
        if not func_name.endswith('_factory'):
            self.error_from_node(FixtureFactoryNameError, fixture, func_name=func_name)


class UnusedFixtureVisitor(Visitor[Config]):
    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:  # noqa: CCE001
        if is_test_function(node.name, patterns=self.config.python_functions):
            self._check_unused_fixtures(node)

        self.generic_visit(node)

    visit_AsyncFunctionDef = visit_FunctionDef  # noqa: CCE001

    def _check_unused_fixtures(self, function_node: AnyFunctionDef):
        """Checks for PF002."""
        fixtures_args = set(get_test_function_fixtures(function_node))
        if not fixtures_args:
            return

        variable_names = get_variable_names(function_node)

        usefixtures: Set[str] = set()
        parametrized_args: Set[str] = set()

        for decorator in function_node.decorator_list:
            if isinstance(decorator, ast.Call):
                if is_pytest_mark_usefixtures(decorator.func):
                    used_fixtures = get_usefixtures_decorator_args(decorator)
                    usefixtures.update(used_fixtures)
                if is_parametrize_call(decorator):
                    parametrized_fixtures = get_parametrize_decorator_args(decorator)
                    parametrized_args.update(parametrized_fixtures)

        unused_fixtures = fixtures_args - variable_names - usefixtures - parametrized_args
        if unused_fixtures:
            for unused_fixture in unused_fixtures:
                self.error_from_node(
                    UnusedFixtureError, node=function_node, fixture_name=unused_fixture
                )
