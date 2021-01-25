install:
	poetry install

lint:
	poetry run flake8 src

start:
	poetry run wh-paranoico
