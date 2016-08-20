# -*- coding: utf-8 -*-

import io
import re

import nltk
import unicodedata

stemmer = nltk.stem.RSLPStemmer()
sentence_tokenizer = nltk.data.load('tokenizers/punkt/portuguese.pickle')


def preprocess_text(text, word_transforms=(), ignored_words=()):
    processed_text = fix_punctuation(text)

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


# File handling functions

def raw_read(filename, encoding):
    with io.open(filename, 'r', encoding=encoding) as _file:
        return _file.read()


def raw_write(filename, encoding, text):
    with io.open(filename, 'w', encoding=encoding) as _file:
        _file.write(text)


# Spelling correction functions

def fix_punctuation(text):
    fixed_text = re.sub(r'([.,;?!])([^\W\d_])', r'\1 \2', text, flags=re.UNICODE)
    fixed_text = re.sub(r'([^\.])(\.\.) ', r'\1... ', fixed_text, flags=re.UNICODE)
    return re.sub(r'([^\.])(\.\.\.\.+) ', r'\1... ', fixed_text, flags=re.UNICODE)


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


def remove_repeated_letters(word):
    # Do not remove repeated letters only if letters are r, s, m, n or c
    regex = r'([^\W\drsmnc])\1+'
    return re.sub(regex, r'\1', word, re.UNICODE)


# Utils

def word_vec_to_string(word_vec):
    return u' '.join(word_vec)
