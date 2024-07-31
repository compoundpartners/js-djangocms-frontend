from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext

from djangocms_frontend.models import FrontendUIItem


class TitelModelMixin:
    pass


class Lightbox(TitelModelMixin, FrontendUIItem):

    class Meta:
        proxy = True
        verbose_name = _("Lightbox")
        _("Lightbox")

    def get_short_description(self):
        descr = self.config.get("plugin_title", {}).get("title", "") or self.config.get(
            "attributes", {}
        ).get("id", "")
        children_count = len(self.child_plugin_instances or [])
        children_count_str = ngettext(
            "(1 child)", "(%(count)i children)", children_count
        ) % {"count": children_count}
        if descr:
            children_count_str = f"{descr} {children_count_str}"
        return children_count_str