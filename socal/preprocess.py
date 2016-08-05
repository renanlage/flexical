# -*- coding: utf-8 -*-

import nltk
import io

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
        for word_transform in word_transforms:
          word = word_transform(word)
        yield word


# File handling functions

def raw_read(filename, encoding):
   with io.open(filename, 'r', encoding=encoding) as file:
      return file.read()

def raw_write(filename, encoding, text):
  with io.open(filename, 'w', encoding=encoding) as file:
      file.write(text)


# Tokenizer functions

def tokenize_sentences(text):
  return sentence_tokenizer.tokenize(text)

def tokenize_words(sentence):
  return nltk.word_tokenize(sentence)


# Word transform functions

def stem_word(word):
  return stemmer.stem(word)


# Utils

def word_vec_to_string(word_vec):
  return u' '.join(word_vec)


if __name__ == "__main__":
  text = raw_read('data/hotels.txt', 'latin-1')
  stopwords = nltk.corpus.stopwords.words('portuguese')
  punctuation = ['.', ',', ';', ':', '?', '!', '""', "''", "``"]
  word_transforms = (stem_word,)

  preprocessed_text = list(preprocess_text(text, word_transforms))
  print preprocessed_text[:200]
  raw_write('output.txt', 'utf-8', word_vec_to_string(preprocessed_text))
