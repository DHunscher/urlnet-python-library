#!/usr/bin/env python
# $Id$
# writepajeknetworkfile.py
from urlnet.urltree import UrlTree
net = UrlTree()
net.BuildUrlTree('http://www.southwindpress.com')
# write URL network file
net.WritePajekNetworkFile('urltree1', 'urltree1urls', urlNet = True)
# write domain network file
net.WritePajekNetworkFile('urltree1', 'urltree1domains', urlNet = False)
