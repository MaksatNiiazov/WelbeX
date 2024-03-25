#!/bin/bash

python manage.py migrate

python manage.py import_from_excel uszips.csv

python manage.py runserver 0.0.0.0:8000
