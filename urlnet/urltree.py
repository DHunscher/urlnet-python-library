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

NO_REGEX = -1

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
            # given an index, returns our linking data structure
            self.DomainByIndex = {}
            #dict by domain hash:
             # given a domain, returns (index)
            self.IndexByDomain = {}

            self.rootDomain = None
            self.rootScheme = None
            self.rootHost = None
            
            # set up redirects, ignorables and truncatables
            self.redirects = _redirects
            self.ignorableText = _ignorableText
            self.truncatableText = _truncatableText
            self.truncatableTextSearchArgs = NO_REGEX
            self.ignorableTextSearchArgs = NO_REGEX

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
            
            # our supplied inclusion checker by page content function is 
            # urlutils.CheckInclusionExclusionCriteria, but you can
            # override it through a call to SetPageContentCheckerFn
            
            self.PageContentCheckerFn = CheckInclusionExclusionCriteria
            self.applyInclusionExclusionCriteriaByURL = None
            
            # initialize attributes used in default inclusion/exclusion
            # checker
            self.include_patternlist = None
            self.include_patternlist_flags = None
            self.exclude_patternlist = None
            self.exclude_patternlist_flags = None
            self.check4InclusionExclusionCriteria = True

            # initialize attribute for custom URL 
            # and domain property setters
            self.CustomUrlPropertiesSetter = None
            self.CustomDomainPropertiesSetter = None
            
            #
            self.lastPage = None
            self.earlyReadSucceeded = True
            
            # default to using cached page if it exists; NCBI will turn this 
            # off, and so will search engine programs, both of which
            # do multiple HTTP GETs in the same Url-derived instance.
            self.useCachedPageIfItExists = True
            
            # Url's constructor will use this to support restoring later
            self.originalUrlClass = None
            
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
            if (not currentItem):
                return False
            getTitles = self.GetProperty('getTitles')
            if (self.singleDomain and self.showLinksToOtherDomains and (self.rootDomain != currentDomain)):
                if isNewItem and getTitles:
                    # set title for output later
                    self.SetItemTitleProperty(currentItem)
                return True 
            if self.truncatableText:
                for text in self.truncatableText:
                    if ((self.truncatableTextSearchArgs == NO_REGEX) \
                                and (text in url)):
                        # truncate tree traversal here. We put the url in the tree, but it's
                        #   not one we want to follow.
                        if isNewItem:
                            # get title only; don't need to do it as a separate action if recursing,
                            # because it will be a side effect of getting the child URLs
                            self.SetItemTitleProperty(currentItem)
                        return True
                    elif ((self.truncatableTextSearchArgs != NO_REGEX) and \
                                (re.search(text, url, self.truncatableTextSearchArgs))):
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

