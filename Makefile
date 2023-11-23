install:
	poetry install --sync

lint:
	ruff check .
	poetry check

run:
	set -e
	poetry run alembic upgrade head
	poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload


admin:
	set -e
	poetry run alembic upgrade head
	poetry run uvicorn app.admin.mail:app --host 0.0.0.0 --port 8000 --reload
