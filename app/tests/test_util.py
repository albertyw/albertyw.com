import random
import unittest

import util


@util.cached_function
def rand(base):
    return base + random.random()


class TestCachedFunction(unittest.TestCase):
    def test_noncached_function(self):
        first = rand(2, False)
        second = rand(2, False)
        self.assertNotEqual(first, second)

    def test_cached_function(self):
        first = rand(2, True)
        second = rand(2, True)
        self.assertEqual(first, second)

    def test_cached_nonmatching_function(self):
        first = rand(2, True)
        second = rand(3, True)
        self.assertNotEqual(first, second)

    def test_separate_cached_function(self):
        @util.cached_function
        def rand2(base):
            return base
        first = rand(2, True)
        second = rand2(2, True)
        self.assertNotEqual(first, second)
