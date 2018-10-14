FROM ubuntu:18.04
LABEL maintainer="git@albertyw.com"
EXPOSE 5000

# Install updates and system packages
RUN apt-get update && apt-get install -y \
    build-essential \
    locales \
    software-properties-common

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
