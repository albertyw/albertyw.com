[albertyw.com](https://www.albertyw.com)
========================================

[ ![Codeship Status for albertyw/albertyw.com](https://codeship.com/projects/74d1ec30-ba55-0133-5935-025ac38368ea/status?branch=master)](https://codeship.com/projects/135665)
[![Dependency Status](https://gemnasium.com/badges/github.com/albertyw/albertyw.com.svg)](https://gemnasium.com/github.com/albertyw/albertyw.com)
[![Code Climate](https://codeclimate.com/github/albertyw/albertyw.com/badges/gpa.svg)](https://codeclimate.com/github/albertyw/albertyw.com)
[![codecov](https://codecov.io/gh/albertyw/albertyw.com/branch/master/graph/badge.svg)](https://codecov.io/gh/albertyw/albertyw.com)
[![New Relic Status](https://img.shields.io/badge/New%20Relic-Monitored-blue.svg)](https://rpm.newrelic.com/accounts/565493/applications/)

Personal website

Development
-----------

With virtualenvwrapper:
```bash
mkvirtualenv albertyw -p python3.5
pip install -r requirements.txt
ln -s .env.development .env
python app/serve.py
```

Testing
-------

```bash
pip install -r requirements-test.txt
cd app
coverage run -m unittest discover
```

Production
----------

```bash
ln -s .env.production .env
bin/setup.sh
```
