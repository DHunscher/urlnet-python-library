#!/usr/bin/env python
# $Id$
###################################################################
#                                                                 #
#                     UrlNet Python Library                       #
#            Copyright (c) Dale A. Hunscher, 2007-2008            #
#                     All rights reserved                         #
#                                                                 #
#                                                                 #
# UrlNet is free for non-commercial use.                          #
# For commercial uses, contact dale.hunscher@thenextroguewave.com #
#                                                                 #
###################################################################

"""
The NCBICoAuthorTree class creates a network by generating a tree of co-authors from data in Pub Med.
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
from ncbitree import NCBITree
from ncbicoauthorurl import NCBICoAuthorUrl
     
###################################################################
###################################################################
###################################################################

class NCBICoAuthorTree(NCBITree):
    """
    Class representing a tree of NCBI URIs
    """


    
    def __init__(self,
                 _email = None,
                 _maxLevel = 2,
                 _urlclass = NCBICoAuthorUrl,
                 _workingDir=None, 
                 _default_socket_timeout = 15,
                 _sleeptime = 3,
                 _userAgent = None,
                 _netItemClass = UrlNetItem): 
        try:
            log = Log('NCBICoAuthorTree ctor')
            #
            # Most of the work is done by the parent class. All we do
            # here is specify what class to use for constructing Url
            # instances. We need to use a descendant of the Url class
            # for this purpose.
            #
            NCBITree.__init__(self,
                             _email,
                             _urlclass = _urlclass,
                             _maxLevel=_maxLevel,
                             _workingDir=_workingDir, 
                             _default_socket_timeout = _default_socket_timeout,
                             _sleeptime=_sleeptime,
                             _userAgent=_userAgent,
                             _netItemClass = _netItemClass,
                              _NCBIApi = NCBITree.NCBI_CO_AUTHOR_API)


                
        except Exception, e:
            self.SetLastError('in NCBICoAuthorTree.__init__: ' + str(e))

############################################################
####################   public APIs   #######################
############################################################

    def BuildUrlTree(self,startUrl,parentItemIdx=None,currentLevel=0,alreadyMassaged=False):
        """
        This is the "plain vanilla" version.
        
        Build the tree, starting from a given URL. Will be called recursively
        for child URLs to whatever level the UrlTree is constructed to handle.
        """
        log = Log('NCBICoAuthorTree.BuildUrlTree','url=' + str(startUrl) + '\nparent idx=' + str(parentItemIdx) + '\nlevel=' + str(currentLevel))
        currentItem = None
        currentUrl = None
        childUrl = None
        try:
            currentDomain = startUrl

            if not self.rootDomain:
                self.rootDomain = currentDomain
                
            (currentItem, currentIdx, isNewItem) = self.PutUrl(parentItemIdx,startUrl,currentLevel)
            
            if (not currentItem):
                return False
            if isNewItem:
                if not (currentLevel >= self.maxLevel):
                    return self.BuildUrlForest(Urls=currentItem.GetUrl().GetUrlAnchors(),
                                        level=currentLevel+1, parentIdx=currentIdx)
                else:
                    return True
            elif (currentItem.GetProperty('level')  >= self.maxLevel) and not (currentLevel >= self.maxLevel):
                currentItem.SetProperty('level',currentLevel)
                return self.BuildUrlForest(Urls=currentItem.GetUrl().GetUrlAnchors(),
                                    level=currentLevel+1, parentIdx=currentIdx)
            else:
                return True
        except Exception, e:
            self.SetLastError( str(e)\
                              + '\nstarting url: ' + startUrl \
                              + '\ncurrent url: ' + str(currentUrl)
                              + '\nchild url: ' + str(childUrl))
            return False


    def BuildUrlForest(self,Urls,level=0, parentBase=None, parentIdx=None):
        """
        Given a list of urls to be processed, build a tree by calling BuildUrlTree
        successively with each url in the list. In this case there is no root URL,
        unless this is called at some level other than the root.
        """
        self.ResetLastError()
        log = Log('NCBICoAuthorTree.BuildUrlForest')
        currentLevel = level
        rootIdx = parentIdx
        childUrl = None
        try:
            
            for childUrl in Urls:
                childItem = self.BuildUrlTree(startUrl=childUrl,parentItemIdx=rootIdx,
                                currentLevel=currentLevel,
                                alreadyMassaged=True)
                if not childItem:
                    log.Write( 'in NCBICoAuthorTree.BuildUrlForest, NCBICoAuthorTree.BuildUrlTree failed for childUrl: ' + str(childUrl) )
            return True
        except Exception, e:
            self.SetLastError( str(e) + '\ncurrent url: ' + str(childUrl))
            return False

############################################################
##################  helper functions  ######################
############################################################


    # network serializers 
    def WritePajekFile(self,netname,filename):
        ### PAJEK
        URLFILE = None
        log = Log('NCBICoAuthorTree.WritePajekFile',netname+':'+filename)
        try:
            URLFILE = open(filename + ".tmp","w")
            self.WritePajekStream(netname,URLFILE)

            URLFILE.close()
            """
            Pajek always requires DOS-like line endings
            """
            ConvertTextFile2DOS(filename + ".tmp",filename + ".paj")
            
        except Exception, e:
            self.SetLastError('In NCBICoAuthorTree.WritePajekFile: ' + str(e))
            if URLFILE:
                URLFILE.close()


def main():
    # dir to write to
    workingDir =urlutils.GetConfigValue('workingDir')
    log.logging=True
    myLog = Log('main')
    
    x = NCBICoAuthorTree(_maxLevel=2,
                       _email='dalehuns@umich.edu',
                       _workingDir=workingDir)
    x.BuildUrlTree('Hunscher DA')

    
    x.MapFunctionToUrlNetwork(PrintHierarchy,args=sys.stderr)
    x.WritePajekFile('HunscherDA_co_authors','HunscherDA_co_authors')
    x.WriteGuessFile('HunscherDA_co_authors_urls')            # url network


if __name__ == '__main__':
    main()
    sys.exit(0)
    