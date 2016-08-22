# -*- coding: utf-8 -*-

import re
import unicodedata

import nltk

from flexical.text_processing.spelling_correction import fix_ellipsis

stemmer = nltk.stem.RSLPStemmer()
sentence_tokenizer = nltk.data.load('tokenizers/punkt/portuguese.pickle')


def preprocess_text(text, word_transforms=(), ignored_words=()):
    processed_text = fix_ellipsis(text)

    # Tokenize raw text by sentence and then by word
    for sentence in tokenize_sentences(processed_text):
        for word in tokenize_words(sentence):
            word = word.lower()

            # Ignore given words
            if word not in ignored_words and not re.match(r'\d', word, re.UNICODE):
                # Apply word transformation for each word
                yield apply_transforms(word, word_transforms)


def apply_transforms(word, transforms=()):
    for transform in transforms:
        word = transform(word)
    return word


# Tokenizer functions

def tokenize_sentences(text):
    return sentence_tokenizer.tokenize(text)


def tokenize_words(sentence):
    return nltk.word_tokenize(sentence)


# Word transform functions

def stem_word(word):
    return stemmer.stem(word)


def remove_accents(word):
    nkfd_form = unicodedata.normalize('NFKD', word)
    return u''.join(char for char in nkfd_form if not unicodedata.combining(char))


# Utils

def word_vec_to_string(word_vec):
    return u' '.join(word_vec)
