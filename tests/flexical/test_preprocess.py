from unittest.case import TestCase

from flexical.preprocess import remove_repeated_letters


class RemoveRepeatedLettersTest(TestCase):
    def test_remove_repeated_letters(self):
        self.assertEqual(u'legal', remove_repeated_letters(u'legaaaaal'))
        self.assertEqual(u'k', remove_repeated_letters(u'kkkkk'))
        self.assertEqual(u'112233', remove_repeated_letters(u'112233'))
        self.assertEqual(u'passagem', remove_repeated_letters(u'passagem'))
        self.assertEqual(u'emmassar', remove_repeated_letters(u'emmassar'))
