import itertools
from operator import itemgetter

from flexical.data.hotels import hotel_reviews
from flexical.data.reli import reli_reviews
from flexical.logreg.lexicon_generator import LexiconGenerator
from flexical.socal.measures import measure_socal
from flexical.socal.socal import Socal
from flexical.text_processing.file_handling import raw_write


def lexicon_generator_pipeline():
    dataset_loaders = (hotel_reviews, reli_reviews)
    boolean_values = (True, False)
    mask_max_steps_values = range(10, 15)
    bias_values = range(-2, 2)
    threshold_values = frange(0.0, 2.0, 0.05)

    all_results = []
    results_measures = []
    index = 0

    for dataset_loader, stem_words, mask_max_steps, apply_socal_mask, remove_stopwords, bias, threshold in \
            itertools.product(dataset_loaders,
                              boolean_values,
                              mask_max_steps_values,
                              boolean_values,
                              boolean_values,
                              bias_values,
                              threshold_values):
        # Just run for one mask_max_steps value if no need to apply mask
        # The others runs would be the same as mask_max_steps is not used if no mask is applied
        if apply_socal_mask is False and mask_max_steps != 10:
            continue

        lex_generator = LexiconGenerator(dataset_loader, apply_socal_mask=apply_socal_mask,
                                         mask_max_steps=mask_max_steps, remove_stopwords=remove_stopwords,
                                         ignored_words=(), stem_words=stem_words, bias=bias, threshold=threshold)
        lexicon = lex_generator.build_lexicon()

        socal = Socal(stem_words=stem_words, mask_max_steps=mask_max_steps)
        scores, labels = socal.calculate_scores(lambda stem_words: lexicon, dataset_loader)

        acc, mcc, posfscore, wfscore = measure_socal(scores, labels)

        result = [u'-' * 100,
                  u'{:14} {:^4} {:^10} {:^4}    {:2.2f} {:^10} {:^8} {:2.2f}   {:2.2f}   {:2.2f}   {:2.2f}'.format(
                      dataset_loader.__name__, stem_words, mask_max_steps, bias, threshold, apply_socal_mask,
                      remove_stopwords, acc, mcc, posfscore, wfscore
                  )]
        all_results.append(u'\n'.join(result))

        # Save measures for latter analysis
        results_measures.append({'index': index, 'acc': acc, 'mcc': mcc, 'posfscore': posfscore, 'wfscore': wfscore})

        if index==5:
            break

        print index
        index += 1

    params_header = u'{:14} {:4} {:10} {:4} {:6} {:10} {:8} {:6} {:6} {:6} {:6}'.format(
        'dataset', 'stem', 'mask_steps', 'apply_mask', 'bias', 'thresh', 'acc', 'mcc', 'fsc', 'wfsc'
    )

    best_and_worst_results = best_and_worst_positioned(all_results, results_measures, params_header)
    all_results_string = format_results('All results', params_header, results_sorted_by(all_results, results_measures, 'acc'))
    raw_write('results/socal_pipeline.txt', 'utf-8', best_and_worst_results + all_results_string)


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


def frange(x, y, jump):
  while x < y:
    yield x
    x += jump
