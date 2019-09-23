# Needed for python 3.7
FROM ubuntu:18.04

LABEL maintainer="git@albertyw.com"
EXPOSE 5000

ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# Set up directory structures
RUN mkdir -p /var/www/app
COPY . /var/www/app
WORKDIR /var/www/app

# Download static files
RUN bin/container_setup.sh

# Set startup script
CMD ["bin/start.sh"]
