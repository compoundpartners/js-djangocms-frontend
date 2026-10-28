from django import forms
from django.utils.translation import gettext_lazy as _
from entangled.forms import EntangledModelForm

from djangocms_frontend.fields import (
    AttributesFormField,
    ColoredButtonGroup,
    TagTypeFormField,
)
from djangocms_frontend.helpers import first_choice
from djangocms_frontend.models import FrontendUIItem
from djangocms_frontend.settings import COLOR_STYLE_CHOICES


class BadgeForm(EntangledModelForm):
    """
    Components > "Badge" Plugin
    https://getbootstrap.com/docs/5.0/components/badge/
    """

    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "badge_text",
                "badge_context",
                "badge_pills",
                "attributes",
            ]
        }

    badge_text = forms.CharField(
        label=_("Badge text"),
        max_length=255,
    )
    badge_context = forms.ChoiceField(
        label=_("Context"),
        choices=COLOR_STYLE_CHOICES,
        initial=first_choice(COLOR_STYLE_CHOICES),
        # A project may legitimately offer no colour styles at all --
        # COLOR_STYLE_CHOICES is a project setting, and emptying it is how you
        # decline these Bootstrap contexts. Left required, the field is then
        # unsatisfiable: `choices` is empty so no value validates, and
        # `required=True` rejects "" as well, so the plugin cannot be saved in
        # the admin or written through the service layer at all.
        required=bool(COLOR_STYLE_CHOICES),
        widget=ColoredButtonGroup(),
    )
    badge_pills = forms.BooleanField(
        label=_("Pills style"),
        initial=False,
        required=False,
        help_text=_("Activates the pills style."),
    )
    attributes = AttributesFormField()
    tag_type = TagTypeFormField()
