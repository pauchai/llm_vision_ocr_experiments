include .env
export

DOCKER_COMPOSE_FILE := docker-compose.yml

ifeq ($(DOCKER_DEPLOYMENT),GPU)
    DOCKER_COMPOSE_OVERRIDE_FILE := docker-compose-gpu-rtx.yml
else
    DOCKER_COMPOSE_OVERRIDE_FILE := /dev/null
endif

.PHONY: up build down logs shell-ollama

# Запуск всех или указанных сервисов
up:
	@echo "Запуск Docker Compose ($(DOCKER_DEPLOYMENT))"
	docker compose -f $(DOCKER_COMPOSE_FILE) -f $(DOCKER_COMPOSE_OVERRIDE_FILE) up -d $(filter-out $@,$(MAKECMDGOALS))

# Сборка всех или указанных сервисов
build:
	@echo "Сборка Docker Compose ($(DOCKER_DEPLOYMENT))"
	docker compose -f $(DOCKER_COMPOSE_FILE) -f $(DOCKER_COMPOSE_OVERRIDE_FILE) build $(filter-out $@,$(MAKECMDGOALS))

down:
	docker compose -f $(DOCKER_COMPOSE_FILE) -f $(DOCKER_COMPOSE_OVERRIDE_FILE) down

logs:
	docker compose -f $(DOCKER_COMPOSE_FILE) -f $(DOCKER_COMPOSE_OVERRIDE_FILE) logs

shell-ollama:
	docker compose -f $(DOCKER_COMPOSE_FILE) -f $(DOCKER_COMPOSE_OVERRIDE_FILE) exec ollama /bin/bash

# Обработка псевдоаргументов make (чтобы не было ошибки "No rule to make target...")
%:
	@:
