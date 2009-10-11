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

from object import Object
from node import Node

#################### the DomainNetItem class #########################
class DomainNetItem(Node):
    """
    Class representing a node in a domain network. Because it may have one or
    more child nodes, it is itself essentially a domain network.
    The UrlNetItem class is responsible for knowing its relation to links to
    and from it in the domain network managed by the governing UrlTree.

    This class maintains lists of parent and child indices. A given parent
    or child index may appear in the list mutiple times, but the governing
    UrlTree network maintains only one DomainNetItem per url.
    """
    
    def __init__(self, _idx, _domain, _net):
        """
        idx: index from the owning UrlTree's urlList.
        domain: name of the domain this object encapsulates.
        net: the instantiating UrlTree.
        """

        #initialize the parent class
        
        Node.__init__(self, _idx, _net)
        self.SetName( _domain )
       

    def GetDomain(self):
        return self.GetName()

def main():
    domains = [
        'google.com',
        'supportability.com',
        'southwindpress.com',
        'microsoft.com',
        ]
    item = []
    idx = 1
    root = idx
    noParent = None
    
    item.append( DomainNetItem(idx,domains[idx-1],'Net' ) )
    for idx in range(2,5):
        item[0].AppendChild(idx)
        item.append(DomainNetItem(idx,domains[idx-1],'Net'))
        item[idx-1].AppendParent(root)
    print(' ')
    print 'list of ' + str(len(item)) + ' items:'
    print str(item)
    for i in range(1,len(item)+1):
        print i, ' "', item[i-1].GetDomain(), '"'
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


