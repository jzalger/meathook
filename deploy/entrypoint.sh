#!/bin/bash
exec pipenv run gunicorn --config gunicorn_config.py meathook_web.wsgi:meathook_app
