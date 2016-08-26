import itertools
from operator import itemgetter

from flexical.data.hotels import hotel_reviews
from flexical.data.reli import reli_reviews
from flexical.lexicons import oplexicon, flexical_lexicon, sentilex, reli_lexicon
from flexical.socal.measures import measure_socal, measures_to_string
from flexical.socal.socal import Socal
from flexical.text_processing.file_handling import raw_write


def run_pilene_with_all_options():
    lexicon_loaders = (oplexicon, flexical_lexicon, sentilex, reli_lexicon)
    dataset_loaders = (hotel_reviews, reli_reviews)
    stem_words_values = use_irrealis_values = use_intensifiers_values = use_negators_values = (True, False)
    mask_max_steps_values = range(1, 16)

    all_results = []
    results_measures = []
    index = 0

    for lex_loader, dataset_loader, stem_words, mask_max_steps, use_irrealis, use_intensifiers, use_negators \
            in itertools.product(lexicon_loaders, dataset_loaders, stem_words_values, mask_max_steps_values,
                                 use_irrealis_values, use_intensifiers_values, use_negators_values):
        socal = Socal(stem_words=stem_words, mask_max_steps=mask_max_steps, use_irrealis=use_irrealis,
                      use_intensifiers=use_intensifiers, use_negators=use_negators)
        scores, labels = socal.calculate_scores(lex_loader, dataset_loader)
        acc, mcc, posfscore, wfscore = measure_socal(scores, labels)

        result = [u'-' * 100,
                  u'{:12} {:14} {:^4} {:^10} {:^6} {:^5} {:^3} {:2.2f}   {:2.2f}   {:2.2f}   {:2.2f}'.format(
                      lex_loader.__name__, dataset_loader.__name__, stem_words, mask_max_steps, use_irrealis,
                      use_intensifiers, use_negators, acc, mcc, posfscore, wfscore
                  )]
        all_results.append(u'\n'.join(result))

        # Save measures for latter analysis
        results_measures.append({'index': index, 'acc': acc, 'mcc': mcc, 'posfscore': posfscore, 'wfscore': wfscore})

        print index
        index += 1

    params_header = u'{:12} {:14} {:4} {:10} {:6} {:5} {:3} {:6} {:6} {:6} {:6}'.format(
        'lexicon', 'dataset', 'stem', 'mask_steps', 'irreal', 'inten', 'neg', 'acc', 'mcc', 'fsc', 'wfsc'
    )

    best_and_worst_results = best_and_worst_positioned(all_results, results_measures, params_header)
    all_results_string = format_results('All results', params_header, all_results)
    raw_write('results/socal_pipeline.txt', 'utf-8', best_and_worst_results + all_results_string)


def format_results(description_header, params_header, results):
    return '\n'.join(['\n\n', '#' * 100, description_header, '\n', params_header, u'\n'.join(results)])


def best_and_worst_positioned(results, measures, params_header, max=5):
    best_acc, worst_acc = best_and_worst_sorted_by(results, measures, 'acc', max)
    best_mcc, worst_mcc = best_and_worst_sorted_by(results, measures, 'mcc', max)
    best_fscore, worst_fscore = best_and_worst_sorted_by(results, measures, 'posfscore', max)
    best_wfscore, worst_wfscore = best_and_worst_sorted_by(results, measures, 'wfscore', max)

    output = [format_results('Best accuracy results:', params_header, best_acc),
              format_results('Best Mathews Correlation Coefficient results:', params_header, best_mcc),
              format_results('Best Fscore results:', params_header, best_fscore),
              format_results('Best Weighted Fscore results:', params_header, best_wfscore),
              format_results('Worst accuracy results:', params_header, worst_acc),
              format_results('Worst Mathews Correlation Coefficient results:', params_header, worst_mcc),
              format_results('Worst Fscore results:', params_header, worst_fscore),
              format_results('Worst Weighted Fscore results:', params_header, worst_wfscore)]
    return u'\n'.join(output)


def best_and_worst_sorted_by(results, measures, type, max):
    results = [results[measure['index']] for measure in sorted(measures, key=itemgetter(type), reverse=True)]
    return results[:max], results[-max:]
