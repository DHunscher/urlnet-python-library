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
'''
Demonstrate the use of custom property setter.
'''
from urlnet.urltree import UrlTree
from urlnet.log import Log, logging

import math

def MyCustomPropertySetter(net,item,urlToAdd):
    log = Log('MyCustomPropertySetter',urlToAdd)
    logging = True
    '''
    Set some properties for demonstration purposes
    '''
    
    item.SetProperty('length', len(urlToAdd) )        # integer property
    item.SetProperty('sqrt',math.sqrt(len(urlToAdd))) # float property
    
    
    
def main():

    try:
        
        net = UrlTree(_maxLevel=2)
        #
        # tell the algorithm to call the function
        # urlnet.topleveldomainutils.SetUrlTLDProperties
        # to capture TLD properties.
        
        net.SetCustomUrlPropertiesFn(MyCustomPropertySetter)
        
        # The same custom properties setter works for domains; this
        # might not be the case for other applications.
        
        net.SetCustomDomainPropertiesFn(MyCustomPropertySetter)
        
        PropertyDictList4Urls = \
            [
                {
                    'attrName'    : 'length',
                    'PorVName'    : 'URL Length', 
                    'doPartition' : True,
                    'default'     : 9999998,
                    'datatype'    : 'INT',
                },
                {
                    'attrName'    : 'sqrt',
                    'PorVName'    : 'Square root of length of URL', 
                    'doPartition' : False,
                    'default'     : 0.00001,
                    'datatype'    : 'DOUBLE',
                },
            ]
            
        net.SetProperty('additionalUrlAttrs',PropertyDictList4Urls)
        
        # this list is identical to the one above, but is duped
        # so you can use this example as a template for your real
        # work, in which URLs and domains might be handled differently.
        
        PropertyDictList4Domains = \
            [
                {
                    'attrName'    : 'length',
                    'PorVName'    : 'URL Length', 
                    'doPartition' : True,
                    'default'     : 9999998,
                    'datatype'    : 'INT',
                },
                {
                    'attrName'    : 'sqrt',
                    'PorVName'    : 'Square root of length of URL', 
                    'doPartition' : False,
                    'default'     : 0.00001,
                    'datatype'    : 'DOUBLE',
                },
            ]
            
        net.SetProperty('additionalDomainAttrs',PropertyDictList4Domains)
        
        
        net.BuildUrlTree('http://www.southwindpress.com/')
            
        # the Pajek project will contain an additional partition and vector,
        # and the GUESS networks will contain an additional two attributes
        # per vertex
        net.WritePajekFile('customproperties1','customproperties1')
        net.WriteGuessFile('customproperties1Urls', doUrlNetwork = True)
        net.WriteGuessFile('customproperties1Domains', doUrlNetwork = False)
        
    except Exception,e:
        print str(e)
    

    
if __name__ == '__main__':
    main()
    #sys.exit(0)
