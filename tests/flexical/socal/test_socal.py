from unittest.case import TestCase

from flexical.socal.socal import load_hotel_reviews


class LoadHotelReviews(TestCase):
    def test_return_correct_dict(self):
        reviews = load_hotel_reviews('flexical/data/hotels.txt')

        print reviews[:10]
