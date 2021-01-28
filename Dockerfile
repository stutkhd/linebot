FROM python:3.6

WORKDIR /app

RUN apt-get update \
&& apt-get install -y locales \
&& echo ja_JP.UTF-8 UTF-8 >> /etc/locale.gen \
&& locale-gen \
&& update-locale LANG=ja_JP.UTF-8

COPY ./requirements.txt /app/

RUN pip install -U pip \
    && pip install -r requirements.txt

# flask line-bot-sdk