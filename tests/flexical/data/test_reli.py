from unittest.case import TestCase

from flexical.data.reli import reli_reviews


class ReliTest(TestCase):
    def test_reli_load_data_correctly(self):
        reviews, polarities = reli_reviews()

        self.assertEqual(len(reviews), len(polarities))
