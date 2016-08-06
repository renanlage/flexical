from collections import Counter
from unittest.case import TestCase

from flexical.socal.socal import load_hotel_reviews


class LoadHotelReviews(TestCase):
    def test_return_correct_dict(self):
        reviews = load_hotel_reviews(stem_words=True)

        print Counter(score for _, score in reviews)
