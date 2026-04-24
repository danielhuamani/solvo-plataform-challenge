
COMPOSE_FILE := docker/local/docker-compose.yml

.PHONY: build up up-d down manage startapp

build:
	docker compose -f $(COMPOSE_FILE) build

up:
	docker compose -f $(COMPOSE_FILE) up

up-d:
	docker compose -f $(COMPOSE_FILE) up -d

down:
	docker compose -f $(COMPOSE_FILE) down

manage:
	docker compose -f $(COMPOSE_FILE) exec web python manage.py $(cmd)

superuser:
	docker compose -f $(COMPOSE_FILE) exec web python manage.py createsuperuser

startapp:
	docker compose -f $(COMPOSE_FILE) exec web sh -c "mkdir -p apps/$(name) && python manage.py startapp $(name) apps/$(name)"

lint:
	docker compose -f $(COMPOSE_FILE) exec web ruff check .

format:
	docker compose -f $(COMPOSE_FILE) exec web ruff format .

# examples:
# make manage cmd="migrate"
# make manage cmd="createsuperuser"
# make manage cmd="shell"
# make startapp name="mi_app"
# make superuser
