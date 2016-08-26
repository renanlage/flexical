import io
from os import path

from flexical.text_processing.preprocess import remove_accents, stem_word, preprocess_text
from flexical.text_processing.spelling_correction import remove_repeated_letters


def reli_reviews(stem_words=False, ignored_words=()):
    reviews = []
    polarities = []
    word_transforms = [remove_repeated_letters, remove_accents]

    if stem_words:
        word_transforms.insert(2, stem_word)

    authors = ("Amado", "Meyer", "Orwell", "Reboucas", "Salinger", "Saramago", "Sheldon")

    for filename in (path.abspath('flexical/data/ReLi-{}.txt'.format(author)) for author in authors):
        with io.open(filename, 'r', encoding='utf-8') as _file:
            review_words = []
            review_polarity = 0
            in_review = False

            for line in _file:
                if '#Livro' in line:
                    in_review = False
                    continue

                if '#Corpo' in line:
                    in_review = True
                    continue

                if in_review is True:
                    stripped_line = line.strip()

                    if stripped_line:
                        word_info = stripped_line.split('\t')
                        word = word_info[0]
                        word_polarity = polarity_to_int(word_info[4])

                        review_words.append(word)
                        review_polarity += word_polarity
                    else:
                        if review_polarity != 0:
                            review = list(preprocess_text(u' '.join(review_words), word_transforms, ignored_words))
                            reviews.append(review)
                            polarities.append(1 if review_polarity > 0 else -1)

                        review_words = []
                        review_polarity = 0

    return reviews, polarities


def polarity_to_int(polarity):
    if polarity == '+':
        return 1
    elif polarity == '-':
        return -1
    else:
        return 0
