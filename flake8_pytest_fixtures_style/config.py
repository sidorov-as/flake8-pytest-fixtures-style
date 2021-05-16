from typing import List, NamedTuple


class Config(NamedTuple):
    # https://docs.pytest.org/en/6.2.x/example/pythoncollection.html#changing-naming-conventions
    python_files: List[str]
    python_functions: List[str]


DEFAULT_CONFIG = Config(python_files=['test_*.py'], python_functions=['test_*'])
