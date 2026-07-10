#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Install your dependencies
python3 -m pip install -r requirements.txt

# Run your database migrations so 'auth_user' is created
python3 manage.py migrate --noinput

# Collect static files so your CSS/JS loads correctly
python3 manage.py collectstatic --noinput --clear