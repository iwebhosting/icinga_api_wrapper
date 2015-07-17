#!/usr/bin/env python
from flask import Flask, request, current_app, jsonify, Blueprint
import urllib
import urlparse

RETURN_CODES = {
    'OK': '0',
    'WARNING': '1',
    'CRITICAL': '2',
    'UNKNOWN': '3',
}

class Config(object):
    DEBUG = False
    ICINGA_BASE_URL = ''


cmd = Blueprint('cmd', __name__)

def get_url(uri):
    return urlparse.urljoin(current_app.config['ICINGA_BASE_URL'], uri)

@cmd.route('/submit_passive', methods=['POST'])
def submit_passive():
    url = get_url('/cmd.cgi')
    data = {
    }
    resp = urllib.urlopen(url, urllib.urlencode(data))
    return ''

def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)
    app.config.from_envvar('IAW_SETTINGS', silent=True)
    app.register_blueprint(cmd, url_prefix='/cmd')
    return app

application = app = create_app()
if __name__ == '__main__':
    app.run(debug=True)
