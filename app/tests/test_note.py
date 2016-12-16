import tempfile
import unittest

import note_util


class UtilCase(unittest.TestCase):
    def test_get_malformed_note(self):
        note = b''
        note_file = tempfile.NamedTemporaryFile()
        note_file.write(note)
        note = note_util.get_note_file_data(note_file.name, None)
        self.assertEqual(note, None)
        note_file.close()

    def test_prune_tilde_notes(self):
        note_files = ['asdf', 'asdf~']
        note_files = note_util.prune_note_files(note_files)
        self.assertEqual(note_files, ['asdf'])

    def test_prune_dotfile_notes(self):
        note_files = ['asdf', '.asdf']
        note_files = note_util.prune_note_files(note_files)
        self.assertEqual(note_files, ['asdf'])

    def test_get_note_from_unknown_slug(self):
        note = note_util.get_note_from_slug('asdf')
        self.assertEqual(note, None)
