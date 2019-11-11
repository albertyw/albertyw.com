[albertyw.com](https://www.albertyw.com)
========================================

[![Codeship Status for albertyw/albertyw.com](https://codeship.com/projects/74d1ec30-ba55-0133-5935-025ac38368ea/status?branch=master)](https://codeship.com/projects/135665)
[![Updates](https://pyup.io/repos/github/albertyw/albertyw.com/shield.svg)](https://pyup.io/repos/github/albertyw/albertyw.com/)
[![Code Climate](https://codeclimate.com/github/albertyw/albertyw.com/badges/gpa.svg)](https://codeclimate.com/github/albertyw/albertyw.com)
[![codecov](https://codecov.io/gh/albertyw/albertyw.com/branch/master/graph/badge.svg)](https://codecov.io/gh/albertyw/albertyw.com)
[![New Relic Status](https://img.shields.io/badge/New%20Relic-Monitored-blue.svg)](https://rpm.newrelic.com/accounts/565493/applications/)

Personal website

Development
-----------

### Setup (using [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/)):

```bash
mkvirtualenv albertyw -p python3.8
pip install -r requirements.txt
pip install -r requirements-test.txt
ln -s .env.development .env
npm install

# Install shellcheck
# brew install shellcheck
# sudo apt-get install shellcheck
```

### Spinning up the server:

```bash
npm run minify
python app/serve.py
```

### Running tests:
```bash
flake8
mypy app --ignore-missing-imports
shellcheck --exclude=SC1091 bin/*.sh
coverage run -m unittest discover
npm test
```

CI/CD
-----

This repo uses:

```bash
# Setup
pyenv local 3.8
pip install -r requirements.txt
pip install -r requirements-test.txt
ln -s .env.development .env

# Test
flake8
mypy app --ignore-missing-imports
coverage run -m unittest discover
coverage report
codeclimate-test-reporter
npm test

# Deployment
ssh ubuntu@direct.albertyw.com website/bin/deploy.sh
```

### Building and starting the docker container

```bash
docker build -t albertyw.com:test .
docker run -t -i -p 127.0.0.1:5000:5000 albertyw.com:test
```

Production
----------

### Setup

```bash
bin/setup.sh
```

### Deployment

```bash
bin/deploy.sh
```
