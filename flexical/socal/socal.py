from flexical.preprocess import stem_word


class Socal(object):
    def __init__(self, lexicon_loader, dataset_loader, stem_words=False, mask_max_steps=10,
                 use_intensifiers=True, use_irrealis=True, use_negators=True):
        self.stem_words = stem_words
        self.mask_max_steps = mask_max_steps
        self.use_intensifiers = use_intensifiers
        self.use_irrealis = use_irrealis
        self.use_negators = use_negators
        self.lexicon_loader = lexicon_loader
        self.dataset_loader = dataset_loader

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
            "...", ".", ",", ";", "?", "!", "(", ")", '"', "'", "`"
            "ainda", "tambem", "tb", "tbm",
            "mas", "porem", "todavia", "contudo", "entretanto", "senao",
            "portanto", "logo", "porque", "pq", "ora", "ja"
        }
        self.clause_breakers.update(self.negators)

        if self.stem_words:
            self.intensifiers = {stem_word(word): multiplier for word, multiplier in self.intensifiers.iteritems()}
            self.irrealis = {stem_word(word) for word in self.irrealis}
            self.negators = {stem_word(word) for word in self.negators}
            self.clause_breakers = {stem_word(word) for word in self.clause_breakers}

    def calculate_scores(self):
        texts, polarities = self.dataset_loader(stem_words=self.stem_words)
        lexicon = self.lexicon_loader(stem_words=self.stem_words)

        socal_scores = []

        for index, text in enumerate(texts):
            socal_polarities = self.polarities(text, lexicon)
            mask = self.mask(text)
            individual_words_score = [polarity * mask for polarity, mask in zip(socal_polarities, mask)]
            text_score = sum(score for score in individual_words_score)

            socal_scores.append(text_score)

        return socal_scores, polarities

    def polarities(self, text, lexicon):
        return [lexicon.get(word, 0) for word in text]

    def mask(self, text):
        mask = [1] * len(text)

        for index, word in enumerate(text):
            if self.use_intensifiers and word in self.intensifiers:
                start_index = self.index_of_previous_clause_break(text, index) + 1
                end_index = self.index_of_next_clause_break(text, index)
                self.apply_multiplier_to_mask(mask, self.intensifiers[word], start_index, end_index)

            elif self.use_irrealis and word in self.irrealis:
                end_index = self.index_of_next_clause_break(text, index)
                self.apply_multiplier_to_mask(mask, 0, index + 1, end_index)

            elif self.use_negators and word in self.negators:
                end_index = self.index_of_next_clause_break(text, index)
                self.apply_multiplier_to_mask(mask, -1, index + 1, end_index)

        return mask

    def apply_multiplier_to_mask(self, mask, multiplier, start_index, end_index):
        for i in xrange(start_index, end_index):
            mask[i] *= multiplier

    def index_of_next_clause_break(self, words_vec, start_index):
        max_index = min(start_index + 1 + self.mask_max_steps, len(words_vec))

        for i in xrange(start_index + 1, max_index):
            if words_vec[i] in self.clause_breakers:
                return i
        return max_index

    def index_of_previous_clause_break(self, words_vec, start_index):
        min_index = max(start_index - 1 - self.mask_max_steps, 0)

        for i in xrange(start_index - 1, min_index, -1):
            if words_vec[i] in self.clause_breakers:
                return i
        return min_index
