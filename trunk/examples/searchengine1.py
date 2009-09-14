#!/usr/bin/env python
# $Id$
# searchengine1.py
import sys
import os

from urlnet.googletree import GoogleTree
import urlnet.log
from urlnet.clickprobabilities import probabilityByPositionStopSmokingClicks
from urlnet.searchenginetree import computeDescendingStraightLineProbabilityVector,\
                                    computeEqualProbabilityVector
from urlnet.urlutils import GetTimestampString

def main():
    # uncomment one of the vectorGenerator assignments below
    
    # vectorGenerator = computeEqualProbabilityVector
    vectorGenerator = computeDescendingStraightLineProbabilityVector
    
    """
    We are going to make a subdirectory under
    the working directory that will be different each run.
    """
    from urlnet.urlutils import GetConfigValue
    from os.path import join

    baseDir = GetConfigValue('workingDir')

    # make unique directory to write to
    timestamp = GetTimestampString()
    workingDir = join(baseDir,timestamp)
    oldDir = os.getcwd()
    
    myLog = None

    try:
        try:
            os.mkdir(baseDir)
        except Exception, e:
            pass #TODO: make sure it's because the dir already exists
        try:
            os.mkdir(workingDir)
        except Exception, e:
            pass #TODO: make sure it's because the dir already exists
        os.chdir(workingDir)
        myLog = urlnet.log.Log('main')
        urlnet.log.logging=True
        #urlnet.log.trace=True
        urlnet.log.altfd=open('searchengine1.log','w')
    except Exception,e:
        myLog.Write(str(e)+'\n')
        goAhead = False

    
    net = GoogleTree(_maxLevel=1,
                    _workingDir=workingDir,
                    _resultLimit=10,
                    _probabilityVector = probabilityByPositionStopSmokingClicks,
                    _probabilityVectorGenerator = vectorGenerator)
                    
    
    ignorableText = \
        ['video.google.com',
        'books.google.com',
        'news.google.com',
        'maps.google.com',
        'images.google.com',
        'blogsearch.google.com',
        'mail.google.com',
        'fusion.google.com',
        'google.com/intl',
        'google.com/search',
        'google.com/accounts',
        'google.com/preferences',
        'doubleclick',]

    net.SetIgnorableText(ignorableText)
    
    """
    # uncomment these lines if you want to see what results the top-level query returns.

    ##################################################
    ######## get and view the result set URLs ########
    ##################################################
    (queryURL,url,Urls) = net.GetSEResultSet('quit smoking')
    print queryURL
    print Urls
    """

    """
    # comment out the  lines below (from BuildUrlForestWithPhantomRoot
    through the WriteGuessFile calls) if you just want to see 
    # the result set and have activated the above lines.
    """
    
    #########################################################
    ######## build a forest and output some networks ########
    #########################################################
    net.BuildUrlForestWithPhantomRoot('quit smoking')
    #net.SetProperty('getTitles',True)

    net.WritePajekFile('searchengine1-quitsmoking','searchengine1-quitsmoking' \
                       #,useTitles=True \
                       )
    net.WriteGuessFile('searchengine1-quitsmoking_urls'\
                       #,useTitles=True\
                       )            # url network
    net.WriteGuessFile('searchengine1-quitsmoking_domains',False \
                       #,useTitles=True \
                       ) #domain network
    
    # tidy up
    if urlnet.log.altfd:
        urlnet.log.altfd.close()
        urlnet.log.altfd = None
        
    os.chdir(oldDir)

if __name__ == '__main__':
    main()
    sys.exit(0)
