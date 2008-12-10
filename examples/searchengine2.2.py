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
        net = AOLTree(_maxLevel=2,
                       _workingDir=workingDir,
                       _resultLimit=10,
                       _probabilityVector = probability_by_position,
                       _probabilityVectorGenerator = vectorGenerator)

        # build initial network from the Medline Plus portal recommended
        # links
        
        mlp_smokingcessation_portal = \
            'http://www.nlm.nih.gov/medlineplus/smokingcessation.html'

        # save some properties to restore later
        # we're going to override these at first
        savedRegexPattern = net.GetProperty('regexPattern')
        savedFindallArgs = net.GetProperty('findall_args')
        
        # Next, we set the regular expressions to be used in parsing the 
        # MedlinePlus smoking cessation portal page. This is a list of three
        # regular expressions that are used in sequence. The list is declared
        # above.
        net.SetProperty('regexPattern',medlineplusRegexPats)

        # Make sure the regex parser treats newlines as just more whitespace.
        net.SetProperty('findall_args',re.S)

        # ignore pages not relevant to our inquiry
        net.SetIgnorableText(textToIgnore)
        #
        # Don't pursue links in Amazon, YouTube, etc.
        net.SetTruncatableText(textToTruncate)
        
        net.BuildUrlTree( \
            mlp_smokingcessation_portal)
        
        # We now have a network consisting of the first- and second-level
        # outlinks from the Medline Plus smoking cessation portal's
        # recommendations.
        # Now we want to merge in a network generated from the result set of
        # the query to the AOL engine. We need to restore the class 
        # properties we saved in order to use the AOLTree class as it
        # was designed, to process a query.
        
        net.SetProperty('regexPattern',savedRegexPattern)
        net.SetProperty('findall_args',savedFindallArgs)
        net.urlclass = RegexQueryUrl
        #
        # clear the list of top-level URLs, so we can rely on the ones from
        # the search engine.
        net.topLevelUrls = None
        
        # The AOLTree.BuildUrlTreeWithPlaceholderRoot function will add to 
        # in the network already present in the AOLTree instance.
        net.BuildUrlTreeWithPlaceholderRoot(\
            'http://search.aol.com/','quit smoking')

        # generate networks
        net.WritePajekFile('aoltree-quitsmoking','aoltree-quitsmoking')
        net.WriteGuessFile('aoltree-quitsmoking_urls')
        net.WriteGuessFile('aoltree-quitsmoking_domains',False)
        
    except Exception,e:
        myLog.Write(str(e)+'\n on quit smoking query\n')
        
if __name__ == '__main__':
    main()
    sys.exit(0)
