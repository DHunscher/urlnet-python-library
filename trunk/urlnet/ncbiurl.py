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
import time

from urllib import unquote
from urllib import urlencode
from urlparse import *
from htmllib import HTMLParser
from formatter import NullFormatter
from Ft.Xml import InputSource, Sax

import ncbiconstants

from url import Url
from log import Log

#################### the NCBIUrl class ######################
class NCBIUrl(Url):
    "A class encapsulating low-level functions for accessing NCBI data bases"

    key = None
    DEFAULT_RESULTSET_SIZE_LIMIT = 20
    DEFAULT_ID_COUNT_LIMIT = 50
    root = None
    url = None
    methodPrefix = None
    base = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    tool = 'UrlNet Python Library'
    
    def __init__(self, _inboundUrl, _network=None, limit=None, start=1):
        """initialize NCBI url instance
        """
        
        # Don't allow a GetPage call in the Url ctor - it would
        # waste time, because we do our own GetPage later, with
        # the NCBI CoAuthor version of GetAnchorList
        
        log = Log('NCBIUrl ctor',_inboundUrl)
        Url.__init__(self,_inboundUrl=_inboundUrl,_network=_network,_doInit=False)
        
        self.root = _inboundUrl
        netlimit = self.network.GetProperty('NCBIResultSetSizeLimit')
        if netlimit != None:
            self.netlimit = limit
        elif limit != None:
            self.netlimit = netlimit
        else:
            self.netlimit = self.DEFAULT_RESULTSET_SIZE_LIMIT
            
        idcountlimit = self.network.GetProperty('NCBI_IdCountLimit')
        if idcountlimit != None:
            self.idcountlimit = idcountlimit
        else:
            self.idcountlimit = self.DEFAULT_ID_COUNT_LIMIT
        self.start = start
        self.anchors = None
        self.url = _inboundUrl
        # turn off use of cached pages, if it is turned on
        # (which it is by default in descendant classes of UrlTree)
        if self.network.useCachedPageIfItExists == True:
            self.network.useCachedPageIfItExists = False
        


    #########################################
    ############ high-level functions #######
    #########################################

    def GetIdsOfNCBIItems(self,query,db,tag=None,retmax=None,usehistory='y'):
        """
            Get ids of objects in an NCBI data base using a query and an optional
            tag from the set defined in this class; the tag indicates the type
            of entity described in the query
        """
        log = Log('GetIdsOfNCBIItems')
        if db not in ncbiconstants.dblist:
            raise Exception, 'tag ' + str(db) + ' not in legal db list'
        if tag != None and tag not in ncbiconstants.tagsdict.keys():
            raise Exception, 'tag ' + str(tag) + ' not in legal tag set'
        try:
            
            if tag != None:
                term = query+ncbiconstants.tagsdict[tag]
            else:
                term = query
            
            if retmax == 0 or retmax == None:
                if self.netlimit != None and self.netlimit != 0:
                    retmax=self.netlimit
                else:
                    retmax=self.DEFAULT_RESULTSET_SIZE_LIMIT
                
            # retmax?
            params = {
                'db' : db,
                'usehistory' : usehistory,
                'term' : term,
                'tool' : self.tool,
                'retmode' : 'xml',
                'retmax' : retmax,
                'rettype' : 'uilist',
                }

            email = self.network.GetProperty('email')
            if email:
                params['email'] = email
                
            search_url = self.base + "esearch.fcgi?" + urlencode(params);
            log.Write('esearch query:'+search_url)
            data = self.RetrieveUrlContent(search_url)
            log.Write('esearch result:\n'+data)
            fn = self.network.GetProperty('WriteESearchRawOutput')
            if fn:
                fd = open(fn,'a')
                fd.write(str(data))
                fd.close()
            
            query_key = re.findall('<QueryKey>(.*)<\/QueryKey>',data,re.S)
            if len(query_key) > 0:
                query_key = query_key[0]
            else:
                query_key = None
            WebEnv = re.findall('<WebEnv>(.*)<\/WebEnv>',data,re.S)
            if len(WebEnv) > 0:
                WebEnv = WebEnv[0]
            else:
                WebEnv = None
            ids = re.findall('<Id>(.*)<\/Id>',data)
            # wrap this in a try block so we can examine local vars in debug mode when something goes wrong
            try:
                self.ExceptionIfErrors(data)
            except Exception, e:
                raise
            return (query_key,WebEnv,ids)
        except Exception, e:
            self.SetLastError( str(e) )
            raise Exception, str(e)

    def GetLinksBetweenNCBIItems(self,DbSrcOfIds,DbsToLink,query_key = None,WebEnv = None,ids=None,neighbors=True,
                              neighbor_history=False,linkname=None):
        """
            Get ids of objects in an NCBI data base using a query and an optional
            tag from the set defined in this class; the tag indicates the type
            of entity described in the query

            returns a structure of the form:
            
            retdict : dict
                'dbfromlist' : : dict
                    fromdbname : dict
                        'ids' : dict
                            idfrom : dict
                                'name' : string
                'dbtolist' : dict
                    dbtoname : dict
                        'ids' : dict
                            id : dict
                                'name' : string
                        'idsfrom' : dict
                            idfrom : dict
                                'links' : dict
                                    linkname : list of ids
        """
        log = Log('GetLinksBetweenNCBIItems')
        try:
            """
            cmd = None
            if neighbors:
                if neighbor_history:
                    cmd = 'neighbor_history'
                else:
                    cmd = 'neighbor'
            """
            
            data = self.eLink(DbSrcOfIds,DbsToLink,query_key,WebEnv,ids,linkname)
            fn = self.network.GetProperty('WriteELinkRawOutput')
            if fn:
                fd = open(fn,'a')
                fd.write(str(data))
                fd.close()
            linksets = ''
            links = re.findall('<LinkSet>(.*?)</LinkSet>',data,re.S)
            for link in links:
                link = link.strip()
                linksets = linksets + link + '\n'
            retdict = {}
            retdict['dbfromlist'] = {DbSrcOfIds : {'ids': {},},}
            dbto_list = re.findall('<DbTo>(.*?)</DbTo>',linksets,re.S)
            retdict['dbtolist'] = {}
            for db in dbto_list:
                retdict['dbtolist'][db] = { 'idsfrom' : {}, 'ids' : {},}
            for linkset in links:
                # get idfrom
                idlist = re.findall('<IdList>(.*?)</IdList>',linkset,re.S)[0]
                idsfrom = re.findall('<Id>(.*?)</Id>',idlist,re.S)
                for idfrom in idsfrom:
                    retdict['dbfromlist'][DbSrcOfIds]['ids'][idfrom] = {'name': '',}
                # now get linksetdbs
                linksetdblist = re.findall('<LinkSetDb>(.*?)</LinkSetDb>',linkset,re.S)
                for linksetdb in linksetdblist:
                    # get dbto name
                    dbto_name = re.findall('<DbTo>(.*?)</DbTo>',linksetdb,re.S)[0]
                    dbto_linkname = re.findall('<LinkName>(.*?)</LinkName>',linksetdb,re.S)[0]
                    ids = re.findall('<Id>(.*?)</Id>',linksetdb,re.S)
                    if idfrom not in retdict['dbtolist'][dbto_name]['idsfrom'].keys():
                        retdict['dbtolist'][dbto_name]['idsfrom'][idfrom] = {'links' : {dbto_linkname : [], }, }
                    if dbto_linkname not in retdict['dbtolist'][dbto_name]['idsfrom'][idfrom]['links'].keys():
                        retdict['dbtolist'][dbto_name]['idsfrom'][idfrom]['links'][dbto_linkname] = []
                    for id in ids:
                        if id not in retdict['dbtolist'][dbto_name]['idsfrom'][idfrom]['links'][dbto_linkname]:
                            retdict['dbtolist'][dbto_name]['idsfrom'][idfrom]['links'][dbto_linkname].append(id)
                        if id not in retdict['dbtolist'][dbto_name]['ids'].keys():
                            retdict['dbtolist'][dbto_name]['ids'][id] = { 'name' : '', }


            # get names to go with ids
            fromids = retdict['dbfromlist'][DbSrcOfIds]['ids'].keys()
            if len(fromids):
                docsums = self.eSummary(ids=fromids,db=DbSrcOfIds)
                titles = self.ParseItemsFromDocSums(docsums,'Title',None)
                if titles == None or len(titles) == 0 or len(titles[0]) == 0 or len(titles[0][1]) == 0:
                    titles = self.ParseItemsFromDocSums(docsums,'TITLE',None)
                if titles == None or len(titles) == 0 or len(titles[0]) == 0 or len(titles[0][1]) == 0:
                    titles = self.ParseItemsFromDocSums(docsums,'ScientificName',None)
                if titles == None or len(titles) == 0 or len(titles[0]) == 0 or len(titles[0][1]) == 0:
                    titles = self.ParseItemsFromDocSums(docsums,'PdbDescr',None)
                if titles == None or len(titles) == 0 or len(titles[0]) == 0 or len(titles[0][1]) == 0:
                    titles = self.ParseItemsFromDocSums(docsums,'SNP_ID',None)
                if titles == None or len(titles) == 0 or len(titles[0]) == 0 or len(titles[0][1]) == 0:
                    titles = self.ParseItemsFromDocSums(docsums,'Name',None)
                if titles == None or len(titles) == 0 or len(titles[0]) == 0 or len(titles[0][1]) == 0:
                    titles = self.ParseItemsFromDocSums(docsums,'Marker_Name',None)
                for (id, title) in titles:
                    if len(title) == 0:
                        title = ['']
                    retdict['dbfromlist'][DbSrcOfIds]['ids'][id]['name'] = title[0]
            for db in retdict['dbtolist'].keys():
                toids = retdict['dbtolist'][db]['ids'].keys()
                if len(toids):
                    docsums = self.eSummary(ids=toids,db=db)
                    titles = self.ParseItemsFromDocSums(docsums,'Title',None)
                    if titles == None or len(titles) == 0 or len(titles[0]) == 0 or len(titles[0][1]) == 0:
                        titles = self.ParseItemsFromDocSums(docsums,'Name',None)
                    for (id, title) in titles:
                        #print str(id) + ' ' + str(title)
                        if len(title) == 0:
                            title = ['']
                        retdict['dbtolist'][db]['ids'][id]['name'] = title[0]
            return retdict

        except Exception, e:
            self.SetLastError( str(e) )
            raise Exception, str(e)

        
    #########################################
    ############ helper functions ###########
    #########################################

    def ExceptionIfErrors(self,data,reportButDontDie=True):
        """
        if reportButDontDie is True, write any errors found to log.
        if reportButDontDie is False, write any erros found to log, and also
            raise an exception.
        """
        log = Log('ExceptionIfErrors')
        try:
            errors = re.findall('<ErrorList>(.*)<\/ErrorList>',data,re.S)
            if len(errors) > 0:
                raise Exception, str(errors)
            errors = re.findall('<ERROR>(.*?)<\/ERROR>',data,re.S)
            if len(errors) > 0:
                raise Exception, str(errors)
        except Exception, e:
            log.Write(str(e))
            if self.network.GetProperty('reportButDontDie') != None:
                reportButDontDie=self.network.GetProperty('reportButDontDie')
            if reportButDontDie:
                return
            raise

    def ConcatDBNames(self,dblist):
        """ concat db names for use in call to self.GetLinksBetweenNCBIItems() """
        log = Log('ConcatDBNames')
        outstr = ''
        first = True
        for db in dblist:
            if first:
                outstr = db
                first = False
            else:
                outstr = outstr + ',' + db
        return outstr
            

    def ParseItemsFromDocSums(self,data,itemname,root):
        """
            ParseItemsFromDocSums gets the list of items with the specified name from
            an NCBI document summary from eSummary.
        """
        
        log = Log('ParseItemsFromDocSums')
        retlist = []
        try:
            docsums = re.findall('<DocSum>(.*?)</DocSum>',data,re.S)
            pattern = '<Item Name="' + itemname + '" Type="String.*?">(.*?)</Item>'
            for docsum in docsums:
                docsumitems = []
                id = re.findall('<Id>(.*?)</Id>',docsum,re.S)[0]
                docsumitems.append(id)
                items = re.findall(pattern,docsum,re.S)
                docsumitems.append( items )
                retlist.append(docsumitems)
            return retlist
                
        except Exception, e:
            self.SetLastError(str(e))
            raise Exception, str(e)


    #########################################
    ### direct calls to NCBI functions #######
    #########################################

    def eFetch(self,query_key = None,WebEnv = None,ids = None,db = 'pubmed',retmode = 'xml',
                    rettype=None,retstart=0,retmax=0):
        log = Log('eFetch')
        if (WebEnv == None or query_key == None) and ids == None:
            raise Exception, 'must pass either a list of ids or both a webenv and query_key'
        elif (WebEnv == None or query_key == None) and (len(ids) == 0):
            log.Write( 'WebEnv or query_key not passed, and empty ID set:' + \
                    ' Did prior query fail to get results?' )
        try:
            if retmax == 0 or retmax == None:
                if (self.netlimit == None or self.netlimit == 0) and ids != None:
                    retmax=len(ids) #  (number of items retrieved - default=20)
                elif self.netlimit != None and self.netlimit != 0:
                    retmax=self.netlimit
                else:
                    retmax=self.DEFAULT_RESULTSET_SIZE_LIMIT
                
            params = {
                'db' : db,
                'retmode' : retmode,
                'retstart' : retstart,
                'retmax' : retmax,
                'tool' : self.tool,
                }
            
            if rettype:
                params['rettype'] = rettype
                
            email = self.network.GetProperty('email')
            if email:
                params['email'] = email
            if WebEnv != None and len(WebEnv) > 0 \
               and query_key != None and len(query_key) > 0:
                params['WebEnv'] = WebEnv
                params['query_key'] = query_key
                
            # append ids to params, if they were passed in, but urlencode the others first
            urlencoded_params = urlencode(params)
            if (ids) and 'WebEnv=' not in urlencoded_params:
                for id in ids:
                    urlencoded_params = urlencoded_params + '&id=' + id
            search_url = self.base + "efetch.fcgi?" + urlencoded_params;
            log.Write('eFetch query:'+search_url)
            data = self.RetrieveUrlContent(search_url)
            log.Write('eFetch result:\n'+data)
            fn = self.network.GetProperty('WriteEFetchRawOutput')
            if fn:
                fd = open(fn,'a')
                fd.write(str(data))
                fd.close()

            
            # wrap this in a try block so we can examine local vars in debug mode when something goes wrong
            try:
                self.ExceptionIfErrors(data)
            except Exception, e:
                raise
            return data            
        
        except Exception, e:
            self.SetLastError( str(e) )
            log.Write(str(type(e)))
            raise Exception, str(e)
            

    def eSummary(
        self,
        query_key = None,
        WebEnv = None,
        ids = None,
        db = 'pubmed',
        retmode = 'xml',
        rettype=None,  
        retstart=0,
        retmax=0):
        """
        run NCBI esummary API
        """
        i = 0
        log = Log('eSummary')
        if (WebEnv == None or query_key == None) and (ids == None):
            raise Exception, 'must pass either a list of ids or both a webenv and query_key'
        elif (WebEnv == None or query_key == None) and (len(ids) == 0):
            log.Write( 'WebEnv or query_key not passed, and empty ID set:' + \
                    ' Did prior query fail to get results?' )
        try:
            if retmax == 0 or retmax == None:
                if (self.netlimit == None or self.netlimit == 0) and ids != None:
                    retmax=len(ids) #  (number of items retrieved - default=20)
                elif self.netlimit != None and self.netlimit != 0:
                    retmax=self.netlimit
                else:
                    retmax=self.DEFAULT_RESULTSET_SIZE_LIMIT
                
            params = {
                'db' : db,
                'retmode' : retmode,
                'retstart' : retstart,
                'retmax' : retmax,
                'tool' : self.tool,
                }
            
            if rettype:
                params['rettype'] = rettype
                
            email = self.network.GetProperty('email')
            if email:
                params['email'] = email
                
            if WebEnv != None and len(WebEnv) > 0 \
               and query_key != None and len(query_key) > 0:
                params['WebEnv'] = WebEnv
                params['query_key'] = query_key
                
            # append ids to params, if they were passed in, but urlencode the others first
            urlencoded_params = urlencode(params)
            
            if ids != None and len(ids) > 0 and 'WebEnv=' not in urlencoded_params:
                data = ''
                for i in range(0,len(ids),self.idcountlimit):
                    subset_ids = ids[i:i+self.idcountlimit]
                    subset_urlencoded_params = urlencoded_params
                    first = True
                    for id in subset_ids:
                        if first:
                            first = False
                            subset_urlencoded_params = subset_urlencoded_params + '&id=' + id
                        else:
                            subset_urlencoded_params = subset_urlencoded_params + ',' + id
                    search_url = self.base + "esummary.fcgi?" + subset_urlencoded_params
                    log.Write('esummary query:'+search_url)
                    subsetData = self.RetrieveUrlContent(search_url)
                    if self.GetLastError() != 'None':
                        log.Write('in ncbiurl.eSummary, RetrieveUrlContent failed: ' + self.GetLastError())
                    data = data + subsetData

            else:
                search_url = self.base + "esummary.fcgi?" + urlencoded_params;
                log.Write('esummary query:'+search_url)
                data = self.RetrieveUrlContent(search_url)
            # wrap this in a try block so we can examine local vars in debug mode when something goes wrong
            log.Write('eFetch result:\n'+data)
            fn = self.network.GetProperty('WriteESummaryRawOutput')
            if fn:
                fd = open(fn,'a')
                fd.write(str(data))
                fd.close()
            self.ExceptionIfErrors(data,reportButDontDie=True)
            return data            
        
        except Exception, e:
            self.SetLastError( str(e) )
            log.Write(str(type(e))+': '+str(e))
            raise Exception, str(e)
            
    def eLink(self,DbSrcOfIds,DbsToLink,query_key = None,WebEnv = None,ids=None,cmd=None,linkname=None):
        """
            Get ids of objects in an NCBI data base using a query and an optional
            tag from the set defined in this class; the tag indicates the type
            of entity described in the query
        """
        log = Log('GetLinksBetweenNCBIItems')
        try:
            # there can be multiple dbs on the 'to' side
            if DbSrcOfIds not in ncbiconstants.dblist:
                raise Exception, 'DbSrcOfIds ' + str(DbSrcOfIds) + ' not in legal db list'
            dbs = DbsToLink.split(',')
            for a_db in dbs:
                if a_db not in ncbiconstants.dblist:
                    raise Exception, 'DbsToLink db ' + str(a_db) + ' not in legal db list'
            
            if linkname != None and linkname not in ncbiconstants.linklist:
                raise Exception, 'linkname ' + str(linkname) + ' not in legal linkname set'
            
            if (WebEnv == None or query_key == None) and (ids == None):
                raise Exception, 'must pass either a list of ids or both a webenv and query_key'

            if (WebEnv == None or query_key == None) and (ids != None and len(ids) == 0):
                log.Write( 'WebEnv or query_key not passed, and empty ID set:' + \
                        ' Did prior query fail to get results?' )

            if (WebEnv != None and query_key != None) and ids != None:
                log.Write( 'Both a list of ids and a webenv and query_key were passed; using id set with %d ids' % len(ids) )
            
                
