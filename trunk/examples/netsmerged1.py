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
# netsmerged1.py

import sys
import os
from os.path import join
import re

from urlnet.log import Log, logging, altfd
from urlnet.aoltree import AOLTree
from urlnet.urlutils import GetTimestampString, GetConfigValue
from urlnet.searchenginetree import computeDescendingStraightLineProbabilityVector,\
                                    computeEqualProbabilityVector
from urlnet.ignoreandtruncate import textToIgnore, textToTruncate
import urlnet.log


def main():
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

    # uncomment one of the vectorGenerator assignments below
    
    # vectorGenerator = computeEqualProbabilityVector
    vectorGenerator = computeDescendingStraightLineProbabilityVector
    query = None
    try:
        try:
            os.mkdir(workingDir)
        except Exception, e:
            pass #TODO: make sure it's because the dir already exists
        os.chdir(workingDir)
        myLog = Log('main')
        urlnet.log.logging=True
        #urlnet.log.trace=True
        urlnet.log.altfd=open('netsmerged1.log','w')
    except Exception,e:
        myLog.Write(str(e)+'\n')
        goAhead = False
    try:
        # combine forests from 'quit smoking', 'stop smoking', and 'smoking cessation'
        # query result trees
        x = AOLTree(_maxLevel=2,
                       _workingDir=workingDir,
                       _resultLimit=10)
        x.SetIgnorableText(textToIgnore)
        x.SetTruncatableText(textToTruncate)
        for query in ('quit smoking','stop smoking','smoking cessation'):
            root='http://www.aol.com/search?q='+re.sub(' ','+',query)
            x.BuildUrlTreeWithPlaceholderRoot(root,query)

        query = 'done building net'
        x.WritePajekFile('netsmerged1','netsmerged1')

    except Exception,e:
        if query == None:
            myLog.Write(str(e)+'\n on constructor invocation\n')
        elif query == 'done building net':
            myLog.Write(str(e)+'\n during Pajek output file generation\n')
        else:
            myLog.Write(str(e)+'\n on ' + query + ' query\n')
        goAhead = False

        
    # tidy up
    if urlnet.log.altfd:
        urlnet.log.altfd.close()
        urlnet.log.altfd = None
        
    os.chdir(oldDir)
        
if __name__ == '__main__':
    main()
    sys.exit(0)

    """
    schtasks /Create /SC DAILY /ST 12:00:00 /TN stopsmoking-collector /TR "c:\Python25\python25.exe c:\docume~1\dalehuns\desktop\blogstuff\aol-stopsmoking-collector.py 1"
    """    
