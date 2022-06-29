"""Configure the admin interface."""
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

csrf_protect_m = method_decorator(csrf_protect)


class PreferencesAdmin(admin.ModelAdmin):
    """Admin Class for Preferences app."""

    @csrf_protect_m
    def changelist_view(self, request, extra_context=None):
        """If we only have a single preference object redirect to it.

        Otherwise we display the listing of all objects.
        """
        model = self.model
        if model.objects.all().count() > 1:
            return super().changelist_view(request)
        else:
            obj = model.singleton.get()
            return redirect(
                reverse(
                    f"admin:{model._meta.app_label}"
                    f"_{model._meta.model_name}_change",
                    args=(obj.id,),
                )
            )
