import io

from flexical.preprocess import preprocess_text, stem_word, remove_accents, remove_repeated_letters


def load_hotel_reviews_with_label(stem_words=False):
    reviews_with_label = []
    word_transforms = [remove_repeated_letters, remove_accents]

    if stem_words:
        word_transforms.insert(0, stem_word)

    with io.open('flexical/data/hotels.txt', 'r', encoding='latin-1') as _file:
        while True:
            raw_review = _file.readline()
            rating = int(_file.readline())
            score = rating_to_label(rating)

            # Ignore neutral reviews with rating = 3 / score = 0
            if score != 0:
                processed_review = list(preprocess_text(raw_review, word_transforms))
                reviews_with_label.append((processed_review, score))

            # Jump blank line after rating
            # stop reading if end of file reached
            if not _file.readline():
                break

        return reviews_with_label


def rating_to_label(rating):
    if rating <= 2:
        return -1
    elif rating >= 4:
        return 1
    else:
        return 0
