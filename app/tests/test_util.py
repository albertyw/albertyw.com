import random
import unittest

from app import util


def rand(base):
    return base + random.random()


@util.cached_function
def cached_rand(base):
    return rand(base)


class TestCachedFunction(unittest.TestCase):
    def setUp(self):
        self.orig_cache = util.SHOULD_CACHE
        util.SHOULD_CACHE = True

    def tearDown(self):
        util.SHOULD_CACHE = self.orig_cache

    def test_noncached_function(self):
        self.assertNotEqual(rand(2), rand(2))

    def test_cached_function(self):
        self.assertEqual(cached_rand(2), cached_rand(2))

    def test_cached_nonmatching_function(self):
        self.assertNotEqual(cached_rand(2), cached_rand(3))
