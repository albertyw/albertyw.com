from urllib.parse import urljoin

from feedgen.feed import FeedGenerator
from flask import (
    Blueprint,
    Response,
    abort,
    redirect,
    render_template,
    request,
    url_for,
)
from varsnap import varsnap
from typing import Any

from app import note_util


handlers = Blueprint('handlers', __name__)


@handlers.route("/")
def index() -> Any:
    return render_template("index.htm")


@handlers.route("/resume")
def resume() -> Any:
    return render_template("resume.htm")


@handlers.route("/projects")
def projects() -> Any:
    return render_template("projects.htm")


@handlers.route("/notes")
def notes() -> Any:
    posts = note_util.get_notes()
    return render_template("notes.htm", posts=posts)


@handlers.route("/note/<slug>")
def note(slug: str = '') -> Any:
    if slug.lower() != slug:
        return redirect(url_for('handlers.note', slug=slug.lower()))
    post = note_util.get_note_from_slug(slug)
    if not post:
        abort(404)
    return render_template("note.htm", post=post)


@handlers.route("/contact")
def contact() -> Any:
    return redirect(url_for('handlers.about'))


@handlers.route("/about")
def about() -> Any:
    return render_template("about.htm")


@handlers.route("/atom.xml")
def atom_feed() -> Any:
    fg = FeedGenerator()
    fg.title('albertyw.com')
    fg.id(request.url)
    fg.author(name='Albert Wang', email='me@albertyw.com')
    fg.link(href=request.url, rel='self')
    fg.link(href=request.url_root, rel='alternate')
    fg.language('en')
    fg.updated(note_util.get_notes()[0].time)
    for post in list(note_util.get_notes())[:5]:
        url = url_for('handlers.note', slug=post.slug)
        url = urljoin(request.url_root, url)

        fe = fg.add_entry()
        fe.title(post.title)
        fe.id(url)
        fe.content(post.note, type='html')
        fe.author(name='Albert Wang', email='me@albertyw.com')
        fe.source(url)
        fe.updated(post.time)
        fe.link(href=url)
    return Response(fg.atom_str(pretty=True), mimetype='application/atom+xml')


@varsnap
def sitemap_urls() -> Any:
    for post in list(note_util.get_notes()):
        yield url_for('handlers.note', slug=post.slug, _external=True)
