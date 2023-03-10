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
)

if "djangocms_icon" in django_settings.INSTALLED_APPS:
    from djangocms_icon.fields import IconField
else:
    class IconField(forms.CharField):  # lgtm [py/missing-call-to-init]
        def __init__(self, *args, **kwargs):
            kwargs["widget"] = forms.HiddenInput
            super().__init__(*args, **kwargs)

from ... import settings
from ...fields import HTMLFormField
from ...helpers import first_choice
from ...models import FrontendUIItem
from ..link.forms import AbstractLinkForm
from .constants import PROMO_TEMPLATE_CHOICES
from djangocms_frontend.fields import IconGroup


class PromoForm(BackgroundFormMixin, ForegroundFormMixin, TemplateChoiceMixin, AbstractLinkForm, EntangledModelForm):

    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "template",
                "link_name",
                "title",
                "subtitle",
                "content",
                "icon",
                "alignment",
                "attributes",
                "foreground_image",
            ]
        }
    link_is_optional = True

    template = forms.ChoiceField(
        label=_("Template"),
        choices=PROMO_TEMPLATE_CHOICES,
        initial=first_choice(PROMO_TEMPLATE_CHOICES),
        help_text=_("This is the template that will be used for the component."),
    )
    link_name = forms.CharField(
        label=_("Display name"),
        required=False,
    )
    title = forms.CharField(
        label=_("Title"),
        required=False,
        initial="",
    )
    subtitle = forms.CharField(
        label=_("Sub title"),
        required=False,
        initial="",
    )
    content = HTMLFormField(
        label=_("Content"),
        required=False,
        initial="",
    )
    icon = IconField(
        label=_("Icon"),
        initial="",
        required=False,
    )
    alignment = forms.ChoiceField(
        label=_("Alignment"),
        choices=settings.EMPTY_CHOICE + settings.ALIGN_CHOICES,
        required=False,
        widget=IconGroup(),
    )
    attributes = AttributesFormField()
    tag_type = TagTypeFormField()


    def clean(self):
        super().clean()
        content_field_names = (
            "title",
            "subtitle",
            "content",
        )
        content_fields = {
            key: self.cleaned_data.get(key, None) for key in content_field_names
        }
        provided_content_fields = {
            key: value for key, value in content_fields.items() if value
        }

        if len(provided_content_fields) == 0:
            raise ValidationError(_("Please provide a title, subtitle or content."))
