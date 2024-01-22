lint:
	poetry run flake8 gendiff

test:
	poetry run pytest -s

self-check:
	poetry check

check: self-check lint test

test-coverage:
	poetry run pytest --cov=gendiff --cov-report xml

.PHONY: test lint self-check check build
