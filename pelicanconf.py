AUTHOR = u"Buck Ryan"
SITENAME = u"buckryan.com"
SITESUBTITLE = u""
SITEURL = "http://localhost:8888"

TIMEZONE = "America/New_York"

DEFAULT_LANG = u"en"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
LINKS =  (("Pelican", "http://getpelican.com/"),
          ("Python.org", "http://python.org/"),
          ("Jinja2", "http://jinja.pocoo.org/"),
          ("You can modify those links in your config file", "#"),)

SOCIAL = (("twitter", "https://twitter.com/_buckryan"),
          ("github", "https://github.com/b-ryan"),)

DEFAULT_PAGINATION = 10

STATIC_PATHS = ["files"]

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

DISPLAY_PAGES_ON_MENU = True
DISPLAY_CATEGORIES_ON_MENU = False
DISPLAY_AUTHOR = False
DISPLAY_FOOTER = False

THEME = "flex"
PATH = "content"
SITELOGO = "/static/me.png"
# FAVICON = "https://www.dbrhino.com/theme/img/dbrhino-logo.ico"
ROBOTS = "index, follow"
CC_LICENSE = {
    "name": "Creative Commons Attribution-ShareAlike",
    "version": "4.0",
    "slug": "by-sa"
}
COPYRIGHT_YEAR = 2017
FEED_ALL_ATOM = "feeds/all.atom.xml"
CATEGORY_FEED_ATOM = "feeds/%s.atom.xml"
SOCIAL = (("github", "https://github.com/b-ryan"),
          ("twitter", "https://twitter.com/_buckryan"),
          ("rss", "//www.buckryan.com/feeds/all.atom.xml"))

SITEMAP = {
    "format": "xml",
    "priorities": {
        "articles": 0.6,
        "indexes": 0.6,
        "pages": 0.5,
    },
    "changefreqs": {
        "articles": "monthly",
        "indexes": "daily",
        "pages": "monthly",
    }
}
MAIN_MENU = True
MENUITEMS = (("Archives", "/archives.html"),
             ("Categories", "/categories.html"),
             ("Tags", "/tags.html"),)

STATIC_PATHS = ["extra"]
EXTRA_PATH_METADATA = {
    "extra/me.png": {"path": "static/me.png"},
    "extra/resume-2017-01.pdf": {"path": "static/resume-2017-01.pdf"},
}
LINKS = tuple()
