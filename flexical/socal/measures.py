from __future__ import division

from flexical.socal.socal import Socal
from flexical.lexicons import load_oplexicon


def confusion_matrix(scores, labels, average=0):
    matrix = {'true_positive': 0, 'true_negative': 0, 'false_positive': 0, 'false_negative': 0}

    for i in xrange(len(scores)):
        if scores[i] > average:
            predicted_label = 1
        elif scores[i] < average:
            predicted_label = -1
        else:
            predicted_label = 0

        if labels[i] == 1:
            if predicted_label == 1:
                matrix['true_positive'] += 1
            else:
                matrix['false_negative'] += 1
        else:
            if predicted_label == -1:
                matrix['true_negative'] += 1
            else:
                matrix['false_positive'] += 1

    return matrix


def accuracy(confusion_matrix):
    tp = confusion_matrix['true_positive']
    tn = confusion_matrix['true_negative']

    return (tp + tn) / sum(confusion_matrix.values())


def precision(confusion_matrix):
    tp = confusion_matrix['true_positive']
    fp = confusion_matrix['false_positive']

    if tp + fp == 0:
        return 0.001

    return tp / (tp + fp)


def recall(confusion_matrix):
    tp = confusion_matrix['true_positive']
    fn = confusion_matrix['false_negative']

    if (tp + fn) == 0:
        return 0.001

    return tp / (tp + fn)


def fscore(precision, recall):
    return 2 * precision * recall / (precision + recall)


def measure_socal():
    scores, labels = Socal(load_oplexicon, use_intensifiers=False, use_irrealis=False, use_negators=False).scores()
    conf_matrix = confusion_matrix(scores, labels)

    print '{}', accuracy(conf_matrix)

    scores, labels = Socal(load_oplexicon, use_intensifiers=False, use_irrealis=False, use_negators=True).scores()
    conf_matrix = confusion_matrix(scores, labels)

    print '-', accuracy(conf_matrix)

    scores, labels = Socal(load_oplexicon, use_intensifiers=False, use_irrealis=True, use_negators=False).scores()
    conf_matrix = confusion_matrix(scores, labels)

    print '0', accuracy(conf_matrix)

    scores, labels = Socal(load_oplexicon, use_intensifiers=True, use_irrealis=False, use_negators=False).scores()
    conf_matrix = confusion_matrix(scores, labels)

    print '+', accuracy(conf_matrix)

    scores, labels = Socal(load_oplexicon, use_intensifiers=True, use_irrealis=True, use_negators=True).scores()
    conf_matrix = confusion_matrix(scores, labels)

    print '+0-', accuracy(conf_matrix)

    scores, labels = Socal(load_oplexicon, use_intensifiers=True, use_irrealis=True, use_negators=False).scores()
    conf_matrix = confusion_matrix(scores, labels)

    print '+0', accuracy(conf_matrix)
