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
# includeexclude.py
from urlnet.urltree import UrlTree
from urlnet.urlutils import CheckInclusionExclusionCriteria
import re # for search flags

# in case we need to be polite...
SLEEPTIME = 0
MAXLEVEL = 2

net = UrlTree(_maxLevel=MAXLEVEL,_sleeptime=SLEEPTIME)

# test inclusion patterns

# The include_patternlist and exclude_patternlist property values,
# if present, must evaluate to a list or sequence. Items in the
# list are 'regular expressions' - the simplest form of which is
# a text string. Regular expressions support wildcards and many other
# subtle search tweaks. Search Google for "python regular expressions"
# to learn more about them.

# For readability's sake, I put each item in the list on its own
# line. Python doesn't care about the extra newlines and spaces,
# as long as the indentation is consistent.

incl_patternlist = [
    # new words or phrases could be added by copying and modifying this line.
    'CATALOG', 
    ]

# use the UrlNet-provided simple inclusion/exclusion checker
net.SetPageContentCheckerFn(\
        CheckInclusionExclusionCriteria)
        
net.SetProperty('include_patternlist',incl_patternlist)

net.BuildUrlTree('http://www.southwindpress.com')

# write URL network file
net.WritePajekNetworkFile('urltreeinclexcl1', 'urltreeinclexcl1', \
                            urlNet = True)

# round 2 - test flags.

net = UrlTree(_maxLevel=MAXLEVEL,_sleeptime=SLEEPTIME)

# we are changing the case of the word 'CATALOG' to test use of the
# ability to pass flags from module re to re.search() in the
# inclusion/exclusion checker. This version should find significantly
# fewer legal nodes -- if any, other than the root URL.

incl_patternlist = [
    'catalog',
    ]

# use the UrlNet-provided simple inclusion/exclusion checker
net.SetPageContentCheckerFn(\
        CheckInclusionExclusionCriteria)
        
net.SetProperty('include_patternlist',incl_patternlist)
net.SetProperty('exclude_patternlist',['discovering tacit assumptions',])

net.BuildUrlTree('http://www.southwindpress.com')
# write URL network file
net.WritePajekNetworkFile('urltreeinclexcl2', 'urltreeinclexcl2', \
                            urlNet = True)

# round 3
# test exclusion patterns - this network should contain fewer vertices
# than the network produced in round #1.

net = UrlTree(_maxLevel=MAXLEVEL,_sleeptime=SLEEPTIME)

incl_patternlist = [
    'catalog',
    ]

# use the UrlNet-provided simple inclusion/exclusion checker
net.SetPageContentCheckerFn(\
        CheckInclusionExclusionCriteria)
        
        
net.SetProperty('include_patternlist',incl_patternlist)

# pass in the re module flag that says to ignore case, re.IGNORECASE;
# re.I would also work. 'catalog' in the pattern list should match 'CATALOG'
# in the HTML text. Because it will also match 'catalog' or 'Catalog'
# or any similar mixed-case form, it may now include new vertices that
# were not in the round 1 network.

net.SetProperty('include_patternlist_flags',re.IGNORECASE)  
                                        
# try to exclude one vertex.
excl_patternlist = [
    'discovering tacit assumptions',
    ]

net.SetProperty('exclude_patternlist',excl_patternlist)
net.SetProperty('exclude_patternlist_flags',re.IGNORECASE)  

net.BuildUrlTree('http://www.southwindpress.com')
# write URL network file
net.WritePajekNetworkFile('urltreeinclexcl3', 'urltreeinclexcl3', \
                            urlNet = True)