#            usehistory = 'y'
            
            params = {
                'dbfrom' : DbSrcOfIds,
                'db' : DbsToLink,
#                'usehistory' : usehistory,
                'tool' : self.tool,
#                'retmode' : 'xml',
#                'rettype' : 'uilist',
                }

            if ids == None \
               and WebEnv != None and len(WebEnv) > 0 \
               and query_key != None and len(query_key) > 0:
                params['WebEnv'] = WebEnv
                params['query_key'] = query_key
                
            if cmd:
                params['cmd'] = cmd
                
            if linkname != None:
                params['linkname'] = linkname
                
            email = self.network.GetProperty('email')
            if email:
                params['email'] = email

            # append ids to params, if they were passed in, but urlencode the others first
            urlencoded_params = urlencode(params)
            if (ids) and 'WebEnv=' not in urlencoded_params:
                for id in ids:
                    urlencoded_params = urlencoded_params + '&id=' + id
            search_url = self.base + "elink.fcgi?" + urlencoded_params;
            log.Write('elink query:'+search_url)
            data = self.RetrieveUrlContent(search_url)
            # stub for the moment
            return data
            """
            query_key = re.findall('<QueryKey>(.*)<\/QueryKey>',data,re.S)[0]
            WebEnv = re.findall('<WebEnv>(.*)<\/WebEnv>',data,re.S)[0]
            ids = re.findall('<Id>(.*)<\/Id>',data)
            self.ExceptionIfErrors(data)
            return (query_key,WebEnv,ids)
            """
        except Exception, e:
            self.SetLastError( str(e) )
            log.Write(str(type(e))+': '+str(e))
            raise
        
    def RetrieveUrlContent(self,theUrl=None,getTitleOnly=False):
        page = Url.RetrieveUrlContent(self,theUrl)
        self.thePage = None
        return page
        

