#!/usr/bin/env python3
"""Posts to the DouchebagBrainwaves Tumblr account, much like my other
automatically generated text accounts.

Project homepage:
    http://patrickbrianmooney.nfshost.com/~patrick/projects/DouchebagBrainwaves/
The blog itself:
    https://douchebagbrainwaves.tumblr.com/
Github repo:
    https://github.com/patrick-brian-mooney/douchebag_brainwaves
"""

import random, pprint, sys

import nltk             # http://www.nltk.org/; sudo pip install -U nltk

import patrick_logger    # From https://github.com/patrick-brian-mooney/personal-library
import social_media      # From https://github.com/patrick-brian-mooney/personal-library
from social_media_auth import douchebag_brainwaves_client

sys.path.append('/DouchebagBrainwaves/markov_sentence_generator/')
from sentence_generator import *                            # https://github.com/patrick-brian-mooney/markov-sentence-generator


# Parameter declarations
main_chains_file            = '/DouchebagBrainwaves/essays/graham.3.pkl'
title_chains_file           = '/DouchebagBrainwaves/essays/titles.1.pkl'
actual_graham_titles_path   = '/DouchebagBrainwaves/essays/titles.txt'

normal_tags = 'automatically generated text, Markov chains, Paul Graham, Python, Patrick Mooney, '
brainwave_length = random.choice(list(range(8, 16)))
patrick_logger.verbosity_level = 2
the_content = ''

the_markov_length, the_starts, the_mapping = read_chains(main_chains_file)


def get_fake_graham_title():
    """Generate a fake title based on the corpus only of Graham's titles; reject it if it's an actual Graham title."""
    ret = "Apple's Mistake"     # Start with a title that IS in Graham's list of titles.
    with open(actual_graham_titles_path) as actual_graham_titles_file:
        actual_graham_titles = actual_graham_titles_file.read()
    title_m_length, title_starts, title_mapping = read_chains(title_chains_file)
    while not ret in actual_graham_titles:
        ret = gen_text(title_mapping, title_starts, markov_length=title_m_length, sentences_desired=1, paragraph_break_probability=0).upper().strip()[:-1]
    return ret

def get_a_noun(the_brainwave):
    """Get a random noun that appears in the text"""
    tokens = nltk.word_tokenize(the_brainwave)
    tagged = nltk.pos_tag(tokens)
    nouns = [word for word,pos in tagged if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS')]
    alphanumeric = [word for word in nouns if word.isalnum()]
    return random.choice(alphanumeric)

def get_a_title(the_brainwave):
    """Gets a title for this particular Paul Graham-style brainwave"""
    possible_topical_starts = [
      ['startups', 'VC', 'startup', 'VCs', 'entrepreneur', 'entrepreneurship', 'vision', 'drive', 'commitment'],
      ['Lisp', 'Arc', 'programming', 'C++', 'coding', 'ALGOL', 'Pascal', 'Python', 'FORTRAN'],
      ['women', 'woman', 'sexism', 'sexist', 'discrimination', 'power', 'girls', 'females', 'female', 'patriarchy']
    ]
    topical_starts = random.choice(possible_topical_starts)

    possible_titles = [
      lambda: 'YOU GUYS I JUST THOUGHT OF THIS',
      lambda: 'REASONS WHY STARTUPS FAIL',
      lambda: gen_text(the_mapping, the_starts, markov_length=the_markov_length, sentences_desired=1, paragraph_break_probability=0).upper().strip()[:-1],
      lambda: gen_text(the_mapping, topical_starts, markov_length=the_markov_length, sentences_desired=1, paragraph_break_probability=0).upper().strip()[:-1],
      lambda: "OK, I'LL TELL YOU YOU ABOUT %s" % get_a_noun(the_brainwave).upper(),
      lambda: "I'VE BEEN PONDERING %s" % get_a_noun(the_brainwave).upper(),
      lambda: get_fake_graham_title()
    ]
    return random.choice(possible_titles)()

def get_some_tags(the_brainwave):
    """Gets some random tags to add to the standard tags."""

    # First, get some nouns from the brainwave.    
    tokens = nltk.word_tokenize(the_brainwave)
    tagged = nltk.pos_tag(tokens)
    nouns = [word for word,pos in tagged if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS')]
    alphanumeric = [word for word in nouns if word.isalnum()]
    maxx = int(round(len(alphanumeric)/4))
    if maxx < 3: maxx = 3
    how_many = random.randint(3, maxx)
    tags = ', '.join(random.sample(alphanumeric, how_many))
    return tags

if __name__ == "__main__":
    patrick_logger.log_it("INFO: Everything's set up, let's go...")

    patrick_logger.log_it('INFO: Getting %d sentences.' % brainwave_length)
    the_brainwave = gen_text(the_mapping, the_starts, markov_length=the_markov_length, sentences_desired=brainwave_length, paragraph_break_probability=0)
    patrick_logger.log_it("INFO: here's the brainwave:\n\n%s" % the_brainwave, 2)

    the_title = get_a_title(the_brainwave)
    patrick_logger.log_it('INFO: Title is: %s' % the_title)

    the_status = social_media.tumblr_text_post(douchebag_brainwaves_client, normal_tags + get_some_tags(the_brainwave), the_title, the_brainwave)
    patrick_logger.log_it('INFO: the_status is: ' + pprint.pformat(the_status), 2)

    patrick_logger.log_it('INFO: We\'re done', 2)
