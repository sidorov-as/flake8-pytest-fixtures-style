import ast
from typing import Set

from flake8_plugin_utils import Visitor
from flake8_pytest_style.utils import (
    extract_parametrize_call_args,
    is_parametrize_call,
    AnyFunctionDef,
)

from flake8_pytest_fixtures_style.config import Config
from flake8_pytest_fixtures_style.errors import FixtureFactoryNameError, UnusedFixtureError
from flake8_pytest_fixtures_style.utils import (
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
        if not is_test_function(node.name, patterns=self.config.python_functions):
            return self.generic_visit(node)

        fixtures = {arg.arg for arg in node.args.args}
        if fixtures:
            self._check_unused_fixture(node, fixtures)

        self.generic_visit(node)

    visit_AsyncFunctionDef = visit_FunctionDef  # noqa: CCE001

    def _check_unused_fixture(self, fixture: AnyFunctionDef, fixtures: Set[str]):
        """Checks for PF002."""
        names = {node.id for node in ast.walk(fixture) if isinstance(node, ast.Name)}

        usefixtures: Set[str] = set()
        parametrized_args: Set[str] = set()

        for decorator in fixture.decorator_list:
            if isinstance(decorator, ast.Call):
                if is_pytest_mark_usefixtures(decorator.func):
                    usefixtures.update(arg.value for arg in decorator.args)  # type: ignore
                if is_parametrize_call(decorator):
                    args = extract_parametrize_call_args(decorator)
                    parametrized_args.update(name.value for name in args.names.elts)

        unused_fixtures = fixtures - names - usefixtures - parametrized_args
        if unused_fixtures:
            for unused_fixture in unused_fixtures:
                self.error_from_node(UnusedFixtureError, node=fixture, fixture_name=unused_fixture)
