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
# forest4blogs.py
from urlnet2.urltree import UrlTree
import urlnet2.log

net = UrlTree(_maxLevel=1,_useHostNameForDomainName = True)

urlforest = (
'http://hunscher.typepad.com',
)

#net = UrlTree(_maxLevel=1)


ignorableText = \
       ['video.google.com',
       'blogsearch.google.com',
       'google.com',
       'books.google.com',
       'news.google.com',
       'maps.google.com',
       'images.google.com',
       'blogsearch.google.com',
       'mail.google.com',
       'fusion.google.com',
       'google.com/intl',
       'google.com/search',
       'google.com/accounts',
       'google.com/preferences',
       'www.stumbleupon.com/submit',
       'cache',
       'google',
       '74.125.77.132',
       '209.85.229.132',
       '#',
       'statcounter.',
       '/analytics/',
       'onestat',
       'doubleclick',
       'swicki',
       'eurekster',
       'yahoo.com',
       'submit?',
       'quantcast',
       'ads2.',
       'overture.',
       '/rss/',
       '/rdf/',
       '/feed/',
       'feeddigest',
       'sitemeter',
       'clustrmaps',
       'adbureau',
       'zeus.com',
       'products/acrobat',
       'hon.ch',
       'feedburner.com',
       '://help.',
       'businesswire',
       '/faq.',
       'sys-con.com',
       'jigsaw.w3c.org',
       '/categories',
       'sitemap',
       'site-map',
       'site_map',
       'rss.xml',
       'misoso.com',
       'adjuggler.com',
       'skype.com',
       'validator.w3c.org',
       'digg.com/submit',
       'addthis.com',
       'feedblitz',
       'del.icio.us/post',
       'feeddigest',
       'feedster',
       '/about/',
       'careers',
       'employment',
       'sitemap',
       'site-map',
       'aolstore.com',
       'aolsyndication.com',
       '/privacy/',
       '/privacy.',
       'twitter.com/?status'
       'twitter.com/home?status',
       '/help/',
       'phpbb',
       'crawlability',
       'w3.org',
       '4networking',
       'www.adtech.com'
       'technorati',
       '/submit?'
       '/share.php',
       'adserver',
       'invisionboard',
       'reddit.com/submit',
       'www.myspace.com/Modules/PostTo/Pages/',
       'www.facebook.com/share.php?',
       'www.facebook.com/sharer.php?',
       'www.linkedin.com/shareArticle?',
       'doubleclick',]

net.SetIgnorableText(ignorableText)

urlnet2.log.logging=True
success = net.BuildUrlForest(Urls=urlforest)
# success = net.BuildUrlTree(urlforest[0])
print net.GetLastError()

if success:
   net.WritePajekFile('urlforest4blogs', 'urlforest4blogs')
   net.WritePajekNetworkFile('urlforest4blogs', 'urlforest4blogs', urlNet =
False)

