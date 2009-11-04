#!/usr/bin/env python
# $Id: twittertree.py 55 2009-10-11 21:00:51Z dalehunscher $
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

"""
The TwitterTree class provides a foundation for classes that will create a network
by generating a tree of twitter API objects. 
"""

import re
import string
import sys
import os
import urllib
import socket
import time

from urllib import unquote
from urllib2 import urlopen, Request
from urllib import urlencode
from urlparse import *
from htmllib import HTMLParser
from formatter import NullFormatter
from Ft.Xml import InputSource, Sax

from object import Object
from url import Url, DomainFromHostName
from urlparse import urlparse
from urlnetitem import UrlNetItem
from domainnetitem import DomainNetItem
from log import Log, logging, file_only
import log
from urltree import UrlTree
from urlutils import *
from twittertree import TwitterTree
from twitterurl import TwitterUrl
import twitterconstants



     
###################################################################
###################################################################
###################################################################

class TwitterPeopleTree(TwitterTree):
    """
    Class representing a tree of twitter URIs
    """

    
    def __init__(self,
                 _twitterUser,
                 _twitterPassword,
                 _twitterApi = twitterconstants.NO_API_SPECIFIED,
                 _maxLevel = 2,
                 _urlclass = None,
                 _workingDir=None, 
                 _default_socket_timeout = 15,
                 _sleeptime = 3,
                 _userAgent = None,
                 _netItemClass = UrlNetItem
                ): 
        try:
            log = Log('TwitterPeopleTree ctor')
            #
            # Most of the work is done by the parent class. All we do
            # here is specify what class to use for constructing Url
            # instances. We need to use a descendant of the Url class
            # for this purpose.
            #

            # twitter requires at least 1 seconds sleep time between requests
            sleepTime = _sleeptime
            if sleepTime == None or sleepTime < 1:
                sleepTime = 1 # always >= 1 second
                
            urlClass = _urlclass
            if urlClass == None:
                urlClass = TwitterUrl

            TwitterTree.__init__(
                 self,
                 _twitterUser=_twitterUser,
                 _twitterPassword=_twitterPassword,
                 _twitterApi = _twitterApi,
                 _maxLevel = _maxLevel,
                 _urlclass = urlClass, # input argument overridden
                 _workingDir=_workingDir, 
                 _default_socket_timeout = _default_socket_timeout,
                 _sleeptime = sleepTime, # input argument overridden
                 _userAgent = _userAgent,
                 _netItemClass = _netItemClass
                )
                
            if self.twitterApi not in (\
                twitterconstants.PEOPLE,\
                twitterconstants.FRIENDS,\
                twitterconstants.FOLLOWERS\
                ):
                raise \
                    Exception, \
                    'TwitterPeopleTree requires an API to be ' + \
                      'selected (see twitterconstants.py), and ' + \
                      'it must be FRIENDS, FOLLOWERS, or PEOPLE.'
                
        except Exception, e:
            self.SetLastError('in __init__: ' + str(e))
            raise


############################################################
####################   public APIs   #######################
############################################################

    def BuildUrlTree(self,startUrl,parentItemIdx=None,currentLevel=0):
        """
        The startUrl argument must be a Twitter screen name or User object.
        
        Build the tree, starting from a given URL. Will be called recursively
        for child "URL"s to whatever level the UrlTree is constructed to handle.
        """
        log = Log('TwitterPeopleTree.BuildUrlTree','url=' + str(startUrl) + '\nparent idx=' + str(parentItemIdx) + '\nlevel=' + str(currentLevel))
        currentItem = None
        # This property determines the direction of arcs in 
        # TwitterTree.PutUrl(): user -> friend and follower -> user
        saveFollowers = self.GetProperty('ProcessingFollowers')
        Urls = None
        try:
            if 'str' in str(type(startUrl)):
                url = startUrl
            else: # better be a twitter user dict
                url = startUrl['screenName']
                
            (currentItem, currentIdx, isNewItem) = self.PutUrl(parentItemIdx,url,currentLevel)
            if (not currentItem):
                return False
            if isNewItem and not (currentLevel >= self.maxLevel):
                # friends
                fo = None
                fr = None
                theUrl = currentItem.GetUrl()
                if  self.twitterApi == twitterconstants.PEOPLE or \
                    self.twitterApi == twitterconstants.FRIENDS:
                    self.SetProperty('ProcessingFollowers',False)
                    fr = self.BuildUrlForest(Urls=theUrl.GetAnchorList(twitterconstants.FRIENDS),
                                        level=currentLevel+1,parentBase=url, parentIdx=currentIdx)
                if  self.twitterApi == twitterconstants.PEOPLE or \
                    self.twitterApi == twitterconstants.FOLLOWERS:
                    # followers
                    self.SetProperty('ProcessingFollowers',True) 
                    fo = self.BuildUrlForest(Urls=theUrl.GetAnchorList(twitterconstants.FOLLOWERS),
                                        level=currentLevel+1,parentBase=url, parentIdx=currentIdx)
                ret = (fo in (None,True)) and (fr in (None, True)) 
            else:
                ret = True
            self.SetProperty('ProcessingFollowers',saveFollowers)
            return ret
        except Exception, e:
            self.SetProperty('ProcessingFollowers',saveFollowers)
            self.SetLastError('%s in TwitterPeopleTree.BuildUrlTree: %s' % (str(type(e)), str(e)))
            return False


    # network serializers 
    def WritePajekStream(self,netname,stream,doDomains=False,doOnlyDomains=False,useTitles=False):
        """
        twitter doesn't use the domain concept, so we override the Pajek parameters having to do with them.
        We include the two spurious domain-related arguments so we can rely on the URLTree WritePajekFile()
        function, rather than having to copy and paste it here.
        """
        ### PAJEK
        log = Log('twitterTree.WritePajekStream',netname)
        try:
            # force doDomains to False
            if doDomains:
                log.Write('There are no domain networks in twitter trees')
            UrlTree.WritePajekStream(self,netname,stream,doDomains=False,doOnlyDomains=False,useTitles=useTitles)
        except Exception, e:
            self.SetLastError('In twitterTree.WritePajekStream: ' + str(e))
            raise

    def WriteGuessFile(self,filename,doUrlNetwork=True,useTitles=False):
        log = Log('twitterTree.WriteGuessFile',filename)
        try:
            # force doUrlNetwork to True
            if doUrlNetwork == False:
                log.Write('There are no domain networks in twitter trees')
            UrlTree.WriteGuessFile(self,filename,True)
        except Exception, e:
            self.SetLastError('In twitterTree.WriteGuessFile: ' + str(e))
            raise

