FROM python:3.10.10-slim

COPY ./requirements.txt /

RUN apt-get update

RUN apt-get install -y libpq-dev gcc

RUN pip install -r /requirements.txt

ENV TZ="Asia/Taipei"