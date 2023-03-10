from django.conf import settings
from django.utils.translation import gettext_lazy as _

CODE_TYPE_CHOICES = (
    ("code", _("Inline code")),
    ("pre", _("Code block")),
    ("var", _("Variables")),
    ("kbd", _("User input")),
    ("samp", _("Sample output")),
)

BLOCKQUOTE_TEMPLATE_CHOICES = (("default", _("Default")),) + tuple(getattr(
    settings,
    "DJANGOCMS_FRONTEND_BLOCKQUOTE_TEMPLATES",
    ()
))

