from django import forms
from django.utils.translation import gettext_lazy as _
from entangled.forms import EntangledModelForm

from djangocms_frontend import settings
from djangocms_frontend.models import FrontendUIItem


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
