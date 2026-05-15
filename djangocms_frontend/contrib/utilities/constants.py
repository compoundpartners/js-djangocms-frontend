from django.conf import settings
from django.utils.translation import gettext_lazy as _

#dict with plugin class name as key and value function returned toc tuple
TOC_PLUGIN_TUPLES = getattr(
    settings,
    "DJANGOCMS_FRONTEND_TOC_PLUGIN_TUPLES",
    {},
)

TOC_TEMPLATE_CHOICES = (("default", _("Default")),) + tuple(getattr(
    settings,
    "DJANGOCMS_FRONTEND_TOC_TEMPLATES",
    ()
))
