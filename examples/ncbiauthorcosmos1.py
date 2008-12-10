# ncbiauthorcosmos1.py
import sys

from urlnet.ncbiauthorcosmostree import NCBIAuthorCosmosTree
from urlnet.urlutils import PrintHierarchy
import urlnet.log
from urlnet.urlutils import GetConfigValue
from os.path import join

workingDir = GetConfigValue('workingDir')

urlnet.log.logging = True
# write the log output to a file...
urlnet.log.altfd = open(join( workingDir, "log-ncbiauthorcosmos1.txt"),'w')
# ...and only to the file, not to sys.stderr.
urlnet.log.file_only = True

mylog = urlnet.log.Log('main')

net = NCBIAuthorCosmosTree(_maxLevel=2,
                   _workingDir=workingDir,
                   _sleeptime=1)
ret = net.BuildUrlTree('Strecher VJ')

if ret:
    net.WriteUrlHierarchyFile('strechervj_cosmos_hierarchy')
    net.WritePajekFile('strechervj_cosmos','strechervj_cosmos')
    net.WriteGuessFile('strechervj_cosmos')            # url network
    
urlnet.log.altfd.close()
urlnet.log.altfd=None
