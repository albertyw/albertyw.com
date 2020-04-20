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
        self.note_file = ''
        self.title = ''
        self.slug = ''
        self.time = ''
        self.note = ''
        self.markdown = ''

    @staticmethod
    def get_note_file_data(note_file, timezone):
        with open(note_file) as note_handle:
            lines = note_handle.readlines()
        lines = [line.strip("\n") for line in lines]
        if len(lines) < 4 or not lines[4].isdigit():
            return None
        note_parsed = Note()
        note_parsed.note_file = note_file
        note_parsed.title = lines[0]
        note_parsed.slug = lines[2]
        note_parsed.time = Note.parse_time(lines[4], timezone)
        note_parsed.markdown = '\n'.join(lines[6:])
        note_parsed.note = Note.parse_markdown(note_parsed.markdown)
        return note_parsed

    @staticmethod
    @varsnap
    def parse_time(timestamp, timezone):
        timestamp = int(timestamp)
        time = datetime.datetime.fromtimestamp(timestamp, timezone)
        return time

    @staticmethod
    @varsnap
    def parse_markdown(markdown):
        note = markdown2.markdown(markdown, extras=MARKDOWN_EXTRAS)
        return note

    def write_note(self):
        assert Note.parse_markdown(self.markdown) == self.note
        with open(self.note_file, 'w') as handle:
            handle.write(self.title + "\n\n")
            handle.write(self.slug + "\n\n")
            handle.write(str(int(self.time.timestamp())) + "\n\n")
            handle.write(self.markdown + "\n")


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


# @varsnap
@cached_function
def get_notes():
    note_files = get_note_files()
    timezone = pytz.timezone(os.environ['DISPLAY_TIMEZONE'])
    notes = []
    for note_file in note_files:
        note_parsed = Note.get_note_file_data(note_file, timezone)
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
