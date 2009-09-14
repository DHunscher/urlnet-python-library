#!/usr/bin/env python
# $Id$
# technorati1.py

# build networks using the Technorati API

'''
This sample program requires the 4Suite XML library, which can
be downloaded for free from:

http://4suite.org/index.xhtml


This program will generate a warning from the 4Suite XML library:

FtWarning: Creation of InputSource without a URI

This warning can be ignored.
'''

import sys

from urlnet.technoratitree import TechnoratiTree, TECHNORATI_COSMOS_API
from urlnet.urlutils import PrintHierarchy
import urlnet.log
from urlnet.urlutils import GetConfigValue
from os.path import join

workingDir = GetConfigValue('workingDir')

urlnet.log.logging = True
# write the log output to a file...
urlnet.log.altfd = open(join( workingDir, "log-technorati1.txt"),'w')
# ...and only to the file, not to sys.stderr.
urlnet.log.file_only = True

mylog = urlnet.log.Log('main')

myTechnoratiKey=GetConfigValue("technoratiKey")
if myTechnoratiKey == None:
    raise Exception, 'You must provide a technorati key in urlnet.cfg'

net = TechnoratiTree(_maxLevel=2,
                   _technoratiApi=TECHNORATI_COSMOS_API,
                   _workingDir=workingDir,
                   _technoratiKey=myTechnoratiKey,
                   _sleeptime=1)
ret = net.BuildUrlTree('http://paulcourant.net/')

if ret:
    net.WriteUrlHierarchyFile('technorati1urlhierarchy.txt'\
                              #,useTitles=True\
                              )
    net.WriteDomainHierarchyFile('technorati1domainhierarchy.txt')
    net.WritePajekFile('technorati1_cosmos_courant','technorati1_cosmos_courant')
    net.WriteGuessFile('technorati1_cosmos_courant_urls')            # url network
    net.WriteGuessFile('technorati1_cosmos_courant_domains',False)      #domain network
    
urlnet.log.altfd.close()
urlnet.log.altfd=None
