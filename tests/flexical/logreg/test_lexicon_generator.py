from unittest.case import TestCase

from flexical.data import hotel_reviews, reli_reviews
from flexical.logreg.lexicon_generator import LexiconGenerator


class LexiconGeneratorTest(TestCase):
    def test_build_lexicon_for_reviews(self):
        generator = LexiconGenerator(hotel_reviews)
        generator.build_lexicon('flexical/lexicons/flexical.csv')

    def test_build_lexicon_for_reli(self):
        generator = LexiconGenerator(reli_reviews)
        generator.build_lexicon('flexical/lexicons/flexical.csv')
