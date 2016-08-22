# -*- coding: utf-8 -*-

import io

from flexical.text_processing.preprocess import stem_word, remove_accents, apply_transforms


def load_oplexicon(accepted_lex_types=('adj', 'emot'), stem_words=False):
    lexicon = {}
    word_transforms = [remove_accents]

    if stem_words is True:
        word_transforms.append(stem_word)

    with io.open('flexical/lexicons/oplexicon.txt', 'r', encoding='utf-8') as _file:
        for line in _file:
            word, lex_type, score = line.split(',')[:3]

            if score != "0" and lex_type in accepted_lex_types:
                word = apply_transforms(word, word_transforms)
                lexicon[word] = int(score)

    return lexicon


def load_flexical(stem_words=False):
    lexicon = {}

    with io.open('flexical/lexicons/flexical.csv', 'r', encoding='utf-8') as _file:
        for line in _file:
            word, score = line.split(',')
            polarity = float(score.rstrip())

            if stem_words is True:
                word = stem_word(word)

            if polarity > 0:
                lexicon[word] = 1
            elif polarity < 0:
                lexicon[word] = -1

    return lexicon


def load_sentilex(stem_words=False):
    lexicon = {}

    word_transforms = [remove_accents]

    if stem_words is True:
        word_transforms.append(stem_word)

    with io.open('flexical/lexicons/sentilex.txt', 'r', encoding='latin-1') as _file:
        for line in _file:
            word, info = line.split('.')
            polarity = int(info.split(';')[2].split('=')[-1])

            if stem_words is True:
                word = stem_word(word)

            if polarity != 0:
                word = apply_transforms(word, word_transforms)
                lexicon[word] = polarity

    return lexicon
