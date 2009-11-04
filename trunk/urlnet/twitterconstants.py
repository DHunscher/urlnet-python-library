#!/usr/bin/env python
# $Id: logging3.py 56 2009-10-11 21:03:43Z dalehunscher $
###################################################################
#                                                                 #
#                     UrlNet Python Library                       #
#            Copyright (c) Dale A. Hunscher, 2007-2009            #
#                     All rights reserved                         #
#                                                                 #
#                                                                 #
# UrlNet is free for non-commercial use.                          #
# For commercial uses, contact dale.hunscher@thenextroguewave.com #
#                                                                 #
###################################################################
# twitterconstants.py

# supported twitter apis


# error default
NO_API_SPECIFIED = (-1)
FRIENDS = 0
FOLLOWERS = 1
HASHTAGS = 2
TWEETS = 3
PEOPLE = 4 # friends and followers

COSMOS = 99  # people, tweets, and hashtags

# Twitter has a limit on how many API calls you can do, so limit what
# you get (unless you can get whitelisted; see Twitter API wiki for
# details).

FOLLOWER_LIMIT  = 10
FRIEND_LIMIT    = 10

