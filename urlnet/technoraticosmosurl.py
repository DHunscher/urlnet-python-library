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
from Ft.Xml import InputSource, Sax

#################### the TechnoratiUrl class ######################
class TechnoratiCosmosUrl(Url):
    "A class to wrap Technorati's Cosmos RESTful Web Service (http://api.technorati.com) "
    key = None
    limit = 10
    root = None
    url = None
    methodPrefix = None
    
    def __init__(self, _inboundUrl, _network=None, limit=20, start=1):
        """constructor can take a url and init (a flag).
        If init is true, get page and anchors for url
        during construction. Get errors occurring in constructor
        by calling lastError().
        """
        
        # Don't allow a GetPage call in the Url ctor - it would
        # waste time, because we do our own GetPage later, with
        # the technorati cosmos version of GetAnchorList
        
        log = Log('TechnoratiUrl ctor',_inboundUrl)
        Url.__init__(self,_inboundUrl=_inboundUrl,_network=_network,_doInit=False)
        
        self.root = _inboundUrl
        parts = urlparse(self.root)
        self.root = parts[1] + parts[2] + parts[3] + parts[4] + parts[5]
        self.methodPrefix = parts[0]
        
        if _network:
            self.key = _network.GetProperty('technoratiKey')
        else:
            self.SetLastError('NO TECHNORATI KEY')
            self.key = None
        self.limit = limit
        self.start = start
        self.anchors = None
        self.url = _inboundUrl
        
    def GetTapiTree(self):
        log = Log('GetTapiTree')
        """
            GetTapiTree uses the inherited URL as the root of a Technorati 
            URL that is constructed on-the-fly for use as the URL to fetch 
            via the inherited GetPage function. The page is an XML document

            Returns a dictionary with a single entry, having the inherited
            URL as the key and a list of inlinking URLs as the value
        """
        

        class tapi_processor:
            def startDocument(self):
                self.in_result = False
                self.in_item = False
                self.in_error = False
                self.itemList = []
                self.tapiTree = {}
                self.nodeUrl = ''
                self.error = ''

            def startElementNS(self, name, qname, attribs):
                if unicode(name[1]) == u'error':
                    self.in_error = True
                    self.error = ''
                elif unicode(name[1]) == u'result':
                    self.in_result = True
                    self.url = ''
                elif unicode(name[1]) == u'item':
                    self.in_item = True
                    self.url = ''
                elif self.in_result:
                    if unicode(name[1]) == u'url':
                        self.in_url = True
                        self.url = ''
                elif self.in_item:
                    if unicode(name[1]) == u'url':
                        self.in_url = True
                        self.url = ''
                return

            def endElementNS(self, name, qname):
                if unicode(name[1]) == u'error':
                    self.tapiTree[u'error'] = self.error
                    self.error = ''
                elif unicode(name[1]) == u'url':
                    if self.in_result :
                        self.in_result = False
                        self.nodeUrl = self.url
                        self.url = ''
                    elif self.in_item :
                        self.in_item = False
                        self.itemList.append( self.url )
                        self.url = ''

            def characters(self, text):
                if self.in_result or self.in_item:
                    self.url = self.url + text
                elif self.in_error:
                    self.error = self.error + text

            def ignorableWhitespace(self, ws):
                return

            def endDocument(self):
                self.tapiTree[self.nodeUrl] = self.itemList

        # first get the data        
        prefix = 'http://api.technorati.com/cosmos?'
        args = {'key' : self.key, 'url' : self.root, 'limit' : str(self.limit),
                'start' : str(self.start), 'type' : 'link', 'format' : 'xml',}
        suffix = urlencode(args)
        self.url = prefix + suffix
        page = self.GetPage()

        # next parse using SAX
        try:
            import xml
            self.ResetLastError()
            factory = InputSource.DefaultFactory
            isrc = factory.fromString(page)
            parser = Sax.CreateParser()
            handler = tapi_processor()
            parser.setFeature(xml.sax.handler.feature_validation, False)
            parser.setContentHandler(handler)
            parser.parse(isrc)
            return handler.tapiTree
        except Exception, e:
            self.SetLastError( e )
            return None

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
                # parse to get the href
                #
                tree = self.GetTapiTree()
                lookupUrl = self.methodPrefix + '://' + self.root

                # check for errors
                error = None
                if u'error' in tree.keys():
                    raise Exception, tree[u'error']

                # no error, so proceed
                treelist = tree[lookupUrl]
                self.anchors = treelist
                return self.anchors
                    
            except Exception, inst:
                self.SetLastError( 'GetAnchorList' + ": " + str(type(inst)) + '\n' + self.url )
                return []

def main():
    from object import Object
    from log import Log
    testnet = Object()
    technoratiKey = '13083c881893e0023f4a6f6e42d8c770'
    testnet.SetProperty('technoratiKey',technoratiKey)
    testnet.SetProperty('sleeptime',1)
    x = TechnoratiCosmosUrl('http://hunscher.typepad.com/',_network=testnet)
    #tree = x.GetTapiTree()
    #print str(tree)
    for a in x.GetUrlAnchors():
        print a
    print x.GetLastError()

if __name__ == '__main__':
    main()
    sys.exit(0)
    