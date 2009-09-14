#!/usr/bin/env python
# $Id$
# logging1.py
from urlnet.urltree import UrlTree
from urlnet.urlutils import GetConfigValue

workingDir = GetConfigValue('workingDir')
import urlnet.log
urlnet.log.logging=True
net = UrlTree(_maxLevel=3, _workingDir=workingDir)
net.SetProperty('getTitles',True)
net.BuildUrlTree('http://www.southwindpress.com')
net.WritePajekFile('logging1', 'logging1',useTitles=True)
