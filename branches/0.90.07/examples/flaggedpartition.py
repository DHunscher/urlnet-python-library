#!/usr/bin/env python
# $Id$
# flaggedpartition.py
from urlnet.urltree import UrlTree
from urlnet.log import Log
from urlparse import urlparse

import os

def FlagSelectedURLs(network,item,level):
    '''
    This function shows a way to selectively flag certain URLs in a network.
    '''
    log = Log('FlagSelectedURLs','url=%s' % (str(item.GetName())))
    try:
        URLsToFlag = network.GetProperty('URLsToFlag')
        
        # remove 'http://' or any other scheme prefix
        
        parts = urlparse(item.GetName())
        ignore = len(parts[0])
        if ignore > 0:
            ignore = ignore + 3
        
        url = item.GetName()[ignore:]
        
        # this line will set the flag property to True if the URL is
        # found in the list, False if it is not in the list
        item.SetProperty('flag', url in URLsToFlag ) 
            
        return True
    except Exception, inst:
        theError = 'FlagSelectedURLs: %s\n%s\non URL %s' % ( str(type(inst)), str(inst), theUrl )
        network.SetLastError ( theError )
        log.Write(theError)
        #print theError
        return False

def main():
    try:
        network = UrlTree()

        # your URLs go in this list, single or double quoted
        # note that the realm prefix is removed (http://, ftp://...)
        # this is not necessary, but it speeds things up a bit
        urlsToFlag = [
        "payloadz.com/go?id=349877"   ,
        "www.payloadz.com/go/view_cart.asp?id_user=42699"   ,
        "payloadz.com/go?id=349878"   ,
        "payloadz.com/go?id=349879"   ,
        "payloadz.com/go?id=349880"   ,
        "payloadz.com/go?id=350289"   ,
        "payloadz.com/go?id=250731"   ,
        "payloadz.com/go?id=253420"   ,
        "payloadz.com/go?id=350295"   ,
        "payloadz.com/go?id=350296"   ,

        ]

        network.SetProperty('URLsToFlag',urlsToFlag)
        
        network.SetCustomUrlPropertiesFn(FlagSelectedURLs)
        
        # We create a 'dict' entry in the PropertyDictList4Urls dictionary 
        # to translate the 'flag' property's boolean value to an integer 
        # value.
        booleanDict = \
            { 
            True : 1, 
            False : 0, 
            }
            
        PropertyDictList4Urls = \
            [
                {
                    'attrName'    : 'flag',
                    'PorVName'    : 'URL in list (1=True, 0=False)', 
                    'doPartition' : True,
                    'default'     : 0,
                    'datatype'    : 'INT',
                    'dict'        : booleanDict
                },
            ]
            
        network.SetProperty('additionalUrlAttrs',PropertyDictList4Urls)

        network.BuildUrlTree('http://www.southwindpress.com/')

        # Pajek project will have a new partition, and 
        # the GUESS network's vertices will have a new attribute

        network.WritePajekFile('flaggedpartition1', 'flaggedpartition1')
        network.WriteGuessFile('flaggedpartition1')
    except Exception, e:
        print str(e)
        return
    
if __name__ == '__main__':
    main()
