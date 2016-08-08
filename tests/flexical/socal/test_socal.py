from unittest.case import TestCase

from flexical.socal.socal import Socal


class SocalTest(TestCase):
    def test_return_something(self):
        socal = Socal()
        print socal.scores()[:100]
