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
The TechnoratiTree class creates a network (actually two networks, one for URLs
and one for their domains) by generating a tree of Technorati API objects.
"""

import re
import string
import sys
import os
import urllib
import socket

from object import Object
from url import Url, DomainFromHostName
from urlparse import urlparse
from urlnetitem import UrlNetItem
from domainnetitem import DomainNetItem
from log import Log, logging, file_only
import log
from urltree import UrlTree
from technoraticosmosurl import TechnoratiCosmosUrl
from urlutils import *

# supported technorati apis
TECHNORATI_COSMOS_API = 1

# soon, but not yet...
TECHNORATI_TAG_API = 2
TECHNORATI_SEARCH_API = 3

     
###################################################################
###################################################################
###################################################################

class TechnoratiTree(UrlTree):
    """
    Class representing a tree of technorati URIs
    """
    
    def __init__(self,
                 _technoratiKey,
                 _technoratiApi = TECHNORATI_COSMOS_API,
                 _maxLevel = 2,
                 _singleDomain=False, 
                 _showLinksToOtherDomains=False,
                 _workingDir=None, 
                 _redirects = None,
                 _ignorableText = None,
                 _truncatableText = None,
                 _default_socket_timeout = 15,
                 _sleeptime = 2,
                 _userAgent=None,
                 _useHostNameForDomainName = True,
                 _netItemClass = UrlNetItem): # override UrlTree default to handle blogs
        try:
            log = Log('TechnoratiTree ctor')
            #
            # Most of the work is done by the parent class. All we do
            # here is specify what class to use for constructing Url
            # instances. We need to use a descendant of the Url class
            # for this purpose.
            #
            if _technoratiApi == TECHNORATI_COSMOS_API:
                UrlTree.__init__(self,
                                 _maxLevel,
                                 TechnoratiCosmosUrl,
                                 _singleDomain=False, 
                                 _showLinksToOtherDomains=False,
                                 _workingDir=_workingDir, 
                                 _redirects = _redirects,
                                 _ignorableText = _ignorableText,
                                 _truncatableText = _truncatableText,
                                 _default_socket_timeout = _default_socket_timeout,
                                 _sleeptime=_sleeptime,
                                 _userAgent=_userAgent,
                                 _useHostNameForDomainName = _useHostNameForDomainName,
                                 _netItemClass = _netItemClass)
            else:
                raise Exception, 'no Technorati API specified'

            # We need to make our technorati developer key available...
            tk = _technoratiKey
            if tk == None:
                tk = urlutils.GetConfigValue('technoratiKey')
                
            # remove quotes, in case urlnet coder thought they were necessary
            if (tk[0] == '"' and tk[-1] == '"') or (tk[0] == "'" and tk[-1] == "'"):
                tk = tk[1:-1]
            
            # save it to a property of the object    
            self.SetProperty('technoratiKey',tk)            

        except Exception, e:
            self.SetLastError('in __init__: ' + str(e))



def main():
    # dir to write to
    workingDir =urlutils.GetConfigValue('workingDir')
    log.logging=True
    myLog = Log('main')
    myTechnoratiKey = '13083c881893e0023f4a6f6e42d8c770'
    
    x = TechnoratiTree(_maxLevel=4,
                       _technoratiApi=TECHNORATI_COSMOS_API,
                       _workingDir=workingDir,
                       _technoratiKey=myTechnoratiKey,
                       _sleeptime=1)
    x.BuildUrlTree('http://hunscher.typepad.com/futurehit')

    #x = UrlTree(_maxLevel=3,_workingDir=workingDir)
    #x.BuildUrlForest('http://www.livejournal.com',urls)
    
    x.MapFunctionToUrlNetwork(PrintHierarchy,args=sys.stderr)
    x.MapFunctionToDomainNetwork(PrintHierarchy,args=sys.stderr)
    x.WritePajekFile('futurehit_cosmos','futurehit_cosmos')
    x.WriteGuessFile('futurehit_cosmos_urls')            # url network
    x.WriteGuessFile('futurehit_cosmos_domains',False)      #domain network


if __name__ == '__main__':
    main()
    sys.exit(0)
    
