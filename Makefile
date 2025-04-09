up:
	docker compose up -d ollama api

build:
	docker compose build ollama api

down:
	docker compose down

logs:
	docker compose logs

shell-ollama:
	docker compose exec ollama sh
