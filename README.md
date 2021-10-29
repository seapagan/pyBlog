# Django-based Blogging engine

This is work in progress to write a blogging Engine in Django for my own use,
and release as OSS when it reaches that level.

This README is very basic and will be updated as more functionality is coded
into the project.

## Progress

### Already Implemented

- Users can login/logout/register etc. Registered users cannot post, though they
  can be elevated to Author status by a Superuser. This allows 'Guest Poster'
  functionality. All registered users can comment. Anonymous users can also
  comment though they will need to supply a username (and soon email), and
  cannot edit a comment once submitted.
- Users with a registered Gravatar will have this automatically used for their
  profile picture, but can also specify another.
- Ability to Post (limited to superuser and users with the Author flag set as
  true)
- Comment on a Post
- Tag posts with similar topics, list all the tags and list posts for each tag.
- Posts can be set as draft and published later. Draft posts are hidden from all
  but Superuser or the post author.
- Ability to 'like' a post, single vote per logged or anonymous user. Page views
  are tracked (anonymously and only used for internal page ranking). Like button
  uses Ajax so does not force a page refresh.
- Responsive design - Sidebar on larger screens and degrading cleanly to a drop
  down menu on smaller. Menu is CSS only, no JS needed.
- Sidebar has a section for 6 most 'Popular Posts' (ranked by page views then
  user likes) and 'Recent Posts' showing the 6 latest.
- Full WYSIWYG editor for both Posts and Comments, author can add links,
  pictures, emojis etc. Comments however do not have the ability to add images.
- Profile page for each registered user, showing their Posts, Comments and
  Social Media links.
- Posts can have an image assigned to them, this will appear on the main page
  sumary and each posts detail page. If the image is not specified, a default
  will be used.
- Pagination of posts and Comments
- Ability to 'Pin' a single post at the top of the first page to give it exposure.
- Post URL's use a 'slug' created from the post title, helping with SEO.

### Minimum required before Release

- Implement site search functionality - the search UI is already there.
- Add proper Testing.
- Tidy up new comment form for anonymous users.
- Add Timezone support so the user sees all times in his local timezone.
- Disable Django own admin in Production mode - remove the app and urls. This is
  already done, though I may want to add the ability for certain trusted IP to
  still access if needed.
- Sensitive variables (Secret, database login etc) moved to ENV variables and
  taken out the code.
- Some small tweaks needed to the CSS on smaller screens
- Implement code minimization and tidy up the CSS, probably refactor as PostCSS

### Good to Have

- Dedicated Admin site for superusers and potentially an 'admin' user (who will
  only be able to access Blog admin, not the Django admin site.)
- Add 'Series' functionality where a set of posts can be grouped numerically and
  accessed as such.
- Add list of other recommended posts at the bottom of each post, calculated on
  post tags and popularity.
- Add a future post mode. Can use the background module to daily check for any
  future published posts and publish them.

See the [TODO.md](TODO.md) in the root of this repository for full details of
outstanding bugs and future plans.

## Development

From the root of the checked out repository.

### Install the dependencies

```bash
pip install -r requirements.txt
```

### Migrate the database

You will need to adjust the database settings to your own needs, the application
defaults to using a file-based `SQLite` database.

```bash
python manage.py migrate
```

### Run the Development server

The application defaults to **Production** mode unless the `DEBUG` variable is set
to 1

```bash
DEBUG=1 python manage.py runserver
```

You can now access the application in your browser at `http://localhost:8000`
