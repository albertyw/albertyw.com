import datetime
import os
from typing import Any, List, Optional, cast

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
TIMEZONE = pytz.timezone(os.environ['DISPLAY_TIMEZONE'])


class Note(object):
    def __init__(self) -> None:
        self.note_file = ''
        self.title = ''
        self.slug = ''
        self.time: datetime.datetime = datetime.datetime.now()
        self.note = ''
        self.markdown = ''

    def __eq__(self, other: Any) -> bool:
        return type(self) == type(other) and \
                self.title == getattr(other, 'title') and \
                self.slug == getattr(other, 'slug') and \
                self.time == getattr(other, 'time') and \
                self.note == getattr(other, 'note') and \
                self.markdown == getattr(other, 'markdown')

    def __repr__(self) -> str:
        return 'Note: %s\n%s\n%s\n%s\n%s' % (
            self.title, self.slug, self.time, self.note, self.markdown
        )

    @staticmethod
    def get_note_file_data(note_file: str) -> Optional["Note"]:
        with open(note_file) as note_handle:
            lines = note_handle.readlines()
        lines = [line.strip("\n") for line in lines]
        if len(lines) < 4 or not lines[4].isdigit():
            return None
        note_parsed = Note()
        note_parsed.note_file = note_file
        note_parsed.title = lines[0]
        note_parsed.slug = lines[2]
        note_parsed.time = Note.parse_time(lines[4])
        note_parsed.markdown = '\n'.join(lines[6:])
        note_parsed.note = Note.parse_markdown(note_parsed.markdown)
        return note_parsed

    @staticmethod
    @varsnap
    def parse_time(timestamp_str: str) -> datetime.datetime:
        timestamp = int(timestamp_str)
        time = datetime.datetime.fromtimestamp(timestamp, TIMEZONE)
        return time

    @staticmethod
    @varsnap
    def parse_markdown(markdown: str) -> str:
        note = markdown2.markdown(markdown, extras=MARKDOWN_EXTRAS)
        note_str = cast(str, note)
        return note_str

    def write_note(self) -> None:
        assert Note.parse_markdown(self.markdown) == self.note
        with open(self.note_file, 'w') as handle:
            handle.write(self.title + "\n\n")
            handle.write(self.slug + "\n\n")
            handle.write(str(int(self.time.timestamp())) + "\n\n")
            handle.write(self.markdown + "\n")


@varsnap
def prune_note_files(note_files: List[str]) -> List[str]:
    def is_valid_note(note_file: str) -> bool:
        if '~' in note_file:
            return False
        if note_file[0] == '.':
            return False
        return True
    files = [note_file for note_file in note_files if is_valid_note(note_file)]
    return files


def get_note_files() -> List[str]:
    current_directory = os.path.dirname(os.path.realpath(__file__))
    notes_directory = os.path.join(current_directory, 'notes')
    files = os.listdir(notes_directory)
    files.sort(reverse=True)
    files = prune_note_files(files)
    files = [os.path.join(notes_directory, note_file) for note_file in files]
    return files


# @varsnap
@cached_function
def get_notes() -> List[Note]:
    note_files = get_note_files()
    notes = []
    for note_file in note_files:
        note_parsed = Note.get_note_file_data(note_file)
        if note_parsed:
            notes.append(note_parsed)
    return notes


@varsnap
@cached_function
def get_note_from_slug(slug: str) -> Optional[Note]:
    """ Given the slug of a note, return the note contents """
    notes = get_notes()
    for note in notes:
        if note.slug == slug:
            return cast(Note, note)
    return None
