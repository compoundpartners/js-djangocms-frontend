from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _

from djangocms_frontend import settings
from djangocms_frontend.common.attributes import AttributesMixin
from djangocms_frontend.common.background import BackgroundMixin
from djangocms_frontend.common.foreground import ForegroundMixin
from djangocms_frontend.common.responsive import ResponsiveMixin
from djangocms_frontend.common.sizing import SizingMixin
from djangocms_frontend.common.spacing import SpacingMixin
from djangocms_frontend.helpers import get_plugin_template

from ...cms_plugins import CMSUIPlugin
from ...common.title import TitleMixin
from ...helpers import add_plugin
from .. import grid
from . import forms, models
from .constants import (
    GRID_TEMPLATE_CHOICES,
    ROW_TEMPLATE_CHOICES,
    COL_TEMPLATE_CHOICES,
)

mixin_factory = settings.get_renderer(grid)


@plugin_pool.register_plugin
class GridContainerPlugin(
    mixin_factory("GridContainer"),
    AttributesMixin,
    ResponsiveMixin,
    SpacingMixin,
    BackgroundMixin,
    ForegroundMixin,
    SizingMixin,
    TitleMixin,
    CMSUIPlugin,
):
    """
    Layout > Grid: "Container" Plugin
    https://getbootstrap.com/docs/5.0/layout/grid/
    """

    name = _("Container")
    module = _("Frontend")
    model = models.GridContainer
    form = forms.GridContainerForm
    change_form_template = "djangocms_frontend/admin/grid_container.html"
    allow_children = True

    fieldsets = [
        (
            None,
            {
                "fields": (
                    (
                        "template",
                        "container_type",
                        "plugin_title",
                    ),
                )
            },
        ),
    ]

    def get_render_template(self, context, instance, placeholder, template=None):
        return get_plugin_template(
            instance, "grid", "container", GRID_TEMPLATE_CHOICES
        )


@plugin_pool.register_plugin
class GridRowPlugin(
    mixin_factory("GridRow"),
    AttributesMixin,
    ResponsiveMixin,
    SpacingMixin,
    BackgroundMixin,
    ForegroundMixin,
    TitleMixin,
    CMSUIPlugin,
):
    """
    Layout > Grid: "Row" Plugin
    https://getbootstrap.com/docs/5.0/layout/grid/
    """

    name = _("Row")
    module = _("Frontend")
    model = models.GridRow
    form = forms.GridRowForm
    change_form_template = "djangocms_frontend/admin/grid_row.html"
    allow_children = True
    child_classes = ["GridColumnPlugin", "CardPlugin"]

    fieldsets = [
        (
            None,
            {
                "fields": (
                    (
                        "create",
                        "template",
                        "plugin_title",
                    ),
                )
            },
        ),
        (
            _("Responsive settings"),
            {
                "fields": ([f"row_cols_{size}" for size in settings.DEVICE_SIZES],),
            },
        ),
        (
            _("Alignment"),
            {
                "fields": (
                    ("vertical_alignment", "horizontal_alignment"),
                    "gutters",
                ),
            },
        ),
    ]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        data = form.cleaned_data
        for pos in range(data["create"] if data["create"] is not None else 0):
            extra = dict(column_alignment=None)
            for size in settings.DEVICE_SIZES:
                extra[f"{size}_col"] = data.get(f"create_{size}_col")
                extra[f"{size}_order"] = None
                extra[f"{size}_offset"] = None
                extra[f"{size}_ml"] = None
                extra[f"{size}_mr"] = None
            add_plugin(
                obj.placeholder,
                models.GridColumn(
                    parent=obj,
                    placeholder=obj.placeholder,
                    position=obj.position + pos + 1,
                    language=obj.language,
                    plugin_type=GridColumnPlugin.__name__,
                    ui_item=models.GridColumn.__class__.__name__,
                    config=extra,
                ),
            )

    def get_render_template(self, context, instance, placeholder):
        TEMPLATE_CHOICES = ROW_TEMPLATE_CHOICES
        plugin = instance
        if getattr(instance, 'template', None):
            pass
        elif instance.parent and instance.parent.plugin_type == "GridContainerPlugin":
            TEMPLATE_CHOICES = GRID_TEMPLATE_CHOICES
            plugin = instance.parent.get_plugin_instance()[0]
        return get_plugin_template(
            plugin,
            "grid",
            "grid_row",
            TEMPLATE_CHOICES,
        )


@plugin_pool.register_plugin
class GridColumnPlugin(
    mixin_factory("GridColumn"),
    AttributesMixin,
    ResponsiveMixin,
    SpacingMixin,
    BackgroundMixin,
    ForegroundMixin,
    TitleMixin,
    CMSUIPlugin,
):
    """
    Layout > Grid: "Column" Plugin
    https://getbootstrap.com/docs/5.0/layout/grid/
    """

    name = _("Column")
    module = _("Frontend")
    model = models.GridColumn
    form = forms.GridColumnForm
    change_form_template = "djangocms_frontend/admin/grid_column.html"
    allow_children = True
    require_parent = True
    # TODO it should allow for the responsive utilitiy class
    # https://getbootstrap.com/docs/5.0/layout/grid/#column-resets
    parent_classes = ["GridRowPlugin"]

    fieldsets = [
        (
            None,
            {
                "fields": (
                    (
                        "template",
                        "column_alignment",
                        "text_alignment",
                    ),
                )
            },
        ),
        (
            _("Responsive settings"),
            {
                "fields": (
                    [f"{size}_col" for size in settings.DEVICE_SIZES],
                    [f"{size}_order" for size in settings.DEVICE_SIZES],
                    [f"{size}_offset" for size in settings.DEVICE_SIZES],
                    [f"{size}_ms" for size in settings.DEVICE_SIZES],
                    [f"{size}_me" for size in settings.DEVICE_SIZES],
                )
            },
        ),
        (_("Title settings"), {"fields": ("plugin_title",)}),
    ]

    def get_render_template(self, context, instance, placeholder):
        TEMPLATE_CHOICES = COL_TEMPLATE_CHOICES
        plugin = instance
        if getattr(instance, 'template', None):
            pass
        elif instance.parent and instance.parent.plugin_type == "GridRowPlugin":
            TEMPLATE_CHOICES = ROW_TEMPLATE_CHOICES
            plugin = instance.parent.get_plugin_instance()[0]
        elif instance.parent and instance.parent.parent and instance.parent.parent.plugin_type == "GridContainerPlugin":
            TEMPLATE_CHOICES = GRID_TEMPLATE_CHOICES,
            plugin = instance.parent.parent.get_plugin_instance()[0],
        return get_plugin_template(
            plugin,
            "grid",
            "grid_col",
            TEMPLATE_CHOICES,
        )

