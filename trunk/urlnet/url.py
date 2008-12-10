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

import re
import string
import sys
import os
import time

from urllib import unquote
from urllib2 import urlopen, Request
from urllib import urlencode
from urlparse import *
from htmllib import HTMLParser
from formatter import NullFormatter
from object import Object
from log import Log


# module-level function
def DomainFromHostName(host):
    """
    Given an Internet hostname (e.g., www.msis.med.umich.edu) return the
    domain name (e.g., umich.edu).
    """
    ct = 0
    start = 0
    international = False
    limit = 2
    if host:
        if 'javascript' in host:
            return 'host is javascript call'
        if host[-3] == '.': # international url, e.g. bbc.co.uk
            international = True
            limit = 3
        for i in range(len(host)-1,-1,-1):
            if host[i] == '.':
                ct = ct + 1
            if ct == limit:
                start = i + 1
                break
    else:
        sys.stderr.write('*** NULL HOST ***\n')
        return host
    return host[start:]

#################### the Url class #########################
class Url(Object):
    """
    A class to wrap WWW URLs. Knows:
    1) Its url parts
    2) its domain
    4) its raw page
    n) how to enumerate its child urls
    Later
    n+1) return an Html DOM Tree
    n+2) enumerate child urls filtered:
        a) by ignoring child urls containing any of a list of embedded text fragments
        b) by removing prefixes
        c) by use of some reg expression
        
    """
    url = None
    pathOnly = None
    myHost = None    
    domainOnly = None
    page = ''
    page_lower = ''
    anchors = None
    parts = None
    includeMethod = False
    maxLength = 65535
    network = None
    sleeptime = 0
    user_agent = None
    req_headers = None
    last_query = None
    last_successful_query = None
    
    def __init__(self, _inboundUrl, _network=None, _includeMethod = False, \
                 _maxLength = 65535, _doInit=False):
        """constructor takes a url, and two optional used in GetTruncatedUrl().
        Get errors occurring in constructor
        by calling GetLastError(), inherited from Object.
        """
        log = Log('Url constructor')
        Object.__init__(self)
        self.url = None
        self.pathOnly = None
        self.myHost = None
        self.domainOnly = None
        self.anchors = None
        self.parts = None
        self.includeMethod = _includeMethod
        self.maxLength = _maxLength
        self.anchors = None
        self.network=_network
        self.sleeptime = self.network.GetProperty('sleeptime')
        if self.sleeptime:
            try:
                self.sleeptime = float(self.sleeptime)
            except Exception, e:
                log.Write('for self.sleeptime in Url constructor, can\'t convert "' + str(self.sleeptime) + '" into float')
                self.sleeptime = 0.0
        else:
            self.sleeptime = 0.0
        self.user_agent = self.network.GetProperty('user-agent')
        self.req_headers = self.network.GetProperty('request-headers')
        self.last_query = None
        self.last_successful_query = None
        if self.req_headers == None:
            self.req_headers = {}
        if 'User-Agent' not in self.req_headers.keys():
            if self.user_agent:
                self.req_headers['User-Agent'] = self.user_agent
            else:
                self.req_headers['User-Agent'] = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT; UrlNet Python Library;'
                
        try:
            self.url = _inboundUrl
            parts = self.GetUrlParts()
            if not parts or parts[0] == '':
                self.url = 'http://' + self.url
            self.Init(_doInit)
        except Exception, e:
            self.SetLastError ( str(e) )
    
    def Init(self,doInit): 
        """
        Initialize the object
        """
        log = Log('Init')
        self.ResetLastError()
        try:
            self.pathOnly = self.GetTruncatedUrl()
            parts = self.GetUrlParts()
            host = parts.hostname
            if not host:
                host = 'No host in %s' % (str(self.url))
            # remove trailing slash(es), if present
            while host[-1:] == '/':
                host = host[:-1]
            self.myHost = host
            self.domainOnly = DomainFromHostName(self.myHost)

            if doInit:
                self.GetPage()
        except Exception, e:
            self.SetLastError( 'Init: ' + str(e) + '\n\url: << ' + self.url + ' >>' )

    def GetUrl(self):
        """ returns the URL used to create this object instance. """
        return self.url

    def GetDomain(self):
        """ returns the domain of this item (e.g., google.com) """
        return self.domainOnly
    
    def GetHost(self):
        """ returns the qualified host of this item (e.g., groups.google.com) """
        return self.myHost

    def GetLastQuery(self):
        """ returns last query for which a urlopen was attempted
        """
        return self.last_query

    def GetLastSuccessfulQuery(self):
        """ returns last query that was successfully opened and read
        """
        return self.last_successful_query

    
    def RetrieveUrlContent(self,theUrl=None,getTitleOnly=False):
        """
        Get page from the current url. Handles the need for sleep if we are
        being polite. Returns a string containing what the url GET retrieves.
        """
        log = Log('RetrieveUrlContent',theUrl)
        self.ResetLastError()
        if theUrl == None:
            theUrl = self.url
            
        try:
            tries = 0
            originalUrl=theUrl
            while(1):
                if self.req_headers:
                    req = Request(url=theUrl,headers=self.req_headers)
                else:
                    req = Request(theUrl)
                self.last_query = theUrl
                urlobject = urlopen(req)
                getTitles = self.network.GetProperty('getTitles')
                if (getTitles == False or getTitles == None) and getTitleOnly:
                    return theUrl
                if getTitleOnly and getTitles:
                    # don't get the whole thing, just enough to be sure to get the title,
                    # if there is a <title> element in the <head> element.
                    page = urlobject.read(2000)
                else:
                    page = urlobject.read()
                # handle Javascript redirects, which are not handled by the httplib2 mechanism
                # This is a KLUDGE!!!
                if 'redirect' in page.lower():
                    redirs = re.findall('window.location.replace\s*?\(\s*?[\'"](.*?)[\'"]\s*?\)',page)
                    if len(redirs) > 0:
                        pass
                    else:
                        redirs = re.findall('window.location.href\s*?\=\s*?[\'"](.*?)[\'"]',page)
                    if len(redirs) > 0:
                        if tries < 5: # a MAGIC NUMBER!!!
                            tries = tries + 1
                            theUrl = redirs[0]
                            continue
                        else:
                            raise Exception,'Too many redirect tries (5) on url ' + str(originalUrl)
                    else:
                        break
                else:
                    break
            urlobject.close()
            self.last_successful_query = theUrl
            if self.sleeptime:
                time.sleep(float(self.sleeptime))
            # if the page has a title, get it now
            # set a property for the title to either the title (if any),
            #   or the url if no title
            if getTitles:
                if len(page) > 0:
                    t = re.findall('<title>(.*?)</title>',page,re.I|re.S)
                    if len(t) > 0:
                        title = t[0]
                    else:
                        title = theUrl
                else:
                    title = theUrl
                self.SetProperty('title',title)
            else:
                title = theUrl
            if getTitleOnly:
                return title
            return page
        except Exception, inst:
            self.SetLastError ( 'RetrieveUrlContent: ' + str(type(inst)) + '\n' + str(inst) + '\non URL ' + theUrl )
            return ''

    def GetPage(self):
        """
        Retrieve the page pointed to by the url. Returns None if error occurs;
        get error text by calling GetLastError().
        """
        log = Log('GetPage')
        #sys.stderr.write('in GetPage\n')
            
        page = ''
        self.anchors = None
        parts = urlparse(self.url)
        if ( len(parts[0]) == 0 ):
            self.url = 'http://' + self.url
        try:
            #sys.stderr.write('GetPage: ' + self.url + '\n')
            page = self.RetrieveUrlContent()
            #sys.stderr.write('GetPage: opened\n')
            #sys.stderr.write('GetPage: closed\n')
            #sys.stderr.write(self.page + '\n')
            if page:
                page_lower = page.lower()
                if 'object moved' in page_lower or ('404' in page_lower \
                                                         and 'not found' in page_lower):
                    self.SetLastError ( 'url ' + self.url + ' not found.\n' )
                    return None
                elif 'meta http-equiv="refresh"' in page_lower and not ('no-cache' in page_lower):
                    self.SetLastError ( 'url ' + self.url + ' redirected.\n' )
                    return None
                else:
                    return page
            else:
                return None
        except Exception, inst:
            self.SetLastError ( 'GetPage: ' + str(type(inst)) + '\n' + str(inst) + '\non URL ' + self.url )
            return False

    def GetUrlParts(self):
        """
        Get the parts of the URL as defined in urlparse.urlparse.
        """
        u = urlparse(self.url)
        return u
    
    def GetTruncatedUrl(self, includeMethod = False, maxLength = 65535):
        """ return just the domain and page parts of the url,
              optionally prefixed with the method (http, ftp, etc.)
              and optionally truncated to a maximum length, in which case
                the last three characters are removed and an ellipsis is
                appended
        """
        log = Log('GetTruncatedUrl')
        parts = self.GetUrlParts()
        #sys.stderr.write('***reduceToPath***\n' + str(parts) + '\n')
        truncatedUrl = parts[1] + parts[2]
        if includeMethod and len(parts[0]) > 0:
            truncatedUrl = parts[0] + '//' + truncatedUrl
        if maxLength < 65535 and len(truncatedUrl) > maxLength:
            truncatedUrl = truncatedUrl[0:maxLength-3] + '...'
        return truncatedUrl

    def GetUrlAnchors(self):
        """
        Yields the hrefs found in the document, e.g., for use in 'for' statement.
        """
        log = Log('GetUrlAnchors')
        #print "00"
        self.ResetLastError()

        for anchor in self.GetAnchorList():
                yield anchor

    def GetPDFAnchorList(self,page):
        """ get list of URI references in PDF document.
        """
        log = Log('GetPDFAnchorList')
        self.ResetLastError()
        try:
            if '\r\n' in page[0:20]:
                lines = page.split('\r\n')
            else:
                lines = page.split('\n')
            #print 'number of lines: ' + str(len(lines))
            signature = lines[0][0:5]
            #print bytes[-1000:]
            if signature != '%PDF-':
                self.SetLastError( 'not a pdf document' )
                return []
            regex = '/URI\((.*)\)'
            p = re.compile(regex)
            self.anchors = []
            for line in lines:
                anchor = p.search(line)
                if anchor:
                    self.anchors.append(anchor.re.findall(anchor.group(0))[0])
            return self.anchors
                 
        except Exception, inst:
            self.SetLastError( 'GetPDFAnchorList: ' + str(type(inst)) + '\n' + self.url )
            return []
        
    def GetAnchorList(self):
        """
        Return the list of anchors (urls in the 'href' attributes
        found in 'a' elements in the document).
        """
        log = Log('GetAnchorList')
        self.ResetLastError()
        try:
            page = self.GetPage()
            if not page:
                return []

            # save the current page as a network property, if so desired
            # (e.g., to do NLP on it)
            save_page_as_property_value = self.network.GetProperty('save_page_as_property_value')
            if save_page_as_property_value:
                self.network.SetProperty('current_page',page)
                
            if page[0:5] == '%PDF-':
                return self.GetPDFAnchorList(page)
            # parse to Get the href
            parser = HTMLParser(NullFormatter())
            parser.feed(page)
            self.anchors = parser.anchorlist
            return self.anchors
                 
        except Exception, inst:
            self.SetLastError( 'GetAnchorList: ' + str(type(inst)) + '\n' + self.url )
            return []

