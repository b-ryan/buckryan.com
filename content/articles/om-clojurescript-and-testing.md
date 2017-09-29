Title: Om, Clojurescript, and Testing
Date: 2015-07-16
Category:
Tags:
Author: Buck Ryan
Summary:

This past week I started learning React, Om, and Clojurescript all at once.
When beginning to use [cemerick's
.clojurescript.test](https://github.com/cemerick/clojurescript.test), I kept
running into this error:

    #!text
    Error: cemerick is undefined

    ERROR: cemerick.cljs.test was not required.

    You can resolve this issue by ensuring [cemerick.cljs.test] appears
    in the :require clause of your test suite namespaces.
    Also make sure that your build has actually included any test files.

But I clearly had included it in my test! I googled and grumbled, but could not
figure out what was wrong. Finally I discovered that
[slimerjs](https://slimerjs.org/) has the `-jsconsole` flag, which, as the docs
say, will

    #!text
    Open a window to view all javascript errors during the execution

Great, using that I finally found the actual problem:

    #!text
    Script Error: Error: Assert failed: No target specified to om.core/root
    (not (nil? target))
           Stack:
             -> file:///tmp/runner6386761518784950059.js.html: 55456

This makes much more sense. The issue is that my `core.cljs` namespace was
running `om/root` when the page loads. The code looked like:

    #!clojure
    (om/root main-view
             app-state
             {:target (. js/document (getElementById "app"))}))

But since the tests are not loading the index.html page (as they shouldn't),
there is no element with ID app. Ultimately the problem is with running code
at the namespace level. What would be preferred would be if there were some
way to specify a main function to initialize the app. This would be run for
the actual application, but not the tests.

First take at a Solution
========================

It took awhile of searching, but I finally found some inspiration from
[this project](https://github.com/jalehman/react-tutorial-om) and specifically
[this line of code](https://github.com/jalehman/react-tutorial-om/blob/60867fb0efcb48a3f20bc94361c2f981e6c96f44/resources/public/index.html#L15):

    #!html
    <script type="text/javascript">goog.require("react_tutorial_om.app");</script>

I realized I could just wrap my `om/root` call in a main function and then call
this from the index.html page. Here is what the code in `core.cljs` looks like
now:

    #!clojure
    (defn app []
      (om/root main-view
               app-state
               {:target (. js/document (getElementById "app"))}))

and the corresponding code in `index.html`:

    #!html
    <script type="text/javascript">
    goog.require("my.namespace.core");
    my.namespace.core.app();
    </script>

Now running the tests no longer had any problem. However, I realized that
lein figwheel was not reloading the page properly when I made changes to the
code. This is because the javascript would be reloaded, which previously was
running `om/root` every time. To solve this I added to the `on-js-reload`
function so that the app was reinitialized:

    #!clojure
    (defn on-js-reload []
      (app))

Improving the Solution
======================

As I continued learning about Om, I came across the
[om-cookbook](https://github.com/omcljs/om-cookbook) repository. The following
is based on the structure of the project in the
`recipes/routing-with-secretary` directory (and possibly others in the repo).

Let's assume your project currently has this directory structure:

    resources/...
    src/my/namespace/core.cljs
    project.clj

We are going to add a directory called `env` which will house code that is
specific to different environments, namely development vs. production. Create
directories such that your project now looks like this:

    env/dev/src/my/namespace/dev.cljs
       /prod/src/my/namespace/prod.cljs
    resources/...
    src/my/namespace/core.cljs
    project.clj

You can see that in `env/dev` and `env/prod` we mimick the `src` directory.
Within `dev.cljs` we will add code that is only to be run when developing.
Here is what that namespace will basically look like for the dev environment:

    #!clojure
    (ns my.namespace.dev
      (:require [my.namespace.core :as core]
                [figwheel.client :as figwheel :include-macros true]))

    (enable-console-print!)

    (defn on-js-reload []
      (core/app))

    (core/app)

For production, this can be much simpler:

    #!clojure
    (ns my.namespace.prod
      (:require [my.namespace.core :as core]))

    (core/app)

Now all we need to do is modify `project.clj` to use these environments. This
is accomplished using different build configurations. Here is a sample of
how that would look:

    #!clojure
    :cljsbuild {:builds [{:id "dev"
                          :source-paths ["src" "env/dev/src"]
                          ; blah blah blah
                          }
                         {:id "prod"
                          :source-paths ["src" "env/prod/src"]
                          ; blah blah blah
                          }
                         {:id "test"
                          :source-paths ["src" "test"]
                          ; blah blah blah
                          }]}

Finally, make sure to remove the code that was added to `index.html` in our
first take at a solution.

And there you have it. The dev environment will end up compiling `dev.cljs`,
and since this namespace includes a call to `core/app` at the namespace-level,
it will run when the javascript is loaded. We do not include the file for the
test build, meaning the tests do not try to run `om/root`.

Alternative Approach
====================

An entirely different approach to all of this (and perhaps a lot simpler)
would be to simply check if your target element exists. Your code could then
look like

    #!clojure
    (if-let [target (. js/document (getElementById "app"))]
      (om/root main-view
               app-state
               {:target target}))

You might prefer this approach. The reason I tend to not like this is that you
still have functionality that executes when you require the namespace. It also
introduces a silent failure. If you change the main element to have a different
id, your app would just show up blank with no errors printed.

I was pretty surprised to not be able to find anything about this. Maybe I'm
missing something obvious. I am new to Clojurescript and Om, so it could just
be a newbie mistake. If so let me know!
