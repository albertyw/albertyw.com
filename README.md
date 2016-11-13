[albertyw.com](https://www.albertyw.com)
========================================

[ ![Codeship Status for albertyw/albertyw.com](https://codeship.com/projects/74d1ec30-ba55-0133-5935-025ac38368ea/status?branch=master)](https://codeship.com/projects/135665)
[![Code Climate](https://codeclimate.com/github/albertyw/albertyw.com/badges/gpa.svg)](https://codeclimate.com/github/albertyw/albertyw.com)
[![codecov](https://codecov.io/gh/albertyw/albertyw.com/branch/master/graph/badge.svg)](https://codecov.io/gh/albertyw/albertyw.com)
[![New Relic Status](https://img.shields.io/badge/New%20Relic-Monitored-blue.svg)](https://rpm.newrelic.com/accounts/565493/applications/)

Personal website

Development
-----------

With virtualenvwrapper:
```
mkvirtualenv albertyw -p python3.5
pip install -r requirements.txt
python app/serve.py
```

Testing
-------

```
cd app
python -m unittest
```
