# phantomroot1.py
from urlnet.urltree import UrlTree

net = UrlTree(_maxLevel=2)
ret = net.BuildUrlForestWithPhantomRoot("http://www.nlm.nih.gov/medlineplus/melanoma.html")
if ret:
    net.WritePajekFile('phantomroot1', 'phantomroot1')
    net.WriteGuessFile('phantomroot1urls',doUrlNetwork=True)
    net.WriteGuessFile('phantomroot1domains',doUrlNetwork=False)
