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
        urlnet.log.altfd=open('ncbilinkstree.log.txt','w')
    except Exception,e:
        myLog.Write(str(e)+'\n')
        goAhead = False

    if goAhead:
        try:
            net = NCBILinksTree(_maxLevel=1)
            net.SetProperty('nodeLengthLimit',100)
            # write results of NCBI web service GETs to disk for later inspection
            net.SetProperty('WriteELinkRawOutput', 'elinkoutput-raw.txt')
            net.SetProperty('WriteESearchRawOutput', 'esearchoutput-raw.txt')
            net.SetProperty('WriteEFetchRawOutput', 'efetchoutput-raw.txt')
            net.SetProperty('WriteESummaryRawOutput', 'esummaryoutput-raw.txt')
            # build the cosmos network of proteins, nucleotides, and SNPs around a gene
            dbs = urlnet.ncbiconstants.ConcatDBNames( (urlnet.ncbiconstants.PROTEIN,
                                                       urlnet.ncbiconstants.NUCLEOTIDE,
                                                       urlnet.ncbiconstants.SNP) )
            qry = 'BRAF[GENE]'
            net.BuildUrlForestWithPhantomRoot(qry,DbSrcOfIds=urlnet.ncbiconstants.GENE,DbsToLink=dbs)
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
