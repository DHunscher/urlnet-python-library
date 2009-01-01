# savetreeloadtree1.py

from urlnet.urltree import UrlTree
from urlnet.urlutils import saveTree, loadTree

net = UrlTree()
net.BuildUrlTree('http://www.southwindpress.com')
net.WritePajekFile('savetreeloadtree1', 'savetreeloadtree1')

# save to file and reload into different instance
print 'saving...'
saveTree(net,'savetreeloadtree1.pckl')
print 'loading...'
net2=loadTree('savetreeloadtree1.pckl')
print 'done loading.'

net2.WritePajekFile('savetreeloadtree1.1','savetreeloadtree1.1')

