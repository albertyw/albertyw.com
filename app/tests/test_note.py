import tempfile
import unittest

import pytz

from app import note_util


class TestNote(unittest.TestCase):
    def setUp(self):
        self.note = note_util.Note()

    def test_parse_time(self):
        time = 1504334092
        self.note.parse_time(time, pytz.timezone('America/Los_Angeles'))
        self.assertEqual(self.note.time.year, 2017)
        self.assertEqual(self.note.time.month, 9)
        self.assertEqual(self.note.time.day, 1)

    def test_parse_note(self):
        note = ['[x](y)']
        self.note.parse_note(note)
        self.assertEqual(self.note.note, '<p><a href="y">x</a></p>\n')


class UtilCase(unittest.TestCase):
    def test_get_malformed_note(self):
        note = b''
        note_file = tempfile.NamedTemporaryFile()
        note_file.write(note)
        note = note_util.get_note_file_data(note_file.name, None)
        self.assertEqual(note, None)
        note_file.close()

    def check_prune_note_files(self, file_name, assert_contains):
        note_files = note_util.prune_note_files([file_name])
        contains = file_name in note_files
        self.assertTrue(contains == assert_contains)

    def test_normal_notes(self):
        self.check_prune_note_files('asdf', True)

    def test_prune_tilde_notes(self):
        self.check_prune_note_files('asdf~', False)

    def test_prune_dotfile_notes(self):
        self.check_prune_note_files('.asdf', False)

    def test_get_note_from_unknown_slug(self):
        note = note_util.get_note_from_slug('asdf')
        self.assertEqual(note, None)

    def test_slug_lower_case(self):
        notes = note_util.get_notes()
        for note in notes:
            self.assertEqual(note.slug, note.slug.lower())
