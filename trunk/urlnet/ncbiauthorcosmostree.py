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
The NCBIAuthorCosmosTree class creates a network by generating a tree of co-authors from data in Pub Med.
"""

import re
import string
import sys
import os
import urllib
import socket
import time

from urllib import unquote
from urllib2 import urlopen, Request
from urllib import urlencode
from urlparse import *
from htmllib import HTMLParser
from formatter import NullFormatter
from Ft.Xml import InputSource, Sax

from object import Object
from url import Url, DomainFromHostName
from urlparse import urlparse
from urlnetitem import UrlNetItem
from domainnetitem import DomainNetItem
from log import Log, logging, file_only
import log
from urltree import UrlTree
from urlutils import *
from ncbitree import NCBITree
from ncbiauthorcosmosurl import NCBIAuthorCosmosUrl
     
###################################################################
###################################################################
###################################################################

class NCBIAuthorCosmosTree(NCBITree):
    """
    Class representing a tree of NCBI URIs
    """


    
    def __init__(self,
                 _email = None,
                 _maxLevel = 2,
                 _urlclass = NCBIAuthorCosmosUrl,
                 _workingDir=None, 
                 _default_socket_timeout = 15,
                 _sleeptime = 3,
                 _userAgent = None,
                 _netItemClass = UrlNetItem): 
        try:
            log = Log('NCBIAuthorCosmosTree ctor')
            #
            # Most of the work is done by the parent class. All we do
            # here is specify what class to use for constructing Url
            # instances. We need to use a descendant of the Url class
            # for this purpose.
            #
            NCBITree.__init__(self,
                             _email,
                             _urlclass = _urlclass,
                             _maxLevel=_maxLevel,
                             _workingDir=_workingDir, 
                             _default_socket_timeout = _default_socket_timeout,
                             _sleeptime=_sleeptime,
                             _userAgent=_userAgent,
                             _netItemClass = _netItemClass,
                              _NCBIApi = NCBITree.NCBI_AUTHOR_COSMOS_API)


                
        except Exception, e:
            self.SetLastError('in NCBIAuthorCosmosTree.__init__: ' + str(e))

############################################################
####################   public APIs   #######################
############################################################

    def BuildUrlTree(self,author,parentItemIdx=None,currentLevel=0,alreadyMassaged=False):
        """
        This is the "plain vanilla" version.
        
        Build the tree, starting from a given URL. Will be called recursively
        for child URLs to whatever level the UrlTree is constructed to handle.
        """
        log = Log('NCBIAuthorCosmosTree.BuildUrlTree','url=' + str(author) + '\nparent idx=' + str(parentItemIdx) + '\nlevel=' + str(currentLevel))
        currentItem = None
        title = None
        co_author = None
        mesh_term = None
        props = {'nodeType':'author',}
        try:
            currentDomain = author

            if not self.rootDomain:
                self.rootDomain = currentDomain

            # add a node for the author we were given                
            (currentItem, currentIdx, isNewItem) = self.PutUrl(parentItemIdx,author,currentLevel,props)
            
            if (not currentItem):
                raise Exception, 'PutUrl failed on author'
            # get pub titles and pmids; process co-authors and MeSH terms at this level
            props2 = props
            authidxlist = []
            meshidxlist = []
            for (title,pmid) in currentItem.GetUrl().GetPubTitles():
                props['nodeType'] = 'pub'
                props['pmid'] = pmid
                # Add the title as a node
                (titleItem, titleIdx, isNewItem) = self.PutUrl(currentIdx,title,currentLevel+1,props)
                if not titleItem:
                    raise Exception, 'PutUrl failed on title'
                # add co-authors
                for co_author in currentItem.GetUrl().GetCoAuthors(title):
                    props2['nodeType'] = 'author'
                    (coauthorItem, coauthorIdx, isNewItem) = self.PutUrl(titleIdx,co_author,currentLevel,props2)
                    if not coauthorItem:
                        raise Exception, 'PutUrl failed on co-author'
                    authidxlist.append((coauthorItem,coauthorIdx,))
                # relate everybody to each other
                for (item, idx) in authidxlist:
                    for (otheritem,otheridx) in authidxlist:
                        if idx != otheridx:
                            item.AppendChild(otheridx)
                # add MeSH terms
                for mesh_term in currentItem.GetUrl().GetMeSHTerms(title):
                    props2['nodeType'] = 'mesh_term'
                    (meshItem, meshtermIdx, isNewItem) = self.PutUrl(titleIdx,mesh_term,currentLevel,props2)
                    if not meshItem:
                        raise Exception, 'PutUrl failed on MeSH term'
                    meshidxlist.append((meshItem, meshtermIdx,))
                # relate everybody to each MeSH term
                for (item, idx) in authidxlist:
                    for (otheritem,otheridx) in meshidxlist:
                        item.AppendChild(otheridx)
                # ...and vice versa
                for (item, idx) in meshidxlist:
                    for (otheritem,otheridx) in authidxlist:
                        item.AppendChild(otheridx)
                # relate each term to each other term
                for (item, idx) in meshidxlist:
                    for (otheritem,otheridx) in meshidxlist:
                        if idx != otheridx:
                            item.AppendChild(otheridx)
                authidxlist = []
                meshidxlist = []

            if currentItem and isNewItem and not (currentLevel >= self.maxLevel):
                return self.BuildUrlForest(Authors=currentItem.GetUrl().GetCoAuthors(title),
                                    level=currentLevel+1, parentIdx=currentIdx)
            else:
                return True
        except Exception, e:
            self.SetLastError( str(e)\
                              + '\nstarting author: ' + author \
                              + '\ncurrent title: ' + str(title)
                              + '\ncurrent co-author: ' + str(co_author)
                              + '\ncurrent mesh term: ' + str(mesh_term))
            return False


    def BuildUrlForest(self,Authors,level=0, parentBase=None, parentIdx=None):
        """
        Given a list of urls to be processed, build a tree by calling BuildUrlTree
        successively with each url in the list. In this case there is no root URL,
        unless this is called at some level other than the root.
        """
        self.ResetLastError()
        log = Log('NCBIAuthorCosmosTree.BuildUrlForest')
        currentLevel = level
        rootIdx = parentIdx
        author = None
        try:
            
            for author in Authors:
                childItem = self.BuildUrlTree(author=author,parentItemIdx=rootIdx,
                                currentLevel=currentLevel,
                                alreadyMassaged=True)
                if not childItem:
                    log.Write( 'in NCBIAuthorCosmosTree.BuildUrlForest, NCBIAuthorCosmosTree.BuildUrlTree failed for childUrl: ' + str(childUrl) )
            return True
        except Exception, e:
            self.SetLastError( str(e) + '\ncurrent author: ' + str(author))
            return False

############################################################
##################  helper functions  ######################
############################################################


    # network serializers 
    def WritePajekFile(self,netname,filename):
        ### PAJEK
        URLFILE = None
        log = Log('NCBIAuthorCosmosTree.WritePajekFile',netname+':'+filename)
        try:
            URLFILE = open(filename + ".tmp","w")
            self.WritePajekStream(netname,URLFILE)
            maxIdx = len(self.UrlNetItemByIndex.keys())
            URLFILE.write('\n\n*Partition NodeTypes: 0=author,1=pub,2=MeSH cat\n*Vertices ' + str(maxIdx) + ' \n')
            itemlist = {}
            nodetype2valuedict = {'author':0,'pub':1,'mesh_term':2,}
            self.MapFunctionToUrlItemList(BuildListOfItemIndicesWithPropertyValueDict,
                                              args=(itemlist,'nodeType',nodetype2valuedict))
            keys = itemlist.keys()
            keys.sort()
            for idx in keys:
                nodetype = itemlist[idx]
                spaces = ' '*(8-len(str(nodetype)))
                URLFILE.write(spaces + str(nodetype) + '\n')
                if idx > maxIdx:
                    self.SetLastError( 'too many keys in partition list: ' + str(idx) )
            URLFILE.close()
            """
            Pajek always requires DOS-like line endings
            """
            ConvertTextFile2DOS(filename + ".tmp",filename + ".paj")
            
        except Exception, e:
            self.SetLastError('In NCBIAuthorCosmosTree.WritePajekFile: ' + str(e))
            if URLFILE:
                URLFILE.close()


def main():
    # dir to write to
    workingDir =urlutils.GetConfigValue('workingDir')
    log.logging=True
    myLog = Log('main')
    
    x = NCBIAuthorCosmosTree(_maxLevel=2,
                       _email='dalehuns@umich.edu',
                       _workingDir=workingDir)
    x.BuildUrlTree('Athey BD')

    
    x.MapFunctionToUrlNetwork(PrintHierarchy,args=sys.stderr)
    x.WritePajekFile('AtheyBD_author_cosmos','AtheyBD_author_cosmos')
    x.WriteGuessFile('AtheyBD_author_cosmos_urls')            # url network


if __name__ == '__main__':
    main()
    sys.exit(0)
    
