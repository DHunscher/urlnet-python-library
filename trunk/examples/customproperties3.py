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
'''
Demonstrate the use of custom properties.
'''
from urlnet.log import Log
from urlnet.topleveldomainutils import SetUrlTLDProperties
from urlnet.yahootree import YahooTree

from urlnet.ignoreandtruncate import textToIgnore, textToTruncate

import urlnet.log
import re


def main():

    
    tldExceptions = { 
        'smoking-cessation.org': 'fake', 
        'whyquit.com' : 'org',
        'quitsmokingnaturally.org' : 'fake',
        'stopsmoking.org' : 'fake',
        'smokingreviews.org' : 'fake',
        'allthewebsites.org' : 'fake',
        'mayoclinic.com' : 'org',
        }
    try:
        urlnet.log.logging = True
        
        # Prepare to run a search query against the Yahoo search engine.
        
        net = YahooTree(_maxLevel=1,
                       _resultLimit=10)
        #
        # tell the algorithm to call the function
        # urlnet.topleveldomainutils.SetUrlTLDProperties
        # to capture TLD properties.
        
        net.SetCustomUrlPropertiesFn(SetUrlTLDProperties)
        
        # The same custom properties setter works for domains; this
        # might not be the case for other applications.
        
        net.SetCustomDomainPropertiesFn(SetUrlTLDProperties)
        
        # TLDExceptions is a property used in the top-level domain algorithms;
        # if your custom functions need properties to be set, do
        # so here.
        
        net.SetProperty('TLDExceptions',tldExceptions)
        
        TLDPropertyDictList4Urls = \
            [
                {
                    'attrName'    : 'forProfitUrlTLD',
                    'PorVName'    : 'URL Net TLD For-Profit/Not-For-Profit', 
                    'doPartition' : True,
                },
                {
                    'attrName'    : 'urlTLD',
                    'PorVName'    : 'URL Net TLD Type', 
                    'doPartition' : True,
                },
                {
                    'attrName'    : 'urlTLDVector',
                    'PorVName'    : 'URL Net TLD Type', 
                    'doPartition' : False,
                },
            ]
            
        net.SetProperty('additionalUrlAttrs',TLDPropertyDictList4Urls)

        TLDPropertyDictList4Domains = \
            [
                {
                    'attrName'    : 'forProfitUrlTLD',
                    'PorVName'    : 'Domain Net TLD For-Profit/Not-For-Profit', 
                    'doPartition' : True,
                },
                {
                    'attrName'    : 'urlTLD',
                    'PorVName'    : 'Domain Net TLD Type', 
                    'doPartition' : True,
                },
                {
                    'attrName'    : 'urlTLDVector',
                    'PorVName'    : 'Domain Net TLD Type', 
                    'doPartition' : False,
                },
            ]

        
        net.SetProperty('additionalDomainAttrs',TLDPropertyDictList4Domains)
        
        # we can safely ignore a bunch of URLs that have to do
        # with marketing, Acrobat Reader, etc. We'll also ignore
        # truste.org, but we want to remove yahoo.com from the 
        # standard list.
        
        textToIgnore.append('truste.org')
        textToIgnore.remove('yahoo.com')
        net.SetIgnorableText(textToIgnore)
        #
        # Don't pursue links in Amazon, YouTube, etc.
        # 'truncate' means truncate the depth-first traversal here;
        # include matching URLs, but don't spider their outlinks
        # even if the max level hasn't yet been reached.
        
        net.SetTruncatableText(textToTruncate)        
        
        net.BuildUrlTreeWithPlaceholderRoot('http://search.yahoo.com/','quit smoking')
            
        net.WritePajekFile('customproperties2','customproperties2')
        
    except Exception,e:
        myLog.Write(str(e)+'\n on Yahoo quit smoking query\n')
        print str(e)
    

    
if __name__ == '__main__':
    main()
    #sys.exit(0)
