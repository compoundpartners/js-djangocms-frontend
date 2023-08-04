from django import forms
from django.utils.translation import gettext_lazy as _
from entangled.forms import EntangledModelForm

from djangocms_frontend import settings
from djangocms_frontend.common.title import TitleFormMixin
from djangocms_frontend.fields import AttributesFormField
from djangocms_frontend.helpers import first_choice
from djangocms_frontend.models import FrontendUIItem
from .constants import (
    MODAL_TEMPLATE_CHOICES,
    PERSENTAGES,
    COOKIE_SETTINGS,
)


class ModalForm(
    TitleFormMixin,
    EntangledModelForm,
):

    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "template",
                "modal_id",
                "percentage_scrolled",
                "seconds_passed",
                "cookie_settings",
                "attributes",
            ]
        }

    template = forms.ChoiceField(
        label=_("Template"),
        choices=MODAL_TEMPLATE_CHOICES,
        initial=first_choice(MODAL_TEMPLATE_CHOICES),
    )
    modal_id = forms.CharField(
        label=_("Modal ID"),
        required=False,
    )
    percentage_scrolled = forms.ChoiceField(
        label=_("Percentage Scrolled"),
        choices=PERSENTAGES,
        initial=first_choice(PERSENTAGES),
        required=False,
    )
    seconds_passed = forms.IntegerField(
        label=_("Seconds Passed"),
        required=False,
    )
    cookie_settings = forms.ChoiceField(
        label=_("Cookie Settings"),
        choices=COOKIE_SETTINGS,
        initial=first_choice(COOKIE_SETTINGS),
        required=False,
    )
    attributes = AttributesFormField()

