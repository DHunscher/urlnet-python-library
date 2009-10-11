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
# logging2.py
from urlnet.urltree import UrlTree
from urlnet.urlutils import GetConfigValue

workingDir = GetConfigValue('workingDir')
import urlnet.log
urlnet.log.logging=True

# the following line causes lots of output to be generated!
urlnet.log.trace=True

net = UrlTree(_maxLevel=2, _workingDir=workingDir)
net.SetProperty('getTitles',True)
net.BuildUrlTree('http://www.southwindpress.com')
net.WritePajekFile('logging2', 'logging2',useTitles=True)
