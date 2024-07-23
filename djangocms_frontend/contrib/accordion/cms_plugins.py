from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _

from djangocms_frontend import settings
from djangocms_frontend.cms_plugins import CMSUIPlugin
from djangocms_frontend.common.attributes import AttributesMixin
from djangocms_frontend.common.background import BackgroundMixin
from djangocms_frontend.common.foreground import ForegroundMixin
from djangocms_frontend.helpers import add_plugin, get_plugin_template
from djangocms_frontend.contrib import accordion
from . import forms, models
from .constants import ACCORDION_TEMPLATE_CHOICES

mixin_factory = settings.get_renderer(accordion)


@plugin_pool.register_plugin
class AccordionPlugin(
    mixin_factory("Accordion"), 
    BackgroundMixin,
    ForegroundMixin,
    AttributesMixin, 
    CMSUIPlugin
):
    """
    Component > "Accordion" Plugin
    https://getbootstrap.com/docs/5.0/components/accordion/
    """

    name = _("Accordion")
    module = _("Frontend")
    model = models.Accordion
    form = forms.AccordionForm
    allow_children = True
    child_classes = [
        "AccordionItemPlugin",
    ]

    fieldsets = [
        (
            None,
            {
                "fields": (
                    "create",
                    (
                        "accordion_header_type",
                        "accordion_flush",
                        "template",
                    ),
                )
            },
        ),
    ]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        data = form.cleaned_data
        for pos in range(data["create"] if data["create"] is not None else 0):
            item = models.AccordionItem(
                parent=obj,
                position=obj.position + 1 + pos,
                placeholder=obj.placeholder,
                language=obj.language,
                plugin_type=AccordionItemPlugin.__name__,
                ui_item=models.AccordionItem.__class__.__name__,
                config=dict(
                    accordion_item_header=_("Item {}").format(pos + 1),
                    accordion_item_open=(pos == 0),
                ),
            ).initialize_from_form(forms.AccordionItemForm)
            add_plugin(obj.placeholder, item)

    def get_render_template(self, context, instance, placeholder):
        return get_plugin_template(
            instance, "accordion", "accordion", ACCORDION_TEMPLATE_CHOICES
        )


@plugin_pool.register_plugin
class AccordionItemPlugin(mixin_factory("AccordionItem"), CMSUIPlugin):
    """
    Component > "Collapse" Plugin
    https://getbootstrap.com/docs/5.0/components/collapse/
    """

    name = _("Accordion item")
    module = _("Frontend")
    model = models.AccordionItem
    form = forms.AccordionItemForm
    allow_children = True
    parent_classes = [
        "AccordionPlugin",
    ]

    fieldsets = [
        (
            None,
            {
                "fields": (
                    "accordion_item_header",
                    "accordion_item_open",
                )
            },
        ),
        (
            _("Advanced settings"),
            {
                "classes": ("collapse",),
                "fields": (
                    "tag_type",
                    "attributes",
                ),
            },
        ),
    ]

    def get_render_template(self, context, instance, placeholder):
        return get_plugin_template(
            instance.parent.get_plugin_instance()[0],
            "accordion",
            "accordion_item",
            ACCORDION_TEMPLATE_CHOICES,
        )
