from django import forms
from django.conf import settings as django_settings
from django.utils.translation import gettext_lazy as _
from entangled.forms import EntangledModelForm

from djangocms_frontend import settings

from djangocms_frontend.common.background import BackgroundFormMixin
from djangocms_frontend.common.foreground import ForegroundFormMixin
from djangocms_frontend.common.responsive import ResponsiveFormMixin
from djangocms_frontend.common.spacing import MarginFormMixin, PaddingFormMixin
from djangocms_frontend.fields import (
    AttributesFormField,
    ButtonGroup,
    ColoredButtonGroup,
    TagTypeFormField,
)
from djangocms_frontend.models import FrontendUIItem
from djangocms_frontend.helpers import first_choice
from .constants import LISTGROUP_STATE_CHOICES, LISTGROUP_TEMPLATE_CHOICES

if "djangocms_icon" in django_settings.INSTALLED_APPS:
    from djangocms_icon.fields import IconField
else:
    class IconField(forms.CharField):  # lgtm [py/missing-call-to-init]
        def __init__(self, *args, **kwargs):
            kwargs["widget"] = forms.HiddenInput
            super().__init__(*args, **kwargs)


class ListGroupForm(MarginFormMixin, 
                    BackgroundFormMixin,
                    ForegroundFormMixin,
                    ResponsiveFormMixin, 
                    EntangledModelForm):
    """
    Components > "List Group" Plugin
    https://getbootstrap.com/docs/5.0/components/list-group/
    """

    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "template",
                "list_group_flush",
                "attributes",
            ]
        }
        untangled_fields = ("tag_type", "foreground_image")

    template = forms.ChoiceField(
        label=_("template"),
        choices=LISTGROUP_TEMPLATE_CHOICES,
        initial=first_choice(LISTGROUP_TEMPLATE_CHOICES),
    )
    list_group_flush = forms.BooleanField(
        label=_("List group flush"),
        initial=False,
        required=False,
        help_text=_("Create lists of content in a card with a flush list group."),
    )
    attributes = AttributesFormField()
    tag_type = TagTypeFormField()


class ListGroupItemForm(PaddingFormMixin, 
                        ForegroundFormMixin,
                        ResponsiveFormMixin, 
                        EntangledModelForm):
    """
    Components > "List Group Item" Plugin
    https://getbootstrap.com/docs/5.0/components/list-group/
    """

    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "simple_content",
                "list_context",
                "list_state",
                "icon",
                "attributes",
            ]
        }
        untangled_fields = ("tag_type",)

    simple_content = forms.CharField(
        label=_("One line content"),
        required=False,
        help_text=_(
            "List item text. Is only show if this list item has no child plugins."
        ),
    )
    list_context = forms.ChoiceField(
        label=_("Context"),
        choices=settings.EMPTY_CHOICE + settings.COLOR_STYLE_CHOICES,
        initial=settings.EMPTY_CHOICE[0][0],
        required=False,
        widget=ColoredButtonGroup(),
    )
    list_state = forms.ChoiceField(
        label=_("State"),
        choices=settings.EMPTY_CHOICE + LISTGROUP_STATE_CHOICES,
        initial=settings.EMPTY_CHOICE[0][0],
        required=False,
        widget=ButtonGroup(attrs=dict(property="list_state")),
    )
    icon = IconField(
        label=_("Icon"),
        initial="",
        required=False,
    )
    attributes = AttributesFormField()
    tag_type = TagTypeFormField()
