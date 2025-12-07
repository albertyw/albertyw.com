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
        headers = {
            'User-Agent': 'albertyw.com link checker (https://www.albertyw.com/)',
        }
        async with session.get(url, headers=headers) as response:
            content_binary = await response.read()
            debug_info = f"Failed to access link: {url}"
            try:
                content = content_binary.decode('utf-8')
                debug_info += f"\n\n{content}"
            except UnicodeDecodeError:
                pass
            if b'cRay' in content_binary:
                return
            self.assertEqual(response.status, 200, debug_info)
            self.assertTrue(content_binary, f"Link {url} returned empty response")

    async def test_links(self) -> None:
        shelf = data.get_shelf()
        urls: list[str] = []
        for section in shelf.sections:
            for item in section.items:
                if 'unsplash.com' in item.link:
                    # Unsplash blocks automated requests
                    continue
                urls.append(item.link)
        async with aiohttp.ClientSession() as session:
            await asyncio.gather(*(self.get(url, session) for url in urls))
