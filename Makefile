.PHONY: dev build stop clean logs

dev:
	docker compose up --build

build:
	docker compose build

stop:
	docker compose down

clean:
	docker compose down -v

logs:
	docker compose logs -f

backend-logs:
	docker compose logs -f backend

frontend-logs:
	docker compose logs -f frontend

