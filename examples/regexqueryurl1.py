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
# regexqueryurl1.py
from urlnet.urltree import UrlTree
from urlnet.regexqueryurl import RegexQueryUrl
import re

net=UrlTree(_maxLevel=2,\
            _urlclass=RegexQueryUrl)
regexPats = [
    '<ul id="subcatlist">.*</ul>',
    '<span class="categoryname"><a name=".*?</ul>',
    '<a href="([^/#].*?)"',
    ]

net.SetProperty('regexPattern',regexPats)
net.SetProperty('findall_args',re.S)
net.SetProperty('SEQueryFileName','regexqueryurl1_out')
#success = net.BuildUrlTree('http://www.nlm.nih.gov/medlineplus/melanoma.html')
success = net.BuildUrlTree('http://www.nlm.nih.gov/medlineplus/smokingcessation.html')
if success:
    net.WritePajekFile('regexqueryurl1','regexqueryurl1')

