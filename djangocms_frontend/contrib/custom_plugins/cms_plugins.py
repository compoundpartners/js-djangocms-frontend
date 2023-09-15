from cms.plugin_pool import plugin_pool
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.encoding import escape_uri_path

from ... import settings
from ...cms_plugins import CMSUIPlugin
from ...common.attributes import AttributesMixin
from ...helpers import get_plugin_template
from . import forms, models
from .constants import (
    GATED_CONTENT_TEMPLATES_CHOICES,
    CUSTOM_PLUGIN_TEMPLATES_CHOICES,
)


@plugin_pool.register_plugin
class RawHTMLPlugin(CMSUIPlugin):

    name = _("Raw HTML")
    module = _("Frontend")
    model = models.RawHTML
    form = forms.RawHTMLForm
    allow_children = False
    render_template_prefix = "custom_plugins"
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

    def render(self, context, instance, placeholder):
        context.update({
            'content': instance.content,
        })
        return context


@plugin_pool.register_plugin
class RawHTMLPluginWithID(CMSUIPlugin):

    name = _("Raw HTML With ID")
    module = _("Frontend")
    model = models.RawHTMLWithID
    form = forms.RawHTMLFormWithID
    allow_children = False
    render_template_prefix = "custom_plugins"
    render_template = "djangocms_frontend/raw_html.html"

    fieldsets = [
        (
            None,
            {
                "fields": [
                    "content",
                    "parameters",
                ]
            },
        ),
    ]

    def render(self, context, instance, placeholder):
        request = context['request']
        html = instance.content
        for param in instance.parameters.split(','):
            param = param.strip()
            key = '[%s]' % param.upper()
            if key in ['[URL]','[URL_ESCAPED]']:
                url = request.build_absolute_uri()
                if key == '[URL_ESCAPED]':
                    url = escape_uri_path(url)
                html = html.replace(key, url)
            else:
                html = html.replace(key, request.GET.get(param) or request.POST.get(param, ''))
        context.update({
            'content': html,
        })
        return context



@plugin_pool.register_plugin
class GatedContentPlugin(CMSUIPlugin):

    name = _("Gated Content")
    module = _("Frontend")
    model = models.GatedContent
    form = forms.GatedContentForm
    allow_children = True

    fieldsets = [
        (
            None,
            {
                "fields": [
                    "template",
                    "link_url",
                    "cookie_name",
                ]
            },
        ),
    ]

    def render(self, context, instance, placeholder):
        context.update({
            'instance': instance,
            'link_url': instance.link_url,
            'cookie_name': instance.cookie_name,
        })
        return context

    def get_render_template(self, context, instance, placeholder, template=None):
        return get_plugin_template(
            instance, "custom_plugins", "gated_content", GATED_CONTENT_TEMPLATES_CHOICES
        )


@plugin_pool.register_plugin
class GatedTriggerPlugin(CMSUIPlugin):

    name = _("Gated Trigger")
    module = _("Frontend")
    model = models.GatedTrigger
    render_template_prefix = "custom_plugins"
    render_template = "djangocms_frontend/gated_trigger.html"
    allow_children = True

    fieldsets = [
        (
            None,
            {
                "fields": []
            },
        ),
    ]

    def render(self, context, instance, placeholder):
        context.update({
            'instance': instance,
        })
        return context


@plugin_pool.register_plugin
class CustomPlugin(AttributesMixin, CMSUIPlugin):

    name = _("Custom Plugin")
    module = _("Frontend")
    model = models.Custom
    form = forms.CustomForm
    allow_children = True

    fieldsets = [
        (
            None,
            {
                "fields": [
                    "template",
                ]
            },
        ),
    ]

    def render(self, context, instance, placeholder):
        context.update({
            'instance': instance,
        })
        return context

    def get_render_template(self, context, instance, placeholder, template=None):
        return get_plugin_template(
            instance, "custom_plugins", "custom_plugins", CUSTOM_PLUGIN_TEMPLATES_CHOICES
        )
