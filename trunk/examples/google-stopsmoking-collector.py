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
from urlnet.log import Log, logging, altfd
from urlnet.googletree import GoogleTree
from urlnet.urlutils import PrintHierarchy
import sys
from time import strftime, localtime
import os
from urlnet.searchenginetree import computeDescendingStraightLineProbabilityVector,\
                                    computeEqualProbabilityVector
from urlnet.ignoreandtruncate import textToIgnore, textToTruncate
from urlnet.clickprobabilities import probabilityByPositionStopSmokingClicks as probability_by_position

from urlnet.regexqueryurl import RegexQueryUrl
import re
medlineplusRegexPats = [
    '<ul id="subcatlist">.*</ul>',
    '<span class="categoryname"><a name=".*?</ul>',
    '<a href="([^/#].*?)"',
    ]

def main(which):
    import urlnet.log
    from urlnet.urlutils import GetConfigValue
    from os.path import join
    """
    We are going to make a subdirectory under
    the working directory that will be different each run.
    """

    baseDir = GetConfigValue('workingDir')
    # dir to write to
    timestamp = strftime('%Y-%m-%d--%H-%M-%S',localtime())
    workingDir = join(baseDir,'stopsmoking',timestamp)

    oldDir = os.getcwd()
    goAhead = True

    # uncomment one of the vectorGenerator assignments below
    
    # vectorGenerator = computeEqualProbabilityVector
    vectorGenerator = computeDescendingStraightLineProbabilityVector
    
    try:
        try:
            os.mkdir(workingDir)
        except Exception, e:
            pass #TODO: make sure it's because the dir already exists
        os.chdir(workingDir)
        myLog = Log('main')
        urlnet.log.logging=True
        #urlnet.log.trace=True
        urlnet.log.altfd=open('googletree.log','w')
    except Exception,e:
        myLog.Write(str(e)+'\n')
        goAhead = False
    try:
        if goAhead:
            if which == 1:
                # quit smoking
                net = GoogleTree(_maxLevel=2,
                               _workingDir=workingDir,
                               _resultLimit=10,
                               _probabilityVector = probability_by_position,
                               _probabilityVectorGenerator = vectorGenerator)
                net.SetIgnorableText(textToIgnore)
                net.SetTruncatableText(textToTruncate)
                net.BuildUrlForestWithPhantomRoot('quit smoking')
                net.SetFilenameFromQuery('medlineplus_smokingcessation')
                net.SetProperty('regexPattern',medlineplusRegexPats)
                net.SetProperty('findall_args',re.S)
                net.urlclass = RegexQueryUrl
                net.BuildUrlTree('http://www.nlm.nih.gov/medlineplus/smokingcessation.html')

                #net.MapFunctionToUrlNetwork(PrintHierarchy,args=sys.stderr)
                #net.MapFunctionToDomainNetwork(PrintHierarchy,args=sys.stderr)
                net.WritePajekFile('googletree-quitsmoking','googletree-quitsmoking')
                net.WriteGuessFile('googletree-quitsmoking_urls')            # url network
                net.WriteGuessFile('googletree-quitsmoking_domains',False)      #domain network

            elif which == 2:            
                # stop smoking        
                net = GoogleTree(_maxLevel=2,
                               _workingDir=workingDir,
                               _resultLimit=10,
                               _probabilityVector = probability_by_position,
                               _probabilityVectorGenerator = vectorGenerator)
                net.SetIgnorableText(textToIgnore)
                net.SetTruncatableText(textToTruncate)
                net.BuildUrlForestWithPhantomRoot('stop smoking')
                net.SetFilenameFromQuery('medlineplus_smokingcessation')
                net.SetProperty('regexPattern',medlineplusRegexPats)
                net.SetProperty('findall_args',re.S)
                net.urlclass = RegexQueryUrl
                net.BuildUrlTree('http://www.nlm.nih.gov/medlineplus/smokingcessation.html')

                net.WritePajekFile('googletree-stopsmoking','googletree-stopsmoking')
                net.WriteGuessFile('googletree-stopsmoking_urls')            # url network
                net.WriteGuessFile('googletree-stopsmoking_domains',False)      #domain network

            elif which == 3:
                # smoking cessation        
                net = GoogleTree(_maxLevel=2,
                               _workingDir=workingDir,
                               _resultLimit=10,
                               _probabilityVector = probability_by_position,
                               _probabilityVectorGenerator = vectorGenerator)
                net.SetIgnorableText(textToIgnore)
                net.SetTruncatableText(textToTruncate)
                net.BuildUrlForestWithPhantomRoot('smoking cessation')
                net.SetFilenameFromQuery('medlineplus_smokingcessation')
                net.SetProperty('regexPattern',medlineplusRegexPats)
                net.SetProperty('findall_args',re.S)
                net.urlclass = RegexQueryUrl
                net.BuildUrlTree('http://www.nlm.nih.gov/medlineplus/smokingcessation.html')
                
                net.WritePajekFile('googletree-smokingcessation','googletree-smokingcessation')
                net.WriteGuessFile('googletree-smokingcessation_urls')            # url network
                net.WriteGuessFile('googletree-smokingcessation_domains',False)      #domain network
            
    except Exception,e:
        myLog.Write(str(e)+'\n on smoking cessation query\n')
        goAhead = False

        
    # tidy up
    if urlnet.log.altfd:
        urlnet.log.altfd.close()
        urlnet.log.altfd = None
        
    os.chdir(oldDir)
        
if __name__ == '__main__':
    if len(sys.argv) == 1:
        if len(sys.argv[0]) > 0:
            print 'Usage: python %s [number of test to run]' % (sys.argv[0])
        else:
            print 'Usage: python google-stopsmoking-collector.py [number of test to run]'
    else:
        main(int(sys.argv[1]))
    sys.exit(0)

    """
    schtasks /Create /SC DAILY /ST 12:00:00 /TN stopsmoking-collector /TR "c:\Python25\python25.exe c:\docume~1\dalehuns\desktop\blogstuff\google-stopsmoking-collector.py 1"
    """    
