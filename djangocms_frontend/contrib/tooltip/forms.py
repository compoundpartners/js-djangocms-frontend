from django import forms
from django.conf import settings as django_settings
from django.core.exceptions import ValidationError
from django.db.models.fields.related import ManyToOneRel
from django.utils.translation import gettext_lazy as _
from entangled.forms import EntangledModelForm

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
from .constants import TOOLTIP_TEMPLATE_CHOICES, TOOLTIP_ALLOW_HTML

POSITION_CHOICES = (
    ('top', _('Top')), 
    ('left', _('Left')), 
    ('right', _('Right')), 
    ('bottom', _('Bottom')),
)

if not TOOLTIP_ALLOW_HTML:
    HTMLFormField = forms.CharField


class TooltipForm(BackgroundFormMixin, ForegroundFormMixin, TemplateChoiceMixin, EntangledModelForm):

    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "template",
                "tooltip_position",
                "content",
                "icon",
                "attributes",
            ]
        }
        untangled_fields = ["foreground_image", "foreground_color"]
    background_fields = ('background_color', )

    template = forms.ChoiceField(
        label=_("Template"),
        choices=TOOLTIP_TEMPLATE_CHOICES,
        initial=first_choice(TOOLTIP_TEMPLATE_CHOICES),
        help_text=_("This is the template that will be used for the component."),
    )
    tooltip_position = forms.ChoiceField(
        label=_('Position'),
        choices=POSITION_CHOICES,
        required=False,
    )
    content = HTMLFormField(
        label=_("Content"),
        required=True,
        initial="",
        widget=forms.Textarea if not TOOLTIP_ALLOW_HTML else None
    )
    icon = IconField(
        label=_("Icon"),
        initial="",
        required=False,
    )
    attributes = AttributesFormField()
    tag_type = TagTypeFormField()