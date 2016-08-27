from flexical.logreg.pipeline import lexicon_generator_pipeline
from flexical.socal.pipeline import run_pilene_with_all_options


def socal():
    run_pilene_with_all_options()


def lex_gen():
    lexicon_generator_pipeline()


if __name__ == "__main__":
    socal()
