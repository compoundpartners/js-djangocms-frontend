from django.conf import settings
from django.utils.translation import gettext_lazy as _


GATED_CONTENT_TEMPLATES_CHOICES = (("default", _("Default")),) + tuple(getattr(
    settings,
    "GATED_CONTENT_TEMPLATES",
    ()
))
CUSTOM_PLUGIN_TEMPLATES_CHOICES = (("default", _("Default")),) + tuple(getattr(
    settings,
    "CUSTOM_PLUGIN_TEMPLATES",
    ()
))
