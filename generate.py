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
normal_tags                     = 'automatically generated text, Markov chains, Paul Graham, Python, Patrick Mooney, '
patrick_logger.verbosity_level  = 3
the_brainwave                   = ''
force_gratitude                 = False
force_notes                     = False

#File locations
main_chains_file                = '/DouchebagBrainwaves/essays/graham.3.pkl'
title_chains_file               = '/DouchebagBrainwaves/essays/titles.1.pkl'
actual_graham_titles_path       = '/DouchebagBrainwaves/essays/titles.txt'
gratitude_path                  = '/DouchebagBrainwaves/essays/gratitude.txt'
notes_chains_file               = '/DouchebagBrainwaves/essays/notes.2.pkl'

# OK, read the primary chains into memory
the_markov_length, the_starts, the_mapping = read_chains(main_chains_file)

# Here's a list of 30 topics that MALLET found in Paul Graham's essays, with pruning of some common words that slipped through.
graham_topics = [
   ['founders', 'thing', 'number', 'change', 'VCs', 'person', 'running', 'yahoo', 'source', 'stop', 'advantage', 'force', 'friend', 'worse', 'current', 'practice', 'news', 'wait', 'treat', 'Perl'],
   ['software', 'means', 'back', 'design', 'VCs', 'end', 'realize', 'round', 'simply', 'funding', 'life', 'remember', 'quality', 'focus', 'process', 'biggest', 'succeed', 'fail', 'American'],
   ['language', 'real', 'spam', 'matter', 'computer', 'stock', 'office', 'easier', 'form', 'guys', 'figure', 'ambitious', 'students', 'price', 'difference', 'building', 'days', 'open', 'books'],
   ['inside', 'die', 'granted', 'derived', 'probabilities', 'carefully', 'convinced', 'increases', 'Cambridge', 'meet', 'artist', 'macro', 'naive', 'west', 'corpus', 'paragraph', 'pinch', 'estimate'],
   ['people', 'startup', 'make', 'things', 'investors', 'time', 'lot', 'hard', 'writing', 'reason', 'problems', 'technology', 'give', 'programmers', 'day', 'rich', 'feel'],
   ['start', 'business', 'years', 'kind', 'making', 'languages', 'valley', 'power', 'future', 'year', 'combinator', 'fundraising', 'imagine', 'general', 'hacker', 'approach', 'happened', 'century'],
   ['company', 'companies', 'problem', 'world', 'bad', 'fact', 'small', 'starting', 'early', 'deal', 'wealth', 'word', 'applications', 'buy', 'worth', 'stuff'],
   ['plan', 'pretty', 'Viaweb', 'huge', 'risk', 'default', 'meetings', 'principle', 'grew', 'thing', 'room', 'surprisingly', 'conventional', 'related', 'succeeding', 'complex', 'papers', 'slow'],
   ['ideas', 'write', 'tend', 'interesting', 'found', 'half', 'young', 'user', 'research', 'decide', 'head', 'hire', 'increasingly', 'gradually', 'bought', 'Java', 'city', 'promising'],
   ['sales', 'earlier', 'beat', 'street', 'draw', 'account', 'network', 'replace', 'technological', 'responsibility', 'regard', 'enjoy', 'human', 'iPhone', 'killed', 'continue', 'selection', 'eliminate', 'cap', 'widely'],
   ['work', 'big', 'important', 'makes', 'market', 'code', 'common', 'invest', 'web', 'times', 'sense', 'run', 'investor', 'angel', 'spend', 'true', 'wrong'],
   ['made', 'programming', 'type', 'live', 'choose', 'control', 'effect', 'public', 'groups', 'lots', 'dollars', 'hope', 'development', 'summer', 'performance', 'felt', 'began', 'growing', 'sitting', 'prefer'],
   ['startups', 'good', 'money', 'users', 'working', 'great', 'school', 'long', 'point', 'Google', 'talk', 'successful', 'job'],
   ['short', 'launch', 'feels', 'fear', 'student', 'agree', 'identical', 'disagree', 'systems', 'procrastination', 'prestigious', 'bug', 'larger', 'survive', 'mode', 'browser', 'server-based', 'influence', 'twenties'],
   ['act', 'store', 'fine', 'typical', 'national', 'format', 'security', 'future', 'unions', 'coast', 'pattern', 'texts', 'sell', 'minds', 'exception', 'twenty', 'intrinsically', 'benevolent', 'salary', 'lunch'],
   ['Steve', 'property', 'brand', 'drive', 'bank', 'amounts', 'David', 'tells', 'yields', 'blogging', 'editors', 'statement', 'decreasing', 'developers', 'planned', 'unexpected', 'zero-sum', 'spot', 'concentrated', 'ran'],
   ['hour', 'losing', 'empirically', 'worry', 'fraction', 'generating', 'automatically', 'community', 'sending', 'applied', 'internal', 'developed', 'moved', 'definition', 'recruiting', 'Javascript', 'Amazon', 'feet', 'interview'],
   ['idea', 'hackers', 'thought', 'smart', 'pay', 'question', 'case', 'powerful', 'till', 'raise', 'fast', 'couple', 'high', 'talking', 'care', 'win', 'words', 'avoid'],
   ['demand', 'stores', 'page', 'suddenly', 'fairly', 'pushing', 'desperate', 'strongly', 'doctor', 'generates', 'extract', 'reality', 'start', 'Kerry', 'mails', 'accept', 'startups', 'standing', 'equation', 'norm'],
   ['reporters', 'literature', 'software', 'long', 'definite', 'ancient', 'familiar', 'measuring', 'throwaway', 'earliest', 'imitating', 'pleasure', 'distinct', 'vote', 'fundamental', 'leaders', 'breaking', 'brain', 'pays', 'origins'],
   ['considered', 'front', 'designing', 'finding', 'brain', 'previous', 'meaning', 'background', 'cheaply', 'awkward', 'external', 'graduate', 'miss', 'eating', 'election', 'story', 'noticed', 'sentences', 'made', 'seats'],
   ['computers', 'phone', 'evil', 'regular', 'manage', 'speak', 'corporate', 'intended', 'worried', 'surely', 'built', 'parallel', 'author', 'shot', 'wisdom', 'areas', 'mobile', 'Sam', 'mathematicians'],
   ['investment', 'experience', 'situations', 'ahead', 'page', 'industrial', 'equal', 'fashions', 'sophisticated', 'trust', 'practice', 'unlike', 'assumption', 'Einstein', 'Python', 'disputes', 'nervous', 'believing'],
   ['structure', 'hit', 'changing', 'perfect', 'function', 'organization', 'insiders', 'task', 'advise', 'shares', 'lazy', 'cofounder', 'object-oriented', 'quiet', 'collection', 'defining', 'prototype', 'union', 'depending', 'combine'],
   ['university', 'outcome', 'versions', 'strange', 'implement', 'screen', 'hierarchy', 'counterintuitive', 'Aristotle', 'stripe', 'intellectually', 'quit', 'developer', 'limits', 'modern', 'rapid', 'stages', 'statistics', 'executive', 'lead'],
   ['venture', 'meet', 'novels', 'ugly', 'admissions', 'leaving', 'involved', 'innocent', 'revolution', 'clients', 'text', 'suggest', 'fragmentation', 'balance', 'attacking', 'attractive', 'overlap', 'Artix', 'Cambridge', 'energetic'],
   ['support', 'depends', 'death', 'option', 'positives', 'benefit', 'lead', 'desire', 'prices', 'theoretical', 'rational', 'compare', 'develop', 'conceal', 'discard', 'hub', 'lying', 'every', 'paperwork', 'find'],
   ['learning', 'determined', 'basic', 'edge', 'local', 'aim', 'direct', 'possibly', 'hundreds', 'exercise', 'products', 'inevitable', 'bias', 'alternative', 'constant', 'existence', 'environment', 'detail', 'degrees', 'manager'],
   ['find', 'started', 'large', 'ago', 'site', 'data', 'experience', 'life', 'field', 'surprising', 'reasons', 'works', 'product', 'potential', 'math', 'technical', 'reading', 'save', 'turns', 'weeks'],
   ['fund', 'essay', 'writers', 'living', 'prevent', 'rapidly', 'philosophy', 'level', 'syntax', 'factor', 'check', 'mind', 'topic', 'career', 'batch', 'secret', 'conference', 'behavior', 'influenced', 'technologies']
]

