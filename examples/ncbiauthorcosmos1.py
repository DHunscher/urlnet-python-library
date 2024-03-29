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
# ncbiauthorcosmos1.py
import sys

from urlnet.ncbiauthorcosmostree import NCBIAuthorCosmosTree
from urlnet.urlutils import PrintHierarchy
import urlnet.log
from urlnet.urlutils import GetConfigValue
from os.path import join

workingDir = GetConfigValue('workingDir')

urlnet.log.logging = True
# write the log output to a file...
urlnet.log.altfd = open(join( workingDir, "log-ncbiauthorcosmos1.txt"),'w')
# ...and only to the file, not to sys.stderr.
urlnet.log.file_only = True

mylog = urlnet.log.Log('main')

net = NCBIAuthorCosmosTree(_maxLevel=2,
                   _workingDir=workingDir,
                   _sleeptime=1)
                
net.SetProperty('email','dalehunscher@gmail.com')
ret = net.BuildUrlTree('Strecher VJ')

if ret:
    net.WriteUrlHierarchyFile('strechervj_cosmos_hierarchy')
    net.WritePajekFile('strechervj_cosmos','strechervj_cosmos')
    net.WriteGuessFile('strechervj_cosmos')            # url network
    
urlnet.log.altfd.close()
urlnet.log.altfd=None
