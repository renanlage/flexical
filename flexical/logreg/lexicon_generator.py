# -*- coding: utf-8 -*-
import io
import operator

import nltk
from sklearn.linear_model.logistic import LogisticRegression

from flexical.text_processing.bow import BowGenerator


class LexiconGenerator(object):
    def __init__(self, dataset_loader, apply_socal_mask=True, mask_max_steps=10, remove_stopwords=False,
                 stem_words=False, bias=0, threshold=0.27):
        self.dataset_loader = dataset_loader
        self.stem_words = stem_words
        self.mask_max_steps = mask_max_steps
        self.stopwords = nltk.corpus.stopwords.words('portuguese') if remove_stopwords else ()
        self.apply_socal_mask = apply_socal_mask
        self.bias = bias
        self.threshold = threshold

    def build_lexicon(self, filename=None):
        # Load dataset and gold labels
        docs, polarities = self.dataset_loader(stem_words=self.stem_words)

        # Represent dataset as bag of words features
        bow_generator = BowGenerator(apply_socal_mask=self.apply_socal_mask, mask_max_steps=self.mask_max_steps,
                                     stopwords=self.stopwords)
        bows = bow_generator.fit_transform(docs)
        vocabulary = bow_generator.get_feature_names()

        # Train classifier and get logistic regression coefficients
        classifier = LogisticRegression().fit(bows, polarities)
        coefs = classifier.coef_

        if filename:
            self.export_lexicon_to_file(filename, vocabulary, coefs)

    def accept_word_coefficient(self, coef):
        return coef > self.bias + self.threshold or coef < self.bias - self.threshold

    def export_lexicon_to_file(self, filename, vocabulary, coefficients):
        with io.open(filename, 'w', encoding='utf-8') as _file:
            for i in xrange(coefficients.size):
                coef = coefficients[0, i]
                if self.accept_word_coefficient(coef):
                    _file.write(u'{}, {}\n'.format(vocabulary[i], coef))


def show_high_and_low_coef_words(words_coefs, show_count=10):
    print '{} words with the highest coefficients:'.format(show_count)

    for word, coef in sorted(words_coefs.iteritems(), key=operator.itemgetter(1), reverse=True)[:show_count]:
        print '{}\t\t{}'.format(coef, word)

    print '\n{} words with the lowest coefficients:'.format(show_count)

    for word, coef in sorted(words_coefs.iteritems(), key=operator.itemgetter(1), reverse=False)[:show_count]:
        print '{}\t\t{}'.format(coef, word)
