FROM ubuntu:16.04
COPY ./ /var/opt/app
RUN apt-get update 
RUN apt-get -y install python-pip libpq-dev python-dev build-essential postgresql-server-dev-all
RUN pip install django djangorestframework psycopg2 numpy requests django-rest-swagger
EXPOSE 8000
ENTRYPOINT DJANGO_LOG_LEVEL=DEBUG SQLPW=3312crystal python /var/opt/app/manage.py runserver 8000
