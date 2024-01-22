lint:
	poetry run flake8 gendiff

test:
	poetry run pytest -s

#test-coverage:
#	poetry run pytest --cov=gendiff --cov-report xml

.PHONY: install test lint selfcheck check build
