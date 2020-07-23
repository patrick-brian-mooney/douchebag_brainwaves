#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Unit providing simple interfaces for social media accounts I use.

I import another unit, social_media_auth.py, that contains the necessary
authentication constants. social_media_auth.py is not, of course, contained
in the GitHub repo that contains this unit, because, well, those are my private
authentication constants.

This script is copyright 2017-18 by Patrick Mooney. It is licensed under the GNU
GPL, either version 3 or (at your option) any later version. See the file
LICENSE.md for details.
"""

from tumblpy import Tumblpy     # [sudo] pip[3] install python-tumblpy; https://github.com/michaelhelmick/python-tumblpy
import tweepy                   # http://www.tweepy.org/

verbosity_level = 2

def log_it(what, debug_level=1):
    if debug_level >= verbosity_level:
        print(what)

# Format for Tumblr clients is:
# the_client = Tumblpy(
#    'a string',   # consumer_key
#    'a string',   # consumer_secret
#    'a string',   # token_key
#    'a string'    # token_secret       )

def Tumblpy_from_dict(data):
    """Create a Tumblpy object from the authentication constants stored in a dictionary."""
    return Tumblpy(data['consumer_key'], data['consumer_secret'], data['token_key'], data['token_secret'])

def tumblr_text_post(the_client, the_tags, the_title, the_content):
    """Create a text post on Tumblr, using THE_CLIENT as an API object. THE_TAGS,
    THE_TITLE, and THE_CONTENT all describe what you'd expect them to describe, and
    they're all strings.

    Returns two dictionaries: one contains a status code, the other contains more
    info.
    """
    tumblr_data = the_client.post('user/info')
    tumblog_url = tumblr_data['user']['blogs'][0]['url']
    if tumblog_url.startswith('https://'):
        tumblog_url = 'http://' + tumblog_url[8:]
    the_status = the_client.post('post', blog_url=tumblog_url,
                                 params={'type': 'text', 'tags': the_tags, 'title': the_title, 'body': the_content})
    return the_status, tumblr_data


# Format for Twitter clients is a dictionary:
# a_client = {
#    'consumer_key'        : 'a string',
#    'consumer_secret'     : 'a string',
#    'access_token'        : 'a string',
#    'access_token_secret' : 'a string'
#    }

def get_new_twitter_API(client_credentials):
    """Get an instance of the Tweepy API object to work with."""
    auth = tweepy.OAuthHandler(client_credentials['consumer_key'], client_credentials['consumer_secret'])
    auth.set_access_token(client_credentials['access_token'], client_credentials['access_token_secret'])
    ret = tweepy.API(auth)
    ret.wait_on_rate_limit, ret.wait_on_rate_limit_notify = True, True
    return ret

def _the_API(client_credentials=None, API_instance=None):
    """Private convenience function to get an API instance object from several
    possible values that the calling code might supply.
    """
    if API_instance is None:
        if client_credentials is None:
            raise NotImplementedError("You must pass either client credentials or an already-initialized API instance")
        else:
            API_instance = get_new_twitter_API(client_credentials)
    return API_instance

def post_tweet(the_tweet, client_credentials=None, API_instance=None):
    """Post a tweet, THE_TWEET. If you already have a Tweepy API instance handy
    pass that in as API_instance; otherwise, pass in a CLIENT_CREDENTIALS
    dictionary and a throwaway API object will be created, then discarded.
    """
    return _the_API(client_credentials, API_instance).update_status(status=the_tweet)

def post_reply_tweet(text, user_id, tweet_id, client_credentials=None, API_instance=None):
    """Post a reply tweet. TWEET_ID is the id of the tweet that this tweet is a reply
    to; the USER_ID is the person to whom we are replying, and the user_id is
    automatically prepended to the beginning of TEXT before posting.

    This routine is now believed to work; previously, it was a stub.
    """
    log_it("INFO: posting tweet: @%s %s  ----  in reply to tweet ID# %d" % (user_id, text, tweet_id))
    return _the_API(client_credentials, API_instance).update_status("@%s %s" % (user_id, text), in_reply_to_status_id = tweet_id)

def modified_retweet(text, user_id, tweet_id):
    """Tweet a message about another tweet.
    """
    log_it("%s\n\nhttps://twitter.com/%s/status/%s" % (text, user_id, tweet_ID))
    the_API.update_status("%s\n\nhttps://twitter.com/%s/status/%s" % (text, user_id, tweet_ID))

def send_DM(the_API, text, user):
    """Send a direct message to another user. Currently, this method is only used to
    reply to DMs sent by other users. Does not currently do anything.
    """
    log_it("DM @%s: %s" % (user, text))
    the_API.send_direct_message(user=user, text=text)
