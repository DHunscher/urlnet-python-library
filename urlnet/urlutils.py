#!/usr/bin/env python
# $Id$
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
Utility functions for UrlTree and its descendant and helper classes.
"""

import re
import string
import sys
import os
import urllib
import socket
import re

# for GetTimestampString
from time import strftime, localtime

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


# constants for url top-level domain types returned by UrlTree.GetUrlTLDConstant
DOTCOM   = 1
DOTORG   = 2
DOTNET   = 3
DOTEDU   = 4
DOTGOV   = 5
DOTADM   = 6
DOTMIL   = 7
OKDOTCOM = 8
# imposter
DOTFAKE  = 9
# unknown
DOTUNK   = 999

V_DOTCOM  = 0.01
V_DOTORG  = 0.5
V_DOTNET  = 0.01
V_DOTEDU  = 0.5
V_DOTGOV  = 0.5
V_DOTADM  = 0.01
V_DOTMIL  = 0.01
V_OKDOTCOM = 0.25
# imposter
V_DOTFAKE = 0.01
# unknown
V_DOTUNK  = 0.01

# 3 types of URLs in terms of "goodness"

GOOD_DOMAIN = 21
OK_DOMAIN = 1
BAD_DOMAIN = 3

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
    log = Log('WritePairArcOrEdge',"%d %d args=%s" % (fromIdx,toIdx,str(args)))
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
        log.Write('Exception in WritePairArcOrEdge: %s' % (str(e)))
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
            for attrName, attrType in additionalGuessAttrs:
                value = item.GetProperty(attrName)
                if attrType.upper() in ('VARCHAR','CHAR','DATE','TIME','DATETIME','BOOLEAN'):
                    if value is None:
                        value = ''
                    else: # DOUBLE, INT, TINYINT, FLOAT, BIGINT
                        value = str(value)
                    FILE.write(',"%s"' % (value))
                else:
                    if value is None:
                        value = '0'
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
        additionalDomainAttrs = args[1]
        idx = item.GetIdx()
        domain = item.GetName()
        domain = ReplaceIllegalChars(domain)
        FILE.write('v' + str(idx) + ',' + domain )
        if additionalDomainAttrs != None:
            for attrName, attrType in additionalDomainAttrs:
                value = item.GetProperty(attrName)
                if value is None:
                    if ' DEFAULT ' in attrType.upper():
                        value = ''
                    elif attrType.upper() in ('FLOAT','DOUBLE'):
                        value = '0.0'
                    elif attrType.upper() in ('INT', 'TINYINT', 'BIGINT'):
                        value = '0'
                    else:
                        value = str(value)
                else:
                    value = str(value)
                if (' DEFAULT ' in attrType.upper() or (attrType.upper()) in ('FLOAT','DOUBLE','INT', 'TINYINT', 'BIGINT')):
                    FILE.write(',%s' % (value))
                else:
                    FILE.write(',"%s"' % (value))
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
    
