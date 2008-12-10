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
The SearchEngineTree class creates a network (actually two networks, one for URLs
and one for their domains) by generating a tree of objects from a search engine
query results page. 
"""

import re
import string
import sys
import os
import urllib
import socket

from object import Object
from url import Url, DomainFromHostName
from urlparse import urlparse
from urlnetitem import UrlNetItem
from domainnetitem import DomainNetItem
from log import Log, logging, file_only
import log
from urltree import UrlTree
from urlutils import *


     
###################################################################
######### out-of-the-box probability vector generators ############
###################################################################



def computeDescendingStraightLineProbabilityVector(network,numberOfSiblings,parentProbability):
    """
        Use a tailored algorithm to generate the probability distribution for the children of this UrlNetItem.
        Set the 'pos_prob' property on each child item to its probability from the distribution.
        The sum of the probabilities in this distribution must add up to the value passed as parentProbability.
        Invoke the same function recursively on each child item, passing the network, the child item,
        and its probability from the distribution.
    """
    network.ResetLastError()
    probabilityVector = None
    try:
        log = Log("SearchEngineTree module's computeDescendingStraightLineProbabilityVector")
        probabilityVector =  [0.0] * numberOfSiblings
        if parentProbability <= network.probabilityDefault:
            return probabilityVector
        else:
            # construct a probability vector for this item
            denominator = 0
            # sum up the numbers 1..n where n is the number of children
            for i in range(1,numberOfSiblings+1):
                denominator = denominator + i
            """
                First, create a list of numbers the size of the number of siblings (we'll call it N), 
                where the values are the numbers 1..N in reverse order - e.g., for number of siblings = 5,
                the list will be [5,4,3,2,1]). Compute a value we'll call 'denominator' by summing the numbers
                in this list.
                Then divide each value in the list by the computed denominator, and multiply that fraction 
                by the parent probability to compute this rank's proportion of the parent probability. 
                This produces a downsloped probability distribution, with the first anchor in the page
                having the highest proportion of the parent probability. In the example list above, if the
                parent probability is .5, the denominator is 15, so the computed probabilities will be the list
                [5/15*.5,4/15*.5,3/15*.5,2/15*.5,1/15*.5] or [0.6667,0.1333,0.1000,0.0667,0.0333]
            """
            for i in range(1,numberOfSiblings+1):
                # vector is zero-based, range is 1-based hence [i-1] indexing
                probabilityVector[i-1] = (float(numberOfSiblings-i+1)/denominator)*parentProbability
                if probabilityVector[i-1] <= network.probabilityDefault:
                    probability = 0.0
                
        return probabilityVector
    except Exception, e:
        network.SetLastError( "in SearchEngineTree module's computeDescendingStraightLineProbabilityVector: " + str(e) )
        raise Exception, e
        pass

        
def computeEqualProbabilityVector(network,numberOfSiblings,parentProbability):
    """
        Create a distribution where each child has an equal share of the parent's probability.
    """
    network.ResetLastError()
    try:
        log = Log('SearchEngineTree.computeEqualProbabilityVector')
        if parentProbability/float(numberOfSiblings) <= network.probabilityDefault:
            return [0.0] * numberOfSiblings
        return [parentProbability/float(numberOfSiblings)] * numberOfSiblings
    except Exception, e:
        network.SetLastError( "in SearchEngineTree module's computeEqualProbabilityVector: " + str(e) )
        raise Exception, e


     
###################################################################
###################################################################
###################################################################

class SearchEngineTree(UrlTree):
    """
    Class representing a tree of SearchEngine result set URLs
    """
    probabilityVector = None
    probabilityDefault = None
    topLevelUrls = None
    def __init__(self,
                 _maxLevel = 2,
                 _singleDomain=False,
                 _urlclass=Url,
                 _resultLimit=10,
                 _typeSpecificQueryFormatter=None,
                 _showLinksToOtherDomains=False,
                 _workingDir=None, 
                 _redirects = None,
                 _ignorableText = None,
                 _truncatableText = None,
                 _default_socket_timeout = 15,
                 _sleeptime = 0,
                 _userAgent=None,
                 _netItemClass = UrlNetItem,
                 _useHostNameForDomainName = False,
                 _probabilityVector = None,
                 _probabilityVectorGenerator = computeEqualProbabilityVector,
                 _probabilityDefault = 0.0001):
        try:
            log = Log('SearchEngineTree ctor')
            #
            # Most of the work is done by the parent class. All we do
            # here is specify what class to use for constructing Url
            # instances. We need to use a descendant of the Url class
            # for this purpose.
            #
            UrlTree.__init__(self,
                             _maxLevel,
                             _urlclass=_urlclass,
                             _singleDomain=False, 
                             _showLinksToOtherDomains=False,
                             _workingDir=_workingDir, 
                             _redirects = _redirects,
                             _ignorableText = _ignorableText,
                             _truncatableText = _truncatableText,
                             _default_socket_timeout = _default_socket_timeout,
                             _sleeptime=_sleeptime,
                             _userAgent=_userAgent,
                             _netItemClass = _netItemClass,
                             _useHostNameForDomainName = _useHostNameForDomainName)
            self.SetProperty('numSearchEngineResults',_resultLimit)
            if (_typeSpecificQueryFormatter):
                self.SetProperty('typeSpecificQueryFormatter',_typeSpecificQueryFormatter)

            # if a probability vector has been passed, save it for later                
            self.probabilityVector = _probabilityVector
            self.probabilityDefault = _probabilityDefault
            self.probabilityVectorGenerator = _probabilityVectorGenerator
            # ensure we have a vector generator
            if self.probabilityVector != None and self.probabilityVectorGenerator == None:
                self.probabilityVectorGenerator = computeEqualProbabilityVector
            
            self.topLevelUrls = None
            if self.probabilityVector != None:
                proplist = self.GetProperty('additionalUrlAttrs')
                if proplist == None:
                    proplist = []
                proplist.append(\
                    ('pos_prob','DOUBLE',)\
                    )
                self.SetProperty('additionalUrlAttrs',proplist)
            
        except Exception, e:
            self.SetLastError('in SearchEngineTree:__init__: ' + str(e))

    def FormatSEQuery(self,freeTextQuery,args=None):
        """ This function can be directly overridden in the derived class, or a property
            can be set to provide a query formatter specific to the situation of the moment.
            This is especially useful for networks that have multiple node types requiring
            different queries, e.g., a network that consists of author, document, and
            semantic tag node types.

            If the function to be used is a member on a class derived from SearchEngineTree, the
            method signature should be the same as this function:

                def myTagQueryFormatter(self,freeTextQuery,args=None):
                
            If the function is defined outside a derived class, it should expect a SearchEngineTree
            instance reference as the first argument, so the signature can look like this:

                def myTagQueryFormatter(myDerivedClassInstance,freeTextQuery,args=None):
                
            In either case, the SetProperty call should look like this:

                self.SetProperty('typeSpecificQueryFormatter',self.myTagQueryFormatter)

            Either form should return a formatted query. By default, as you will see below,
            this function returns the input query as the output.
        """
        typeSpecificQueryFormatter = self.GetProperty('typeSpecificQueryFormatter')
        if typeSpecificQueryFormatter:
            # potentially dynamically selected query formatter
            return typeSpecificQueryFormatter(self,freeTextQuery,args)
        else:
            return freeTextQuery
        pass


    def GetSEResultSet(self,query,putRoot=False):
        try:
            queryURL = self.FormatSEQuery(query)
            url = self.urlclass(_inboundUrl=queryURL,_network=self)
            Urls = url.GetAnchorList()
            if putRoot:
                self.PutRootUrl(queryURL)
            return (queryURL,url,Urls)
        except Exception, e:
            raise Exception, 'in SearchEngineTree.BuildUrlTree: ' + str(e)

    def SetFilenameFromQuery(self,freeTextQuery):
        # create a name we can use for writing a file with the result set URLs later
        name = ''
        for c in freeTextQuery.lower():
            if c in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZO123456789-_':
                name = name + c
            else:
                name = name + '_'
        if len(name) == 0:
            name = 'googletree_query'
        timestamp = self.GetProperty('timestamp')
        if not timestamp:
            timestamp = GetTimestampString()
        self.SetProperty('SEQueryFileName', timestamp + '-' + name + '.txt')

           
    def BuildUrlTree(self,startUrl,parentItemIdx=None,currentLevel=None,alreadyMassaged=False):
        """
        Override parent in order to format the query. Pass query in startUrl
        in free text form, just as you would enter it in Search Engine's search box;
        we handle the URL-encoding.

        The top-level call should leave currentLevel set to None. This function is called  
        called recursively, and only the top-level URL is a class-composed SE query. Absence of
        a currentLevel setting tells the function that this is the top level
        """
        log = Log('SearchEngineQueryTree.BuildUrlTree','startUrl=' + str(startUrl) + '\nparent idx=' + str(parentItemIdx) + '\nlevel=' + str(currentLevel))
        try:
            if currentLevel == None and '://' not in startUrl:
                (queryURL,url,Urls) = self.GetSEResultSet(query=startUrl,putRoot=True)
                ret = self.BuildUrlForest(self, Urls, level=1, parentIdx=parentItemIdx)
                return ret
            else:
                if currentLevel == None:
                    currentLevel = 0
                ret = UrlTree.BuildUrlTree(self,startUrl,parentItemIdx,currentLevel,alreadyMassaged)
                    
                return ret
        except Exception, e:
            raise Exception, 'in SearchEngineTree.BuildUrlTree: ' + str(e)

    def BuildUrlTreeWithPlaceholderRoot(self,rootPlaceholder,query):
        """
        Override parent in order to format the query. Pass query as you would enter it in SE's search box;
        we handle the URL-encoding.
        """

        try:
            (queryURL,url,Urls) = self.GetSEResultSet(query=query,putRoot=False)
            
            return UrlTree.BuildUrlTreeWithPlaceholderRoot(self,rootPlaceholder,Urls)
        except Exception, e:
            raise Exception, 'in SearchEngineTree.BuildUrlTreeWithPlaceholderRoot: ' + str(e)


    def BuildUrlForestWithPhantomRoot(self,query):
        """
        Given a root URL that is to be processed recursively but not included
        in the network itself, build a tree by calling BuildUrlTree
        successively with each url in the "phantom" URL's anchor list.
        The phantom URL in this case is a SE query URL we create,
        and you want the network to have only the results and not the
        search engine page itself. 
        """
        self.ResetLastError()
        log = Log('SearchEngineTree.BuildUrlForestWithPhantomRoot', query)
        try:
            (queryURL,url,anchorlist) = self.GetSEResultSet(query=query,putRoot=False)
            self.isPhantomRoot=True
            phantomRoot = queryURL
            parts = urlparse(phantomRoot)
            self.rootDomain = DomainFromHostName(parts.hostname)
            self.rootScheme = parts.scheme
            self.rootHost = parts.hostname
            myBase = phantomRoot
            if len(anchorlist) == 0:
                return False # no outlinks is *not* OK
            url = None # free up memory

            successful = UrlTree.BuildUrlForest(self,Urls=anchorlist,parentBase=myBase)
            if not successful:
                log.Write( 'BuildUrlForest may have failed for url: ' + str(phantomRoot) )
            return True
        except Exception, e:
            self.SetLastError('in SearchEngineTree.BuildUrlForestWithPhantomRoot: ' + str(e)\
                              + '\nquery: ' + query 
                              )
            return False

    def AssignTopLevelProbabilities(self):
        """
        Assign hit probabilities by position in the set of result set urls, based
        on a probability distribution established when creating the tree. 
        """
        self.ResetLastError()
        log = Log('SearchEngineTree.AssignTopLevelProbabilities')
        try:
            if self.topLevelUrls == None or self.probabilityVector == None:
                return
            
            for i in range(0,len(self.topLevelUrls)):
                self.topLevelUrls[i] = self.topLevelUrls[i].split('#')[0]    
                while self.topLevelUrls[i][-1:] == '/':
                    self.topLevelUrls[i] = self.topLevelUrls[i][:-1]
                
                item = self.GetUrlNetItemByUrl(self.topLevelUrls[i])
                if not item:
                        log.Write( 'self.GetUrlNetItemByUrl failed for top-level url #' + str(i+1) + ': ' + str(self.topLevelUrls[i]) )
                        continue
                if item.GetProperty('pos_prob') == None:
                    if i < len(self.probabilityVector):
                        item.SetProperty('pos_prob',self.probabilityVector[i])
                        if item.GetNumberOfChildren() > 0:
                            self.AssignProbabilitiesToChildUrls(item,self.probabilityVector[i])
                    else:
                        item.SetProperty('pos_prob',self.probabilityDefault)
                        if item.GetNumberOfChildren() > 0:
                            self.AssignProbabilitiesToChildUrls(item,self.probabilityDefault)
                else:
                    old_prob = item.GetProperty('pos_prob')
                    if i < len(self.probabilityVector):
                        # only override if we can do better than the probability already set
                        if self.probabilityVector[i] > old_prob:
                            item.SetProperty('pos_prob',self.probabilityVector[i])
                        if item.GetNumberOfChildren() > 0:
                            self.AssignProbabilitiesToChildUrls(item,self.probabilityVector[i])
                    else:
                        item.SetProperty('pos_prob',self.probabilityDefault)
                        if item.GetNumberOfChildren() > 0:
                            self.AssignProbabilitiesToChildUrls(item,self.probabilityDefault)
            return True
        except Exception, e:
            self.SetLastError( 'in SearchEngineTree.AssignTopLevelProbabilities: ' + str(e) )
            return False

    def AssignProbabilitiesToChildUrls(self,thisItem,theProbabilityOfThisItem):
        """
        Since the outlinks of the top-level URLs are encountered dynamically, we must compute
        the probability of a seeker choosing each such link, as a proportion of the probability
        assigned at the top level. This function calls the external function assigned to the 
        member variable 'probabilityVectorGenerator', which was initialized by an argument to 
        the constructor.
        """
        self.ResetLastError()
        try:
            log = Log('SearchEngineTree.AssignProbabilitiesToChildUrls')
            numberOfSiblings = thisItem.GetNumberOfChildren()
            # the call looks strange because we shouldn't have to pass 'self' explicitly to a class
            # function, but self.probabilityVectorGenerator is not a class function, it's a class
            # data member holding the address of a vector generator outside the class to which the class
            # is delegating the task of creating a vector of probabilities for child nodes.
            probabilityVector = self.probabilityVectorGenerator(self,numberOfSiblings,theProbabilityOfThisItem)
            i = 0
            for id in thisItem.GetChildren():
                probability = probabilityVector[i]
                i = i + 1
                item = self.GetUrlNetItemByIndex(id)
                pos_prob = item.GetProperty('pos_prob')
                if pos_prob == None:
                    item.SetProperty('pos_prob',probability)
                    if item.GetNumberOfChildren() > 0:
                        # assume for now that child probabilities are distributed evenly
                        # one could also try assuming all child URLs would be visited
                        self.AssignProbabilitiesToChildUrls(item,probability)
                elif pos_prob < probability:
                    item.SetProperty('pos_prob',probability)
                    if item.GetNumberOfChildren() > 0:
                        # recompute child probabilities
                        self.AssignProbabilitiesToChildUrls(item,probability)
                else:
                    pass # no need to change the item's probability or recompute children
            return True
        except Exception, e:
            network.SetLastError( 'in SearchEngineTree.AssignProbabilitiesToChildUrls: ' + str(e) )
            return False


    # network serializers 
    def WritePajekFile(self,netname,filename,doDomains=True,doOnlyDomains=False,useTitles=False):
        ### PAJEK
        stream = None
        log = Log('WritePajekFile',netname+':'+filename)
        maxIdx = len(self.UrlNetItemByIndex.keys())
        try:
            stream = open(filename + ".paj","w")
            self.WritePajekStream(netname,stream,doDomains,doOnlyDomains=doOnlyDomains,useTitles=useTitles)

            # calculate and write probability vector, if appropriate
            if not self.probabilityVector:
                return
        
            if not self.AssignTopLevelProbabilities():
                raise Exception, self.GetLastError()
            
            stream.write('\n\n*Vector PositionalProbabilities\n*Vertices ' + str(maxIdx) + ' \n')
            itemlist = {}
            self.MapFunctionToUrlItemList(
                    BuildListOfItemIndicesWithPropertyValueLookup,
                    args=['pos_prob',itemlist,0.0])
            keys = itemlist.keys()
            keys.sort()
            for idx in keys:
                try:
                    value = itemlist[idx]
                except Exception, e:
                    log.Write('in SearchEngineTree.WritePajekFile, no value for item with index %d' % (idx))
                    value = None
                if value == None:
                        value = 0.0
                valuestr = '%.4f' % (value)
                spaces = ' '*(8-len(valuestr))
                stream.write(spaces + str(value) + '\n')
                if idx > maxIdx:
                    self.SetLastError( 'too many keys in partition list: ' + str(idx) )


            stream.close()
        except Exception, e:
            self.SetLastError('In SearchEngineTree.WritePajekFile: ' + str(e))
            if stream:
                stream.close()


def main():
    # dir to write to
    workingDir =urlutils.GetConfigValue('workingDir')
    log.logging=True
    log.altfd=open('googletree.log','w')
    myLog = Log('main')
    
    x = SearchEngineTree(_maxLevel=2,
                       _workingDir=workingDir,
                   _resultLimit=10)
    
    x.BuildUrlForestWithPhantomRoot('smoking cessation')

    #x = UrlTree(_maxLevel=3,_workingDir=workingDir)
    #x.BuildUrlForest('http://www.livejournal.com',urls)
    
    x.MapFunctionToUrlNetwork(PrintHierarchy,args=sys.stderr)
    x.MapFunctionToDomainNetwork(PrintHierarchy,args=sys.stderr)
    x.WritePajekFile('googletree-smokingcessation','googletree-smokingcessation')
    x.WriteGuessFile('googletree-smokingcessation_urls')            # url network
    x.WriteGuessFile('googletree-smokingcessation_domains',False)      #domain network
    log.altfd.close()
    log.altfd = None

if __name__ == '__main__':
    main()
    sys.exit(0)

    