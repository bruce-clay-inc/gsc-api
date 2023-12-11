#!/bin/sh

# Script to ensure the app is setup, up-to-date and restart services if needed.

POETRY="/home/ubuntu/.local/bin/poetry"
PROJECT="/home/ubuntu/gsc-api"

cd "$PROJECT"

# Install Dependencies
$POETRY install --without=dev --no-root

# Django stuff
cd gsc
$POETRY run python manage.py migrate

# Gunicorn and Webserver activation
sudo cp $PROJECT/scripts/confs/nginx.conf /etc/nginx/sites-available/gsc-api
sudo cp $PROJECT/scripts/confs/gsc-api.service /etc/systemd/system/gsc-api.service
sudo cp $PROJECT/scripts/confs/gsc-api.socket /etc/systemd/system/gsc-api.socket

sudo systemctl daemon-reload
sudo systemctl restart gsc-api.service

sudo service nginx reload