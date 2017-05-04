#!/bin/bash

# This script is meant to be run on a server with the production app running.
# It can be called from a CI/CD tool like Codeship.

# Update repository
cd /var/www/albertyw.com/ || exit 1
git checkout master
git pull

# Update python packages
virtualenvlocation=$(which virtualenvwrapper.sh)
# shellcheck source=/dev/null
source "$virtualenvlocation"
workon "albertyw.com"
pip install -r requirements.txt

# Make generated static file directory writable
sudo chown www-data app/static/gen
sudo chown www-data app/static/.webassets-cache

# Download static files
wget https://github.com/albertyw/resume/raw/master/resume.pdf
mv resume.pdf app/static/gen/resume.pdf

# Restart services
sudo service nginx restart
sudo systemctl restart albertyw.com-uwsgi
