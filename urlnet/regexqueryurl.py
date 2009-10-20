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

from urllib import urlopen, urlencode, unquote_plus
from urlparse import *
from url import Url
from log import Log, logging
import log

#################### the RegexQueryUrl class ######################
class RegexQueryUrl(Url):
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

    regexPattern = None
    nextUrlClass = None
    findall_args = None
    
    def __init__(self, _inboundUrl, _network=None, limit=20, start=1):
        """
        Get errors occurring in constructor by calling lastError().
        """
        
        # Don't allow a GetPage call in the Url ctor - set
        # _doInit to False automatically, so we can retrieve
        # the anchors using regular expressions on the fly.
        
        myLog = Log('RegexQueryUrl ctor',_inboundUrl)
        Url.__init__(self,_inboundUrl,_network=_network,_doInit=False)

        # this property is required.
        self.regexPattern = self.network.GetProperty('regexPattern')
        if not self.regexPattern:
            raise Exception, 'RegexQueryUrl ctor: regular expression property not found'
        
        # the next two properties are optional.
        self.findall_args = self.network.GetProperty('findall_args')
        
        self.nextUrlClass = self.network.GetProperty('nextUrlClass')
        if not self.nextUrlClass:
            self.nextUrlClass = Url
            
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
                
                filename = self.network.GetProperty('SEQueryFileName')
                if filename:
                    fd = open(filename + '.html','w')
                    fd.write('%s\n' % page)
                    fd.close()

                self.anchors = []
                ptype = str(type(self.regexPattern)).lower()
                if 'str' in ptype:
                    regexExprs = [self.regexPattern,]
                elif ('list' in ptype) or ('tuple' in ptype): # already a list or other tuple type
                    regexExprs = self.regexPattern
                else:
                    raise Exception, 'unsupported regex pattern type "' + ptype + '" in RegexQueryUrl.GetAnchorList()'
                items = [page,]
                """
                The following code can handle the simple case of applying one regex pattern to the starting page,
                or multiple regex expressions to the starting page; it can also handle the most complex case,
                where the set of regex expressions is used to derive one or more text chunks, each of which is
                then processed using the remaining regex expressions in the list, allowing the caller to apply
                successively more specific regex expressions to the text.
                """
                for regexPattern in regexExprs:
                    results = []
                    for item in items:
                        if self.findall_args:
                            results = results + re.findall(regexPattern,item,self.findall_args)
                        else:
                            results = results + re.findall(regexPattern,item)
                    # only replace items with results if results list is not empty
                    if len(results) > 0:
                        # apply regex patterns to set derived from the list we just obtained
                        items = results
                        
                """
                We may have got more than we needed; see if we need to filter. 
                If we are filtering, we most likely retrieved more than we needed.
                If so, limit the results returned to the number specified as
                the desired limit in the network constructor.
                """
                filtering = self.network.GetProperty('filterToKeep')
                if filtering:
                    numResults = self.network.GetProperty('numSearchEngineResults')
                    
                    newItems = []
                    count = 0
                    for item in items:
                        if self.network.IgnoreFilteredUrl(item):
                            pass
                        else:
                            newItems.append(item)
                            count = count + 1
                            if count == numResults:
                                break
                    items = newItems
                    
                self.anchors = items

                for i in range(0,len(self.anchors)):
                    self.anchors[i] = self.anchors[i].strip()
                    
                self.network.urlclass = self.nextUrlClass

                # leave behind a list of the urls retrieved
                if filename:
                    try:
                        fd = open(filename + '.txt','w')
                        i = 1
                        for anchor in self.anchors:
                            fd.write(str(i) + '\t' + anchor + '\n')
                            i = i + 1
                        fd.close()
                    except Exception, inst:
                        self.SetLastError( 'RegexQueryUrl.GetAnchorList' + ' while trying to write to ' + filename + ': ' + str(type(inst)) + '\n' + self.url )

                # get rid of markup embedded in urls by search engines
                i = 0
                for url in self.anchors:
                    #print i+1
                    #print url
                    in_markup = False
                    url_without_markup = ''
                    for c in url:
                        if in_markup:
                            if c == '>':
                                in_markup = False
                        elif c == '<':
                            in_markup = True
                        else:
                            url_without_markup = url_without_markup + c
                    #print url_without_markup
                    url_without_markup = unquote_plus(url_without_markup)
                    #print url_without_markup
                    url_without_markup = re.sub('&amp;','&',url_without_markup)
                    #print url_without_markup
                    

                    # handle the case of URLs that begin with a reference to the host root
                    # (e.g., /cgi-bin/processor.pl?spam=3&eggs=2)
                    
                    if '://' not in url_without_markup:
                        parts = urlparse(self.url)
                        if url_without_markup[0] == '/':
                            if self.network.rootDomain == None:
                                url_without_markup = parts.hostname + url_without_markup
                        url_without_markup = parts.scheme + '://' + url_without_markup
                    self.anchors[i] = url_without_markup
                    #print urls[i]
                    i = i + 1
                    
                i = 0
                for url in self.anchors:
                    # get rid of in-page links
                    url = url.split('#')[0]
                    url2 = self.network.MassageUrl(url,-1)
                    if url2:
                        self.anchors[i] = url2
                    else:
                        myLog.Write('top level url "' + url + '" rejected by MassageUrl')
                    i = i + 1
                    
                if self.network.topLevelUrls == [] or self.GetProperty('isRootUrl') != None:
                    self.network.topLevelUrls.append(self.anchors)
                    
                return self.anchors
                    
            except Exception, inst:
                self.SetLastError( 'RegexQueryUrl.GetAnchorList' + ": " + str(type(inst)) + '\n' + self.url )
                return []

        
    def getPage(self):
        # just in case...
        self.thePage = None
        page = getPage(self)
        # don't allow page cacheing on regex queries.
        self.thePage = None
        return page
        


if __name__ == '__main__':
    pass # unit test specific to this module needed!
