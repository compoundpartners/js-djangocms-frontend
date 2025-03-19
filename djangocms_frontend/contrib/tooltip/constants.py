from django.conf import settings
from django.utils.translation import gettext_lazy as _

TOOLTIP_TEMPLATE_CHOICES = (("default", _("Default")),) + tuple(getattr(
    settings,
    "DJANGOCMS_FRONTEND_TOOLTIP_TEMPLATES",
    ()
))

TOOLTIP_ALLOW_HTML = getattr(
    settings,
    "DJANGOCMS_FRONTEND_TOOLTIP_ALLOW_HTML",
    False
)
