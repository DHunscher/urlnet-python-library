#!/usr/bin/env python
# $Id$
# urltree2.py
from urlnet.urltree import UrlTree
net = UrlTree(_maxLevel=3)
net.BuildUrlTree('http://www.southwindpress.com')
net.WritePajekFile('urltree2', 'urltree2')
