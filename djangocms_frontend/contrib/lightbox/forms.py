from copy import copy

from django import forms
from django.db.models.fields.related import ManyToOneRel
from django.utils.translation import gettext_lazy as _
from entangled.forms import EntangledModelForm
from filer.fields.folder import AdminFolderFormField, FilerFolderField
from filer.models import Folder

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
                "items_per_page",
            ]
        }
        untangled_fields = (
            "tag_type",
            "create",
            "folder",
        )

    create = forms.IntegerField(
        label=_("Create children"),
        help_text=_("Number of images to create when saving."),
        required=False,
        min_value=0,
        max_value=99,
    )
    folder = AdminFolderFormField(
        rel=ManyToOneRel(FilerFolderField, Folder, 'id'),
        queryset=Folder.objects.all(),
        to_field_name='id',
        required=False,
        label=_("or select folder"),
    )
    template = forms.ChoiceField(
        label=_("template"),
        choices=LIGHTBOX_TEMPLATE_CHOICES,
        initial=first_choice(LIGHTBOX_TEMPLATE_CHOICES),
    )
    items_per_page = forms.IntegerField(
        label=_("Items per page"),
        initial=0,
    )
    attributes = AttributesFormField()
    tag_type = TagTypeFormField()


