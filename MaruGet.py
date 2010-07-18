#!/usr/bin/env python

import urllib2
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import NavigableString
from BeautifulSoup import Tag
import re

class MaruBlog:
    """
    maruBlog is a simple little class that gets a maru blog post.
    """

    # __ENCODING is a private variable that stores the expected
    # encoding.  This should be had programatically, but meh.
    __ENCODING = 'euc-jp'

    # entryNumber is the blog entry number. None to get most recent.
    entryNumber = int()

    # maruUrl is the url path to a maru blog post
    maruUrl = "http://sisinmaru.blog17.fc2.com/blog-entry-^ENTRYNUM^.html"

    maruUrlNone = "http://sisinmaru.blog17.fc2.com/"

    # urlFile is the result from urllib.urlopen() action, which
    # is a file-like object.
    urlFile = None

    # wholeBody is the body of the blog post, in Unicode
    wholeBody = None

    # entryBodyHtml is the content part of the blog post - that is, pictures
    # and text (complete with markup)
    entryBodyHtml = None

    # entryTitle is the tile of the blog post
    entryTitle = None

    # soup is the BeauitfulSoup object created out of the post.
    soup = None

    def __init__(self, entryNumber = None):
	self.entryNumber = entryNumber
	self.__constructMaruUrl()
	self.__getUrl()
	self.__readBody()
	self.soup = BeautifulSoup(self.wholeBody)
	self.__findContent()
	self.__setTitle()
	return

    def __constructMaruUrl(self):
	# TODO: Make this work properly if entryNumber == None.
	if (self.entryNumber == None):
	    self.maruUrl = self.maruUrlNone
	else:
	    self.maruUrl = self.maruUrl.replace('^ENTRYNUM^', str(self.entryNumber))

    def __getUrl(self):
	"""
	Gets the url and stores it in a urllib2 object
	"""
	self.urlFile = urllib2.urlopen(self.maruUrl)
	return

    def __readBody(self):
	"""
	Takes the entire body, converts it to Unicode, and 
	stores it in self.wholeBody
	"""
	body = self.urlFile.read()
	self.wholeBody = unicode(body, self.__ENCODING)
	return

    def __findContent(self):
	"""
	Finds the exciting content in the blog post.
	"""
	self.entryBodyHtml = self.soup.find('div', {'class':'entry_body'})
	return

    def __setTitle(self):
	"""
	Sets the title of the blog post.
	"""
	try:
	    self.entryTitle = self.soup.find('div', {'class':'entry_title'}).a.getText()
	except AttributeError:
	    self.entryTitle = None
	return

    def ircContent(self):
	"""
	Returns a string of the content, properly formatted for posting an in IRC channel. 
	"""
	# This could be interesting. The blog posts are messes of <br /> 
	# tags, and not using something HTML-aware could be painful.
	# This will most likely be accomplished using parts of Beautiful
	# Soup.

	# There are a few tags that seem to be used in fc2 blogs, at least
	# this one in particular.
	#  * br tags are abused for formatting
	#  * img tags contain pictures
	#    and are stored within a tags.
	#  * Text is just placed outside of everything.
	#    Text is of type BeautifulSoup.NavigableString.

	ircString = unicode()
	try:
	    for item in self.entryBodyHtml:

		if (type(item) == Tag):
		    if(item.find('img') != None):
			# Image.
			ircString += item.find('img')['src'] + u"\n"

		    elif(item.find('embed') != None):
			# Youtube video.
			ircString += item.find('embed')['src'] + u"\n"

		# Text:
		if (type(item) == NavigableString):
		    ircString += item + u"\n"
	except TypeError:
	    ircString = u"No blog post found."
	    
	return ircString

    def latestPost(self):
	"""
	Returns the integer number of the most recent blog post.
	"""
	allLinks = self.soup.findAll('a')
	for link in allLinks:
	    url = link.get("href")
	    result = re.match("http://sisinmaru.blog17.fc2.com/blog-entry-....html", url)
	    if (result != None):
		pos = re.search("[0-9][0-9][0-9]", url)
		start = pos.start()
		end = pos.end()
		return int(url[start:end])
	return None
