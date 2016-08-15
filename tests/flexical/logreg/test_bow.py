from unittest.case import TestCase

from flexical.logreg.bow import review_as_bag_of_words


class ReviewAsBagOfWordsTest(TestCase):
    def test_return_corect_bow(self):
        review_as_bag_of_words()
