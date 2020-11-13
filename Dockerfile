FROM python:3.6

WORKDIR /app

RUN apt-get update \
&& apt-get install -y locales \
&& echo ja_JP.UTF-8 UTF-8 >> /etc/locale.gen \
&& locale-gen \
&& update-locale LANG=ja_JP.UTF-8

RUN pip install --upgrade pip \
&& pip install oauth2client gspread google-api-python-client

# VOLUME /app

ENTRYPOINT [ "/bin/bash" ]

# flask line-bot-sdk