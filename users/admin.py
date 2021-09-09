"""Admin set up for the User app."""
from django.contrib import admin

from users.models import Profile

admin.site.register(Profile)
