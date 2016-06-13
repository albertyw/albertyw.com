import datetime
import json
import os

import dotenv
root_path = os.path.dirname(os.path.realpath(__file__)) + '/../'
dotenv.read_dotenv(os.path.join(root_path, '.env'))
from getenv import env
import pytz


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
            note = note_handle.read()
        try:
            note = json.loads(note)
        except ValueError:
            continue
        note['time'] = datetime.datetime.fromtimestamp(note['time'], timezone)
        notes.append(note)
    return notes
