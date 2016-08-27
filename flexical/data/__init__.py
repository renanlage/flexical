from flexical.data.hotels import hotel_reviews
from flexical.data.reli import reli_reviews


def all_datasets(stem_words=False):
    hotels_r, hotels_p = hotel_reviews(stem_words=stem_words)
    reli_r, reli_p = reli_reviews(stem_words=stem_words)

    return hotels_r.extend(reli_r), hotels_p.extend(reli_p)
