#!/bin/bash

# Update repository
cd /var/www/website/
git pull

# Update python packages
source `which virtualenvwrapper.sh`
workon albertyw.com
pip install -r requirements.txt

# Configure settings
cd albertyw.com
ln -sf prod_settings.py settings.py

# Restart services
sudo service nginx restart
sudo service uwsgi restart
