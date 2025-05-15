include .env
export

DOCKER_COMPOSE_FILE := docker-compose.yml

ifeq ($(DOCKER_DEPLOYMENT),GPU)
    DOCKER_COMPOSE_OVERRIDE_FILE := docker-compose-gpu-rtx.yml
else
    DOCKER_COMPOSE_OVERRIDE_FILE := /dev/null
endif

up:
	@echo "Запуск  $(DOCKER_DEPLOYMENT)"

	
#docker compose -f $(DOCKER_COMPOSE_FILE) -f $(DOCKER_COMPOSE_OVERRIDE_FILE) up -d  qwen_api ollama api jupyter
	docker compose -f $(DOCKER_COMPOSE_FILE) -f $(DOCKER_COMPOSE_OVERRIDE_FILE) up -d  qwen_api 

build:
	@echo "Сборка Docker Compose с файлом $(DOCKER_DEPLOYMENT)"
#docker compose -f $(DOCKER_COMPOSE_FILE) -f $(DOCKER_COMPOSE_OVERRIDE_FILE) build  qwen_api ollama api jupyter
	docker compose -f $(DOCKER_COMPOSE_FILE) -f $(DOCKER_COMPOSE_OVERRIDE_FILE) build  qwen_api

down:
	@echo "Остановка Docker Compose с файлом $(DOCKER_DEPLOYMENT)"
	docker compose -f $(DOCKER_COMPOSE_FILE) -f $(DOCKER_COMPOSE_OVERRIDE_FILE) down

logs:
	@echo "Вывод логов Docker Compose с файлом $(DOCKER_DEPLOYMENT)"
	docker compose -f $(DOCKER_COMPOSE_FILE) -f $(DOCKER_COMPOSE_OVERRIDE_FILE) logs

shell-ollama:
	@echo "Запуск оболочки в контейнере ollama $(DOCKER_DEPLOYMENT)"
	docker compose -f $(DOCKER_COMPOSE_FILE) -f $(DOCKER_COMPOSE_OVERRIDE_FILE) exec ollama /bin/bash
