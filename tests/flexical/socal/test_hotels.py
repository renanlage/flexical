from unittest import TestCase

from flexical.socal.hotels import load_hotel_reviews_with_label


class LoadHotelReviewsTest(TestCase):
    def test_return_correct_dict(self):
        review_scores = load_hotel_reviews_with_label(stem_words=True)

        self.assertIsInstance(review_scores, list)

        for review, score in review_scores:
            self.assertIsInstance(review, list)
            self.assertIn(score, (-1, 1))

            for word in review:
                self.assertIsInstance(word, unicode)
