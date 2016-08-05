# -*- coding: utf-8 -*-

import io
import re

import nltk
import unicodedata

stemmer = nltk.stem.RSLPStemmer()
sentence_tokenizer = nltk.data.load('tokenizers/punkt/portuguese.pickle')


def preprocess_text(text, word_transforms=(), ignored_words=()):
    # Tokenize raw text by sentence and then by word
    for sentence in tokenize_sentences(text):
        for word in tokenize_words(sentence):
            word = word.lower()

            # Ignore given words
            if word not in ignored_words:
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
    # Do not remove repeated letters only if letters are r, s, m or n
    regex = r'([a-z&&[^rsmn]])\1+'
    return re.sub(regex, r'\1', word)


# Utils

def word_vec_to_string(word_vec):
    return u' '.join(word_vec)


def main():
    text = raw_read('data/hotels.txt', 'latin-1')
    stopwords = nltk.corpus.stopwords.words('portuguese')
    punctuation = ['.', ',', ';', ':', '?', '!', '""', "''", "``"]
    word_transforms = (stem_word,)

    preprocessed_text = list(preprocess_text(text, word_transforms))
    print preprocessed_text[:200]
    raw_write('output.txt', 'utf-8', word_vec_to_string(preprocessed_text))


if __name__ == "__main__":
    main()
