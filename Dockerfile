FROM python:3
ENV LANG C.UTF-8

MAINTAINER Songpon Imyen "t.songpon@gmail.com"

RUN mkdir /django_challenge

RUN apt-get -y update
RUN apt-get install -y python python3-pip python-dev postgresql-client

ADD requirements.txt /django_challenge/requirements.txt
RUN pip install -r /django_challenge/requirements.txt

RUN apt-get -y update && apt-get -y autoremove
ADD . /django_challenge/
WORKDIR /django_challenge

EXPOSE 8000

CMD python3 manage.py runserver 0.0.0.0:8000