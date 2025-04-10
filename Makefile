DOCKER_COMPOSE_FILE := docker-compose.yml

up:
	@echo "Запуск Docker Compose с файлом $(DOCKER_COMPOSE_FILE)"

	docker compose -f $(DOCKER_COMPOSE_FILE) up -d ollama api

build:
	@echo "Сборка Docker Compose с файлом $(DOCKER_COMPOSE_FILE)"
	docker compose -f $(DOCKER_COMPOSE_FILE) build ollama api

down:
	@echo "Остановка Docker Compose с файлом $(DOCKER_COMPOSE_FILE)"
	docker compose -f $(DOCKER_COMPOSE_FILE) down

logs:
	@echo "Вывод логов Docker Compose с файлом $(DOCKER_COMPOSE_FILE)"
	docker compose -f $(DOCKER_COMPOSE_FILE) logs

shell-ollama:
	@echo "Запуск оболочки в контейнере ollama"
	docker compose -f $(DOCKER_COMPOSE_FILE) exec ollama /bin/bash
