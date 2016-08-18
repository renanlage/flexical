from unittest.case import TestCase

from flexical.logreg.bow import build_lexicon


class ReviewAsBagOfWordsTest(TestCase):
    def test_return_corect_bow(self):
        build_lexicon(threshold=0.3)
