from unittest.case import TestCase

from flexical.lexicons import oplexicon, sentilex, flexical_lexicon


class LoadOplexiconTest(TestCase):
    def test_return_lexicon_in_expected_format(self):
        lexicon = oplexicon()

        self.assertIsInstance(lexicon, dict)

        for entry in lexicon.items()[:10]:
            self.assertIsInstance(entry[0], unicode)
            self.assertIn(entry[1], (-1, 1))

    def test_return_stemmed_lexicon_in_expected_format(self):
        lexicon = oplexicon(stem_words=True)

        self.assertIsInstance(lexicon, dict)

        for entry in lexicon.items()[:10]:
            self.assertIsInstance(entry[0], unicode)
            self.assertIn(entry[1], (-1, 1))


class LoadSentilexTest(TestCase):
    def test_return_lexicon_in_expected_format(self):
        lexicon = sentilex()

        self.assertIsInstance(lexicon, dict)

        for entry in lexicon.items()[:10]:
            self.assertIsInstance(entry[0], unicode)
            self.assertIn(entry[1], (-1, 1))

    def test_return_stemmed_lexicon_in_expected_format(self):
        lexicon = sentilex(stem_words=True)

        self.assertIsInstance(lexicon, dict)

        for entry in lexicon.items()[:10]:
            self.assertIsInstance(entry[0], unicode)
            self.assertIn(entry[1], (-1, 1))


class LoadFlexicalTest(TestCase):
    def test_return_lexicon_in_expected_format(self):
        lexicon = flexical_lexicon(stem_words=False)

        self.assertIsInstance(lexicon, dict)

        for entry in lexicon.items()[:10]:
            self.assertIsInstance(entry[0], unicode)
            self.assertIn(entry[1], (-1, 1))

    def test_return_stemmed_lexicon_in_expected_format(self):
        lexicon = flexical_lexicon(stem_words=True)

        self.assertIsInstance(lexicon, dict)

        for entry in lexicon.items()[:10]:
            self.assertIsInstance(entry[0], unicode)
            self.assertIn(entry[1], (-1, 1))
