from __future__ import absolute_import

import unittest

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
        self.page_test('/contact', b'Contact')

    def test_robots_load(self):
        self.page_test('/robots.txt', b'')

    def test_sitemap_load(self):
        self.page_test('/sitemap.xml', b'xml')

    def page_test(self, path, string):
        response = self.app.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertIn(string, response.get_data())


if __name__ == '__main__':
    unittest.main()
