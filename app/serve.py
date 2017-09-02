import os

from flask import (
    Flask,
    got_request_exception,
    render_template,
)
from flask_assets import Environment, Bundle
from flask_sitemap import Sitemap

import dotenv

from routes import handlers
import note_util
import util


root_path = os.path.dirname(os.path.realpath(__file__)) + '/../'
dotenv.read_dotenv(os.path.join(root_path, '.env'))

app = Flask(__name__)
app.debug = os.environ['DEBUG'] == 'true'
app.config['SERVER_NAME'] = os.environ['SERVER_NAME']

app.config['SITEMAP_INCLUDE_RULES_WITHOUT_PARAMS'] = True
app.config['SITEMAP_URL_SCHEME'] = 'https'
assets = Environment(app)
ext = Sitemap(app=app)


js = Bundle(
    'js/jquery.js',
    'js/tether.js',
    'js/bootstrap.js',
    'js/pdfobject.js',
    'js/global.js',
    filters='rjsmin', output='gen/bundle.min.js'
)
assets.register('js_all', js)
css = Bundle(
    'css/normalize.css',
    'css/tether.css',
    'css/bootstrap.css',
    'css/syntax.css',
    'css/global.css',
    filters='cssmin', output='gen/bundle.min.css'
)
assets.register('css_all', css)


if os.environ['ENV'] == 'production':
    import rollbar
    import rollbar.contrib.flask

    @app.before_first_request
    def init_rollbar():
        """init rollbar module"""
        rollbar.init(
            os.environ['ROLLBAR_SERVER_TOKEN'],
            # environment name
            os.environ['ENV'],
            # server root directory, makes tracebacks prettier
            root=os.path.dirname(os.path.realpath(__file__)),
            # flask already sets up logging
            allow_logging_basic_config=False)

        # send exceptions from `app` to rollbar, using flask's signal system.
        got_request_exception.connect(
            rollbar.contrib.flask.report_exception, app)


@app.context_processor
def inject_envs():
    envs = {}
    envs['ROLLBAR_CLIENT_TOKEN'] = os.environ['ROLLBAR_CLIENT_TOKEN']
    envs['SEGMENT_TOKEN'] = os.environ['SEGMENT_TOKEN']
    return {'ENV': envs}


shouldCache = os.environ['ENV'] == 'production'
note_util.get_notes = util.cached_function(note_util.get_notes, shouldCache)
note_util.get_note_from_slug = util.cached_function(
    note_util.get_note_from_slug,
    shouldCache
)


app.register_blueprint(handlers)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.htm"), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0")
