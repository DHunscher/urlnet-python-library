#!/usr/bin/env python
# $Id$
# linktree1.py

import sys
import os
from time import strftime, localtime

from urlnet.log import Log, logging, file_only
import urlnet.log
from urlnet.googlelinktree import GoogleLinkTree
from urlnet.urlutils import GetConfigValue

def main():
    # dir to write to
    timestamp = strftime('%Y-%m-%d--%H-%M-%S',localtime())
    baseDir = GetConfigValue('workingDir')
    #baseDir = urlutils.GetConfigValue('workingDir')
    workingDir = os.path.join(baseDir,timestamp)
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
        myLog = Log('main')
        urlnet.log.logging=True
        #log.trace=True
        urlnet.log.altfd=open('GoogleLinkTree.log','w')
    except Exception,e:
        myLog.Write(str(e)+'\n')

    
    x = GoogleLinkTree(_maxLevel=2,
                    _workingDir=workingDir,
                    _resultLimit=20)
                    
    if False:
        (queryURL,url,Urls) = x.GetSEResultSet('http://compoundthinking.com/blog/')
        print queryURL
        print Urls

    if True:
        x.BuildUrlTree('http://compoundthinking.com/blog/')

        x.WritePajekFile('GoogleLinkTree-linktree','GoogleLinkTree-linktree')
        x.WriteGuessFile('GoogleLinkTree-linktree_urls')            # url network
        x.WriteGuessFile('GoogleLinkTree-linktree_domains',False)      #domain network
    
    # tidy up
    if log.altfd:
        log.altfd.close()
        log.altfd = None
        
    os.chdir(oldDir)

if __name__ == '__main__':
    main()
    sys.exit(0)
    