# pull official base image
FROM python:3.11.3-slim-buster

# set work directory
WORKDIR /usr/src/app


# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY ./app .
COPY ./data ./data

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
