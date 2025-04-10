# Django with Docker Compose and PostgreSQL

This is a **Medical Center** web application built with **Django**, using **Docker Compose** for containerization and **PostgreSQL** as the database. The app is currently under development, with features related to patient management, appointments, and medical records. This template provides an easy way to set up the development environment using Docker.

## Requirements

- **Docker**: Use Docker to build and run the containers.
- **Docker Compose**: Tool for managing multi-container Docker applications.
- **Make**: A tool to automate tasks.
- **Python 3.x** and **Django**.

## Requirements

- **[Docker](https://www.docker.com/)**: A platform used for building, running, and shipping applications inside containers.
- **[Docker Compose](https://docs.docker.com/compose/)**: A tool for defining and running multi-container Docker applications.
- **[Make](https://www.gnu.org/software/make/)**: A build automation tool that helps automate tasks like starting services, building code, or running tests.


## Installation and Setup

1. Clone the repository:
   
   ```bash
   git clone https://github.com/143life/med_center.git
   cd your-project-directory

2. Install all required packages in 'Requirements' section

### Implemented Commands

* 'make app' - up application and db infrastructure
* 'make app-down' - down application and all infrastructure
* 'make app-logs' - follow the logs to app container
* 'make storages' - up only storages. you should run your application locally to debug/develop for debugging/development purposes
* 'make storages-down' - down all infrastructure
* 'make storages-logs' - follow the logs in storages containers

### Most Used Django Specific Commands

* 'make migrations' - make migrations to models
* 'make migrate' - apply all made migrations
* 'make collectstatic' - collect static
* 'make superuser' - create admin user