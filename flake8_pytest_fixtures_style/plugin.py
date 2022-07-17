import argparse
from typing import List, Type

from flake8.options.manager import OptionManager
from flake8_plugin_utils import Plugin as BasePlugin, Visitor

from flake8_pytest_fixtures_style import __version__ as pkg_version
from flake8_pytest_fixtures_style.config import DEFAULT_CONFIG, Config
from flake8_pytest_fixtures_style.visitors import FixtureFactoryVisitor, UnusedFixtureVisitor


class Plugin(BasePlugin[Config]):
    name: str = 'flake8-pytest-fixtures'
    version: str = pkg_version

    visitors: List[Type[Visitor[Config]]] = [FixtureFactoryVisitor, UnusedFixtureVisitor]

    @classmethod
    def add_options(cls, option_manager: OptionManager) -> None:
        option_manager.add_option(
            '--python-functions',
            type=str,
            default=DEFAULT_CONFIG.python_functions,
            parse_from_config=True,
            dest='python_functions',
            nargs='+',
        )

    @classmethod
    def parse_options_to_config(
        cls, option_manager: OptionManager, options: argparse.Namespace, args: List[str]
    ) -> Config:
        return Config(python_functions=options.python_functions)
