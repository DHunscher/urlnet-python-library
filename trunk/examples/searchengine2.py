from urlnet.log import Log, logging, altfd
from urlnet.aoltree import AOLTree
from urlnet.urlutils import PrintHierarchy
import sys
from time import strftime, localtime
import os
from urlnet.searchenginetree import computeDescendingStraightLineProbabilityVector,\
                                    computeEqualProbabilityVector
from urlnet.ignoreandtruncate import textToIgnore, textToTruncate
from urlnet.clickprobabilities import probabilityByPositionStopSmokingClicks \
                                       as probability_by_position

from urlnet.regexqueryurl import RegexQueryUrl
import re
medlineplusRegexPats = [
    '<ul id="subcatlist">.*</ul>',
    '<span class="categoryname"><a name=".*?</ul>',
    '<a href="([^/#].*?)"',
    ]

def main():
    import urlnet.log
    from urlnet.urlutils import GetConfigValue
    from os.path import join
    """
    We are going to make a subdirectory under
    the working directory that will be different each run.
    """

    baseDir = GetConfigValue('workingDir')
    # dir to write to
    timestamp = strftime('%Y-%m-%d--%H-%M-%S',localtime())
    workingDir = join(baseDir,'stopsmoking',timestamp)

    oldDir = os.getcwd()

    # uncomment one of the vectorGenerator assignments below
    
    # vectorGenerator = computeEqualProbabilityVector
    vectorGenerator = computeDescendingStraightLineProbabilityVector
    myLog = Log('main')
    urlnet.log.logging=True
    #urlnet.log.trace=True
    urlnet.log.altfd=open('aoltree.log','w')
    try:
        try:
            os.mkdir(workingDir)
        except Exception, e:
            pass #TODO: make sure it's because the dir already exists
        os.chdir(workingDir)
        urlnet.log.logging=True
        #urlnet.log.trace=True
        urlnet.log.altfd=open('aoltree.log','w')
    except Exception,e:
        myLog.Write(str(e)+'\n')
        return
    try:
        # build initial network based on query 'quit smoking'
        
        net = AOLTree(_maxLevel=2,
                       _workingDir=workingDir,
                       _resultLimit=10,
                       _probabilityVector = probability_by_position,
                       _probabilityVectorGenerator = vectorGenerator)
        #
        # tell the algorithm to ignore the MedlinePlus smoking cessation portal for now.
        textToIgnore.append('medlineplus/smokingcess')
        net.SetIgnorableText(textToIgnore)
        #
        # Don't pursue links in Amazon, YouTube, etc.
        net.SetTruncatableText(textToTruncate)        
        net.BuildUrlTreeWithPlaceholderRoot('http://search.aol.com/','quit smoking')

        # We now have a network consisting of the first- and second-level
        # links generated from the result set of the query to the AOL engine.
        # Now we want to merge in a network generated from the Medline Plus 
        # smoking cessation portal's recommendations. We need to reset some class 
        # properties in order to use the RegexQueryUrl class; the MedlinePlus
        # portal page has a lot of generic links we don't want to include in
        # the network.
        #
        # First, make sure we haven't already seen it.
        
        mlp_smokingcessation_portal = \
            'http://www.nlm.nih.gov/medlineplus/smokingcessation.html'
        item = net.GetUrlNetItemByUrl(mlp_smokingcessation_portal)
        if net.UrlExists(mlp_smokingcessation_portal):
            net.ForceNodeToLevel(level=0,url=mlp_smokingcessation_portal)
        else:
            # First we change the filename that will be used to output the top-level URLs

            net.SetFilenameFromQuery('medlineplus_smokingcessation')

            # Next, we set the regular expressions to be used in parsing the 
            # MedlinePlus smoking cessation portal page. This is a list of three
            # regular expressions that are used in sequence. It's declared above.

            net.SetProperty('regexPattern',medlineplusRegexPats)

            # Make sure the regex parser treats newlines as just more whitespace.

            net.SetProperty('findall_args',re.S)

            # remove the signal to ignore the MedlinePlus smoking cessation URL
            
            net.SetIgnorableText(textToIgnore[:-1])
            
            # Finally, reset the Url-derived class to use for the root URL.

            net.urlclass = RegexQueryUrl

            # The AOLTree.BuildUrlTree function will add to the network already present
            # in the AOLTree instance.
            net.BuildUrlTree( \
                mlp_smokingcessation_portal)
            
        net.WritePajekFile('aoltree-quitsmoking','aoltree-quitsmoking')
        net.WriteGuessFile('aoltree-quitsmoking_urls')
        net.WriteGuessFile('aoltree-quitsmoking_domains',False)
        
    except Exception,e:
        myLog.Write(str(e)+'\n on quit smoking query\n')
        
if __name__ == '__main__':
    main()
    sys.exit(0)
