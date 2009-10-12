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
The BingTree class creates a network (actually two networks, one for URLs
and one for their domains) by generating a tree of Bing UrlNetItem instances.

It relies heavily on the SearchEngineTree class. Bing-specific code is noted
below.

TODO: add probabilities to the test...
"""

import re
import string
import sys
import os
import urllib
import socket
from time import strftime, localtime

from object import Object
from url import Url
from urlparse import urlparse
from urlnetitem import UrlNetItem
from domainnetitem import DomainNetItem
from log import Log, logging, file_only
import log
from searchenginetree import SearchEngineTree
from regexqueryurl import RegexQueryUrl
from urlutils import *
from searchenginetree import computeDescendingStraightLineProbabilityVector,\
                                    computeEqualProbabilityVector
from clickprobabilities import probabilityByPositionStopSmokingClicks


     
###################################################################
###################################################################
###################################################################

class BingTree(SearchEngineTree):
    """
    Class representing a tree of Bing result set URLs
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
                 _sleeptime = 0,
                 _userAgent=None,
                 _netItemClass = UrlNetItem,
                 _useHostNameForDomainName = False,
                 _probabilityVector = None,
                 _probabilityVectorGenerator = None,
                 _probabilityDefault = 0.0001):
        try:
            log = Log('BingTree ctor')
            #
            # Most of the work is done by the parent class. All we do
            # here is specify what class to use for constructing Url
            # instances. We need to use a descendant of the Url class
            # for this purpose.
            #
            SearchEngineTree.__init__(self,
                            _maxLevel=_maxLevel,
                            _singleDomain=False, 
                            _urlclass=_urlclass,
                            _resultLimit=_resultLimit,
                            _showLinksToOtherDomains=False,
                            _workingDir=_workingDir, 
                            _redirects = _redirects,
                            _ignorableText = _ignorableText,
                            _truncatableText = _truncatableText,
                            _default_socket_timeout = _default_socket_timeout,
                            _sleeptime=_sleeptime,
                            _userAgent=_userAgent,
                            _netItemClass = _netItemClass,
                            _useHostNameForDomainName = _useHostNameForDomainName,
                            _probabilityVector = _probabilityVector,
                            _probabilityVectorGenerator = _probabilityVectorGenerator,
                            _probabilityDefault = _probabilityDefault)

            # set necessary properties for use in Url-derived class
            # number of results to fetch - must be 10,20,30,50, or 100
            # default is 10 results.
            self.SetProperty('numSearchEngineResults',_resultLimit)

            # Url-derived class to use for all but the Bing query Url.
            # If the property is not set, the default Url class will be used.
            self.SetProperty('nextUrlClass',Url)
            # Bing-specific regex pattern
            self.SetProperty('regexPattern','class="sb_tlst"><h3><a href=\"(.*?)\"')
            self.SetProperty('findall_args',re.S)
        
        except Exception, e:
            self.SetLastError('in BingTree.__init__: ' + str(e))


    def FormatSEQuery(self,freeTextQuery,args=None):
        """
        This function is Bing-specific.
        """
        log = Log('BingTree.FormatSEQuery',freeTextQuery)
        if args:
            numResults = int(args)
        else:
            numResults = self.GetProperty('numSearchEngineResults')
        if (not numResults):
            numResults = 10
        if str(numResults) not in ('10','20',):
            raise Exception, \
                  'Exception in BingTree.FormatSEQuery: ' \
                  + "numSearchEngineResults property must be one of '10' or '20'"
        prefix = 'http://search.bing.com/search?'
        query=urlencode({ 'q': freeTextQuery, })
        query = prefix + query

        # create a name we can use for writing a file with the result set URLs later,
        # and set the 'SEQueryFileName' property with the generated filename
        self.SetFilenameFromQuery(freeTextQuery)

        return query


def main():

    # uncomment one of the vectorGenerator assignments below
    
    # vectorGenerator = computeEqualProbabilityVector
    vectorGenerator = computeDescendingStraightLineProbabilityVector
    
    # dir to write to
    timestamp = strftime('%Y-%m-%d--%H-%M-%S',localtime())
    baseDir = urlutils.GetConfigValue('workingDir')
    #baseDir = urlutils.GetConfigValue('workingDir')
    workingDir = baseDir+timestamp
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
        log.altfd=open('aoltree.log','w')
    except Exception,e:
        myLog.Write(str(e)+'\n')
        goAhead = False

    
    x = BingTree(_maxLevel=1,
                    _workingDir=workingDir,
                    _resultLimit=20,
                    _probabilityVector = probabilityByPositionStopSmokingClicks,
                    _probabilityVectorGenerator = vectorGenerator)
    ##(queryURL,url,Urls) = x.GetSEResultSet('quit smoking')
    
    x.BuildUrlForestWithPhantomRoot('quit smoking')

    x.MapFunctionToUrlNetwork(PrintHierarchy,args=sys.stderr)
    x.MapFunctionToDomainNetwork(PrintHierarchy,args=sys.stderr)
    x.WritePajekFile('aoltree-quitsmoking','aoltree-quitsmoking')
    x.WriteGuessFile('aoltree-quitsmoking_urls')            # url network
    x.WriteGuessFile('aoltree-quitsmoking_domains',False)      #domain network
    
    # tidy up
    if log.altfd:
        log.altfd.close()
        log.altfd = None
        
    os.chdir(oldDir)

if __name__ == '__main__':
    main()
    sys.exit(0)
    