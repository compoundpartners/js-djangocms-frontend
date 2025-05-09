from cms.app_base import CMSAppExtension
from .cms_plugins import create_custom_plugin

class CustomPluginsCMSExtension(CMSAppExtension):
    def configure_app(self, cms_config):
        if hasattr(cms_config, 'custom_plugins_add'):
            for properties in cms_config.custom_plugins_add:
                create_custom_plugin(properties)