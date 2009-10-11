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
# writepajeknetworkfile.py
from urlnet.urltree import UrlTree
net = UrlTree()
net.BuildUrlTree('http://www.southwindpress.com')

# write URL network file
net.WritePajekNetworkFile('urltreenet1', 'urltreenet1urls', urlNet = True)

# write levels partition
net.WritePajekPartitionFile('urltreenet1UrlLevels','URLLevels','level', \
            urlNet=True,valueDict=None)

# write domain network file
net.WritePajekNetworkFile('urltreedomnet1', 'urltreenet1domains', \
            urlNet = False)
            
# write levels partition
net.WritePajekPartitionFile('urltreenet1DomainLevels','DomainLevels', \
            'level', urlNet=False,valueDict=None)
            
# just for fun, provide a trivial example of the use of a dictionary in
# producing a partition.

myDict = { 0 : 123, 1 : 234, 2 : 456, }

# write levels partition using the dictionary approach
net.WritePajekPartitionFile('urltreenet1DomainLevelsUsingDict','DomainLevels', \
            'level', urlNet=False,valueDict=myDict)

