import random
import unittest

import util


def rand(base):
    return base + random.random()


@util.cached_function(True)
def cached_rand(base):
    return rand(base)


class TestCachedFunction(unittest.TestCase):
    def test_noncached_function(self):
        first = rand(2)
        second = rand(2)
        self.assertNotEqual(first, second)

    def test_cached_function(self):
        first = cached_rand(2)
        second = cached_rand(2)
        self.assertEqual(first, second)

    def test_cached_nonmatching_function(self):
        first = cached_rand(2)
        second = cached_rand(3)
        self.assertNotEqual(first, second)
