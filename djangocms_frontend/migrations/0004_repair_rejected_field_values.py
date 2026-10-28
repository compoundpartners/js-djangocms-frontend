"""Repair stored values the current forms reject.

Found by running every plugin on a real site through its own
``clean_plugin_data``, which is what the django CMS 6 service layer does for
any write. 21 of 656 plugins held values their form no longer accepts -- so the
admin refuses to save them, and any API or import path refuses too, while the
templates render them happily. Three distinct causes, repaired separately here.

Each repair reports every value it rewrites, because some of them change what
the page renders and that should be visible in the deploy log rather than
discovered later.
"""

from django.db import migrations

# --- 1. withdrawn colour-style contexts ------------------------------------
# `alert_context` / `badge_context` take their choices from the project setting
# DJANGOCMS_FRONTEND_COLOR_STYLE_CHOICES. A project that declines these
# Bootstrap contexts empties that setting, which orphans any content already
# using one. Only values that are BOTH a known Bootstrap context AND absent
# from the project's current choices are cleared, so a custom or
# still-offered value is never touched.
CONTEXT_FIELDS = ("alert_context", "badge_context")
BOOTSTRAP_CONTEXTS = frozenset({
    "primary", "secondary", "success", "danger",
    "warning", "info", "light", "dark",
})

# --- 2. card_outline changed from a boolean to a choice --------------------
# Stored as Python True/False; the field now accepts "" or "transparent". An
# outlined card is the transparent-background variant, so True maps to it and
# False to "" (no outline). Mapping False to "transparent" instead would turn
# three plain cards into outlined ones.
OUTLINE = {True: "transparent", False: ""}

# --- 3. tab_index below its minimum ---------------------------------------
# The field validates >= 1; content exists holding 0.
TAB_INDEX_FIELD = "tab_index"
TAB_INDEX_MIN = 1


def _offered_contexts():
    """The colour contexts this project currently offers."""
    from django.conf import settings

    choices = getattr(settings, "DJANGOCMS_FRONTEND_COLOR_STYLE_CHOICES", None)
    if choices is None:
        from djangocms_frontend import settings as frontend_settings
        choices = getattr(frontend_settings, "COLOR_STYLE_CHOICES", ())
    return {str(code) for code, _label in (choices or ())}


def repair_config(config, offered):
    """Return ``(new_config, changes)``; never mutates the input.

    A plain function so the mapping can be tested without a database.
    """
    if not isinstance(config, dict):
        return config, []
    updated, changes = dict(config), []

    for field in CONTEXT_FIELDS:
        value = updated.get(field)
        if (isinstance(value, str) and value
                and value in BOOTSTRAP_CONTEXTS and value not in offered):
            updated[field] = ""
            changes.append((field, value, ""))

    if "card_outline" in updated and isinstance(updated["card_outline"], bool):
        old = updated["card_outline"]
        updated["card_outline"] = OUTLINE[old]
        changes.append(("card_outline", old, updated["card_outline"]))

    value = updated.get(TAB_INDEX_FIELD)
    if isinstance(value, int) and not isinstance(value, bool) and value < TAB_INDEX_MIN:
        updated[TAB_INDEX_FIELD] = TAB_INDEX_MIN
        changes.append((TAB_INDEX_FIELD, value, TAB_INDEX_MIN))

    return updated, changes


def forwards(apps, schema_editor):
    UIItem = apps.get_model("djangocms_frontend", "FrontendUIItem")
    offered = _offered_contexts()
    keys = list(CONTEXT_FIELDS) + ["card_outline", TAB_INDEX_FIELD]
    touched, report = [], []
    for item in (UIItem.objects
                 .filter(config__has_any_keys=keys)
                 .iterator(chunk_size=500)):
        config, changes = repair_config(item.config, offered)
        if not changes:
            continue
        item.config = config
        touched.append(item)
        report.extend((item.pk, item.plugin_type, *c) for c in changes)
        if len(touched) >= 500:
            UIItem.objects.bulk_update(touched, ["config"])
            touched = []
    if touched:
        UIItem.objects.bulk_update(touched, ["config"])

    if report:
        print(f"\n  repaired {len(report)} value(s) the forms reject")
        for pk, ptype, field, old, new in report:
            print(f"    plugin {pk} ({ptype}) {field}: {old!r} -> {new!r}")
    else:
        print("\n  nothing to repair")


# Not reversible, for the same reason as 0003: this repairs invalid data, and
# the previous state is a value the field's own form refuses. Restoring it
# would re-break the content.
backwards = migrations.RunPython.noop


class Migration(migrations.Migration):
    dependencies = [
        ("djangocms_frontend", "0003_fix_background_alignment_vocabulary"),
    ]
    operations = [
        migrations.RunPython(forwards, backwards, elidable=False),
    ]