########
    def SetPageContentCheckerFn(self, fn):
        self.PageContentCheckerFn = fn

    def SetApplyInclusionExclusionCriteriaByUrlFn(self, fn):
        self.applyInclusionExclusionCriteriaByURL = fn

    def SetCustomDomainPropertiesFn(self, fn):
        self.CustomDomainPropertiesSetter = fn

    def SetCustomUrlPropertiesFn(self, fn):
        self.CustomUrlPropertiesSetter = fn

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
            self.lastPage = None
            
            # remove trailing slash to avoid differentiating between
            # 'www.a.com' and 'www.a.com/'
            while urlToAdd[-1:] == '/':
                urlToAdd = urlToAdd[:-1]
            
            # check to see if we need to exclude based on the URL in and of
            # itself, as opposed to due to page content criteria.
            
            if self.applyInclusionExclusionCriteriaByURL:
                if self.applyInclusionExclusionCriteriaByURL(self,urlToAdd) == True:
                    return (None,self.masterItemIdx,False)
            
            item = self.GetUrlNetItemByUrl(urlToAdd)
            # see if URL is already registered
            if not item:
                # new item
                # check inclusion/exclusion criteria here, if applicable
                if self.PageContentCheckerFn != None: 
                    if self.PageContentCheckerFn(self,\
                                urlToAdd,\
                                level):
                        pass
                    else:
                        return (None,self.masterItemIdx,False)
                isNewItem = True
                itemIdx = self.masterItemIdx + 1
                try:
                    item = self.netitemclass(itemIdx,urlToAdd,self,self.urlclass)
                except Exception, e:
                    raise Exception, 'self.netitemclass constructor failed: '+str(e)
                item.SetProperty('level',level)
                
                # see if we should set custom properties
                if self.CustomUrlPropertiesSetter:
                    try:
                        self.CustomUrlPropertiesSetter(self,item,urlToAdd)
                    except Exception, e:
                        log.Write(
                            'user defined custom URL properties Setter function threw exception: %s' % (str(e)))
                        self.CustomUrlPropertiesSetter = None
                        
                # if we applied a custom inclusion/exclusion function earlier, 
                # we may have left some URL properties to set, which we couldn't do
                # then because the item instance didn't exist yet. The custom
                # function should have left any properties to set in the form
                # of a dictionary as the value of the net property 'UrlPropsToSet'.
                # If they're there, set them now.
                if self.PageContentCheckerFn != None: 
                    props2Set = self.GetProperty('UrlPagePropsToSet')
                    if props2Set:
                        item.SetProperties(props2Set)
                        self.SetProperty('UrlPagePropsToSet', None)
                        
                # do the same if a properties argument was passed to this
                # function.
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

                domainItem.SetProperty('level',level)

                # see if we should set custom properties
                if self.CustomDomainPropertiesSetter:
                    try:
                        self.CustomDomainPropertiesSetter(self,domainItem,urlToAdd)
                    except Exception, e:
                        log.Write(
                            'user defined custom domain properties setter function threw exception: %s' % (str(e)))
                        self.CustomDomainPropertiesSetter = None

                # if we applied a custom inclusion/exclusion function earlier, 
                # we may have left some domain properties to set, which we couldn't do
                # then because the item instance didn't exist yet. The custom
                # function should have left any properties to set in the form
                # of a dictionary as the value of the net property 'DomainPagePropsToSet'.
                # If they're there, set them now.
                if self.PageContentCheckerFn != None: 
                    props2Set = self.GetProperty('DomainPagePropsToSet')
                    if props2Set:
                        domainItem.SetProperties(props2Set)
                        self.SetProperty('DomainPagePropsToSet', None)
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
        log = Log('PutRootUrl',urlToAdd)
        try:
            self.ResetLastError()
            self.lastPage = None

            # warn if we exclude the root based on user-defined criteria
            if self.applyInclusionExclusionCriteriaByURL:
                if self.applyInclusionExclusionCriteriaByURL(self,urlToAdd) == True:
                    log.Write('Warning: excluded root URL %s' % urlToAdd)
                    return (None,self.masterItemIdx,False)
            
            # check inclusion/exclusion criteria here
            if self.PageContentCheckerFn != None: 
                if self.PageContentCheckerFn(self,urlToAdd,0):
                    pass
                else:
                    return (None,self.masterItemIdx,False)

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
            
            # see if we should set custom properties
            if self.CustomUrlPropertiesSetter:
                try:
                    self.CustomUrlPropertiesSetter(self,item,urlToAdd)
                except Exception, e:
                    log.Write(
                        'user defined custom URL propertiesSetter function threw exception: %s' % (str(e)))
                    self.CustomUrlPropertiesSetter = None
                    
            # if we applied a custom inclusion/exclusion function earlier, 
            # we may have left some URL properties to set, which we couldn't do
            # then because the item instance didn't exist yet. The custom
            # function should have left any properties to set in the form
            # of a dictionary as the value of the net property 'UrlPagePropsToSet'.
            # If they're there, set them now.
            if self.PageContentCheckerFn != None: 
                props2Set = self.GetProperty('UrlPagePropsToSet')
                if props2Set:
                    item.SetProperties(props2Set)
                    self.SetProperty('UrlPagePropsToSet', None)
                    
            self.UrlNetItemByIndex[itemIdx] = item
            self.IndexByUrl[urlToAdd] = itemIdx
            self.masterItemIdx = itemIdx

            domain = item.GetDomain()
            domainIdx = self.masterDomainIdx+1
            try:
                domainItem = DomainNetItem(domainIdx,domain,self)
            except Exception, e:
                raise Exception, 'DomainNetItem constructor failed: '+str(e)

            domainItem.SetProperty('level',0) # always zero for the root url
            
            # see if we should set custom properties
            if self.CustomDomainPropertiesSetter:
                try:
                    self.CustomDomainPropertiesSetter(self,domainItem,urlToAdd)
                except Exception, e:
                    log.Write(
                        'user defined custom domain properties setter function threw exception: %s' % (str(e)))
                    self.CustomDomainPropertiesSetter = None

            # if we applied a custom inclusion/exclusion function earlier, 
            # we may have left some domain properties to set, which we couldn't do
            # then because the item instance didn't exist yet. The custom
            # function should have left any properties to set in the form
            # of a dictionary as the value of the net property 'DomainPagePropsToSet'.
            # If they're there, set them now.
            if self.PageContentCheckerFn != None: 
                props2Set = self.GetProperty('DomainPagePropsToSet')
                if props2Set:
                    domainItem.SetProperties(props2Set)
                    self.SetProperty('DomainPagePropsToSet', None)
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
            
    def RestoreOriginalUrlClass(self):
        """ 
        restore the Url-derived urlclass set when the instance was
        constructed.

        Returns the value of self.urlclass before it was changed (the "old"
        class).
        """
        log = Log('RestoreOriginalUrlClass')
        try:
            currentClass = self.urlclass
            if self.originalUrlClass != None and self.originalUrlClass != self.urlclass:
                self.urlclass = self.originalUrlClass
            return currentClass
        except Exception, e:
            self.SetLastError( 'in RestoreOriginalUrlClass, %s: %s' % (str(type(e)), str(e))  )
            return self.urlclass
            
    def SetNewUrlClass(self,newClass):
        """ 
        replace the current Url-derived urlclass set with a new class.

        Note: pass the name of the class without trailing parentheses!
        
        For example:
        
        net.SetNewUrlClass(urlnet.regexqueryurl.RegexQueryUrl)
        
        Returns the value of self.urlclass before it was changed (the "old"
        class).
        """
        log = Log('RestoreOriginalUrlClass')
        try:
            currentClass = self.urlclass
            if newClass != self.urlclass:
                self.urlclass = newClass
            return currentClass
        except Exception, e:
            self.SetLastError( 'in SetNewUrlClass, %s: %s' % (str(type(e)), str(e))  )
            return self.urlclass
            
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
                        if self.ignorableTextSearchArgs == NO_REGEX:
                            if text in url:
                                return None
                        else:
                            if re.search(text, url, self.ignorableTextSearchArgs):
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
                log.Write('item without level encountered: %s' % item.GetName())
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
 
    def MapFunctionToUniqueParentChildPairs(self,functionToMap,args=None,passFreq=False):
        """
        map a function against each unique parent-child index pair for
        each item in network, in ascending index order for parent.
        The mapper function must take 4 or 5 arguments:
            parentItemIdx:  index of current parent self.netitemclass
            childItemIdx:   index of current child item
            frequency:      if passFreq is True when this function is called,
                            it will pass the number of links extant between
                            parent and child.
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
                if passFreq:
                    doContinue = functionToMap(parentIdx, childIdx, children[childIdx], self, args)
                else:
                    doContinue = functionToMap(parentIdx, childIdx, self, args)
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
                log.Write('item without level encountered: %s' % item.GetName())
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
 
    def MapFunctionToUniqueDomainParentChildPairs(self,functionToMap,args=None,passFreq=False):
        """
        map a function against each the parent-child index pairs for
        each item in network, in ascending index order for parent.
        The mapper function must take 5 arguments:
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
                try:
                    count = children[childIdx]
                    children[childIdx] = count + 1
                except Exception, e:
                    children[childIdx] = 1

            keys = children.keys()
            keys.sort()
            for childIdx in keys:
                if passFreq:
                    doContinue = functionToMap(parentIdx, childIdx, children[childIdx], self, args)
                else:
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
                                            fd=stream,
                                            partitionName=partitionName,
                                            propertyName=propertyName,
                                            dict=valueDict,
                                            doDomains=(urlNet == False) )
            else:
                self.WritePajekPartitionFromPropertyValueLookup(
                                            fd=stream,
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
            reverseDirection = self.GetProperty('reverseArcOrEdgeDirection')
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
                    
                stream.write('\n\n*Partition URLLevels\n*Vertices ' + str(maxIdx) + ' \n')
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

                # process additional URL attributes, if any
                additionalUrlAttrs = self.GetProperty('additionalUrlAttrs')
                if additionalUrlAttrs != None:
                    for theDict in additionalUrlAttrs:
                        outputName = theDict['PorVName']
                        attrName = theDict['attrName']
                        generatePartition = theDict['doPartition']
                        if 'default' in theDict.keys():
                            default = theDict['default']
                        elif generatePartition:
                            default = UrlTree.PAJEK_NULL_PARTITION
                        else:
                            default = 0.0
                        if 'dict' in theDict.keys() \
                                    and generatePartition == True:
                            dictionary = theDict['dict']
                        else:
                            dictionary = None
                        if generatePartition:
                            # write partition
                            if dictionary:
                                self.WritePajekPartitionFromPropertyDict(
                                                fd=stream,
                                                partitionName=outputName, 
                                                propertyName=attrName, 
                                                dict=dictionary,
                                                defaultPartitionNumber=default,
                                                doDomains=False)
                            else:
                                self.WritePajekPartitionFromPropertyValueLookup(
                                                fd=stream,
                                                partitionName=outputName, 
                                                propertyName=attrName, 
                                                defaultPartitionNumber=default,
                                                doDomains=False)
                        else:
                            # write vector
                            self.WritePajekVectorFromPropertyValueLookup(
                                                stream,
                                                vectorName=outputName,
                                                propertyName=attrName,
                                                defaultVectorValue=default,
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
                    
                stream.write('\n\n*Partition DomainLevels\n*Vertices ' + str(maxIdx) + ' \n')
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

                # process additional domain attributes, if any
                additionalDomainAttrs = self.GetProperty('additionalDomainAttrs')
                if additionalDomainAttrs != None:
                    for theDict in additionalDomainAttrs:
                        outputName = theDict['PorVName']
                        attrName = theDict['attrName']
                        generatePartition = theDict['doPartition']
                        if 'default' in theDict.keys():
                            default = theDict['default']
                        elif generatePartition:
                            default = UrlTree.PAJEK_NULL_PARTITION
                        else:
                            default = 0.0
                        if 'dict' in theDict.keys() \
                                    and generatePartition == True:
                            dictionary = theDict['dict']
                        else:
                            dictionary = None
                        if generatePartition:
                            # write partition
                            if dictionary:
                                self.WritePajekPartitionFromPropertyDict(
                                                fd=stream,
                                                partitionName=outputName, 
                                                propertyName=attrName, 
                                                dict=dictionary,
                                                defaultPartitionNumber=default,
                                                doDomains=True)
                            else:
                                self.WritePajekPartitionFromPropertyValueLookup(
                                                fd=stream,
                                                partitionName=outputName, 
                                                propertyName=attrName, 
                                                defaultPartitionNumber=default,
                                                doDomains=True)
                        else:
                            # write vector
                            self.WritePajekVectorFromPropertyValueLookup(
                                                stream,
                                                vectorName=outputName,
                                                propertyName=attrName,
                                                defaultVectorValue=default,
                                                doDomains=True)

        except Exception, e:
            self.SetLastError('In WritePajekStream: ' + str(e))
            log.Write('In WritePajekStream: ' + str(e))
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

    def WritePajekVectorFromPropertyValueLookup(self,fd,vectorName, \
                propertyName, defaultVectorValue,doDomains = False):
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
            fd.write('\n\n')
                
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
                if present, additionalUrlAttrs property value must be a list containing a dictionary 
                for each additional attribute. In each dictionary, there must be two entries, 
                'attrName' and 'datatype'. The value of the attrName entry must be a legal Java  
                variable name, and the value of the datatype entry must be one of the constants
                CHAR, VARCHAR, DATE, TIME, DATETIME, BOOLEAN, INT, FLOAT, DOUBLE, BIGINT, or TINYINT; the
                name of the type should of course be a string.
                
                attrName should be a property on each URlNetItem instance in the network.  The entry can 
                optionally contain another entry 'default' whose value is a default to use if an item does 
                not have the property. For example:
                    
                IF the network's additionalUrlAttrs property contains 
                
                    [{'attrName' : 'pos_prob', 'datatype' : 'DOUBLE',},]

                THEN each item should have a property named 'pos_prob' whose value is a double float.
                
                """
                additionalUrlAttrs = self.GetProperty('additionalUrlAttrs')
                if additionalUrlAttrs != None:
                    for theDict in additionalUrlAttrs:
                        attrName = theDict['attrName']
                        attrType = theDict['datatype']
                        nodedef = '%s, %s %s' % (nodedef, attrName, attrType)
                stream.write(nodedef + '\n')
                maxIdx = len(self.UrlNetItemByIndex.keys())
                # write vertices by mapping a function to each item in the list
                    
                self.MapFunctionToUrlItemList(functionToMap=WriteGuessVertex,args=(stream,useTitles,additionalUrlAttrs))

                # write arcs by mapping a function to each parent-child pair in the list.
                stream.write(edgedef + '\n')
                self.MapFunctionToUniqueParentChildPairs(functionToMap=WriteGuessArc,
                                                         args=(stream,reverseDirection),
                                                         passFreq=True)
            else:
                additionalDomainAttrs = self.GetProperty('additionalDomainAttrs')
                if additionalDomainAttrs != None:
                    for theDict in additionalDomainAttrs:
                        attrName = theDict['attrName']
                        attrType = theDict['datatype']
                        domainNodedef = '%s, %s %s' % (domainNodedef, attrName, attrType)
                stream.write(domainNodedef + '\n')
                maxIdx = len(self.DomainByIndex.keys())

                # write vertices by mapping a function to each item in the list
                
                self.MapFunctionToDomainItemList(functionToMap=WriteGuessDomainVertex,args=(stream,additionalDomainAttrs))

                # write arcs by mapping a function to each parent-child pair in the list.
                stream.write(edgedef + '\n')
                self.MapFunctionToUniqueDomainParentChildPairs(functionToMap=WriteGuessDomainArc,
                     args=(stream,reverseDirection),
                     passFreq=True)
 
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
        

    def SetTruncatableText(self,listOfStrings, searchArgs=NO_REGEX):
        self.truncatableText = listOfStrings
        self.truncatableTextSearchArgs = searchArgs
    

    def GetTruncatableText(self):
        return self.truncatableText


    def SetIgnorableText(self,listOfStrings, searchArgs=NO_REGEX):
        self.ignorableText = listOfStrings
        self.ignorableTextSearchArgs = searchArgs
    

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
    
