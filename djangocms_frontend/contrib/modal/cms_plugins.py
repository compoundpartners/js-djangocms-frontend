from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _

from djangocms_frontend import settings
from djangocms_frontend.common.attributes import AttributesMixin
from djangocms_frontend.common.title import TitleMixin
from djangocms_frontend.cms_plugins import CMSUIPlugin
from djangocms_frontend.helpers import get_plugin_template

from . import forms, models
from .constants import MODAL_TEMPLATE_CHOICES


@plugin_pool.register_plugin
class ModalPlugin(
    AttributesMixin,
    TitleMixin,
    CMSUIPlugin,
):

    name = _("Modal")
    module = _("Frontend")
    model = models.Modal
    form = forms.ModalForm
    allow_children = True

    fieldsets = [
        (
            None,
            {
                "fields": [
                        "template",
                        "plugin_title",
                        "modal_id",
                        "percentage_scrolled",
                        "seconds_passed",
                        "cookie_settings",
                ]
            },
        ),
    ]

    def get_render_template(self, context, instance, placeholder, template=None):
        return get_plugin_template(
            instance, "modal", "modal", MODAL_TEMPLATE_CHOICES
        )
