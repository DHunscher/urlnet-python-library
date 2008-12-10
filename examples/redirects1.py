# redirects.py

"""
This program can take an hour or more to run! It gathers 180+
top-level URLs and pursues each of them on layer further down.
"""

from urlnet.urltree import UrlTree
import urlnet.log

urlnet.log.logging = True

# use a standard list of ignorables provided by the library.
from urlnet.ignoreandtruncate import textToIgnore

# this handles hitsphere.com urls, which look like this:
# /mc/mc.php?link=http://healthnex.typepad.com/web_log/&feed=3&...etc.
testRedirects = (('/mc/mc.php?','link',1),)
net = UrlTree(_maxLevel=2,_redirects=testRedirects)
net.SetIgnorableText(textToIgnore)
#net.SetProperty('getTitles',True)
success = net.BuildUrlTree('http://www.hitsphere.com/')
if success:
    net.WritePajekFile('redirects1','redirects1' \
                       #,useTitles=True \
                       )


