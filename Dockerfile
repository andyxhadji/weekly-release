FROM python:3.7

RUN pip install fastapi uvicorn

RUN pip install --upgrade pip

COPY ./app/requirements.txt /app/requirements.txt

RUN pip install --default-timeout=100 -r /app/requirements.txt


EXPOSE 80

COPY ./app /app

COPY google_credentials.json /app/google_credentials.json

COPY config.json /app/config.json

RUN sed -i "s|from urllib import quote_plus|from urllib.parse import quote_plus |g" /usr/local/lib/python3.7/site-packages/trello/__init__.py

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
