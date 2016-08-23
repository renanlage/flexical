from unittest.case import TestCase

from flexical.data.hotels import load_hotel_reviews_with_polarity
from flexical.data.reli import load_reli_reviews_with_polarity
from flexical.logreg.lexicon_generator import LexiconGenerator


class LexiconGeneratorTest(TestCase):
    def test_build_lexicon_for_reviews(self):
        generator = LexiconGenerator(load_hotel_reviews_with_polarity)
        generator.build_lexicon('flexical/lexicons/flexical.csv')

    def test_build_lexicon_for_reli(self):
        generator = LexiconGenerator(load_reli_reviews_with_polarity)
        generator.build_lexicon('flexical/lexicons/flexical.csv')
