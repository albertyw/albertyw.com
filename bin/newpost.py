#!/usr/bin/env python3
"""
This script generates a new note
"""

import calendar
import datetime
import os
from pathlib import Path
import subprocess

from syspath import get_git_root


EDITOR = os.environ.get('EDITOR', 'vim')


def generate_note() -> Path:
    current_time = datetime.datetime.utcnow()

    note_filename = current_time.strftime('%Y%m%d-%H%M.md')
    note_path = get_git_root() / 'app' / 'notes' / note_filename

    timestamp = calendar.timegm(current_time.utctimetuple())
    note = "title\n\nslug\n\n%s\n\nnote\n" % timestamp

    with open(note_path, 'w') as note_handle:
        note_handle.write(note)
    return note_path


def edit_note(note_path: Path) -> None:
    subprocess.call([EDITOR, str(note_path)])


if __name__ == '__main__':
    note_path = generate_note()
    print('Note template written to %s' % note_path)
    edit_note(note_path)
