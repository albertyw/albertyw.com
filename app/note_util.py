import datetime
import os

import markdown2
import pytz
from varsnap import varsnap

from app.util import cached_function


# See https://github.com/trentm/python-markdown2/wiki/Extras
MARKDOWN_EXTRAS = [
    'code-friendly',
    'fenced-code-blocks',
    'smarty-pants',
    'tables',
]


class Note(object):
    def __init__(self):
        self.title = ''
        self.slug = ''
        self.time = ''
        self.note = ''
        self.markdown = ''

    @varsnap
    def parse_time(self, timestamp, timezone):
        timestamp = int(timestamp)
        self.time = datetime.datetime.fromtimestamp(timestamp, timezone)
        return self.time

    @varsnap
    def parse_note(self, note):
        self.note = markdown2.markdown(
            "\n".join(note),
            extras=MARKDOWN_EXTRAS,
        )
        return self.note


@varsnap
def prune_note_files(note_files):
    def is_valid_note(note_file):
        if '~' in note_file:
            return False
        if note_file[0] == '.':
            return False
        return True
    files = [note_file for note_file in note_files if is_valid_note(note_file)]
    return files


def get_note_files():
    current_directory = os.path.dirname(os.path.realpath(__file__))
    notes_directory = os.path.join(current_directory, 'notes')
    files = os.listdir(notes_directory)
    files.sort(reverse=True)
    files = prune_note_files(files)
    files = [os.path.join(notes_directory, note_file) for note_file in files]
    return files


def get_note_file_data(note_file, timezone):
    with open(note_file) as note_handle:
        note = note_handle.readlines()
    note = [line.strip("\n") for line in note]
    if len(note) < 4 or not note[4].isdigit():
        return None
    note_parsed = Note()
    note_parsed.title = note[0]
    note_parsed.slug = note[2]
    note_parsed.parse_time(note[4], timezone)
    note_parsed.parse_note(note[6:])
    note_parsed.markdown = '\n'.join(note[6:])
    return note_parsed


# @varsnap
@cached_function
def get_notes():
    note_files = get_note_files()
    timezone = pytz.timezone(os.environ['DISPLAY_TIMEZONE'])
    notes = []
    for note_file in note_files:
        note_parsed = get_note_file_data(note_file, timezone)
        if note_parsed:
            notes.append(note_parsed)
    return notes


@varsnap
@cached_function
def get_note_from_slug(slug):
    """ Given the slug of a note, reurn the note contents """
    notes = get_notes()
    for note in notes:
        if note.slug == slug:
            return note
    return None
