#!/usr/bin/env bash
export DJANGO_SETTINGS_MODULE=backend.backend.settings
export PYTHONPATH=/opt/render/project/src

pip install -r requirements.txt
python backend/manage.py collectstatic --noinput
python backend/manage.py migrate
