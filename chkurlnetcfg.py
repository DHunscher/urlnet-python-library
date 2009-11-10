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
# chkurlnetcfg.py

'''
This script will reveal problems locating either the urlnet.cfg file
itself, or information contained therein.
'''

import os
from os.path import exists, join, abspath
from os import pathsep, environ
from string import split
import platform

# name of file (to be found on path) where we can find 
# configuration information
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
    try:
        # allow for the possibility that there is no HOME env variable
        home = None
        try:
            home = os.environ['HOME']
        except Exception, e:
            pass
        print('HOME env var: <%s>' % str(home))
        # 
        if home != None and len(home) > 0:
            paths.append(home)
        paths = paths + split(search_path, pathsep)
        print 'Search paths that will be checked:'
        for path in paths:
            print '    %s' % path
        for path in paths:
            if exists(join(path, filename)):
                file_found = 1
                break
        if file_found:
            path = abspath(join(path, filename))
            try:
                print 'trying to open : %s' % path
                fd = open(path)
                lines = fd.readlines()
                fd.close()
                return lines
            except Exception, e:
                print('%s %s' % (str(type(e)), str(e)))
                return None
        else:
            print("Can't find %s in paths" % str(filename))
            return None
    except Exception, e:
        print('%s %s' % (str(type(e)), str(e)))
        return None
    

def main():
    try:
        print 'Python version: %s' % platform.python_version()
        print 'System OS: %s (%s)' % (platform.system(), \
                                     platform.architecture()[0])
        print 'Processor: %s' % platform.processor()
        print 'Node: %s' % platform.node()
        try:
            import simplejson
            print 'simplejson module is available'
        except Exception, e:
            print 'simplejson module not available, some examples will not work'
        try:
            import twitter
            print 'twitter module is available'
        except Exception, e:
            print 'twitter module not available, some examples will not work'
        try:
            import Ft.Xml
            print 'Ft.Xml module is available'
        except Exception, e:
            print 'Ft.Xml module not available, some examples will not work'
        vars = {}
        lines = read_config_file()
        i = 0
        if lines == None:
            lines = []
        for line in lines:
            i = i + 1
            print '%03d: %s' % (i , line.rstrip() )
            line = line.strip()
            if len(line) > 0:
                # ignore comments
                if line[0] == '#':
                    continue
                parts = line.split('=')
                if len(parts) != 2:
                    continue
                ename = parts[0].strip().lower()
                value = parts[1].strip()    # don't lower-case; path may 
                                            # be case-sensitive
                vars[ename] = value
        if i == 0:
            raise Exception('no lines returned!')
        if len(vars.keys()) == 0:
            raise Exception('No name-value pairs found!')
        print '*** name-value pairs ***'
        for name in vars.keys():
            print '  %s: %s' % (name, vars[name])
            if name.lower() == 'workingdir':
                dir = vars[name]
                try:
                    tmp = os.path.join(dir,'98765432.tmp')
                    fd = open(tmp,'w')
                    fd.close()
                    os.remove(tmp)
                    print '    (directory %s is writeable)' % dir
                except Exception, e:
                    print '**Warning! directory %s does not exist or is write-protected!' % dir
    except Exception, e:
        print('%s %s' % (str(type(e)), str(e)))
        
    
if __name__ == '__main__':
    main()
    