from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _

from djangocms_frontend.helpers import get_plugin_template, get_related_object

from djangocms_frontend import settings
from djangocms_frontend.cms_plugins import CMSUIPlugin
from djangocms_frontend.common.attributes import AttributesMixin
from djangocms_frontend.common.background import BackgroundMixin
from djangocms_frontend.common.foreground import ForegroundMixin
from djangocms_frontend.common.animation import AnimationMixin
from ..link.cms_plugins import LinkPluginMixin
from . import forms, models
from .constants import PROMO_TEMPLATE_CHOICES


@plugin_pool.register_plugin
class PromoPlugin(
    LinkPluginMixin, 
    AttributesMixin, 
    BackgroundMixin, 
    ForegroundMixin, 
    AnimationMixin,
    CMSUIPlugin
):
    name = _("Promo")
    module = _("Frontend")
    model = models.Promo
    form = forms.PromoForm
    allow_children = False

    link_fieldset_position = -1
    link_show_name = True

    fieldsets = [
        (
            None,
            {
                "fields": (
                    "template",
                    "title",
                    "subtitle",
                    "content",
                    "icon",
                    "alignment",
                    "modal_video",
                )
            },
        ),
    ]

    def get_render_template(self, context, instance, placeholder):
        return get_plugin_template(
            instance, "promo", "promo", PROMO_TEMPLATE_CHOICES
        )
