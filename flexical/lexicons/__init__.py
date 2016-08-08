# -*- coding: utf-8 -*-

import io

from flexical.preprocess import stem_word, remove_accents, apply_transforms


def load_oplexicon(accepted_lex_types=('adj', 'emot'), stem_words=False):
    lexicon = {}
    word_transforms = [remove_accents]

    if stem_words is True:
        word_transforms.append(stem_word)

    with io.open('flexical/lexicons/oplexicon.txt', 'r', encoding='utf-8') as _file:
        for line in _file:
            word, lex_type, score, _ = line.split(',')

            if score != "0" and lex_type in accepted_lex_types:
                word = apply_transforms(word, word_transforms)
                lexicon[word] = int(score)

    return lexicon
