from django import forms
from django.utils.translation import gettext_lazy as _
from entangled.forms import EntangledModelForm

from djangocms_frontend import settings
from djangocms_frontend.contrib import accordion
from djangocms_frontend.fields import (
    AttributesFormField, 
    TagTypeFormField,
    TemplateChoiceMixin,
)
from djangocms_frontend.common.background import BackgroundFormMixin
from djangocms_frontend.common.foreground import ForegroundFormMixin
from djangocms_frontend.helpers import first_choice
from djangocms_frontend.models import FrontendUIItem
from .constants import ACCORDION_TEMPLATE_CHOICES

mixin_factory = settings.get_forms(accordion)


class AccordionForm(
    mixin_factory("Accordion"), 
    BackgroundFormMixin,
    ForegroundFormMixin,
    TemplateChoiceMixin, 
    EntangledModelForm
):
    """
    Components > "Accordion" Plugin
    https://getbootstrap.com/docs/5.0/components/accordion/
    """

    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "accordion_header_type",
                "accordion_flush",
                "template",
                "attributes",
            ]
        }
        untangled_fields = (
            "tag_type",
            "create",
        )

    create = forms.IntegerField(
        label=_("Create accordion items"),
        help_text=_("Number of accordion items to create when saving."),
        required=False,
        initial=False,
        min_value=0,
        max_value=20,
    )
    accordion_header_type = forms.ChoiceField(
        label=_("Header type"),
        initial=settings.EMPTY_CHOICE[0][0],
        choices=settings.EMPTY_CHOICE + settings.HEADER_CHOICES,
        required=False,
    )
    accordion_flush = forms.BooleanField(
        label=_("Integrate into parent"),
        initial=False,
        required=False,
        help_text=_(
            "Removes the default background-color, some borders, and some rounded corners "
            "to render accordions edge-to-edge with their parent container "
        ),
    )
    template = forms.ChoiceField(
        label=_("Layout"),
        choices=ACCORDION_TEMPLATE_CHOICES,
        initial=first_choice(ACCORDION_TEMPLATE_CHOICES),
        help_text=_("This is the template that will be used for the component."),
    )
    attributes = AttributesFormField()
    tag_type = TagTypeFormField()


class AccordionItemForm(mixin_factory("AccordionItem"), EntangledModelForm):
    """
    Components > "AccordionItem" Plugin
    https://getbootstrap.com/docs/5.0/components/accordion/
    """

    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "accordion_item_header",
                "accordion_item_open",
                "attributes",
            ]
        }
        untangled_fields = ("tag_type",)

    accordion_item_header = forms.CharField(
        label=_("Header"),
        required=True,
    )
    accordion_item_open = forms.BooleanField(
        label=_("Item open"),
        initial=False,
        required=False,
        help_text=_("Initially shows this accordion item on page load."),
    )
    attributes = AttributesFormField()
    tag_type = TagTypeFormField()
