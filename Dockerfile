FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update -y
RUN apt-get -y install binutils libproj-dev gdal-bin python3-lxml
RUN apt-get -y install libmemcached-dev
RUN apt-get -y install redis

RUN mkdir /code
WORKDIR /code

ADD requirements.txt /code/

RUN pip install -r requirements.txt

ADD . /code/
