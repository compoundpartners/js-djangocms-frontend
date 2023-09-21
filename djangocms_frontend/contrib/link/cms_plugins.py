from cms.plugin_pool import plugin_pool
from django.apps import apps
from django.conf import settings as django_settings
from django.utils.translation import gettext_lazy as _

from djangocms_frontend.helpers import get_plugin_template, insert_fields

from ... import settings
from ...cms_plugins import CMSUIPlugin
from ...common.attributes import AttributesMixin
from ...common.spacing import SpacingMixin
from .. import link
from . import forms, models
from .constants import USE_LINK_ICONS

mixin_factory = settings.get_renderer(link)

is_there = lambda x, y: x in y and y[x]
split = lambda x: tuple((x[i], x[i+1]) for i in range(0, len(x)-1, 2)) + tuple((x[-1],) if len(x) % 2 else tuple())

setup = settings.LINK_SETTINGS
setup.update(
    getattr(django_settings, 'DJANGOCMS_FRONTEND_LINK_PLUGIN_SETTINGS', {})
)

fields = ["name", "link_type", "external_link",
          "internal_link", "external_link_type", 
          "new_window", "link_context", "link_size",
          "link_outline", "link_block", "link_stretched"]
UILINK_FIELDS = split([f for f in fields if is_there(f, setup)])

UILINK_FIELDSET = [
    (
        None,
        {
            "fields": ("template",)
            + (
                UILINK_FIELDS + (("icon_left", "icon_right"),)
                if USE_LINK_ICONS
                else UILINK_FIELDS
            )
        },
    ),
]
if is_there("file_link", setup):
    UILINK_FIELDSET += [
        (
            _("Link settings"),
            {
                "classes": ("collapse",),
                "fields": (
                    #dm ("mailto", "phone"),
                    #dm ("anchor", "target"),
                    ("file_link",),
                ),
            },
        ),
    ]


class LinkPluginMixin:
    link_fields = ["external_link", "internal_link", 
                   "external_link_type", "new_window", "file_link"]

    link_fieldset_position = None
    link_show_name = True

    def get_form(self, request, obj=None, change=False, **kwargs):
        """The link form needs the request object to check permissions"""
        form = super().get_form(request, obj, change, **kwargs)
        form.request = request
        return form
    
    def get_link_fields(self):
        model_name = self.model.__name__.upper()
        setup = settings.LINK_SETTINGS
        setup.update(
            getattr(django_settings, 'DJANGOCMS_FRONTEND_%s_LINK_SETTINGS' % model_name, {})
        )
        fields = split([f for f in self.link_fields if is_there(f, setup)])
        if self.link_show_name:
            fields = (("link_name",),) + fields
        return fields
        
    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if self.link_fieldset_position is not None:
            fieldsets = insert_fields(
                fieldsets,
                self.get_link_fields(),
                blockname=_("Link settings"),
                position=self.link_fieldset_position,
            )
        return fieldsets


class LinkPlugin(
    mixin_factory("Link"), AttributesMixin, SpacingMixin, LinkPluginMixin, CMSUIPlugin
):
    """
    Components > "Button" Plugin
    https://getbootstrap.com/docs/5.0/components/buttons/
    """

    name = _("Link / Button")
    module = _("Frontend")
    model = models.Link
    form = forms.LinkForm
    change_form_template = "djangocms_frontend/admin/link.html"
    text_enabled = True
    allow_children = True

    fieldsets = UILINK_FIELDSET

    def get_render_template(self, context, instance, placeholder):
        return get_plugin_template(
            instance, "link", "link", settings.LINK_TEMPLATE_CHOICES
        )


if "djangocms_frontend.contrib.link" in django_settings.INSTALLED_APPS:
    #  Only register plugin if in INSTALLED_APPS

    plugin_pool.register_plugin(LinkPlugin)
