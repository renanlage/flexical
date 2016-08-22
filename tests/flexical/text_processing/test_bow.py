from unittest.case import TestCase

from flexical.text_processing.bow import BowGenerator


class BowTest(TestCase):
    def test_return_expected_bow_if_mask_is_not_applied(self):
        docs = [u'grande coisa essa coisa nao muito grande se o mundo acabar'.split(), [u'doideira', u'isso']]

        bow_generator = BowGenerator(apply_socal_mask=False)
        bows = bow_generator.fit_transform(docs)
        vocabulary = bow_generator.get_feature_names()

        self.assertEqual([u'acabar', u'coisa', u'doideira', u'essa', u'grande', u'isso', u'muito', u'mundo',
                          u'nao', u'o', u'se'], vocabulary)
        self.assertEqual(bows.toarray().tolist(),
                         [[1, 2, 0, 1, 2, 0, 1, 1, 1, 1, 1],
                          [0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0]])

    def test_return_expected_bow_if_mask_is_applied(self):
        docs = [u'grande coisa essa coisa nao muito grande se o mundo acabar'.split(), [u'doideira', u'isso']]

        bow_generator = BowGenerator()
        bows = bow_generator.fit_transform(docs)
        vocabulary = bow_generator.get_feature_names()

        self.assertEqual([u'coisa', u'doideira', u'essa', u'grande', u'isso'], vocabulary)
        self.assertEqual(bows.toarray().tolist(),
                         [[2,  0,  1, -1,  0],
                          [0,  1,  0,  0,  1]])

    def test_ignore_stopwords_in_bows_and_vocabulary_if_provided(self):
        docs = [u'grande coisa essa coisa nao muito grande se o mundo acabar'.split(), [u'doideira', u'isso']]

        bow_generator = BowGenerator(stopwords={u'coisa'})
        bows = bow_generator.fit_transform(docs)
        vocabulary = bow_generator.get_feature_names()

        self.assertEqual([u'doideira', u'essa', u'grande', u'isso'], vocabulary)
        self.assertEqual(bows.toarray().tolist(), [[0, 1, -1, 0], [1, 0, 0, 1]])
