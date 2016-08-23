import io
from os import path

from flexical.text_processing.preprocess import preprocess_text, stem_word, remove_accents
from flexical.text_processing.spelling_correction import remove_repeated_letters


def load_hotel_reviews_with_polarity(stem_words=False):
    reviews = []
    polarities = []
    word_transforms = [remove_repeated_letters, remove_accents]

    if stem_words:
        word_transforms.insert(1, stem_word)

    with io.open(path.abspath('flexical/data/hotels.txt'), 'r', encoding='utf-8') as _file:
        while True:
            raw_review = _file.readline()
            rating = int(_file.readline().rstrip())
            polarity = rating_to_polarity(rating)

            # Ignore neutral reviews with rating = 3 / polarity = 0
            if polarity != 0:
                processed_review = list(preprocess_text(raw_review, word_transforms))
                reviews.append(processed_review)
                polarities.append(polarity)

            # Jump blank line after rating
            # stop reading if end of file reached
            if not _file.readline():
                break

        return reviews, polarities


def rating_to_polarity(rating):
    if rating <= 2:
        return -1
    elif rating >= 4:
        return 1
    else:
        return 0


def merge_hotels_reviews_to_one_file():
    reviews_count = 0
    reviews_with_rating = set()
    reviews_filenames = ('flexical/data/hotels2.txt', 'flexical/data/hotels_orig.txt', 'flexical/data/hotelsdev.txt',
                         'flexical/data/hotelstest.txt')

    for filename in reviews_filenames:
        with io.open(path.abspath(filename), encoding='latin-1') as _file:
            while True:
                reviews_count += 1
                review = _file.readline().rstrip()
                rating = int(_file.readline().rstrip())

                reviews_with_rating.add((review, rating))

                # Jump blank line after rating
                # stop reading if end of file reached
                if not _file.readline():
                    break

    # Total number of reviews:  970
    # Total number of polarized reviews:  934
    # Total number of distinct polarized reviews:  423
    # Total number of distinct positive reviews:  128
    # Total number of distinct negative reviews:  295

    print '\n\n\n'
    print 'Total number of reviews: ', reviews_count

    print 'Total number of distinct reviews: ', len(reviews_with_rating)
    print 'Total number of distinct positive reviews: ', sum(1 for _, rating in reviews_with_rating if rating > 3)
    print 'Total number of distinct negative reviews: ', sum(1 for _, rating in reviews_with_rating if rating < 3)
    print 'Total number of distinct neutral reviews: ', sum(1 for _, rating in reviews_with_rating if rating == 3)

    with io.open(path.abspath('flexical/data/hotels.txt'), 'w', encoding='utf-8') as _file:
        for index, (review, rating) in enumerate(reviews_with_rating):
            if index < len(reviews_with_rating) - 1:
                _file.write(u'{}\n{}\n\n'.format(review, rating))
            else:
                _file.write(u'{}\n{}'.format(review, rating))
