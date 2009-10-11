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
'''
tldconstants.py

Constants for url top-level domain (TLD) types returned by 
UrlTree.GetUrlTLDConstant.

'''

# arbitrary constants representing different TLD types.
DOTCOM   = 1
DOTORG   = 2
DOTNET   = 3
DOTEDU   = 4
DOTGOV   = 5
DOTADM   = 6
DOTMIL   = 7
OKDOTCOM = 8
# imposter
DOTFAKE  = 9
# unknown
DOTUNK   = 999

# author-defined relative value of different TLD types. 
V_DOTCOM  = 0.01
V_DOTORG  = 0.5
V_DOTNET  = 0.01
V_DOTEDU  = 0.5
V_DOTGOV  = 0.5
V_DOTADM  = 0.01
V_DOTMIL  = 0.01
V_OKDOTCOM = 0.25
# imposter
V_DOTFAKE = 0.01
# unknown
V_DOTUNK  = 0.01

# 3 types of URLs in terms of "goodness"
GOOD_DOMAIN = 21
OK_DOMAIN = 1
BAD_DOMAIN = 3

# dictionary of constants for url types
urlTypeConstants = {
    'com' : (DOTCOM,V_DOTCOM),
    'biz' : (DOTCOM,V_DOTCOM),
    'co' : (DOTCOM,V_DOTCOM),
    'icio' : (DOTCOM,V_DOTCOM),
    'tv' : (DOTCOM,V_DOTCOM),
    'us' : (DOTCOM,V_DOTCOM),
    'info' : (DOTCOM,V_DOTCOM),
    'google' : (DOTCOM,V_DOTCOM),
    'org' : (DOTORG,V_DOTORG),
    'or' : (DOTORG,V_DOTORG),
    'net' : (DOTNET,V_DOTNET),
    'ne' : (DOTNET,V_DOTNET),
    'edu' : (DOTEDU,V_DOTEDU),
    'ed' : (DOTEDU,V_DOTEDU),
    'gov' : (DOTGOV,V_DOTGOV),
    'go' : (DOTGOV,V_DOTGOV),
    'nhs' : (DOTGOV,V_DOTGOV), # UK's health system
    'gc' : (DOTGOV,V_DOTGOV), # Canadian government
    'int' : (DOTGOV,V_DOTGOV),
    'ad' : (DOTADM,V_DOTADM),
    'mil' : (DOTMIL,V_DOTMIL),
    'fake' : (DOTFAKE,V_DOTFAKE),
    'okcom' : (OKDOTCOM,V_OKDOTCOM),
    '???' : (DOTUNK,V_DOTUNK),
    }

urlTypeForProfitConstants = {
    'com' : True,
    'biz' : True,
    'co' : True,
    'icio' : True,
    'tv' : True,
    'us' : True,
    'info' : True,
    'google' : True,
    'org' : False,
    'or' : False,
    'net' : True,
    'ne' : True,
    'edu' : False,
    'ed' : False,
    'gov' : False,
    'go' : False,
    'nhs' : False,
    'gc' : False,
    'int' : False,
    'ad' : False,
    'mil' : False,
    'fake' : True,
    'okcom' : True,
    '???' : False,
    }

