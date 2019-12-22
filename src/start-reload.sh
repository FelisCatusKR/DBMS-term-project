#! /usr/bin/env sh

# Let the DB start
sleep 10;

# Run database initializing
python /init_db.py

exec uvicorn app.main:app --port 80 --host 0.0.0.0 --reload
