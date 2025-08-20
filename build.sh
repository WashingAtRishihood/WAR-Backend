#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input

# Generate migrations
python manage.py makemigrations --no-input

# Apply migrations
python manage.py migrate --no-input

python manage.py ensure_superuser