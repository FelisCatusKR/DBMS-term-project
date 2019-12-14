FROM python:3.7

RUN pip install --no-cache-dir fastapi \
                               uvicorn \
                               SQLAlchemy \
                               GeoAlchemy2 \
                               psycopg2-binary \
                               requests

ENV PYTHONPATH=/app

COPY ./init_db.py ./customers.csv ./drugs.csv ./start.sh /
CMD chmod +x /start.sh

CMD ["/start.sh"]
