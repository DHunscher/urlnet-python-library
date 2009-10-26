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
A generic base class for our objects.
"""
import sys
#import traceback

import log

#################### the Object class #########################
class Object:
    """
    A root class for objects, providing rudimentary error handling.
    """
    lastError = None
    properties = None

    def __init__(self):
        self.lastError = None
        self.properties = {}
        self.myName = None

    def GetLastError(self):
        return str(self.lastError)

    def ResetLastError(self):
        self.lastError = None

    def SetLastError(self,e):
        myLog = log.Log('SetLastError')
        #myLog.Write('%s\n' % traceback.format_exc())
        self.lastError = str(e)
        if e and log.logging:
            myLog.Write(str(e))
        
        
    def SetProperties(self,properties):
        """
        set one or more properties based on key/value pairs in dict passed in as 'properties'.
        """
        if properties:
            for key in properties.keys():
                self.SetProperty(key, properties[key])
        

    def SetProperty(self,key,value):
        self.properties[key] = value

    def GetProperty(self,key):
        try:
            value = self.properties[key]
            return value
        except Exception, e:
            #self.SetLastError(' GetProperty lookup error on "' + str(key) + '"')
            return None

    def GetPropertyNames(self):
        list = []
        for name in self.properties.keys():
            list.append(name)
        return list
            
    def SetName(self,name):
        self.myName = name

    def GetName(self):
        return str(self.myName)

    def tmpfile(self, mode='w'):
        fn = str(int(time.time()*10000))
        fn = fn + '.txt'
        fd = open(fn, mode)
        return (fn,fd)
    
        

if __name__ == '__main__':
    import log, urlutils
    log.logging = True
    workingDir =urlutils.GetConfigValue('workingDir')
    log.altfd = open(workingDir+'log.txt','w')

    myLog = log.Log('main')
    
    x = Object()

    print x.GetName()
    x.SetName('bob')
    print x.GetName()

    x.SetLastError('hey!!')
    print x.GetLastError()
    x.ResetLastError()
    print x.GetLastError()
    x.SetProperty('foo','bar')
    x.SetProperty('spam','spamspamspam')
    print str(x.GetProperty('foo'))
    print str(x.GetProperty('bar'))
    print x.GetLastError()
    print str(x.GetPropertyNames())
    log.altfd.close()
    log.altfd = None
    
              
