from cms.plugin_pool import plugin_pool
from cms.utils.plugins import get_bound_plugins
from django.utils.translation import gettext_lazy as _

from djangocms_frontend import settings
from djangocms_frontend.helpers import get_plugin_template

from ...cms_plugins import CMSUIPlugin
from ...common.attributes import AttributesMixin
from ...common.spacing import SpacingMixin
from .. import utilities
from . import forms, models, constants

mixin_factory = settings.get_renderer(utilities)


@plugin_pool.register_plugin
class SpacingPlugin(mixin_factory("Spacing"), AttributesMixin, CMSUIPlugin):
    """
    Components > "Card" Plugin
    https://getbootstrap.com/docs/5.0/components/card/
    """

    name = _("Spacing")
    module = _("Frontend")
    model = models.Spacing
    form = forms.SpacingForm

    change_form_template = "djangocms_frontend/admin/spacing.html"
    allow_children = True

    fieldsets = [
        (
            None,
            {
                "fields": (
                    "space_property",
                    "space_sides",
                    "space_size",
                    "space_device",
                )
            },
        ),
    ]


@plugin_pool.register_plugin
class EditorNotePlugin(mixin_factory("EditorNote"), CMSUIPlugin):
    """Room for notes for editor only visible in edit mode"""

    name = _("Editor note")
    module = _("Frontend")
    allow_children = True
    change_form_template = "djangocms_frontend/admin/no_form.html"


@plugin_pool.register_plugin
class HeadingPlugin(
    mixin_factory("Heading"), AttributesMixin, SpacingMixin, CMSUIPlugin
):
    """Room for notes for editor only visible in edit mode"""

    name = _("Heading")
    module = _("Frontend")
    model = models.Heading
    form = forms.HeadingForm

    render_template = "djangocms_frontend/heading.html"
    allow_children = True

    fieldsets = [
        (
            None,
            {
                "fields": (
                    ("heading_level", "heading_id"),
                    "heading",
                    "heading_overline",
                    ("heading_number", "heading_alignment"),
                    "heading_context",
                )
            },
        ),
    ]

    def render(self, context, instance, placeholder):
        if not hasattr(context["request"], "TOC"):
            context["request"].TOC = []
        if toc := instance.get_toc_tuple():
            context["request"].TOC.append(toc)
        context["instance"] = instance
        return super().render(context, instance, placeholder)


class TOCMixin:
    """Mixin for CMS plugins that register entries in the Table of Contents.
    Uses DJANGOCMS_FRONTEND_TOC_PLUGIN_TUPLES setting to map plugin classes to TOC tuples."""

    def render(self, context, instance, placeholder):
        if not hasattr(context["request"], "TOC"):
            context["request"].TOC = []
        tuples_config = constants.TOC_PLUGIN_TUPLES
        plugin_name = self.__class__.__name__
        if plugin_name in tuples_config:
            toc_tuple = tuples_config[plugin_name](instance)
            if toc_tuple and toc_tuple[0] and toc_tuple[1]:
                context["request"].TOC.append(toc_tuple)
        return super().render(context, instance, placeholder)


def create_tree(request_toc):
    def process_level():
        nonlocal i

        previous_level = None
        toc_tree = []
        while i < len(request_toc):
            if previous_level is None or previous_level == request_toc[i][2]:
                toc_tree.append((request_toc[i][0], request_toc[i][1], None))
                previous_level = request_toc[i][2]
                i += 1
            elif previous_level < request_toc[i][2]:
                children = process_level()
                if toc_tree:
                    last = toc_tree[-1]
                    toc_tree[-1] = (last[0], last[1], children)
            elif previous_level > request_toc[i][2]:
                break
        return toc_tree

    i = 0
    return process_level()


@plugin_pool.register_plugin
class TOCPlugin(mixin_factory("TOC"), AttributesMixin, CMSUIPlugin):
    name = _("Table of contents")
    module = _("Frontend")

    model = models.TableOfContents
    form = forms.TableOfContentsForm

    fieldsets = [
        (
            None,
            {
                "fields": (
                    "template",
                )
            },
        ),
    ]

    def get_render_template(self, context, instance, placeholder):
        return get_plugin_template(
            instance, "toc", "toc", constants.TOC_TEMPLATE_CHOICES
        )

    def render(self, context, instance, placeholder):
        toc_list = self.get_toc(instance)
        if toc_list:
            context["toc"] = create_tree(toc_list)
        else:
            context["toc"] = []
        context["instance"] = instance
        return super().render(context, instance, placeholder)

    def get_toc(self, instance):
        content = []
        source = getattr(instance.placeholder, 'source', None)
        if source and hasattr(source, 'placeholders'):
            placeholders = source.placeholders.all()
        else:
            placeholders = [instance.placeholder]

        plugin_types = ['HeadingPlugin'] + list(constants.TOC_PLUGIN_TUPLES.keys())
        for ph in placeholders:
            for p in get_bound_plugins(
                ph.get_plugins(language=instance.language)
                .filter(plugin_type__in=plugin_types)
            ):
                if hasattr(p, 'get_toc_tuple'):
                    toc = p.get_toc_tuple()
                else:
                    toc = constants.TOC_PLUGIN_TUPLES.get(p.plugin_type, lambda x: tuple())(p)
                if toc and len(toc) == 3 and toc[0]:
                    content.append(toc)
        return content