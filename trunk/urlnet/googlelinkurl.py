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

import re
import string
import sys
import os

from regexqueryurl import RegexQueryUrl
from urllib import urlopen, urlencode, unquote_plus
from urlparse import *
from url import Url
from log import Log, logging
import log

#################### the GoogleLinkUrl class ######################
class GoogleLinkUrl(RegexQueryUrl):
    """ A class to parse retrieved documents using Python regular expressions. It
        It is optimized for use with search engines, which is why regex-related things
        are passed as properties rather than arguments. The top-level search
        engine URL is parsed to get the result set URLs using this class, and
        the result URLs are treated as garden-variety URLs by default.
        The nextUrlClass property, if present, provides the class to use for
        instantiation of Url-derived instances to follow in the network generation process,
        and if not present, the base Url class itself will be used.

        The regular expression to be used in scanning the retrieved document for URL anchors is
        passed in the regexPattern property, which can be either a list of regular expression strings or
        a single string. The optional findall_args property is the flags to use in the call to
        re.findall().
    """
    
    def __init__(self, _inboundUrl, _network=None, limit=20, start=1):
        """
        Get errors occurring in constructor by calling lastError().
        """
        
        # Don't allow a GetPage call in the Url ctor - set
        # _doInit to False automatically, so we can retrieve
        # the anchors using regular expressions on the fly.
        
        myLog = Log('GoogleLinkUrl ctor',_inboundUrl)
        RegexQueryUrl.__init__(self,_inboundUrl,_network=_network,limit=limit,start=start)

        self.nextUrlClass = self.network.GetProperty('nextUrlClass')
        if not self.nextUrlClass:
            self.nextUrlClass = GoogleLinkUrl
            
    def GetAnchorList(self):
        """
        Overriding the same function in the Url class.
        """
        myLog = Log('GetAnchorList')
        #print "00"
        if self.url == None:
            #print "01"
            return []
        elif self.anchors != None:
            #print "02"
            return self.anchors
        else:
            #print "03"
            try:
                # parse to get the href
                #
                page = self.GetPage()
                self.anchors = []
                if page is None or len(page) == 0:
                    return []
                ptype = str(type(self.regexPattern)).lower()
                if 'str' in ptype:
                    regexExprs = [self.regexPattern,]
                elif ('list' in ptype) or ('tuple' in ptype): # already a list or other tuple type
                    regexExprs = self.regexPattern
                else:
                    raise Exception, 'unsupported regex pattern type "' + ptype + '" in GoogleLinkUrl.GetAnchorList()'
                items = [page,]
                for regexPattern in regexExprs:
                    results = []
                    for item in items:
                        if self.findall_args:
                            results = results + re.findall(regexPattern,item,self.findall_args)
                        else:
                            results = results + re.findall(regexPattern,item)
                    self.anchors += results

                for i in range(0,len(self.anchors)):
                    self.anchors[i] = self.anchors[i].strip()
                    
                self.network.urlclass = self.nextUrlClass

                
                i = 0
                for url in self.anchors:
                    url = url.split('#')[0]
                    url2 = self.network.MassageUrl(url,-1)
                    if url2:
                        self.anchors[i] = url2
                    else:
                        myLog.Write('top level url "' + url + '" rejected by MassageUrl')
                    i = i + 1
                    
                if self.network.topLevelUrls == None:
                    self.network.topLevelUrls = self.anchors
                    
                return self.anchors
                    
            except Exception, inst:
                self.SetLastError( 'GoogleLinkUrl.GetAnchorList' + ": " + str(type(inst)) + '\n' + self.url )
                return []


if __name__ == '__main__':
    pass # unit test specific to this module needed!
