# Todo

## Important functionality

* Comments - `Basic functionality complete`
* Tags
* Sidebar
* API to read / post Blog Posts and Comments, allowing a completely separate
  front end to be written and used.

### Comments

* Offer to remember commenter for next visit, or use credentials from logged in
  user.
* ~~Integrate an HTML editor. Could use markdown but it gives unexpected results
  to those not used to it (ie missing linebreaks). Comments saved as HTML and
  filtered through 'safe'~~ Using Markdown with WYSIWYG functionality for now.
* profile links for registered users need to be switched to specific links, once
  that functionality is added
* add ReCapcha to the comment entry form
* Nested comments

### Misc Bugs / Fixes / Ideas

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
* pass the post count for a user to the profile template for display. due to
  pagination, `{{ posts|length }}` only displays the number on that page.
* refactor CSS to PostCSS, using [`django-compressor`][djc] and
  [`django-compressor-postcss`][djc-postcss]
* add a 'like' option to a post
* add social media sharing to a post
* Toggle (from manage.py) to disable the native Django front end completely if
  required, so an external one can use the API (maybe make into a plugin app?)

[djc]: https://github.com/django-compressor/django-compressor
[djc-postcss]: https://github.com/Pithikos/django-compressor-postcss
