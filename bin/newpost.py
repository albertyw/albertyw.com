#!/usr/bin/env python3
import argparse
import calendar
import datetime
import os
from pathlib import Path
import subprocess
from typing import Optional, cast

from syspath import get_git_root


DESCRIPTION = "This script generates a new note or reference"
EDITOR = os.environ.get('EDITOR', 'vim')


def get_reference_slug() -> Optional[str]:
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('reference_slug', nargs='?', type=str)
    params = parser.parse_args()
    reference_slug = cast(Optional[str], params.reference_slug)
    return reference_slug


def generate_note(reference_name: Optional[str]) -> Path:
    current_time = datetime.datetime.now(datetime.timezone.utc)

    if reference_name:
        note_filename = f'{reference_name}.md'
        note_path = get_git_root() / 'app' / 'reference' / note_filename
        slug = reference_name
    else:
        note_filename = current_time.strftime('%Y%m%d-%H%M.md')
        note_path = get_git_root() / 'app' / 'notes' / note_filename
        slug = 'slug'

    timestamp = calendar.timegm(current_time.utctimetuple())
    note = f"title\n\n{slug}\n\n{timestamp}\n\nnote\n"

    if note_path.exists():
        raise ValueError(f'note at {note_path} already exists')
    with open(note_path, 'w') as note_handle:
        note_handle.write(note)
    return note_path


def edit_note(note_path: Path) -> None:
    subprocess.call([EDITOR, str(note_path)])


if __name__ == '__main__':
    reference_name = get_reference_slug()
    note_path = generate_note(reference_name)
    print('Note template written to %s' % note_path)
    edit_note(note_path)
