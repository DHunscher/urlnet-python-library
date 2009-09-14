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
The UrlTree class creates a network (actually two networks, one for URLs
and one for their domains) by following links from a set of URLs.
"""

import re
import string
import sys
import os
import urllib
import socket
from time import strftime, localtime

from object import Object
from url import Url, DomainFromHostName
from urlparse import urlparse, urljoin, urldefrag, urlunparse
from urlnetitem import UrlNetItem
from domainnetitem import DomainNetItem
from log import Log
from urlutils import * 

###################################################################
###################################################################
###################################################################

# version of this library
lib_version = '1.0'

class UrlTree(Object):
    """
    Class representing a tree of URIs
    """
    #master item index sequence (highest index so far)
    masterItemIdx = 0
    #dict by index:
    UrlNetItemByIndex = {}
    #dict by url hash:
     #returns (index)
    IndexByUrl = {}

    #master domain index sequence (highest index so far)
    masterDomainIdx = 0
    #dict by index:
    DomainByIndex = {}
    #dict by domain hash:
     #returns (index)
    IndexByDomain = {}

    # how deep do we search?
    maxLevel = 1
    # what Url class do we use?
    urlclass = None
    # do we restrict ourselves to a single domain, or pursue offsite links as
    # depth permits?
    singleDomain = False
    # if working with a single domain, do we show first-order offsite links without
    # pursuing them?
    showLinksToOtherDomains = False
    # what is the domain of the root URL?
    rootDomain = None
    rootScheme = None
    rootHost = None

    # if a url contains text from this list (if a list is provided),
    # ignore the url
    ignorableText = None

    IGNORABLE_MEDIA_TYPES = ('.avi','.mov','.mp3','.wav','.wmv','.jpg',\
                             '.jpeg','.gif','.png','.rss','.rdf','.tif',\
                             '.tiff','.swf',)
    
    """
    sometimes links are embedded in redirect urls...
    
    e.g., when the child url begines with 'http://www.google.com/url?',
    the actual child url will be found in the urlencoded-style 'url'
    parameter, e.g.

    http://www.google.com/url?sa=t&ct=res&cd=1&url=http%3A%2F%2Fen.wikipedia.org%2Fwiki%2FCanada&ei=txqVR... (etc.)

    This will typically apply on only one level, and typically only
    when BuildUrlTree is being used. In BuildUrlForest, the embedded
    links will normally have already been translated out for (or by) you.
    
    a valid redirects list that would handle this case would be:

    redirects = ('www.google.com/url?','url',1)

    redirects contains a sequence of sequences, the inner sequences being
    triplets of values, the first being a URL fragment to search for, the
    second value being the parameter containing the actual url if the
    encountered url matches the first value, and the third the level on
    which to perform the restrict. The urls to be massaged are this level's
    child urls
    
    The UrlTree class cycles through the pairs in redirects, and when a url
    beginning with redirects[i][0] is found at level redirects[i][2], the url 
    parameter named redirects[i][1] contains the url to use as the child.
    In the above example, if the url shown above is encountered,
    redirects[0][0] is 'www.google.com/url?', so a match exists, and
    redirects[0][1] is 'url', so the encountered url is parsed and its
    'url' parameter contains the value of the *real* url(in this case
    'http://en.wikipedia.org/wiki/Canada')
    """
    
    redirects = None
    
    # internal flags

    isPhantomRoot=False
    isPlaceholderRoot=False
    

    truncatableText = None
    
    netitemclass = None

    PAJEK_NULL_PARTITION = 9999998
    
    def __init__(self,
                 _maxLevel = 2,
                 _urlclass=Url,
                 _singleDomain=False, 
                 _showLinksToOtherDomains=False,
                 _workingDir=None, 
                 _redirects = None,
                 _ignorableText = None,
                 _truncatableText = None,
                 _default_socket_timeout = None,
                 _sleeptime = None,
                 _userAgent = None,
                 _useHostNameForDomainName = False,
                 _netItemClass = UrlNetItem): 
        global lib_version
        try:
            log = Log('UrlTree ctor')
            Object.__init__(self)

            if _workingDir:
                os.chdir(_workingDir)
            else:
                _workingDir = GetConfigValue('workingDir')
                if _workingDir:
                    os.chdir(_workingDir)
                
            self.urlclass = _urlclass
            self.netitemclass = _netItemClass
            
            self.maxLevel = _maxLevel # defaults to root and one layer down
            
            #master item index sequence (highest index so far)
            self.masterItemIdx = 0

            """
            should we restrict to the first domain encountered?
            i.e., build a site map? If so, should we show (but not
            follow) links to domains other than the first domain?
            """
            self.singleDomain = _singleDomain
            self.showLinksToOtherDomains = _showLinksToOtherDomains
            # we need this for site maps
            self.rawRootUrl = None

            """
            Dictionaries by which we keep track of the urls we encounter.
            """
            #dict by index:
            # given an index, returns our linking data structure
            self.UrlNetItemByIndex = {}
            
            #dict by url hash:
             # given a url, returns (index)
            self.IndexByUrl = {}

            #master domain index sequence (highest index so far)
            self.masterDomainIdx = 0

            """
            Dictionaries by which we keep track of the domains
            we encounter
            """
            #dict by index:
            self.DomainByIndex = {}
            #dict by domain hash:
            #returns (index)
            self.IndexByDomain = {}

            self.rootDomain = None
            self.rootScheme = None
            self.rootHost = None
            self.redirects = _redirects
            self.ignorableText = _ignorableText
            self.truncatableText = _truncatableText
            self.rawRootUrl = None
            
            if _default_socket_timeout == None:
                _default_socket_timeout = GetConfigValue('default_socket_timeout')
            if _default_socket_timeout == None:
                _default_socket_timeout = 15
            socket.setdefaulttimeout(float(_default_socket_timeout))
    
            #
            # set time for sleep between url opens
            #
            if _sleeptime == None:
                _sleeptime = GetConfigValue('sleeptime')
            if _sleeptime == None:
                _sleeptime = 0
            self.SetProperty('sleeptime',_sleeptime)
            
            #
            # set name of user-agent to use in urlopens
            #
            if _userAgent:
                self.SetProperty('user-agent',_userAgent)
            else:
                userAgent = GetConfigValue('userAgent')
                if userAgent == None:
                    userAgent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT; ' + 'UrlTree v' + lib_version + ')'
                self.SetProperty('user-agent',userAgent)

            self.isPhantomRoot=False
            self.isPlaceHolderRoot=False

            self.useHostNameForDomainName = _useHostNameForDomainName

            timestamp = strftime('%Y-%m-%d--%H-%M-%S',localtime())
            self.SetProperty('timestamp',timestamp)
            
            self.urlsToFlag = None
            self.FlaggedUrlPartitionName = None
        except Exception, e:
            self.SetLastError('in UrlTree.__init__: ' + str(e))
            raise

############################################################
####################   public APIs   #######################
############################################################

    def BuildUrlTree(self,startUrl,parentItemIdx=None,currentLevel=0,alreadyMassaged=False):
        """
        This is the "plain vanilla" version.
        
        Build the tree, starting from a given URL. Will be called recursively
        for child URLs to whatever level the UrlTree is constructed to handle.
        """
        log = Log('vanilla BuildUrlTree','url=' + str(startUrl) + '\nparent idx=' + str(parentItemIdx) + '\nlevel=' + str(currentLevel))
        currentItem = None
        currentUrl = None
        childUrl = None
        try:
            url = startUrl
            if not alreadyMassaged:
                url = self.MassageUrl(startUrl,currentLevel)
                if not url:
                    log.Write('url '+str(startUrl)+' rejected by MassageUrl.')
                    return False
            parts = urlparse(url)
            currentDomain = DomainFromHostName(parts.hostname)
            if self.rawRootUrl == None:
                self.rawRootUrl = startUrl

            if not self.rootDomain:
                self.rootDomain = currentDomain
                self.rootScheme = parts.scheme
                self.rootHost = parts.hostname
                pathPart = self.ParsePathParts(parts.path)
                
            elif self.singleDomain and (self.rootDomain != currentDomain) and not self.showLinksToOtherDomains:
                # don't process if we are building a single-domain tree and we have an outlink to another domain
                return True # not really an error
            
            (currentItem, currentIdx, isNewItem) = self.PutUrl(parentItemIdx,url,currentLevel)
            getTitles = self.GetProperty('getTitles')
            if (not currentItem):
                return False
            if (self.singleDomain and self.showLinksToOtherDomains and (self.rootDomain != currentDomain)):
                if isNewItem and getTitles:
                    # set title for output later
                    self.SetItemTitleProperty(currentItem)
                return True 
            if self.truncatableText:
                for text in self.truncatableText:
                    if text in url:
                        # truncate tree traversal here. We put the url in the tree, but it's
                        #   not one we want to follow.
                        if isNewItem:
                            # get title only; don't need to do it as a separate action if recursing,
                            # because it will be a side effect of getting the child URLs
                            self.SetItemTitleProperty(currentItem)
                        return True
            # recurse for each child if we have an item, it hasn't been processed already, we
            # are not already at the maximum depth, and the current item not a fake placeholder root.
            # 
            # truncate MP3's and such; they have no children anyway
            if url.lower().endswith(self.IGNORABLE_MEDIA_TYPES):
                return True
            
            #print 'urlprefix', urlprefix
            if isNewItem and not (currentLevel >= self.maxLevel):
                return self.BuildUrlForest(Urls=currentItem.GetUrl().GetUrlAnchors(),
                                    level=currentLevel+1,parentBase=url, parentIdx=currentIdx)
            elif isNewItem and getTitles:
                # get title only; don't need to do it as a separate action if recursing,
                # because it will be a side effect of getting the child URLs
                self.SetItemTitleProperty(currentItem)
                return True
            else:
                return True
        except Exception, e:
            self.SetLastError('in vanilla BuildUrlTree: ' + str(e)\
                              + '\nstarting url: ' + startUrl \
                              + '\ncurrent url: ' + str(currentUrl)
                              + '\nchild url: ' + str(childUrl))
            return False


    def BuildUrlTreeWithPlaceholderRoot(self,rootPlaceholder,Urls):
        """
        Given a root URL that is to be used as a placeholder and not itself
        processed recursively, along with a list of urls to be processed,
        build a tree by calling BuildUrlTree successively with each
        url in the list. The placeholder URL must be a real URL, even
        though it will not be recursively processed. This is useful,
        for example, in situations where you have a list of URLs from a 
        search engine data set, and want to show the relationship between
        the URLs and the search engine. If any or all of the listed URLs 
        are relative URLs, the scheme and hostname of the placeholder root
        will be used to construct the full-fledged URL.
        """
        self.ResetLastError()
        log = Log('BuildUrlTreeWithPlaceholderRoot', rootPlaceholder)
        currentUrl = rootPlaceholder
        if '://' not in currentUrl:
            currentUrl = 'http://' + currentUrl
        self.isPlaceholderRoot=True
        if self.rawRootUrl == None:
            self.rawRootUrl = rootPlaceholder
        
        currentLevel = 0
        rootIdx = None
        try:
            currentUrl = self.MassageUrl(currentUrl,currentLevel)
            if not currentUrl:
                log.Write('url '+str(rootPlaceholder)+' rejected by MassageUrl.')
                return False
            (root,rootIdx,pathPart) = self.PutRootUrl(rootPlaceholder)
            myPrefix = self.rootScheme + '://' + self.rootHost + pathPart
            for url in Urls:
                currentUrl = url
                if '://' not in currentUrl:
                    currentUrl = 'http://' + currentUrl
                success = self.BuildUrlTree(startUrl=currentUrl,parentItemIdx=rootIdx,currentLevel=1)
                if not success:
                    log.Write( 'BuildUrlTree failed for childUrl: ' + str(currentUrl) )
            return True
        except Exception, e:
            self.SetLastError('in BuildUrlTree with placeholder: ' + str(e)\
                              + '\nstarting url: ' + rootPlaceholder \
                              + '\ncurrent url: ' + str(currentUrl))
            return False
        
    def BuildUrlForestWithPhantomRoot(self,phantomRoot):
        """
        Given a root URL that is to be processed recursively but not included
        in the network itself, build a tree by calling BuildUrlTree
        successively with each url in the "phantom" URL's anchor list.
        The phantom URL could, for example, be a search engine result page,
        but you want the network to have only the results and not the
        search engine page itself. 
        """
        self.ResetLastError()
        log = Log('BuildUrlForestWithPhantomRoot', phantomRoot)
        try:
            self.isPhantomRoot=True
            if self.rawRootUrl == None:
                self.rawRootUrl = phantomRoot
            # pass -1 to ensure we don't match any redirect levels accidentally
            # sorry about the "magic number!"
            massagedRoot = self.MassageUrl(phantomRoot,-1) 
            if not massagedRoot:
                raise Exception, 'phantomRoot '+str(phantomRoot)+' rejected by MassageUrl'
            else:
                phantomRoot = massagedRoot
                parts = urlparse(phantomRoot)
                self.rootDomain = DomainFromHostName(parts.hostname)
                self.rootScheme = parts.scheme
                self.rootHost = parts.hostname
            url = self.urlclass(_inboundUrl=phantomRoot, _network=self, _doInit=False)
            anchorlist = url.GetAnchorList()
            if len(anchorlist) == 0:
                return True # no outlinks is OK
            url = None # free up memory

            successful = self.BuildUrlForest(Urls=anchorlist,parentBase=massagedRoot,level=0)
            if not successful:
                log.Write( 'BuildUrlForest may have failed for url: ' + str(phantomRoot) )
            return True
        except Exception, e:
            self.SetLastError('in BuildUrlForestWithPhantomRoot: ' + str(e)\
                              + '\nstarting url: ' + phantomRoot 
                              )
            return False
        
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
                parts = urlparse(childUrl)
                # ignore schemes we don't handle, like telnet,
                # mailto, javascript, etc.
                if parts.scheme != '' and parts.scheme not in \
                   PERMISSIBLE_SCHEMES:
                    continue
                if parts.hostname == None and parentBase == None:
                    raise Exception, 'relative URL, no parentBase provided: '+str(childUrl)

                # ignore fragments
                if parts.hostname == None and parts.path == '':
                    continue
                
                if parts.hostname == None and parts.path != '':
                    childUrl = urljoin(parentBase,childUrl)
                    
                childUrl = self.MassageUrl(childUrl,level)
                if not childUrl:
                    continue
                
                #eliminate fragment references within parent base page
                frags = urldefrag(childUrl)
                if parentBase and (urlparse(frags[0]).geturl() == urlparse(parentBase).geturl()):
                    continue

                # if this is a site map, make sure we don't go any higher than the root
                #
                if self.singleDomain:
                    if self.rawRootUrl != None:
                        childBase = urlunparse(list(parts[0:3]) + ['','',''])
                        if '/' in childBase:
                            childBase = childBase[0:childBase.rindex('/')]
                        rootBase = urlunparse(list(urlparse(self.rawRootUrl)[0:3]) + ['','',''])
                        if '/' in rootBase:
                            rootBase = rootBase[0:rootBase.rindex('/')]
                        if rootBase.startswith(childBase) and childBase != rootBase:
                            continue

                
                childItem = self.BuildUrlTree(startUrl=childUrl,parentItemIdx=rootIdx,
                                currentLevel=currentLevel,
                                alreadyMassaged=True)
                if not childItem:
                    log.Write( 'in BuildUrlForest, BuildUrlTree failed for childUrl: ' + str(childUrl) )
            return True
        except Exception, e:
            self.SetLastError('in BuildUrlForest: ' + str(e)\
                              + '\ncurrent url: ' + str(childUrl))
            return False

############################################################
##################  helper functions  ######################
############################################################


    def AddListOfUrlsToFlag(self, urls, partitionName):
        '''
        Data structure being maintained here is a dict with the
        partitionName param as a key and the list of urls as the
        corresponding value.
        '''
        log = Log('AddListOfUrlsToFlag','urls=%s, parititionName=%s' % \
                (str(urls), str(partitionName) ) \
            )
        try:
            if self.urlsToFlag == None:
                self.urlsToFlag = {}
            # urls could be a file name or path
            if type(urls) is str:
                # should be a legitimate file path
                fd = open(urls)
                tmp = fd.readlines()
                fd.close()
                urls = []
                for line in tmp:
                    line = line.strip()
                    if len(line) > 0:
                        urls.append(line)
            self.urlsToFlag[partitionName] = urls
        except Exception, e:
            log.Write('in AddListOfUrlsToFlag( urls=%s, partitionName=%s ) %s' \
                % (str(urls), str(partitionName), str(e)))
            return
        

    def FlagUrlCheck(self,item,urlToAdd):
        '''
        This method can be used to create a partition in which URLs found in
        a caller-provided list are valued 1 and URLs not found in the list
        are valued zero.
        
        self.urlsToFlag is a dict consisting of lists of URLs indexed by
        partition names. For each such list, urlToAdd is checked to see if
        if it is present, in which case the value of its property named for
        the partition name will be set to 1, otherwise to zero.

        '''
        log = Log('FlagUrlCheck',urlToAdd)
        try:
            flagged = False
            if self.urlsToFlag == None:
                return
            if len(self.urlsToFlag.keys()) == 0:
                return
            urlToAdd = RemoveRealmPrefix(urlToAdd)
            for partition in self.urlsToFlag.keys():
                urls = self.urlsToFlag[partition]
                if urlToAdd in urls:
                    item.SetProperty(partition,1)
                else:
                    item.SetProperty(partition,0)
        except Exception, e:
            log.Write('in FlagUrlCheck( ' + str(urlToAdd) + ' ): ' + str(e))
            return
        
    def SetUrlTLDProperties(self,item,urlToAdd):
        """ If the program has set the TrackTLDProperties property to True,
            set the URL item's TLD properties. These include:
            
            urlTLD: the url's top-level domain.
            urlTLDVector: a value indicating (in the library author's
                arbitrary opinion) the relative value of this type of
                TLD.
            forProfitUrlTLD: True if url is probably for-profit, else set
                to False.
            """
        log = Log('SetUrlTLDProperties',urlToAdd)
        try:
            doTLDProps = self.GetProperty('TrackTLDProperties')
            if doTLDProps == None or doTLDProps == False:
                return
            tldConstants = self.GetUrlTLDConstants(urlToAdd)
            item.SetProperty('urlTLD',tldConstants[0])
            item.SetProperty('urlTLDVector',tldConstants[1])
            item.SetProperty('forProfitUrlTLD',
                self.IsForProfitUrlTLD(urlToAdd,returnBoolean = False))
        except Exception, e:
            log.Write('in SetUrlTLDProperties( ' + str(urlToAdd) + ' ): ' + str(e))
            return
        
    def GetUrlTLD(self,url):
        """ get the URL's type and return it in lowercase """
        log = Log('GetUrlTLD',url)
        
        try:
            '''
            First, the TLDExceptions property is checked to see if the
            caller has defined exceptions to the general rules for
            identifying the nature of top-level domains.
            
            TLDExceptions is used to correctly identify domains that attempt
            to pass themselves off as a different top-level domain type than
            that representing their proper categorization, e.g., a commercial
            entity representing itself as a dot-org.
            
            If set, the property value for TLDExceptions must be a dict in which
            the keys are fragments of URLs and the dict entry values are from
            the set of keys for the urlTypeconstants dictionary in 
            GetUrlTLDConstants. If the key is found in this particular url, 
            the dict entry value will be used as the tld string.
            
            For example, the dictionary
            
            d = { 'smoking-cessation.org': 'fake', 'whyquit.com' : 'org',}
            
            ...would ensure that the domain smoking-cessation.org is recognized
            as a commercial domain posing as a non-profit domain 
            rather than a true non-profit, and that whyquit.com (a labor-of-
            love site) is recognized as a nonprofit rather than a commercial 
            domain.
            
            The value 'fake' is used to identify for-profit sites masquerading
            as non-profit to allow their identification as such in network
            partitions. Conversely, the value 'okcom' is used to denote
            dot-coms that are essentially altruistic by nature.
            
            If there is no exception, the final token delimited by periods
            is used as the TLD string to be returned to the caller, except for 
            two-character TLD strings (country identifiers). For these,
            the second-last token delimited by periods is returned. This works
            in some cases, but there is no reliable algorithm for determining
            the profit status of international urls.
            '''
            TLDExceptions = self.GetProperty('TLDExceptions')
            if TLDExceptions != None:
                for e in TLDExceptions.keys():
                    if e.lower() in url.lower():
                        return TLDExceptions[e]

            # if we get here there is no exception
            urlType = urlparse(url)[1].split('.')
            if len(urlType[-1]) == 2:
                return  urlType[-2].lower()
            else:
                return urlType[-1].lower()
        except Exception, e:
            log.Write('in GetUrlTLD( ' + str(url) + ' ): ' + str(e))
            return '???'
        
        
    def IsForProfitUrlTLD(self,url,returnBoolean = True):
        """ By default, return True if the TLD applies to for-profit 
        entities (e.g.,  com and net), False if TLD applies to non-profit 
        or is unknown. If returnBoolean is False, return 1 for True and
        0 (zero) for False.
        """
        log = Log('IsForProfitUrlTLD',url)

        urlTypeForProfitConstants = {
            'com' : True,
            'co' : True,
            'tv' : True,
            'us' : True,
            'info' : True,
            'google' : True,
            'icio' : True,
            'org' : False,
            'or' : False,
            'net' : True,
            'ne' : True,
            'edu' : False,
            'ed' : False,
            'gov' : False,
            'go' : False,
            'nhs' : False,
            'gc' : False,
            'int' : False,
            'ad' : False,
            'mil' : False,
            'fake' : True,
            'okcom' : True,
            '???' : False,
            }
        try:
            isForProfit = urlTypeForProfitConstants[self.GetUrlTLD(url)]
            if returnBoolean:
                return isForProfit
            else: # caller wants an integer return value
                if isForProfit == True:
                    return 1
                else:
                    return 0
                
        except Exception, e:
            if returnBoolean:
                return True
            else:
                return 1

    def GetUrlTLDConstants(self,url):
        """ Return a sequence containing two values: an integer constant 
            representing the type of TLD in the URL, and a float constant
            for use in vectors, representing the library creator's rather
            arbitrary assessment of the relative value of the TLD type.
            Constants are defined in urlutils.py.
        """
        log = Log('GetUrlTLDConstant',url)
        # dictionary of constants for url types
        urlTypeConstants = {
            'com' : (DOTCOM,V_DOTCOM),
            'biz' : (DOTCOM,V_DOTCOM),
            'co' : (DOTCOM,V_DOTCOM),
            'icio' : (DOTCOM,V_DOTCOM),
            'us' : (DOTCOM,V_DOTCOM),
            'info' : (DOTCOM,V_DOTCOM),
            'google' : (DOTCOM,V_DOTCOM),
            'org' : (DOTORG,V_DOTORG),
            'or' : (DOTORG,V_DOTORG),
            'net' : (DOTNET,V_DOTNET),
            'ne' : (DOTNET,V_DOTNET),
            'edu' : (DOTEDU,V_DOTEDU),
            'ed' : (DOTEDU,V_DOTEDU),
            'gov' : (DOTGOV,V_DOTGOV),
            'go' : (DOTGOV,V_DOTGOV),
            'nhs' : (DOTGOV,V_DOTGOV), # UK's health system
            'gc' : (DOTGOV,V_DOTGOV), # Canadian government
            'int' : (DOTGOV,V_DOTGOV),
            'ad' : (DOTADM,V_DOTADM),
            'mil' : (DOTMIL,V_DOTMIL),
            'fake' : (DOTFAKE,V_DOTFAKE),
            'okcom' : (OKDOTCOM,V_OKDOTCOM),
            '???' : (DOTUNK,V_DOTUNK),
            }
        try:
            tld = self.GetUrlTLD(url)
            return urlTypeConstants[tld]
        except Exception, e:
            log.Write('%s in GetUrlTLDConstant: %s in %s' % (str(e), str(tld), str(url)) )
            return (DOTUNK,V_DOTUNK)
        
        
        
    def IgnoreFilteredUrl(self, url):
        log = Log('IgnoreFilteredUrl',url)    
        try:
            """
            # filter based on top-level domains (TLDs) or categories under country codes
            
            Return True if the url should be ignored, False otherwise.
            
            common TLDs and country codes are:
            com = company
            org = non-profit organization
            net = ISP
            gov = government
            mil = military
            edu = academic institution
            int = international organization
            
            categories under country codes are administered by the 
            country itself (if at all), so there is a lot of variation. some
            common categories are:
            co = company
            or = non-profit
            ac = academic institution
            go = government
            ad = network administration
            ne = ISP

            The property filterToKeep should contain two items:
            1. a list of strings representing the 
            TLD categories to keep, without any periods before or 
            after, in lower case. 
            2. a number indicating the
            maximum number of items in the result set requested.
            For example, to keep government, non-profit, and 
            academic, and get the first 10 matches out of 100,
            we would use:
            
            net.setProperty('filterToKeep', \
                    [['gov','go','org','or', 'edu','ac',], 100])
                    
            TLDs are generally reliable, though 'net' is often
            abused, and 'org' is sometimes abused.
            """
            
            filterlist = self.GetProperty('filterToKeep')
            if filterlist != None:
                try:
                    filterlist = filterlist[0]
                    urlType = self.GetUrlTLD(url)
                    if urlType == 'com':
                        pass
                    # strip off country codes
                    if len(urlType[-1]) == 2:
                        urlType = urlType[-2].lower()
                    else:
                        urlType = urlType[-1].lower()
                    # keep url if its TLD is in filterlist
                    if urlType in filterlist:
                        return False
                    else:
                        return True
                         
                except Exception, e:
                    # keep the weird ones
                    return False
                        
            return False
        
        except Exception, e:
            # keep the weird ones
            return False
                
            

