URLNET PYTHON LIBRARY README FILE
VERSION 0.90.07
29 OCTOBER 2009
==================
NEWS FLASH
==================
This is the final release for 0.90, which now becomes the most recent stable version. 


0	DEPENDENCIES
	- Python 2.5 (http://www.python.org/download/releases/2.5/)
	- 4Suite XML Library (http://4suite.org/?xslt=downloads.xslt)

4Suite is needed for a few example programs; you'll get error messages
when you need it.

1	INSTALLING THE LIBRARY

At present there is no automated install, but the procedure is very simple.  
It assumes you have already installed Python 5 and downloaded the UrlNet zip file.  
Python 2.5 or later is required. My apologies to the die-hards using earlier 
versions.

1.1	UNZIP THE DISTRIBUTION

Unzip the distribution file to a location of your choice. It will create a 
tree with the following structure.

urlnet-v0.90.06
	urlnet
	examples
	doc
conf

The version number in the name of the root directory may be different from 
what is shown here.

1.2	COPY THE LIBRARY DIRECTORY TO YOUR PYTHON INSTALLATION'S 
	LIB/SITE-PACKAGES DIRECTORY

The directory referred to here is the urlnet subdirectory under the 
urlnet-v1.0 directory, which in turn is found under wherever you unzipped 
the distribution file. You can actually put it anywhere in the Python path 
(possibly found in the PYTHONPATH environment variable, or in Unix and Linux,
by implication from the command 'which python'). The Python installation's 
Lib/site-packages directory is the normal place to keep third-party modules, 
which is why I am recommending it here.

1.3	UPDATE URLNET.CFG AND COPY TO A LOCATION ON THE EXECUTION PATH

Edit the urlnet.cfg file in the conf subdirectory to, at minimum, set the 
workingDir vale to the default working directory of your choice.  You can 
override this at will, but this eliminates the proliferation of calls to os.chdir.  

Other variables you may want to set now are your Technorati key, if you have one, 
and your email address.  The email address is an optional but polite parameter 
for the Web APIs of the National Center for Biomedical Informatics. Neither is 
needed until you actually work with a Technorati or NCBI example, but if you are 
editing, you might as well take care of it.

1.4	COPY THE EXAMPLE PROGRAMS TO A LOCATION OF YOUR CHOICE

The working directory you set in urlnet.cfg is a good starting point. 
If you copy the examples there, you won't have to modify any code to override 
the working directory.

1.5	TEST THE INSTALL

From your operating system shell's command line, enter the command

python urltree1.py

It should take a short while to run, after which you should find a small Pajek 
project file named urltree1.paj in the working directory.

2	THE EXAMPLE PROGRAMS

Numerous example programs are provided, illustrating many of the features of 
the library. Most are only a few lines long, making them easy to understand and 
also demonstrating the power of the library.  Longer programs show more 
complicated scenarios, such as setting up a production batch program that 
runs periodically to retrieve the current state of a URL network. All examples
are described in the manual.

3	RELEASE NOTES

0.90: Many new features added, a few bugs fixed, a bunch of new examples.
Apologies for the lack of detail, but the user guide covers everything.
There's too much to list here in the release notes.

0.82: Added urlutils functions for persisting (saving and loading) networks.

0.81: urlnet.cfg is now sought in the current directory prior to searching the 
folders listed in the PATH environment variable. This change is found in urlutils.py.
TechnoratiTree (found in technoratitree.py) now removes single and double quotes 
erroneously wrapping the Technorati API key, and checks for it in urlnet.cfg if 
the passed value for the key is the Python constant None.

0.71: This release contains a minor bug fix that is important 
for those running on Unix or Linux platforms. Without this fix, the urlnet.cfg 
file will not be found on these platforms. The one-line change is in urlutils.py. 

Another change: the Technorati API key placeholder in the urlnet.cfg file is 
incorrectly wrapped in single quotes, causing the technorati1.py sample program
to fail even if the placeholder value is replaced by a valid key. The quotes have 
been removed in this release.

