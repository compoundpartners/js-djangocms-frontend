from importlib import import_module

from cms.forms.utils import get_page_choices
from cms.models import Page
from django.conf import settings as django_settings
from django.contrib.admin import site
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import FieldError, ObjectDoesNotExist
from django.urls import NoReverseMatch, reverse
from django.utils.encoding import force_str
from django.utils.html import mark_safe
from django.core.cache import cache
from django.utils.translation import get_language


LINK_MODELS = getattr(django_settings, "DJANGOCMS_FRONTEND_LINK_MODELS", [])


def import_models(link_models):
    models = {}
    for item in link_models:
        if item["class_path"] != "cms.models.Page":
            # CMS pages are collected using a cms function to preserve hierarchy
            parts = item["class_path"].rsplit(".", 1)
            models[item["class_path"]] = getattr(import_module(parts[0]), parts[1])
    return models
# =======
#             cls = getattr(import_module(parts[0]), parts[1])
#             queryset = cls.objects

#             if "manager_method" in item:
#                 queryset = getattr(queryset, item["manager_method"])()

#             if "filter" in item:
#                 for k, v in item["filter"].items():
#                     try:
#                         # Attempt to execute any callables in the filter dict.
#                         item["filter"][k] = v()
#                     except TypeError:
#                         # OK, it wasn't a callable, so, leave it be
#                         pass
#                 queryset = queryset.filter(**item["filter"])
#             else:
#                 if "manager_method" not in item:
#                     queryset = queryset.all()
#             if "order_by" in item:
#                 queryset = queryset.order_by(item["order_by"])
#             querysets.append((section, queryset, item.get("search", None), cls))
#     return querysets
# >>>>>>> upstream/master


def get_model_queryset(link_model, queryset):
    if "manager_method" in link_model:
        queryset = getattr(queryset, link_model["manager_method"])()
    if "filter" in link_model:
        for (k, v) in link_model["filter"].items():
            try:
                # Attempt to execute any callables in the filter dict.
                link_model["filter"][k] = v()
            except TypeError:
                # OK, it wasn't a callable, so, leave it be
                pass
        queryset = queryset.filter(**link_model["filter"])
    else:
        if "manager_method" not in link_model:
            queryset = queryset.all()
    if "order_by" in link_model:
        queryset = queryset.order_by(link_model["order_by"])
    return queryset


_models = import_models(LINK_MODELS)


def get_object_for_value(value):
    if isinstance(value, str) and "-" in value:
        type_id, obj_id = value.split("-", 1)
        try:
            content_type = ContentType.objects.get(id=type_id)
            return dict(
                model=f"{content_type.app_label}.{content_type.model}",
                pk=int(obj_id),
            )
        except (ObjectDoesNotExist, TypeError):
            pass
    return None


def get_link_choices(request, term="", lang=None, nbsp=""):
    global _models

    available_objects = []
    # Now create our list of cms pages
    type_id = ContentType.objects.get_for_model(Page).id
    for value, descr in get_page_choices(lang):
        if isinstance(descr, list):
            available_objects.append(
                {
                    "text": value,
                    "children": [
                        dict(
                            id=f"{type_id}-{page}",
                            text=mark_safe(name.replace("&nbsp;", nbsp)),
                        )
                        for page, name in descr
                        if not isinstance(term, str) or term.upper() in name.upper()
                    ],
                }
            )
        elif value and isinstance(value, int):
            available_objects.append(dict(id=f"{type_id}-{value}"))

    for link_model in LINK_MODELS:
        if link_model["class_path"] in _models:
            cls = _models[link_model["class_path"]]
            queryset = cls.objects
            search = link_model.get("search", None)
            type_class = ContentType.objects.get_for_model(cls)
            if search:
                queryset = get_model_queryset(link_model, queryset)
                try:
                    queryset = queryset.filter(**{search + "__icontains": term})
                except FieldError:
                    queryset.none()
                available_objects.append(
                    {
                        "text": force_str(link_model["type"]),
                        "children": [
                            dict(id=f"{type_class.id}-{obj.id}", text=str(obj))
                            for obj in queryset
                            #dm
                            # if request is None
                            # or model_admin
                            # and model_admin.has_view_permission(request, obj=obj)
                        ],
                    }
                )
            else:
                values = []
                language = get_language()
                if hasattr(queryset, 'versionable') and hasattr(queryset.versionable, 'content_model'):
                    for item in get_model_queryset(link_model, queryset.versionable.content_model.objects.filter(language=language)):
                        values.append(dict(id=f"{type_class.id}-{getattr(item, '%s_id' % item.grouper_field_name)}", text=str(item)))
                else:
                    for item in get_model_queryset(link_model, queryset):
                        values.append(dict(id=f"{type_class.id}-{item.id}", text=str(item)))
                available_objects.append(
                    {
                        "text": force_str(link_model["type"]),
                        "children": [
                            item
                            for item in values
                            if (not isinstance(term, str)) or term.upper() in str(item['text']).upper()
                        ],
                    }
                )
    return available_objects


def get_choices(request, term="", lang=None) -> list:
    def to_choices(json):
        return list(
            (elem["text"], to_choices(elem["children"]))
            if "children" in elem
            else (elem["id"], elem["text"])
            for elem in json
        )

    return to_choices(get_link_choices(request, term, lang, "&nbsp;"))


def ensure_select2_url_is_available() -> None:
    """Install the URLs"""
    try:
        reverse("dcf_autocomplete:ac_view")
    except NoReverseMatch:  # Not installed yet
        urlconf_module = import_module(django_settings.ROOT_URLCONF)
        from django.urls import clear_url_caches, include, path

        urlconf_module.urlpatterns = [
            path(
                "@dcf-links/",
                include(
                    "djangocms_frontend.contrib.link.urls",
                    namespace="dcf_autocomplete",
                ),
            )
        ] + urlconf_module.urlpatterns
        clear_url_caches()
