Title: Automatically Focus on Amazon's Search Bar
Date: 2013-03-07
Category: Programming
Tags: chrome, extension, amazon, autofocus, javascript
Author: Buck Ryan
Summary: Creating a very basic Chrome extension that focuses the search bar on Amazon

Whenever I visit Amazon's homepage, I do so hoping to search for things. I'm
not one to browse around and I'm sure many others are the same. However, I get
annoyed each time this happens because the search bar does not have the focus
when you visit the homepage. After coming across a
[comment](http://news.ycombinator.com/item?id=5333209) on Hacker News
describing the same problem, I realized I could fix this with a pretty simple
Chrome extension. Check it out
[here](https://chrome.google.com/webstore/detail/amazon-search-auto-focus/mlblghbllacignpjknjbpbefjmgnbpca)
and read on for a short description of how I put it together.

About one or two years back, I was interested in making extensions for Chrome,
but never went very far with it. However, the brief foray meant that yesterday,
I knew the basics I would need to make the extension. The most important part
of this is the [manifest](http://developer.chrome.com/extensions/manifest.html),
which describes your extension, lists the permissions it needs, files it
contains, and so forth.

The manifest for this app was really simple:

    #!json
    {
        "manifest_version": 2,
        "name": "Amazon Search AutoFocus",
        "description": "Automatically focus on search bar when visiting Amazon",
        "version": "1",
        "permissions": [
            "http://*.amazon.com/",
            "https://*.amazon.com/"
        ],
        "content_scripts": [
            {
                "matches": ["http://*.amazon.com/"],
                "js": ["script.js"]
            }
        ]
    }

Most of this is pretty obvious. The documentation on the
[manifest_version](http://developer.chrome.com/extensions/manifest.html#manifest_version)
indicates that version 1 is deprecate. The version indicated lets Google
manage the extension among users. This number will be used to determine if a
user is on an older version of the extension and it needs to be updated.

Permissions are bit complicated, as they can include whether the extension
can operate on tabs or windows, have access to sites, etc. For this really
simple app, I only need to indicate that I want access to the amazon sites.

Finally, the hardest part of it all was figuring out how to get some javascript
to run when I visited Amazon's homepage. Using some Google-foo, I discovered
that [Content Scripts](http://developer.chrome.com/extensions/content_scripts.html)
are the way to do this. As the documentation says, `content scripts run in the
context of web pages`. This means the javascript file specified above
(script.js) will be run when Amazon loads. This is exactly what I wanted!

So finally I just needed to write the javascript. It turned out to be dead
simple. Here's the only line needed:

    document.getElementById("twotabsearchtextbox").focus();

I briefly examined Amazon's search box using the Chrome
[developer tools](https://developers.google.com/chrome-developer-tools/docs/elements)
and I saw that the ID of the search box was `twotabsearchtextbox`. So I used
some native javascript functions to set the focus and it was done!

Hopefully this helps if you want to write your own Chrome extension! If I make
any changes or improvements to this, the updated code will be
[on Bitbucket](https://bitbucket.org/b_ryan/amazon-autofocus) for your viewing
pleasure.
