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
from twitterurl import TwitterUrl
import twitterconstants

# DeWitt Clinton's Twitter library for Python- requires simpleJSON
import twitter

# supported twitter apis


# error default
NO_API_SPECIFIED = 0


     
###################################################################
###################################################################
###################################################################

class TwitterTree(UrlTree):
    """
    Class representing a tree of twitter URIs
    """
    username   = None
    password   = None
    twitterApi = twitterconstants.NO_API_SPECIFIED
    
    def __init__(self,
                 _twitterUser,
                 _twitterPassword,
                 _twitterApi = twitterconstants.NO_API_SPECIFIED,
                 _email = None,
                 _maxLevel = 2,
                 _urlclass = None,
                 _workingDir=None, 
                 _default_socket_timeout = 15,
                 _sleeptime = 3,
                 _userAgent = None,
                 _netItemClass = UrlNetItem
                ): 
        try:
            log = Log('TwitterTree ctor')
            #
            # Most of the work is done by the parent class. All we do
            # here is specify what class to use for constructing Url
            # instances. We need to use a descendant of the Url class
            # for this purpose.
            #

            # twitter requires at least 1 seconds sleep time between requests
            if _sleeptime == None or _sleeptime < 1:
                _sleeptime = 1
                
            urlClass = _urlclass
            if urlClass == None:
                urlClass = TwitterUrl

            UrlTree.__init__(self,
                             _maxLevel=_maxLevel,
                             _urlclass = urlClass,
                             _workingDir=_workingDir, 
                             _default_socket_timeout = _default_socket_timeout,
                             _sleeptime=_sleeptime,
                             _userAgent=_userAgent,
                             _netItemClass = _netItemClass)

            
            self.username       = _twitterUser
            self.password       = _twitterPassword
            self.twitterApi     = _twitterApi
            if not (self.username and self.password):
                raise Exception, \
                   'TwitterTree requires a username and password.'
            elif self.twitterApi == twitterconstants.NO_API_SPECIFIED \
                    or self.twitterApi == None:
                raise \
                    Exception, \
                    'TwitterTree requires an API to be ' + \
                      'selected (see twitterconstants.py).'
            
            self.myApi = None
            self.SetProperty('TwitterFriendLimit', twitterconstants.FRIEND_LIMIT)
            self.SetProperty('TwitterFollowerLimit', twitterconstants.FOLLOWER_LIMIT)
            
            try:
                self.myApi = twitter.Api(username=self.username, password=self.password)
            except Exception, e:
                raise Exception, '%s in TwitterTree constructor: %s' % (str(type(e)), str(e))
            if not self.myApi:
                raise Exception, 'TwitterTree API call returned None.'
        except Exception, e:
            self.SetLastError('in __init__: ' + str(e))
            raise

############################################################
####################   public APIs   #######################
############################################################

    # One or more of these must be implemented in a derived class.
    
    def BuildUrlTree(self,startUrl,parentItemIdx=None,currentLevel=0,alreadyMassaged=False):
        """
        not supported
        """
        raise Exception, 'BuildUrlTree not supported.'
        

    def BuildUrlForest(self,Urls,level=0, parentBase=None, parentIdx=None):
        """
        Given a list of urls to be processed, build a tree by calling BuildUrlTree
        successively with each url in the list. In this case there is no root URL,
        unless this is called at some level other than the root.
        """
        self.ResetLastError()
        log = Log('vanilla BuildUrlForest')
        currentLevel = level
        rootIdx = parentIdx
        childUrl = None
        try:
            for childUrl in Urls:

                
                childItem = self.BuildUrlTree(startUrl=childUrl,parentItemIdx=rootIdx,
                                currentLevel=currentLevel)
                if not childItem:
                    log.Write( 'in BuildUrlForest, BuildUrlTree failed for childUrl: ' + str(childUrl) )
            return True
        except Exception, e:
            self.SetLastError('in BuildUrlForest: ' + str(e)\
                              + '\ncurrent url: ' + str(childUrl))
            return False


    def BuildUrlTreeWithPlaceholderRoot(self,rootPlaceholder,Urls):
        """
        not supported
        """
        raise Exception, 'BuildUrlTreeWithPlaceholderRoot not supported.'
        
        
    def BuildUrlForestWithPhantomRoot(self,phantomRoot):
        """
        not supported
        """
        raise Exception, 'BuildUrlForestWithPhantomRoot not supported.'
        
