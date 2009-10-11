#!/usr/bin/env python
# $Id$

from log import Log
from tldconstants import *
from urlparse import urlparse

def GetUrlTLD(net,url):
    """ get the URL's top-level domain type and return 
        it in lowercase.
    """
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
        TLDExceptions = net.GetProperty('TLDExceptions')
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
    
    
def IsForProfitUrlTLD(net,url,returnBoolean = True):
    """ By default, return True if the TLD applies to for-profit 
    entities (e.g.,  com and net), False if TLD applies to non-profit 
    or is unknown. If returnBoolean is False, return 1 for True and
    0 (zero) for False.
    """
    log = Log('IsForProfitUrlTLD',url)

    try:
        isForProfit = urlTypeForProfitConstants[GetUrlTLD(net,url)]
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

def GetUrlTLDConstants(net,url):
    """ Return a sequence containing two values: an integer constant 
        representing the type of TLD in the URL, and a float constant
        for use in vectors, representing the library creator's rather
        arbitrary assessment of the relative value of the TLD type.
        Constants are defined in urlutils.py.
    """
    log = Log('GetUrlTLDConstants',url)
    try:
        tld = GetUrlTLD(net,url)
        return urlTypeConstants[tld]
    except Exception, e:
        log.Write('%s in GetUrlTLDConstants: %s in %s' % (str(e), str(tld), str(url)) )
        return (DOTUNK,V_DOTUNK)
    
    
    
def KeepTLDFilteredUrl(net, url):
    log = Log('IgnoreFilteredUrl',url)    
    try:
        """
        # filter based on top-level domains (TLDs) or categories under country codes
        
        Return False if the url should be ignored, True otherwise.
        
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
        
        filterlist = net.GetProperty('filterToKeep')
        if filterlist != None:
            try:
                filterlist = filterlist[0]
                urlType = GetUrlTLD(net,url)
                if urlType == 'com':
                    pass
                # strip off country codes
                if len(urlType[-1]) == 2:
                    urlType = urlType[-2].lower()
                else:
                    urlType = urlType[-1].lower()
                # keep url if its TLD is in filterlist; otherwise
                # omit URL (and its descendants) from network
                if urlType in filterlist:
                    return True # keep URL
                else:
                    return False # omit
                     
            except Exception, e:
                # keep the weird ones
                return True
                    
        return True
    
    except Exception, e:
        # keep the weird ones
        return True
            
        
def SetUrlTLDProperties(net,item,urlToAdd):
    """ If the program has set the TrackTLDProperties property to True,
        set the URL item's TLD properties. These include:
        
        urlTLD: the url's top-level domain.
        urlTLDVector: a value indicating (in the library author's
            arbitrary opinion) the relative value of this type of
            TLD.
        forProfitUrlTLD: True if url is probably for-profit, else set
            to False.
            
        This function also happens to work for domain items.
        """
    log = Log('SetUrlTLDProperties',urlToAdd)
    try:
        tldConstants = GetUrlTLDConstants(net,urlToAdd)
        item.SetProperty('urlTLD',tldConstants[0])
        item.SetProperty('urlTLDVector',tldConstants[1])
        item.SetProperty('forProfitUrlTLD',
            IsForProfitUrlTLD(net,urlToAdd,returnBoolean = False))
    except Exception, e:
        log.Write('in SetUrlTLDProperties( ' + str(urlToAdd) + ' ): ' + str(e))
        return
    
