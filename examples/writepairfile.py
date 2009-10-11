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
# writepairfile.py
from urlnet.urltree import UrlTree
net = UrlTree()
net.BuildUrlTree('http://www.southwindpress.com')
# write URL network file
net.WritePairNetworkFile('urltree1', 'urltree1urls', urlNet = True)
# write domain network file
# in this one we change the default delimiter (tab) to a bunch of spaces
# and exercise the other optional arguments as well
net.WritePairNetworkFile('urltree1',
                         'urltree1domains',
                         urlNet = False, # do domains instead
                         uniquePairs = True,
                         delimiter = '        ')
