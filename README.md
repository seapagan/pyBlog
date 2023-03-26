# Django-based Blogging engine <!-- omit in toc -->

This application is a work in progress to write a blogging Engine in Django for
my personal use, and release as OSS when it reaches that level.

This README is very basic and will be updated as I add more functionality to the
project.

- [Progress](#progress)
  - [Already Implemented](#already-implemented)
  - [Minimum required before Release](#minimum-required-before-release)
  - [Good to Have](#good-to-have)
- [Installation and Usage](#installation-and-usage)
  - [Install the dependencies](#install-the-dependencies)
  - [Register for Google Recaptcha](#register-for-google-recaptcha)
  - [Optionally add Google Analytics](#optionally-add-google-analytics)
  - [Set up the .env file](#set-up-the-env-file)
  - [Migrate the Database](#migrate-the-database)
  - [Create a Superuser](#create-a-superuser)
  - [Download GeoIP data if required](#download-geoip-data-if-required)
  - [Run the Development server](#run-the-development-server)
  - [Maintenance mode](#maintenance-mode)
  - [Running behind a Proxy](#running-behind-a-proxy)

## Progress

### Already Implemented

- Users can login/logout/register etc. Registered users cannot post, though they
  can be elevated to Author status by a Superuser. This allows 'Guest Poster'
  functionality. All registered users can comment. Anonymous users can also
  comment though they need to supply a username (and soon email) and
  cannot edit a comment once submitted.
- Users with a registered Gravatar have this automatically used for their
  profile picture, but can also specify another.
- Ability to Post (limited to Superuser and users with the Author flag set as
  true)
- Comment on a Post
- Tag posts with similar topics, list all the tags, and list posts for each tag.
- A post can be set as 'draft' and published later. Draft posts are hidden from
  all but a Superuser or the post author.
- Ability to 'like' a post, with a single vote per logged or anonymous user.
  Page views are tracked (anonymously and only used for internal page ranking).
  Like button uses Ajax, so it does not force a page refresh.
- Responsive design - Sidebar on larger screens and degrading cleanly to a
  drop-down menu on smaller. The menu is CSS only.
- Sidebar has a section for 6 most 'Popular Posts' (ranked by page views then
  user likes) and 'Recent Posts' showing the 6 latest.
- Full WYSIWYG editor for both Posts and Comments, the author can add links,
  pictures, emojis, etc. We cannot add images to comments, however
- Profile page for each registered user, showing their Posts, Comments and
  Social Media links.
- Posts can have an image assigned to them; this appears on the main page
  summary and each post detail page. If the image is not specified, we show a
  default.
- Pagination of posts and Comments
- Ability to 'Pin' a single post at the top of the first page to give it
  exposure.
- Post URLs use a 'slug' created from the post title, helping with SEO.
- URLs are protected by Authentication/Authorization and custom 403/404 views
  have been implemented.
- Site maintenance functionality - the whole site is blocked with an informative
  page when enabled, except for logged in 'Staff' user or above.
- Site preferences module is integrated, which sets the site Name, Tagline,
  Pinned post and more through the Database. This allows very easy customization
  without needing to change the code. All styling is through CSS classes, so
  it is easy to change the look.
- Sensitive variables (Secret, database credentials, etc) are taken from ENV
  variables or `.env` file if it exists
- Post search functionality - currently only searches by post Title and
  Description.
- ReCaptcha to help protect the Login, Registration, and comment functionality
  from abuse.
- Google Search sitemap generated on request at `/sitemap.xml`.
- RSS feed available for Blog Posts at `/feed/posts/`. I will probably add a
  comments feed or upgrade this feed to list comments also.
- Local HTML, CSS and JS are minimized on the fly in production mode, left as-is
  in DEBUG mode.
- Add the metadata for Twitter Cards.
- Display image metadata for the main title image
- Add a `Google Analytics` tag if required

### Minimum required before Release

- Add proper Testing.
- Add Timezone support, so the user sees all times in his local timezone.
- Disable Django's admin in Production mode - (completely - the admin app and
  URLs are not even loaded). `This is already done`, though I may want to add
  the ability for specific trusted IPs to still access the admin if needed.
- Tidy up the CSS, probably refactor to SCSS

### Good to Have

- Dedicated Admin site for superusers and potentially an 'admin' user (who can
  only access Blog admin, not the Django admin site.)
- Add 'Series' functionality where a set of posts can be grouped numerically and
  accessed as such.
- API to allow this backend to be used by totally separate frontend, Token Auth
  where needed.
- Add a list of other recommended posts at the bottom of each post, calculated
  on post tags and popularity.
- Add a future post mode. Can use the background module to daily check for any
  future published posts and publish them.
- Two-factor Authentication. Optional for normal users, compulsory for Staff,
  Authors and Superuser.

See the [TODO.md](TODO.md) at the root of this repository for full details of
outstanding bugs and plans.

## Installation and Usage

From the root of the checked-out repository:

### Install the dependencies

I have switched over to using [Poetry](https://python-poetry.org/) to have much
better control of Dependencies. Please make sure that it is installed globally
before continuing.

```terminal
poetry install
poetry shell
```

This will install all the dependencies and switch to a virtual environment ready
to use the app.

### Register for Google Recaptcha

The Comment system is protected using a `Recaptcha` to help avoid bots.

Visit the [Google Recaptcha][recaptcha] site, register if not already done, then
set up a site for this Blog. Copy the public and private keys; you need to
add them to the `.env` file below. Choose the `V2 Tickbox type` as that is
what we use for this application (at the moment, however, this hard-coded
setting will likely be removed later to allow all types).

### Optionally add Google Analytics

You can add Google Analytics by adding your own personal site key to the `.env`
file :

```ini
GOOGLE_ANALYTICS_ENABLED=1 # 0 is disabled (default), 1 is enabled
GOOGLE_ANALYTICS_TAG='UA-1234567-1' #Use your own key
```

### Set up the .env file

We keep some of the more secret settings in a .env file which does not go into
source control. There is a file `.env.example` in the project root - rename this
to `.env` and set the values as you need. First, you want to generate
a new SECRET_KEY and set up the database login details :

```ini
# set our secret key. Go to https://djecrety.ir/ to generate a good one
SECRET_KEY="this_is_not_very_secret"

# set up Database Users. We are using Postgresql, and this should already
# exist with the correct user and password
BLOG_DB_USER=
BLOG_DB_PASSWORD=
BLOG_DB_NAME=
BLOG_DB_HOST=
BLOG_DB_PORT=

# Extra hosts for ALLOWED_HOSTS, generally the same as your domain name / IP
# this should be a string of comma-separated values, e.g.:
# ALLOWED_HOSTS="www.example.com,www.example.net"
ALLOWED_HOSTS=""

# setup ReCaptcha keys - SET THESE TO YOUR OWN KEYS FROM ABOVE
RECAPTCHA_PUBLIC_KEY="my_public_key"
RECAPTCHA_PRIVATE_KEY="my_private_key"

# Google analytics key - CHANGE TO YOUR OWN SITE-SPECIFIC KEY
# This functionality is not currently working!
GOOGLE_ANALYTICS_ENABLED=1
GOOGLE_ANALYTICS_TAG='UA-1234567-1'
```

In Production, If you are self-hosting your app and the server is secure, you
can keep the .env file, and it will be used in Production. However, with
services that support ENV variables (eg Heroku, Netlify, and more), it is better
to define the variables in their dedicated interfaces. Also, make sure that the
.env file CANNOT be loaded using a web browser! It is possible to use the AWS
'Parameter Store', GCS 'Secret Manager', Hashicorp 'Vault' or others for your
production env.

### Migrate the Database

You need to adjust the database settings to your own needs; we use Postgresql as
the Database backend.

```bash
python manage.py migrate
```

### Create a Superuser

The Superuser automatically has Author rights, which regular users
registered to the app will not, so we need at least one. The Django default
admin site is completely removed in a non-DEBUG setting.

```bash
python manage.py createsuperuser
```

### Download GeoIP data if required

The sessions package can list the GeoIP data of your logged-in users; however,
it needs you to download a couple of files that we cannot redistribute. See
[This website][geo_data] for details. These 2 `.mmdb` files should be put in the
`/geoip` directory of this repository. Without them, the sessions will not
return location data.

This option may also be used for later (anonymous) visitor profiling, nothing
planned yet.

### Run the Development server

The application defaults to **Production** mode unless the `DEBUG` variable is
set to 1 (you can also set this in the .env file)

```bash
DEBUG=1 python manage.py runserver
```

You can now access the application in your browser at `http://localhost:8000`

### Maintenance mode

The entire site can be locked down, returning a `503 Service Unavailable` error
for all anonymous users or registered users below the 'Staff' level. Locking
can be done by the **Superuser only** from the sidebar or menu. It can also be
done from the local terminal in the Django project directory using the below
management commands :

```bash
python manage.py maintenance_mode <on|off>
```

During Maintenance mode, a banner is shown at the top of the screen to remind
any logged in users that the site is unavailable to the public.

### Running behind a Proxy

If you are running the site behind an HTTP proxy (`Nginx`, for example), it is
possible the Geo-location will not work, as the IP address will be blank or
wrong. We need to modify the `REMOTE_ADDR` HTTP header to use the address from
`HTTP_X_FORWARDED_FOR`. There is a middleware installed in the application to do
this, but we disable this by default. Try without first (this is a security risk
UNLESS you are running behind a proxy you control), but if your sessions cannot
get the IP, or Geo-location does not work, change the `FIX_PROXY_IP` in `.env`
to be 1; by default, it is False (0):

```python
# Set to 1 IF NEEDED AND BEHIND A PROXY. See README.
FIX_PROXY_IP=0
```

[geo_data]: https://dev.maxmind.com/geoip/geolite2-free-geolocation-data
[recaptcha]: https://www.google.com/recaptcha/about/
