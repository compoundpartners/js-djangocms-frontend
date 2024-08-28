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
from djangocms_frontend.contrib.image.models import Image
from djangocms_frontend.contrib.image.cms_plugins import ImagePlugin
from ...cms_plugins import CMSUIPlugin
from ...common.title import TitleMixin
from ...helpers import add_plugin
from . import forms, models
from .constants import LIGHTBOX_TEMPLATE_CHOICES, LIGHTBOX_PLACEHOLDER_IMAGE


@plugin_pool.register_plugin
class LightboxPlugin(
    AttributesMixin,
    TitleMixin,
    CMSUIPlugin,
):

    name = _("Lightbox")
    module = _("Frontend")
    model = models.Lightbox
    form = forms.LightboxForm
    allow_children = True
    child_classes = [
        "GridColumnPlugin", "CardPlugin", "ShowcaseObjectPlugin", "ImagePlugin"
    ]

    fieldsets = [
        (
            None,
            {
                "fields": (
                    (
                        "create",
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
            extra = {
                'width': None, 
                'height': None, 
                'caption': '', 
                'picture': None, 
                'margin_x': '', 
                'margin_y': '', 
                'template': 'default', 
                'use_crop': False, 
                'alignment': '', 
                'file_link': None, 
                'attributes': {'class': 'img-fluid'}, 
                'new_window': False, 
                'use_upscale': False, 
                'lazy_loading': False, 
                'external_link': '', 
                'internal_link': '', 
                'picture_fluid': True, 
                'margin_devices': None, 
                'link_attributes': {}, 
                'picture_rounded': False, 
                'use_no_cropping': False, 
                'external_picture': LIGHTBOX_PLACEHOLDER_IMAGE, 
                'picture_thumbnail': False, 
                'thumbnail_options': None, 
                'external_link_type': '', 
                'use_responsive_image': 'inherit', 
                'responsive_visibility': None, 
                'use_automatic_scaling': False                
            }
            add_plugin(
                obj.placeholder,
                Image(
                    parent=obj,
                    placeholder=obj.placeholder,
                    position=obj.position + pos + 1,
                    language=obj.language,
                    plugin_type=ImagePlugin.__name__,
                    ui_item=Image.__class__.__name__,
                    config=extra,
                ),
            )

    def get_render_template(self, context, instance, placeholder):
        return get_plugin_template(
            instance,
            "lightbox",
            "lightbox",
            LIGHTBOX_TEMPLATE_CHOICES,
        )
