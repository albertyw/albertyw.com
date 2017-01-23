import unittest
from urllib.parse import urlparse

import serve


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
        response = self.app.get('/contact')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(urlparse(response.location).path, '/about')

    def test_about_load(self):
        self.page_test('/about', b'Contact')

    def test_robots_load(self):
        self.page_test('/robots.txt', b'')

    def test_sitemap_load(self):
        self.page_test('/sitemap.xml', b'xml')

    def test_note_load(self):
        self.page_test('/note/fibonaccoli', b'Romanesco')

    def test_nonexistent_note_load(self):
        response = self.app.get('/note/asdf')
        self.assertEqual(response.status_code, 404)

    def page_test(self, path, string):
        response = self.app.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertIn(string, response.get_data())
