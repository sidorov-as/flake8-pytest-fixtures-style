from flake8_plugin_utils import assert_error, assert_not_error

from flake8_pytest_fixtures_style.config import DEFAULT_CONFIG
from flake8_pytest_fixtures_style.errors import FixtureFactoryNameError
from flake8_pytest_fixtures_style.visitors import FixtureFactoryVisitor


def test_no_errors():
    code = """                
        @pytest.fixture()
        def user_factory():
            defaults = {"fist_name": "John", "last_name": "Doe"}
        
            def with_params(**overrides):
                return User(**defaults, **overrides)
        
            return with_params
    """

    assert_not_error(FixtureFactoryVisitor, code, config=DEFAULT_CONFIG)


def test_errors():
    code = """
        @pytest.fixture()
        def user():
            defaults = {"fist_name": "John", "last_name": "Doe"}
        
            def with_params(**overrides):
                return User(**defaults, **overrides)
        
            return with_params
    """

    assert_error(
        FixtureFactoryVisitor,
        code,
        FixtureFactoryNameError,
        config=DEFAULT_CONFIG,
        func_name='user',
    )
