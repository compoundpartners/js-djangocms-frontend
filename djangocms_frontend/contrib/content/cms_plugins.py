from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _

from djangocms_frontend import settings
from djangocms_frontend.cms_plugins import CMSUIPlugin
from djangocms_frontend.common.attributes import AttributesMixin
from djangocms_frontend.common.background import BackgroundMixin
from djangocms_frontend.common.foreground import ForegroundMixin
from djangocms_frontend.common.responsive import ResponsiveMixin
from djangocms_frontend.common.spacing import SpacingMixin
from djangocms_frontend.helpers import get_plugin_template
from .. import content
from .constants import BLOCKQUOTE_TEMPLATE_CHOICES
from . import forms, models

mixin_factory = settings.get_renderer(content)


@plugin_pool.register_plugin
class CodePlugin(
    mixin_factory("Code"),
    AttributesMixin,
    ResponsiveMixin,
    SpacingMixin,
    BackgroundMixin,
    CMSUIPlugin,
):
    """
    Content > "Code" Plugin
    https://getbootstrap.com/docs/5.0/content/code/
    """

    name = _("Code")
    module = _("Frontend")
    model = models.CodeBlock
    form = forms.CodeForm
    change_form_template = "djangocms_frontend/admin/code.html"
    render_template_prefix = "content"

    fieldsets = [
        (
            None,
            {
                "fields": (
                    "code_content",
                    "code_type",
                )
            },
        ),
    ]


if settings.PLUGINS_AND_FIELDS.get('Blockquote'):
    @plugin_pool.register_plugin
    class BlockquotePlugin(
        mixin_factory("Blockquote"),
        AttributesMixin,
        ResponsiveMixin,
        SpacingMixin,
        BackgroundMixin,
        ForegroundMixin,
        CMSUIPlugin,
    ):
        """
        Content > "Blockquote" Plugin
        https://getbootstrap.com/docs/5.0/content/typography/#blockquotes
        """

        name = _("Blockquote")
        module = _("Frontend")
        model = models.Blockquote
        form = forms.BlockquoteForm
        change_form_template = "djangocms_frontend/admin/blockquote.html"
        allow_children = True

        fieldsets = [
            (
                None,
                {
                    "fields": (
                        "template",
                        "quote_content",
                        "quote_origin_name",
                        "quote_origin_role",
                        "quote_origin_company",
                        "quote_alignment",
                    )
                },
            ),
        ]

        def get_render_template(self, context, instance, placeholder):
            return get_plugin_template(
                instance, "content", "blockquote", BLOCKQUOTE_TEMPLATE_CHOICES
            )


if settings.PLUGINS_AND_FIELDS.get('Figure'):
    @plugin_pool.register_plugin
    class FigurePlugin(
        mixin_factory("Figure"),
        AttributesMixin,
        ResponsiveMixin,
        SpacingMixin,
        BackgroundMixin,
        CMSUIPlugin,
    ):
        """
        Content > "Figure" Plugin
        https://getbootstrap.com/docs/5.0/content/figures/
        """

        name = _("Figure")
        module = _("Frontend")
        model = models.Figure
        form = forms.FigureForm
        change_form_template = "djangocms_frontend/admin/figure.html"
        allow_children = True
        render_template_prefix = "content"

        fieldsets = [
            (
                None,
                {
                    "fields": (
                        "figure_caption",
                        "figure_alignment",
                    )
                },
            ),
        ]
