#!/usr/bin/env python
# $Id$
# urlforest1.py
from urlnet.urltree import UrlTree

msn_melanoma_urls = (
'http://www.melanoma.com/site_map.html',
'http://www.skincancer.org/melanoma/index.php',
'http://www.melanoma.org/',
'http://www.mpip.org/',
'http://www.cancerresearch.org/melanomabook.html',
'http://www.nlm.nih.gov/medlineplus/melanoma.html',
)

net = UrlTree(_maxLevel=2)
success = net.BuildUrlForest(Urls=msn_melanoma_urls)
if success:
    net.WritePajekFile('urlforest1', 'urlforest1')
