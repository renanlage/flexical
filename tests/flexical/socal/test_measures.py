from unittest.case import TestCase

from flexical.data.hotels import load_hotel_reviews_with_polarity
from flexical.lexicons import load_oplexicon
from flexical.socal.measures import measure_socal
from flexical.socal.socal import Socal


class MeasureSocalTest(TestCase):
    def test_measure_socal(self):
        socal = Socal(lexicon_loader=load_oplexicon, dataset_loader=load_hotel_reviews_with_polarity)
        socal_scores, polarities = socal.calculate_scores()

        self.assertIsInstance(measure_socal(socal_scores, polarities), float)
