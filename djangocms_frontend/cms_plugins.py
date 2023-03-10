from cms.plugin_base import CMSPluginBase
from django.utils.encoding import force_str
from .helpers import get_template_path


class CMSUIPlugin(CMSPluginBase):
    render_template = "djangocms_frontend/html_container.html"
    change_form_template = "djangocms_frontend/admin/base.html"

    def __str__(self):
        return force_str(super().__str__())

    def get_render_template(self, context, instance, placeholder):
        default = "djangocms_frontend/html_container.html"
        if hasattr(self, 'render_template') and self.render_template != default:
            parts = self.render_template.split('/')
            try:
                name = parts[-1].split('.')[0]
            except IndexError:
                name = self.model.__name__.lower()
            if hasattr(self, 'render_template_prefix'):
                prefix = self.render_template_prefix
            else:
                prefix = name.split('_')[0]
            return get_template_path(prefix, None, name)
        return default