########

    def PutUrl(self, parentUrlNetItemIdx, urlToAdd, level,properties=None):
        """
        Add a new URL to the network, or if it already exists, ignore it.
        In either case, return the Node and item index for the URL.
        """
        log = Log('PutUrl',urlToAdd)    
        #print parentUrlNetItemIdx
        #print urlToAdd
        self.ResetLastError()
        try:
            domainItem = None
            isNewItem = False
            
            # remove trailing slash to avoid differentiating between
            # 'www.a.com' and 'www.a.com/'
            while urlToAdd[-1:] == '/':
                urlToAdd = urlToAdd[:-1]
            
            if self.IgnoreFilteredUrl(urlToAdd) == True:
                return (None,self.masterItemIdx,False)
            
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
                self.FlagUrlCheck(item,urlToAdd)
                self.SetUrlTLDProperties(item,urlToAdd)
                
                # we can set multiple properties at once via a dictionary -
                # key-value pairs become properties with name = key, value=value
                if properties:
                    item.SetProperties(properties)
                self.UrlNetItemByIndex[itemIdx] = item
                self.IndexByUrl[urlToAdd] = itemIdx
                self.masterItemIdx = itemIdx
            else:
                itemIdx = item.GetIdx()
                # we always keep the *minimum* level, by default
                oldLevel = item.GetProperty('level')
                if oldLevel != None and level < oldLevel:
                    item.SetProperty('level',level)
                    if oldLevel == self.maxLevel:
                        # force call to GetUrlForest; it wasn't done before because
                        # this item was at the max level the first time it was
                        # encountered.
                        isNewItem = True
                        
            # now do the domain
            isNewDomain = False
            if self.useHostNameForDomainName:
                domain = item.GetHost()
            else:
                domain = item.GetDomain()
            domainIdx = self.GetIndexByDomain(domain)
            if not domainIdx:
                isNewDomain = True
                domainIdx = self.masterDomainIdx + 1
                try:
                    domainItem = DomainNetItem(domainIdx,domain,self)
                except Exception, e:
                    raise Exception, 'DomainNetItem constructor failed: '+str(e)
                self.SetUrlTLDProperties(domainItem,urlToAdd)
                self.DomainByIndex[domainIdx] = domainItem
                self.IndexByDomain[domain] = domainIdx
                self.masterDomainIdx = domainIdx
            else:
                domainItem = self.GetDomainByIndex(domainIdx)

            item.SetDomainIdx(domainIdx)
            oldLevel = domainItem.GetProperty('level')
            if (oldLevel == None or level < oldLevel):
                domainItem.SetProperty('level',level)
                
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
                    # now the domain
                    parentDomainIndex = parent.GetDomainIdx()
                    if parentDomainIndex:
                        domainIdx = item.GetDomainIdx()
                        domainItem = self.GetDomainByIndex(domainIdx)
                        domainItem.AppendParent(parentDomainIndex)
                        # get parent's edgelist and append this
                        parentDomain = self.GetDomainByIndex(parentDomainIndex)
                        if parentDomain:
                            parentDomain.AppendChild(domainIdx)
                                

            #print 'PutUrl added %s...' % urlToAdd
            return (item,itemIdx,isNewItem)
                
        except Exception, e:
            self.SetLastError('in putUrl: ' + str(e) + '\nurl: ' + urlToAdd)
            return (None,-1,False)

    def PutRootUrl(self, urlToAdd):
        """ this function operates a lot like PutUrl, but 'knows' that
            this url is the root, therefore there will be no parent,
            thereby simplifying processing.
        """
        try:
            log = Log('PutRootUrl',urlToAdd)
            #print parentUrlNetItemIdx
            #print urlToAdd
            self.ResetLastError()

            parts = urlparse(urlToAdd)
            pathPart = self.ParsePathParts(parts.path)
            currentDomain = DomainFromHostName(parts.hostname)
            self.rootDomain = currentDomain
            self.rootScheme = parts.scheme
            self.rootHost = parts.hostname

            itemIdx = self.masterItemIdx+1
            try:
                item = self.netitemclass(itemIdx,urlToAdd,self,self.urlclass)
            except Exception, e:
                raise Exception, 'self.netitemclass constructor failed: '+str(e)
            
            item.SetProperty('level',0) # always zero for the root url
            self.FlagUrlCheck(item,urlToAdd)
            self.SetUrlTLDProperties(item,urlToAdd)
            self.UrlNetItemByIndex[itemIdx] = item
            self.IndexByUrl[urlToAdd] = itemIdx
            self.masterItemIdx = itemIdx

            domain = item.GetDomain()
            domainIdx = self.masterDomainIdx+1
            try:
                domainItem = DomainNetItem(domainIdx,domain,self)
            except Exception, e:
                raise Exception, 'DomainNetItem constructor failed: '+str(e)
            self.SetUrlTLDProperties(domainItem,urlToAdd)
            self.DomainByIndex[domainIdx] = domainItem
            self.IndexByDomain[domain] = domainIdx
            self.masterDomainIdx = domainIdx

            item.SetDomainIdx(domainIdx)                                
                
            return (item,itemIdx,pathPart)
                
        except Exception, e:
            self.SetLastError('in putRootUrl: ' + str(e) + '\nurl: ' + urlToAdd)
            return (None,-1,'')

    def SetItemTitleProperty(self,currentItem):
        if currentItem:
            name=currentItem.GetName()
        if name == None or name == '':
            name = 'no name?'
        log = Log('SetItemTitleProperty','item='+name)
        title = currentItem.GetUrl().RetrieveUrlContent(getTitleOnly=True)
        if title == None or title == '':
            title = currentItem.GetName()
            if title == None or title == '':
                title = currentItem.GetUrl()
            if title != None and title != '':
                currentItem.GetUrl().SetProperty('title',title)
        else:
            pass # the property was already set successfully in RetrieveUrlContent()
        
    def ParsePathParts(self,path):
        log = Log('ParsePathParts','path='+str(path))
        realPath = ''
        pathparts = str(path).split('/')
        for i in range(0,len(pathparts)-1):
            if len(pathparts[i])>0:
                realPath = realPath + pathparts[i] + '/'
                
        # always start and end in slash
        if len(realPath) == 0:
            realPath = '/'
        elif realPath[0] != '/':
            realPath = '/' + realPath
        return realPath
    
    def ParamsDictFromUrl(self, url):
        log = Log('ParamsDictFromUrl',url)
        params = {}
        try:
            parts = urlparse(url)
            if not parts[4] or len(parts[4]) == 0:
                return params
            pairs = parts[4].split('&')
            for pair in pairs:
                nmval = pair.split('=')
                params[nmval[0]] = urllib.unquote(nmval[1])
            return params
        except Exception, e:
            self.SetLastError( 'ParamsDictFromUrl: ' + str(e) + '\n\url: << ' + self.url + ' >>' )
            return params
            
    def MassageUrl(self,url,level):
        """ look at, and possibly replace or erase, the url we
                encountered in search
        """
        log = Log('MassageUrl',url)
        try:
            parts = urlparse(url)
            if not parts.hostname:
                return None
            if parts.scheme != '' and parts.scheme not in \
               PERMISSIBLE_SCHEMES:
                return None

            if level != None and level >= 0:
                if self.ignorableText:
                    for text in self.ignorableText:
                        if text in url:
                            return None

            # remove fragments
            lastSlash = url.rfind('/')
            lastPoundSign = url.rfind('#')
            if lastSlash >= 0 and lastPoundSign >= 0:
                if lastPoundSign > lastSlash:
                    url = url[0:lastPoundSign]

            # get rid of tabs, newlines, returns, and spaces by replacing with
            # their uuencode counterparts
            url = re.sub('\t','%07',url)
            url = re.sub('\r','%0D',url)
            url = re.sub('\n','%0A',url)
            url = re.sub(' ','%20',url)
                        
            if self.redirects:
                restrictAtThisLevel = False
                #print url
                for searchTriplet in self.redirects:
                    restrictLevel = searchTriplet[2]
                    textFragment = searchTriplet[0]
                    urlParam = searchTriplet[1]
                    if restrictLevel == level:
                        restrictAtThisLevel = True
                        if textFragment in url:
                            parts = urlparse(url)
                            if len(parts[4]) > 0:
                                pairs = parts[4].split('&')
                                for pair in pairs:
                                    nmval = pair.split('=')
                                    name = nmval[0]
                                    if urlParam == name:
                                        value = nmval[1]
                                        return urllib.unquote(value)
                # if this level had one or more redirects,
                # the only urls of interest are matches;
                # if we got here, there was no match, so
                # if there were restricts for this level,
                # we ignore this url
                if restrictAtThisLevel:
                    return None
                        
            # do nothing else here
            return url
    
        except Exception, e:
            self.SetLastError('in MassageUrl: ' + str(e)\
                              + '\nurl: ' + str(url) )
            return None
       

    def GetUrlNetItemByUrl(self,url):
        """look up index of url in dict by url
        if found:
            get from dict by index
            return self.netitemclass found
        else:
            return None"""
        try:
            log = Log('GetUrlNetItemByUrl',url)
            if url in self.IndexByUrl.keys():
                #log.Write('found in keys()')    
                idx = self.IndexByUrl[url]
                #log.Write('idx=%d' % (idx,))
                return self.GetUrlNetItemByIndex(idx)
            else:
                return None    
        except Exception, e:
            return None

    def GetUrlNetItemByIndex(self,idx):
        """get from dict by index
        return self.netitemclass, or None if not found"""
        log = Log('GetUrlNetItemByIndex',idx)
        try:
            item = self.UrlNetItemByIndex[idx]
            return item
        except Exception, e:
            # new item
            return None

    def UrlExists(self,url):
        """
        See if this URL is already in the network
        """
        log = Log('urlExists',str(url))
        try:
            return (url in self.IndexByUrl.keys())
        except Exception, e:
            return False


    def ForceNodeToLevel(self,level,idx=None,url=None):
        """
        Force an item to a particular level, causing all its child nodes' levels to be
        re-evaluated as well. Either a node index or URL must be supplied.
        """
        log = Log('ForceNodeToLevel','idx: %s, url: %s' % (str(idx),str(url)))
        try:
            if idx == None and url == None:
                raise Exception, 'either index or url must be supplied'
            if idx != None:
                item = self.GetUrlNetItemByIndex(idx)
                if item == None:
                    raise Exception, 'invalid node index'
            else:
                item = self.GetUrlNetItemByUrl(url)
                if item == None:
                    raise Exception, 'invalid url'
            currLevel = item.GetProperty('level')
            if currLevel == None or level < currLevel or pressOnRegardless == True:
                # set new level and recurse into children
                item.SetProperty('level',level)
                for childIdx in item.GetChildren():
                    self.ForceNodeToLevel(level+1,childIdx)
        except Exception, e:
            log.Write('in %: %s' % ('ForceNodeToLevel',str(e)))
            

    
    def MapFunctionToUrlNetwork(self,functionToMap,start=1,level = 0,direction=SEARCH_DOWN,args=None,stack=None):
        """
        map a function against each item in Url network. to avoid recursion, it will not 
        the mapper function takes 4 arguments:
            item:   current self.netitemclass
            net:    current UrlTree
            level:  level in hierarchy, for recursive use; defaults to zero
            args:   user-defined argument; can be sequence or list if
                    multiple arguments are needed
        """
        log = Log('MapFunctionToUrlNetwork')
        # get the start item
        item = self.GetUrlNetItemByIndex(start)
        doContinue = True
        if item:
            doContinue = functionToMap(item, self, level, args)
        else:
            return

        if doContinue and not (level >= self.maxLevel):
            if direction == SEARCH_DOWN:
                list = item.GetChildren()
            else:
                list = item.GetParents()
                
            for edgeID in list:
                self.MapFunctionToUrlNetwork(functionToMap,edgeID,level+1,direction,args,stack)
    
    def MapFunctionToUrlItemList(self,functionToMap,args=None):
        log = Log('MapFunctionToUrlItemList')
        """
        map a function against each item in network, in ascending index order.
        the mapper function takes 4 arguments:
            item:   current self.netitemclass
            net:    current UrlTree
            level:  level property of the current item
            args:   user-defined argument; can be sequence or list if
                    multiple arguments are needed
        """
        # get the start item
        maxIdx = len(self.UrlNetItemByIndex.keys())
        for idx in range(1,maxIdx+1):
            item = self.GetUrlNetItemByIndex(idx)
            level = item.GetProperty('level')
            if level == None:
                log.Write('item without level encountered')
                level = 0
            doContinue = functionToMap(item, self, level, args)
            if not doContinue:
                break
 

    def MapFunctionToParentChildPairs(self,functionToMap,args=None):
        """
        map a function against each the parent-child index pair for
        each item in network, in ascending index order for parent.
        The mapper function must take 4 arguments:
            parentItemIdx:  index of current parent self.netitemclass
            childItemIdx:   index of current child item
            net:            current UrlTree
            args:           user-defined argument; can be sequence or list if
                            multiple arguments are needed
        """
        log = Log('MapFunctionToParentChildPairs')
        # get the start item
        maxIdx = len(self.UrlNetItemByIndex.keys())
        doContinue = True
        for parentIdx in range(1,maxIdx+1):
            item = self.GetUrlNetItemByIndex(parentIdx)
            for childIdx in item.GetChildren():
                doContinue = functionToMap(parentIdx, childIdx, self, args)
                if not doContinue:
                    break
            if not doContinue:
                break
 
    def MapFunctionToUniqueParentChildPairs(self,functionToMap,args=None):
        """
        map a function against each unique parent-child index pair for
        each item in network, in ascending index order for parent.
        The mapper function must take 5 arguments:
            parentItemIdx:  index of current parent self.netitemclass
            childItemIdx:   index of current child item
            frequency:      number of times this arc/edge occurs
            net:            current UrlTree
            args:           user-defined argument; can be sequence or list if
                            multiple arguments are needed
        """
        log = Log('MapFunctionToUniqueParentChildPairs')
        # get the start item
        maxIdx = len(self.UrlNetItemByIndex.keys())
        doContinue = True
        for parentIdx in range(1,maxIdx+1):
            item = self.GetUrlNetItemByIndex(parentIdx)
            children = {}
            for childIdx in item.GetChildren():
                try:
                    count = children[childIdx]
                    children[childIdx] = count + 1
                except Exception, e:
                    children[childIdx] = 1

            keys = children.keys()
            keys.sort()
            for childIdx in keys:
                doContinue = functionToMap(parentIdx, childIdx, children[childIdx], self, args)
                if not doContinue:
                    break
            if not doContinue:
                break

    # domain functions
    def GetIndexByDomain(self,domain):        
        """get from dict by domain name
        return index, or None if not found"""
        log = Log('GetIndexByDomain',domain)
        try:
            domainIdx = self.IndexByDomain[domain]
            return domainIdx
        except Exception, e:
            # new domain
            return None

    def GetDomainByIndex(self,idx):        
        """get from dict by index
        return domain item, or None if not found"""
        log = Log('GetDomainByIndex',idx)
        try:
            domain = self.DomainByIndex[idx]
            return domain
        except Exception, e:
            # new domain
            return None

    def MapFunctionToDomainNetwork(self,functionToMap,start=1,level = 0,direction=SEARCH_DOWN,args=None,stack=None):
        """
        map a function against each item in domain network. to avoid recursion, it will not 
        the mapper function takes 4 arguments:
            item:   current DomainNetItem
            net:    current UrlTree
            level:  level in hierarchy, for recursive use; defaults to zero
            args:   user-defined argument; can be sequence or list if
                    multiple arguments are needed
        """
        log = Log('MapFunctionToDomainNetwork')
        # get the start item
        item = self.GetDomainByIndex(start)
        doContinue = True
        if item:
            doContinue = functionToMap(item, self, level, args)
        else:
            return

        if doContinue and not (level >= self.maxLevel):
            if direction == SEARCH_DOWN:
                list = item.GetChildren()
            else:
                list = item.GetParents()
                
            for edgeID in list:
                self.MapFunctionToDomainNetwork(functionToMap,edgeID,level+1,direction,args,stack)
 
    def MapFunctionToDomainItemList(self,functionToMap,args=None):
        log = Log('MapFunctionToDomainItemList')
        """
        map a function against each item in network, in ascending index order.
        the mapper function takes 4 arguments:
            item:   current DomainItem
            net:    current UrlTree
            level:  level of current DomainItem
            args:   user-defined argument; can be sequence or list if
                    multiple arguments are needed
        """
        # get the start item
        maxIdx = len(self.DomainByIndex.keys())
        for idx in range(1,maxIdx+1):
            item = self.GetDomainByIndex(idx)
            level = item.GetProperty('level')
            if level == None:
                log.Write('item without level encountered')
                level = 0
            doContinue = functionToMap(item, self, level, args)
            if not doContinue:
                break
 
    def MapFunctionToDomainParentChildPairs(self,functionToMap,args=None):
        """
        map a function against each the parent-child index pairs for
        each item in network, in ascending index order for parent.
        The mapper function must take 4 arguments:
            parentItemIdx:  index of current parent DomainNetItem
            childItemIdx:   index of current child item
            net:            current UrlTree
            args:           user-defined argument; can be sequence or list if
                            multiple arguments are needed
        """
        log = Log('MapFunctionToDomainParentChildPairs')
        # get the start item
        maxIdx = len(self.DomainByIndex.keys())
        doContinue = True
        for parentIdx in range(1,maxIdx+1):
            item = self.GetDomainByIndex(parentIdx)
            for childIdx in item.GetChildren():
                doContinue = functionToMap(parentIdx, childIdx, self, args)
                if not doContinue:
                    break
            if not doContinue:
                break
 
    def MapFunctionToUniqueDomainParentChildPairs(self,functionToMap,args=None):
        """
        map a function against each the parent-child index pairs for
        each item in network, in ascending index order for parent.
        The mapper function must take 4 arguments:
            parentItemIdx:  index of current parent DomainNetItem
            childItemIdx:   index of current child item
            frequency:      number of times this arc/edge occurs
            net:            current UrlTree
            args:           user-defined argument; can be sequence or list if
                            multiple arguments are needed
        """
        log = Log('MapFunctionToUniqueDomainParentChildPairs')
        # get the start item
        maxIdx = len(self.DomainByIndex.keys())
        doContinue = True
        for parentIdx in range(1,maxIdx+1):
            item = self.GetDomainByIndex(parentIdx)
            children = {}
            for childIdx in item.GetChildren():
                children[childIdx] = 1

            keys = children.keys()
            keys.sort()
            for childIdx in keys:
                doContinue = functionToMap(parentIdx, childIdx, self, args)
                # print '%d %d' % (parentIdx, childIdx)
                if not doContinue:
                    break
            if not doContinue:
                break

    # network serializers 
    def WritePajekNetworkStream(self,
                                stream,
                                netname,
                                useTitles,
                                urlNet=True,
                                directed=True,
                                reverseDirection=False):
        """
        This function writes a Pajek network or partition for either URLs or domains
        """
        ### first create a directed network
        log = Log('WritePajekNetworkStream','urlNet:' + str(urlNet) + ', directed:'+str(directed))
        try:
            if urlNet == True:
                netType = 'urls'
                maxIdx = len(self.UrlNetItemByIndex.keys())
                vertexMapperFunction = self.MapFunctionToUrlItemList
                arcOrEdgeMapperFunction = self.MapFunctionToParentChildPairs
                arcOrEdgeWriter = WritePajekArcOrEdge
                vertexWriter=WritePajekVertex
            else:
                netType = 'domains'
                maxIdx = len(self.DomainByIndex.keys())
                vertexMapperFunction = self.MapFunctionToDomainItemList
                arcOrEdgeMapperFunction = self.MapFunctionToDomainParentChildPairs
                arcOrEdgeWriter = WritePajekDomainArcOrEdge
                vertexWriter=WritePajekVertex # same for urls and domains
                useTitles = False # force it if it isn't already the case
                
            stream.write('*Network ' + netType + '_' + netname + '_directed\n')
            
            # write vertices by mapping a function to each item in the list
            
            stream.write('*Vertices ' + str(maxIdx) + '\n')
            vertexMapperFunction(functionToMap=vertexWriter,args=(stream,useTitles))

            # write arcs by mapping a function to each parent-child pair in the list.

            stream.write('*Arcs\n')
            if directed == True:
                arcOrEdgeMapperFunction(functionToMap=arcOrEdgeWriter,args=(stream,reverseDirection))

            stream.write('*Edges\n')
            if directed == False:
                arcOrEdgeMapperFunction(functionToMap=arcOrEdgeWriter,args=stream)

        except Exception, e:
            self.SetLastError('In WritePajekNetworkStream: ' + str(e))
            raise

    def WritePajekNetworkFile(self,netname,filename,directed=True,urlNet=True,useTitles=False):
        """
        This function writes a Pajek network file, by default a directed URL network 
        and the levels partition for each. It works by opening the file after adding
        the extension '.net' and then calling WritePajekNetworkStream().
        """
        ### PAJEK
        stream = None
        log = Log('WritePajekNetworkFile',netname+':'+filename)
            
        try:
            if useTitles:
                getTitles = self.GetProperty('getTitles')
                if not getTitles:
                     raise Exception, 'useTitles requested and titles not available; '\
                        + 'set \'getTitles\' property to True before building network'
            stream = open(filename + ".tmp","wb")
            self.WritePajekNetworkStream(stream,
                                netname,
                                useTitles=useTitles,
                                urlNet=urlNet,
                                directed=directed)
            stream.close()
            
            """
            Pajek always requires DOS-like line endings
            """
            ConvertTextFile2DOS(filename + ".tmp",filename + ".net")

        except Exception, e:
            self.SetLastError('In WritePajekNetworkFile: ' + str(e))
            if stream:
                stream.close()
            raise

    def WritePajekPartitionStream(self,stream,partitionName,propertyName,urlNet=True,valueDict=None):
        """
        This function writes a Pajek partition stream, by default a URL partition. 
        It works by calling either WritePajekPartitionFromPropertyValueLookup() or
        WritePajekPartitionFromPropertyDict(), depending on whether a translation
        dictionary is provided.
        """
        
        log = Log('WritePajekNetworkStream','partitionName:' + str(partitionName) \
                  + ', urlNet:'+str(urlNet) \
                  + ', propertyName:'+str(propertyName) \
                  )
            
        try:
            if valueDict != None:
                self.WritePajekPartitionFromPropertyDict(
                                            stream=stream,
                                            partitionName=partitionName,
                                            propertyName=propertyName,
                                            dict=valueDict,
                                            doDomains=(urlNet == False) )
            else:
                self.WritePajekPartitionFromPropertyValueLookup(
                                            stream=stream,
                                            partitionName=partitionName,
                                            propertyName=propertyName,
                                            doDomains=(urlNet == False) )
        except Exception, e:
            self.SetLastError('In WritePajekNetworkStream: ' + str(e))
            raise

    def WritePajekPartitionFile(self,filename,partitionName,propertyName,urlNet=True,valueDict=None):
        """
        This function writes a Pajek partition file, by default a URL partition. 
        It works by opening the file after adding the extension '.clu' and then
        calling either WritePajekPartitionFromPropertyValueLookup() or
        WritePajekPartitionFromPropertyDict(), depending on whether a translation
        dictionary is provided.
        """
        
        ### PAJEK
        stream = None
        log = Log('WritePajekPartitionFile','partitionName:' + str(partitionName) \
                  + ', urlNet:'+str(urlNet) \
                  + ', propertyName:'+str(propertyName) \
                  + ', filename:'+str(filename)
                  )
            
        try:
            stream = open(filename + ".tmp","wb")
            self.WritePajekPartitionStream(stream,partitionName,
                        propertyName,urlNet,valueDict)
            stream.close()
            
            """
            Pajek always requires DOS-like line endings
            """
            ConvertTextFile2DOS(filename + ".tmp",filename + ".clu")

        except Exception, e:
            self.SetLastError('In WritePajekPartitionFile: ' + str(e))
            if stream:
                stream.close()
            raise

    def WritePairNetworkStream(self,
                                stream,
                                netname,
                                urlNet,
                                uniquePairs,
                                delimiter):
        """
        This function writes a Pajek network or partition for either URLs or domains
        """
        ### first create a directed network
        log = Log('WritePairNetworkStream','urlNet = ' + str(urlNet) + \
            ', netname:' + str(netname) + ', uniquePairs:'+str(uniquePairs))
        try:
            if urlNet == True:
                netType = 'urls'
                maxIdx = len(self.UrlNetItemByIndex.keys())
                if uniquePairs == False:
                    arcOrEdgeMapperFunction = self.MapFunctionToParentChildPairs
                else:
                    arcOrEdgeMapperFunction = self.MapFunctionToUniqueParentChildPairs
                arcOrEdgeWriter = WritePairArcOrEdge
            else:
                netType = 'domains'
                maxIdx = len(self.DomainByIndex.keys())
                if uniquePairs == False:
                    arcOrEdgeMapperFunction = self.MapFunctionToDomainParentChildPairs
                else:
                    arcOrEdgeMapperFunction = self.MapFunctionToUniqueDomainParentChildPairs
                arcOrEdgeWriter = WritePairDomainArcOrEdge
                
            # write arcs by mapping a function to each parent-child pair in the list.

            arcOrEdgeMapperFunction(functionToMap=arcOrEdgeWriter,args=(stream,uniquePairs,delimiter))
            
        except Exception, e:
            self.SetLastError('In WritePairNetworkStream: ' + str(e))
            raise

    def WritePairNetworkFile(self,netname,filename,urlNet=True, uniquePairs = False, delimiter = '\t'):
        """
        This function writes a file containing, by default, both URL and domain networks,
        and the levels partition for each. It works by opening the file after appending
        the extension 'paj' and then calling WritePajekStream().
        """
        
        stream = None
        log = Log('WritePairNetworkFile',netname+':'+filename)
            
        try:
            stream = open(filename + ".tmp","wb")
            self.WritePairNetworkStream(stream,netname,urlNet,uniquePairs,delimiter)
            stream.close()
            
            """
            Pajek always requires DOS-like line endings
            """
            ConvertTextFile2DOS(filename + ".tmp",filename + ".pairs")

        except Exception, e:
            self.SetLastError('In WritePairNetworkFile: ' + str(e))
            if stream:
                stream.close()
            raise

    def WritePajekFile(self,netname,filename,doDomains=True,doOnlyDomains=False,useTitles=False):
        ### PAJEK
        URLFILE = None
        log = Log('WritePajekFile',netname+':'+filename)
            
        try:
            if useTitles:
                getTitles = self.GetProperty('getTitles')
                if not getTitles:
                     raise Exception, 'useTitles requested and titles not available; '\
                        + 'set ''getTitles'' property to True before building network'
            URLFILE = open(filename + ".tmp","wb")
            self.WritePajekStream(netname,URLFILE,doDomains,doOnlyDomains,useTitles)
            URLFILE.close()
            """
            Pajek always requires DOS-like line endings
            """
            ConvertTextFile2DOS(filename + ".tmp",filename + ".paj")
                
        except Exception, e:
            self.SetLastError('In WritePajekFile: ' + str(e))
            if URLFILE:
                URLFILE.close()
                os.remove(filename + ".tmp")
            raise

    def WritePajekStream(self,netname,stream,doDomains=True,doOnlyDomains=False,useTitles=False):
        ### PAJEK
        log = Log('WritePajekStream',netname)
        try:
            # for some kinds of networks, it is useful to reverse direction of arcs
            # or edges
            reverseDirection = False
            try:
                reverseDirection = self.GetProperty('reverseArcOrEdgeDirection')
            except Exception, e:
                raise 'in UrlTree.WritePajekStream, self.GetProperty call threw exception ' + str(e)
            if reverseDirection == None:
                reverseDirection = False
            elif reverseDirection != False:
                reverseDirection = True
                
            stream.write('*Network urls_' + netname + '_directed\n')
            maxIdx = len(self.UrlNetItemByIndex.keys())

            if not doOnlyDomains:
                
                ### first create a directed network
                
                # write vertices by mapping a function to each item in the list
                
                stream.write('*Vertices ' + str(maxIdx) + '\n')
                self.MapFunctionToUrlItemList(functionToMap=WritePajekVertex,args=(stream,useTitles))

                # write arcs by mapping a function to each parent-child pair in the list.

                stream.write('*Arcs\n')
                self.MapFunctionToParentChildPairs(functionToMap=WritePajekArcOrEdge,args=(stream,reverseDirection))

                stream.write('*Edges\n')
                #none

                ### now create an undirected network
                # write vertices by mapping a function to each item in the list
                
                stream.write('\n*Network urls_' + netname + '_undirected\n')
                stream.write('*Vertices ' + str(maxIdx) + '\n')
                self.MapFunctionToUrlItemList(functionToMap=WritePajekVertex,args=(stream,useTitles))

                # write arcs by mapping a function to each parent-child pair in the list.

                stream.write('*Arcs\n')
                #none

                stream.write('*Edges\n')
                self.MapFunctionToParentChildPairs(functionToMap=WritePajekArcOrEdge,args=(stream,reverseDirection))
                    
                stream.write('\n\n*Partition URLLevels.clu\n*Vertices ' + str(maxIdx) + ' \n')
                itemlist = {}
                self.MapFunctionToUrlItemList(BuildListOfItemIndicesWithLevel,args=itemlist)
                keys = itemlist.keys()
                keys.sort()
                for idx in keys:
                    (level,count) = itemlist[idx]
                    spaces = ' '*(8-len(str(level)))
                    stream.write(spaces + str(level) + '\n')
                    if idx > maxIdx:
                        self.SetLastError( 'too many keys in partition list: ' + str(idx) )

            doTLDProps = self.GetProperty('TrackTLDProperties')
            if doTLDProps == None or doTLDProps == False:
                pass
            else:
                # write for-profit and not-for-profit partition
                self.WritePajekPartitionFromPropertyValueLookup(stream,\
                    'URL Net TLD For-Profit/Not-For-Profit','forProfitUrlTLD',
                                                   defaultPartitionNumber=0,
                                                   doDomains=False)
                # write for-profit and not-for-profit partition
                self.WritePajekPartitionFromPropertyValueLookup(stream,\
                    'URL Net TLD Type','urlTLD',
                                                   defaultPartitionNumber=DOTUNK,
                                                   doDomains=False)
                # write TLD type vector
                self.WritePajekVectorFromPropertyValueLookup(stream,\
                    vectorName='URL Net TLD Type',propertyName='urlTLDVector',
                                                   defaultVectorValue=0.0,
                                                   doDomains=False)
                                                
                                                
            # see if there are flag paritions we need to process
            doFlaggedPartitions = (\
                self.urlsToFlag != None and len(self.urlsToFlag.keys()) > 0)
            
            if doFlaggedPartitions:
                for partition in self.urlsToFlag.keys():
                    self.WritePajekPartitionFromPropertyValueLookup(stream,\
                        partition, partition, \
                                                   defaultPartitionNumber=0, \
                                                   doDomains=False)
                
            ########################################
            # now do the domain networks
            ########################################
            if doDomains:
                stream.write('*Network domains_' + netname + '_directed\n')
                maxIdx = len(self.DomainByIndex.keys())

                ### first create a directed network
                
                # write vertices by mapping a function to each item in the list
                
                stream.write('*Vertices ' + str(maxIdx) + '\n')
                # domain networks don't use titles
                self.MapFunctionToDomainItemList(functionToMap=WritePajekVertex,args=(stream,False))

                # write arcs by mapping a function to each parent-child pair in the list.

                stream.write('*Arcs\n')
                self.MapFunctionToDomainParentChildPairs(functionToMap=WritePajekDomainArcOrEdge,
                    args=(stream,reverseDirection))

                stream.write('*Edges\n')
                #none

                ### now create an undirected network
                # write vertices by mapping a function to each item in the list
                
                stream.write('\n*Network domains_' + netname + '_undirected\n')
                stream.write('*Vertices ' + str(maxIdx) + '\n')
                # domain networks don't use titles
                self.MapFunctionToDomainItemList(functionToMap=WritePajekVertex,args=(stream,False))

                # write arcs by mapping a function to each parent-child pair in the list.

                stream.write('*Arcs\n')
                #none

                stream.write('*Edges\n')
                self.MapFunctionToDomainParentChildPairs(functionToMap=WritePajekDomainArcOrEdge,
                    args=(stream,reverseDirection))
                    
                stream.write('\n\n*Partition DomainLevels.clu\n*Vertices ' + str(maxIdx) + ' \n')
                itemlist = {}
                self.MapFunctionToDomainItemList(BuildListOfItemIndicesWithLevel,args=itemlist)
                keys = itemlist.keys()
                keys.sort()
                for idx in keys:
                    (level,count) = itemlist[idx]
                    spaces = ' '*(8-len(str(level)))
                    stream.write(spaces + str(level) + '\n')
                    if idx > maxIdx:
                        print 'too many keys in partition list: ' + str(idx)
                if doTLDProps == None or doTLDProps == False:
                    pass
                else:
                    # write for-profit and not-for-profit partition
                    self.WritePajekPartitionFromPropertyValueLookup(stream,\
                        'Domain Net TLD For-Profit/Not-For-Profit','forProfitUrlTLD',
                                                       defaultPartitionNumber=0,
                                                       doDomains=True)
                    # write for-profit and not-for-profit partition
                    self.WritePajekPartitionFromPropertyValueLookup(stream,\
                        'Domain Net TLD Type','urlTLD',
                                                       defaultPartitionNumber=DOTUNK,
                                                       doDomains=True)
                    # write TLD type vector
                    self.WritePajekVectorFromPropertyValueLookup(stream,\
                        vectorName='Domain Net TLD Type',propertyName='urlTLDVector',
                                                       defaultVectorValue=0.0,
                                                       doDomains=True)
        except Exception, e:
            self.SetLastError('In WritePajekFile: ' + str(e))
            log.Write('In WritePajekFile: ' + str(e))
            raise

    def WritePajekPartitionFromPropertyValueLookup(self,fd,partitionName,propertyName,
                                                   defaultPartitionNumber=None,
                                                   doDomains=False):
        """
        Write a Pajek partition using the value of a property on each 
        UrlNetItem-descended node instance. The property value must be an 
        integer.
        """
        log = Log('WritePajekPartitionFromPropertyValueLookup',"%s, %s, %s" % (str(partitionName),str(propertyName),str(dict)))
        try:
            if doDomains == False:
                maxIdx = len(self.UrlNetItemByIndex.keys())
            else:
                maxIdx = len(self.DomainByIndex.keys())
            fd.write(('\n\n*Partition %s \n*Vertices ' % (partitionName)) + str(maxIdx) + ' \n')
            itemlist = {}
            if defaultPartitionNumber == None:
                defaultPartitionNumber = self.PAJEK_NULL_PARTITION
            if doDomains == False:
                self.MapFunctionToUrlItemList(BuildListOfItemIndicesWithPropertyValueLookup,
                                                  args=(propertyName,itemlist,defaultPartitionNumber))
            else:
                self.MapFunctionToDomainItemList(BuildListOfItemIndicesWithPropertyValueLookup,
                                                  args=(propertyName,itemlist,defaultPartitionNumber))
            keys = itemlist.keys()
            keys.sort()
            for idx in keys:
                nodetype = itemlist[idx]
                spaces = ' '*(8-len(str(nodetype)))
                fd.write(spaces + str(nodetype) + '\n')
                if idx > maxIdx:
                    self.SetLastError( 'too many keys in partition list: ' + str(idx) )
        except Exception, e:
            self.SetLastError('In WritePajekPartitionFromPropertyValueLookup: ' + str(e))
            raise

    def WritePajekPartitionFromPropertyDict(self,fd,partitionName,propertyName,dict,
                                                defaultPartitionNumber=None,
                                                doDomains=False):
        """
        Write a Pajek partition using the value of a property on each 
        UrlNetItem-descended node instance. A dictionary is used to 
        translate property values into integer partition numbers.
        """
        log = Log('WritePajekPartitionFromPropertyDict',"%s, %s, %s" % \
            (str(partitionName),str(propertyName),str(dict)))
        try:
            if doDomains == False:
                maxIdx = len(self.UrlNetItemByIndex.keys())
            else:
                maxIdx = len(self.DomainByIndex.keys())
            if defaultPartitionNumber == None:
                defaultPartitionNumber = self.PAJEK_NULL_PARTITION
            fd.write('\n\n*Partition %s (' % (partitionName))
            first = True
            keys = dict.keys()
            keys.sort()
            for name in keys:
                if first:
                    first = False
                else:
                    fd.write(',')
                fd.write('%s=%d' % (name, dict[name]))
            fd.write(') \n*Vertices ' + str(maxIdx) + ' \n')
            itemlist = {}
            if doDomains == False:
                self.MapFunctionToUrlItemList(BuildListOfItemIndicesWithPropertyValueDict,
                                                  args=(itemlist,propertyName,dict,defaultPartitionNumber))
            else:
                self.MapFunctionToDomainItemList(BuildListOfItemIndicesWithPropertyValueDict,
                                                  args=(itemlist,propertyName,dict,defaultPartitionNumber))
            keys = itemlist.keys()
            keys.sort()
            for idx in keys:
                nodetype = itemlist[idx]
                spaces = ' '*(8-len(str(nodetype)))
                fd.write(spaces + str(nodetype) + '\n')
                if idx > maxIdx:
                    self.SetLastError( 'too many keys in partition list: ' + str(idx) )
        except Exception, e:
            self.SetLastError('In WritePajekPartitionFromPropertyDict: ' + str(e))
            raise

    def WritePajekVectorFromPropertyValueLookup(self,fd,vectorName,propertyName,defaultVectorValue,doDomains = False):
        """
        Write a Pajek vector using the value of a property on each UrlNetItem-descended
        node instance. A dictionary is used to translate property values into integer
        partition numbers.
        """
        log = Log('WritePajekVectorFromPropertyValueLookup',"%s, %s, %s" \
                % (str(vectorName),str(propertyName),str(defaultVectorValue)))
        try:
            if doDomains == False:
                maxIdx = len(self.UrlNetItemByIndex.keys())
            else:
                maxIdx = len(self.DomainByIndex.keys())
            fd.write('\n\n*Vector %s\n*Vertices %d \n' % (vectorName,maxIdx))
            itemlist = {}
            if doDomains == False:
                self.MapFunctionToUrlItemList(BuildListOfItemIndicesWithPropertyValueLookup,
                                                  args=(propertyName,itemlist,defaultVectorValue))
            else:
                self.MapFunctionToDomainItemList(BuildListOfItemIndicesWithPropertyValueLookup,
                                                  args=(propertyName,itemlist,defaultVectorValue))
            keys = itemlist.keys()
            keys.sort()
            for idx in keys:
                try:
                    value = itemlist[idx]
                except Exception, e:
                    log.Write('in UrlTree.WritePajekVectorFromPropertyValueLookup, no value for item with index %d' % (idx))
                    value = None
                if value == None:
                        value = 0.0
                valuestr = '%.4f' % (value * 100.0)
                spaces = ' '*(8-len(valuestr))
                fd.write(spaces + str(value) + '\n')
                if idx > maxIdx:
                    self.SetLastError( 'too many keys in partition list: ' + str(idx) )
        except Exception, e:
            log.Write('In WritePajekVectorFromPropertyValueLookup: ' + str(e))
            self.SetLastError('In WritePajekVectorFromPropertyValueLookup: ' + str(e))
            raise


    def WriteGuessFile(self,filename,doUrlNetwork=True,useTitles=False):
        """
        Write either a URL network or a domain network in GUESS
        format; which to write depends on the value of doUrlNetwork.
        """
        log = Log('WriteGuessFile',"%s, %s" % (str(filename),str(doUrlNetwork)))
        URLFILE = None
        try:
            if useTitles:
                getTitles = self.GetProperty('getTitles')
                if not getTitles:
                     raise Exception, 'useTitles requested and titles not available; '\
                        + 'set ''getTitles'' property to True before building network'
            URLFILE = open(filename + ".gdf","w")
            self.WriteGuessStream(URLFILE,doUrlNetwork,useTitles)
            URLFILE.close()
        except Exception, e:
            self.SetLastError('In WriteGuessFile: ' + str(e))
            if URLFILE:
                URLFILE.close()
            raise

    def WriteGuessStream(self,stream,doUrlNetwork=True,useTitles=False):
        """
        Write either a URL network or a domain network in GUESS
        format; which to write depends on the value of doUrlNetwork.
        """
        log = Log('WriteGuessStream',"%s" % (str(doUrlNetwork)))
        nodedef = 'nodedef>name VARCHAR, url VARCHAR,domain VARCHAR, theLevel INT'
        domainNodedef = 'nodedef>name VARCHAR, domain VARCHAR'
        edgedef = 'edgedef>node1 VARCHAR,node2 VARCHAR,frequency INT'       
        try:
            # for some kinds of networks, it is useful to reverse direction of arcs
            # or edges
            reverseDirection = False
            try:
                reverseDirection = self.GetProperty('reverseArcOrEdgeDirection')
            except Exception, e:
                raise 'in UrlTree.WriteGuessStream, self.GetProperty call threw exception ' + str(e)
            if reverseDirection == None:
                reverseDirection = False
            elif reverseDirection != False:
                reverseDirection = True
                
            if doUrlNetwork:
                """
                if present, additionalUrlAttrs property value should be a list of two-item tuples containing
                name/type pairs. The name should be a legal Python variable name, and the type should be one
                of CHAR, VARCHAR, DATE, TIME, DATETIME, BOOLEAN, INT, FLOAT, DOUBLE, BIGINT, or TINYINT; the
                name of the type should of course be a string.
                The name should be a property on each URlNetItem instance in the network. For example:
                    
                IF the network's additionalUrlAttrs property contains [('pos_prob','DOUBLE',),]
                THEN each item should have a property named 'pos_prob' whose value is a double float.
                """
                additionalUrlAttrs = self.GetProperty('additionalUrlAttrs')
                if additionalUrlAttrs != None:
                    for attrName, attrType in additionalUrlAttrs:
                        nodedef = '%s, %s %s' % (nodedef, attrName, attrType)
                stream.write(nodedef + '\n')
                maxIdx = len(self.UrlNetItemByIndex.keys())
                # write vertices by mapping a function to each item in the list
                    
                self.MapFunctionToUrlItemList(functionToMap=WriteGuessVertex,args=(stream,useTitles,additionalUrlAttrs))

                # write arcs by mapping a function to each parent-child pair in the list.
                stream.write(edgedef + '\n')
                self.MapFunctionToUniqueParentChildPairs(functionToMap=WriteGuessArc,
                    args=(stream,reverseDirection))
            else:
                additionalDomainAttrs = self.GetProperty('additionalDomainAttrs')
                if additionalDomainAttrs != None:
                    for attrName, attrType in additionalDomainAttrs:
                        domainNodedef = '%s, %s %s' % (domainNodedef, attrName, attrType)
                stream.write(domainNodedef + '\n')
                maxIdx = len(self.DomainByIndex.keys())

                # write vertices by mapping a function to each item in the list
                
                self.MapFunctionToDomainItemList(functionToMap=WriteGuessDomainVertex,args=(stream,additionalDomainAttrs))

                # write arcs by mapping a function to each parent-child pair in the list.
                stream.write(edgedef + '\n')
                self.MapFunctionToUniqueDomainParentChildPairs(functionToMap=WriteGuessDomainArc,
                    args=(stream,reverseDirection))
 
        except Exception, e:
            self.SetLastError('In WriteGuessStream: ' + str(e))
            raise

    def WriteUrlHierarchyStream(self,fd,useTitles=False):
        log = Log('WriteUrlHierarchyStream')
        try:
            self.MapFunctionToUrlItemList(PrintHierarchy,args=(fd,useTitles))
        except Exception, e:
            print str(e)
            self.SetLastError(str(e))
        
    def WriteUrlHierarchyFile(self,filename,writeHeader=True,useTitles=False):
        log = Log('WriteUrlHierarchyFile')
        try:
            fd = open(filename,'w')
            if writeHeader:
                fd.write('********** URL Network ***************\n\n')
            self.WriteUrlHierarchyStream(fd,useTitles=useTitles)
            fd.close()
        except Exception, e:
            print str(e)
            self.SetLastError(str(e))
        
    def WriteDomainHierarchyStream(self,fd):
        log = Log('WriteDomainHierarchyStream')
        try:
            # we never use titles with domain networks.
            self.MapFunctionToDomainItemList(PrintHierarchy,args=(fd,False))
        except Exception, e:
            print str(e)
            self.SetLastError(str(e))
        
    def WriteDomainHierarchyFile(self,filename,writeHeader=True):
        log = Log('WriteDomainHierarchyFile')
        try:
            fd = open(filename,'w')
            if writeHeader:
                fd.write('********** Domain Network ***************\n\n')
            self.WriteDomainHierarchyStream(fd)
            fd.close()
        except Exception, e:
            print str(e)
            self.SetLastError(str(e))
        

    def SetTruncatableText(self,listOfStringsThatWhenFoundEmbeddedTriggerTruncatingaURL):
        self.truncatableText = listOfStringsThatWhenFoundEmbeddedTriggerTruncatingaURL
    

    def GetTruncatableText(self):
        return self.truncatableText


    def SetIgnorableText(self,listOfStringsThatWhenFoundEmbeddedTriggerIgnoringaURL):
        self.ignorableText = listOfStringsThatWhenFoundEmbeddedTriggerIgnoringaURL
    

    def GetIgnorableText(self):
        return self.ignorableText

    def SetRedirects(self,redirects):
        self.redirects = redirects
    
    def GetRedirects(self):
        return self.redirects

