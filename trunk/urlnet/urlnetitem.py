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

import re
import string
import sys
import os

from urllib import unquote
from urllib import urlopen
from urllib import urlencode
from urlparse import *
from htmllib import HTMLParser
from formatter import NullFormatter
from object import Object
from url import Url
from node import Node
#from swdtechnoratiurl import TechnoratiUrl
      
#################### the UrlNetItem class #########################
class UrlNetItem(Node):
    """
    Class representing a node in a URL network. Because it may have one or
    more child nodes, it is itself essentially a URL network.
    The UrlNetItem class is responsible for knowing its relation to links to
    and from it in the URL network managed by the governing UrlTree.

    This class maintains lists of parent and child indices. A given parent
    or child index may appear in the list mutiple times, but the governing
    UrlTree network maintains only one UrlNetItem per url.
    """
    
    # my Url object (or descendant thereof)
    myUrl = None

    # the class to use for creating child url objects - either Url or a descentant thereof    
    urlclass = Url

    # My domain index.
    myDomainIdx = None

    myDomainName = None

    myHostName = None
    
    def __init__(self, _idx, _url, _net, _urlclass = Url):
        """
        idx: index from the owning UrlTree's master index of urls.
        url: the url passed by the instantiating UrlTree.
        net: the instantiating UrlTree.
        urlclass: the class Url or a class derived therefrom. Used
                   to create an instance of a Url object or derivative
                   class.
                   Make sure you pass the *class name* itself, undecorated,
                   not the class name in quotes or the name of an
                   instance of the class.        
        """

        #initialize the parent class
        
        Node.__init__(self,_idx, _net)
        self.urlclass = _urlclass
        self.myDomainIdx = None
        self.myNet = _net
        self.myUrl = self.urlclass(_inboundUrl=_url,_network=_net)
        self.myDomainName = self.myUrl.GetDomain()
        self.myHostName = self.myUrl.GetHost()
        
    
    def GetUrl(self):
        """ get the url this instance represents
        """
        return self.myUrl

    def GetUrlText(self):
        """ get the url this instance represents
        """
        return self.myUrl.GetUrl()

    def GetName(self):
        """ get the url this instance represents
        """
        return self.myUrl.GetUrl()

    def SetDomainIdx(self,idx):
        self.myDomainIdx = idx
    

    def GetDomainIdx(self):
        return self.myDomainIdx

    def GetDomain(self):
        return self.myDomainName
        
    def GetHost(self):
        return self.myHostName
        
    
def main():
    urls = [
        'http://www.google.com',
        'http://www.supportability.com',
        'http://www.southwindpress.com',
        'http://www.microsoft.com',
        ]
    item = []
    idx = 1
    root = idx
    noParent = None
    
    item.append( UrlNetItem(idx,urls[idx-1],'Net' ) )
    for idx in range(2,5):
        item[0].AppendChild(idx)
        item.append(UrlNetItem(idx,urls[idx-1],'Net'))
        item[idx-1].AppendParent(root)
        item[idx-1].SetDomainIdx(idx+1000)
    print(' ')
    print 'list of ' + str(len(item)) + ' items:'
    print str(item)
    for i in range(1,len(item)+1):
        print i, ' "', item[i-1].GetUrlText(), '"'
        print str( item[i-1].GetUrl() )
        print str( item[i-1].GetDomainIdx() )
        print str( item[i-1].GetDomain() )
        print str(item[i-1].GetIdx())
        print str(item[i-1].GetParents())
        print str(item[i-1].GetChildren())
        if i > 0 and len(item[i-1].GetParents()) > 0:
            print str(item[i-1].GetParentHitCount(item[i-1].GetParents()[0]))
            print str(item[i-1].GetNumberOfParents())
        else:
            print 'no parents'
        if i > 0 and len(item[i-1].GetChildren()) > 0:
            print str(item[i-1].GetChildHitCount(item[i-1].GetChildren()[0]))
            print str(item[i-1].GetNumberOfChildren())
        else:
            print 'no children'
        print '-----------'
    
    return 0

if __name__ == '__main__':
    main()

