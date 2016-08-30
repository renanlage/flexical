from unittest.case import TestCase

from flexical.data import hotel_reviews
from flexical.lexicons import oplexicon
from flexical.socal.socal import Socal


class SocalTest(TestCase):
    def test_return_something(self):
        socal = Socal()
        socal_scores, polarities = socal.calculate_scores(lexicon_loader=oplexicon,
                                                          dataset_loader=hotel_reviews)

        self.assertEqual(len(socal_scores), len(polarities))
