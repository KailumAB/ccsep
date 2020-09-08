#!/bin/bash
flask db upgrade
node pptr.js &
exec gunicorn -b :8000 --access-logfile - --error-logfile - vulnerable_app:app
