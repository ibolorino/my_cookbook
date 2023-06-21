build:
	docker compose build

down:
	docker compose down

makemigrations:
	docker compose run --rm backend alembic revision --autogenerate -m "$(MSG)"

migrate:
	docker compose run --rm backend alembic upgrade head

runserver:
	docker compose up

test:
	docker compose run --rm backend python -m unittest discover -v -s tests/$(DIR)
