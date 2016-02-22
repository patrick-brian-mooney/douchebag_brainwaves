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

import random, pprint, sys, json, urllib, requests
from urllib.request import urlopen

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
gratitude_path              = '/DouchebagBrainwaves/essays/gratitude.txt'
notes_chains_file           = '/DouchebagBrainwaves/essays/notes.2.pkl'

normal_tags = 'automatically generated text, Markov chains, Paul Graham, Python, Patrick Mooney, '
patrick_logger.verbosity_level = 2
the_brainwave = ''

the_markov_length, the_starts, the_mapping = read_chains(main_chains_file)


def get_fake_graham_title():
    """Generate a fake title based on the corpus only of Graham's titles; reject it if it's an actual Graham title."""
    ret = "Apple's Mistake"     # Start with a title that IS in Graham's list of titles.
    with open(actual_graham_titles_path) as actual_graham_titles_file:
        actual_graham_titles = actual_graham_titles_file.read()
    title_m_length, title_starts, title_mapping = read_chains(title_chains_file)
    while ''.join([x for x in ret.lower() if x.isalnum()]) in ''.join([x for x in actual_graham_titles.lower() if x.isalnum()]):
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
      lambda: 'THE COURAGE OF %s' % get_a_noun(the_brainwave),
      lambda: 'EVERY FOUNDER SHOULD KNOW ABOUT %s' % get_a_noun(the_brainwave),
      lambda: gen_text(the_mapping, the_starts, markov_length=the_markov_length, sentences_desired=1, paragraph_break_probability=0).strip()[:-1],
      lambda: gen_text(the_mapping, topical_starts, markov_length=the_markov_length, sentences_desired=1, paragraph_break_probability=0).strip()[:-1],
      lambda: "OK, I'LL TELL YOU YOU ABOUT %s" % get_a_noun(the_brainwave),
      lambda: "STARTUPS AND %s" % get_a_noun(the_brainwave),
      lambda: "WHAT'S WRONG THESE DAYS WITH %s" % get_a_noun(the_brainwave),
      lambda: "I'VE BEEN PONDERING %s" % get_a_noun(the_brainwave),
      lambda: "WHAT NO ONE UNDERSTANDS ABOUT %s" % get_a_noun(the_brainwave),
      lambda: get_fake_graham_title()
    ]
    return random.choice(possible_titles)().upper()

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

def get_notes():
    """Get a set of notes for the end of the essay."""
    notes_m_length, notes_starts, notes_mapping = read_chains(notes_chains_file)
    ret = "<p>Notes</p>\n<ol>\n"
    for which_note in range(random.randint(1,15)):
        ret = ret + '<li>%s</li>\n' % gen_text(notes_mapping, notes_starts, notes_m_length, random.randint(1, 4), paragraph_break_probability=0)
    ret = ret + "</ol>\n"
    return ret

def get_thanks():
    """Get a set of credits for people who helped Virtual Paul Graham to write this set of thoughts"""
    wp_specials = ('Special:', 'Wikipedia:', 'Category:', 'Template:', 'File:', 'Help:', 'Portal:', 'User:',
        'MediaWiki:', 'Book:', 'Draft:', 'Education Program:', 'TimedText:', 'Module:', 'Gadget:', 'Topic:')
    # First, get a list of people who were actually thanked by actual Paul Graham
    with open(gratitude_path) as gratitude_file:
        actually_thanked_by_graham = [ the_person.strip() for the_person in gratitude_file.readlines() ]
    
    # OK, now get a list of (previously) hot topics
    wp_response = urlopen('http://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia/all-access/2015/10/10')
    wp_data = wp_response.read().decode()
    wp_dict = json.loads(wp_data)
    wp_articles = [ wp_dict['items'][0]['articles'][x]['article'] for x in range(len(wp_dict['items'][0]['articles'])) ]
    real_wp_articles = [x.replace('_', ' ') for x in wp_articles if not x.startswith(wp_specials)]
    
    grateful_to = list(set(random.sample(actually_thanked_by_graham + real_wp_articles, random.randint(3,10))))

    ret = 'Thanks to ' + ', '.join(grateful_to[:-1]) + ', and ' + grateful_to[-1]
    ret = ret + ' ' + random.choice(['for their feedback on these thoughts.', 'for inviting me to speak.',
       'for reading a previous draft.'])
    return ret

if __name__ == "__main__":
    patrick_logger.log_it("INFO: Everything's set up, let's go...")

    for which_para in range(random.randint(2,8)):
        paragraph_length = random.choice(list(range(7, 12)))
        patrick_logger.log_it('INFO: Getting %d sentences.' % paragraph_length)
        the_brainwave = the_brainwave + gen_text(the_mapping, the_starts, the_markov_length, paragraph_length, paragraph_break_probability=0) + '\n'

    the_title = get_a_title(the_brainwave)
    patrick_logger.log_it('INFO: Title is: %s' % the_title)
    
    if random.random() <= .45:
        the_brainwave = the_brainwave + '\n' + get_notes()
    
    if random.random() <= 1 / 3:
        the_brainwave = the_brainwave + '\n' + get_thanks()

    patrick_logger.log_it("INFO: here's the brainwave:\n\n%s" % the_brainwave, 2)
    
    brainwave_tags = normal_tags + get_some_tags(the_brainwave)
    patrick_logger.log_it('INFO: tags are: %s' % brainwave_tags, 2)

    the_brainwave = '\n'.join([ '<p>%s</p>' % x if not x.strip().startswith('<') else x for x in the_brainwave.split('\n') ])
    the_status = social_media.tumblr_text_post(douchebag_brainwaves_client, brainwave_tags, the_title, the_brainwave)
    patrick_logger.log_it('INFO: the_status is: ' + pprint.pformat(the_status), 2)

    patrick_logger.log_it('INFO: We\'re done', 2)
