from unittest import TestCase

from flexical.data.hotels import load_hotel_reviews_with_polarity, merge_hotels_reviews_to_one_file


class LoadHotelReviewsTest(TestCase):
    def test_return_reviews_with_polarities_associated_by_index(self):
        reviews, polarities = load_hotel_reviews_with_polarity(stem_words=False)

        self.assertIsInstance(reviews, list)
        self.assertIsInstance(polarities, list)
        self.assertEqual(len(reviews), len(polarities))

        for i in xrange(len(reviews[:10])):
            self.assertIsInstance(reviews[i], list)
            self.assertIn(polarities[-1], (-1, 1))

            for word in reviews[i]:
                self.assertIsInstance(word, unicode)

    def test_return_stemmed_reviews_with_polarities_associated_by_index(self):
        reviews, polarities = load_hotel_reviews_with_polarity(stem_words=True)

        self.assertIsInstance(reviews, list)
        self.assertIsInstance(polarities, list)
        self.assertEqual(len(reviews), len(polarities))

        for i in xrange(len(reviews[:10])):
            self.assertIsInstance(reviews[i], list)
            self.assertIn(polarities[-1], (-1, 1))

            for word in reviews[i]:
                self.assertIsInstance(word, unicode)

    def test_merge_hotels_reviews(self):
        merge_hotels_reviews_to_one_file()
