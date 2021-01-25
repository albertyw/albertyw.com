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


class TestShelf(unittest.TestCase):
    def setUp(self) -> None:
        self.original_cache = util.SHOULD_CACHE
        util.SHOULD_CACHE = True

    def tearDown(self) -> None:
        util.SHOULD_CACHE = self.original_cache

    def test_load(self) -> None:
        shelf = data.Shelf.load()
        self.assertNotEqual(shelf.data, {})
        self.assertIn('Technology', shelf.data)
        self.assertIn('link', shelf.data['Technology'][0])

    def test_get_shelf(self) -> None:
        shelf1 = data.get_shelf()
        shelf2 = data.get_shelf()
        self.assertEqual(shelf1, shelf2)
