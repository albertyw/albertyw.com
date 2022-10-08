import datetime
import os
from pathlib import Path
from typing import Any, Optional, cast

from flask import url_for
import markdown2
import syspath
from varsnap import varsnap
from zoneinfo import ZoneInfo

from app.util import cached_function


# See https://github.com/trentm/python-markdown2/wiki/Extras
MARKDOWN_EXTRAS = [
    'code-friendly',
    'fenced-code-blocks',
    'smarty-pants',
    'tables',
]
TIMEZONE = ZoneInfo(os.environ['DISPLAY_TIMEZONE'])
NOTES_DIRECTORY = 'notes'
REFERENCE_DIRECTORY = 'reference'


class Note(object):
    def __init__(self, note_file: Path) -> None:
        self.note_file = note_file
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
    def get_note_file_data(note_file: Path) -> Optional["Note"]:
        with open(note_file) as note_handle:
            lines = note_handle.readlines()
        lines = [line.strip("\n") for line in lines]
        if len(lines) < 4 or not lines[4].isdigit():
            return None
        note_parsed = Note(note_file)
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

    def url(self) -> str:
        if REFERENCE_DIRECTORY in str(self.note_file.resolve()):
            return url_for('handlers.reference', slug=self.slug)
        elif NOTES_DIRECTORY in str(self.note_file.resolve()):
            return url_for('handlers.note', slug=self.slug)
        else:
            raise ValueError('Cannot get url for unknown note type')


@varsnap
def prune_note_files(note_files: list[Path]) -> list[Path]:
    def is_valid_note(note_file: Path) -> bool:
        if '~' in str(note_file):
            return False
        if str(note_file)[0] == '.':
            return False
        return True
    files = [note_file for note_file in note_files if is_valid_note(note_file)]
    return files


def get_note_files(directory: str) -> list[Path]:
    current_directory = syspath.get_current_path()
    notes_directory = current_directory / directory
    files = list(notes_directory.iterdir())
    files.sort(reverse=True)
    files = prune_note_files(files)
    files = [notes_directory / note_file for note_file in files]
    return files


@cached_function
def get_notes_directories(directories: list[str]) -> List[Note]:
    notes: list[Note] = []
    for directory in directories:
        notes += get_notes(directory)
    notes = sorted(notes, key=lambda n: n.time, reverse=True)
    return notes


# @varsnap
@cached_function
def get_notes(directory: str) -> list[Note]:
    note_files = get_note_files(directory)
    notes: list[Note] = []
    for note_file in note_files:
        note_parsed = Note.get_note_file_data(note_file)
        if note_parsed:
            notes.append(note_parsed)
    return notes


@varsnap
@cached_function
def get_note_from_slug(directory: str, slug: str) -> Optional[Note]:
    """ Given the slug of a note, return the note contents """
    notes = get_notes(directory)
    for note in notes:
        if note.slug == slug:
            return cast(Note, note)
    return None
