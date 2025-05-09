from django.conf import settings
from django.utils.translation import gettext_lazy as _

DEFAULT_TEMPLATE_CHOICES = (("default", _("Default")),)

GATED_CONTENT_TEMPLATES_CHOICES = DEFAULT_TEMPLATE_CHOICES + tuple(getattr(
    settings,
    "GATED_CONTENT_TEMPLATES",
    ()
))

CUSTOM_PLUGIN_TEMPLATES_CHOICES = DEFAULT_TEMPLATE_CHOICES + tuple(getattr(
    settings,
    "CUSTOM_PLUGIN_TEMPLATES",
    ()
))

def get_template_choices(module_and_model_name):
    return DEFAULT_TEMPLATE_CHOICES + tuple(getattr(
        settings,
        f"{module_and_model_name.upper()}_TEMPLATES",
        ()
    ))

PLUGINS_CHILD_CLASSES = getattr(
    settings,
    "PLUGINS_CHILD_CLASSES",
    {}
)