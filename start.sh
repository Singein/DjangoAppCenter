#!/bin/bash
python3 DjangoAppCenter dev makemigrations
gunicorn DjangoAppCenter.wsgi:application -c gunicorn.conf.py