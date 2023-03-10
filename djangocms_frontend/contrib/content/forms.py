from django import forms
from django.conf import settings as django_settings
from django.utils.translation import gettext_lazy as _
from entangled.forms import EntangledModelForm
from js_color_picker.forms import RGBColorField
from js_color_picker.widgets import ColorFieldWidget

from djangocms_frontend.settings import ALIGN_CHOICES

from ... import settings
from ...common.background import BackgroundFormMixin
from ...common.responsive import ResponsiveFormMixin
from ...common.spacing import SpacingFormMixin
from ...fields import (
    AttributesFormField,
    HTMLFormField,
    IconGroup,
    TagTypeFormField,
    TemplateChoiceMixin
)
from ...helpers import first_choice
from ...models import FrontendUIItem
from .. import content
from .constants import CODE_TYPE_CHOICES, BLOCKQUOTE_TEMPLATE_CHOICES

mixin_factory = settings.get_forms(content)


class CodeForm(
    mixin_factory("Code"),
    SpacingFormMixin,
    ResponsiveFormMixin,
    BackgroundFormMixin,
    EntangledModelForm,
):
    """
    Content > "Code" Plugin
    https://getbootstrap.com/docs/5.0/content/code/
    """

    class Media:
        js = (
            "admin/vendor/ace/ace.js"
            if "djangocms_static_ace" in django_settings.INSTALLED_APPS
            else "https://cdnjs.cloudflare.com/ajax/libs/ace/1.9.6/ace.js",
        )

    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "code_content",
                "code_type",
                "attributes",
            ]
        }

    code_content = forms.CharField(
        label=_("Code"),
        initial="",
        required=True,
        widget=forms.widgets.Textarea(attrs={"class": "js-ckeditor-use-selected-text"}),
    )
    code_type = forms.ChoiceField(
        label=_("Code type"),
        choices=CODE_TYPE_CHOICES,
        initial=first_choice(CODE_TYPE_CHOICES),
        required=True,
    )
    attributes = AttributesFormField()
    tag_type = TagTypeFormField()


class BlockquoteForm(
    mixin_factory("Blockquote"),
    TemplateChoiceMixin,
    SpacingFormMixin,
    ResponsiveFormMixin,
    BackgroundFormMixin,
    EntangledModelForm,
):
    """
    Content > "Blockquote" Plugin
    https://getbootstrap.com/docs/5.0/content/typography/#blockquotes
    """

    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "template",
                "quote_content",
                "quote_origin_name",
                "quote_origin_role",
                "quote_origin_company",
                "quote_alignment",
                "foreground_color",
                "attributes",
            ]
        }

    template = forms.ChoiceField(
        label=_("Template"),
        choices=BLOCKQUOTE_TEMPLATE_CHOICES,
        initial=first_choice(BLOCKQUOTE_TEMPLATE_CHOICES),
        help_text=_("This is the template that will be used for the component."),
    )
    quote_content = HTMLFormField(
        label=_("Quote"),
        initial="",
        required=True,
    )
    quote_origin_name = forms.CharField(
        label=_("Name"),
        required=False,
    )
    quote_origin_role = forms.CharField(
        label=_("Role"),
        required=False,
    )
    quote_origin_company = forms.CharField(
        label=_("Company"),
        required=False,
    )
    quote_alignment = forms.ChoiceField(
        label=_("Alignment"),
        choices=settings.EMPTY_CHOICE + ALIGN_CHOICES,
        initial=settings.EMPTY_CHOICE[0][0],
        required=False,
        widget=IconGroup(),
    )
    foreground_color = RGBColorField(
        label=_('Foreground color'),
        required=False,
        widget=ColorFieldWidget(
            mode=settings.COLORPICKER_MODE,
            colors=settings.COLORPICKER_COLORS
        ),
    )
    attributes = AttributesFormField()
    tag_type = TagTypeFormField()

    def __init__(self, *args, **kwargs):
        FIELD_SETTINGS = {
            'quote_is_richtext': False
        }
        if type(settings.PLUGINS_AND_FIELDS.get('Blockquote')) is dict:
            FIELD_SETTINGS.update(settings.PLUGINS_AND_FIELDS.get('Blockquote'))
        super().__init__(*args, **kwargs)
        if not FIELD_SETTINGS['quote_is_richtext']:
            self.fields['quote_content'].widget = forms.Textarea()


class FigureForm(
    mixin_factory("Figure"),
    SpacingFormMixin,
    ResponsiveFormMixin,
    BackgroundFormMixin,
    EntangledModelForm,
):
    """
    Content > "Figure" Plugin
    https://getbootstrap.com/docs/5.0/content/figures/
    """

    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "figure_caption",
                "figure_alignment",
                "attributes",
            ]
        }

    figure_caption = HTMLFormField(
        label=_("Caption"),
        initial="",
        required=True,
    )
    figure_alignment = forms.ChoiceField(
        label=_("Alignment"),
        choices=settings.EMPTY_CHOICE + ALIGN_CHOICES,
        initial=settings.EMPTY_CHOICE[0][0],
        required=False,
        widget=IconGroup(),
    )
    attributes = AttributesFormField()
    tag_type = TagTypeFormField()

