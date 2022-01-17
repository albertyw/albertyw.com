from typing import Any
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

from app import data, note_util


handlers = Blueprint('handlers', __name__)


@handlers.route("/")
@varsnap
def index() -> Any:
    return render_template("index.htm")


@handlers.route("/resume")
def resume() -> Any:
    return render_template("resume.htm")


@handlers.route("/projects")
def projects() -> Any:
    projects = data.get_projects()
    return render_template("projects.htm", projects=projects)


@handlers.route("/notes")
def notes() -> Any:
    posts = note_util.get_notes(note_util.NOTES_DIRECTORY)
    return render_template("notes.htm", posts=posts)


@handlers.route("/shelf")
def shelf() -> Any:
    shelf = data.get_shelf()
    return render_template("shelf.htm", shelf=shelf)


@handlers.route("/note/<slug>")
def note(slug: str = '') -> Any:
    if slug.lower() != slug:
        return redirect(url_for('handlers.note', slug=slug.lower()))
    post = note_util.get_note_from_slug(note_util.NOTES_DIRECTORY, slug)
    if not post:
        abort(404)
    return render_template("note.htm", post=post)


@handlers.route("/reference")
def references() -> Any:
    references = note_util.get_notes(note_util.REFERENCE_DIRECTORY)
    return render_template("references.htm", references=references)


@handlers.route("/reference/<slug>")
def reference(slug: str = '') -> Any:
    if slug.lower() != slug:
        return redirect(url_for('handlers.reference', slug=slug.lower()))
    post = note_util.get_note_from_slug(note_util.REFERENCE_DIRECTORY, slug)
    if not post:
        abort(404)
    return render_template("reference.htm", post=post)


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
    fg.updated(note_util.get_notes(note_util.NOTES_DIRECTORY)[0].time)
    for post in list(note_util.get_notes(note_util.NOTES_DIRECTORY))[:5]:
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
    for post in list(note_util.get_notes(note_util.NOTES_DIRECTORY)):
        yield url_for('handlers.note', slug=post.slug, _external=True)
    for post in list(note_util.get_notes(note_util.REFERENCE_DIRECTORY)):
        yield url_for('handlers.reference', slug=post.slug, _external=True)
