from unittest.case import TestCase

from flexical.lexicons import load_oplexicon
from flexical.socal.hotels import load_hotel_reviews_with_polarity
from flexical.socal.socal import Socal


class SocalTest(TestCase):
    def test_return_something(self):
        socal = Socal(lexicon_loader=load_oplexicon, dataset_loader=load_hotel_reviews_with_polarity)
        socal_scores, polarities = socal.calculate_scores()

        self.assertEqual(len(socal_scores), len(polarities))
