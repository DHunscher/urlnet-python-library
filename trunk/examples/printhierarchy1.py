# printhierarchy1.py
from urlnet.urltree import UrlTree
from urlnet.urlutils import PrintHierarchy

net = UrlTree(_maxLevel=3)
net.SetProperty('getTitles',True)
success = net.BuildUrlTree('http://www.southwindpress.com')
if success:
    try:
        net.WritePajekFile('printhierarchy1', 'printhierarchy1',useTitles=True)
        net.WriteUrlHierarchyFile('printhierarchyurls1.txt')
        net.WriteDomainHierarchyFile('printhierarchydomains1.txt')
    except Exception, e:
        print str(e)
