#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Buck Ryan'
SITENAME = u'buckryan.com'
SITESUBTITLE = u''
SITEURL = ''

TIMEZONE = 'America/New_York'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
LINKS =  (('Pelican', 'http://getpelican.com/'),
          ('Python.org', 'http://python.org/'),
          ('Jinja2', 'http://jinja.pocoo.org/'),
          ('You can modify those links in your config file', '#'),)

SOCIAL = (('twitter', 'https://twitter.com/_buckryan'),
          ('github', 'https://github.com/b-ryan'),)

DEFAULT_PAGINATION = 10

STATIC_PATHS = ['files']

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

DISPLAY_PAGES_ON_MENU = True
DISPLAY_CATEGORIES_ON_MENU = False
DISPLAY_AUTHOR = False
DISPLAY_FOOTER = False

THEME = "theme"
