# Django with Docker Compose and PostgreSQL

This is a **Medical Center** web application built with **Django**, using **Docker Compose** for containerization and **PostgreSQL** as the database. The app is currently under development, with features related to patient management, appointments, and medical records. This template provides an easy way to set up the development environment using Docker.

## Requirements

- **[Docker](https://www.docker.com/)**: A platform used for building, running, and shipping applications inside containers.
- **[Docker Compose](https://docs.docker.com/compose/)**: A tool for defining and running multi-container Docker applications.
- **[Make](https://www.gnu.org/software/make/)**: A build automation tool that helps automate tasks like starting services, building code, or running tests.

## Installation and Setup

### Ubuntu
1. Install Docker:
**[Docker](https://docs.docker.com/engine/install/ubuntu/)**

2. Post-Installation Steps:
**[Manage Docker as a non-root user](https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user)**

3. For Makefile:
   ```bash
   sudo apt install make

4. Clone the repository:
   
   ```bash
   git clone https://github.com/143life/med_center.git
   cd your-project-directory

5. In project directory create file .env:
   ```bash
   DJANGO_SECRET_KEY=my_secretkey
   DJANGO_PORT=8000
   POSTGRES_DB=container_name_db
   POSTGRES_USER=my_user
   POSTGRES_PASSWORD=my_password
   POSTGRES_PORT=5432
   POSTGRES_HOST=my_service

6. Start app:
   ```bash
   make build
   make app
   make migrate
   make superuser
   make collectstatic

### Windows

In development...

### Implemented Commands

* 'make build' - build app-container
* 'make app' - up application and db infrastructure
* 'make app-down' - down application and all infrastructure
* 'make app-logs' - follow the logs to app container
* 'make storages' - up only storages. you should run your application locally to debug/develop for debugging/development purposes
* 'make storages-down' - down all infrastructure
* 'make storages-logs' - follow the logs in storages containers

### Most Used Django Specific Commands

* 'make collectstatic' - collect static
* 'make migrations' - make migrations to models
* 'make migrate' - apply all made migrations
* 'make showmigrations' - show all migrations
* 'make superuser' - create admin user