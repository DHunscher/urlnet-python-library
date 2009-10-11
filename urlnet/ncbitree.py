#!/usr/bin/env python
# $Id$
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
The NCBITree class provides a foundation for classes that will create a network
by generating a tree of NCBI API objects. 
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
from ncbiauthorcosmosurl import NCBIAuthorCosmosUrl
from ncbiurl import NCBIUrl
from ncbicoauthorurl import NCBICoAuthorUrl

# supported NCBI apis
NCBI_AUTHOR_COSMOS_API = 1
NCBI_CO_AUTHOR_API = 2
NCBI_ELINK_API = 3
# error default
NO_API_SPECIFIED = 0


     
###################################################################
###################################################################
###################################################################

class NCBITree(UrlTree):
    """
    Class representing a tree of NCBI URIs
    """

    # supported NCBI apis
    NCBI_AUTHOR_COSMOS_API = 1
    NCBI_CO_AUTHOR_API = 2
    NCBI_ELINK_API = 3
    # error default
    NO_API_SPECIFIED = 0

    myAPI = NO_API_SPECIFIED
    
    def __init__(self,
                 _email = None,
                 _maxLevel = 2,
                 _urlclass = None,
                 _workingDir=None, 
                 _default_socket_timeout = 15,
                 _sleeptime = 3,
                 _userAgent = None,
                 _netItemClass = UrlNetItem,
                 _NCBIApi = NO_API_SPECIFIED,
                 _NCBIResultSetSizeLimit = NCBIUrl.DEFAULT_RESULTSET_SIZE_LIMIT): 
        try:
            log = Log('NCBITree ctor')
            #
            # Most of the work is done by the parent class. All we do
            # here is specify what class to use for constructing Url
            # instances. We need to use a descendant of the Url class
            # for this purpose.
            #

            # NCBI requires at least 3 seconds sleep time between requests
            if _sleeptime == None or _sleeptime < 3:
                _sleeptime = 3

                
            self.myAPI = _NCBIApi
            if self.myAPI == NCBI_CO_AUTHOR_API:
                
                   
                UrlTree.__init__(self,
                                 _maxLevel=_maxLevel,
                                 _urlclass = NCBICoAuthorUrl,
                                 _workingDir=_workingDir, 
                                 _default_socket_timeout = _default_socket_timeout,
                                 _sleeptime=_sleeptime,
                                 _userAgent=_userAgent,
                                 _netItemClass = _netItemClass)
            elif self.myAPI == NCBI_AUTHOR_COSMOS_API:
                UrlTree.__init__(self,
                                 _maxLevel=_maxLevel,
                                 _urlclass = NCBIAuthorCosmosUrl,
                                 _workingDir=_workingDir, 
                                 _default_socket_timeout = _default_socket_timeout,
                                 _sleeptime=_sleeptime,
                                 _userAgent=_userAgent,
                                 _netItemClass = _netItemClass)
            elif self.myAPI == NCBI_ELINK_API:
                UrlTree.__init__(self,
                                 _maxLevel,
                                 NCBIUrl,
                                 _workingDir=_workingDir, 
                                 _default_socket_timeout = _default_socket_timeout,
                                 _sleeptime=_sleeptime,
                                 _userAgent=_userAgent,
                                 _netItemClass = _netItemClass)
            else:
                raise Exception, 'no NCBI API specified'

            if _email:
                self.SetProperty('email',_email)
            else:
                _email = GetConfigValue("email")
                if _email:
                    self.SetProperty('email',_email)
                

            if _NCBIResultSetSizeLimit:
                self.SetProperty('NCBIResultSetSizeLimit',_NCBIResultSetSizeLimit)
                
        except Exception, e:
            self.SetLastError('in __init__: ' + str(e))

############################################################
####################   public APIs   #######################
############################################################

    # One or more of these must be implemented in a derived class.
    
    def BuildUrlTree(self,startUrl,parentItemIdx=None,currentLevel=0,alreadyMassaged=False):
        """
        not supported
        """
        raise Exception, 'BuildUrlTree not supported.'
        


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
        
    def BuildUrlForest(self,Urls,level=0, parentBase=None, parentIdx=None):
        """
        not supported
        """
        raise Exception, 'BuildUrlTree not supported.'

