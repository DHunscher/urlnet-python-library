#!/usr/bin/env python
# $Id: twitterurl.py 55 2009-10-11 21:00:51Z dalehunscher $
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

import re
import string
import sys
import os
import time

from urllib import unquote
from urllib import urlencode
from urlparse import *
from htmllib import HTMLParser
from formatter import NullFormatter

# We use DeWitt Clinton's Python wrapper for Twitter:
# http://code.google.com/p/python-twitter/

import twitter
import twitterconstants

from url import Url
from log import Log

#################### the TwitterUrl class ######################
class TwitterUrl(Url):
    "A class encapsulating low-level functions for accessing Twitter"

    
    def __init__(self, _inboundUrl, _userObject = None, _network=None):
        """initialize Twitter url instance.  In this case, instead of
           a URL, what we get can be a user's screen name, a user Id,
           or a hashtag. For starters...
        """
        try:
            # _inboundUrl should be the screen name of a Twitter user;
            # _userObject should be the result of a twitter.Api.GetUser()
            # call (optional; will be retrieved if not present)
            
            log = Log('TwitterUrl ctor',_inboundUrl)
            Url.__init__(self,_inboundUrl=_inboundUrl,_network=_network,_doInit=False)
            self.network = _network
            self.userObject = _userObject
            if self.userObject == None:
                self.userObject = self.network.myApi.GetUser(_inboundUrl)
            self.myUser = self.UserDict(self.userObject)
            
            # turn off use of cached pages, if it is turned on
            # (which it is by default in descendant classes of UrlTree)
            if self.network.useCachedPageIfItExists == True:
                self.network.useCachedPageIfItExists = False
                
        except Exception, e:
            self.SetLastError('%s: %s' % (str(type(e)), str(e)) )
            raise

    def UserDict(self,u):
        return  {
                'user'          : u.GetName(), 
                'screenName'    : u.GetScreenName(), 
                'id'            : u.GetId(),
                'userObject'    : u, 
                }



    #########################################
    ############ high-level functions #######
    #########################################

    def GetFriends(self):
        '''
        Return a list of structures containing the current user's
        friends' screen names, real names, twitter IDs, and User objects
        '''
        log = Log('TwitterUrl.GetFriends')
        try:
            friends = []
            flist = self.network.myApi.GetFriends(self.myUser['id'])
            limit = self.network.GetProperty('TwitterFriendLimit')
            if limit == None:
                limit = twitterconstants.FRIEND_LIMIT
            flist = flist[:limit]

            for u in flist:
                friends.append(self.UserDict(u))
            return friends
        except Exception, e:
            print '%s %s' % (str(type(e)), str(e))
            raise
    
    def GetFollowers(self):
        '''
        Return a list of structures containing the current user's
        followers' screen names, real names, and twitter IDs
        '''
        log = Log('TwitterUrl.GetFollowers')
        try:
            followers = []
            flist = self.network.myApi.GetFollowers(self.myUser['userObject'])
            limit = self.network.GetProperty('TwitterFollowerLimit')
            if limit == None:
                limit = twitterconstants.FOLLOWER_LIMIT
            flist = flist[:limit]
            for u in flist:
                followers.append(self.UserDict(u))
            return followers
        except Exception, e:
            print '%s %s' % (str(type(e)), str(e))
            raise
    
    def RetrieveUrlContent(self,theUrl=None,getTitleOnly=False):
        '''
        Turn off page cacheing for Twitter API calls. Not sure this will
        even get called...
        '''
        log = Log('TwitterUrl.RetrieveUrlContent')
        try:
            self.thePage = None
            page = Url.RetrieveUrlContent(self,theUrl)
            self.thePage = None
            return page
        except Exception, e:
            print '%s %s' % (str(type(e)), str(e))
            raise
        
    def GetAnchorList(self, type):
        log = Log('TwitterUrl.GetAnchorList')
        try:
            if type == twitterconstants.FRIENDS:
                return self.GetFriends()
            elif type == twitterconstants.FOLLOWERS:
                return self.GetFollowers()
            else:
                raise Exception, 'Anchor list request for unknown type %s ' % (str(type))
        except Exception, e:
            print '%s %s' % (str(type(e)), str(e))
            raise


def main():
        log = Log('TwitterUrl main')
        try:
            from twittertree import TwitterTree
            
            net = TwitterTree('DHunscher','OffWorld')
            url = TwitterUrl('DHunscher',_network=net)
            f = url.GetFriends()
            print str(f)
            f = url.GetFollowers()
            print str(f)
        except Exception, e:
            print '%s %s' % (str(type(e)), str(e))
            
if __name__ == '__main__':
    main()
