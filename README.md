# [albertyw.com](https://www.albertyw.com)

[![Build Status](https://drone.albertyw.com/api/badges/albertyw/albertyw.com/status.svg)](https://drone.albertyw.com/albertyw/albertyw.com)
[![Updates](https://pyup.io/repos/github/albertyw/albertyw.com/shield.svg)](https://pyup.io/repos/github/albertyw/albertyw.com/)
[![Code Climate](https://codeclimate.com/github/albertyw/albertyw.com/badges/gpa.svg)](https://codeclimate.com/github/albertyw/albertyw.com)
[![Test Coverage](https://api.codeclimate.com/v1/badges/a41593e78d63ae7ec7d6/test_coverage)](https://codeclimate.com/github/albertyw/albertyw.com/test_coverage)
[![Varsnap Status](https://www.varsnap.com/project/6bf37bef-44a3-4c93-947b-47a21f2d3f3a/varsnap_badge.svg)](https://www.varsnap.com/project/6bf37bef-44a3-4c93-947b-47a21f2d3f3a/)

Personal website

## Development

### Setup (using [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/))

```bash
mkvirtualenv albertyw -p python3.10
pip install -r requirements.txt
pip install -r requirements-test.txt
ln -s .env.development .env
npm install

# Install shellcheck
# brew install shellcheck
# sudo apt-get install shellcheck
```

### Spinning up the server

```bash
npm run minify
python app/serve.py
```

### Running tests

```bash
flake8
mypy app --ignore-missing-imports --strict --allow-untyped-decorators
shellcheck --exclude=SC1091 bin/*.sh
coverage run -m unittest discover
npm test
```

## CI/CD

This repo uses:

```bash
# Setup
pyenv local 3.10
pip install -r requirements.txt
pip install -r requirements-test.txt
ln -s .env.development .env

# Test
flake8
mypy app --ignore-missing-imports --strict --allow-untyped-decorators
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

## Production

### Setup

Run this once on a new server to set up the web app:

```bash
bin/setup.sh
```

### Deployment

Run this every time for a new commit to the repository:

```bash
bin/deploy.sh
```
