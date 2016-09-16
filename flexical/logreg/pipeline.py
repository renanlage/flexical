import itertools
from operator import itemgetter

from flexical.data import hotel_reviews, reli_reviews, all_reviews
from flexical.logreg.lexicon_generator import LexiconGenerator
from flexical.socal.measures import measure_socal
from flexical.socal.socal import Socal
from flexical.text_processing.file_handling import raw_write

# lex 1: no mask, l1
# lex 2: with mask, l1
# lex 3: with mask, l2

# in datasets: hotel, reli, all

DATASETS = {
    # 'hotel': hotel_reviews(),
    'reli': reli_reviews(),
    # 'all': all_reviews(),
    # 'hotel_stem': hotel_reviews(stem_words=True),
    # 'reli_stem': reli_reviews(stem_words=True),
    # 'all_stem': all_reviews(stem_words=True)}
}

# extraction -> bias, thresh
# polarization -> binary, raw, normalized
# fix positive bias -> true, false


PARAMS_HEADER = u'{:11} {:11} {:7} {:4} {:11} {:5} {:5} {:8} {:8} {:8} {:10} {:8} {:6} {:6} {:6} {:6}'.format(
    'in_data', 'out_data', 'len_lex', 'stem', 'mask_steps', 'bias', 'thresh', 'penalty', 'fix_bias', 'lex_type', 'apply_mask', 'rm_stopw', 'acc', 'mcc', 'fsc', 'wfsc'
)
PARAMS_VALUES = u'{:11} {:11} {:^7} {:^4} {:^11} {:3.2f}   {:3.2f} {:^8} {:^8} {:^8} {:^10} {:^8} {:2.2f}   {:2.2f}   {:2.2f}   {:2.2f}'


def dataset_loader(dataset_repr, stem_words):
    if stem_words:
        dataset_repr += '_stem'

    return DATASETS.get(dataset_repr)


def lexicon_generator_pipeline():
    print 'loading stuff...'

    logreg_dataset_repr_values = ('reli',)
    socal_dataset_repr_values = ('reli',)
    stem_words_values = (False,)
    apply_socal_mask_values = (True,)
    remove_stopwords_values = (True,)
    mask_max_steps_values = (6,)
    fix_positive_bias = (True,)
    lex_type_values = ('binary', 'raw', 'normalized')
    bias_values = list(frange(-2.0, 1.0, 0.2))
    threshold_values = list(frange(0.0, 0.80, 0.1))
    penalty_values = ('l2',)

    file_strs = []
    total_index = 0

    for logreg_dataset_repr, socal_dataset_repr in itertools.product(logreg_dataset_repr_values,
                                                                     socal_dataset_repr_values):
        results = []
        results_measures = []
        index = 0

        for stem_words, mask_max_steps, apply_mask, remove_stopwords, bias, threshold, penalty, fix_bias, lex_type in \
                itertools.product(stem_words_values,
                                  mask_max_steps_values,
                                  apply_socal_mask_values,
                                  remove_stopwords_values,
                                  bias_values,
                                  threshold_values,
                                  penalty_values,
                                  fix_positive_bias,
                                  lex_type_values):
            # Just run for one mask_max_steps value if no need to apply mask
            # The others runs would be the same as mask_max_steps is not used if no mask is applied
            if apply_mask is False:
                if mask_max_steps == mask_max_steps_values[0]:
                    mask_max_steps = '-'
                else:
                    print 'No socal_mask so skipping mask steps {}'.format(mask_max_steps)
                    continue

            if logreg_dataset_repr == socal_dataset_repr:
                result, measure = cross_validate(index, dataset_loader(logreg_dataset_repr, stem_words),
                                                 logreg_dataset_repr, stem_words, mask_max_steps, apply_mask,
                                                 remove_stopwords, bias, threshold, penalty)
                results.append(result)
                # Save measures for latter analysis
                results_measures.append(measure)

                print total_index
                index += 1
                total_index += 1

            try:
                lex_generator = LexiconGenerator(dataset_loader(logreg_dataset_repr, stem_words),
                                                 apply_socal_mask=apply_mask, mask_max_steps=mask_max_steps,
                                                 remove_stopwords=remove_stopwords, ignored_words=(),
                                                 stem_words=stem_words, bias=bias, threshold=threshold,
                                                 penalty=penalty, fix_bias=fix_bias, lex_type=lex_type)
                # lexicon = lex_generator.build_lexicon('results/lexicons/lex-{}.csv'.format(total_index))
                lexicon = lex_generator.build_lexicon()

                if not lexicon:
                    print 'No lexicon generated'
                    continue

                result, measure = socal_result(index, lexicon, dataset_loader(socal_dataset_repr, stem_words),
                                               logreg_dataset_repr, socal_dataset_repr, stem_words, mask_max_steps,
                                               apply_mask, remove_stopwords, bias, threshold, penalty)
            except Exception as e:
                print e
                result = e.message
                measure = {'index': index, 'acc': 0, 'mcc': 0, 'posfscore': 0, 'wfscore': 0}

            results.append(result)
            # Save measures for latter analysis
            results_measures.append(measure)

            print total_index
            index += 1
            total_index += 1

        best_and_worst_results = ''  # best_and_worst_positioned(all_results, results_measures, params_header)
        all_results_string = format_results('All results', PARAMS_HEADER, results_sorted_by(results, results_measures))
        file_strs.append(best_and_worst_results + all_results_string)

    raw_write('results/logreg_pipeline.txt', 'utf-8', u''.join(file_strs))


