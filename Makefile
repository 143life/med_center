DC = docker compose
STORAGES_FILE = docker_compose/storages.yaml
QUEUE_FILE = docker_compose/queue.yaml
EXEC = docker exec -it
DB_CONTAINER = medcenter-db
APP_CONTAINER = main-app
LOGS = docker logs
ENV = --env-file .env
ENV_PROD = --env-file .env.prod
DB = med_center
DB_USER = my_user
APP_FILE = docker_compose/app.yaml
PROD_BUILD_FILE = docker_compose/docker-compose.build.yaml
PROD_FILE = docker_compose/docker-compose.prod.yaml
MANAGE_PY = python manage.py

.PHONY: build-prod
build-prod:
	${DC} -f ${PROD_BUILD_FILE} ${ENV_PROD} build

.PHONY: app-prod
app-prod:
	${DC} -f ${PROD_FILE} ${ENV_PROD} up --build -d

.PHONY: prod-down
prod-down:
	${DC} -f ${PROD_FILE} down

.PHONY: build
build:
	${DC} -f ${APP_FILE} ${ENV} build

.PHONY: storages
storages:
	${DC} -f ${STORAGES_FILE} ${ENV} up -d

.PHONY: storages-down
storages-down:
	${DC} -f ${STORAGES_FILE} down

.PHONY: postgres
postgres:
	${EXEC} ${DB_CONTAINER} psql -U ${DB_USER} ${DB}

.PHONY: app
app:
	${DC} -f ${STORAGES_FILE} -f ${APP_FILE} ${ENV} up --build -d

.PHONY: queue
queue:
	${DC} -f ${QUEUE_FILE} up --build -d

.PHONY: storages-logs
storages-logs:
	${LOGS} ${DB_CONTAINER} -f

.PHONY: app-logs
app-logs:
	${LOGS} ${APP_CONTAINER} -f

.PHONY: app-down
app-down:
	${DC} -f ${APP_FILE} -f ${STORAGES_FILE} down

.PHONY: app-in
app-in:
	${EXEC} ${APP_CONTAINER} ash

.PHONY: migrate
migrate:
	${EXEC} ${APP_CONTAINER} ${MANAGE_PY} migrate

.PHONY: migrations
migrations:
	${EXEC} ${APP_CONTAINER} ${MANAGE_PY} makemigrations

.PHONY: showmigrations
showmigrations:
	${EXEC} ${APP_CONTAINER} ${MANAGE_PY} showmigrations

.PHONY: superuser
superuser:
	${EXEC} ${APP_CONTAINER} ${MANAGE_PY} createsuperuser

.PHONY: collectstatic
collectstatic:
	${EXEC} ${APP_CONTAINER} ${MANAGE_PY} collectstatic
