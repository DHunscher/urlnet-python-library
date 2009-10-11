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
from os.path import join
import sys
import os

from urlnet.ncbilinkstree import NCBILinksTree
from urlnet.urlutils import GetConfigValue, GetTimestampString
import urlnet.ncbiconstants
import urlnet.log


def main():
    # dir to write to
    timestamp = GetTimestampString()
    baseDir = GetConfigValue('workingDir')
    workingDir = join(baseDir,timestamp)
    oldDir = os.getcwd()
    
    myLog = None
    goAhead = True
    
    try:
        try:
            os.mkdir(workingDir)
        except Exception, e:
            pass #TODO: make sure it's because the dir already exists
        os.chdir(workingDir)
        myLog = urlnet.log.Log('main')
        urlnet.log.logging=True
        urlnet.log.altfd=open('ncbilinkstree.log','w')
    except Exception,e:
        myLog.Write(str(e)+'\n')
        goAhead = False

    if goAhead:
        try:
            net = NCBILinksTree(_maxLevel=1)
            net.SetProperty('nodeLengthLimit',50)
            # build the cosmos network of genes, nucleotides, and SNPs around a protein
            # (dUTPase) related to HIV; throw in the related documents as well.
            #dbs = urlnet.ncbiconstants.ConcatDBNames( (urlnet.ncbiconstants.GENE,
            #                                           urlnet.ncbiconstants.SNP,
            #                                           urlnet.ncbiconstants.PUBMED) )
            dbs = urlnet.ncbiconstants.PUBMED
            qry = '"sleep apnea, obstructive" AND "interleukin-6"'
            net.BuildUrlForestWithPhantomRoot(qry,DbSrcOfIds=urlnet.ncbiconstants.PROTEIN,DbsToLink=dbs)
            net.WritePajekFile(qry,qry)
        except Exception, e:
            myLog.Write( str(e) )
    # tidy up
    if urlnet.log.altfd:
        urlnet.log.altfd.close()
        # must set altfd to None to avoid problems with the log instance's destructor
        # executes
        urlnet.log.altfd = None
        
    os.chdir(oldDir)


if __name__ == '__main__':
    main()
    sys.exit(0)
