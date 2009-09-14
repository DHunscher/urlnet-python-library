#!/usr/bin/env python
# $Id$
# placeholderroot1.py
from urlnet.urltree import UrlTree

some_msn_melanoma_urls = (
'www.melanoma.com/site_map.html',
'www.skincancer.org/melanoma/index.php',
'www.melanoma.org/',
'www.mpip.org/',
)

net = UrlTree(_maxLevel=2)
success = net.BuildUrlTreeWithPlaceholderRoot(\
    rootPlaceholder="http://search.msn.com/",\
    Urls=some_msn_melanoma_urls)
if success:
    net.WritePajekFile('placeholderroot1', 'placeholderroot1')
