#!/usr/bin/env python
# $Id$
# urltree1.py
from urlnet.urltree import UrlTree
net = UrlTree()
net.BuildUrlTree('http://www.southwindpress.com')
net.WritePajekFile('urltree1', 'urltree1')
