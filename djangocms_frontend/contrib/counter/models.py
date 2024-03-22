from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _

from djangocms_frontend.models import FrontendUIItem
from djangocms_frontend.contrib.link.models import GetLinkMixin


class Counter(GetLinkMixin, FrontendUIItem):

    class Meta:
        proxy = True
        verbose_name = _("Counter")

    def get_short_description(self):
        content_text = ""

        if self.content:
            text = strip_tags(self.content).strip()
            if len(text) > 100:
                content_text = f"{text[:100]}..."
            else:
                content_text = f"{text}"

        return self.title or content_text
