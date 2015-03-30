# UrlNet Python Library for Social Network Analysis Data Collection on the Web #

## Attention users and prospective users! Check out CurrentKnownBugsAndWorkarounds! ##
<a href='http://urlnet-python-library.googlecode.com/svn/wiki/healthcareguy-cosmos-2.jpg'><img src='http://urlnet-python-library.googlecode.com/svn/wiki/healthcareguy-cosmos-2.jpg' width='400' /></a>

_**Technorati cosmos network.** Click picture for full-size image in new window._


# Introduction #
This code repository is the home of the UrlNet Python Library for network analysis data collection on the Web.

When studying aspects of the World Wide Web (hereinafter "Web") using network analysis tools and techniques, building networks for analysis can be tedious, time-consuming, and error-prone.  The UrlNet library, written in the Python scripting language, is intended to provide a powerful, flexible, easy to use mechanism for generating such networks.

# Outlink harvesting #

Starting at a given page (which we can call the root page), we can collect, or "harvest", the outlinks on the page and follow them to other pages. We can harvest the outlinks on these pages, and follow them, et cetera, to the search depth we desire. These actions create a directed graph in which the pages are vertices and the outlinks form the arcs between vertices. While this graph begins in tree form, it often loops back on itself in many places, forming an acyclic graph that illustrates the interrelationships within and between clusters of knowledge representations on the Web. It is often useful to create such networks when studying phenomena on the Web, for example the findability of a given page from a known starting-point page, or when looking at the structure of a particular Website (a site map).

When using link harvesting to generate networks, UrlNet by default constructs a domain network in addition to the URL network. This provides a high-level view of the network, often useful in cases where the URL network consists of tens or hundreds of thousands of nodes.

In addition to leveraging the default capabilities of Python's urllib and urllib2 modules, UrlNet provides facilities for the use of Python regular expressions for link extraction, and makes it easy to custom-build URLs from information derived from a Web page. This method was developed to support the study of search engine result sets, but has been generalized for use in any number of additional contexts.

<a href='http://urlnet-python-library.googlecode.com/svn-history/r23/wiki/sitemap-1.jpg'><img src='http://urlnet-python-library.googlecode.com/svn-history/r23/wiki/sitemap-1.jpg' width='800' /></a>

_**Site-map network.** Click picture for full-size image in new window._

# Web Service APIs #

While URLs are typically thought of as links from Web pages to other Web pages, that is only one of their uses. Web Services based on the SOAP/WSDL standards, and also lightweight APIs based on the REST paradigm, can also be accessed via URLs.  Social networking sites such as Technorati, Delicious, and Bibsonomy provide such APIs. The National Library of Medicine offers URL-based APIs that access its Medline database and its bioinformatics data repositories.  There are many others too numerous to mention.

Because UrlNet is written as a class library, it is easy to specialize and/or extend its functionality by subclassing one or more of its classes. One example provided shows how to building networks using the Technorati Cosmos API by subclassing two classes and writing a total of four fairly short functions.

# Trees and Forests #

Some URL-based networks are by nature best thought of as upside-down tree structures, for example a site map. Such networks are actually directed graphs, since lower-level nodes may have links to siblings and ancestor nodes as well as their own child nodes. Nonetheless, each node can be said to exist at some level under the root node (e.g., the home page in a site map).


Other networks - often more interesting networks - can be depicted as "forests" rather than trees.  A forest has multiple root nodes, each of which is a tree in its own right. The trees in the forest can have links to other trees, but there is no requirement that any given tree link to any other tree at all.

