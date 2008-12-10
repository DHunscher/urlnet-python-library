# ignorabletext.py
from urlnet.urltree import UrlTree

ignorableText = ['payloadz','sitemeter',]

net = UrlTree(_maxLevel=3, _ignorableText=ignorableText)
net.BuildUrlTree('http://www.southwindpress.com')
net.WritePajekFile('ignorabletext', 'ignorabletext')
