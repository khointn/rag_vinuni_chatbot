# NLP Project

## Requirements

* [Docker](https://www.docker.com/).
* [Docker Compose](https://docs.docker.com/compose/install/).
* [Poetry](https://python-poetry.org/) for Python package and environment management.


## Installation

### Set up virtual environment

```shell
python -m venv venv
. venv/bin/activate
```

### Install dependencies

- Install poetry: https://python-poetry.org/
- Install dependencies

```shell
poetry install
```

#### Local Requirements
```shell
poetry install --with local
```

Download embedding and(or) LLM models
```shell
python setup.py
```

### Install `pre-commit` hooks

```shell
pre-commit install
```

## Running
```shell
docker compose up -d
poetry run python -m app
```

## URLs
### Development URLs
#### Gradio UI
http://localhost:8000

#### API Documentation
http://localhost:8000/docs