One example of a forest is the union of URL trees created from each of the URLs extracted from a search engine query result set.  The root URLs of a forest could also come from a data set obtained from a search engine provider, such as the 2006 AOL data set (see http://gregsadetsky.com/aol-data/ for sources).  One might, for example, investigate the "Vocabulary Problem" to see how the result sets of different search queries expressing the same concept overlap (or fail to overlap).

UrlNet supports building several variations on forest networks.  The vanilla version uses a caller-provided list of URLs as the root nodes for the forest.  Another variation allows you to supply a URL that will not be included in the network as the root node, but whose outlinks form the list of URLs used as the forest roots.  We call the initial URL in this variation a phantom root.  Other variations build on these routines, applying them, for example, to result sets from various search engines, including but not limited to Google, Yahoo! Search, Windows Live Search, and AOL Search.

There is even a way to create a forest from a set of URLs and to unify them into a tree structure by the addition of an arbitrary root node.  We call the arbitrary root node a placeholder root.

<a href='http://urlnet-python-library.googlecode.com/svn-history/r23/wiki/healia-quitsmoking-components.jpg'><img src='http://urlnet-python-library.googlecode.com/svn-history/r23/wiki/healia-quitsmoking-components.jpg' width='800' /></a>

_**Weak components in a forest network.** Click picture for full-size image in new window._

# Generating input data for network visualization software #

UrlNet generates an abstract data structure in memory, from which any number of outputs could potentially be generated.  Currently, the library supports output to three formats: a printable text hierarchy, Pajek project files, and GUESS network files. Other formats can be added easily.

I chose Pajek and GUESS because they are freely available programs, and because they are the software tools on which I learned everything I know about network visualization.  You can download them from the Web at the addresses shown in the following table.

| **Pajek** | Download from the Pajek Wiki at http://pajek.imfm.si/doku.php The wiki has links to other useful software tools for working with Pajek, and tells how to sign up for the Pajek mailing list. There is a very insightful book written by W. de Nooy, A. Mrvar, and V. Batagelj, entitled Exploratory Social Network Analysis with Pajek, published in 2005 by the Cambridge University Press. There is a downloadable version of Pajek that is much older and less functional than the most current version, but has the advantage of being fully compatible with the command set described in the book. UrlNet-generated Pajek projects are fully compatible with both the current version and the "book" version. The "book" version of Pajek can be downloaded at http://vlado.fmf.uni-lj.si/pub/networks/data/esna/Pajek.be.exe.  |
|:----------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **GUESS** | GUESS is the creation of Eytan Adar, and can be downloaded at the main GUESS website, http://graphexploration.cond.org/. UrlNet support for GUESS is presently limited to building simple networks for URL and domain networks. I have been using Pajek longer and more frequently than GUESS, so the GUESS facilities are more primitive than I would like them to be. |

<a href='http://urlnet-python-library.googlecode.com/svn-history/r23/wiki/guess1.jpg'><img src='http://urlnet-python-library.googlecode.com/svn-history/r23/wiki/guess1.jpg' width='800' /></a>

_**GUESS-generated network.** Click picture for full-size image in new window._

# Specialized features for analysis of search engine result sets #

UrlNet was initially developed for use in the analysis of the findability of high-quality information on the Internet. As a result, it has a number of features targeted at that analytical domain, including the ability to generate hit-probability vectors. The following diagram illustrates the use of this feature to identify problems in the findability of high-quality information on smoking cessation:

<a href='http://urlnet-python-library.googlecode.com/svn-history/r23/wiki/google-quitsmoking-03182008.jpg'><img src='http://urlnet-python-library.googlecode.com/svn-history/r23/wiki/google-quitsmoking-03182008.jpg' width='800' /></a>

_**Network used for search engine result set analysis.** Click picture for full-size image in new window._

# Social network analysis in a document corpus #

UrlNet has special features for analysis of networks of publications, co-authors, and !MeSH keywords using APIs provided by the National Library of Medicine's National Center for Biological Information (NCBI). NCBI has numerous databases accessible through these Web Service APIs, and UrlNet can be used for analysis of many different interdisciplinary research questions in genomics, proteomics, metabolomics, cellular biology, and clinical science.

<a href='http://urlnet-python-library.googlecode.com/svn-history/r23/wiki/strecher-cosmos.jpg'><img src='http://urlnet-python-library.googlecode.com/svn-history/r23/wiki/strecher-cosmos.jpg' width='800' /></a>

_**Publication, co-author, and !MeSH keyword cosmos network derived from PubMed data.** Click picture for full-size image in new window._


# Important Links #

|[Latest ZIP package](http://code.google.com/p/urlnet-python-library/source/browse/trunk/latest-download/)|
|:--------------------------------------------------------------------------------------------------------|
|[Readme file](http://code.google.com/p/urlnet-python-library/source/browse/trunk/readme.txt)|
|[Manual (PDF)](http://code.google.com/p/urlnet-python-library/source/browse/trunk/doc/UrlNetUserGuide.doc) |