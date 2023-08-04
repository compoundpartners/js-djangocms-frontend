from django.conf import settings
from django.utils.translation import gettext_lazy as _


MODAL_TEMPLATE_CHOICES = (("default", _("Default")),) + tuple(getattr(
    settings,
    "DJANGOCMS_FRONTEND_MODAL_TEMPLATES",
    ()
))

PERSENTAGES = (
    ('', 'default'),
    ('5', '5%'),
    ('25', '25%'),
    ('50', '50%'),
    ('75', '75%'),
    ('90', '90%'),
    ('100', '100%'),
)


COOKIE_SETTINGS = (
    ('', 'Show every time (default)'),
    ('once-per-session', 'Cap at one view per session'),
    ('once-ever', 'Show once ever'),
)
