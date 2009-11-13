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
# twitterpeople1.py

from urlnet.twitterpeopletree import TwitterPeopleTree
import urlnet.twitterconstants 
import urlnet.log


def main():
    
    urlnet.log.logging = True
    urlnet.log.traceback = True
    urlnet.log.trace = True
    urlnet.log.file_only = True
    try:
        urlnet.log.altfd = open('twitterpeople1.log.txt','w')
        
        net = TwitterPeopleTree( \
            _twitterUser        = 'DHunscher',
            _twitterPassword    = 'OffWorld',
            _twitterApi         = urlnet.twitterconstants.FRIENDS,
            _maxLevel           = 2 
            )
        #if net.BuildUrlTree('DHunscher'):
        #    net.WritePajekNetworkFile('twitter1','twitter1')
        net.BuildUrlTree('DHunscher')
        net.WritePajekNetworkFile('twitter1','twitter1')
        
        
    except Exception, e:
        print str(e)
    if urlnet.log.altfd:
        close(urlnet.log.altfd)
        

if __name__ == '__main__':
    main()
    


