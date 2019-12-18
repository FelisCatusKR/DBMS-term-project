FROM python:3.7

ENV PYTHONUNBUFFERED 1

COPY ./init_db.py ./requirements.txt /
RUN pip install --no-cache-dir -r requirements.txt

ENV APP_MODE DEV

COPY ./start-reload.sh ./customers.csv ./drugs.csv /
RUN chmod +x /start-reload.sh

CMD ["/start-reload.sh"]
