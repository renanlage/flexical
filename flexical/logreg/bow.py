# -*- coding: utf-8 -*-

import nltk
from sklearn.feature_extraction.text import CountVectorizer

from flexical.socal.hotels import load_hotel_reviews_with_label

import nltk
import random
#from nltk.corpus import movie_reviews
from nltk.classify.scikitlearn import SklearnClassifier
import pickle
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from nltk.classify import ClassifierI
from nltk.tokenize import word_tokenize


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


def bow_to_nltk_features(bow):
    import ipdb; ipdb.set_trace()
    return {word_index: frequency for word_index, frequency in enumerate(bow)}


def classify():
    bows, vocabulary, labels = review_as_bag_of_words_features()
    features = [bow_to_nltk_features(bow) for bow in bows]

    # training_set = [()]
    #
    # classifier = LogisticRegression().fit(training_set, labels)
    # classifier.train(training_set)
    #
    # print u'Acurácia: {}'.format(nltk.classify.accuracy(classifier, testing_set) * 100)


