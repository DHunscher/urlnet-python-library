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
The NCBILinksTree class generates a tree of NCBI API objects
through the use of the NCBI eLink API. 
"""

import re
import string
import sys
import os
import urllib
import socket
import time


from object import Object
from url import Url, DomainFromHostName
from urlparse import urlparse
from urlnetitem import UrlNetItem
from domainnetitem import DomainNetItem
from log import Log, logging, file_only
import log
from urltree import UrlTree
from urlutils import *
from ncbiurl import NCBIUrl
from ncbitree import NCBITree
import ncbiconstants



     
###################################################################
###################################################################
###################################################################

class NCBILinksTree(NCBITree):
    """
    Class representing a tree of NCBI eLink URIs
    """

    
    def __init__(self,
                 _email = None,
                 _maxLevel = 1,
                 _urlclass = NCBIUrl,
                 _workingDir=None, 
                 _default_socket_timeout = 15,
                 _sleeptime = 3,
                 _userAgent = None,
                 _netItemClass = UrlNetItem,
                 _NCBIResultSetSizeLimit = NCBIUrl.DEFAULT_RESULTSET_SIZE_LIMIT): 
        try:
            log = Log('NCBILinksTree ctor')
            #
            # Most of the work is done by the parent class. All we do
            # here is specify what class to use for constructing Url
            # instances. We need to use a descendant of the Url class
            # for this purpose.
            #

            NCBITree.__init__(self,
                             _email,
                             _maxLevel,
                             _urlclass,
                             _workingDir=_workingDir, 
                             _default_socket_timeout = _default_socket_timeout,
                             _sleeptime=_sleeptime,
                             _userAgent=_userAgent,
                             _netItemClass = _netItemClass,
                             _NCBIApi = NCBITree.NCBI_ELINK_API,
                             _NCBIResultSetSizeLimit = _NCBIResultSetSizeLimit)
            self.dbDict = {}
            self.dbIdx = 0
            
        except Exception, e:
            self.SetLastError('in NCBILinksTree.__init__: ' + str(e))

############################################################
####################   public APIs   #######################
############################################################

    # One or more of these must be implemented in a derived class.
    
    def BuildUrlTree(self,startUrl,parentItemIdx=None,currentLevel=0,alreadyMassaged=False):
        """
        Our startUrl is a query we will pass to eLink.
        """
        raise Exception, 'NCBILinksTree.BuildUrlTree not supported.'
        


    def BuildUrlTreeWithPlaceholderRoot(self,rootPlaceholder,Urls):
        """
        not supported
        """
        raise Exception, 'NCBILinksTree.BuildUrlTreeWithPlaceholderRoot not supported.'
        
    def BuildUrlForestWithPhantomRoot(self,query,DbSrcOfIds,DbsToLink,tag=None,recurseFlags=None
                                      ):
        """
        Our phantomRoot is a query we will pass to eLink. DbSrcOfIds should be one of
        the database constants from the parent NCBITree class, and DbsToLink should be the result of a call
        to the parent class member function ConcatDBNames, which accepts and validates 
        a list of one or more database constants from the parent NCBITree class. The
        query is used to generate a list of entities from DbSrcOfIds that form the
        top level (zero) of the forest; there is no built-in root node. The related
        entities in each of the DbsToLink form level 1. If the _maxLevel argument to
        the constructor is left at the default of 1, no further recursion is done.
        
        If LinkUpward is True, a linkage is performed from each id in level 1 back to
        the DbSrcOfIds. The entities identified in that call are added to the network at
        level 2. 
        """
        log = Log('NCBILinksTree.BuildUrlForestWithPhantomRoot','query=' + query + ', dbfrom=' + str(DbSrcOfIds) + ', dbs to=' + str(DbsToLink) + ', tag=' + str(tag))
        try:
            #query='depression gene protein'
            url = self.urlclass(query,self)
            (query_key,webenv,ids) = url.GetIdsOfNCBIItems(query=query,tag=tag,db=DbSrcOfIds,usehistory='n')
            #print (self.GetLastSuccessfulQuery())
            #print str(ids)
            data = url.GetLinksBetweenNCBIItems(DbSrcOfIds=DbSrcOfIds,DbsToLink=DbsToLink,ids=ids)
            url = None
            for fromdb in data['dbfromlist'].keys():
                if ncbiconstants.dbentitynamesdict[fromdb] not in self.dbDict.keys():
                    self.dbDict[ncbiconstants.dbentitynamesdict[fromdb]] = self.dbIdx
                    self.dbIdx = self.dbIdx + 1
                for id in data['dbfromlist'][fromdb]['ids'].keys():
                    name = data['dbfromlist'][fromdb]['ids'][id]['name']
                    (item,itemIdx,isNewItem) = self.PutUrl(None,name,level=0,\
                                    properties={'db':ncbiconstants.dbentitynamesdict[fromdb],'pmid':id,})
                    data['dbfromlist'][fromdb]['ids'][id]['idx'] = itemIdx
                                                           
                    for todb in data['dbtolist'].keys():
                        if ncbiconstants.dbentitynamesdict[todb] not in self.dbDict.keys():
                            self.dbDict[ncbiconstants.dbentitynamesdict[todb]] = self.dbIdx
                            self.dbIdx = self.dbIdx + 1
                        if id in data['dbtolist'][todb]['idsfrom'].keys():
                            for link in data['dbtolist'][todb]['idsfrom'][id]['links'].keys():
                                for toid in data['dbtolist'][todb]['idsfrom'][id]['links'][link]:
                                    toname = data['dbtolist'][todb]['ids'][toid]['name']
                                    (toItem,toItemIdx,isToNewItem) = self.PutUrl(itemIdx,toname,level=1,\
                                                        properties={'db':ncbiconstants.dbentitynamesdict[todb],'pmid':toid,})
                                    data['dbtolist'][todb]['ids'][toid]['idx'] = toItemIdx
            fd = open('elinkoutput.txt','w')
            fd.write(str(data))
            fd.close()
            #print 'all done!'
        except Exception, e:
            raise # for now
        
    def BuildUrlForest(self,Urls,level=0, parentBase=None, parentIdx=None):
        """
        not supported
        """
        raise Exception, 'NCBILinksTree.BuildUrlTree not supported.'

    # network serializers
    
    def WritePajekFile(self,netname,filename):
        ### PAJEK
        URLFILE = None
        log = Log('NCBILinksTree.WritePajekFile',netname+':'+filename)
        try:
            URLFILE = open(filename + ".paj","w")
            self.WritePajekStream(netname,URLFILE)
            # write partition based on a dictionary of names:integer values
            self.WritePajekPartitionFromPropertyDict(URLFILE,'NodeTypes','db',self.dbDict)
            URLFILE.close()
        except Exception, e:
            self.SetLastError('In NCBILinksTree.WritePajekFile: ' + str(e))
            if URLFILE:
                URLFILE.close()
    

def main(which):
    # dir to write to
    timestamp = time.strftime('\\%Y-%m-%d--%H-%M-%S',time.localtime())
    baseDir = GetConfigValue('workingDir')
    workingDir = baseDir+timestamp
    oldDir = os.getcwd()
    
    myLog = None
    goAhead = True
    
    try:
        try:
            os.mkdir(baseDir)
        except Exception, e:
            pass #TODO: make sure it's because the dir already exists
        try:
            os.mkdir(workingDir)
        except Exception, e:
            pass #TODO: make sure it's because the dir already exists
        os.chdir(workingDir)
        myLog = Log('main')
        log.logging=True
        #log.trace=True
        log.altfd=open('ncbilinkstree.log','w')
    except Exception,e:
        myLog.Write(str(e)+'\n')
        goAhead = False

    if goAhead:
        try:
            net = NCBILinksTree(_maxLevel=1,
                               _email='dalehuns@umich.edu',
                               _workingDir=workingDir,
                               _sleeptime=3,
                               _NCBIResultSetSizeLimit = 20)
            if which == 1:
                dbs = ncbiconstants.ConcatDBNames( (ncbiconstants.PROTEIN,ncbiconstants.NUCLEOTIDE,ncbiconstants.SNP) )
                qry = 'BRAF[GENE]'
                net.BuildUrlForestWithPhantomRoot(qry,DbSrcOfIds=ncbiconstants.GENE,DbsToLink=dbs)
                net.WritePajekFile(qry,qry)
            elif which == 2:
                dbs = ncbiconstants.PUBMED
                qry = 'quit smoking'
                net.BuildUrlForestWithPhantomRoot(qry,DbSrcOfIds=ncbiconstants.PUBMED,DbsToLink=dbs)
                net.WritePajekFile(qry,qry)
            elif which == 3:
                dbs = ncbiconstants.PUBMED
                qry = 'stop smoking'
                net.BuildUrlForestWithPhantomRoot(qry,DbSrcOfIds=ncbiconstants.PUBMED,DbsToLink=dbs)
                net.WritePajekFile(qry,qry)
            elif which == 4:
                dbs = ncbiconstants.PUBMED
                qry = 'smoking cessation'
                net.BuildUrlForestWithPhantomRoot(qry,DbSrcOfIds=ncbiconstants.PUBMED,DbsToLink=dbs)
                net.WritePajekFile(qry,qry)
        except Exception, e:
            print str(e)
    # tidy up
    if log.altfd:
        log.altfd.close()
        log.altfd = None
        
    os.chdir(oldDir)



if __name__ == '__main__':
    for i in (\
            1,\
            #2,\
            #3,\
            #4
            ):
        main(i)
    sys.exit(0)
    