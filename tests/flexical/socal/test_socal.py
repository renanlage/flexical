from unittest.case import TestCase

from flexical.data.hotels import load_hotel_reviews_with_polarity
from flexical.lexicons import load_oplexicon
from flexical.socal.socal import Socal


class SocalTest(TestCase):
    def test_return_something(self):
        socal = Socal()
        socal_scores, polarities = socal.calculate_scores(lexicon_loader=load_oplexicon,
                                                          dataset_loader=load_hotel_reviews_with_polarity)

        self.assertEqual(len(socal_scores), len(polarities))
