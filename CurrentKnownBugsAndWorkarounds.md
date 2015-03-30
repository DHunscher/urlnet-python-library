# Issues List #

Always check the [Issues List](http://code.google.com/p/urlnet-python-library/issues/list) to see if there are any emergent bugs and workarounds being discussed. The ones that make it to this page are ones that aren't likely to be fixed in the source code soon, usually because no work is currently underway on another rev in which the suggested changes will be included. If work is underway, fixes from the Issues List will not necessarily appear here.

# Current Bugs and Workarounds #

The GoogleTree class has a bug that prevents proper parsing of Google result set pages. The workaround is this: in the class constructor, find the regular expression containing '<h2' and change to '<h3'. This will be fixed in the next patch release.