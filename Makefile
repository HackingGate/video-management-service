# Makefile for Docker Compose Project

# Default value for MEDIA_VOLUME_PATH (can be overridden)
MEDIA_VOLUME_PATH ?= /mnt/Unlimited/Media/Shared

# Export the MEDIA_VOLUME_PATH so it's available to docker-compose
export MEDIA_VOLUME_PATH

build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

restart:
	docker compose restart

logs:
	docker compose logs -f
