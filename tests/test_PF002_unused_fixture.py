from flake8_plugin_utils import assert_error, assert_not_error

from flake8_pytest_fixtures_style.config import DEFAULT_CONFIG
from flake8_pytest_fixtures_style.errors import UnusedFixtureError
from flake8_pytest_fixtures_style.visitors import UnusedFixtureVisitor


def test_no_errors():
    code = """
        @pytest.mark.usefixtures('fixture2', 'fixture3')
        def test_something(fixture1, fixture2, fixture3):
            expected = fixture1()
        
            result = some_action()
        
            assert result == expected
    """

    assert_not_error(UnusedFixtureVisitor, code, config=DEFAULT_CONFIG)


def test_no_errors_parametrize():
    code = """
        @pytest.mark.parametrize(("param1", "param2"), [('example1', 'example2'), ('example3', 'example4')])
        @pytest.mark.usefixtures('fixture2', 'fixture3')
        def test_something(param1, param2, fixture1, fixture2, fixture3):
            expected = fixture1()
        
            result = some_action()
        
            assert result == expected
    """

    assert_not_error(UnusedFixtureVisitor, code, config=DEFAULT_CONFIG)


def test_errors():
    code = """
        def test_something(fixture1, fixture2):
            expected = fixture1()
        
            result = some_action()
        
            assert result == expected
    """

    assert_error(
        UnusedFixtureVisitor,
        code,
        UnusedFixtureError,
        fixture_name='fixture2',
        config=DEFAULT_CONFIG,
    )


def test_errors_parametrize():
    code = """ 
        @pytest.mark.parametrize(("param1", "param2"), [('example1', 'example2'), ('example3', 'example4')])
        def test_something(param1, param2, fixture1, fixture2):
            expected = fixture1()
    
            result = some_action()
    
            assert result == expected
    """

    assert_error(
        UnusedFixtureVisitor,
        code,
        UnusedFixtureError,
        fixture_name='fixture2',
        config=DEFAULT_CONFIG,
    )
