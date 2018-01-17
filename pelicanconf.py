#!/usr/bin/env python
import time

AUTHOR = "Buck Ryan"
SITENAME = "Buck Ryan"
SITEURL = "http://localhost:40101"
TAGLINE = "Software Engineer by Day, Husband et. al by Night"
TIMEZONE = "America/New_York"
DEFAULT_DATE_FORMAT = "%a %B %d,%Y"
DEFAULT_LANG = "en"
TEMPLATE_PAGES = {
    # eg: "pricing.html": "pricing.html",
}
THEME = "theme"
CACHE_BUST = str(time.time())
MENUITEMS = [
    ("Articles", "/archives.html"),
    ("Categories", "/categories.html"),
    ("Tags", "/tags.html"),
]
STATIC_PATHS = ["extra"]
EXTRA_PATH_METADATA = {
    "extra/resume.pdf": {"path": "static/resume.pdf"},
    "extra/pgp.txt": {"path": "static/pgp.txt"},
}
PLUGIN_PATHS = ["/home/buck/src/pelican-plugins"]
PLUGINS = ["pelican-toc", "asset_functions"]
TOC = {
    "TOC_HEADERS": "^h[1-6]",
    "TOC_RUN": "true",
    "TOC_INCLUDE_TITLE": "true",
}
