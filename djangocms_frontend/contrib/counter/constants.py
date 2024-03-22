from django.conf import settings
from django.utils.translation import gettext_lazy as _

COUNTER_TEMPLATE_CHOICES = (("default", _("Default")),) + tuple(getattr(
    settings,
    "DJANGOCMS_FRONTEND_COUNTER_TEMPLATES",
    ()
))
