# urltree3.py
from urlnet.urltree import UrlTree
net = UrlTree(_maxLevel=3)
net.SetProperty('getTitles',True)
net.BuildUrlTree('http://www.southwindpress.com')
net.WritePajekFile('urltree3', 'urltree3',useTitles=True)
