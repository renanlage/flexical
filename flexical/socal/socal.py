import io

from flexical.preprocess import preprocess_text, stem_word, remove_accents, remove_repeated_letters


def load_hotel_reviews(filepath, stem_words=False):
    reviews_score = []
    word_transforms = (remove_repeated_letters, remove_accents)

    if stem_words:
        word_transforms = [stem_word].extend(word_transforms)

    with io.open(filepath, 'r', encoding='latin-1') as _file:
        while True:
            raw_review = _file.readline()
            rating = int(_file.readline())

            processed_review = list(preprocess_text(raw_review, word_transforms))
            reviews_score.append((processed_review, rating))

            # Jump blank line after rating
            # stop reading if end of file reached
            if not _file.readline():
                break

        return reviews_score
