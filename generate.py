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

import random

import patrick_logger    # From https://github.com/patrick-brian-mooney/personal-library
import social_media      # From https://github.com/patrick-brian-mooney/personal-library
from social_media_auth import douchebag_brainwaves_client

sys.path.append('/DouchebagBrainwaves/markov_sentence_generator/')
from sentence_generator import *                            # https://github.com/patrick-brian-mooney/markov-sentence-generator


# Parameter declarations
normal_tags = 'automatically generated text, Markov chains, Paul Graham, Python, Patrick Mooney, '
brainwave_length = random.choice(list(range(4, 10)))
the_content = ''
patrick_logger.verbosity_level = 2
chains_file = '/DouchebagBrainwaves/essays/graham.3.pkl'

def get_a_title():
    """Gets a title for this particular Paul Graham-style brainwave"""
    return 'YOU GUYS I JUST THOUGHT OF THIS'

def get_some_tags():
    """Gets some random tags to add to the standard tags."""
    return ""       # For now.

if __name__ == "__main__":
    patrick_logger.log_it("INFO: Everything's set up, let's go ...")
    
    the_markov_length, the_starts, the_mapping = read_chains(chains_file)
    patrick_logger.log_it('INFO: chains read, moving on ...')
    
    the_title = get_a_title()
    patrick_logger.log_it('INFO: Title is: %s' % the_title)
    
    patrick_logger.log_it('INFO: Getting %d sentences.' % brainwave_length)
    the_brainwave = gen_text(the_mapping, the_starts, markov_length=the_markov_length, sentences_desired=brainwave_length, paragraph_break_probability=0)
    patrick_logger.log_it("INFO: here's the brainwave:\n\n%s" %  the_brainwave, 2)
    
    the_status = social_media.tumblr_text_post(douchebag_brainwaves_client, normal_tags + get_some_tags(), the_title, the_brainwave)
