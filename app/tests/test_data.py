import unittest

from app import data


class TestProjects(unittest.TestCase):
    def test_load(self) -> None:
        projects = data.Projects.load()
        self.assertNotEqual(projects.data, {})
        self.assertIn('Python', projects.data)
        self.assertIn('Git Browse', projects.data['Python'])
        self.assertIn('description', projects.data['Python']['Git Browse'])
