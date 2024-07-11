# RAG-Based Chatbot for Admission FAQ at VinUni

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

#### Requirements
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

## References

This project is done based on:
* PrivateGPT repo: https://github.com/zylon-ai/private-gpt/
* Weaviate: https://weaviate.io/developers/weaviate
* Telegram API: https://core.telegram.org/bots/api
* pyTelegramBotAPI: https://github.com/eternnoir/pyTelegramBotAPI
* My capstone teammates.

