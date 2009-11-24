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
# linkforest1.py

'''
This program leaves its results in a directory under your
default working directory, the directory being named with
a timestamp of the form YYYY-MM-DD--HH-MM-SS.
'''
import sys
import os
from time import strftime, localtime

from urlnet.log import Log, logging, file_only
import urlnet.log
from urlnet.googlelinktree import GoogleLinkTree
from urlnet.urlutils import GetConfigValue

'''
Google is very sensitive to 'link:' type queries coming at
it in rapidfire succession from the same URL. It suspects
the host at the IP address of running some kind of
robot spidering program (heaven forbid!). It will attempt
to force you to enter a 'captcha' phrase from a graphic,
which UrlNet is sadly unable to do.  Sleeping 3
seconds between queries seems to be enough to avoid
this limitation. The GoogleLinkTree class will force
a sleeptime of 2 seconds if its constructor is given a
smaller value for the _sleeptime argument.

Here we are taking advantage of the ability to set a
range for sleeptime, which will make us look a bit 
less robotic...
'''
SLEEPTIME = (5,9)

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
        urlnet.log.altfd=open('googlelinkforest.log.txt','w')
    except Exception,e:
        myLog.Write(str(e)+'\n')

    urlforest = (
        'http://histalk2.com',
        'http://www.healthcareguy.com',
        'http://medicalconnectivity.com',
        )
    '''
    textToIgnore = [
        'compoundthinking.com/blog/index.php?s=dict',
        'compoundthinking.com/blog/index.php/200',
        'compoundthinking.com/blog/index.php/tag',
        ]
    '''
    net = GoogleLinkTree(_maxLevel=2,
                         _workingDir=workingDir,
                         _resultLimit=20,
                         _sleeptime = SLEEPTIME,
                        _useHostNameForDomainName = True
                        )
                    
    #net.SetIgnorableText(textToIgnore)
    net.SetProperty('SEQueryFileName','googlelinkforest')

    
    # This code can be activated by setting the if condition to true
    # in order to see what query URL was generated and what Google returned.
    # 
    if net.BuildUrlForest(Urls=urlforest):

        net.WritePajekFile('GoogleLinkTree-linkforest','GoogleLinkTree-linkforest')
        net.WriteGuessFile('GoogleLinkTree-linkforest_urls')            # url network
        net.WriteGuessFile('GoogleLinkTree-linkforest_domains',False)      #domain network
    
    # tidy up
    if urlnet.log.altfd:
        urlnet.log.altfd.close()
        urlnet.log.altfd = None
        
    os.chdir(oldDir)

if __name__ == '__main__':
    main()
    sys.exit(0)
    