############################################################
##################  helper functions  ######################
############################################################


    def FormatTwitterItemName(self,user):
        '''
        For use in output to networks. Can be overridden in derived
        classes to handle different types of networks built on Twitter
        data.
        '''
        return user['user']
    
    def PutUrl(self, 
            parentUrlNetItemIdx, 
            urlToAdd, 
            level,
            properties=None
            ):
        """
        Add a new URL to the network, or if it already exists, ignore it.
        In either case, return the Node and item index for the URL.

        For twitter URLs, eliminate use of domain network, which is
        inapplicable.
        """
        log = Log('twitterTree.PutUrl',urlToAdd)    
        #print parentUrlNetItemIdx
        #print urlToAdd
        self.ResetLastError()
        try:
            # in Twitter, a friend is someone you follow (arc from you to
            # the friend in the network), and a follower is someone who
            # has friended you (arc from follower to you)
            # see if the current item is a friend or follower
            # if a follower, add this item to parent's parent list,
            # and to the item's child list. If a friend, add this item 
            # to parent's child list, and parent to this item's parent
            # list.
            isFollower = self.GetProperty('ProcessingFollowers')
            isNewItem = False
            
            item = self.GetUrlNetItemByUrl(urlToAdd)
            # see if URL is already registered
            if not item:
                # new item
                isNewItem = True
                itemIdx = self.masterItemIdx + 1
                try:
                    item = self.netitemclass(
                        itemIdx,
                        urlToAdd,
                        self,
                        _urlclass = self.urlclass)
                except Exception, e:
                    raise Exception, 'self.netitemclass constructor failed: '+str(e)
                item.SetProperty('level',level)
                if properties:
                    item.SetProperties(properties)
                self.UrlNetItemByIndex[itemIdx] = item
                self.IndexByUrl[urlToAdd] = itemIdx
                self.masterItemIdx = itemIdx
            else:
                itemIdx = item.GetIdx()
                oldLevel = item.GetProperty('level')
                if oldLevel != None and level < oldLevel:
                    item.SetProperty('level',level)
                    if oldLevel == self.maxLevel:
                        # force call to GetUrlForest; it wasn't done before because
                        # this item was at the max level the first time it was
                        # encountered.
                        isNewItem = True
                        
                
            # one way or another, we now have an item; if we also have
            # a parent (i.e., if this is not the root item), add linkages
            # to the item's parent list and the parent's child list
            # (or vice versa if this is a friend of the parent)
            if isFollower: 
                # current user is a follower of the "parent" user;
                # reverse direction of arc. Append parent to the current
                # user's child list (i.e. users s/he is following)
                if parentUrlNetItemIdx: 
                    if parentUrlNetItemIdx not in item.GetChildren():
                        item.AppendChild(parentUrlNetItemIdx)
                    itemIdx = item.GetIdx()
                    # get parent's edgelist and append this user
                    # to its parent (i.e. follower) list
                    parent = self.GetUrlNetItemByIndex(parentUrlNetItemIdx)
                    if parent != None and itemIdx not in parent.GetParents():
                        parent.AppendParent(itemIdx)
            else: 
                # the current user is being followed by "parent" user
                # The arc should go *to* current item *from* the parent item,
                # so add parent idx to this item's parent list, and add
                # this item to parent's child list.
                if parentUrlNetItemIdx: 
                    if parentUrlNetItemIdx not in item.GetParents():
                        item.AppendParent(parentUrlNetItemIdx)
                    itemIdx = item.GetIdx()
                    # get parent's edgelist and append this user to his/her
                    # child list
                    parent = self.GetUrlNetItemByIndex(parentUrlNetItemIdx)
                    if parent != None and itemIdx not in parent.GetChildren():
                        parent.AppendChild(itemIdx)
                                

            #print 'PutUrl added %s...' % urlToAdd
            return (item,itemIdx,isNewItem)
                
        except Exception, e:
            self.SetLastError('in twitterTree.putUrl: ' + str(e) + '\nurl: ' + urlToAdd)
            return (None,-1,False)


    def MassageUrl(self,url):
        return url

    def GetIndexByDomain(self,domain):        
        """
        not supported
        """
        raise Exception, 'twitterTree.GetIndexByDomain not supported.'

    def GetDomainByIndex(self,idx):        
        """
        not supported
        """
        raise Exception, 'twitterTree.GetDomainByIndex not supported.'

    def MapFunctionToDomainNetwork(self,functionToMap,start=1,level = 0,direction=SEARCH_DOWN,args=None,stack=None):
        """
        not supported
        """
        raise Exception, 'twitterTree.MapFunctionToDomainNetwork not supported.'

    def MapFunctionToDomainParentChildPairs(self,functionToMap,args=None,unique=True):
        """
        not supported
        """
        raise Exception, 'twitterTree.MapFunctionToDomainParentChildPairs not supported.'

    def MapFunctionToDomainItemList(self,functionToMap,args=None):
        """
        not supported
        """
        raise Exception, 'twitterTree.MapFunctionToDomainItemList not supported.'

    def MapFunctionToDomainNetwork(self,functionToMap,start=1,level = 0,direction=SEARCH_DOWN,args=None,stack=None):
        """
        not supported
        """
        raise Exception, 'twitterTree.MapFunctionToDomainNetwork not supported.'

    def MapFunctionToUniqueDomainParentChildPairs(self,functionToMap,args=None,unique=True):
        """
        not supported
        """
        raise Exception, 'twitterTree.MapFunctionToUniqueDomainParentChildPairs not supported.'

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


def main():
    '''
    # dir to write to
    workingDir =urlutils.GetConfigValue('workingDir')
    log.logging=True
    myLog = Log('main')
    try:
        print 'An exception is expected behavior...'
        x = TwitterTree(_maxLevel=2,
                           _email='dalehuns@umich.edu',
                           _twitterApi=twitter_CO_AUTHOR_API,
                           _workingDir=workingDir,
                           _sleeptime=1)
        x.BuildUrlTree('Hunscher DA') # should throw an exception...
        print 'test failed!'
    except Exception, e:
        print str(e)

if __name__ == '__main__':
    main()
    sys.exit(0)
    '''
