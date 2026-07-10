#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Install dependencies bypassing the externally-managed environment restriction
python3 -m pip install -r requirements.txt --break-system-packages

# Run database migrations
python3 manage.py migrate --noinput

# Collect static files
python3 manage.py collectstatic --noinput --clear