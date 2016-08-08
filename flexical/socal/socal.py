from itertools import izip

from flexical.lexicons import load_oplexicon
from flexical.preprocess import stem_word
from flexical.socal.hotels import load_hotel_reviews_with_label


CLAUSE_BREAKERS = {
    '.', ',', ';', '?', '!',
    "e", "nem", "nao", "tambem",
    "mas", "porem", "todavia", "contudo", "entretanto", "senao",
    "portanto", "logo", "porque",
    "ou", "ora", "ja", "quer"
}


class Socal(object):
    def __init__(self, stem_words=False, use_intensifiers=True, use_irrealis=True, use_negators=True):
        self.stem_words = stem_words
        self.use_intensifiers = use_intensifiers
        self.use_irrealis = use_irrealis
        self.use_negators = use_negators

        self.intensifiers = {
            "muito": 2, "bem": 2, "bastante": 2, "demais": 2, "demas": 2, "mais": 2, "mt": 2, "d+": 2, "muto": 2,
            u"tao": 2, "quase": 0.5, "qse": 0.5, "tanto": 0.5, "pouco": 0.5
        }
        self.irrealis = {u"se", u"caso", u"poderia", u"poderiamos", u"poderiam", u"haveria", u"haveriamos", u"haveriam"}
        self.negators = {u"nao", u"nem", u'n', u"nenhum", u"ninguem", u'ngm' u"nada", u"nunca", u"jamais", u"tampouco"}

        if stem_words:
            self.intensifiers = {stem_word(word): multiplier for word, multiplier in self.intensifiers.iteritems()}
            self.irrealis = {stem_word(word) for word in self.irrealis}
            self.negators = {stem_word(word) for word in self.negators}

    def scores(self):
        lexicon = load_oplexicon(stem_words=self.stem_words)
        reviews_with_label = load_hotel_reviews_with_label(stem_words=self.stem_words)
        reviews, labels = izip(*reviews_with_label)

        # all_reviews_polarities = []
        # all_reviews_socal_masks = []
        all_reviews_socal_scores = []

        for review in reviews:
            review_polarities = self.calculate_polarities(lexicon, review)
            review_socal_masks = self.calculate_socal_masks(review)
            review_socal_score = [polarity * mask for polarity, mask in zip(review_polarities, review_socal_masks)]

            all_reviews_socal_scores.append(review_socal_score)

        return [sum(score) for score in all_reviews_socal_scores]

    def calculate_polarities(self, lexicon, review):
        return [lexicon.get(word, 0) for word in review]

    def calculate_socal_masks(self, review):
        mask = [1] * len(review)

        for index, word in enumerate(review):
            if self.use_intensifiers and word in self.intensifiers:
                apply_multiplier_till_clause_break(review, mask, index + 1, self.intensifiers[word])

            elif self.use_irrealis and word in self.irrealis:
                apply_multiplier_till_clause_break(review, mask, index + 1, 0)

            elif self.use_negators and word in self.negators:
                apply_multiplier_till_clause_break(review, mask, index + 1, -1)

        return mask


def apply_multiplier_till_clause_break(review, mask, index, multiplier):
    """ Apply multiplier for all words after itensifier until end of clause """
    for index in xrange(index, len(review)):
        if review[index] in CLAUSE_BREAKERS:
            break

        mask[index] *= multiplier
