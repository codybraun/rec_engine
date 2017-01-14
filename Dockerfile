FROM ubuntu:14.04
COPY . /var/opt/
RUN sudo apt-get update 
RUN sudo apt-get -y install python-django python-pip  
RUN cd /var/opt & ls
RUN DJANGO_LOG_LEVEL=DEBUG SQLPW=3312crystal python manage.py runserver 8000
