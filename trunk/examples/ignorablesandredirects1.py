# ignorablesandredirects1.py
# This one can take a while to run!

from urlnet.urltree import UrlTree
import urlnet.log
from urlnet.urlutils import GetConfigValue
from os.path import join

workingDir = GetConfigValue('workingDir')


urlnet.log.logging = True
urlnet.log.altfd=open( join( workingDir, "log-ignorablesandredirects1.txt"),"w" )
mylog = urlnet.log.Log('main')

textToIgnore = [
    'buzz.blogger.com',
    'code.blogspot.com',
    'hl7.org',
    'hl7.com',
    'statcounter.com',
    'swicki',
    'eurekster',
    'yahoo.com',
    'technorati.com',
    'ads2.',
    'feeddigest',
    'sitemeter',
    'clustrmaps',
    'del.icio.us',
    'digg.com',
    'zeus.com',
    'feedburner.com',
    'google.com',
    'go.microsoft.com',
    'help.blogger.com',
    'home.businesswire.com',
    'sys-con.com',
    'jigsaw.w3c.org',
    'medicalconnectivity.com/categories',
    'rss.xml',
    'misoso.com',
    'adjuggler.com',
    'skype.com',
    'validator.w3c.org',
    'google.ca',
    'hollywood.com',
    'addthis.com',
    'www.ahrq.com',
    'amia.org',
    'bordersstores.com',
    'wholinkstome.com',
    'hhs.gov',
    'feedblitz',
    'feeddigest',
    'feedster',
    '.com/about/',
    'sitemap',
    'site-map',
    'flickr.com',
    'gpoaccess.gov',
    'googlestore.com',
    'www.himss',
    '/faq.',
    'www.hl7.org',
    'linkedin.com',
    'loinc.org',
    'www.medinfo',
    'mysql.com',
    'www.nytimes.com/',
    'www.state.wv',
    '/privacy/',
    '/privacy.',
    'usa.gov',
    'www.va.gov',
    'youtube.com',
    'www.typepad.com',
    ]
        
testRedirects = (('/mc/mc.php?','link',0),)
net = UrlTree(_maxLevel=1,_workingDir=workingDir,_redirects=testRedirects)
net.SetIgnorableText(textToIgnore)
net.BuildUrlForestWithPhantomRoot('http://www.hitsphere.com/')
net.WritePajekFile('ignorablesandredirects1hitsphere', 'ignorablesandredirects1hitsphere')
net.WriteGuessFile('ignorablesandredirects1hitsphereurls',doUrlNetwork=True)
net.WriteGuessFile('ignorablesandredirects1hitspheredomains',doUrlNetwork=False)

urlnet.log.altfd.close()
urlnet.log.altfd = None
