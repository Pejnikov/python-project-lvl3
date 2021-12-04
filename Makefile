lint:
	poetry run flake8 page_loader
	poetry run mypy page_loader

install:
	poetry install

test:
	poetry run pytest --cov=page_loader --cov-report xml

package-install:
	python3 -m pip uninstall hexlet-code
	python3 -m pip install --user dist/*.whl

build:
	poetry build