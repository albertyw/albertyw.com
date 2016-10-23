from __future__ import absolute_import

import tempfile
import unittest

import serve, utils


class PageCase(unittest.TestCase):
    def setUp(self):
        serve.app.config['TESTING'] = True
        self.app = serve.app.test_client()

    def test_index_load(self):
        self.page_test('/', b'Albert Wang')

    def test_resume_load(self):
        self.page_test('/resume', b'Resum')

    def test_projects_load(self):
        self.page_test('/projects', b'Projects')

    def test_notes_load(self):
        self.page_test('/notes', b'Notes')

    def test_contact_load(self):
        self.page_test('/contact', b'Contact')

    def test_robots_load(self):
        self.page_test('/robots.txt', b'')

    def test_sitemap_load(self):
        self.page_test('/sitemap.xml', b'xml')

    def page_test(self, path, string):
        response = self.app.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertIn(string, response.get_data())


class UtilCase(unittest.TestCase):
    def test_get_malformed_note(self):
        note = b''
        note_file = tempfile.NamedTemporaryFile()
        note_file.write(note)
        note = utils.get_note(note_file.name, None)
        self.assertEqual(note, None)
        note_file.close()

    def test_prune_tilde_notes(self):
        note_files = ['asdf', 'asdf~']
        note_files = utils.prune_note_files(note_files)
        self.assertEqual(note_files, ['asdf'])

    def test_prune_dotfile_notes(self):
        note_files = ['asdf', '.asdf']
        note_files = utils.prune_note_files(note_files)
        self.assertEqual(note_files, ['asdf'])


if __name__ == '__main__':
    unittest.main()
