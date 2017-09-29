import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

SITEURL = "http://buckryan.com"
RELATIVE_URLS = False

FEED_ALL_ATOM = "feeds/all.atom.xml"
CATEGORY_FEED_ATOM = "feeds/%s.atom.xml"

DELETE_OUTPUT_DIRECTORY = True

CLICKY_ID = 100683631
DISQUS_SITENAME = "buckryan"
GOOGLE_ANALYTICS = "UA-39435134-1"
