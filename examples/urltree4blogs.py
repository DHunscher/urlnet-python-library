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
# urltree4blogs.py
from urlnet.urltree import UrlTree

# first build a default Pajek project, in which the
# domain networks use domain names (e.g. typepad.com)
net = UrlTree()
net.BuildUrlTree('http://healthitgirl.com/')
net.WritePajekFile('urltree4blogs1', 'urltree4blogs1')
# now do the same thing, but turn on host names
# (e.g., sethgodin.typepad.com)
net = UrlTree(_useHostNameForDomainName = True)
net.BuildUrlTree('http://healthitgirl.com/')
net.WritePajekFile('urltree4blogs2', 'urltree4blogs2')
