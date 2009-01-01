# ncbiauthorcosmos1.py
import sys
from os.path import join

from urlnet.ncbiauthorcosmostree import NCBIAuthorCosmosTree
from urlnet.urlutils import PrintHierarchy
import urlnet.log
from urlnet.urlutils import GetConfigValue
from urlnet.urlutils import saveTree, loadTree


workingDir = GetConfigValue('workingDir')

urlnet.log.logging = True
# write the log output to a file...
urlnet.log.altfd = open(join( workingDir, "log-savetreeloadtree2.txt"),'w')
# ...and only to the file, not to sys.stderr.
urlnet.log.file_only = True

mylog = urlnet.log.Log('main')

net = NCBIAuthorCosmosTree(_maxLevel=2,
                   _workingDir=workingDir,
                   _sleeptime=1)
ret = net.BuildUrlTree('Strecher VJ')

if ret:
    net.WriteUrlHierarchyFile('savetreeloadtree2_hierarchy')
    net.WritePajekFile('savetreeloadtree2','savetreeloadtree2')
    net.WriteGuessFile('savetreeloadtree2')
    
    # save to file and reload into different instance
    print 'saving...'
    saveTree(net,'savetreeloadtree2.pckl')
    print 'loading...'
    net2=loadTree('savetreeloadtree2.pckl')
    print 'done loading.'
    
    net2.WriteUrlHierarchyFile('savetreeloadtree2_1_hierarchy')
    net2.WritePajekFile('savetreeloadtree2.1','savetreeloadtree2.1')
    net2.WriteGuessFile('savetreeloadtree2.1')
else:
    print 'error occurred.'
    
urlnet.log.altfd.close()
urlnet.log.altfd=None
