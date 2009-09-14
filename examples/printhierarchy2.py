#!/usr/bin/env python
# $Id$
# printhierarchy2.py
from urlnet.urltree import UrlTree

msn_melanoma_urls = (
'http://www.melanoma.com/site_map.html',
'http://www.skincancer.org/melanoma/index.php',
'http://www.melanoma.org/',
'http://www.mpip.org/',
'http://www.cancerresearch.org/melanomabook.html',
'http://www.nlm.nih.gov/medlineplus/melanoma.html',
)

net = UrlTree(_maxLevel=1)
#net.SetProperty('getTitles',True)
success = net.BuildUrlForest(Urls=msn_melanoma_urls)
if success:
    try:
        net.WriteUrlHierarchyFile('printhierarchyurls2.txt'\
                                  #,useTitles=True\
                                  )
        net.WriteDomainHierarchyFile('printhierarchydomains2.txt')
    except Exception, e:
        print str(e)
