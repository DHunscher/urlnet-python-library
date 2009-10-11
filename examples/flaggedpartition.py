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
# flaggedpartition.py
from urlnet.urltree import UrlTree
import os

net = UrlTree()

# your URLs go in this list, single or double quoted
# make sure the realm prefix is removed (http://, ftp://...)
urlsToFlag = [
"payloadz.com/go?id=349877"   ,
"www.payloadz.com/go/view_cart.asp?id_user=42699"   ,
"payloadz.com/go?id=349878"   ,
"payloadz.com/go?id=349879"   ,
"payloadz.com/go?id=349880"   ,
"payloadz.com/go?id=350289"   ,
"payloadz.com/go?id=250731"   ,
"payloadz.com/go?id=253420"   ,
"payloadz.com/go?id=350295"   ,
"payloadz.com/go?id=350296"   ,

]

net.AddListOfUrlsToFlag(urlsToFlag,'partition from list of urls')

# change the URL from 'http://www.southwindpress.com/'
# to the starting-point URL  of your choice.
# this could also be a call to net.BuildUrlForest or any
# of the other network-builder methods.
net.BuildUrlTree('http://www.southwindpress.com/')

# change 'flaggedpartition' to the network and file name of
# your choice

net.WritePajekFile('flaggedpartition1', 'flaggedpartition1')

# now try with list in file

# the first argument to net.AddListOfUrlsToFlag() is a filename or path
# instead of a list. The file must contain URLs without quotes or commas,
# like so:
'''
payloadz.com/go?id=349878
payloadz.com/go?id=349879
etc...
'''
# blank lines in the file are ignored

tmpfilename = 'listOfUrls.tmp'

fd = open(tmpfilename,'w')
for url in urlsToFlag:
    fd.write('%s\n' % (url) )
fd.close()

net = UrlTree()

net.AddListOfUrlsToFlag(tmpfilename,'partition from file containing list of urls')

# delete the temp file now
# os.remove(tmpfilename)

net.BuildUrlTree('http://www.southwindpress.com/')

net.WritePajekFile('flaggedpartition2', 'flaggedpartition2')


