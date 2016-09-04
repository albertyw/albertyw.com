from __future__ import absolute_import

import unittest

import serve


class PageCase(unittest.TestCase):
    def setUp(self):
        serve.app.config['TESTING'] = True
        self.app = serve.app.test_client()

    def test_index_load(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Albert Wang', response.get_data())

    def test_resume_load(self):
        response = self.app.get('/resume')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Resum', response.get_data())

    def test_projects_load(self):
        response = self.app.get('/projects')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Projects', response.get_data())

    def test_notes_load(self):
        response = self.app.get('/notes')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Notes', response.get_data())

    def test_contact_load(self):
        response = self.app.get('/contact')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Contact', response.get_data())


if __name__ == '__main__':
    unittest.main()
