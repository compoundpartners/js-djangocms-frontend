from django import forms
from django.utils.translation import gettext as _
from entangled.forms import EntangledModelForm

from djangocms_frontend import settings
from djangocms_frontend.common.spacing import PaddingFormMixin
from djangocms_frontend.common.background import BackgroundFormMixin
from djangocms_frontend.common.foreground import ForegroundFormMixin
from djangocms_frontend.fields import (
    AttributesFormField,
    ButtonGroup,
    IconGroup,
    TagTypeFormField,
    TemplateChoiceMixin,
)
from djangocms_frontend.helpers import first_choice
from djangocms_frontend.models import FrontendUIItem
from .constants import (
    TAB_ALIGNMENT_CHOICES,
    TAB_EFFECT_CHOICES,
    TAB_TEMPLATE_CHOICES,
    TAB_TYPE_CHOICES,
)


class TabForm(ForegroundFormMixin, BackgroundFormMixin, TemplateChoiceMixin, EntangledModelForm):
    """
    Components > "Navs - Tab" Plugin
    https://getbootstrap.com/docs/5.0/components/navs/
    """

    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "template",
                "tab_type",
                "tab_alignment",
                "tab_index",
                "tab_effect",
                "attributes",
            ]
        }
        untangled_fields = ("tag_type", "foreground_image")

    template = forms.ChoiceField(
        label=_("Layout"),
        choices=TAB_TEMPLATE_CHOICES,
        initial=first_choice(TAB_TEMPLATE_CHOICES),
        help_text=_("This is the template that will be used for the component."),
    )
    tab_type = forms.ChoiceField(
        label=_("Type"),
        choices=TAB_TYPE_CHOICES,
        initial=first_choice(TAB_TYPE_CHOICES),
        widget=ButtonGroup(attrs=dict(property="text")),
    )
    tab_alignment = forms.ChoiceField(
        label=_("Alignment"),
        choices=settings.EMPTY_CHOICE + TAB_ALIGNMENT_CHOICES,
        initial=settings.EMPTY_CHOICE[0][0],
        required=False,
        widget=IconGroup(),
    )
    tab_index = forms.IntegerField(
        label=_("Index"),
        min_value=1,
        required=False,
        help_text=_("Index of element to open on page load starting at 1."),
    )
    tab_effect = forms.ChoiceField(
        label=_("Animation effect"),
        choices=settings.EMPTY_CHOICE + TAB_EFFECT_CHOICES,
        required=False,
    )
    attributes = AttributesFormField()
    tag_type = TagTypeFormField()


class TabItemForm(ForegroundFormMixin, BackgroundFormMixin, PaddingFormMixin, EntangledModelForm):
    """
    Components > "Navs - Tab Item" Plugin
    https://getbootstrap.com/docs/5.0/components/navs/
    """

    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "tab_title",
                "tab_bordered",
                "attributes",
            ]
        }
        untangled_fields = ("tag_type", "foreground_image")

    tab_title = forms.CharField(
        label=_("Tab title"),
    )
    tab_bordered = forms.BooleanField(
        label=_("Bordered"),
        required=False,
        help_text=_("Add borders to the tab item"),
    )

    attributes = AttributesFormField()
    tag_type = TagTypeFormField()
