from django.utils.translation import gettext_lazy as _

from djangocms_frontend.models import FrontendUIItem


class RawHTML(FrontendUIItem):

    class Meta:
        proxy = True
        verbose_name = _("Raw HTML")

    def get_short_description(self):
        return f"({self.content[:40]})"
