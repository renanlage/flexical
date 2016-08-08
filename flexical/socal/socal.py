from itertools import izip

from flexical.preprocess import stem_word
from flexical.socal.hotels import load_hotel_reviews_with_label


class Socal(object):
    def __init__(self, lexicon_loader, stem_words=False, use_intensifiers=True, use_irrealis=True, use_negators=True):
        self.stem_words = stem_words
        self.use_intensifiers = use_intensifiers
        self.use_irrealis = use_irrealis
        self.use_negators = use_negators
        self.lexicon = lexicon_loader(stem_words=stem_words)

        self.set_mask_related_attributes()

    def set_mask_related_attributes(self):
        self.intensifiers = {
            "muito": 2, "bem": 2, "bastante": 2, "demais": 2, "demas": 2, "mais": 2, "mt": 2, "d+": 2,
            "muto": 2, "tao": 2, "quase": 0.5, "qse": 0.5, "tanto": 0.5, "pouco": 0.5
        }
        self.irrealis = {
            "se", "caso", "poderia", "poderiamos", "poderiam", "haveria", "haveriamos", "haveriam"
        }
        self.negators = {
            "nao", "nem", "n", "nenhum", "ninguem", "ngm" "nada", "nunca", "jamais", "tampouco"
        }
        self.clause_breakers = {
            ".", ",", ";", "?", "!",
            "ainda", "nem", "nao", "n", "tambem", "tb", "tbm",
            "mas", "porem", "todavia", "contudo", "entretanto", "senao",
            "portanto", "logo", "porque", "pq"
            "o", "ora", "ja", "quer"
        }

        if self.stem_words:
            self.intensifiers = {stem_word(word): multiplier for word, multiplier in self.intensifiers.iteritems()}
            self.irrealis = {stem_word(word) for word in self.irrealis}
            self.negators = {stem_word(word) for word in self.negators}
            self.clause_breakers = {stem_word(word) for word in self.clause_breakers}

    def scores(self):
        reviews_with_label = load_hotel_reviews_with_label(stem_words=self.stem_words)
        reviews, reviews_labels = izip(*reviews_with_label)

        reviews_scores = []

        for index, review in enumerate(reviews):
            review_polarities = self.calculate_polarities(review)
            review_mask = self.calculate_mask(review)
            review_words_score = [polarity * mask for polarity, mask in zip(review_polarities, review_mask)]
            review_score = sum(score for score in review_words_score)

            reviews_scores.append(review_score)

        return reviews_scores, reviews_labels

    def calculate_polarities(self, review):
        return [self.lexicon.get(word, 0) for word in review]

    def calculate_mask(self, review):
        mask = [1] * len(review)

        for index, word in enumerate(review):
            if self.use_intensifiers and word in self.intensifiers:
                start_index = self.index_of_previous_clause_break(review, index, max_steps=8) + 1
                end_index = self.index_of_next_clause_break(review, index, max_steps=8)
                self.apply_multiplier_to_mask(mask, self.intensifiers[word], start_index, end_index)

            elif self.use_irrealis and word in self.irrealis:
                end_index = self.index_of_next_clause_break(review, index, max_steps=8)
                self.apply_multiplier_to_mask(mask, 0, index + 1, end_index)

            elif self.use_negators and word in self.negators:
                end_index = self.index_of_next_clause_break(review, index, max_steps=8)
                self.apply_multiplier_to_mask(mask, 0, index + 1, end_index)

        return mask

    def apply_multiplier_to_mask(self, mask, multiplier, start_index, end_index):
        for i in xrange(start_index, end_index):
            mask[i] *= multiplier

    def index_of_next_clause_break(self, words_vec, start_index, max_steps):
        max_index = min(start_index + 1 + max_steps, len(words_vec))

        for i in xrange(start_index + 1, max_index):
            if words_vec[i] in self.clause_breakers:
                return i
        return max_index

    def index_of_previous_clause_break(self, words_vec, start_index, max_steps):
        min_index = max(start_index - 1 - max_steps, 0)

        for i in xrange(start_index - 1, min_index, -1):
            if words_vec[i] in self.clause_breakers:
                return i
        return min_index