############################################################
##################  helper functions  ######################
############################################################

    def PutUrl(self, parentUrlNetItemIdx, urlToAdd, level,properties=None):
        """
        Add a new URL to the network, or if it already exists, ignore it.
        In either case, return the Node and item index for the URL.

        For NCBI URLs, eliminate use of domain network, which is
        inapplicable.
        """
        log = Log('NCBITree.PutUrl',urlToAdd)    
        #print parentUrlNetItemIdx
        #print urlToAdd
        self.ResetLastError()
        try:
            isNewItem = False
            
            item = self.GetUrlNetItemByUrl(urlToAdd)
            # see if URL is already registered
            if not item:
                # new item
                isNewItem = True
                itemIdx = self.masterItemIdx + 1
                try:
                    item = self.netitemclass(itemIdx,urlToAdd,self,self.urlclass)
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
            if parentUrlNetItemIdx: 
                item.AppendParent(parentUrlNetItemIdx)
                itemIdx = item.GetIdx()
                # get parent's edgelist and append this
                parent = self.GetUrlNetItemByIndex(parentUrlNetItemIdx)
                if parent:
                    parent.AppendChild(itemIdx)
                                

            #print 'PutUrl added %s...' % urlToAdd
            return (item,itemIdx,isNewItem)
                
        except Exception, e:
            self.SetLastError('in NCBITree.putUrl: ' + str(e) + '\nurl: ' + urlToAdd)
            return (None,-1,False)


    def MassageUrl(self,url):
        return url

    def GetIndexByDomain(self,domain):        
        """
        not supported
        """
        raise Exception, 'NCBITree.GetIndexByDomain not supported.'

    def GetDomainByIndex(self,idx):        
        """
        not supported
        """
        raise Exception, 'NCBITree.GetDomainByIndex not supported.'

    def MapFunctionToDomainNetwork(self,functionToMap,start=1,level = 0,direction=SEARCH_DOWN,args=None,stack=None):
        """
        not supported
        """
        raise Exception, 'NCBITree.MapFunctionToDomainNetwork not supported.'

    def MapFunctionToDomainParentChildPairs(self,functionToMap,args=None,unique=True):
        """
        not supported
        """
        raise Exception, 'NCBITree.MapFunctionToDomainParentChildPairs not supported.'

    def MapFunctionToDomainItemList(self,functionToMap,args=None):
        """
        not supported
        """
        raise Exception, 'NCBITree.MapFunctionToDomainItemList not supported.'

    def MapFunctionToDomainNetwork(self,functionToMap,start=1,level = 0,direction=SEARCH_DOWN,args=None,stack=None):
        """
        not supported
        """
        raise Exception, 'NCBITree.MapFunctionToDomainNetwork not supported.'

    def MapFunctionToUniqueDomainParentChildPairs(self,functionToMap,args=None,unique=True):
        """
        not supported
        """
        raise Exception, 'NCBITree.MapFunctionToUniqueDomainParentChildPairs not supported.'

    # network serializers 
    def WritePajekStream(self,netname,stream,doDomains=False,doOnlyDomains=False,useTitles=False):
        """
        NCBI doesn't use the domain concept, so we override the Pajek parameters having to do with them.
        We include the two spurious domain-related arguments so we can rely on the URLTree WritePajekFile()
        function, rather than having to copy and paste it here.
        """
        ### PAJEK
        log = Log('NCBITree.WritePajekStream',netname)
        try:
            # force doDomains to False
            if doDomains:
                log.Write('There are no domain networks in NCBI trees')
            UrlTree.WritePajekStream(self,netname,stream,doDomains=False,doOnlyDomains=False,useTitles=useTitles)
        except Exception, e:
            self.SetLastError('In NCBITree.WritePajekStream: ' + str(e))
            raise

    def WriteGuessFile(self,filename,doUrlNetwork=True,useTitles=False):
        log = Log('NCBITree.WriteGuessFile',filename)
        try:
            # force doUrlNetwork to True
            if doUrlNetwork == False:
                log.Write('There are no domain networks in NCBI trees')
            UrlTree.WriteGuessFile(self,filename,True)
        except Exception, e:
            self.SetLastError('In NCBITree.WriteGuessFile: ' + str(e))
            raise


def main():
    # dir to write to
    workingDir =urlutils.GetConfigValue('workingDir')
    log.logging=True
    myLog = Log('main')
    try:
        print 'An exception is expected behavior...'
        x = NCBITree(_maxLevel=2,
                           _email='dalehuns@umich.edu',
                           _NCBIApi=NCBI_CO_AUTHOR_API,
                           _workingDir=workingDir,
                           _sleeptime=1)
        x.BuildUrlTree('Hunscher DA') # should throw an exception...
        print 'test failed!'
    except Exception, e:
        print str(e)

if __name__ == '__main__':
    main()
    sys.exit(0)
    
