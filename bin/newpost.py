#!/usr/bin/env python3
"""
This script generates a new note
"""

import calendar
import datetime
import os
import subprocess


EDITOR = os.environ.get('EDITOR', 'vim')


def generate_note() -> str:
    current_time = datetime.datetime.utcnow()

    current_directory = os.path.dirname(os.path.realpath(__file__))
    notes_directory = os.path.join(
        current_directory, '..', 'app', 'notes')
    note_filename = current_time.strftime('%Y%m%d-%H%M.md')
    note_path = os.path.join(notes_directory, note_filename)
    note_path = os.path.normpath(note_path)

    timestamp = calendar.timegm(current_time.utctimetuple())
    note = "title\n\nslug\n\n%s\n\nnote\n" % timestamp

    with open(note_path, 'w') as note_handle:
        note_handle.write(note)
    return note_path


def edit_note(note_path: str) -> None:
    subprocess.call([EDITOR, note_path])


if __name__ == '__main__':
    note_path = generate_note()
    print('Note template written to %s' % note_path)
    edit_note(note_path)
