SHELL := /bin/bash

flask-app-1:
	source ./venv/bin/activate && \
	cd ./flask_app_1 && \
    gunicorn -c gunicorn.conf.py demo_app:app

django-app-1:
	source ./venv/bin/activate && \
	cd ./django_app_1 && \
    gunicorn -c gunicorn.conf.py app.wsgi

flask-app-2:
	source ./venv/bin/activate && \
	cd ./flask_app_2 && \
    gunicorn -c gunicorn.conf.py demo_app:app
