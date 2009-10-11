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
# ignorabletext1.py
from urlnet.urltree import UrlTree
import re

# first, we create Pajek project without ignorables and truncatables
# for comparison purposes

net = UrlTree(_maxLevel=3)
net.BuildUrlTree('http://www.southwindpress.com')
net.WritePajekFile('ignorabletext1', 'ignorabletext1')

# next, we create Pajek project with ignorables and truncatables

ignorableText = ['sitemeter',]
truncatableText = ['Payloadz',]

# we could also set ignorable text by calling net.SetIgnorableText after
# instantiating the net, instead of passing as a constructor argument
# as we do here.

net = UrlTree(_maxLevel=3, _ignorableText=ignorableText)

# we could have also set truncatable text by passing our list
# as the _truncatableText argument to the constructor;
# this is the proper approach if you want to set re.search flags,
# as we do here

net.SetTruncatableText(truncatableText,\
                re.IGNORECASE) # could use re.I instead

net.BuildUrlTree('http://www.southwindpress.com')

# nets in this Pajek project should have no sitemeter links,
# and payloadz links should be truncated where they appear.
net.WritePajekFile('ignorabletext2', 'ignorabletext2')
