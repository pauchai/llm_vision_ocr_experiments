up:
	docker compose  up -d 
build : 
	docker compose build
down:
	docker compose  down
logs:
	docker compose logs
shell-ollama:
	docker compose exec ollama sh
