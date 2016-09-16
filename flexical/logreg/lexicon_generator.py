# -*- coding: utf-8 -*-
import io
import operator

import nltk
import numpy
from sklearn.linear_model.logistic import LogisticRegression

from flexical.text_processing.bow import BowGenerator

OUTLIER_LIMIT = 3.5


class LexiconGenerator(object):
    def __init__(self, dataset, apply_socal_mask=True, mask_max_steps=10, remove_stopwords=False,
                 ignored_words=(), stem_words=False, bias=0, threshold=0.27, penalty='l1', fix_bias=True, lex_type='raw'):
        self.dataset = dataset
        self.stem_words = stem_words
        self.mask_max_steps = mask_max_steps
        self.stopwords = nltk.corpus.stopwords.words('portuguese') if remove_stopwords else ()
        self.ignored_words = ignored_words
        self.apply_socal_mask = apply_socal_mask
        self.bias = bias
        self.threshold = threshold
        self.penalty = penalty
        self.fix_bias = fix_bias
        self.lex_type = lex_type

    def build_lexicon(self, filename=None):
        # Load dataset and gold labels
        docs, polarities = self.dataset

        # Represent dataset as bag of words features
        bow_generator = BowGenerator(apply_socal_mask=self.apply_socal_mask, mask_max_steps=self.mask_max_steps,
                                     stopwords=self.stopwords)
        bows = bow_generator.fit_transform(docs)
        vocabulary = bow_generator.get_feature_names()

        # Train classifier and get logistic regression coefficients
        classifier = LogisticRegression(penalty=self.penalty, class_weight='balanced').fit(bows, polarities)
        coefs = classifier.coef_

        if self.lex_type == 'raw':
            lexicon = self.raw_lexicon_as_dict(vocabulary, coefs)
        elif self.lex_type == 'binary':
            lexicon = self.binary_lexicon_as_dict(vocabulary, coefs)
        elif self.lex_type == 'normalized':
            lexicon = self.normalized_lexicon_as_dict(vocabulary, coefs)
        else:
            raise

        if filename:
            self.export_lexicon_to_file(filename, lexicon)
        return lexicon

    def get_coef(self, coef):
        if self.fix_bias and coef < 0:
            return coef * 1.5
        return coef

    def coefficient_to_raw_polarity(self, coef):
        if self.coefficient_is_valid(coef):
            return self.get_coef(coef)
        return 0

    def coefficient_to_binary_polarity(self, coef):
        if coef > self.bias + self.threshold:
            return 1
        elif coef < self.bias - self.threshold:
            return -1
        else:
            return 0

    def binary_lexicon_as_dict(self, vocabulary, coefficients):
        lexicon = {}
        for i in xrange(coefficients.size):
            coef = coefficients[0, i]
            polarity = self.coefficient_to_binary_polarity(coef)
            if polarity:
                lexicon[vocabulary[i]] = polarity
        return lexicon

    def raw_lexicon_as_dict(self, vocabulary, coefficients):
        lexicon = {}
        for i in xrange(coefficients.size):
            coef = coefficients[0, i]
            polarity = self.coefficient_to_raw_polarity(coef)
            if polarity:
                lexicon[vocabulary[i]] = polarity
        return lexicon

    def coefficient_is_valid(self, coef):
        return coef > self.bias + self.threshold or coef < self.bias - self.threshold

    def normalized_lexicon_as_dict(self, vocabulary, coefficients):
        lexicon = []
        old_min = 99999999
        old_max = -99999999
        for i in xrange(coefficients.size):
            coef = coefficients[0, i]
            if self.coefficient_is_valid(coef):
                lexicon.append([vocabulary[i], coef])
                if coef < old_min:
                    old_min = coef
                if coef > old_max:
                    old_max = coef

        new_min = -5
        new_max = 5
        old_range = old_max - old_min
        new_range = new_max - new_min

        def normalize_coef(coef):
            if coef > OUTLIER_LIMIT:
                return new_max
            if coef < -OUTLIER_LIMIT:
                return new_min
            return (((self.get_coef(coef) - old_min) * new_range) / old_range) + new_min

        return {word: normalize_coef(coef) for word, coef in lexicon}

    def export_lexicon_to_file(self, filename, lexicon):
        with io.open(filename, 'w', encoding='utf-8') as _file:
            for word, score in lexicon.iteritems():
                _file.write(u'{}, {}\n'.format(word, score))


def show_high_and_low_coef_words(words_coefs, show_count=10):
    print '{} words with the highest coefficients:'.format(show_count)

    for word, coef in sorted(words_coefs.iteritems(), key=operator.itemgetter(1), reverse=True)[:show_count]:
        print '{}\t\t{}'.format(coef, word)

    print '\n{} words with the lowest coefficients:'.format(show_count)

    for word, coef in sorted(words_coefs.iteritems(), key=operator.itemgetter(1), reverse=False)[:show_count]:
        print '{}\t\t{}'.format(coef, word)
