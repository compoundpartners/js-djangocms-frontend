from importlib import import_module

from djangocms_frontend import settings

try:
    module = import_module(f"..{settings.framework}.js_foreground", __name__)
    ForegroundFormMixin = module.ForegroundFormMixin
    ForegroundMixin = module.ForegroundMixin
except ModuleNotFoundError:

    class ForegroundMixin:
        pass

    class ForegroundFormMixin:
        pass
