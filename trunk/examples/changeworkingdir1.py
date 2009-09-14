#!/usr/bin/env python
# $Id$
# changeworkingdir1.py

from urlnet.urltree import UrlTree

# change this to a value that works for you...
workingDir = 'C:\\Users\\dalehuns\\Documents\\Python\\blogstuff'

net = UrlTree(_maxLevel=2, _workingDir=workingDir)
net.BuildUrlTree('http://www.southwindpress.com')
net.WritePajekFile('changeworkingdir1', 'changeworkingdir1')