###################### end of class ########################

# current number of unit tests
numtests = 4

def main(tests=range(1,numtests+1)):
    import log
    global numtests

    # get workingDir from the config file
    workingDir = GetConfigValue('workingDir')
    if workingDir:
        os.chdir(workingDir)
    else:
        raise Exception( 'no working directory entry in config file, or config file not found' )
    
    log.logging = True
    log.altfd = open(workingDir+'/log.txt','w')
    mylog = Log('main')
    
    urls = [
        'http://hunscher.livejournal.com/profile',
        'http://www.livejournal.com/support/',
        'http://www.livejournal.com/support',
        ]
    textStringsToIgnore = [
        'payloadz.com',
        'sitemeter.com',
        ]
    
    if 1 in tests:
        x = UrlTree(_maxLevel=3,_ignorableText=textStringsToIgnore)
        ret = x.BuildUrlTree('http://www.southwindpress.com')
        if ret:
            testfd=open('test1.txt','w')
            testfd.write('********** URL Network ***************\n\n')
            x.MapFunctionToUrlNetwork(PrintHierarchy,args=(testfd,False))
            testfd.write('\n\n\n\n********** Domain Network ***************\n\n')
            x.MapFunctionToDomainNetwork(PrintHierarchy,args=(testfd,False))
            x.WritePajekFile('test1','test1')
            x.WriteGuessFile('test1urls')            # url network
            x.WriteGuessFile('test1domains',False)      #domain network
            testfd.close()


    if 2 in tests:
        x = UrlTree(_maxLevel=2,_workingDir=workingDir)
        ret = x.BuildUrlForest(urls)
        if ret:
            testfd=open('test2.txt','w')
            testfd.write('********** URL Network ***************\n\n')
            x.MapFunctionToUrlNetwork(PrintHierarchy,args=(testfd,False))
            testfd.write('\n\n\n\n********** Domain Network ***************\n\n')
            x.MapFunctionToDomainNetwork(PrintHierarchy,args=(testfd,False))
            x.WritePajekFile('test2','test2')
            x.WriteGuessFile('test2urls')            # url network
            x.WriteGuessFile('test2domains',False)      #domain network
            testfd.close()


    if 3 in tests:    
        x = UrlTree(_maxLevel=3,_workingDir=workingDir)
        ret = x.BuildUrlTreeWithPlaceholderRoot('http://www.livejournal.com',urls)
        if ret:
            testfd=open('test3.txt','w')
            testfd.write('********** URL Network ***************\n\n')
            x.MapFunctionToUrlNetwork(PrintHierarchy,args=(testfd,False))
            testfd.write('\n\n\n\n********** Domain Network ***************\n\n')
            x.MapFunctionToDomainNetwork(PrintHierarchy,args=(testfd,False))
            x.WritePajekFile('test3','test3')
            x.WriteGuessFile('test3urls')            # url network
            x.WriteGuessFile('test3domains',False)      #domain network
            testfd.close()
    

    if 4 in tests:       
        textToIgnore = [
        'buzz.blogger.com',
        'code.blogspot.com',
        'hl7.org',
        'hl7.com',
        'statcounter.com',
        'swicki',
        'eurekster',
        'yahoo.com',
        'technorati.com',
        'ads2.',
        'feeddigest',
        'sitemeter',
        'clustrmaps',
        'del.icio.us',
        'digg.com',
        'zeus.com',
        'feedburner.com',
        'google.com',
        'go.microsoft.com',
        'overture.com',
        '/feed/',
        '/rdf/',
        '/rss/',
        'help.blogger.com',
        'home.businesswire.com',
        'sys-con.com',
        'jigsaw.w3c.org',
        'medicalconnectivity.com/categories',
        'rss.xml',
        'misoso.com',
        'adjuggler.com',
        'skype.com',
        'validator.w3c.org',
        'google.ca',
        'hollywood.com',
        'addthis.com',
        'www.ahrq.com',
        'amia.org',
        'bordersstores.com',
        'hhs.gov',
        'feedblitz',
        'feeddigest',
        'feedster',
        '.com/about/',
        'sitemap',
        'site-map',
        'flickr.com',
        'gpoaccess.gov',
        'googlestore.com',
        'www.himss',
        '/faq.',
        'www.hl7.org',
        'linkedin.com',
        'loinc.org',
        'www.medinfo',
        'mysql.com',
        'www.nytimes.com/',
        'www.state.wv',
        '/privacy/',
        '/privacy.',
        'usa.gov',
        'www.va.gov',
        'youtube.com',
        ]

        # Because we are using a phantom root, the URLs found in the phantom
        # root page's anchorlist will be at level 1, which is where we want to
        # do our checking. In this case we are looking for just one pattern.
        testRedirects = (('/mc/mc.php?','link',0),
                         )
        x = UrlTree(_maxLevel=1,_workingDir=workingDir,_redirects=testRedirects)
        x.SetIgnorableText(textToIgnore)
        ret = x.BuildUrlForestWithPhantomRoot('http://www.hitsphere.com/')
        if ret:
            testfd=open('test4.txt','w')
            testfd.write('********** URL Network ***************\n\n')
            x.MapFunctionToUrlNetwork(PrintHierarchy,args=(testfd,False))
            testfd.write('\n\n\n\n********** Domain Network ***************\n\n')
            x.MapFunctionToDomainNetwork(PrintHierarchy,args=(testfd,False))
            x.WritePajekFile('test4','test4')
            x.WriteGuessFile('test4urls')            # url network
            x.WriteGuessFile('test4domains',doUrlNetwork=False) #domain network
            testfd.close()
    
    log.altfd.close()
    log.altfd=None
    sys.exit(0)

if __name__ == '__main__':

    # to do one test or selected tests, put their numbers in a list:
    # main([1,2,3,4])
    main([1,])

    # to do all tests, no argument is needed:
    #main()
    