def cross_validate(index, dataset, dataset_repr, stem_words, mask_max_steps, apply_mask, remove_stopwords,
                   bias, threshold, penalty, fix_bias, lex_type, n_folds=5):
    fold_size = len(dataset[0]) / n_folds
    indexes = [fold_size * i for i in range(1, n_folds)]
    indexes.append(len(dataset[0]))
    start_index = 0

    n_tests = 0
    avg_measures = {'acc': 0, 'mcc': 0, 'posfscore': 0, 'wfscore': 0, 'len_lex': 0}

    for end_index in indexes:
        try:
            testing_data = (dataset[0][start_index:end_index], dataset[1][start_index:end_index])
            training_data = (dataset[0][:start_index] + dataset[0][end_index:], dataset[1][:start_index] + dataset[1][end_index:])

            lex_generator = LexiconGenerator(training_data, apply_socal_mask=apply_mask,
                                             mask_max_steps=mask_max_steps, remove_stopwords=remove_stopwords,
                                             ignored_words=(), stem_words=stem_words, bias=bias, threshold=threshold,
                                             fix_bias=fix_bias, lex_type=lex_type)
            lexicon = lex_generator.build_lexicon()

        except ValueError as e:
            print e
            continue

        if not lexicon:
            continue

        socal = Socal(stem_words=stem_words, mask_max_steps=mask_max_steps, apply_mask=apply_mask)
        scores, labels = socal.calculate_scores(lexicon, testing_data)

        acc, mcc, posfscore, wfscore = measure_socal(scores, labels)
        avg_measures['acc'] += acc
        avg_measures['mcc'] += mcc
        avg_measures['posfscore'] += posfscore
        avg_measures['wfscore'] += wfscore
        avg_measures['len_lex'] += len(lexicon)
        n_tests += 1
        start_index = end_index

    acc, mcc, posfscore, wfscore, len_lex = [avg_measures[measure] / n_tests for measure in ('acc', 'mcc', 'posfscore', 'wfscore', 'len_lex')]

    result = u'\n'.join(
        [u'-' * 120,
         PARAMS_VALUES.format(
             dataset_repr, 'cross', len_lex, stem_words, mask_max_steps, bias, threshold, penalty,
             apply_mask, remove_stopwords, acc, mcc, posfscore, wfscore
         )])
    measure = {'index': index, 'acc': acc, 'mcc': mcc, 'posfscore': posfscore, 'wfscore': wfscore}

    return result, measure


def socal_result(index, lexicon, dataset, logreg_dataset_repr, socal_dataset_repr, stem_words, mask_max_steps,
                 apply_mask, remove_stopwords, bias, threshold, penalty, ):
    socal = Socal(stem_words=stem_words, mask_max_steps=mask_max_steps, apply_mask=apply_mask)
    scores, labels = socal.calculate_scores(lexicon, dataset)

    acc, mcc, posfscore, wfscore = measure_socal(scores, labels)

    result = u'\n'.join(
        [u'-' * 120,
         PARAMS_VALUES.format(
             logreg_dataset_repr, socal_dataset_repr, len(lexicon), stem_words, mask_max_steps, bias, threshold,
             penalty, apply_mask, remove_stopwords, acc, mcc, posfscore, wfscore
         )])
    measure = {'index': index, 'acc': acc, 'mcc': mcc, 'posfscore': posfscore, 'wfscore': wfscore}

    return result, measure


def format_results(description_header, params_header, results):
    return '\n'.join(['\n\n', '#' * 120, description_header, '\n', params_header, u'\n'.join(results)])


def best_and_worst_positioned(results, measures, params_header, max=5):
    best_acc, worst_acc = results_sorted_by(results, measures, 'acc', max)
    best_mcc, worst_mcc = results_sorted_by(results, measures, 'mcc', max)
    best_fscore, worst_fscore = results_sorted_by(results, measures, 'posfscore', max)
    best_wfscore, worst_wfscore = results_sorted_by(results, measures, 'wfscore', max)

    output = [format_results('Best accuracy results:', params_header, best_acc),
              format_results('Best Mathews Correlation Coefficient results:', params_header, best_mcc),
              format_results('Best Fscore results:', params_header, best_fscore),
              format_results('Best Weighted Fscore results:', params_header, best_wfscore),
              format_results('Worst accuracy results:', params_header, worst_acc),
              format_results('Worst Mathews Correlation Coefficient results:', params_header, worst_mcc),
              format_results('Worst Fscore results:', params_header, worst_fscore),
              format_results('Worst Weighted Fscore results:', params_header, worst_wfscore)]
    return u'\n'.join(output)


def results_sorted_by(results, measures, max=None):
    measures.sort(key=itemgetter('acc', 'mcc'), reverse=True)
    measures.sort(key=itemgetter('acc', 'mcc'), reverse=True)
    results = [results[measure['index']] for measure in measures]

    if not max:
        return results

    return results[:max], results[-max:]


def frange(x, y, jump):
  while x < y:
    yield x
    x += jump
