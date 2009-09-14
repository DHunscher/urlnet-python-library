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

import re
import string
import sys
import os

from urllib import unquote
from urllib import urlopen
from urllib import urlencode
from urlparse import *
from url import Url
from log import Log
from ncbipubmedurl import NCBIPubMedUrl

#################### the NCBIUrl class ######################
class NCBIAuthorCosmosUrl(NCBIPubMedUrl):
    "A class to get the pubs, co-authors, and MeSH terms associated with an author from Pub Med "
    key = None
    limit = 10
    root = None
    url = None
    methodPrefix = None
    base = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    tool = 'UrlNet Python Library'
    pubdict = None
    
    def __init__(self, _inboundUrl, _network=None, limit=None, start=1):
        """constructor can take a url and init (a flag).
        If init is true, get page and anchors for url
        during construction. Get errors occurring in constructor
        by calling lastError().
        """
        
        # Don't allow a GetPage call in the Url ctor - it would
        # waste time, because we do our own GetPage later, with
        # the NCBI CoAuthor version of GetAnchorList
        
        log = Log('NCBIAuthorCosmosUrl ctor',_inboundUrl)
        NCBIPubMedUrl.__init__(self,_inboundUrl=_inboundUrl,_network=_network,limit=limit, start=1)
        pubdict = {}
        
    def GetUrlAnchors(self):
        raise Exception, 'GetUrlAnchors not supported in NCBIAuthorCosmosUrl'

    def GetAnchorList(self):
        raise Exception, 'GetAnchorList not supported in NCBIAuthorCosmosUrl'
        
    def GetPubs(self):
        """
        Returns a dictionary whose keys are pub titles; each title accesses a nested dictionary containing the
        PubMed ID (key to retrieve is 'pmid') and lists of co-authors (key is 'authorlist') and MeSH terms (key is
        'meshlist').
        """
        log = Log('GetPubs')
        #print "00"
        if self.url == None:
            #print "01"
            return {}
        elif self.pubdict != None:
            #print "02"
            return self.pubdict
        else:
            #print "03"
            try:
                self.pubdict = self.GetPublications(self.url)
                return self.pubdict
                    
            except Exception, inst:
                self.SetLastError( 'GetPubs: ' + str(type(inst)) + '\n' + self.url )
                return {}

    def GetPubTitles(self):
        """
        This function should be used to drive iteration, since it guarantees the pubdict
        member will  be populated, and provides the titles that can be used to call
        GetCoAuthors() and GetMeSHTerms().
        """
        log = Log('GetPubTitles')
        for title in self.GetPubs().keys():
            yield (title,self.pubdict[title]['pmid'])

    def GetPub(self,title):
        """
        Get the dictionary entry for a title. It contains the title's PM ID and
        lists of co-authors and MeSH terms.
        """
        log = Log('GetPub')
        try:
            return self.pubdict[title]
        except Exception, inst:
            self.SetLastError( 'GetPub: ' + str(type(inst)) + '\n' + self.url )
            return None

    def GetCoAuthors(self,title):
        """
        Get the list of co-authors for a title.
        """
        log = Log('GetCoAuthors')
        try:
            return self.pubdict[title]['authorlist']
        except Exception, inst:
            self.SetLastError( 'GetCoAuthors: ' + str(type(inst)) + '\n' + self.url )
            return None

    def GetMeSHTerms(self,title):
        """
        Get the list of MeSH terms for a title.
        """
        log = Log('GetMeSHTerms')
        try:
            return self.pubdict[title]['meshlist']
        except Exception, inst:
            self.SetLastError( 'GetMeSHTerms: ' + str(type(inst)) + '\n' + self.url )
            return None



        
def main():
    from object import Object
    import log
    workingDir =urlutils.GetConfigValue('workingDir')
    log.logging = True
    log.trace = False
    log.altfd = open(os.path.join(workingDir,'log.txt'),'w')
    myLog = log.Log('main')
    testnet = Object()
    testnet.SetProperty('email','dalehuns@umich.edu')
    testnet.SetProperty('sleeptime',3)
    testnet.SetProperty('NCBIResultSetSizeLimit',10)
    x = NCBIAuthorCosmosUrl('Hunscher DA',_network=testnet)
    for (title, pmid) in x.GetPubTitles():
        print title
        print pmid
        print 'Co-Authors:'
        for coAuthor in x.GetCoAuthors(title):
            print '\t%s' % (coAuthor)
        print 'MeSH Terms:'
        for term in x.GetMeSHTerms(title):
            print '\t%s' % (term)

    log.altfd.close()
    log.altfd=None
    

if __name__ == '__main__':
    main()
    exit(0)
