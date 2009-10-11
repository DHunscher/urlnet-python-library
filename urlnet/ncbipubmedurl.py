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
from Ft.Xml import InputSource, Sax

from url import Url
from log import Log
from ncbiurl import NCBIUrl
import ncbiconstants

#################### the NCBIUrl class ######################
class NCBIPubMedUrl(NCBIUrl):
    "A class to get a list of co-authors from Pub Med "
    key = None
    limit = 10
    root = None
    url = None
    methodPrefix = None
    base = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    tool = 'UrlNet Python Library'
    
    def __init__(self, _inboundUrl, _network=None, limit=None, start=1):
        """constructor can take a url and init (a flag).
        If init is true, get page and anchors for url
        during construction. Get errors occurring in constructor
        by calling lastError().
        """
        
        # Don't allow a GetPage call in the Url ctor - it would
        # waste time, because we do our own GetPage later, with
        # the NCBI CoAuthor version of GetAnchorList
        
        log = Log('NCBIPubMedUrl ctor',_inboundUrl)
        NCBIUrl.__init__(self,_inboundUrl=_inboundUrl,_network=_network,limit=limit, start=1)
        
    def GetPublications(self,author):
        """
        Returns a list of dicts.
        """
        log = Log('GetPublications')
        #print "00"
        if author == None:
            #print "01"
            return []
        #elif self.anchors != None:
        #   #print "02"
        #    return self.anchors
        else:
            #print "03"
            try:
                # get ids via GetIdsOfPubsByAuthor
                (query_key,WebEnv,ids) = self.GetIdsOfPubsByAuthor(author)
                
                # get data set document via eFetch    
                data = self.eFetch(query_key,WebEnv,ids)
                 
                return self.ParseDocsFromPubMedAbstractDocument(data)

                #self.anchors = authorlist
                #return self.authorlist
                    
            except Exception, inst:
                self.SetLastError(str(inst))
                raise Exception, str(inst)

        
    def GetCoAuthorList(self,author):
        """
        Get list of co-authors from Pub Med.
        """
        log = Log('GetCoAuthorList')
        #print "00"
        if author == None:
            #print "01"
            return []
        #elif self.anchors != None:
        #   #print "02"
        #    return self.anchors
        else:
            #print "03"
            try:
                # get ids via GetIdsOfPubsByAuthor
                (query_key,WebEnv,ids) = self.GetIdsOfPubsByAuthor(author)
                
                # get data set document via eSummary    
                data = self.eSummary(query_key,WebEnv,ids)

                 
                #print data

                pubidsAndAuthors = self.ParseAuthorsFromDocSums(data,author)
                authors = []
                for item in pubidsAndAuthors:
                    authors = authors + item[1]
                authorlist = []
                for a in authors:
                    if a not in authorlist and a != author:
                        authorlist.append(a)
                return authorlist    

                #self.anchors = authorlist
                #return self.authorlist
                    
            except Exception, inst:
                self.SetLastError( str(inst) )
                return []

       
    def GetIdsOfPubsByAuthor(self,author):
        """
            Get ids of publications by this author
        """
        log = Log('GetIdsOfPubsByAuthor')
        try:
            return self.GetIdsOfNCBIItems(author,'pubmed',ncbiconstants.AUTHOR)
        except Exception, e:
            self.SetLastError( str(e) )
            raise Exception, str(e)

    def ParseAuthorsFromDocSums(self,data,root):
        """
            ParseAuthorsFromDocSums gets the list of authors associated with a
            PubMed document summary from eSummary.
        """
        
        log = Log('ParseAuthorsFromDocSums')

        try:
            return self.ParseItemsFromDocSums(data,'Author',root)
        except Exception, e:
            self.SetLastError(str(e))
            raise Exception, str(e)


    def ParseDocsFromPubMedAbstractDocument(self,data):
        """
            ParseDocsFromPubMedAbstractDocument returns a list of dicts. Each contains
                title
                authorlist # list of co-authors of paper
                meshlist # list of MeSH headings
                # later...
                pmid
                jname
                volume
                issue
                pubyear
                pubmonth
                
        """
        log = Log('ParseDocsFromPubMedAbstractDocument')

        class doc_processor:
            def __init__(self):
                pass # for now
                
            def startDocument(self):
                self.in_title = False
                self.in_article = False
                self.in_meshterm = False
                self.in_author = False
                self.in_lastname = False
                self.in_initials = False
                self.in_pmid = False
                """
                self.in_journal = False
                self.in_jtitle = False
                self.in_volume = False
                self.in_issue = False
                self.in_year = False
                self.in_month = False
                self.jtitle = ''
                self.volume = ''
                self.issue = ''
                self.year = ''
                self.month = ''
                """
                self.pmid = ''
                self.title = ''
                self.authname = ''
                self.meshterm = ''
                self.itemList = {}
                self.error = ''
                self.article = {}
                
            def startElementNS(self, name, qname, attribs):
                #if name[1] in (u'LastName',u'Initials',u'Author',u'PubmedArticle',u'MeshHeading',u'ArticleTitle'):
                #    print name[1]
                #print name
                #print attribs
                if self.in_article:
                    if self.in_author:
                        if name[1] == u'LastName':
                            self.in_lastname = True
                        elif name[1] == u'Initials':
                            self.in_initials = True
                    elif unicode(name[1]) == u'Author':
                        self.in_author = True
                        self.authname = ''
                        self.initials = ''
                    elif unicode(name[1]) == u'ArticleTitle':
                        self.in_title = True
                        self.title = ''
                    elif unicode(name[1]) == u'MeshHeading':
                        self.in_meshterm = True
                        self.meshterm = ''
                    elif unicode(name[1]) == u'PMID':
                        self.in_pmid = True
                        self.pmid = ''
                    """elif unicode(name[1]) == u'Journal':
                        self.in_journal = True
                        self.jtitle = ''
                        self.volume = ''
                        self.issue = ''
                        self.year = ''
                        self.month = ''
                    """                        
                elif unicode(name[1]) == u'PubmedArticle':
                    self.in_article = True
                    self.initArticle()
                return

            def initArticle(self):
                self.title = ''
                self.article = {}
                self.article['authorlist'] = []
                self.article['meshlist'] = []
                self.article['title'] = ''
                self.article['pmid'] = ''
                
            def endElementNS(self, name, qname):
                #print name[1]
                if self.in_article:
                    if self.in_author:
                        if self.in_lastname and unicode(name[1]) == u'LastName':
                            self.in_lastname = False
                        elif self.in_initials and unicode(name[1]) == u'Initials':
                            self.in_initials = False
                        elif unicode(name[1]) == u'Author':
                            self.in_author = False
                            authname = self.authname + ' ' + self.initials
                            self.article['authorlist'].append( str(authname.strip()) )
                            self.authname = ''
                            self.initials = ''
                    elif self.in_meshterm and unicode(name[1]) == u'MeshHeading':
                        self.in_meshterm = False
                        term = self.meshterm.strip()
                        # remove any leading or trailing colons we added in self.characters()
                        if term[0] == ':':
                            term = term[1:]
                        if term[-1:] == ':':
                            term = term[:-1]
                        self.article['meshlist'].append(str(term))
                        self.meshterm = ''
                    elif self.in_title and unicode(name[1]) == u'ArticleTitle':
                        self.article['title'] = str(self.title.strip())
                        self.in_title = False
                    elif self.in_pmid and unicode(name[1]) == u'PMID':
                        self.article['pmid'] = str(self.pmid.strip())
                        self.in_pmid = False
                        
                    elif unicode(name[1]) == u'PubmedArticle':
                        self.in_article = False
                        self.itemList[self.article['title']] = self.article
                        self.initArticle()

            def characters(self, text):
                if self.in_article:
                    if self.in_author:
                        if self.in_lastname:
                            self.authname = self.authname + text
                        elif self.in_initials:
                            self.initials = self.initials + text
                    elif self.in_title:
                        self.title = self.title + text
                    elif self.in_meshterm:
                        if len(text.strip()) == 0:
                            text = ':'
                        self.meshterm = self.meshterm + text
                    elif self.in_pmid:
                        self.pmid = self.pmid + text.strip()

            def ignorableWhitespace(self, ws):
                return

        # parse using SAX
        try:
            import xml
            factory = InputSource.DefaultFactory
            #fd = open(os.path.join(urlutils.GetConfigValue('workingDir'),'data.txt'),'w')
            #fd.write(data)
            #fd.close()
            isrc = factory.fromString(data)
            parser = Sax.CreateParser()
            handler = doc_processor()
            parser.setFeature(xml.sax.handler.feature_validation, False)
            parser.setContentHandler(handler)
            parser.parse(isrc)
            return handler.itemList
        except Exception, e:
            self.SetLastError(str(e))
            raise Exception, str(e)

def main():
    from object import Object
    import log
    import urlutils
    workingDir =urlutils.GetConfigValue('workingDir')
    log.logging = True
    log.trace = True
    log.altfd = open(os.path.join(workingDir,'log.txt'),'w')
    myLog = log.Log('main')
    testnet = Object()
    testnet.SetProperty('email','dalehuns@umich.edu')
    testnet.SetProperty('NCBIResultSetSizeLimit',10)
    testnet.SetProperty('sleeptime',3)
    x = NCBIPubMedUrl('Hunscher DA',_network=testnet)
    pubs = x.GetPublications('Hunscher DA')
    print str(pubs)
    co_authors = x.GetCoAuthorList('Hunscher DA')
    print str(co_authors)
    log.altfd.close()
    log.altfd=None
    

if __name__ == '__main__':
    main()
    exit(0)
