import os
import logging
from logging.handlers import RotatingFileHandler
from logging import Formatter
from logging import Logger
import time
import sys

import flask

LOG_FORMAT = Formatter(
    '%(asctime)s [%(levelname)s] : %(message)s'
)

log_to_stdout = logging.StreamHandler(sys.stdout)
log_to_stdout.setLevel(logging.DEBUG)
log_to_stdout.setFormatter(LOG_FORMAT) 

app = flask.Flask(__name__)
app.logger.addHandler(log_to_stdout)

_PAGE_CACHE = 5 * 60
_ASSET_CACHE = 5 * 60 * 60


def main():
    port = int(os.environ.get('PORT', 4000))
    app.run(host="0.0.0.0", port=port, debug=True, use_reloader=True)


@app.after_request
def set_caching(response):
    #response.headers['Cache-Control'] = 'public, max-age=3600'
    return response


@app.route('/')
def index():
    return _send_file('', 'index.html', cache_timeout=_PAGE_CACHE)


@app.route('/contact')
def catering():
    return _send_file('', 'contact.html', cache_timeout=_PAGE_CACHE)


@app.route('/gallery')
def gallery():
    return _send_file('', 'gallery.html', cache_timeout=_PAGE_CACHE)


@app.route('/about')
def about():
    return _send_file('', 'about.html', cache_timeout=_PAGE_CACHE)


@app.route('/menu_en')
def menu_en():
    return _send_file('', 'menu_en.html', cache_timeout=_PAGE_CACHE)


@app.route('/menu_cn')
def menu_cn():
    return _send_file('', 'menu_cn.html', cache_timeout=_PAGE_CACHE)


@app.route('/js/<path:filename>')
def deliver_js(filename):
    flask.g.is_static = True
    return _send_file('/js', filename, cache_timeout=_ASSET_CACHE)


@app.route('/css/<path:filename>')
def deliver_css(filename):
    flask.g.is_static = True
    return _send_file('/css', filename, cache_timeout=_ASSET_CACHE)


@app.route('/img/<path:filename>')
def deliver_img(filename):
    flask.g.is_static = True
    return _send_file('/img', filename, cache_timeout=_ASSET_CACHE)


@app.route('/img/<filename>.png')
def png_files(filename):
    flask.g.is_static = True
    return _send_file('/img', filename + '.png', mimetype='image/png', cache_timeout=_ASSET_CACHE)


@app.route('/favicon.ico')
def favicon():
    flask.g.is_static = True
    return _send_file('/img', 'favicon.ico', mimetype='image/vnd.microsoft.icon',
        as_attachment=False, cache_timeout=_ASSET_CACHE)


def _send_file(directory, filename, **options):
    directory = app.root_path + '/static' + directory
    return flask.send_from_directory(directory, filename, **options)


if __name__ == "__main__":
    main()
