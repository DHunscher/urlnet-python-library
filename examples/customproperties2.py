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
# customproperties2.py
from urlnet.urltree import UrlTree
from urlnet.urlutils import GetHttpPage
from urlnet.log import Log

import re # for search flags
import math # for square root

def makeDictionary(length,sqrt):
    '''
    This function provides a single method for creating a dictionary
    from the calculated property values. In our simple example, this
    works for both URL and domain item properties, but that would
    not always be the case; if they were different, there would be separate
    functions for URLs and domains.
    '''
    return { 'length' : length, 'sqrt' : sqrt, }

def SetPageBasedPropertyValues(network,theUrl,level):
    '''
    This function shows the use of UrlNet's inclusion/exclusion checker
    protocol to analyze page content and set properties based on the
    results of the analysis. Our analysis in this case is trivial, but
    it provides a framework in which you can put your own analytical
    features.
    '''
    # default values for use in setting some crazy properties
    length = 0
    sqrt = 0.0
    log = Log('SetPageBasedPropertyValues','url=%s' % (str(theUrl)))
        
    try:
        network.includeexclude_level = network.GetProperty('includeexclude_level')
        # default inclusion/exclusion level is 1 - we assume we want
        # to include the root node in the analysis. If this were used
        # in a URL tree network with a placeholder root, we would want
        # to set the includeexclude_level property to 1.
        if network.includeexclude_level == None:
            network.includeexclude_level = 0
            network.SetProperty('includeexclude_level',0)
                
        if level < network.includeexclude_level:
            network.SetProperty('UrlPagePropsToSet', makeDictionary(length,sqrt) ) 
            network.SetProperty('DomainPagePropsToSet', makeDictionary(length,sqrt) ) 
            return True # no regex searches needed
        
        # Use the standard routine urlutils.GetHttpPage to get the page, ensuring
        # that all necessary housekeeping is done. The checker routine is called
        # early in the processing of a URL, so we will save the page for later
        # to avoid doing a second GET, and if there is an HTTP error we will
        # also save that to warn off attempts to retrieve the page later.         
        page = GetHttpPage(network,theUrl)
        if not page:
            network.SetProperty('UrlPagePropsToSet', makeDictionary(length,sqrt) ) 
            # fudge the domain values so they are a little different...
            network.SetProperty('DomainPagePropsToSet', makeDictionary(length*3,sqrt/2.0) ) 
            return True # press on regardless
        
            
        # ignore anything that is not html, xhtml, or xml
        head = page[:500]
        #print str(head)
        if not re.search('<html',head,re.IGNORECASE):
            if not re.search('<xhtml',head,re.IGNORECASE):
                if not re.search('<xml',head,re.IGNORECASE):
                    network.SetProperty('UrlPagePropsToSet', makeDictionary(length,sqrt) ) 
                    network.SetProperty('DomainPagePropsToSet', makeDictionary(length,sqrt) ) 
                    return True
                
        # set crazy properties to 'real' values
        length = len(page)
        sqrt = math.sqrt(len(page))
        
        network.SetProperty('UrlPagePropsToSet', makeDictionary(length,sqrt) ) 
        network.SetProperty('DomainPagePropsToSet', makeDictionary(length,sqrt) ) 
        return True
    except Exception, inst:
        theError = 'SetPageBasedPropertyValues: %s\n%s\non URL %s' % ( str(type(inst)), str(inst), theUrl )
        network.SetLastError ( theError )
        log.Write(theError)
        #print theError
        return False
    

def main():
    # in case we need to be polite...
    SLEEPTIME = 0
    MAXLEVEL = 2
    try:
        net = UrlTree(_maxLevel=MAXLEVEL,_sleeptime=SLEEPTIME)

        PropertyDictList4Urls = \
            [
                {
                    'attrName'    : 'length',
                    'PorVName'    : 'Page length', 
                    'doPartition' : True,
                    'default'     : 9999998,
                    'datatype'    : 'INT',
                },
                {
                    'attrName'    : 'sqrt',
                    'PorVName'    : 'Square root of length of page', 
                    'doPartition' : False,
                    'default'     : 0.00001,
                    'datatype'    : 'DOUBLE',
                },
            ]
            
        # this list is identical to the one above, but is duped
        # so you can use this example as a template for your real
        # work, in which URLs and domains might be handled differently.
        
        PropertyDictList4Domains = \
            [
                {
                    'attrName'    : 'length',
                    'PorVName'    : 'Page length', 
                    'doPartition' : True,
                    'default'     : 9999998,
                    'datatype'    : 'INT',
                },
                {
                    'attrName'    : 'sqrt',
                    'PorVName'    : 'Square root of length of page', 
                    'doPartition' : False,
                    'default'     : 0.00001,
                    'datatype'    : 'DOUBLE',
                },
            ]
            
        net.SetProperty('additionalDomainAttrs',PropertyDictList4Domains)
        net.SetProperty('additionalUrlAttrs',PropertyDictList4Urls)
        
        # install the custom page checker 
        net.SetPageContentCheckerFn(SetPageBasedPropertyValues)
                
        net.BuildUrlTree('http://www.southwindpress.com')

        # write Pajek project
        net.WritePajekFile('customproperties2', 'customproperties2')
        # write GUESS network files
        net.WriteGuessFile('customproperties2Urls', doUrlNetwork = True)
        net.WriteGuessFile('customproperties2Domains', doUrlNetwork = False)
    except Exception, e:
        print str(e)
        
if __name__ == '__main__':
    main()
    
    
