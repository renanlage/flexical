import os
from unittest.case import TestCase

from flexical.lexicons import load_oplexicon


class LoadOplexiconTest(TestCase):
    def test_return_lexicon_in_expected_format(self):
        lexicon = load_oplexicon(os.path.abspath('flexical/lexicons/oplexicon.txt'))

        self.assertIsInstance(lexicon, dict)

        for entry in lexicon.iteritems():
            self.assertIsInstance(entry[0], unicode)
            self.assertIn(entry[1], (-1, 1))
