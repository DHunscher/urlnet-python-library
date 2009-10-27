#!/usr/bin/env python
# $Id: logging3.py 56 2009-10-11 21:03:43Z dalehunscher $
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
# logging4.py
from os.path import join

from urlnet.urltree import UrlTree
from urlnet.urlutils import GetConfigValue
import urlnet.log

def testTrace3():
    try:
        workingDir = GetConfigValue('workingDir')

        # turn on logging
        urlnet.log.logging=True

        # the following line causes printing of stack trace to logging
        # output when Object.SetLastError('something') is invoked.
        # Object is the root of all UrlNet classes except Log.
        urlnet.log.stacktrace=True

        # unless you have a folder called /Bongo/Congo, this will
        # cause an exception in the constructor and a call to
        # Object.SetLastError(), which should trigger a stack trace.
        net = UrlTree(_maxLevel=2, _workingDir='/Bongo/Congo/')
    except Exception, e:
        print 'caught raised exception of type %s: %s' % (str(type(e)), str(e))
def testTrace2():
    testTrace3()
    
def testTrace():
    testTrace2()
    
def main():
    testTrace()
    

if __name__ == '__main__':
    main()
