from sklearn.feature_extraction.text import CountVectorizer

from flexical.socal.hotels import load_hotel_reviews_with_label


def review_as_bag_of_words():
    reviews_with_label = load_hotel_reviews_with_label()

    reviews = [u' '.join(review) for review, _ in reviews_with_label]

    vectorizer = CountVectorizer(analyzer="word",
                                 tokenizer=None,
                                 preprocessor=None,
                                 stop_words=None,
                                 max_features=10000)

    bow = vectorizer.fit_transform(reviews)
