import asyncio
import unittest

import aiohttp
from app import data, util


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


class TestShelf(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.original_cache = util.SHOULD_CACHE
        util.SHOULD_CACHE = True

    def tearDown(self) -> None:
        util.SHOULD_CACHE = self.original_cache

    async def test_load_from_file(self) -> None:
        shelf = data.Shelf.load_from_file()
        self.assertNotEqual(shelf.sections, [])
        self.assertNotEqual(shelf.sections[0].name, '')
        self.assertNotEqual(shelf.sections[0].items, [])
        self.assertNotEqual(shelf.sections[0].items[0].name, '')
        self.assertNotEqual(shelf.sections[0].items[0].link, '')

    async def test_get_shelf(self) -> None:
        shelf1 = data.get_shelf()
        shelf2 = data.get_shelf()
        self.assertEqual(shelf1, shelf2)

    async def get(self, url: str, session: aiohttp.ClientSession) -> None:
        async with session.get(url) as response:
            content = await response.read()
            self.assertEqual(response.status, 200, f"Failed to access link: {url}")
            self.assertTrue(content, f"Link {url} returned empty response")

    async def test_links(self) -> None:
        shelf = data.get_shelf()
        urls: list[str] = []
        for section in shelf.sections:
            for item in section.items:
                if 'amazon.com' in item.link:
                    # Amazon blocks automated requests
                    continue
                if 'brucefwebster.com' in item.link:
                    # SSL certificate expired
                    continue
                if 'infiniteundo.com' in item.link:
                    # infiteundo.com blocks automated requests
                    continue
                if 'ribbonfarm.com' in item.link:
                    # ribbonfarm.com blocks automated requests
                    continue
                if 'randsinrepose.com' in item.link:
                    # randsinrepose.com blocks automated requests
                    continue
                if 'unsplash.com' in item.link:
                    # Unsplash blocks automated requests
                    continue
                urls.append(item.link)
        async with aiohttp.ClientSession() as session:
            await asyncio.gather(*(self.get(url, session) for url in urls))
