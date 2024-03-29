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
# ncbicoauthortree1.py
import sys

from urlnet.ncbicoauthortree import NCBICoAuthorTree
import urlnet.log
from urlnet.urlutils import GetConfigValue
from os.path import join

workingDir = GetConfigValue('workingDir')

urlnet.log.logging = True
# write the log output to a file...
urlnet.log.altfd = open(join( workingDir, "log-ncbicoauthortree1.txt"),'w')

mylog = urlnet.log.Log('main')

net = NCBICoAuthorTree(_maxLevel=2)
ret = net.BuildUrlTree('Hunscher DA')

if ret:
    net.WritePajekFile('ncbicoauthortree1','ncbicoauthortree1')
    net.WriteGuessFile('ncbicoauthortree1_urls')            # url network
    
urlnet.log.altfd.close()
urlnet.log.altfd=None
