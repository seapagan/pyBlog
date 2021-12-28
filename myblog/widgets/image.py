"""Custom widgets used by multiple apps."""
from django.forms.widgets import ClearableFileInput


class CustomImageField(ClearableFileInput):
    """Create our custom image upload widget."""

    template_name = "blog/widgets/clearable_file_input.html"
    initial_text = "Current Image"
    input_text = "Change Image"
    clear_checkbox_label = "Remove Image"
    # our own custom context variables.
    add_text_label = "Add an Image"
    show_initial = False

    def get_context(self, name, value, attrs):
        """Add our new variables to the context."""
        context = super().get_context(name, value, attrs)
        context["widget"].update(
            {
                "add_text_label": self.add_text_label,
                "show_initial": self.show_initial,
            }
        )
        return context
