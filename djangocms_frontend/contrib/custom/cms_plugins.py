from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _

from ... import settings
from ...cms_plugins import CMSUIPlugin
from . import forms, models


@plugin_pool.register_plugin
class RawHTMLPlugin(CMSUIPlugin):

    name = _("Raw HTML")
    module = _("Frontend")
    model = models.RawHTML
    form = forms.RawHTMLForm
    allow_children = False
    render_template_prefix = "custom"
    render_template = "djangocms_frontend/raw_html.html"

    fieldsets = [
        (
            None,
            {
                "fields": [
                    "content",
                ]
            },
        ),
    ]
