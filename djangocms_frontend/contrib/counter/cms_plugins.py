from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _

from djangocms_frontend.helpers import get_plugin_template, get_related_object

from djangocms_frontend import settings
from djangocms_frontend.cms_plugins import CMSUIPlugin
from djangocms_frontend.common.attributes import AttributesMixin
from djangocms_frontend.common.background import BackgroundMixin
from djangocms_frontend.common.foreground import ForegroundMixin
from .. import carousel
from ..link.cms_plugins import LinkPluginMixin
from . import forms, models
from .constants import COUNTER_TEMPLATE_CHOICES


@plugin_pool.register_plugin
class CounterPlugin(AttributesMixin, BackgroundMixin, ForegroundMixin, CMSUIPlugin):
    name = _("Counter")
    module = _("Frontend")
    model = models.Counter
    form = forms.CounterForm
    allow_children = False

    fieldsets = [
        (
            None,
            {
                "fields": (
                    "template",
                    "title",
                    "counter",
                    "label",
                    "icon",
                    "prefix",
                    "suffix",
                    "content",
                )
            },
        ),
    ]

    def get_render_template(self, context, instance, placeholder):
        return get_plugin_template(
            instance, "counter", "counter", COUNTER_TEMPLATE_CHOICES
        )
