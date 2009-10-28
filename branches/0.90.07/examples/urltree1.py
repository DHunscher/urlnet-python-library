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
# urltree1.py
from urlnet.urltree import UrlTree
net = UrlTree()
net.BuildUrlTree('http://www.southwindpress.com')
net.WritePajekFile('urltree1', 'urltree1')
