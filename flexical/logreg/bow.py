# -*- coding: utf-8 -*-
import io
import operator

import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model.logistic import LogisticRegression

from flexical.socal.hotels import load_hotel_reviews_with_label


def review_as_bag_of_words_features():
    reviews_with_label = load_hotel_reviews_with_label()

    stopwords = nltk.corpus.stopwords.words('portuguese')
    vectorizer = CountVectorizer(analyzer="word",
                                 tokenizer=None,
                                 preprocessor=None,
                                 stop_words=None,
                                 max_features=None)
    reviews, labels = zip(*reviews_with_label)
    bows = vectorizer.fit_transform(u' '.join(review) for review in reviews)

    return bows, vectorizer.get_feature_names(), labels


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
    words_coefs = associate_coefficients_to_words(classifier.coef_, vocabulary)
    show_high_and_low_coef_words(words_coefs)

    return words_coefs


def export_lexicon_to_file(filename, lexicon):
    with io.open(filename, 'w', encoding='utf-8') as _file:
        for word, coef in lexicon.iteritems():
            _file.write(u'{}, {}\n'.format(word, coef))


def build_lexicon(features_extracting_func=review_as_bag_of_words_features, bias=0, threshold=0.1):
    bows, vocabulary, labels = features_extracting_func()
    words_coefs = extract_logistic_regression_coefficients(bows, vocabulary, labels)

    lexicon = {word: coef for word, coef in words_coefs.iteritems() if coef > bias + threshold or coef < bias - threshold}
    export_lexicon_to_file('flexical/lexicons/mylex.csv', lexicon)

    return lexicon
