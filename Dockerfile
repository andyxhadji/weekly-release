FROM python:3.6-slim

RUN apt-get update; apt-get install -y curl

RUN pip install fastapi uvicorn

#RUN pip install --upgrade pip

#RUN pip install --default-timeout=100 cryptography==2.1.0

#RUN pip install --default-timeout=100 requests[security]==2.25.0

#COPY ./app/requirements.txt /app/requirements.txt

#RUN pip install --default-timeout=100 -r /app/requirements.txt
ENV PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring


# Install Poetry
#RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
#    cd /usr/local/bin && \
#    ln -s /opt/poetry/bin/poetry && \
#    poetry config virtualenvs.create false

# Copy using poetry.lock* in case it doesn't exist yet
COPY ./app/app.toml ./app/poetry.lock* /app/

#RUN poetry install --no-root --no-dev

EXPOSE 80

COPY ./app /app

COPY google_credentials.json /app/google_credentials.json

COPY config.json /app/config.json

#RUN sed -i "s|from urllib import quote_plus|from urllib.parse import quote_plus |g" /usr/local/lib/python3.6/site-packages/trello/__init__.py

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
