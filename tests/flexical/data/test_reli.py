from unittest.case import TestCase

from flexical.data.reli import load_reli_reviews_with_polarity


class ReliTest(TestCase):
    def test_reli_load_data_correctly(self):
        reviews, polarities = load_reli_reviews_with_polarity()

        self.assertEqual(len(reviews), len(polarities))
