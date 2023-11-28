from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _

from djangocms_frontend import settings
from djangocms_frontend.cms_plugins import CMSUIPlugin
from djangocms_frontend.common.attributes import AttributesMixin
from djangocms_frontend.common.background import BackgroundMixin
from djangocms_frontend.common.foreground import ForegroundMixin
from djangocms_frontend.common.responsive import ResponsiveMixin
from djangocms_frontend.common.spacing import MarginMixin, PaddingMixin
from djangocms_frontend.helpers import get_plugin_template
from djangocms_frontend.contrib import listgroup
from . import forms, models
from .constants import LISTGROUP_TEMPLATE_CHOICES

mixin_factory = settings.get_renderer(listgroup)


@plugin_pool.register_plugin
class ListGroupPlugin(
    mixin_factory("ListGroup"),
    AttributesMixin,
    ResponsiveMixin,
    MarginMixin,
    BackgroundMixin,
    ForegroundMixin,
    CMSUIPlugin,
):
    """
    Components > "List Group" Plugin
    https://getbootstrap.com/docs/5.0/components/list-group/
    """

    name = _("List group")
    module = _("Frontend")
    model = models.ListGroup
    form = forms.ListGroupForm
    change_form_template = "djangocms_frontend/admin/list-group.html"
    allow_children = True
    child_classes = ["ListGroupItemPlugin", "LinkPlugin"]
    # TODO consider linking to tab-content

    fieldsets = [
        (None, {"fields": ("template", "list_group_flush",)}),
    ]

    def get_render_template(self, context, instance, placeholder):
        return get_plugin_template(
            instance, "listgroup", "listgroup", LISTGROUP_TEMPLATE_CHOICES
        )


@plugin_pool.register_plugin
class ListGroupItemPlugin(
    mixin_factory("ListGroupItem"),
    AttributesMixin,
    ResponsiveMixin,
    PaddingMixin,
    CMSUIPlugin,
):
    """
    Components > "List Group Item" Plugin
    https://getbootstrap.com/docs/5.0/components/list-group/
    """

    name = _("List item")
    module = _("Frontend")
    model = models.ListGroupItem
    form = forms.ListGroupItemForm
    change_form_template = "djangocms_frontend/admin/list-group.html"
    allow_children = True
    parent_classes = ["ListGroupPlugin"]

    fieldsets = [
        (
            None,
            {
                "fields": (
                    "simple_content",
                    "list_context",
                    "list_state",
                )
            },
        ),
    ]
