from typing import Optional

from setuptools import find_packages, setup

package_name = 'flake8_pytest_fixtures_style'


def get_version() -> Optional[str]:
    with open('flake8_pytest_fixtures_style/__init__.py', 'r') as f:
        lines = f.readlines()
    for line in lines:
        if line.startswith('__version__'):
            return line.split('=')[-1].strip().strip("'")
    return None


def get_long_description() -> str:
    with open('README.md') as f:
        return f.read()


setup(
    name=package_name,
    description='A flake extension that checks pytest fixtures',
    classifiers=[
        'Environment :: Console',
        'Framework :: Flake8',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Documentation',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Quality Assurance',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    python_requires='>=3.8',
    include_package_data=True,
    keywords='flake8',
    version=get_version(),
    author='Alexey Sidorov',
    author_email='ereon.dev@gmail.com',
    install_requires=[
        'astpretty==1.6.0',
        'flake8==4.0.1',
        'setuptools',
        'flake8-plugin-utils==1.3.2',
        'flake8-pytest-style==1.6.0',
    ],
    entry_points={'flake8.extension': ['PF = flake8_pytest_fixtures_style.plugin:Plugin']},
    url='https://github.com/sidorov-as/flake8-pytest-fixtures-style',
    license='MIT',
    py_modules=[package_name],
    zip_safe=False,
)
