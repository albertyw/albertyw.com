import unittest

from app import data, util


class TestProjects(unittest.TestCase):
    def setUp(self) -> None:
        self.original_cache = util.SHOULD_CACHE
        util.SHOULD_CACHE = True

    def tearDown(self) -> None:
        util.SHOULD_CACHE = self.original_cache

    def test_load(self) -> None:
        projects = data.Projects.load()
        self.assertNotEqual(projects.data, {})
        self.assertIn('Python', projects.data)
        self.assertIn('Git Browse', projects.data['Python'])
        self.assertIn('description', projects.data['Python']['Git Browse'])

    def test_get_projects(self) -> None:
        projects1 = data.get_projects()
        projects2 = data.get_projects()
        self.assertEqual(projects1, projects2)
