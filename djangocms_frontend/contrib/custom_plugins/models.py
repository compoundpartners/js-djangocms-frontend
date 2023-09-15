from django.utils.translation import gettext_lazy as _

from djangocms_frontend.models import FrontendUIItem


class RawHTML(FrontendUIItem):

    class Meta:
        proxy = True
        verbose_name = _("Raw HTML")

    def get_short_description(self):
        return f"({self.content[:40]})"


class RawHTMLWithID(FrontendUIItem):

    class Meta:
        proxy = True
        verbose_name = _("Raw HTML With ID")

    def get_short_description(self):
        return f"({self.parameters})"


class GatedContent(FrontendUIItem):

    class Meta:
        proxy = True
        verbose_name = _("Gated Content")

    def get_short_description(self):
        return f"({self.link_url or self.cookie_name or self.pk})"


class GatedTrigger(FrontendUIItem):

    class Meta:
        proxy = True
        verbose_name = _("Gated Trigger")

    def get_short_description(self):
        return f"({self.pk})"


class Custom(FrontendUIItem):

    class Meta:
        proxy = True
        verbose_name = _("Custom plugin")

    def get_short_description(self):
        return f"({self.pk})"
