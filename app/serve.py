import os

from jinja2 import Environment, PackageLoader
from sanic import Sanic
from sanic.exceptions import NotFound
from sanic.response import html, text

import dotenv
from getenv import env

import note_util
import util


root_path = os.path.dirname(os.path.realpath(__file__)) + '/../'
dotenv.read_dotenv(os.path.join(root_path, '.env'))

app = Sanic(__name__)
jinja_env = Environment(
    loader=PackageLoader('__main__', 'templates'),
)
jinja_env.globals['ENV'] = env


shouldCache = env('ENV') == 'production'
note_util.get_notes = util.cached_function(note_util.get_notes, shouldCache)
note_util.get_note_from_slug = util.cached_function(
    note_util.get_note_from_slug,
    shouldCache
)


@app.route("/")
async def index(request):
    template = jinja_env.get_template("index.htm")
    return html(template.render(request=request))


@app.route("/resume")
async def resume(request):
    template = jinja_env.get_template("resume.htm")
    return html(template.render(request=request))


@app.route("/projects")
async def projects(request):
    template = jinja_env.get_template("projects.htm")
    return html(template.render(request=request))


@app.route("/notes")
async def notes(request):
    posts = note_util.get_notes()
    template = jinja_env.get_template("notes.htm")
    return html(template.render(request=request, posts=posts))


@app.route("/note/<slug>")
async def note(request, slug=''):
    post = note_util.get_note_from_slug(slug)
    if not post:
        raise NotFound()
    template = jinja_env.get_template("note.htm")
    return html(template.render(request=request, post=post))


@app.route("/contact")
async def contact(request):
    template = jinja_env.get_template("contact.htm")
    return html(template.render(request=request))


@app.route("/robots.txt")
async def robots(request):
    return text("")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=env('DEBUG'), port=5000)
