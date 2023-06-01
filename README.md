# test-fastapi

## Backend Requirements

* [Docker](https://www.docker.com/).
* [Docker Compose](https://docs.docker.com/compose/install/).
* [Poetry](https://python-poetry.org/) for Python package and environment management.


## Folder Structure
- **Scripts** Here are scripts which get exectuted inside the `docker-compose.override.yml`.
  - scripts come from template repository.
  - Not touched for current development.
  - Needed for the proper docker compose.
- **Backend** Actual backend code
  - `backend.dockerfile` for the backend image
  - app folder for the actual code
    - alembic: folder for alchemist framework for db management
      - `env.py`:manages env for the DB
      - versions folder: revisiong of the DB versions
    - app
    - scripts


## Dockerization
Docker compose is used to orchastrate 4 images. Traefik is used for service-to-service communication. 

In `dockercompose.yml` all four images are created
- backend (contained in ./backend)
- PostgreSQL (pull prebuild image)
- PGAdmin (pull prebuild image)
- Network proxy (pull prebuild image)


## Environment Setup
The `.env` file contains the environment settings, which are passed in the `dockercompose.yml` to the respective images. In the image itself the environment variables
can be accessed via
```
import os
os.environ.get("ENV_VAR")
```


## Backend local development

* Build images and start the stack with Docker Compose:

```bash
docker-compose up -d
```

* Now you can open your browser and interact with these URLs:

Backend, JSON based web API based on OpenAPI: http://localhost/api/

Automatic interactive documentation with Swagger UI (from the OpenAPI backend): http://localhost/docs

Alternative automatic documentation with ReDoc (from the OpenAPI backend): http://localhost/redoc

PGAdmin, PostgreSQL web administration: http://localhost:5050

**Note**: The first time you start your stack, it might take a minute for it to be ready. While the backend waits for the database to be ready and configures everything. You can check the logs to monitor it.

To check the logs, run:

```bash
docker-compose logs
```

To check the logs of a specific service, add the name of the service, e.g.:

```bash
docker-compose logs backend
```


## Database Development

### Database Schemas
DB Schemas are maintained in `app/app/models`. One files creates one table.

The folder structure is as follows:
- `app/app/models`: contains all table schemas which are relevant throught the whole app
- `app/app/models/<app-module>`: contains all table schemas which are relevant for the mentioned app-module

### Performing CRUD operations
CRUD opterations are maintained in `app/app/crud`. 
- `base.py`: Parent class for all CRUD operations on specific tables. Contains the general logic which needs to be parameterized by the child classes
   for a given table
- folder / file structure identical to `app/app/models` folder since it follows also the one files per table policy.


### DB Alchemist Maintenance
In the folder `app/app/db` all tables need to be mentioned in order to be picked up and properly being updated.
- `base.py`:list all models
- `init_db.py`: update tables during deployment without creating a new revision



### Database Updates in running images
To execute the changes while the image is running, the following commands are needed:
```
cd <root>/service-main
docker-compose exec backend bash
alembic revision --autogenerate -m "<Comment for changes>"
```


## API Development

### API Data Models
API data models are maintained in `app/app/schemas`. App-wide files are directly contained in this folder. Files, which are relevant for specific modules
are contained in a subfolder for that module. **Follows the same file / folder structure as `app/app/models`**.

### Common API functionality
Functionality that is used in more than just one specific end-point is contained in the folder `app/app/core`. In particular, this folder contains
- the recommendation logic

### API end-points
The API end-points are defined in the folder `app/app/api`.
- `deps.py`: contains information about the current users
- `api_v1/api.py`: contains the routers to the sub-areas
- `api_v1/endpoints`: folder containing the actual endpoints. Structure follows the folder `app/app/models`.


### Login
- The folder `app/app/email-templates` contains the functionality to reset the user token with email and password.
