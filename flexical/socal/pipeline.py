import itertools
from operator import itemgetter

from flexical.data import all_reviews, hotel_reviews, reli_reviews
from flexical.lexicons import oplexicon, sentilex, reli_lexicon
from flexical.socal.measures import measure_socal
from flexical.socal.socal import Socal
from flexical.text_processing.file_handling import raw_write


DATASETS = {'hotel': hotel_reviews(), 'reli': reli_reviews(), 'all': all_reviews(),
            'hotel_stem': hotel_reviews(stem_words=True), 'reli_stem': reli_reviews(stem_words=True),
            'all_stem': all_reviews(stem_words=True)}

LEXICONS = {'oplexicon': oplexicon(), 'sentilex': sentilex(), 'reli_lex': reli_lexicon(),
            'oplexicon_stem': oplexicon(stem_words=True), 'sentilex_stem': sentilex(stem_words=True),
            'reli_lex_stem': reli_lexicon(stem_words=True)}


def dataset_loader(dataset_repr, stem_words):
    if stem_words:
        dataset_repr += '_stem'

    return DATASETS.get(dataset_repr)


def lexicon_loader(lexicon_repr, stem_words):
    if stem_words:
        lexicon_repr += '_stem'

    return DATASETS.get(lexicon_repr)


def run_pilene_with_all_options():
    lex_repr_values = ('oplexicon', 'sentilex', 'reli_lex')
    dataset_repr_values = ('hotel', 'reli', 'all')
    stem_words_values = apply_mask_values = (True,)
    mask_max_steps_values = range(2, 16)

    all_results = []
    results_measures = []
    index = 0

    for lex_repr, dataset_repr, stem_words, mask_max_steps, apply_mask \
            in itertools.product(lex_repr_values,
                                 dataset_repr_values,
                                 stem_words_values,
                                 mask_max_steps_values,
                                 apply_mask_values):
        # Just run for one mask_max_steps value if no need to apply mask
        # The others runs would be the same as mask_max_steps is not used if no mask is applied
        if apply_mask is False and mask_max_steps != mask_max_steps_values[0]:
            continue

        result, measure = socal_result(index, stem_words, mask_max_steps, apply_mask,
                                       lex_repr, lexicon_loader(lex_repr, stem_words),
                                       dataset_repr, dataset_loader(dataset_repr, stem_words))
        all_results.append(result)

        # Save measures for latter analysis
        results_measures.append(measure)

        print index
        index += 1

    params_header = u'{:16} {:8} {:16} {:4} {:10} {:8} {:6} {:6} {:6} {:6}'.format(
        'lexicon', 'lex_size', 'dataset', 'stem', 'mask_steps', 'use_mask', 'acc', 'mcc', 'fsc', 'wfsc'
    )

    best_and_worst_results = best_and_worst_positioned(all_results, results_measures, params_header)
    sorted_results = results_sorted_by(all_results, results_measures, 'acc')
    all_results_string = format_results('All results', params_header, sorted_results)
    raw_write('results/socal_pipeline.txt', 'utf-8', best_and_worst_results + all_results_string)


def socal_result(index, stem_words, mask_max_steps, apply_mask, lex_repr, lexicon, dataset_repr, dataset):
    socal = Socal(stem_words=stem_words, mask_max_steps=mask_max_steps, use_irrealis=apply_mask,
                  use_intensifiers=apply_mask, use_negators=apply_mask)
    scores, labels = socal.calculate_scores(lexicon, dataset)
    acc, mcc, posfscore, wfscore = measure_socal(scores, labels)

    result = u'\n'.join([u'-' * 100, u'{:16} {:^8} {:16} {:^4} {:^10} {:^8} {:2.2f}   {:2.2f}   {:2.2f}   {:2.2f}'.format(
            lex_repr, len(lexicon),  dataset_repr, stem_words, mask_max_steps,
            apply_mask, acc, mcc, posfscore, wfscore
    )])
    measure = {'index': index, 'acc': acc, 'mcc': mcc, 'posfscore': posfscore, 'wfscore': wfscore}

    return result, measure


def format_results(description_header, params_header, results):
    return '\n'.join(['\n\n', '#' * 100, description_header, '\n', params_header, u'\n'.join(results)])


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


def results_sorted_by(results, measures, type, max=None):
    results = [results[measure['index']] for measure in sorted(measures, key=itemgetter(type), reverse=True)]

    if not max:
        return results

    return results[:max], results[-max:]
