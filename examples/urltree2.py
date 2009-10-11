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
# urltree2.py
from urlnet.urltree import UrlTree
net = UrlTree(_maxLevel=3)
net.BuildUrlTree('http://www.southwindpress.com')
net.WritePajekFile('urltree2', 'urltree2')
