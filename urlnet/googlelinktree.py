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
The GoogleLinkTree class creates a network (actually two networks, one for URLs
and one for their domains) by generating a tree of Google UrlNetItem instances.

It relies heavily on the SearchEngineTree class. Google-specific code is noted
below.
"""

import re
import string
import sys
import os

from object import Object
from urlnetitem import UrlNetItem
from log import Log, logging, file_only
import log
from googletree import GoogleTree
from regexqueryurl import RegexQueryUrl
from googlelinkurl import GoogleLinkUrl
from urlutils import *


     
###################################################################
###################################################################
###################################################################

class GoogleLinkTree(GoogleTree):
    """
    Class representing a tree of Google result set URLs where 'link:' will
    be used as a prefix to a target URL.
    """
    
    def __init__(self,
                 _maxLevel = 2,
                 _urlclass=RegexQueryUrl,
                 _singleDomain=False,
                 _resultLimit=10,
                 _showLinksToOtherDomains=False,
                 _workingDir=None, 
                 _redirects = None,
                 _ignorableText = None,
                 _truncatableText = None,
                 _default_socket_timeout = 15,
                 _sleeptime = 2,
                 _userAgent=None,
                 _netItemClass = UrlNetItem,
                 _useHostNameForDomainName = False,
                 _probabilityVector = None,
                 _probabilityVectorGenerator = None,
                 _probabilityDefault = 0.0001):
        try:
            log = Log('GoogleLinkTree ctor')
            #
            # Most of the work is done by the parent class. All we do
            # here is specify what class to use for constructing Url
            # instances. We need to use a descendant of the Url class
            # for this purpose.
            #
            
            if _sleeptime == None or _sleeptime < 2:
                log.Write('_sleeptime must be >= 2 for GoogleLinkTree class, setting to 2.')
                _sleeptime = 2
            
            GoogleTree.__init__(self,
                            _maxLevel=_maxLevel,
                            _singleDomain=_singleDomain, 
                            _urlclass=_urlclass,
                            _resultLimit=_resultLimit,
                            _showLinksToOtherDomains=_showLinksToOtherDomains,
                            _workingDir=_workingDir, 
                            _redirects=_redirects,
                            _ignorableText=_ignorableText,
                            _truncatableText=_truncatableText,
                            _default_socket_timeout=_default_socket_timeout,
                            _sleeptime=_sleeptime,
                            _userAgent=_userAgent,
                            _netItemClass=_netItemClass,
                            _useHostNameForDomainName=_useHostNameForDomainName,
                            _probabilityVector=_probabilityVector,
                            _probabilityVectorGenerator=_probabilityVectorGenerator,
                            _probabilityDefault=_probabilityDefault)

            # GoogleTree will have set this property to Url: we must set
            # it back toRegexQueryUrl so we can format queries to retrieve
            # inbound links
            self.SetProperty('nextUrlClass',GoogleLinkUrl)
            
            # link networks must reverse direction of arcs/edges
            self.SetProperty('reverseArcOrEdgeDirection',True)

            # Google-specific regex patterns
            self.SetProperty('regexPattern',\
                ['<h3 class=r><a href=\"(.*?)\"',
                 '<p><a href=\"(.*?)\"',
                ]
                )
        
        except Exception, e:
            self.SetLastError('in GoogleLinkTree.__init__: ' + str(e))

    def FormatSEQuery(self,freeTextQuery):
        """
        This function is Google-specific.
        """
        log = Log('GoogleLinkTree.FormatSEQuery',freeTextQuery)
        numResults = self.GetProperty('numSearchEngineResults')
        if (not numResults):
            numResults = 10
        if str(numResults) not in ('10','20','30','40','50','100'):
            raise Exception, \
                  'Exception in GoogleLinkTree.FormatSEQuery: ' \
                  + "numSearchEngineResults property must be one of '10',\
                 '20','30','40','50', or '100'"
        prefix = 'http://www.google.com/search?hl=en&'
        
        # make sure freeTextQuery is of the form 
        #    'link:someurlwithoutschemeprefix'
        
        '''    
        if '://' in freeTextQuery:
            freeTextQuery = freeTextQuery[freeTextQuery.index('://')+3:]

        if freeTextQuery[0:5] != 'link:':
            freeTextQuery = 'link:' + freeTextQuery
        '''    
        query=urlencode({'num' : numResults, 'as_lq': freeTextQuery, \
                             'btnG': 'Search' })
        query = prefix + query 

        log.Write('query=%s' % query)
        
        return query
            
    
    def BuildUrlTree(self,startUrl,parentItemIdx=None,currentLevel=None,alreadyMassaged=False):
        #Override parent class in order to format the query.
        log = Log('GoogleLinkTree.BuildUrlTree','startUrl=' + str(startUrl) + '\nparent idx=' + str(parentItemIdx) + '\nlevel=' + str(currentLevel))
        try:
            if currentLevel == None:
                currentLevel = 0
            putRoot = False
            if currentLevel == 0 and self.masterItemIdx == 0:
                putRoot = True
                self.currentRun = 1
            elif currentLevel == 0:
                self.currentRun += 1
            if currentLevel == 0: # added for debugging
                pass
            (queryURL,url,Urls) = self.GetSEResultSet(query=startUrl,putRoot=putRoot)
            getTitles = self.GetProperty('getTitles')
            if putRoot:
                currentIdx = 1
                currentItem = self.GetUrlNetItemByIndex(currentIdx)
                isNewItem = True
            (currentItem, currentIdx, isNewItem) = self.PutUrl(parentItemIdx,startUrl,currentLevel)
            if (not currentItem):
                return False
            if isNewItem and not (currentLevel >= self.maxLevel):
                return self.BuildUrlForest(Urls,
                                    level=currentLevel+1,parentBase=startUrl,
                                           parentIdx=currentIdx)
            elif isNewItem and getTitles:
                # get title only; don't need to do it as a separate action if recursing,
                # because it will be a side effect of getting the child URLs
                self.SetItemTitleProperty(currentItem)
                return True
            else:
                return True
        except Exception, e:
            raise Exception, 'in GoogleLinkTree.BuildUrlTree: ' + str(e)
    
    
    def BuildUrlTreeWithPlaceholderRoot(self,rootPlaceholder,query):
        """
        This function is not applicable to link networks.
        """
        raise Exception, 'in GoogleLinkTree.BuildUrlTreeWithPlaceholderRoot: Function not implemented for this class'


    def BuildUrlForestWithPhantomRoot(self,query):
        """
        This function is not applicable to link networks.
        """
        raise Exception, 'in GoogleLinkTree.BuildUrlTreeWithPlaceholderRoot: Function not implemented for this class'



        
def main():
    # dir to write to
    timestamp = strftime('%Y-%m-%d--%H-%M-%S',localtime())
    baseDir = GetConfigValue('workingDir')
    #baseDir = urlutils.GetConfigValue('workingDir')
    workingDir = os.path.join(baseDir,timestamp)
    oldDir = os.getcwd()
    
    myLog = None

    try:
        try:
            os.mkdir(baseDir)
        except Exception, e:
            pass #TODO: make sure it's because the dir already exists
        try:
            os.mkdir(workingDir)
        except Exception, e:
            pass #TODO: make sure it's because the dir already exists
        os.chdir(workingDir)
        myLog = Log('main')
        log.logging=True
        #log.trace=True
        log.altfd=open('GoogleLinkTree.log','w')
    except Exception,e:
        myLog.Write(str(e)+'\n')
        goAhead = False

    
    x = GoogleLinkTree(_maxLevel=2,
                    _workingDir=workingDir,
                    _resultLimit=20)
                    
    if False:
        (queryURL,url,Urls) = x.GetSEResultSet('http://compoundthinking.com/blog/')
        print queryURL
        print Urls

    if True:
        x.BuildUrlTree('http://ehealth.johnwsharp.com/')

        x.WritePajekFile('GoogleLinkTree-linktree','GoogleLinkTree-linktree')
        x.WriteGuessFile('GoogleLinkTree-linktree_urls')            # url network
        x.WriteGuessFile('GoogleLinkTree-linktree_domains',False)      #domain network
    
    # tidy up
    if log.altfd:
        log.altfd.close()
        log.altfd = None
        
    os.chdir(oldDir)

if __name__ == '__main__':
    main()
    sys.exit(0)
    
