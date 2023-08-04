from django.conf import settings
from django.utils.translation import gettext_lazy as _

LISTGROUP_STATE_CHOICES = (
    ("active", _("Active")),
    ("disabled", _("Disabled")),
)

LISTGROUP_TEMPLATE_CHOICES = (("default", _("Default")),) + tuple(getattr(
    settings,
    "DJANGOCMS_FRONTEND_LISTGROUP_TEMPLATES",
    ()
))
