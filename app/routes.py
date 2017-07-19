from urllib.parse import urljoin
from werkzeug.contrib.atom import AtomFeed

from flask import (
    Blueprint,
    abort,
    redirect,
    render_template,
    request,
    url_for,
)

import note_util
import util


handlers = Blueprint('handlers', __name__)


@handlers.route("/")
def index():
    return render_template("index.htm")


@handlers.route("/resume")
def resume():
    return render_template("resume.htm")


@handlers.route("/projects")
def projects():
    return render_template("projects.htm")


@handlers.route("/notes")
def notes():
    posts = note_util.get_notes()
    return render_template("notes.htm", posts=posts)


@handlers.route("/note/<slug>")
def note(slug=''):
    post = note_util.get_note_from_slug(slug)
    if not post:
        abort(404)
    return render_template("note.htm", post=post)


@handlers.route("/contact")
def contact():
    return redirect(url_for('handlers.about'))


@handlers.route("/about")
def about():
    return render_template("about.htm")


@handlers.route("/atom.xml")
def atom_feed():
    feed = AtomFeed('albertyw.com', feed_url=request.url, url=request.url_root)
    for post in list(note_util.get_notes())[:5]:
        url = urljoin(request.url_root, url_for('handlers.note', slug=post['slug']))
        feed.add(
            post['title'],
            post['note'],
            content_type='html',
            author='Albert Wang',
            url=url,
            updated=post['time'],
        )
    return feed.get_response()


@handlers.route("/robots.txt")
def robots():
    return ""
