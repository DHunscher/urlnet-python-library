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

      
#################### the Node class #########################
class Node(Object):
    """
    Class representing a node in a URL or domain network. 
    The Node class is responsible for knowing its relation to links to
    and from it in the network managed by the governing UrlTree. It is the 
    base class for UrlNetItem and DomainNetItem classes

    This class maintains lists of parent and child indices. A given parent
    or child index may appear in the list mutiple times, but the governing
    UrlTree network maintains only one Node instance per url or domain.
    """
    
    # the network of which I am part
    myNet = None

    # my index    
    myIdx = 0

   
    """
     dictionaries of indices of urls pointing to, or pointed to by, this item.
     the value used to look up is the parent or child index, the value returned
     by the lookup is the number of times this edge is traversed in the network.
    """
    parents = {}
    children = {}
    
    def __init__(self, _idx, _net):
        """
        idx: index from the owning UrlTree's urlList.
        net: the instantiating UrlTree.
        """

        #initialize the parent class
        
        Object.__init__(self)
        self.myIdx = _idx
        self.myNet = _net
        self.parents = {}
        self.children = {}
        self.SetName(str(_idx))
       
    def GetIdx(self):
        """ get unique ID of this instance
        """
        return self.myIdx
    
    def GetParents(self):
        """ get list of indices of parents of this item
        """
        return self.parents.keys()

    def GetChildren(self):
        """ get list of indices of children of this item
        """
        return self.children.keys()

    def GetParentHitCount(self,idx):
        """ get count of hits on parent of item
        """
        if idx in self.parents.keys():
            return self.parents[idx]
        else:
            return 0
    
    def GetChildHitCount(self,idx):
        """ get count of hits on this child item
        """
        if idx in self.children.keys():
            return self.children[idx]
        else:
            return 0

    def GetNumberOfParents(self):
        """ get count of parents of this item
        """
        return len(self.parents.keys())
    
    def GetNumberOfChildren(self):
        """ get the count associated with a child item
        """
        return len(self.children.keys())

    def AppendParent(self,parentIdx = None):
        if parentIdx != None and self.myIdx != parentIdx: # can't be my own parent
            count = -1
            try:
                count = self.parents[parentIdx]
                count = count + 1
            except Exception, e:
                count = 1
            
            self.parents[parentIdx] = count
        
    def AppendChild(self,childIdx):
        """ append the index of a child of this item to the
        children list, and the index of the parent to the parents
        list. """
        
        if childIdx != self.myIdx: # can't be my own child
            count = -1
            try:
                count = self.children[childIdx]
                count = count + 1
            except Exception, e:
                count = 1
                
            self.children[childIdx] = count
    
    def GetName(self):
        """ get the name of this node
        """
        return self.myName

    def SetName(self,name):
        self.myName = name

def main():
    item = []
    idx = 1
    root = idx
    noParent = None
    
    item.append( Node(idx,'Net') )
    item[0].AppendChild(idx) # should do nothing
    item[0].AppendParent(idx) # should do nothing
    for idx in range(2,5):
        item[0].AppendChild(idx)
        item.append(Node(idx,'Net'))
        item[idx-1].AppendParent(root)
        if idx == 3:
            item[idx-1].SetName('number ' + str(item[idx-1].GetIdx()))
    print(' ')
    print 'list of ' + str(len(item)) + ' items:'
    print str(item)
    for i in range(1,len(item)+1):
        print i, ' "', item[i-1].GetName(), '"'
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

