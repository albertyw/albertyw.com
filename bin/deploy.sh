#!/bin/bash

# Update repository
cd /var/www/website/
git checkout master
git pull

# Update python packages
virtualenvlocation=$(which virtualenvwrapper.sh)
# shellcheck source=/dev/null
source "$virtualenvlocation"
workon albertyw.com
pip install -r requirements.txt

# Configure settings
cd albertyw.com
ln -sf .env.production .env

# Restart services
sudo service nginx restart
sudo service uwsgi restart
