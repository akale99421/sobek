.PHONY: dev dev-hot build stop clean logs

dev:
	docker compose up --build

dev-hot:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build

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

