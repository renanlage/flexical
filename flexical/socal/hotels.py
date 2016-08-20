import io

from flexical.preprocess import preprocess_text, stem_word, remove_accents, remove_repeated_letters


def load_hotel_reviews_with_polarity(stem_words=False):
    reviews = []
    polarities = []
    word_transforms = [remove_repeated_letters, remove_accents]

    if stem_words:
        word_transforms.insert(0, stem_word)

    with io.open('flexical/data/hotels.txt', 'r', encoding='utf-8') as _file:
        while True:
            raw_review = _file.readline()
            polarity = int(_file.readline())

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
    reviews_with_polarity = set()
    reviews_filenames = ('flexical/data/hotels2.txt', 'flexical/data/hotels_orig.txt', 'flexical/data/hotelsdev.txt',
                         'flexical/data/hotelstest.txt')

    reviews_count = 0
    polarized_reviews_count = 0

    for filename in reviews_filenames:
        with io.open(filename, 'r', encoding='latin-1') as _file:
            while True:
                review = _file.readline().rstrip()
                rating = int(_file.readline().rstrip())
                polarity = rating_to_polarity(rating)

                reviews_count += 1

                # Ignore neutral reviews with rating = 3 / polarity = 0
                if polarity != 0:
                    polarized_reviews_count += 1
                    reviews_with_polarity.add((review, polarity))

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
    print 'Total number of polarized reviews: ', polarized_reviews_count

    print 'Total number of distinct polarized reviews: ', len(reviews_with_polarity)
    print 'Total number of distinct positive reviews: ', sum(1 for _, polarity in reviews_with_polarity if polarity == 1)
    print 'Total number of distinct negative reviews: ', sum(1 for _, polarity in reviews_with_polarity if polarity == -1)

    with io.open('flexical/data/hotels.txt', 'w', encoding='utf-8') as _file:
        for index, (review, polarity) in enumerate(reviews_with_polarity):
            if index < len(reviews_with_polarity) - 1:
                _file.write(u'{}\n{}\n\n'.format(review, polarity))
            else:
                _file.write(u'{}\n{}'.format(review, polarity))