def main():
    import log
    import urlutils
    log.logging = True
    log = Log('main')
    import os
    os.chdir(urlutils.GetConfigValue('workingDir'))
    print "***testing constructor/n"
    net = Object() # for getproperty
    net.SetProperty('sleeptime',5)
    if False:
        #u = Url('http://www.google.com/',_network = net)
        u = Url('http://www.google.com/',_network = net)
        print 'error, if any: ' + u.GetLastError()
        print "\n\n*** testing anchor list functions\n"
        for href in u.GetUrlAnchors():
            print href
        print 'error, if any: ' + u.GetLastError()
        pg = u.GetPage()
        print 'error, if any: ' + u.GetLastError()
       
    if True:
        # test a Javascript redirect
        u = Url('http://www.cdc.gov/tobacco/how2quit.htm',_network = net)
        print 'error, if any: ' + u.GetLastError()
        print "\n\n*** testing PDF anchor list\n"
        for href in u.GetUrlAnchors():
            print href
        print 'error, if any: ' + u.GetLastError()
        print u.GetDomain()
        print u.GetHost()
    
    if False:
            
        print DomainFromHostName('ftp://www.edgar.org')
        print DomainFromHostName('javascript:void(0)')
        print DomainFromHostName('bob.com')
        print DomainFromHostName('www.bbc.co.uk')
        print DomainFromHostName('bbc.co.uk')
        print DomainFromHostName(None)

       
    

if __name__=='__main__':
    main()
