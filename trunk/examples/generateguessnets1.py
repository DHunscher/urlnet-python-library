# generateguessnets1.py
from urlnet.urltree import UrlTree

ignorableText = ['payloadz','sitemeter',]

net = UrlTree(_maxLevel=2, _ignorableText=ignorableText)
#net.SetProperty('getTitles',True)
net.BuildUrlTree('http://www.southwindpress.com')
# generate GUESS URL network
net.WriteGuessFile('generateguessnets1urls',doUrlNetwork=True) #,useTitles=True)
# generate GUESS domain network
net.WriteGuessFile('generateguessnets1domains',doUrlNetwork=False)
