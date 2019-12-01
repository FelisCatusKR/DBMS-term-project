FROM python:3.7

RUN pip install --no-cache-dir fastapi \
                               uvicorn \
                               SQLAlchemy \
                               psycopg2-binary

COPY ./app /app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]
