# Todo

## Important functionality

* Optimize thumbnails of the post header image, create smalledr sized ones for
  this when they are added/changed. Currently, the full size image is used and
  resized in the template which is slow and results in a large image being
  downloaded.
* Add Backup / Restore ability for posts, tags, etc.
* Option for commenters to get sent an email if another comment is added to a
  post they have commented on.
* Add the ability to pin a post from its edit page. Also, warn that doing this
  will unpin the current pinned post. Superuser only.
* Add 'Category' functionality to categorize posts under specific categories and
  allow to sort/list by same. `Honestly, not sure if needed; tags should be
  pretty specific for now.`
* API to read / post Blog Posts and Comments, allowing a completely separate
  front end to be written and used.
* Add option to 'unlike' a post.
* Add a future post mode. Can use the background module to daily check for any
  future published posts and publish them.
* Add functionality to temporarily disable a post (transparently - it will not
  be hidden, it instead will be replaced by a custom message)
* Add 'Series' functionality where a set of posts can be grouped numerically
  and read in order.
* Add a list of other recommended posts at the bottom of each post, calculated
  on post tags and popularity.
* Implement an 'Admin' site, independent of the Django built-in Admin pages and
  specific to administrating just the Blog.
* Add the ability for Admin user to Moderate Comments and Tags, or even a Post
  (if we have guest posters, for example)
* ~~Add search functionality~~ [`DONE`]. Currently, it only searches on the
  title and description. Perhaps we can search on tags too in the future, but
  that is a little more complicated.
* Testing. Seriously, lots and lots of testing. Just DO it.

### Comments

* Comment form should be on same page as the post, at the bottom. This allows
  commenter to refer easily back to the post if needed.
* After posting a comment, automatically scroll down to that comment instead of
  back to top of page.
* Offer to remember commenter for next visit, already uses  credentials from
  logged in user if applicable.
* Nested comments
* Record the IP address of visitors with the comment; this can be used for
  moderation or in case of spamming / abuse. Can use `django-ipware` package.

### Documentation

* Add some! Use [mkdocs](https://www.mkdocs.org/) to generate the docs from
  markdown files. use
  [mkdocs-material](https://squidfunk.github.io/mkdocs-material/) for the theme.

### Misc Bugs / Fixes / Ideas

* Add Meta (site preference) to insert `google-site-verification` tag, used to
  verify ownership of your site for the Google Search Console.
* BUG - Tags only attached to draft posts are still shown in the tag list and
  individual tag pages.
* Implement a Light/Dark mode.
* After login, redirect to the same page user was on.
* If the user has no custom User image, the profile page should show the
  gravatar of the user if it exists, then show the default user image. At the
  moment it wont check for a gravatar.
* If post has been renamed, redirect the old slug to the new slug automatically.
* ~~Style the image upload widget for new/edit post.~~ Base work done for this,
  will need further styling when we redo the entire app.
* Add Emoji reactions to posts and comments
* Image upload support is working, however I would like to be able to save the
  images under the `/media/posts/[slug]` folder like the post header image.
* Detect the users timezone and display date/time formats properly.
* ensure we don't have duplicate slugs. not too difficult in a single-user blog
  but may be more of an issue if multiple users post.
* allow to access posts by /year/month/date/slug also. This will perhaps help
  with the above issue.
* API to allow getting summary data of a users posts for embedding in other
  apps.
* refactor CSS to PostCSS, using [`django-compressor`][djc] and
  [`django-compressor-postcss`][djc-postcss]
* add social media sharing to a post. Add correct post metadata for ~~Twitter~~,
  Facebook etc to give proper share summarys
* Toggle (from manage.py) to disable the native Django front end completely if
  required, so an external one can use the API (maybe make into a plugin app?)
* add `rel=canonical` to \<head\> where it is needed, to avoid Google issues.
  `Currently added to Profile pages only`
* Allow ability to use non-pro version of FontAwesome - atm we use the duotone
  icons which are pro only. I invisage a custom tag that will return the 'fad'
  or 'fas' respectively depending on a setting in settings.py. The link in the
  head will need changed for non-pro also.
* Add 'Follow on Twitter/Youtube etc' links to directly follow/subscribe to the
  relevant accounts. Offer to follow both site and post author.

[djc]: https://github.com/django-compressor/django-compressor
[djc-postcss]: https://github.com/Pithikos/django-compressor-postcss