def main(test):
    myLog = None
    try:
        from object import Object
        testnet = Object()
        testnet.SetProperty('email','dalehuns@umich.edu')
        testnet.SetProperty('NCBIResultSetSizeLimit',10)
        workingDir=urlutils.GetConfigValue('workingDir')
        os.chdir(workingDir)
        x = NCBIUrl('Strecher VJ',_network=testnet)
        x.sleeptime = 3
        import log
        log.logging = True
        log.altfd = open(os.path.join(workingDir,'ncbiurl-log.txt'),'w')
        myLog = Log('main','test='+str(test))
        if test == 1:
            (query_key,webenv,ids) = x.GetIdsOfNCBIItems(query='TRP-2',db=ncbiconstants.PROTEIN,tag=ncbiconstants.PROTEIN_NAME)
            print (x.GetLastSuccessfulQuery())
            data = x.eFetch(db=ncbiconstants.PROTEIN,WebEnv=webenv,query_key=query_key)
            print str(data)
        elif test == 2:
            (query_key,webenv,ids) = x.GetIdsOfNCBIItems(query='TRP-2',db=ncbiconstants.PROTEIN,tag=ncbiconstants.PROTEIN_NAME)
            print (x.GetLastSuccessfulQuery())
            data = x.eFetch(db=ncbiconstants.PROTEIN,ids=ids)
            print str(data)
            print (x.GetLastSuccessfulQuery())
        elif test == 3:
            (query_key,webenv,ids) = x.GetIdsOfNCBIItems(query='TRP-2',db=ncbiconstants.PROTEIN,tag=ncbiconstants.PROTEIN_NAME)
            data = x.GetLinksBetweenNCBIItems( DbSrcOfIds=ncbiconstants.GENE, \
                                            DbsToLink=ncbiconstants.PROTEIN, \
                                            linkname=ncbiconstants.PROTEIN_GENE, \
                                            WebEnv=webenv, \
                                            query_key=query_key)
            print (x.GetLastSuccessfulQuery())
            print str(data)
        elif test == 4:
            (query_key,webenv,ids) = x.GetIdsOfNCBIItems(query='TRP-2',db=ncbiconstants.PROTEIN,tag=ncbiconstants.PROTEIN_NAME)
            data = x.GetLinksBetweenNCBIItems(DbSrcOfIds=ncbiconstants.GENE,DbsToLink=ncbiconstants.PROTEIN,linkname=ncbiconstants.PROTEIN_GENE,ids=ids)
            print (x.GetLastSuccessfulQuery())
            print str(data)
        elif test == 5:
            (query_key,webenv,ids) = x.GetIdsOfNCBIItems(query='melanoma mage-1 mz2-e',db=ncbiconstants.PUBMED)
            data = x.eSummary(db=ncbiconstants.PUBMED,WebEnv=webenv,query_key=query_key)
            print (x.GetLastSuccessfulQuery())
            print str(data)
        elif test == 6:
            (query_key,webenv,ids) = x.GetIdsOfNCBIItems(query='melanoma mage-1 mz2-e',db=ncbiconstants.PUBMED)
            data = x.eFetch(db=ncbiconstants.PUBMED,WebEnv=webenv,query_key=query_key)
            print (x.GetLastSuccessfulQuery())
            print str(data)
        elif test == 7:
            (query_key,webenv,ids) = x.GetIdsOfNCBIItems(query='melanoma mage-1 mz2-e',db=ncbiconstants.PUBMED)
            data = x.eFetch(db=ncbiconstants.PROTEIN,ids=ids)
            print (x.GetLastSuccessfulQuery())
            print str(data)
        elif test == 8:
            (query_key,webenv,ids) = x.GetIdsOfNCBIItems(query='melanoma mage-1 mz2-e',db=ncbiconstants.PUBMED)
            dbs = ncbiconstants.ConcatDBNames( (ncbiconstants.PROTEIN,ncbiconstants.GENE) )
            data = x.GetLinksBetweenNCBIItems( DbSrcOfIds=ncbiconstants.PUBMED, \
                                            DbsToLink=dbs, \
                                            WebEnv=webenv, \
                                            query_key=query_key)
            print (x.GetLastSuccessfulQuery())
            print str(data)
        elif test == 9:
            query='melanoma mage-1 mz2-e'
            (query_key,webenv,ids) = x.GetIdsOfNCBIItems(query=query,db=ncbiconstants.PUBMED)
            print (x.GetLastSuccessfulQuery())
            print str(ids)
            dbs = ncbiconstants.ConcatDBNames( (ncbiconstants.PROTEIN,ncbiconstants.GENE) )
            data = x.GetLinksBetweenNCBIItems(DbSrcOfIds=ncbiconstants.PUBMED,DbsToLink=dbs,ids=ids)
            print (x.GetLastSuccessfulQuery())
            fd = open(os.path.join(urlutils.GetConfigValue('workingDir'),'elinkoutput09.txt'),'w')
            fd.write(str(data))
            fd.close()
            print 'all done!'

        elif test == 10:
            query='depression gene protein'
            (query_key,webenv,ids) = x.GetIdsOfNCBIItems(query=query,db=ncbiconstants.PUBMED,retmax=10)
            print (x.GetLastSuccessfulQuery())
            print str(ids)
            dbs = ncbiconstants.ConcatDBNames( (ncbiconstants.PROTEIN,ncbiconstants.GENE) )
            data = x.GetLinksBetweenNCBIItems(DbSrcOfIds=ncbiconstants.PUBMED,DbsToLink=dbs,ids=ids)
            print (x.GetLastSuccessfulQuery())
            fd = open(os.path.join(urlutils.GetConfigValue('workingDir'),'elinkoutput10.txt'),'w')
            fd.write(str(data))
            fd.close()
            print 'all done!'

        elif test == 11:
            qry = 'BRAF[GENE]'
            (query_key,webenv,ids) = x.GetIdsOfNCBIItems(query=qry,db=ncbiconstants.GENE,retmax=10)
            print (x.GetLastSuccessfulQuery())
            print str(ids)
            dbs = ncbiconstants.ConcatDBNames( (ncbiconstants.PROTEIN,ncbiconstants.NUCLEOTIDE,ncbiconstants.SNP) )
            data = x.GetLinksBetweenNCBIItems(DbSrcOfIds=ncbiconstants.GENE,DbsToLink=dbs,ids=ids)
            print (x.GetLastSuccessfulQuery())
            fd = open(os.path.join(urlutils.GetConfigValue('workingDir'),'elinkoutput11.txt'),'w')
            fd.write(str(data))
            fd.close()
            print 'all done!'
        log.altfd.close()
        log.altfd = None
            
            
    except Exception, e:
        print str(e)
        
        
if __name__ == '__main__':
    for i in (\
#            1,\
#            2,\
#            3,\
#            4,
#            5,
#            6,
#            7,
#            8,
#            9,
#            10,
            11,
            ):
        main(i)
    
