FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

RUN pip install --no-cache-dir SQLAlchemy \
                               GeoAlchemy2 \
                               psycopg2-binary \
                               requests

COPY app /app
