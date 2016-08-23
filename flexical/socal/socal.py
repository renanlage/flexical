from flexical.text_processing.preprocess import stem_word


class Socal(object):
    def __init__(self, stem_words=False, mask_max_steps=10, ignored_words=(),
                 use_intensifiers=True, use_irrealis=True, use_negators=True):
        self.stem_words = stem_words
        self.mask_max_steps = mask_max_steps
        self.ignored_words = ignored_words
        self.use_intensifiers = use_intensifiers
        self.use_irrealis = use_irrealis
        self.use_negators = use_negators

        self.intensifiers = {
            "muito": 2, "bem": 2, "bastante": 2, "demais": 2, "demas": 2, "mais": 2, "mt": 2, "d+": 2,
            "muto": 2, "tao": 2, "quase": 0.5, "qse": 0.5, "tanto": 0.5, "pouco": 0.5
        }

        self.irrealis = {
            "se", "caso", "poderia", "poderiamos", "poderiam", "haveria", "haveriamos", "haveriam", "teria", "teriam",
            "teriamos"
        }
        self.negators = {
            "nao", "nem", "n", "nenhum", "ninguem", "ngm" "nada", "nunca", "jamais", "tampouco"
        }
        self.punctuation = {"...", ".", ",", ";", "?", "!", "(", ")"}
        self.clause_breakers = {
            "ainda", "tambem", "tb", "tbm",
            "mas", "porem", "todavia", "contudo", "entretanto", "senao",
            "portanto", "logo", "porque", "pq", "ora", "ja"
        }
        self.clause_breakers.update(self.punctuation, self.negators)
        self.words_with_no_polarity = set(self.intensifiers.keys()) | self.irrealis | self.clause_breakers

        if stem_words is True:
            self.intensifiers = {stem_word(word): multiplier for word, multiplier in self.intensifiers.iteritems()}
            self.irrealis = {stem_word(word) for word in self.irrealis}
            self.negators = {stem_word(word) for word in self.negators}
            self.punctuation = {stem_word(word) for word in self.punctuation}
            self.clause_breakers = {stem_word(word) for word in self.clause_breakers}
            self.words_with_no_polarity = {stem_word(word) for word in self.words_with_no_polarity}

    def calculate_scores(self, lexicon_loader, dataset_loader):
        texts, polarities = dataset_loader(stem_words=self.stem_words, ignored_words=self.ignored_words)
        lexicon = lexicon_loader(stem_words=self.stem_words)

        socal_scores = []

        for text in texts:
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
                end_index = self.index_of_next_clause_break(text, index, is_irrealis=True)
                self.apply_multiplier_to_mask(mask, 0, index + 1, end_index)

            elif self.use_negators and word in self.negators:
                end_index = self.index_of_next_clause_break(text, index)
                self.apply_multiplier_to_mask(mask, -1, index + 1, end_index)

        # Nullify words with no polarity in mask
        mask = [0 if text[i] in self.words_with_no_polarity else word_mask for i, word_mask in enumerate(mask)]
        return mask

    def index_of_next_clause_break(self, words_vec, start_index, is_irrealis=False):
        clause_breakers = self.punctuation if is_irrealis else self.clause_breakers
        max_index = min(start_index + 1 + self.mask_max_steps, len(words_vec))

        for i in xrange(start_index + 1, max_index):
            if words_vec[i] in clause_breakers:
                return i
        return max_index

    def index_of_previous_clause_break(self, words_vec, start_index, is_irrealis=False):
        clause_breakers = self.punctuation if is_irrealis else self.clause_breakers
        min_index = max(start_index - 1 - self.mask_max_steps, 0)

        for i in xrange(start_index - 1, min_index, -1):
            if words_vec[i] in clause_breakers:
                return i
        return min_index

    def apply_multiplier_to_mask(self, mask, multiplier, start_index, end_index):
        for i in xrange(start_index, end_index):
            mask[i] *= multiplier
