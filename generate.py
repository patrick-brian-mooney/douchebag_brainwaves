#!/usr/bin/env python3
"""Posts to the DouchebagBrainwaves Tumblr account, much like my other
automatically generated text accounts.
"""

import random

import patrick_logger    # From https://github.com/patrick-brian-mooney/personal-library
import social_media      # From https://github.com/patrick-brian-mooney/personal-library
from social_media_auth import douchebag_brainwaves_client

sys.path.append('/lovecraft/markov_sentence_generator/')
from sentence_generator import *                            # https://github.com/patrick-brian-mooney/markov-sentence-generator


# Parameter declarations
tags = 'automatically generated text, Markov chains, Paul Graham, Python, Patrick Mooney'
brainwave_length = random.choice(list(range(4, 10)))
the_content = ''
patrick_logger.verbosity_level = 2
chains_file = '/lovecraft/chains.dat'

patrick_logger.log_it("INFO: Everything's set up, let's go ...", 2)
the_markov_length, the_starts, the_mapping = read_chains(chains_file)


if __name__ == "__main__":
    pass
