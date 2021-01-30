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

# gcloud install layer
# Downloading gcloud package
RUN curl https://dl.google.com/dl/cloudsdk/release/google-cloud-sdk.tar.gz > /tmp/google-cloud-sdk.tar.gz
# Installing the package
RUN mkdir -p /usr/local/gcloud \
  && tar -C /usr/local/gcloud -xvf /tmp/google-cloud-sdk.tar.gz \
  && /usr/local/gcloud/google-cloud-sdk/install.sh
# Adding the package path to local
ENV PATH $PATH:/usr/local/gcloud/google-cloud-sdk/bin

# flask line-bot-sdk