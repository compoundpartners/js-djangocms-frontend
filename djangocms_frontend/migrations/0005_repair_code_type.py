"""Repair `code_type` values that are no longer offered.

`CodeBlock.code_type` chooses the HTML element a code snippet is marked up
with. The choices are a static tuple in this package -- code/pre/var/kbd/samp
-- but content exists holding `html`, which looks like a value from an earlier
vocabulary where the field named a *language* rather than an element.

There is no faithful mapping from a language to an element, so the field's own
declared ``initial`` is used: whatever a newly-created plugin would get. That
is a deliberate choice of "the default" over a guess at intent.

Kept separate from 0004 because the cause is different -- 0004 repairs values
withdrawn by project configuration or changed in type, this repairs a value
dropped from a static vocabulary in this package.
"""

from django.db import migrations

FIELD = "code_type"
#: Mirrors CodeBlock's form field. Hardcoded rather than read from the form so
#: the migration is deterministic and does not depend on runtime imports.
VALID = ("code", "pre", "var", "kbd", "samp")
#: The field's declared ``initial``.
FALLBACK = "code"


def repair_config(config):
    """Return ``(new_config, changes)``; never mutates the input."""
    if not isinstance(config, dict):
        return config, []
    value = config.get(FIELD)
    if not isinstance(value, str) or not value or value in VALID:
        return config, []
    updated = dict(config)
    updated[FIELD] = FALLBACK
    return updated, [(FIELD, value, FALLBACK)]


def forwards(apps, schema_editor):
    UIItem = apps.get_model("djangocms_frontend", "FrontendUIItem")
    touched, report = [], []
    for item in (UIItem.objects
                 .filter(config__has_key=FIELD)
                 .iterator(chunk_size=500)):
        config, changes = repair_config(item.config)
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
        print(f"\n  repaired {len(report)} code_type value(s)")
        for pk, ptype, field, old, new in report:
            print(f"    plugin {pk} ({ptype}) {field}: {old!r} -> {new!r}")
    else:
        print("\n  nothing to repair")


# Not reversible: the prior value is one the field refuses, as with 0003/0004.
backwards = migrations.RunPython.noop


class Migration(migrations.Migration):
    dependencies = [
        ("djangocms_frontend", "0004_repair_rejected_field_values"),
    ]
    operations = [
        migrations.RunPython(forwards, backwards, elidable=False),
    ]
