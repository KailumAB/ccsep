#!/bin/sh
cd /usr/src/app/migrations
alembic upgrade head
cd /usr/src/app
python -m flask run --host=0.0.0.0
