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

from urllib import unquote
from urllib import urlopen
from urllib import urlencode
from urlparse import *
from url import Url
from log import Log
from ncbipubmedurl import NCBIPubMedUrl

#################### the NCBIUrl class ######################
class NCBICoAuthorUrl(NCBIPubMedUrl):
    "A class to get a list of co-authors from Pub Med "
    key = None
    limit = 10
    root = None
    url = None
    methodPrefix = None
    base = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    tool = 'UrlNet Python Library'
    
    def __init__(self, _inboundUrl, _network=None, limit=None, start=1):
        """constructor can take a url and init (a flag).
        If init is true, get page and anchors for url
        during construction. Get errors occurring in constructor
        by calling lastError().
        """
        
        # Don't allow a GetPage call in the Url ctor - it would
        # waste time, because we do our own GetPage later, with
        # the NCBI CoAuthor version of GetAnchorList
        
        log = Log('NCBICoAuthorUrl ctor',_inboundUrl)
        NCBIPubMedUrl.__init__(self,_inboundUrl=_inboundUrl,_network=_network,limit=limit, start=1)
        
        

    def GetAnchorList(self):
        """
        Overriding the same function in the Url class.
        """
        log = Log('GetAnchorList')
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
                self.anchors = self.GetCoAuthorList(self.url)
                return self.anchors
                    
            except Exception, inst:
                self.SetLastError( 'GetAnchorList' + ": " + str(type(inst)) + '\n' + self.url )
                return []

def main():
    from object import Object
    import log
    workingDir =urlutils.GetConfigValue('workingDir')
    log.logging = True
    log.trace = True
    log.altfd = open(os.path.join(workingDir,'log.txt'),'w')
    myLog = log.Log('main')
    testnet = Object()
    testnet.SetProperty('email','dalehuns@umich.edu')
    testnet.SetProperty('sleeptime',3)
    testnet.SetProperty('NCBIResultSetSizeLimit',10)
    x = NCBICoAuthorUrl('Omenn GS',_network=testnet)
    for a in x.GetUrlAnchors():
        print a
    print x.GetLastError()
    log.altfd.close()
    log.altfd=None
    

if __name__ == '__main__':
    main()
    exit(0)
