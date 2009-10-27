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
Simple logging class. Writes messages to stderr and optionally to a
different i/o stream. Activate by setting log.logging to True, and
optionally setting log.altfd to an open file descriptor of your
choosing.

Primarily intended for use in call tree tracing. Instantiating a Log
class instance at the beginning and end of a function will cause
log entries to be written on entering and exit during runtime.

Example:

import sys
from urlnet.log import Log, logging, altfd

def main():
    urlnet.log.altfd = open('log.txt','w') # or 'a' to append
    urlnet.log.logging = True
    foo(2)
    urlnet.log.altfd.close()
    urlnet.log.altfd = None
    sys.exit(0)
    
def foo(bar):
    # create log instance, with name of this function plus optional
    # arguments in string format; an entry trace will be written
    # assuming urlnet.log.logging is set to True
    
    log = Log('foo','bar=%s' % (str(bar)))
    # do your business here
    if x < 0:
        log.Write('x is less than zero')
    return True
    # when the local variable 'log' is cleaned up, the Log class
    # destructor will be called and an exit trace written

log contains:

in foo(bar=2): entering
in foo(bar=2): x is less than zero
in foo(bar=2): exiting


NOTE: If you instantiate a log instance in the routine where you open
the altfd file descriptor, then close the file descriptor, be sure to
set urlnet.log.altfd to None; if you do not, you will see a harmless
but annoying error message like the following:

exception in urlnet.log.Write: I/O operation on closed file

"""
import sys
import os
import time
import traceback

logging = False
altfd = None
limit = 10.0 # must be a float?
file_only = False
trace = False # debugging mode is True; change to False for 
              # better performance in 'production mode'
stacktrace = False # if True, enables printing of stack traces when 
                   # Object.SetLastLerror() is envoked.

class Log:
    myName = None
    myArgs = None
    startTime = None
    def __init__(self,name,args='no args'):
        global trace
        self.myName = str(name)
        self.myArgs = str(args)
        if trace:
            self.Write('entering')
            self.startTime = time.time()
        
             
    def WriteStackTrace(self):
        '''
        Call this to get a stack trace written to logging output stream.
        Called automatically from within Object.SetLastError() if
        log.logging = True and log.traceback = True.
        '''
        global logging, altfd, file_only
        try:
            
            if logging:
                if altfd:
                    traceback.print_stack(
                        limit=None,file=altfd)
                    altfd.flush()
                if not (altfd and file_only):
                    traceback.print_stack(
                        limit=None,file=sys.stderr)
            
        except Exception, e: # in case altfd.write fails...
            print 'exception in Log.WriteStackTrace(): %s' % str(e)
            traceback.print_stack(
                    limit=None,file=sys.stderr)
            
            
            
    def __del__(self):
        global limit, trace
        if trace:
            endTime = time.time()
            elapsed = endTime - self.startTime
            ending = 'exiting, %f secs ' % elapsed
            if elapsed > limit:
                report = '**** > %f sec limit ****' % limit
                ending = ending + report
            self.Write(ending)

    def Write(self,arg):
        global logging, altfd, file_only
        if logging:
            try:
                if altfd:
                    altfd.write( '%s in %s (%s): %s\n' % (time.strftime('%H:%M:%S'),str(self.myName), str(self.myArgs), str(arg)))
                    altfd.flush()
                if not (altfd and file_only):
                    sys.stderr.write( 'at %s in %s (%s): %s\n' % (time.strftime('%H:%M:%S'),str(self.myName), str(self.myArgs), str(arg)))
            except Exception, e:
                sys.stderr.write('%s: exception in urlnet.log.Write: %s\n' % (time.strftime('%H:%M:%S'),str(e),))
                
