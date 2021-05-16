format:
	pre-commit run black --all-files
	pre-commit run absolufy-imports --all-files
	pre-commit run isort --all-files

pre-commit:
	pre-commit run

pre-commit-all:
	pre-commit run --all-files

test:
	python -m pytest

coverage:
	python -m pytest --cov=flake8_pytest_fixtures_style --cov-report=xml

types:
	mypy .

style:
	flake8 .

md:
	mdl README.md
	mdl docs

requirements:
	safety check -r requirements_dev.txt

check:
	make style
	make types
	make test
	make requirements
