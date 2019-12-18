FROM python:3.7

ENV PYTHONUNBUFFERED 1

COPY ./init_db.py  ./requirements.txt /
RUN pip install --no-cache-dir -r requirements.txt

ENV APP_MODE PROD

COPY ./start.sh /
RUN chmod +x /start.sh

CMD ["/start.sh"]
