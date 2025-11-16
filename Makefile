.PHONY: nice docker-build docker-up docker-down docker-logs docker-restart docker-clean help

# Format, lint and type-check the code
nice:
	- uv run ruff format
	- uv run ruff check --fix
	- uv run mypy .

# Docker commands
docker-build:
	docker compose build

docker-up:
	docker compose up -d

docker-down:
	docker compose down

docker-logs:
	docker compose logs -f

docker-restart:
	docker compose restart

docker-clean:
	docker compose down -v
	docker system prune -f

# Show help
help:
	@echo "Available commands:"
	@echo "  make nice           - Format, lint and type-check code"
	@echo "  make docker-build   - Build Docker images"
	@echo "  make docker-up      - Start containers in detached mode"
	@echo "  make docker-down    - Stop and remove containers"
	@echo "  make docker-logs    - Show and follow container logs"
	@echo "  make docker-restart - Restart all containers"
	@echo "  make docker-clean   - Remove containers, volumes and clean up"

get-translations:
	uv run manage.py makemessages -a

compile-translations:
	uv run manage.py compilemessages
