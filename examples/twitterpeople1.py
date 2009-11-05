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
    try:
        
        net = TwitterPeopleTree( \
            _twitterUser        = 'YourName',
            _twitterPassword    = 'YourPassword',
            _twitterApi         = urlnet.twitterconstants.PEOPLE,
            _maxLevel           = 1 
            )
        if net.BuildUrlTree('DHunscher'):
            net.WritePajekNetworkFile('twitter1','twitter1')
        
        
    except Exception, e:
        print str(e)

if __name__ == '__main__':
    main()
    


