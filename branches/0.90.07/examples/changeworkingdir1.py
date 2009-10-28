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
# changeworkingdir1.py

from urlnet.urltree import UrlTree
import os

# if this program succeeds, it will put its output in a directory
# under the current directory where the program is started,
# called changeworkingdir1. A Pajek project should appear there.

workingDir = os.getcwd()
workingDir += os.sep
workingDir += 'changeworkingdir1'
try:
    os.mkdir(workingDir)
except Exception, e:
    print str(type(e)), str(e)

net = UrlTree(_maxLevel=1, _workingDir=workingDir)
net.BuildUrlTree('http://www.southwindpress.com')
net.WritePajekFile('changeworkingdir1', 'changeworkingdir1')
