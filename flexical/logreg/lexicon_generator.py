# -*- coding: utf-8 -*-
import io
import operator

import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model.logistic import LogisticRegression


class LexiconGenerator(object):
    def __init__(self, dataset_loader, apply_socal_mask=True, stem_words=False, remove_stopwords=False,
                 bias=0, threshold=0.25):
        self.dataset_loader = dataset_loader
        self.stem_words = stem_words
        self.remove_stopwords = remove_stopwords
        self.apply_socal_mask = apply_socal_mask
        self.bias = bias
        self.threshold = threshold

    def text_as_bag_of_words_features(self):
        reviews, polarities = self.dataset_loader(stem_words=self.stem_words)

        stopwords = nltk.corpus.stopwords.words('portuguese') if self.remove_stopwords else None
        vectorizer = CountVectorizer(analyzer="word",
                                     token_pattern=r"(?u)\s(.+?)\s",
                                     tokenizer=None,
                                     preprocessor=None,
                                     stop_words=stopwords,
                                     max_features=None)
        bows = vectorizer.fit_transform(u' '.join(review) for review in reviews)

        return bows, vectorizer.get_feature_names(), polarities

    def build_lexicon(self, filename=None):
        bows, vocabulary, labels = self.text_as_bag_of_words_features()
        words_coefs = extract_logistic_regression_coefficients(bows, vocabulary, labels)

        lexicon = {word: coef for word, coef in words_coefs.iteritems() if coef > self.bias + self.threshold or coef < self.bias - self.threshold}

        if filename:
            export_lexicon_to_file(filename, lexicon)

        return lexicon


def associate_coefficients_to_words(coefs, vocabulary):
    assert len(vocabulary) == coefs.size
    return {vocabulary[i]: coefs.item(i) for i in xrange(len(vocabulary))}


def show_high_and_low_coef_words(words_coefs, show_count=10):
    print '{} words with the highest coefficients:'.format(show_count)

    for word, coef in sorted(words_coefs.iteritems(), key=operator.itemgetter(1), reverse=True)[:show_count]:
        print '{}\t\t{}'.format(coef, word)

    print '\n{} words with the lowest coefficients:'.format(show_count)

    for word, coef in sorted(words_coefs.iteritems(), key=operator.itemgetter(1), reverse=False)[:show_count]:
        print '{}\t\t{}'.format(coef, word)


def extract_logistic_regression_coefficients(bows, vocabulary, labels):
    classifier = LogisticRegression().fit(bows, labels)
    return associate_coefficients_to_words(classifier.coef_, vocabulary)


def export_lexicon_to_file(filename, lexicon):
    with io.open(filename, 'w', encoding='utf-8') as _file:
        for word, coef in lexicon.iteritems():
            _file.write(u'{}, {}\n'.format(word, coef))
