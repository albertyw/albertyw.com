FROM ubuntu:18.04
LABEL maintainer="git@albertyw.com"
EXPOSE 5000

# Install updates and system packages
RUN apt-get update -y
RUN apt-get install -y build-essential python-minimal python3-dev python3-setuptools curl supervisor locales

# Set locale
RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# Set up directory structures
RUN mkdir -p /var/www/app
COPY . /var/www/app
WORKDIR /var/www/app
RUN ln -fs .env.production .env

# Set up python
RUN curl https://bootstrap.pypa.io/get-pip.py | python3
RUN pip3 install virtualenvwrapper
RUN pip3 install -r requirements.txt

# Download static files
RUN bin/container_setup.sh

COPY config/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

ENTRYPOINT ["bin/start.sh"]
