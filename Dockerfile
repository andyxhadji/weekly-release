FROM python:3.6-slim

RUN apt-get update; apt-get install -y curl

RUN apt-get install gcc -y

RUN apt-get install build-essential libssl-dev libffi-dev python-dev -y

ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    \
    # poetry
    # https://python-poetry.org/docs/configuration/#using-environment-variables
    POETRY_VERSION=1.0.3 \
    # make poetry install to this location
    POETRY_HOME="/opt/poetry" \
    # make poetry create the virtual environment in the project's root
    # it gets named `.venv`
    #POETRY_VIRTUALENVS_IN_PROJECT=true \
    # do not ask any interactive question
    POETRY_NO_INTERACTION=1 \
    # paths
    # this is where our requirements + virtual environment will live
    PYSETUP_PATH="./app/" \
    VENV_PATH="/opt/pysetup/.venv"

# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python

RUN poetry config virtualenvs.create false

COPY ./app/pyproject.toml ./app/poetry.lock* /

RUN poetry install --no-dev

EXPOSE 80

COPY ./app /app

COPY google_credentials.json /app/google_credentials.json

COPY config.json /app/config.json

RUN sed -i "s|from urllib import quote_plus|from urllib.parse import quote_plus |g" /usr/local/lib/python3.6/site-packages/trello/__init__.py

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--timeout-keep-alive", "60"]
