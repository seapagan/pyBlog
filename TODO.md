# Todo

## Important functionality

* Add Backup / Restore ability for posts, tags, etc.
* ~~Send email to post author when a comment is posted to that post.~~
* Option for commenters to get sent an email if another comment is added to a
  post they have commented on.
* Add the ability to pin a post from its edit page. Also, warn that doing this
  will unpin the current pinned post. Superuser only.
* ~~style Paragraphs (more space below), links and lists (they are default),
  etc. for text in the post BODY~~
* ~~on logout, check if in maintenance mode and, if so, redirect directly to the
  index page, don't show the login/register links.~~ Always redirect to the
  index page.
* ~~Responsive menu, replace the sidebar for smaller screens.~~ `DONE`
* ~~Comments~~ `Basic functionality complete`
* ~~Tags~~ `Basic functionality complete`
* Add 'Category' functionality to categorize posts under specific categories and
  allow to sort/list by same. `Honestly, not sure if needed; tags should be
  pretty specific for now.`
* ~~Sidebar - `Basic functionality complete`. Sections need more coding as the
  relevant functionality is written.~~
* API to read / post Blog Posts and Comments, allowing a completely separate
  front end to be written and used.
* ~~Sensitive variables to ENV vars, using `python-dotenv`~~
* ~~Add a 'like' option to a post~~ `Functionality added, no option to 'unlike'
  a post (yet).
* ~~Implement the 'Popular Posts' sidebar section
  [[#32](https://github.com/seapagan/myblog/issues/32)]. This will need to wait
  until the 'likes' functionality is complete. Also, start logging unique page
  views somehow to help with this.~~
* ~~Add draft mode for new posts~~
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
* ~~Implement a maintenance mode to disable the whole app temporarily if
  needed.~~ [`Done`] Logged in users of staff or higher can still see the site
  and the admin. Logged out or lower will see the '503' page.
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
* ~~Integrate an HTML editor. Could use markdown but it gives unexpected results
  to those not used to it (ie missing linebreaks). Comments saved as HTML and
  filtered through 'safe'. Using Markdown with WYSIWYG functionality for now.~~
  [`Done`] Using CKEditor same as Posts.
* ~~profile links for registered users need to be switched to specific links,
  once that functionality is added~~
* ~~add ReCaptcha to the comment entry form~~
* Nested comments
* Record the IP address of visitors with the comment; this can be used for
  moderation or in case of spamming / abuse. Can use `django-ipware` package.
* ~~humanize the dates and time? (ie '10 minutes ago', 'last month' etc)~~

### Misc Bugs / Fixes / Ideas

* Add Meta (site preference) to insert `google-site-verification` tag, used to
  verify ownership of your site for the Google Search Console.
* BUG - Tags only attached to draft posts are still shown in the tag list and
  individual tag pages.
* Implement a Light/Dark mode.
* ~~Add attribution to post title images, with a link if supplied. Stored in the
  database for each post.~~
* ~~Draft posts are still listed on the profile for other/anon users; they
  should only be seen by the author.~~
* ~~Update settings.ALLOWED_HOSTS to take extra hosts from the .env file.~~
* After login, redirect to the same page user was on.
* ~~Sort out styles on small screen for new comment when not logged in -
  name/email fields need to be stacked.~~
* ~~Seems to be a bug now in the 'like' function - it redirects to 'vote was
  forbidden' but records the vote anyway.
  [#54](https://github.com/seapagan/myblog/issues/54) [`FIXED`] but now the
  Ajax functionality does not work. To be investigated.~~ [`FIXED`]
* ~~if we are on the first page, dont also display a post in the standard list if
  it is also pinned.~~ [`FIXED`]
* ~~profile has double scrollbar on small screens~~
* If the user has no custom User image, the profile page should show the
  gravatar of the user if it exists, then show the default user image. At the
  moment it wont check for a gravatar.
* ~~If no posts, produce a 'holding pattern' screen instead of empty pagination
  controls.~~
* ~~Move the 'New post' above 'Profile' in the User sidebar, in fact make it
  top, with a spacer below?~~
* ~~On new/edit post if no existing tags, say 'None'. Also, curently the New and
  Edit post pages dont show any tags(will be due to the sidebar context
  change.)~~
* ~~When a draft post is published, the created_at date should change to the
  current date/time, not the original creation time.
  [[#24](https://github.com/seapagan/myblog/issues/24)]~~ [`Fixed`]
* ~~Cannot edit the title of a blog post. Add functionality to do this while
  either keeping the slug or generating a new slug but keeping the old one
  pointing at this post for external link security. Offer a choice? (If the post
  is draft we should definitely just change the slug)
  [[#25](https://github.com/seapagan/myblog/issues/25)]~~
* If post has been renamed, redirect the old slug to the new slug automatically.
* ~~Style the image upload widget for new/edit post.~~ Base work done for this,
  will need further styling when we redo the entire app.
* ~~make sure front page link in sidebar doesn't show on front page.~~
* Add Emoji reactions to posts and comments
* ~~More work is needed on the form styles for small mobile devices.
  [[#19](https://github.com/seapagan/myblog/issues/19)]~~
* ~~Make a default post image to use if one is not specified~~ `functionality
  complete with a dummy placeholder image which will need replaced before going
  live`. Also offer default ones based on tag and predefined ones?
* ~~The profile needs link back to main page, or use the sidebar template?~~
* ~~Need to reformat the style for the index page post summary  display, I
  really really don't like it! Probably the post detail display too.~~
* ~~Dynamic page titles~~
* ~~Add a user section in the sidebar (also holding login/register links if not
  logged in). Will allow to create a new post, edit profile etc.~~
* zap up the profile, ~~allow display of social links, and to edit User
  settings~~ etc. `[Probably ready to go]`
* ~~Header is messed up when looking at someone else profile when you are logged
  in or out, it displays the header as if you are logged in as that user (ie the
  avatar and logout display)~~
* ~~redundant code in `blog_edit_post.html` to check if logged in. If not logged
  in, this page is inaccesible anyway d/t view permissions.~~
* ~~buttons missing or not working in the markdown WYSIWYG editor **UPDATE This
  is due to incompatibility with FontAwesome. Need to find an alternative
  HTML/Markup editor or a different Icon source.**~~ [`FIXED`] - swapped to HTML
  and CKEditor plugin. Removed all Markdown support from the applciation.
* Image upload support is working, however I would like to be able to save the
  images under the `/media/posts/[slug]` folder like the post header image.
* Detect the users timezone and display date/time formats properly.
* ~~Add user login/logout/register functionality, though register should be by
  invitation not open to all. [`Working. Register function currently allows
  people to register and make posts but this will need to be changed to only
  superusers can make posts or a new 'poster' permission before release.`]~~
  [`Done`] Only superusers or users with the 'author' flag in their profile can
  create New posts.
* ~~define tag on the body that can wrap the start of the article, which can be
  displayed on the main index page list, followed by a 'read more' button. Can
  do fancy styling to fade the last few lines etc too.~~ Just using the
  description for this `CLOSED`
* ~~paginate the first page to say 5 or 10 etc latest post only.~~
* ~~show a pinned post?~~
* ~~automatically create a google sitemap.xml on request from search engine.~~
* ensure we don't have duplicate slugs. not too difficult in a single-user blog
  but may be more of an issue if multiple users post.
* allow to access posts by /year/month/date/slug also. This will perhaps help
  with the above issue.
* API to allow getting summary data of a users posts for embedding in other
  apps.
* ~~pass the post count for a user to the profile template for display. Due to
  pagination, `{{ posts|length }}` only displays the number on that page.~~
* refactor CSS to PostCSS, using [`django-compressor`][djc] and
  [`django-compressor-postcss`][djc-postcss]
* add social media sharing to a post. Add correct post metadata for ~~Twitter~~,
  Facebook etc to give proper share summarys
* Toggle (from manage.py) to disable the native Django front end completely if
  required, so an external one can use the API (maybe make into a plugin app?)
* ~~sort out different WYSIWYG editor placeholders depending if we are creating
  a post or a comment~~
* add `rel=canonical` to \<head\> where it is needed, to avoid Google issues.
  `Currently added to Profile pages only`
* ~~add site metadata, custom search tags eg for each post, generic ones for the
  others, tag with the n most used tags?~~ The Description tag has been added
  only, Google no longer reads or uses keyword meta tags.
* Allow ability to use non-pro version of FontAwesome - atm we use the duotone
  icons which are pro only. I invisage a custom tag that will return the 'fad'
  or 'fas' respectively depending on a setting in settings.py. The link in the
  head will need changed for non-pro also.
* Add 'Follow on Twitter/Youtube etc' links to directly follow/subscribe to the
  relevant accounts. Offer to follow both site and post author.

[djc]: https://github.com/django-compressor/django-compressor
[djc-postcss]: https://github.com/Pithikos/django-compressor-postcss
