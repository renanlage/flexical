from unittest.case import TestCase

from flexical.lexicons import load_oplexicon, load_sentilex, load_flexical


class LoadOplexiconTest(TestCase):
    def test_return_lexicon_in_expected_format(self):
        lexicon = load_oplexicon()

        self.assertIsInstance(lexicon, dict)

        for entry in lexicon.items()[:10]:
            self.assertIsInstance(entry[0], unicode)
            self.assertIn(entry[1], (-1, 1))

    def test_return_stemmed_lexicon_in_expected_format(self):
        lexicon = load_oplexicon(stem_words=True)

        self.assertIsInstance(lexicon, dict)

        for entry in lexicon.items()[:10]:
            self.assertIsInstance(entry[0], unicode)
            self.assertIn(entry[1], (-1, 1))


class LoadSentilexTest(TestCase):
    def test_return_lexicon_in_expected_format(self):
        lexicon = load_sentilex()

        self.assertIsInstance(lexicon, dict)

        for entry in lexicon.items()[:10]:
            self.assertIsInstance(entry[0], unicode)
            self.assertIn(entry[1], (-1, 1))

    def test_return_stemmed_lexicon_in_expected_format(self):
        lexicon = load_sentilex(stem_words=True)

        self.assertIsInstance(lexicon, dict)

        for entry in lexicon.items()[:10]:
            self.assertIsInstance(entry[0], unicode)
            self.assertIn(entry[1], (-1, 1))


class LoadFlexicalTest(TestCase):
    def test_return_lexicon_in_expected_format(self):
        lexicon = load_flexical(stem_words=False)

        self.assertIsInstance(lexicon, dict)

        for entry in lexicon.items()[:10]:
            self.assertIsInstance(entry[0], unicode)
            self.assertIn(entry[1], (-1, 1))

    def test_return_stemmed_lexicon_in_expected_format(self):
        lexicon = load_flexical(stem_words=True)

        self.assertIsInstance(lexicon, dict)

        for entry in lexicon.items()[:10]:
            self.assertIsInstance(entry[0], unicode)
            self.assertIn(entry[1], (-1, 1))
