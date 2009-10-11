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
# sitemap1.py
from urlnet.urltree import UrlTree

# test building a site map network
net = UrlTree(_maxLevel=4,
              _singleDomain=True,
              _showLinksToOtherDomains=True
              )
net.SetProperty('getTitles',True)
net.BuildUrlTree('http://www.southwindpress.com/')
net.WritePajekFile('sitemap1', 'sitemap1',useTitles=True)
