from unittest.case import TestCase

from flexical.data import hotel_reviews
from flexical.lexicons import oplexicon
from flexical.socal.measures import measure_socal
from flexical.socal.socal import Socal


class MeasureSocalTest(TestCase):
    def test_measure_socal(self):
        socal = Socal(lexicon_loader=oplexicon, dataset_loader=hotel_reviews)
        socal_scores, polarities = socal.calculate_scores()

        self.assertIsInstance(measure_socal(socal_scores, polarities), float)
