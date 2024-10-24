from django.conf import settings
from django.utils.translation import gettext_lazy as _

TAB_TYPE_CHOICES = (
    ("nav-tabs", _("Tabs")),
    ("nav-pills", _("Pills")),
)

TAB_ALIGNMENT_CHOICES = (
    ("nav-fill", _("Fill")),
    ("nav-justified", _("Justified")),
    ("justify-content-start", _("Justify start")),
    ("justify-content-center", _("Justify center")),
    ("justify-content-end", _("Justify end")),
    ("flex-column", _("Column")),
)

TAB_EFFECT_CHOICES = getattr(
    settings,
    "DJANGOCMS_FRONTEND_TAB_EFFECTS",
    (("fade", _("Fade")),),
)

TAB_TEMPLATE_CHOICES = (("default", _("Default")),) + tuple(getattr(
    settings,
    "DJANGOCMS_FRONTEND_TAB_TEMPLATES",
    ()
))
