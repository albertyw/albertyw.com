import datetime
import os

import dotenv
from getenv import env
import markdown2
import pytz

root_path = os.path.dirname(os.path.realpath(__file__)) + '/../'
dotenv.read_dotenv(os.path.join(root_path, '.env'))

# See https://github.com/trentm/python-markdown2/wiki/Extras
MARKDOWN_EXTRAS = [
    'code-friendly',
    'fenced-code-blocks',
    'smarty-pants',
    'tables',
]

def prune_note_files(note_files):
    files = [note_file for note_file in note_files if '~' not in note_file]
    return files


def get_note_files():
    current_directory = os.path.dirname(os.path.realpath(__file__))
    notes_directory = os.path.join(current_directory, 'notes')
    files = os.listdir(notes_directory)
    files.sort(reverse=True)
    files = prune_note_files(files)
    files = [os.path.join(notes_directory, note_file) for note_file in files]
    return files


def get_notes():
    note_files = get_note_files()
    timezone = pytz.timezone(env('DISPLAY_TIMEZONE'))
    notes = []
    for note_file in note_files:
        with open(note_file) as note_handle:
            note = note_handle.readlines()
        note = [line.strip() for line in note]
        if len(note) < 3 or not note[1].isdigit():
            continue
        timestamp = int(note[1])
        note_parsed = {}
        note_parsed['title'] = note[0]
        note_parsed['time'] = datetime.datetime.fromtimestamp(
            timestamp, timezone)
        note_parsed['note'] = markdown2.markdown("\n".join(note[2:]), extras=MARKDOWN_EXTRAS)
        notes.append(note_parsed)
    return notes
