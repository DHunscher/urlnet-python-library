###################################################################
#                                                                 #
#                     UrlNet Python Library                       #
#            Copyright (c) Dale A. Hunscher, 2007-2008            #
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

textToTruncate = [
    '://news.',
    'youtube.com',
    'amazon.com',
    'skype.com',
    'www.metacafe.com',
    ]
