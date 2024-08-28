from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from entangled.forms import EntangledModelFormMixin
from djangocms_frontend.helpers import insert_fields
from djangocms_frontend.settings import ANIMATION_CHOICES


class AnimationMixin:
    def render(self, context, instance, placeholder):
        #instance.add_attribute("title", instance.plugin_title.get("title", ""))
        return super().render(context, instance, placeholder)

    
    def get_fieldsets(self, request, obj=None):
        old = super().get_fieldsets(request, obj)
        fields = [
            "animation",
            "animation_duration",
            "animation_delay",
            "animation_repeat",
            "animation_on_hover",
        ]
        return insert_fields(
            old,
            fields,
            block=None,
            position=-1,
            blockname=_('Animation'),
        )

class AnimationFormMixin(EntangledModelFormMixin):
    class Meta:
        entangled_fields = {
            "config": [
                "animation",
                "animation_duration",
                "animation_delay",
                "animation_repeat",
                "animation_on_hover",
            ]
        }

    animation = forms.ChoiceField(
        label=_('Animation'),
        choices=ANIMATION_CHOICES,
        required=False,
        initial='',
    )
    animation_duration = forms.IntegerField(
        label=_('Duration (ms)'),
        required=False,
        initial=0,
    )
    animation_delay = forms.IntegerField(
        label=_('Delay (ms)'),
        required=False,
        initial=0,
    )
    animation_repeat = forms.IntegerField(
        label=_('Repeat'),
        required=False,
        initial=0,
    )
    animation_on_hover = forms.BooleanField(
        label=_('Play On Hover'),
        required=False,
        initial=False,
    )