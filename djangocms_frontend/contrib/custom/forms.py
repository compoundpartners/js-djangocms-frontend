from django import forms
from django.utils.translation import gettext_lazy as _
from entangled.forms import EntangledModelForm

from djangocms_frontend import settings
from .  import models


class RawHTMLForm(EntangledModelForm):

    class Meta:
        model = models.RawHTML
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
