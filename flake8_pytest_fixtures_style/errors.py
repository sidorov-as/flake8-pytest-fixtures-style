from flake8_plugin_utils import Error


class FixtureFactoryNameError(Error):
    code = 'PF001'
    message = (
        'pytest fixture "{func_name}" returning another fixture must be suffixed with "_factory"'
    )


class UnusedFixtureError(Error):
    code = 'PF002'
    message = (
        'pytest fixture is not used in test function body and '
        'must be specified via a @pytest.mark.usefixtures("{fixture_name}") marker'
    )
