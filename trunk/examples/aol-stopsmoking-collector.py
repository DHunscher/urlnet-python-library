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
This smoking-cessation data collector relies on processQueryForSE, a routine
in collectorutils.py that implements the details of the current algorithm.
Because we are testing three synonymous queries, this eliminates the
need to "cut and paste" the processing algorithm implementation multiple
times whenever it changes as we refine it.
'''
from urlnet.log import Log, logging, altfd
import sys
from time import strftime, localtime
import os
from urlnet.aoltree import AOLTree
from urlnet.searchenginetree \
    import computeDescendingStraightLineProbabilityVector \
    as DescendingVector,\
    computeEqualProbabilityVector as StraightLineVector
from urlnet.ignoreandtruncate import textToIgnore, textToTruncate
from urlnet.clickprobabilities \
    import probabilityByPositionStopSmokingClicks \
    as probability_by_position

from urlnet.collectorutils import processQueryForSE

import re


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
    
    # vectorGenerator = StraightLineVector
    vectorGenerator = DescendingVector
    
    try:
        try:
            os.mkdir(workingDir)
        except Exception, e:
            pass #TODO: make sure it's because the dir already exists
        os.chdir(workingDir)
        myLog = Log('main')
        urlnet.log.logging=True
        #urlnet.log.trace=True
        urlnet.log.altfd=open('aoltree.log.txt','w')
    except Exception,e:
        myLog.Write(str(e)+'\n')
        goAhead = False
    try:
        if goAhead:
            if which == 1:
                # quit smoking
                goAhead = processQueryForSE(maxLevel=MAXLEVEL,
                                  workingDir=workingDir,
                                  netclass=AOLTree,
                                  vectorGenerator=vectorGenerator,
                                  clickProbs=probability_by_position,
                                  placeholderURL='http://search.aol.com/',
                                  query='quit smoking',
                                  netname='aol-quitsmoking')

            elif which == 2:            
                # stop smoking        
                goAhead = processQueryForSE(maxLevel=MAXLEVEL,
                                  workingDir=workingDir,
                                  netclass=AOLTree,
                                  vectorGenerator=vectorGenerator,
                                  clickProbs=probability_by_position,
                                  placeholderURL='http://search.aol.com/',
                                  query='stop smoking',
                                  netname='aol-stopsmoking')

            elif which == 3:
                # smoking cessation        
                goAhead = processQueryForSE(maxLevel=MAXLEVEL,
                                  workingDir=workingDir,
                                  netclass=AOLTree,
                                  vectorGenerator=vectorGenerator,
                                  clickProbs=probability_by_position,
                                  placeholderURL='http://search.aol.com/',
                                  query='smoking cessation',
                                  netname='aol-smokingcessation')

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
            print 'Usage: python aol-stopsmoking-collector.py [number of test to run]'
    else:
        main(int(sys.argv[1]))
    sys.exit(0)

    """
    schtasks /Create /SC DAILY /ST 12:00:00 /TN stopsmoking-collector /TR "c:\Python25\python25.exe c:\docume~1\dalehuns\desktop\blogstuff\aol-stopsmoking-collector.py 1"
    """    
