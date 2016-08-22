from collections import defaultdict

import array
import numpy as np
import scipy.sparse as sp
from sklearn.feature_extraction.text import CountVectorizer, _make_int_array
from sklearn.utils.fixes import frombuffer_empty

from flexical.socal.socal import Socal


class BowGenerator(CountVectorizer):
    def __init__(self, vocabulary=None, stopwords=(), apply_socal_mask=True, mask_max_steps=10):
        self.apply_socal_mask = apply_socal_mask
        self.stopwords = stopwords

        if apply_socal_mask:
            self.socal = Socal(mask_max_steps=mask_max_steps)
            dtype = np.float64
        else:
            self.socal = None
            dtype = np.int64

        super(BowGenerator, self).__init__(vocabulary=vocabulary, dtype=dtype)

    def build_analyzer(self):
        return lambda x: x

    def _count_vocab(self, raw_documents, fixed_vocab):
        """Create sparse feature matrix, and vocabulary where fixed_vocab=False
        """
        if fixed_vocab:
            vocabulary = self.vocabulary_
        else:
            # Add a new value when a new vocabulary item is seen
            vocabulary = defaultdict()
            vocabulary.default_factory = vocabulary.__len__

        j_indices = _make_int_array()
        indptr = _make_int_array()
        values = _make_float_array() if self.apply_socal_mask else None
        indptr.append(0)

        for doc in raw_documents:
            # doc: meu cajado eh muito grande
            # [1, 1, 1, 0, 2]
            if self.apply_socal_mask is True:
                doc_mask = self.socal.mask(doc)

            for index, feature in enumerate(doc):
                try:
                    if feature in self.stopwords:
                        continue

                    # j_incides for a doc: [2, 10, 9, 102, 65]
                    j_indices.append(vocabulary[feature])

                    if self.apply_socal_mask:
                        values.append(doc_mask[index])

                except KeyError:
                    # Ignore out-of-vocabulary items for fixed_vocab=True
                    continue
            indptr.append(len(j_indices))

        if not fixed_vocab:
            # disable defaultdict behaviour
            vocabulary = dict(vocabulary)
            if not vocabulary:
                raise ValueError("empty vocabulary; perhaps the documents only"
                                 " contain stop words")

        j_indices = frombuffer_empty(j_indices, dtype=np.intc)
        indptr = np.frombuffer(indptr, dtype=np.intc)
        values = values if values else np.ones(len(j_indices))

        X = sp.csr_matrix((values, j_indices, indptr),
                          shape=(len(indptr) - 1, len(vocabulary)),
                          dtype=self.dtype)
        X.sum_duplicates()
        return vocabulary, X


def _make_float_array():
    return array.array(str("f"))
