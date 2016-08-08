from unittest.case import TestCase

from flexical.lexicons import load_oplexicon
from flexical.socal.socal import Socal


class SocalTest(TestCase):
    def test_return_something(self):
        socal = Socal(lexicon_loader=load_oplexicon)
        socal.scores()
