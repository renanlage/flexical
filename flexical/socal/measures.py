from __future__ import division


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


def precision(confusion_matrix, negative=False):
    tp = confusion_matrix['true_positive']
    tn = confusion_matrix['true_negative']
    fp = confusion_matrix['false_positive']
    fn = confusion_matrix['false_negative']

    if negative is True:
        if (tn + fn) == 0:
            return 0.001
        return tn / (tn + fn)

    if tp + fp == 0:
        return 0.001
    return tp / (tp + fp)


def recall(confusion_matrix, negative=False):
    tp = confusion_matrix['true_positive']
    tn = confusion_matrix['true_negative']
    fp = confusion_matrix['false_positive']
    fn = confusion_matrix['false_negative']

    if negative is True:
        if (tn + fp) == 0:
            return 0.001
        return tn / (tn + fp)

    if (tp + fn) == 0:
        return 0.001
    return tp / (tp + fn)


def mathews_correlation_coefficient(confusion_matrix):
    tp = confusion_matrix['true_positive']
    tn = confusion_matrix['true_negative']
    fp = confusion_matrix['false_positive']
    fn = confusion_matrix['false_negative']

    return (tp*tn - fp*fn) / ((tp+fp)*(tp+fn)*(tn+fp)*(tn+fn))**0.5


def fscore(confusion_matrix, negative=True):
    if negative is True:
        prec = precision(confusion_matrix, negative=True)
        rec = recall(confusion_matrix, negative=True)
    else:
        prec = precision(confusion_matrix)
        rec = recall(confusion_matrix)

    return 2 * prec * rec / (prec + rec)


def weighted_fscore(confusion_matrix):
    total_positive = confusion_matrix['true_positive'] + confusion_matrix['false_negative']
    total_negative = confusion_matrix['false_positive'] + confusion_matrix['true_negative']

    f1neg = fscore(confusion_matrix, negative=True)
    f1pos = fscore(confusion_matrix, negative=False)

    return (f1pos * total_positive + f1neg * total_negative) / (total_positive + total_negative)


def measures_to_string(acc, mcc, posfscore, wfscore):
    measures = ['Accuracy:         {:2.4f}'.format(acc),
                'Matthews CC:      {:2.4f}'.format(mcc),
                '+F Score:         {:2.4f}'.format(posfscore),
                'Weighted F Score: {:2.4f}'.format(wfscore)]

    return u'\n'.join(measures)


def measure_socal(scores, labels):
    conf_matrix = confusion_matrix(scores, labels)

    return (accuracy(conf_matrix), mathews_correlation_coefficient(conf_matrix),
            fscore(conf_matrix), weighted_fscore(conf_matrix))
