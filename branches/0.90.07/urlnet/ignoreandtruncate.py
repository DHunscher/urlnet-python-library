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

"""
My standard text ignorables and truncatables for search engine results.
"""

# ignore URLs that contain any of these text fragments 
# these can be regular expressions, since the test is re.search()
# to set flags for use in re.search(), such as re.IGNORECASE,
# pass them as the second argument to net.SetIgnorableText()


textToIgnore = [
    '#',
    'statcounter.',
    '/analytics/',
    'onestat',
    'doubleclick',
    'swicki',
    'eurekster',
    'yahoo.com',
    'ads2.',
    'overture.',
    '/rss/',
    '/rdf/',
    '/feed/',
    'feeddigest',
    'sitemeter',
    'clustrmaps',
    'adbureau',
    'digg.com',
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
    'hollywood.com',
    'addthis.com',
    'hhs.gov',
    'feedblitz',
    'feeddigest',
    'feedster',
    '/about/',
    'careers',
    'employment',
    'sitemap',
    'site-map',
    'aolstore.com',
    'aolsyndication.com',
    'linkedin.com',
    '/privacy/',
    '/privacy.',
    '/help/',
    ]

# process URLs that contain any of these text fragments, but truncate
# recursion at this node; i.e., don't follow outlinks in the page.
# these can be regular expressions, since the test is re.search()
# to set flags for use in re.search(), such as re.IGNORECASE,
# pass them as the second argument to net.SetTruncatableText()

textToTruncate = [
    '://news.',
    'youtube.com',
    'amazon.com',
    'skype.com',
    'www.metacafe.com',
    ]
