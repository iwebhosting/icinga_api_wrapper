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
    base = current_app.config.get('ICINGA_BASE_URL')
    if not base:
        raise ValueError('ICINGA_BASE_URL must be set')
    if not base.endswith('/'):
        base += '/'
    return urlparse.urljoin(base, uri.lstrip('/'))

@cmd.route('/submit_passive', methods=['POST'])
def submit_passive():
    url = get_url('cmd.cgi')
    data = {
        'cmd_typ': '30',
        'cmd_mod': '2',
        'hostservice': '^'.join([request.form['host'], request.form['service']]),
        'plugin_state': RETURN_CODES[request.form['result'].upper()],
        'plugin_output': request.form['output'],
        'performance_data': request.form['perfdata'],
    }
    resp = urllib.urlopen(url, urllib.urlencode(data))
    content = resp.read()
    if 'commitFailed' in content:
        d = {'result': 'failed', 'message': 'Submit failed, bad host/service name?'}
        return jsonify(d), 400
    return jsonify({'result': 'success'}), 201

def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)
    app.config.from_envvar('IAW_SETTINGS', silent=True)
    app.register_blueprint(cmd, url_prefix='/cmd')
    return app

application = app = create_app()
if __name__ == '__main__':
    app.run(debug=True)
