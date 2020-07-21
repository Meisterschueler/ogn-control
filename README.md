# ogn-control

[![Build Status](https://travis-ci.org/Meisterschueler/ogn-control.svg?branch=master)](https://travis-ci.org/Meisterschueler/ogn-control)
[![PyPi Version](https://img.shields.io/pypi/v/ogn-control.svg)](https://pypi.python.org/pypi/ogn-control)
[![Coverage Status](https://coveralls.io/repos/github/Meisterschueler/ogn-control/badge.svg?branch=master)](https://coveralls.io/github/Meisterschueler/ogn-control?branch=master)

A python3 module for the [Open Glider Network](http://wiki.glidernet.org/).
It runs on the receiver and visualizes the incoming data


## Installation

Clone the repository

```
git clone https://github.com/Meisterschueler/ogn-control
```

Create a virtual environment (not nessecary, but recommended) and activate

```
python3 -m venv my_environment
source my_environment/bin/activate
```

Install all the packages we need

```
pip install -r requirements.txt
```

Start the flask server

```
export FLASK_APP=ogn_control.py
flask run --port=5000 --host=0.0.0.0
```

The application is now running on port 5000 (port is 5000 per default) and is accessible from every ip (host is 127.0.0.1 per default,
this restricts access to localhost). It proceeds the raw data directly from port 50001 (default port of ogn-decode process).
If you want to develop, set the Flask environment from production (default) to development before starting Flask.

```
export FLASK_ENV=development
```

Now instead of realtime data from OGN receiver data from logfile "app/telnet_logfile.txt" is proceeded.


## License
Licensed under the [AGPLv3](LICENSE).
