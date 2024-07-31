from django.conf import settings
from django.utils.translation import gettext_lazy as _


LIGHTBOX_TEMPLATE_CHOICES = (("default", _("Default")),) + tuple(getattr(
    settings,
    "LIGHTBOX_TEMPLATE_CHOICES",
    ()
))
