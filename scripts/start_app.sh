#!/bin/bash
cd /home/ubuntu/django-app
source venv/bin/activate
# अगर Gunicorn है तो उसे restart करो, वरना test के लिए runserver:
nohup python manage.py runserver 0.0.0.0:8000 > /dev/null 2>&1 &
