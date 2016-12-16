import random
import unittest

import util


def rand(base):
    return base + random.random()


cached_rand = util.cached_function(rand, True)


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

    def test_separate_cached_function(self):
        cached_rand2 = util.cached_function(rand, True)
        first = cached_rand(2)
        second = cached_rand2(2)
        self.assertNotEqual(first, second)
