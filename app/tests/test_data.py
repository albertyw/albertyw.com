import unittest

from app import data, util
import requests


class TestProjects(unittest.TestCase):
    def setUp(self) -> None:
        self.original_cache = util.SHOULD_CACHE
        util.SHOULD_CACHE = True

    def tearDown(self) -> None:
        util.SHOULD_CACHE = self.original_cache

    def test_load_from_file(self) -> None:
        projects = data.Projects.load_from_file()
        self.assertNotEqual(projects.languages, [])
        self.assertTrue(len(projects.languages) > 0)
        self.assertTrue(len(projects.languages[0].projects) > 0)
        self.assertTrue(len(projects.languages[0].projects[0].name) > 0)
        self.assertTrue(len(projects.languages[0].projects[0].description) > 0)

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

    def test_load_from_file(self) -> None:
        shelf = data.Shelf.load_from_file()
        self.assertNotEqual(shelf.sections, [])
        self.assertNotEqual(shelf.sections[0].name, '')
        self.assertNotEqual(shelf.sections[0].items, [])
        self.assertNotEqual(shelf.sections[0].items[0].name, '')
        self.assertNotEqual(shelf.sections[0].items[0].link, '')

    def test_get_shelf(self) -> None:
        shelf1 = data.get_shelf()
        shelf2 = data.get_shelf()
        self.assertEqual(shelf1, shelf2)

    def test_links(self) -> None:
        shelf = data.get_shelf()
        for section in shelf.sections:
            for item in section.items:
                if 'amazon.com' in item.link:
                    continue
                response = requests.get(item.link)
                self.assertEqual(response.status_code, 200, f"Failed to access link: {item.link}")
                self.assertTrue(response.text, f"Link {item.link} returned empty response")
