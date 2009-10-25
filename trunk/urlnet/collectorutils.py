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
This is an experimental routine I am working on to make it easier to 
build analyses of reachability and findability of Medline Plus
pages from various search engines.
'''
from log import Log, logging, altfd
from urlutils import PrintHierarchy
import sys
from time import strftime, localtime
import os
from searchenginetree import computeDescendingStraightLineProbabilityVector,\
                                    computeEqualProbabilityVector
from ignoreandtruncate import textToIgnore, textToTruncate


from regexqueryurl import RegexQueryUrl
import re

medlineplusRegexPats = [
    '<ul id="subcatlist">.*</ul>',
    '<span class="categoryname"><a name=".*?</ul>',
    '<a href="([^/#].*?)"',
    ]

mlp_smokingcessation_portal = \
        'http://www.nlm.nih.gov/medlineplus/smokingcessation.html'

def processQueryForSE(
                    workingDir,
                    netclass,
                    vectorGenerator,
                    clickProbs,
                    placeholderURL,
                    query,
                    netname):
    myLog = Log('processQueryForSE','netclass: %s\nplaceholder URL: %s\nquery=%s\nnetname=%s' \
                    % (str(netclass), str(placeholderURL), str(query), str(netname)))
    try:
        # quit smoking
        net = netclass(_maxLevel=1,
                       _workingDir=workingDir,
                       _resultLimit=10,
                       _probabilityVector = clickProbs,
                       _probabilityVectorGenerator = vectorGenerator,
                       _default_socket_timeout = 5)

        net.SetFilenameFromQuery(query)
        # build initial network from the Medline Plus portal recommended
        # links
        

        # save some properties to restore later
        # we're going to override these at first
        savedRegexPattern = net.GetProperty('regexPattern')
        savedFindallArgs = net.GetProperty('findall_args')
        
        # Next, we set the regular expressions to be used in parsing the 
        # MedlinePlus smoking cessation portal page. This is a list of three
        # regular expressions that are used in sequence. The list is declared
        # above.
        net.SetProperty('regexPattern',medlineplusRegexPats)

        # Make sure the regex parser treats newlines as just more whitespace.
        net.SetProperty('findall_args',re.S)

        # ignore pages not relevant to our inquiry
        net.SetIgnorableText(textToIgnore)
        #
        # Don't pursue links in Amazon, YouTube, etc.
        net.SetTruncatableText(textToTruncate)
        
        net.BuildUrlTree( \
            mlp_smokingcessation_portal)
        
        # We now have a network consisting of the first- and second-level
        # outlinks from the Medline Plus smoking cessation portal's
        # recommendations.
        # Now we want to merge in a network generated from the result set of
        # the query to the AOL engine. We need to restore the class 
        # properties we saved in order to use the netclass class as it
        # was designed, to process a query.
        
        net.SetProperty('regexPattern',savedRegexPattern)
        net.SetProperty('findall_args',savedFindallArgs)
        net.urlclass = RegexQueryUrl
        #
        # clear the list of top-level URLs, so we can rely on the ones from
        # the search engine.
        net.topLevelUrls = None
        
        # The netclass.BuildUrlTreeWithPlaceholderRoot function will add to 
        # in the network already present in the netclass instance.
        net.BuildUrlTreeWithPlaceholderRoot(\
            placeholderURL,query)

        #net.MapFunctionToUrlNetwork(PrintHierarchy,args=sys.stderr)
        #net.MapFunctionToDomainNetwork(PrintHierarchy,args=sys.stderr)
        net.WritePajekFile(netname,netname)
        net.WriteGuessFile(netname + '_urls')            # url network
        net.WriteGuessFile(netname + '_domains',False)      #domain network

        return True

    except Exception,e:
        myLog.Write(str(e)+'\n on ' + query + ' query\n')
        return False
    
