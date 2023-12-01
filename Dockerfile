# pull official base image
FROM python:3.11.3-slim-buster

# set work directory
WORKDIR /usr/src/app


# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY ./app .

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy the entrypoint script
COPY entrypoint.sh /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh
# Set the entrypoint script
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
