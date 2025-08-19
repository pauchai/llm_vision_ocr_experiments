.PHONY: build up down logs shell

# Build the Docker image
build:
	docker build -t huggingface_ocr .

# Run the container
up:
	docker run -d \
		--name huggingface_ocr \
		--gpus all \
		-p 7861:7861 \
		-v /data:/data \
		-e HF_TOKEN=$(HF_TOKEN) \
		huggingface_ocr

# Stop and remove the container
down:
	docker stop huggingface_ocr || true
	docker rm huggingface_ocr || true

# View logs
logs:
	docker logs -f huggingface_ocr

# Shell into the container
shell:
	docker exec -it huggingface_ocr /bin/bash

# Restart the service
restart: down up

# Clean up
clean: down
	docker rmi huggingface_ocr || true
