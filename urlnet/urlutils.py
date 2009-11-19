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
Utility functions for UrlTree and its descendant and helper classes.
"""

import re
import string
import sys
import os
import urllib
import socket

# for GetTimestampString and check for incl/excl
from time import strftime, localtime, sleep

# for read_config_file and GetConfigValue
from os.path import exists, join, abspath
from os import pathsep, environ
from string import split

# for saveTree and loadTree
import cPickle as pickle

from object import Object
from url import Url, DomainFromHostName
from urlparse import urlparse, urlunparse
from urllib import urlencode
from urlnetitem import UrlNetItem
from domainnetitem import DomainNetItem
from log import Log

# for inclusion/exclusion checker
from urllib import unquote, urlencode
from urllib2 import urlopen, Request
from htmllib import HTMLParser
from formatter import NullFormatter, AbstractFormatter, DumbWriter
import StringIO
import gzip
import zlib
import re

# URI schemes we will try to follow
PERMISSIBLE_SCHEMES = ('http','https','ftp','sftp')

#directions to walk the entire net or a subnet from a given node
SEARCH_DOWN = 0
SEARCH_UP = -1

# name of file (to be found on path) where we can find configuration information
URLNET_CFG = 'urlnet.cfg'

def read_config_file():
    """
    Find config file on the path given in os.environ['path']
    if file is found, return its lines as a list; otherwise
    return None.
    """
    file_found = 0
    filename = URLNET_CFG
    search_path=os.environ['PATH']
    paths = ['.',]
    # allow for the possibility that there is no HOME env variable
    home = None
    try:
        home = os.environ['HOME']
    except Exception, e:
        pass
    # 
    if home != None and len(home) > 0:
        paths.append(home)
    paths = paths + split(search_path, pathsep)
    
    for path in paths:
        if exists(join(path, filename)):
            file_found = 1
            break
    if file_found:
        path = abspath(join(path, filename))
        try:
            fd = open(path)
            lines = fd.readlines()
            fd.close()
            return lines
        except Exception, e:
            return None
    else:
        return None

def GetConfigValue(name):
    '''
    Get a single configuraton value by name. If the config file is missing
    or has no lines, None is returned. If the desired name is not found,
    None is returned. If the line is malformed (i.e. not in the form
    <name>=<value>), None is returned. Otherwise, the value is returned,
    stripped of leading and trailing spaces. The name is case-insensitive,
    but the value's case status is maintained as-is.
    '''
    lines = read_config_file()
    if lines == None:
        return None
    try:
        name = name.strip().lower()
        for line in lines:
            line = line.strip()
            if len(line) > 0:
                # ignore comments
                if line[0] == '#':
                    continue
                parts = line.split('=')
                if len(parts) != 2:
                    continue
                ename = parts[0].strip().lower()
                value = parts[1].strip() # don't lower-case; path may be case-sensitive
                if ename == name and len(value) > 0:
                    return(value)
        return None
    except Exception, e:
        return None

def GetTimestampString():
    '''
    Get a text string containing the current local time in the form
    yyyy-mm-dd--hh-mi-ss. Used in creating unique filenames.
    '''
    return strftime('%Y-%m-%d--%H-%M-%S',localtime())
    

def RemoveRealmPrefix(name):
    '''
    Remove the realm prefix (e.g., ftp://) from a url.
    '''
    parts = urlparse(name)
    if len(parts[0]) > 0:
        parts = list(parts)
        parts[0] = ''
        name = urlunparse(parts)
        while len(name) > 0 and name[0] == '/':
                name = name[1:]
    return name
                
        
        
def RemoveNonPrintableChars(name):
    '''Replace control characters in a string with underscores.
    '''
    log = Log('RemoveNonPrintableChars',name)
    out = ''
    for c in name:
        if (c > ' '):
            out = out + c
        elif (c != ' '):
            out = out + '_'
    return out
        
def PrintHierarchy(item,net,level,args):
    """ A mapper function to handle writing a single item in printing the
        network in tab-indented format.
    """
    fd = args[0]
    useTitles = args[1]
    log = Log('PrintHierarchy',item.GetName())
    fd.write( '\t'*level )
    idx = item.GetIdx()
    name = GetNameOfItem(item,idx,useTitles)
    #name = RemoveNonPrintableChars(name)
    fd.write( name + '\n' )
    return True

def BuildListOfItemIndicesWithLevel(item,net,level,args):
    """ A mapper function to build a list of item indices with
       the highest level (in the upside-down tree) at which the
       item occurs, and its frequency *at that level*.
    """
    log = Log('BuildListOfItemIndicesWithLevel')
    dict = args
    # get index 
    idx = item.GetIdx()
    try:
        pair = dict[idx]
        # keep track of the lowest level (highest in the upside down tree) only
        if level < pair[0]:
            pair[0] = level
            pair[1] = 1
        else:
            pair[1] = pair[1] + 1
    except Exception, e:
        dict[idx]=[level,1]
    return True

def BuildListOfItemIndicesWithPropertyValueDict(item,net,level,args):
    """ A mapper function to build a list of item indices with
       the value indirectly obtained by lookup of a property
       value in a dictionary; the property name and the value
       dictionary are passed in args, along with the dictionary
       in which the output item index/lookup value pairs are stored.
    """
    log = Log('BuildListOfItemIndicesWithPropertyValueDict')
    dict = args[0]
    key = args[1]
    valuedict = args[2]
    if len(args) > 3:
        defaultValue = args[3]
    else:
        defaultValue = None
    # get index 
    idx = item.GetIdx()
    nodeType = item.GetProperty(key)
    try:
        keyval = valuedict[nodeType]
        dict[idx] = keyval
    except Exception, e:
        if defaultValue != None:
            dict[idx] = defaultValue
        else:
            raise Exception,\
                'key value not found for node type "%s": %s' % (str(nodeType),str(e))
    return True

def BuildListOfItemIndicesWithPropertyValueLookup(item,net,level,args):
    """
    build dictionary consisting of item indices as the keys and
    a property value as the associated value.
    """
    log = Log('BuildListOfItemIndicesWithPropertyValueLookup',item.GetName())
    errPrefix = 'in BuildListOfItemIndicesWithPropertyValueLookup, '
    argsType = str(type(args))
    if len(args) < 2:
        raise Exception, errPrefix + 'expected args to be property name and dict'
    if 'str' not in str(type(args[0])):
        raise Exception, errPrefix + 'first item in args must be a property name string'
    if 'dict' not in str(type(args[1])):
        raise Exception, errPrefix + 'second item in args must be a dictionary'
    try:
        value = item.GetProperty(args[0])
        if value is None:
            if len(args) > 2:
                value = args[2]
            else:
                raise Exception,'key not found'
        idx = item.GetIdx()
        dict = args[1]
        dict[idx] = value
    except Exception, e:
        #print 'in BuildListOfItemIndicesWithPropertyValueLookup: no property value for ' + args[0] \
        #      + ' in item ' + str(item.GetName())
        dict = args[1]
        idx = item.GetIdx()
        # use default, if one exists
        if len(args) > 2:
            dict[idx] = args[2]
        else:
            dict[idx]=0.0
    return True

def GetNameOfItem(item,idx,useTitles):
    '''
    Get the name of a url item, e.g. for use as the name of a vertex in
    a network. If the useTitles argument is True, the value of the
    'title' property on the UrlNetItem-descended entity passed as the item 
    argument is used as the name. If the property value is missing
    when expected, or useTitles is False, the item's GetName member
    functions is invoked to provide the value. If this function returns
    None or an empty string, a string is created using the index of the
    item prefixed by the letter 'v' for vertex.
    '''
    name = None

    if useTitles:
        name = item.GetUrl().GetProperty('title')
    if name == None or len(name) == 0:
        name = item.GetName()
    if name == None or len(name) == 0:
        name = 'v' + str(idx)
    name = name.strip()
    return name

###################################################################
#####  a set of mapper functions for building Pajek networks. #####
#####  The function names are descriptive of their function.  #####
###################################################################


def WritePajekVertex(item,net,level,args):
    log = Log('WritePajekVertex',item.GetName())
    try:
        FILE = args[0]
        useTitles = args[1]
        idx = item.GetIdx()
        name = RemoveRealmPrefix(GetNameOfItem(item,idx,useTitles))
        trimlength = net.GetProperty('nodeLengthLimit')
        if trimlength != None and len(name) > trimlength:
            name = name[0:trimlength] + '...'
        FILE.write('       ' + str(idx) + ' "' + name + '"   \n')
        return True
    except Exception, e:
        log.Write('Exception in WritePajekVertex: %s' % (str(e)))
        raise

def WritePajekArcOrEdge(fromIdx,toIdx,net,args):
    log = Log('WritePajekArcOrEdge',"%d %d" % (fromIdx,toIdx))
    try:
        FILE = args[0]
        reverseDirection = args[1]
        # get parent item
        item = net.GetUrlNetItemByIndex(fromIdx)
        # get child weight 
        weight = item.GetChildHitCount(toIdx)
        # weight can't be zero
        if weight == 0:
            weight = 1
        # if reverseDirection is true, we need to swap the from and to indices
        if reverseDirection:
            temp = fromIdx
            fromIdx = toIdx
            toIdx = temp
        FILE.write('       ' + str(fromIdx) + '       ' + str(toIdx) + ' ' + str(weight) + ' \n')
        return True
    except Exception, e:
        log.Write('Exception in WritePajekArcOrEdge: %s' % (str(e)))
        raise
     
def WritePajekDomainArcOrEdge(fromIdx,toIdx,net,args):
    log = Log('WritePajekDomainArcOrEdge',"%d %d" % (fromIdx,toIdx))
    try:
        FILE = args[0]
        reverseDirection = args[1]
            
        # get parent item
        item = net.GetDomainByIndex(fromIdx)
        # get child weight 
        weight = item.GetChildHitCount(toIdx)
        # weight can't be zero
        if weight == 0:
            weight = 1
        # if reverseDirection is true, we need to swap the from and to indices
        if reverseDirection:
            temp = fromIdx
            fromIdx = toIdx
            toIdx = temp
        FILE.write('       ' + str(fromIdx) + '       ' + str(toIdx) + ' ' + str(weight) + ' \n')
        return True
    except Exception, e:
        log.Write('Exception in WriteGuessDomainArc: %s' % (str(e)))
        raise

     
###################################################################
#####   a set of mapper functions for building pair networks ######
###################################################################

def WritePairArcOrEdge(fromIdx,toIdx,net,args):
    '''
    Use this writer function to produce a list of simple edge definitions
    (fromurl  tourl). 
    If uniquePairs is not True, write 1 edge definition per parent-child pair 
    '''
    log = Log('WritePairArcOrEdge',"%d %d" % (fromIdx,toIdx))
    try:
        FILE = args[0]
        uniquePairs = args[1]
        delimiter = args[2]
        useTitles = False # for now
        
        # get names of items
        fromItem = net.GetUrlNetItemByIndex(fromIdx)
        fromName = RemoveRealmPrefix(GetNameOfItem(fromItem,fromIdx,useTitles))
        trimlength = net.GetProperty('nodeLengthLimit')
        if trimlength != None and len(fromName) > trimlength:
            fromName = fromName[0:trimlength] + '...'
        toItem = net.GetUrlNetItemByIndex(toIdx)
        toName = RemoveRealmPrefix(GetNameOfItem(toItem,toIdx,useTitles))
        trimlength = net.GetProperty('nodeLengthLimit')
        if trimlength != None and len(toName) > trimlength:
            toName = toName[0:trimlength] + '...'
        # get child weight 
        weight = fromItem.GetChildHitCount(toIdx)
        # weight can't be zero
        if weight == 0 or uniquePairs == True:
            weight = 1
        # write simple edge definition
        while(weight > 0):
            FILE.write(str(fromName) + str(delimiter) + str(toName) + ' \n')
            weight = weight - 1
        return True
    except Exception, e:
        log.Write('Exception in WritePairArcOrEdge: %s' % (str(e)))
        raise
     
def WritePairDomainArcOrEdge(fromIdx,toIdx,net,args):
    '''
    Use this writer function to produce a list of simple edge definitions
    (fromname  toname). 
    If uniquePairs is not True, write 1 edge definition per parent-child pair 
    '''
    log = Log('WritePairDomainArcOrEdge',"%d %d args=%s" % (fromIdx,toIdx,str(args)))
    try:
        FILE = args[0]
        uniquePairs = args[1]
        # get names of items
        fromItem = net.GetDomainByIndex(fromIdx)
        fromName = fromItem.GetName()
        toItem = net.GetDomainByIndex(toIdx)
        toName = toItem.GetName()
        # get child weight 
        weight = fromItem.GetChildHitCount(toIdx)
        # weight can't be zero
        if weight == 0 or uniquePairs == True:
            weight = 1
        # write simple edge definition
        while(weight > 0):
            FILE.write(str(fromName) + '       ' + str(toName) + ' \n')
            weight = weight - 1
        return True
    except Exception, e:
        log.Write('Exception in WritePairDomainArcOrEdge: %s' % (str(e)))
        raise
     
     
###################################################################
#####   a set of mapper functions for building Guess networks #####
###################################################################

def ReplaceIllegalChars(name):
    '''
    Make a string compatible with the requirements of a Java name. 
    '''
    log = Log('ReplaceIllegalChars',name)
    out = ''
    for c in name:
        if (c >= '0' and c <= '9') or (c >= 'A' and c <= 'Z') or (c >= 'a' and c <= 'z'):
            out = out + c
        else:
            out = out + '_'
    return out
        
def WriteGuessVertex(item,net,level,args):
    '''
    Write a single Guess vertex for a url network, adding additional
    attributes per the additionalDomainAttrs argument. Each attribute
    must also be the name of a property found on each UrlNetItem 
    descendant; the value of that property must match the Java type
    of the declaration as described in urltree.WriteGuessStream.
    '''
    log = Log('WriteGuessVertex',item.GetName())
    try:
        #    nodedef = 'nodedef>name VARCHAR, url VARCHAR,domain VARCHAR'
        FILE = args[0]
        useTitles = args[1]
        additionalGuessAttrs = args[2]
        idx = item.GetIdx()
        url = GetNameOfItem(item,idx,useTitles)
        url = RemoveRealmPrefix(url)
        url = ReplaceIllegalChars(url)
        domain = item.GetDomain()
        domain = ReplaceIllegalChars(domain)
        FILE.write(domain + str(idx) + ',"' + url + '","' + domain + '",' + str(level) )
        if additionalGuessAttrs != None:
            for theDict in additionalGuessAttrs:
                attrName = theDict['attrName'] # required
                attrType = theDict['datatype'] # required
                attrDict = None
                try:
                    attrDict = theDict['dict']
                except Exception, e:
                    pass
                    
                default = None
                try:
                    default =  theDict['default'] # optional
                except Exception, e:
                    pass
                value = item.GetProperty(attrName)
                if attrDict:
                    try:
                        value = attrDict[value]
                    except Exception, e:
                        log.Write('attDict lookup on "%s" failed.' \
                                % str(value) )
                if attrType.upper() in \
                    ('VARCHAR','CHAR','DATE','TIME','DATETIME','BOOLEAN'):
                    if value is None:
                        if default:
                            value = str(default)
                        else:
                            value = ''
                    else: 
                        value = str(value)
                elif attrType.upper() in ('INT', 'TINYINT', 'BIGINT'): 
                    if value is None:
                        if default:
                            value = str(default)
                        else:
                            value = '0'
                    else:
                        value = str(value)
                else: # DOUBLE, FLOAT
                    if value is None:
                        if default:
                            value = str(default)
                        else:
                            value = '0.0'
                    else:
                        value = str(value)
                FILE.write(',%s' % (value))
        FILE.write('\n')
        return True
    except Exception, e:
        log.Write('Exception in WriteGuessVertex: %s' % (str(e)))
        raise
    
def WriteGuessArc(fromIdx,toIdx,frequency,net,args):
    log = Log('WriteGuessArc',"%d %d" % (fromIdx,toIdx))
    #    edgedef = 'edgedef>node1 VARCHAR,node2 VARCHAR,frequency INT'
    try:
        FILE = args[0]
        reverseDirection = args[1]
        fromItem = net.GetUrlNetItemByIndex(fromIdx)
        toItem = net.GetUrlNetItemByIndex(toIdx)
        fromDomain = fromItem.GetDomain()
        fromDomain = ReplaceIllegalChars(fromDomain)
        toDomain = toItem.GetDomain()
        toDomain = ReplaceIllegalChars(toDomain)
        # if reverseDirection is true, we need to swap the from and to indices
        if reverseDirection:
            temp = fromIdx
            fromIdx = toIdx
            toIdx = temp
        # frequency can't be zero
        if frequency == 0:
            frequency = 1
        FILE.write(fromDomain + str(fromIdx) + ',' + toDomain + str(toIdx) + ',' + str(frequency) + '\n')
        return True
    except Exception, e:
        log.Write('Exception in WriteGuessArc: %s' % (str(e)))
        raise
     

def WriteGuessDomainVertex(item,net,level,args):
    '''
    Write a single Guess vertex for a domain network. adding additional
    attributes per the additionalDomainAttrs argument. Each attribute
    must also be the name of a property found on each DomainNetItem 
    descendant; the value of that property must match the Java type
    of the declaration as described in urltree.WriteGuessDomainStream.
    '''
    log = Log('WriteGuessDomainVertex',item.GetName())
    #    nodedef = 'nodedef>name VARCHAR,domain VARCHAR'
    try:
        FILE = args[0]
        additionalGuessAttrs = args[1]
        idx = item.GetIdx()
        domain = item.GetName()
        domain = ReplaceIllegalChars(domain)
        FILE.write('v' + str(idx) + ',' + domain )
        if additionalGuessAttrs != None:
            for theDict in additionalGuessAttrs:
                attrName = theDict['attrName'] # required
                attrType = theDict['datatype'] # required
                try:
                    default =  theDict['default'] # optional
                except Exception, e:
                    default = None
                value = item.GetProperty(attrName)
                if attrType.upper() in ('VARCHAR','CHAR','DATE','TIME','DATETIME','BOOLEAN'):
                    if value is None:
                        if default:
                            value = str(default)
                        else:
                            value = ''
                    else: 
                        value = str(value)
                elif attrType.upper() in ('INT', 'TINYINT', 'BIGINT'): 
                    if value is None:
                        if default:
                            value = str(default)
                        else:
                            value = '0'
                    else:
                        value = str(value)
                else: # DOUBLE, FLOAT
                    if value is None:
                        if default:
                            value = str(default)
                        else:
                            value = '0.0'
                    else:
                        value = str(value)
                FILE.write(',%s' % (value))
        FILE.write('\n')
        return True
    except Exception, e:
        log.Write('Exception in WriteGuessDomainVertex: %s' % (str(e)))
        raise

def WriteGuessDomainArc(fromIdx,toIdx,frequency,net,args):
    log = Log('WriteGuessDomainArc',"%d %d" % (fromIdx,toIdx))
    #    edgedef = 'edgedef>node1 VARCHAR,node2 VARCHAR,frequency INT'
    try:
        FILE = args[0]
        reverseDirection = args[1]
        if reverseDirection:
            temp = fromIdx
            fromIdx = toIdx
            toIdx = temp
        # frequency can't be zero
        if frequency == 0:
            frequency = 1
        FILE.write('v' + str(fromIdx) + ',' + 'v' + str(toIdx) + ',' + str(frequency) + '\n')
        return True
    except Exception, e:
        log.Write('Exception in WriteGuessDomainArc: %s' % (str(e)))
        raise

def saveTree(tree,path):
    '''
    Use the Pickle module to save a UrlTree-descended instance to disk.
    '''
    
    log = Log('saveTree','path=%s' % str(path) )
    try:
        fo=open(path, 'wb')
        pickle.dump(tree,fo,-1)
        fo.close()
    except Exception, e:
        log.Write('Exception in saveTree: %s' % (str(e)))
        raise
        
     
def loadTree(path):
    '''
    Use Pickle to load a UrlTree-descended instance back into memory from
    a file saved using the saveTree function.
    '''
    
    log = Log('loadTree','path=%s' % str(path) )
    try:
        fi=open(path, 'rb')
        tree = pickle.load(fi)
        fi.close()
        return tree
    except Exception, e:
        log.Write('Exception in loadTree: %s' % (str(e)))
        raise
        
     
    
def ConvertTextFile2DOS(infilename, outfilename, removeInFileOnSuccess = True):
    '''
    Pajek is a Windows program, and always expects its file format to use
    DOS line endings (CR-LF), even when run under Wine (as I do on my Macbook
    using CrossOver). This routine is used to ensure that a Pajek output file
    always has DOS-style line endings.
    '''
    outfd = None
    infd = None
    try:
        infd = open(infilename,"rb")
        outfd = open(outfilename,"wb")
        for line in infd:
            # strip terminating newline
            if len(line) > 0 and line[-1] == '\n':
                line = line[:-1]
            if len(line) > 0 and line[-1] != '\r':
                outfd.write(line + '\r\n')
            elif len(line) == 0: # empty line
                outfd.write('\r\n')
            else:
                outfd.write(line + '\n')
        
        outfd.close()
        infd.close()
        if removeInFileOnSuccess:
            os.remove(infilename)
    except Exception, e:
        if outfd:
            outfd.close()
        if infd:
            infd.close()
        raise

#### inclusion/exclusion criteria checker ####

def GetHttpPage(network,theUrl):
    '''
    '''
    log = Log('GetHttpPage','url=%s' % (str(theUrl)))
        
    try:
    
        if network.lastPage != None and network.earlyReadSucceeded == True:
            return network.lastPage
        
        network.lastPage = None
        network.earlyReadSucceeded = True
        
        sleeptime = network.GetProperty('sleeptime')
        try:
            sleeptime = float(sleeptime)
        except Exception, e:
            log.Write('while converting sleeptime "%s" to float, exception: %s' % (str(sleeptime),str(e)) )
            sleeptime = 1.0
        # get text of page here so we can check it.
        user_agent = network.GetProperty('user-agent')
        req_headers = network.GetProperty('request-headers')
        if req_headers == None:
            req_headers = {}
        if 'User-Agent' not in req_headers.keys():
            if user_agent:
                req_headers['User-Agent'] = user_agent
            else:
                # req_headers['User-Agent'] = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT;'
                req_headers['User-Agent'] = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT; UrlNet Python Library;'
        # accept compressed content if available
        try:
            accept = req_headers['Accept-Encoding']
            if 'gzip' not in accept.lower():
                if accept[-1] != ',':
                    accept = accept + ','
                accept = accept + 'gzip,'
                req_headers['Accept-Encoding'] = accept
        except:
            req_headers['Accept-Encoding'] = 'gzip'
            
        req = Request(url=theUrl,headers=req_headers)
        last_query = theUrl
        try:
            urlobject = urlopen(req)
            zipped = False
            encoding = urlobject.info().get("Content-Encoding")
            if encoding in ('gzip', 'x-gzip'):
                zipped = True
            page = urlobject.read()
            if zipped:
                log.Write('%s was compressed, size=%d' % (theUrl,len(page)))
                data = gzip.GzipFile('', 'rb', 9, StringIO.StringIO(page))
                page = data.read()
                log.Write('decompressed size: %d' % (len(page)))
        except Exception, e:
            log.Write('on %s, exception: %s' % (str(theUrl), str(e)))
            network.lastPage = None
            network.earlyReadSucceeded = False
            return None
        # save page so Url class doesn't have to fetch it a second time.
        network.lastPage = page
        network.earlyReadSucceeded = True
    
        # be polite!
        if sleeptime:
            sleep(sleeptime)
        return page
    
    except Exception, inst:
        theError = 'GetHttpPage: ' + str(type(inst)) + '\n' + str(inst) + '\non URL ' + theUrl
        network.SetLastError ( theError )
        log.Write(theError)
        #print theError
        return None


def CheckInclusionExclusionCriteria(network,theUrl,level):
    '''
    See if we need to check for presence of one of a set of
    text string patterns, each of which is a plain text string or a 
    regular expression pattern. Return True if (any include pattern
    is found OR there are no include patterns), AND (no exclude pattern 
    is found OR there are no exclude patterns), False otherwise.
    
    For optimum flexibility, regular expressions can be used in the
    include/exclude patterns. the search function from the re module
    is used to check for the presence of a pattern. It is possible
    to specify the flags argument to re.search for both the include
    and exclude pattern searches. 
    
    '''
    NO_INCLEXCL = 42 # This is just a magic number for use in
                     # the context of this function only
                    
    log = Log('CheckInclusionExclusionCriteria','url=%s' % (str(theUrl)))
        
    try:
        # if this routine were not set up as the inclusion/exclusion
        # checker we would never get here. This check is a way to
        # exit quickly if the user didn't provide any criteria.
        # network.check4InclusionExclusionCriteria defaults to True,
        # and if its value is True, the code below will try to get
        # this function's necessary data from network properties,
        # and set it to one of two other possible values: 
        #   False, meaning we have checked and processing should
        #          continue, or
        #   NO_INCLEXCL, defined above, which means we didn't have
        #          the data we needed to continue using this function.
        #   In the latter case, we also set the 
        if network.check4InclusionExclusionCriteria == NO_INCLEXCL:
            return True
        
        if network.check4InclusionExclusionCriteria == True:
            network.check4InclusionExclusionCriteria = False
            network.includeexclude_level = network.GetProperty('includeexclude_level')
            # default inclusion/exclusion level is 1 - we assume we want
            # the root node even if nothing else passes the tests.
            if network.includeexclude_level == None:
                network.includeexclude_level = 1
            network.include_patternlist = network.GetProperty('include_patternlist')
            network.include_patternlist_flags = network.GetProperty('include_patternlist_flags')
            network.exclude_patternlist = network.GetProperty('exclude_patternlist')
            network.exclude_patternlist_flags = network.GetProperty('exclude_patternlist_flags')
                
            if network.include_patternlist == None and network.exclude_patternlist == None:
                # turn off page content checking
                network.check4InclusionExclusionCriteria = NO_INCLEXCL
                return True # no regex searches needed
        if level < network.includeexclude_level:
            return True # no regex searches needed
        
        # Use the standard routine in urlutils to get the page. This ensures
        # all necessary housekeeping is done. The checker routine is called
        # early in the processing of a URL, so we will save the page for later
        # to avoid doing a second GET, and if there is an HTTP error we will
        # also save that to warn off attempts to retrieve the page later.         
        page = GetHttpPage(network,theUrl)
        if not page:
            return False # omit because we can't check content
        
        # ignore anything that is not html, xhtml, or xml
        if not re.search('<html',page,re.IGNORECASE):
            if not re.search('<xhtml',page,re.IGNORECASE):
                if not re.search('<xml',page,re.IGNORECASE):
                    return False # exclude if we can't check content
                
        # parse here to get text
        strIO = StringIO.StringIO() # to hold the page text
        parser = HTMLParser(AbstractFormatter(DumbWriter(file=strIO,maxcol=32767)))
        parser.feed(page)
        data = strIO.getvalue()
        
        # see if page contains at least one item on the include list
        found = None
        if network.include_patternlist:
            for inclusion_pattern in network.include_patternlist:
                if network.include_patternlist_flags:
                    found = re.search(inclusion_pattern,data,network.include_patternlist_flags)
                else:
                    found = re.search(inclusion_pattern,data)
                # all we need is one item to trigger inclusion; 
                # if we found one we can quitlooping
                if found != None:
                    break
            # if we didn't find at least one of the inclusion patterns, scrap the page
            if found == None:
                return False

        # if we get here, either there was no include_patternlist, or at least
        # one of the inclusion patterns was found in the text.
        
        # if there are *exclusion* patterns, see if any of them are
        # found; as soon as we know at least one is found, return False
        
        if network.exclude_patternlist:
            for exclusion_pattern in network.exclude_patternlist:
                if network.exclude_patternlist_flags:
                    found = re.search(exclusion_pattern,data,network.exclude_patternlist_flags)
                else:
                    found = re.search(exclusion_pattern,data)
                # we only need one match on an exclusion pattern to trigger
                # scrapping the page.
                if found != None:
                    return False
                
        # if we get here, either there was no include_patternlist or there
        # was a match on at least one of the inclusion patterns, AND
        # either there was no exclude list or none of the patterns
        # in the exclusion list were found in the page.
        
        return True
    except Exception, inst:
        theError = 'CheckInclusionExclusionCriteria: ' + str(type(inst)) + '\n' + str(inst) + '\non URL ' + theUrl
        network.SetLastError ( theError )
        log.Write(theError)
        #print theError
        return False





###################################################################
###################################################################
###################################################################


if __name__ == '__main__':

    # dir to write to
    workingDir =GetConfigValue('workingDir')
    name = """alice
    bob"""
    name = RemoveNonPrintableChars(name)
    print name

    sys.exit(0)
    

