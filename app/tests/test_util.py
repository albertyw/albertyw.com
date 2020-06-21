import random
import unittest

from app import util


def rand(base: int) -> float:
    return base + random.random()


@util.cached_function
def cached_rand(base: int) -> float:
    return rand(base)


class TestCachedFunction(unittest.TestCase):
    def setUp(self) -> None:
        self.orig_cache = util.SHOULD_CACHE
        util.SHOULD_CACHE = True

    def tearDown(self) -> None:
        util.SHOULD_CACHE = self.orig_cache

    def test_noncached_function(self) -> None:
        self.assertNotEqual(rand(2), rand(2))

    def test_cached_function(self) -> None:
        self.assertEqual(cached_rand(2), cached_rand(2))

    def test_cached_nonmatching_function(self) -> None:
        self.assertNotEqual(cached_rand(2), cached_rand(3))
