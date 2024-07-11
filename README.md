# RAG-Based Chatbot for Admission FAQ at VinUni

For every admission period, the Registrar's Office at VinUni receives an immeasurable number of questions from applicants and parents. By applying LLM with Retrieval-Augmented Generation (RAG), our project aims to build an effective chatbot system that assists the Registrar and Admission Offices in answering these questions and provides up-to-date, accurate information to parents and students. This helps reduce the workload of VinUni faculties and officers, while still ensuring that information is spread to candidate students and parents on time, ensuring their positive experience towards VinUni service.

This is the project for COMP4020 - NLP, with my teammates:
* Nguyen Khoi: https://github.com/khointn/
* Thao Ha: https://github.com/thaohp113/
* Thai Uyen: https://github.com/TraMiu/

Presentation slide: [Canva](https://www.canva.com/design/DAGHzLsFolo/fEpfItEMt6Mr4qfLfgj6jQ/view?utm_content=DAGHzLsFolo&utm_campaign=designshare&utm_medium=link&utm_source=editor)

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

