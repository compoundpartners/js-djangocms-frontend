from django.utils.translation import gettext_lazy as _

from djangocms_frontend.models import FrontendUIItem


class Modal(FrontendUIItem):

    class Meta:
        proxy = True
        verbose_name = _("Modal")

    def get_short_description(self):
        return self.config.get("plugin_title", {}).get("title", "") or self.config.get("modal_id", "without id")
