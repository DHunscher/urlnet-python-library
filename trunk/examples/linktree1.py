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

    textToIgnore = [
        'compoundthinking.com/blog/index.php?s=dict',
        'compoundthinking.com/blog/index.php/200',
        'compoundthinking.com/blog/index.php/tag',
        ]
    
    x = GoogleLinkTree(_maxLevel=2,
                    _workingDir=workingDir,
                    _resultLimit=20)
                    
    x.SetIgnorableText(textToIgnore)
    
    # This code can be activated to see what query URL was generated and
    # what Google returned.
    if False:
        (queryURL,url,Urls) = x.GetSEResultSet('http://compoundthinking.com/blog/')
        print queryURL
        for url in Urls:
            print url

    if True:
        x.BuildUrlTree('http://compoundthinking.com/blog/')

        x.WritePajekFile('GoogleLinkTree-linktree','GoogleLinkTree-linktree')
        x.WriteGuessFile('GoogleLinkTree-linktree_urls')            # url network
        x.WriteGuessFile('GoogleLinkTree-linktree_domains',False)      #domain network
    
    # tidy up
    if urlnet.log.altfd:
        urlnet.log.altfd.close()
        urlnet.log.altfd = None
        
    os.chdir(oldDir)

if __name__ == '__main__':
    main()
    sys.exit(0)
    
