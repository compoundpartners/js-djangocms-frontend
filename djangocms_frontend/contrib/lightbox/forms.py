from copy import copy

from django import forms
from django.utils.translation import gettext_lazy as _
from entangled.forms import EntangledModelForm

from djangocms_frontend.fields import (
    AttributesFormField,
    TagTypeFormField,
)
from djangocms_frontend.helpers import first_choice
from djangocms_frontend.models import FrontendUIItem

from .constants import (
    LIGHTBOX_TEMPLATE_CHOICES,
)


class LightboxForm(
    EntangledModelForm,
):
    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "template",
                "attributes",
            ]
        }
        untangled_fields = (
            "tag_type",
            "create",
        )

    create = forms.IntegerField(
        label=_("Create children"),
        help_text=_("Number of images to create when saving."),
        required=False,
        min_value=0,
        max_value=99,
    )
    template = forms.ChoiceField(
        label=_("template"),
        choices=LIGHTBOX_TEMPLATE_CHOICES,
        initial=first_choice(LIGHTBOX_TEMPLATE_CHOICES),
    )
    attributes = AttributesFormField()
    tag_type = TagTypeFormField()


