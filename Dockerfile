FROM python:3.6

WORKDIR /app

RUN apt-get update

RUN pip install --upgrade pip \
&& pip install oauth2client gspread

# VOLUME /app

ENTRYPOINT [ "/bin/bash" ]

# flask line-bot-sdk