def get_a_noun(the_brainwave):
    """Get a random noun that appears in the text"""
    tokens = nltk.word_tokenize(the_brainwave)
    tagged = nltk.pos_tag(tokens)
    nouns = [word for word,pos in tagged if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS')]
    alphanumeric = [word for word in nouns if word.isalnum()]
    return random.choice(alphanumeric)

def get_fake_graham_title():
    """Generate a fake title based on the corpus only of Graham's titles; reject it if it's an actual Graham title."""
    ret = "Apple's Mistake"     # Start with a title that IS in Graham's list of titles.
    with open(actual_graham_titles_path) as actual_graham_titles_file:
        actual_graham_titles = actual_graham_titles_file.read()
    title_m_length, title_starts, title_mapping = read_chains(title_chains_file)
    while ''.join([x for x in ret.lower() if x.isalnum()]) in ''.join([x for x in actual_graham_titles.lower() if x.isalnum()]):
        ret = gen_text(title_mapping, title_starts, markov_length=title_m_length, sentences_desired=1, paragraph_break_probability=0).upper().strip()[:-1]
    return ret

def get_a_title(the_brainwave):
    """Gets a title for this particular Paul Graham-style brainwave."""
    topical_starts = random.choice(graham_topics)
    
    """Previous titles, no longer in use:
      lambda: 'YOU GUYS I JUST THOUGHT OF THIS',
      lambda: 'REASONS WHY STARTUPS FAIL',
      lambda: "WHAT'S WRONG THESE DAYS WITH %s" % get_a_noun(the_brainwave),
      lambda: "WHAT NO ONE UNDERSTANDS ABOUT %s" % get_a_noun(the_brainwave),
    """
    possible_titles = [
      lambda: 'THE COURAGE OF %s' % get_a_noun(the_brainwave),
      lambda: 'EVERY FOUNDER SHOULD KNOW ABOUT %s' % get_a_noun(the_brainwave),
      lambda: gen_text(the_mapping, the_starts, markov_length=the_markov_length, sentences_desired=1, paragraph_break_probability=0).strip()[:-1],
      lambda: gen_text(the_mapping, topical_starts, markov_length=the_markov_length, sentences_desired=1, paragraph_break_probability=0).strip()[:-1],
      lambda: gen_text(the_mapping, topical_starts, markov_length=the_markov_length, sentences_desired=1, paragraph_break_probability=0).strip()[:-1],
      lambda: gen_text(the_mapping, topical_starts, markov_length=the_markov_length, sentences_desired=1, paragraph_break_probability=0).strip()[:-1],
      lambda: "OK, I'LL TELL YOU YOU ABOUT %s" % get_a_noun(the_brainwave),
      lambda: "STARTUPS AND %s" % get_a_noun(the_brainwave),
      lambda: "WORK ETHIC AND %s" % get_a_noun(the_brainwave),
      lambda: "I'VE BEEN PONDERING %s" % get_a_noun(the_brainwave),
      lambda: get_fake_graham_title(),
      lambda: get_fake_graham_title(),
      lambda: get_fake_graham_title(),
      lambda: get_fake_graham_title(),
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
    patrick_logger.log_it('INFO: OK, we loaded the list of people Paul Graham has actually thanked.', 3)
    
    # OK, now get a list of (previously) hot topics
    # Seems that 1 August 2015 is the first day for which this API returns data. I'm OK with not looking at the 31st of any month. 
    try:
        which_date = '2015/%02d/%02d/' % (random.randint(8,12), random.randint(1,30))
        patrick_logger.log_it("INFO: we're loading nouns from Wikipedia's top 1000 articles from %s" % which_date, 3)
        wp_response = urlopen('http://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia/all-access/2015/10/10/' % which_date)
        wp_data = wp_response.read().decode()
        wp_dict = json.loads(wp_data)
        patrick_logger.log_it("INFO: we loaded and parsed the relevant JSON data from Wikipedia.", 3)
        wp_articles = [ wp_dict['items'][0]['articles'][x]['article'] for x in range(len(wp_dict['items'][0]['articles'])) ]
        real_wp_articles = [x.replace('_', ' ') for x in wp_articles if not x.startswith(wp_specials)]
        patrick_logger.log_it("INFO: There are %d 'real' articles from that date" % len(real_wp_articles), 3)
    except Exception as e:
        patrick_logger.log_it('INFO: exception %s occurred' % e, 1)
        real_wp_articles = []
    
    grateful_to = list(set(random.sample(actually_thanked_by_graham + real_wp_articles, random.randint(3,10))))

    ret = 'Thanks to ' + ', '.join(grateful_to[:-1]) + ', and ' + grateful_to[-1]
    ret = ret + ' ' + random.choice(['for their feedback on these thoughts.', 'for inviting me to speak.',
       'for reading a previous draft.', 'for sharing their expertise on this topic.', 'for putting up with me.'])
    return ret

if __name__ == "__main__":
    patrick_logger.log_it("INFO: Everything's set up, let's go...")

    for which_para in range(random.randint(2,8)):
        paragraph_length = random.choice(list(range(7, 12)))
        patrick_logger.log_it('      Getting %d sentences.' % paragraph_length)
        the_brainwave = the_brainwave + gen_text(the_mapping, the_starts, the_markov_length, paragraph_length, paragraph_break_probability=0) + '\n'

    the_title = get_a_title(the_brainwave)
    patrick_logger.log_it('INFO: Title is: %s' % the_title)
    
    if force_notes or random.random() <= .45:
        the_brainwave = the_brainwave + '\n' + get_notes()
    
    if force_gratitude or random.random() <= 1 / 3 :
        the_brainwave = the_brainwave + '\n' + get_thanks()

    patrick_logger.log_it("INFO: here's the brainwave:\n\n%s" % the_brainwave, 2)
    
    brainwave_tags = normal_tags + get_some_tags(the_brainwave)
    patrick_logger.log_it('INFO: tags are: %s' % brainwave_tags, 2)

    the_brainwave = '\n'.join([ '<p>%s</p>' % x if not x.strip().startswith('<') else x for x in the_brainwave.split('\n') ])
    the_status = social_media.tumblr_text_post(douchebag_brainwaves_client, brainwave_tags, the_title, the_brainwave)
    patrick_logger.log_it('INFO: the_status is: ' + pprint.pformat(the_status), 2)

    patrick_logger.log_it('INFO: We\'re done', 2)
