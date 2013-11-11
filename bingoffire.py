import os
import logging
from logging.handlers import RotatingFileHandler
from logging import Formatter
from logging import Logger
import time

import flask

LOG_SIZE = 1024 ** 2
LOG_FORMAT = Formatter(
    '%(asctime)s [%(levelname)s] : %(message)s'
)

log_to_file = RotatingFileHandler('app', maxBytes=LOG_SIZE)
log_to_file.setLevel(logging.INFO)
log_to_file.setFormatter(LOG_FORMAT)

app = flask.Flask(__name__)
app.logger.addHandler(log_to_file)

_access_log = logging.getLogger('bingoffire')
_access_log_file = RotatingFileHandler('access', maxBytes=LOG_SIZE)
_access_log.setLevel(logging.INFO)
#_access_log.setFormatter(LOG_FORMAT)
_access_log.addHandler(_access_log_file)


@app.after_request
def write_access_log(response):
    req = flask.request
    _access_log.info(' - '.join((str(m) for m in (time.asctime(), req.method, req.path, response.status_code))))
    return response


@app.route('/')
def index():
    return _send_file('', 'index.html')


@app.route('/catering')
def catering():
    return _send_file('', 'catering.html')


@app.route('/gallery')
def gallery():
    return _send_file('', 'gallery.html')


@app.route('/js/<path:filename>')
def deliver_js(filename):
    flask.g.is_static = True
    return _send_file('/js', filename)


@app.route('/css/<path:filename>')
def deliver_css(filename):
    flask.g.is_static = True
    return _send_file('/css', filename)


@app.route('/img/<path:filename>')
def deliver_img(filename):
    flask.g.is_static = True
    return _send_file('/img', filename)


@app.route('/img/<filename>.png')
def png_files(filename):
    flask.g.is_static = True
    return _send_file('/img', filename + '.png', mimetype='image/png')


@app.route('/favicon.ico')
def favicon():
    flask.g.is_static = True
    return _send_file('/img', 'favicon.ico', mimetype='image/vnd.microsoft.icon', as_attachment=False)


def _send_file(directory, filename, **options):
    directory = app.root_path + '/static' + directory
    return flask.send_from_directory(directory, filename, **options)
