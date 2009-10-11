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
# logging3.py
from os.path import join

from urlnet.urltree import UrlTree
from urlnet.urlutils import GetConfigValue
import urlnet.log

workingDir = GetConfigValue('workingDir')

# turn on logging
urlnet.log.logging=True

# the following line causes lots of output to be generated!
urlnet.log.trace=True

# the following line says to flag functions that take more than five
# seconds to complete.
urlnet.log.limit = 5.0

# the following line causes output to be tee'd off to
# the file we open for writing.
urlnet.log.altfd = open(join(workingDir,'logging3.log'),'w')

# The following line tells the log facility to write only to
# the altfd file descriptor and not to stderr.
urlnet.log.file_only = True

net = UrlTree(_maxLevel=2, _workingDir=workingDir)
net.SetProperty('getTitles',True)
net.BuildUrlTree('http://www.southwindpress.com')
net.WritePajekFile('logging3', 'logging3',useTitles=True)

# clean up
urlnet.log.altfd.close()
urlnet.log.altfd = None
