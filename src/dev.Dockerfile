FROM python:3.7

RUN pip install --no-cache-dir fastapi \
                               uvicorn \
                               SQLAlchemy \
                               GeoAlchemy2 \
                               psycopg2-binary \
                               requests

COPY ./prestart.sh /prestart.sh
RUN chmod +x /prestart.sh
RUN /prestart.sh

WORKDIR /app/
ENV PYTHONPATH=/app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
