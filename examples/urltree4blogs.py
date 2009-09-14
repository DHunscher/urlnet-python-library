#!/usr/bin/env python
# $Id$
# urltree4blogs.py
from urlnet.urltree import UrlTree
net = UrlTree(_useHostNameForDomainName = True)
net.BuildUrlTree('http://healthitgirl.com/')
net.WritePajekFile('urltree4blogs', 'urltree4blogs')
