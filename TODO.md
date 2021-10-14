# Todo

## Important functionality

* Comments - `Basic functionality complete`
* Tags - `Basic functionality complete`
* Sidebar - `Basic functionality complete`. Sections need more coding as the
  relevant functionality is written.
* API to read / post Blog Posts and Comments, allowing a completely separate
  front end to be written and used.
* Sensitive variables to ENV vars, using `python-dotenv`
* add a 'like' option to a post
* Implement the 'Popular Posts' sidebar section. This will need to wait until
  the 'likes' functionality is complete.

### Comments

* Offer to remember commenter for next visit, or use credentials from logged in
  user.
* ~~Integrate an HTML editor. Could use markdown but it gives unexpected results
  to those not used to it (ie missing linebreaks). Comments saved as HTML and
  filtered through 'safe'~~ Using Markdown with WYSIWYG functionality for now.
* ~~profile links for registered users need to be switched to specific links, once
  that functionality is added~~
* add ReCapcha to the comment entry form
* Nested comments
* Record visitors IP address with the comment. Can be used for moderation or in
  case of spamming / abuse. Can use `django-ipware` package.

### Misc Bugs / Fixes / Ideas

* Add Emoji reactions to posts and comments
* Need to reformat the style for the index page post summary  display, I really
  really don't like it!
* Dynamic titles using template content blocks
* Add a user section in the sidebar (also holding login/register links in not
  logged in). Will allow to create a new post, edit profile etc.#
* zap up the profile, allow display of social links, make edit page etc.
* ~~Header is messed up when looking at someone else profile when you are logged
  in or out, it displays the header as if you are logged in as that user (ie the
  avatar and logout display)~~
* redundant code in `blog_edit_post.html` to check if logged in. If not logged
  in, this page is inaccesible anyway d/t view permissions.
* buttons missing or not working in the markdown WYSIWYG editor **UPDATE This is
  due to incompatibility with FontAwesome. Need to find an alternative
  HTML/Markup editor or a different Icon source.**
* detect the users timezone and display date/time formats properly.
* add user login/logout/register functionality, though register should be by
  invitation not open to all. [`PARTIAL`]
* define tag on the body that can wrap the start of the article, which can be
  displayed on the main index page list, followed by a 'read more' button. Can
  do fancy styling to fade the last few lines etc too.
* ~~paginate the first page to say 5 or 10 etc latest post only.~~
* show a pinned post?
* automatically create a google sitemap.xml on each new post.
* ensure we don't have duplicate slugs. not too difficult in a single-user blog
  but may be more of an issue if multiple users post.
* allow to access posts by /year/month/date/slug also. This will perhaps help
  with the above issue.
* API to allow getting summary data of a users posts for embedding in other
  apps.
* pass the post count for a user to the profile template for display. Due to
  pagination, `{{ posts|length }}` only displays the number on that page.
* refactor CSS to PostCSS, using [`django-compressor`][djc] and
  [`django-compressor-postcss`][djc-postcss]
* add social media sharing to a post
* Toggle (from manage.py) to disable the native Django front end completely if
  required, so an external one can use the API (maybe make into a plugin app?)
* sort out different WYSIWYG editor placeholders depending if we are creating
  a post or a comment

[djc]: https://github.com/django-compressor/django-compressor
[djc-postcss]: https://github.com/Pithikos/django-compressor-postcss
