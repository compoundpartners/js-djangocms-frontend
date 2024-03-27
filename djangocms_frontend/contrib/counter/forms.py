from django import forms
from django.conf import settings as django_settings
from django.core.exceptions import ValidationError
from django.db.models.fields.related import ManyToOneRel
from django.utils.translation import gettext_lazy as _
from entangled.forms import EntangledModelForm

from filer.fields.image import AdminImageFormField, FilerImageField
from filer.models import Image
from js_color_picker.forms import RGBColorField
from js_color_picker.widgets import ColorFieldWidget
from djangocms_frontend.common.background import BackgroundFormMixin
from djangocms_frontend.common.foreground import ForegroundFormMixin
from djangocms_frontend.fields import (
    AttributesFormField,
    TagTypeFormField,
    TemplateChoiceMixin,
    HTMLFormField,
)

if "djangocms_icon" in django_settings.INSTALLED_APPS:
    from djangocms_icon.fields import IconField
else:
    class IconField(forms.CharField):  # lgtm [py/missing-call-to-init]
        def __init__(self, *args, **kwargs):
            kwargs["widget"] = forms.HiddenInput
            super().__init__(*args, **kwargs)

from ... import settings
from ...helpers import first_choice
from ...models import FrontendUIItem
from .constants import COUNTER_TEMPLATE_CHOICES


class CounterForm(BackgroundFormMixin, ForegroundFormMixin, TemplateChoiceMixin, EntangledModelForm):

    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "template",
                "title",
                "counter",
                "icon",
                "prefix",
                "suffix",
                "content",
                "attributes",
            ]
        }

    template = forms.ChoiceField(
        label=_("Template"),
        choices=COUNTER_TEMPLATE_CHOICES,
        initial=first_choice(COUNTER_TEMPLATE_CHOICES),
        help_text=_("This is the template that will be used for the component."),
    )
    title = forms.CharField(
        label=_("Title"),
        required=False,
        initial="",
    )
    counter = forms.CharField(
        label=_("Counter"),
        required=True,
        initial="",
    )
    icon = IconField(
        label=_("Icon"),
        initial="",
        required=False,
    )
    prefix = forms.CharField(
        label=_("Prefix"),
        required=False,
        initial="",
    )
    suffix = forms.CharField(
        label=_("Suffix"),
        required=False,
        initial="",
    )
    content = HTMLFormField(
        label=_("Content"),
        required=False,
        initial="",
    )
    attributes = AttributesFormField()
    tag_type = TagTypeFormField()