import os
from urllib.parse import urljoin

from flask import (
    Flask,
    abort,
    got_request_exception,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_assets import Environment, Bundle
from flask_sitemap import Sitemap

import dotenv
from getenv import env
from werkzeug.contrib.atom import AtomFeed

import note_util
import util


root_path = os.path.dirname(os.path.realpath(__file__)) + '/../'
dotenv.read_dotenv(os.path.join(root_path, '.env'))

app = Flask(__name__)
app.debug = env('DEBUG') == 'true'
app.config['SERVER_NAME'] = env('SERVER_NAME')

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


if env('ENV') == 'production':
    import rollbar
    import rollbar.contrib.flask

    @app.before_first_request
    def init_rollbar():
        """init rollbar module"""
        rollbar.init(
            env('ROLLBAR_SERVER_TOKEN'),
            # environment name
            env('ENV'),
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
    envs['ROLLBAR_CLIENT_TOKEN'] = env('ROLLBAR_CLIENT_TOKEN')
    envs['SEGMENT_TOKEN'] = env('SEGMENT_TOKEN')
    return {'ENV': envs}


shouldCache = env('ENV') == 'production'
note_util.get_notes = util.cached_function(note_util.get_notes, shouldCache)
note_util.get_note_from_slug = util.cached_function(
    note_util.get_note_from_slug,
    shouldCache
)


@app.route("/")
def index():
    return render_template("index.htm")


@app.route("/resume")
def resume():
    return render_template("resume.htm")


@app.route("/projects")
def projects():
    return render_template("projects.htm")


@app.route("/notes")
def notes():
    posts = note_util.get_notes()
    return render_template("notes.htm", posts=posts)


@app.route("/note/<slug>")
def note(slug=''):
    post = note_util.get_note_from_slug(slug)
    if not post:
        abort(404)
    return render_template("note.htm", post=post)


@app.route("/contact")
def contact():
    return redirect(url_for('about'))


@app.route("/about")
def about():
    return render_template("about.htm")


@app.route("/atom.xml")
def atom_feed():
    feed = AtomFeed('albertyw.com', feed_url=request.url, url=request.url_root)
    for post in list(note_util.get_notes())[:5]:
        url = urljoin(request.url_root, url_for('note', slug=post['slug']))
        feed.add(
            post['title'],
            post['note'],
            content_type='html',
            author='Albert Wang',
            url=url,
            updated=post['time'],
        )
    return feed.get_response()


@app.route("/robots.txt")
def robots():
    return ""


if __name__ == "__main__":
    app.run(host="0.0.0.0")
