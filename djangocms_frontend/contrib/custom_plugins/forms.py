from django import forms
from django.utils.translation import gettext_lazy as _
from entangled.forms import EntangledModelForm

from djangocms_frontend import settings
from djangocms_frontend.models import FrontendUIItem

from djangocms_frontend.helpers import first_choice
from djangocms_frontend.fields import (
    AttributesFormField,
    TemplateChoiceMixin,
)
from .constants import (
    GATED_CONTENT_TEMPLATES_CHOICES,
    CUSTOM_PLUGIN_TEMPLATES_CHOICES,
)


class RawHTMLForm(EntangledModelForm):

    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "content",
            ]
        }
    content = forms.CharField(
        label=_("Content"),
        required=False,
        widget=forms.Textarea()
    )


class RawHTMLFormWithID(EntangledModelForm):

    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "content",
                "parameters",
            ]
        }
    content = forms.CharField(
        label=_("Content"),
        required=False,
        widget=forms.Textarea()
    )
    parameters = forms.CharField(
        label=_('parameters'),
        required=False,
    )


class GatedContentForm(TemplateChoiceMixin, EntangledModelForm):

    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "template",
                "link_url",
                "cookie_name",
            ]
        }
    template = forms.ChoiceField(
        label=_("Template"),
        choices=GATED_CONTENT_TEMPLATES_CHOICES,
        initial=first_choice(GATED_CONTENT_TEMPLATES_CHOICES),
        help_text=_("This is the template that will be used for the component."),
    )
    link_url = forms.CharField(
        label=_("Link url"),
        required=False,
    )
    cookie_name = forms.CharField(
        label=_('Cookie name'),
        required=False,
    )


class CustomForm(TemplateChoiceMixin, EntangledModelForm):

    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "template",
                "attributes",
            ]
        }
    template = forms.ChoiceField(
        label=_("Template"),
        choices=CUSTOM_PLUGIN_TEMPLATES_CHOICES,
        initial=first_choice(CUSTOM_PLUGIN_TEMPLATES_CHOICES),
        help_text=_("This is the template that will be used for the component."),
    )
    attributes = AttributesFormField()