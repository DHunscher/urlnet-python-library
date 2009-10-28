#!/usr/bin/env python
# $Id: netsmerged2.py 82 2009-10-19 13:44:07Z dalehunscher $
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
# netsmerged2.py

import sys
import os
from os.path import join
import re

from urlnet.log import Log, logging, altfd
from urlnet.aoltree import AOLTree
from urlnet.urlutils import GetTimestampString, GetConfigValue
from urlnet.ignoreandtruncate import textToIgnore, textToTruncate
from urlnet.topleveldomainutils import SetUrlTLDProperties
import urlnet.log

# These two constants are the possible values for the 
# whichBuilder argument to main()
PLACEHOLDER = 'PLACEHOLDER'
PHANTOM = 'PHANTOM'

def main(whichBuilder):
    """
    We are going to make a subdirectory under
    the working directory that will be different each run.
    """

    baseDir = GetConfigValue('workingDir')
    # dir to write to
    timestamp = GetTimestampString()
    workingDir = join(baseDir,timestamp)

    oldDir = os.getcwd()
    goAhead = True

    query = None
    try:
        try:
            os.mkdir(workingDir)
        except Exception, e:
            pass # the dir already exists
        os.chdir(workingDir)
        myLog = Log('main')
        urlnet.log.logging=True
        #urlnet.log.trace=True
        urlnet.log.altfd=open('netsmerged2.log.txt','w')
    except Exception,e:
        myLog.Write(str(e)+'\n')
        goAhead = False
    try:
        tldExceptions = { 
            'smoking-cessation.org': 'fake', 
            'whyquit.com' : 'org',
            'quitsmokingnaturally.org' : 'fake',
            'stopsmoking.org' : 'fake',
            'smokingreviews.org' : 'fake',
            'allthewebsites.org' : 'fake',
            'mayoclinic.com' : 'org',
            }
            
        # combine 'quit smoking', 'stop smoking', and 'smoking cessation'
        # query result trees
        net = AOLTree(_maxLevel=1,
                        _workingDir=workingDir,
                        _resultLimit=10
                        )
                        
                        
        #
        # tell the builder algorithm to call the function
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
                    'default'     : 9999998,
                    'datatype'    : 'INT',
                },
                {
                    'attrName'    : 'urlTLD',
                    'PorVName'    : 'URL Net TLD Type', 
                    'doPartition' : True,
                    'default'     : 9999998,
                    'datatype'    : 'INT',
                },
                {
                    'attrName'    : 'urlTLDVector',
                    'PorVName'    : 'URL Net TLD Type', 
                    'doPartition' : False,
                    'default'     : 0.00001,
                    'datatype'    : 'DOUBLE',
                },
            ]
            
        net.SetProperty('additionalUrlAttrs',TLDPropertyDictList4Urls)

        TLDPropertyDictList4Domains = \
            [
                {
                    'attrName'    : 'forProfitUrlTLD',
                    'PorVName'    : 'Domain Net TLD For-Profit/Not-For-Profit', 
                    'doPartition' : True,
                    'default'     : 9999998,
                    'datatype'    : 'INT',
                },
                {
                    'attrName'    : 'urlTLD',
                    'PorVName'    : 'Domain Net TLD Type', 
                    'doPartition' : True,
                    'default'     : 9999998,
                    'datatype'    : 'INT',
                },
                {
                    'attrName'    : 'urlTLDVector',
                    'PorVName'    : 'Domain Net TLD Type', 
                    'doPartition' : False,
                    'default'     : 0.00001,
                    'datatype'    : 'DOUBLE',
                },
            ]

        
        net.SetProperty('additionalDomainAttrs',TLDPropertyDictList4Domains)
        
        # we can safely ignore a bunch of URLs that have to do
        # with marketing, Acrobat Reader, etc. We'll also ignore
        # truste.org, but we want to remove yahoo.com from the 
        # standard list.
        
        net.SetIgnorableText(textToIgnore)
        net.SetTruncatableText(textToTruncate)
        
        
        ret = True
        badQuery = None
        for query in ('quit smoking','stop smoking','smoking cessation'):
            # set a query filename root that tells us which builder method and query were used.
            net.SetFilenameFromQuery('netsmerged2-%s-%s' % (str(whichBuilder),query))

            # NOTE: the following line is crucial to making the merge work
            # as expected. Without it, the search URL is treated as an
            # ordinary URL and all links on that page are processed, not just
            # the links in the search results.
            
            net.RestoreOriginalUrlClass()
            
            root='http://search.aol.com/aol/search?s_it=comsearch40&query=%s&do=Search' % re.sub(' ','+',query)
            if whichBuilder == PLACEHOLDER:
                ret = net.BuildUrlTreeWithPlaceholderRoot(root,query)
            elif whichBuilder == PHANTOM:
                ret = net.BuildUrlForestWithPhantomRoot(query)
            else:
                goAhead = False
                break
            if not ret:
                badQuery = query
                break
            
        if goAhead == False:
            print 'main(whichBuilder) requires whichBuilder to be PHANTOM or PLACEHOLDER-nothing built.'
        elif not ret:
            print 'main(whichBuilder) %s builder function failed for query "%s".' % (whichBuilder, badQuery )
        else:
            qry = query
            query = 'done building net'
            netname = 'netsmerged2-%s' % str(whichBuilder)
            net.WritePajekFile(netname,netname)
            net.WriteGuessFile(netname, doUrlNetwork = True)
            net.WriteGuessFile(netname+'Domains', doUrlNetwork = False)

    except Exception,e:
        if query == None:
            myLog.Write(str(e)+'\n on constructor invocation\n')
        elif query == 'done building net':
            myLog.Write(str(e)+'\n during Pajek output file generation\n')
        else:
            myLog.Write(str(e)+'\n on ' + query + ' query\n')

        
    # tidy up
    if urlnet.log.altfd:
        urlnet.log.altfd.close()
        urlnet.log.altfd = None
        
    os.chdir(oldDir)
        
if __name__ == '__main__':
    # Uncomment to one of these to choose between 
    # net.BuildUrlForestWithPhantomRoot and net.BuildUrlTreeWithPlaceholderRoot
    
    # main(PHANTOM)
    main(PLACEHOLDER)
    print 'Complete!'
    
