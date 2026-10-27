"""Repair background alignment values stored in the wrong vocabulary.

The two background alignment fields deliberately use *different* vocabularies,
because ``ALIGN_MAP`` turns each into a CSS ``background-position`` word:

    background_position_alignment_horizontal   start | center | end
        -> left | center | right
    background_position_alignment_vertical     align-items-start | -center | -end
        -> top | center | bottom

Content exists that stores the horizontal vocabulary in the vertical field (and
in principle the reverse). Such a value is not among the field's choices, so:

* the admin form rejects the plugin on save -- the editor cannot re-save an
  untouched plugin without first fixing a field they never set;
* any API or import path that validates through the form rejects it too, which
  is how this was found: a plugin tree exported and re-imported failed on
  ``"Select a valid choice. center is not one of the available choices."``;
* ``ALIGN_MAP`` tolerates it at render time, which is why nobody noticed.

Rendering is unchanged for ``center`` (both vocabularies map to ``center``).
``start`` and ``end`` DO change: in the vertical field they currently render as
``left``/``right``, which is meaningless on that axis, and become ``top``/
``bottom``. That is the intended correction, not a regression -- but it is a
visible change, so the migration reports every value it rewrites.

Idempotent: a value already in the right vocabulary is left alone.
"""

from django.db import migrations

H_FIELD = "background_position_alignment_horizontal"
V_FIELD = "background_position_alignment_vertical"

#: vertical field: horizontal vocabulary -> the vertical one it should hold
TO_VERTICAL = {
    "start": "align-items-start",
    "center": "align-items-center",
    "end": "align-items-end",
}
#: horizontal field: vertical vocabulary -> the horizontal one it should hold
TO_HORIZONTAL = {value: key for key, value in TO_VERTICAL.items()}


def remap_config(config, to_vertical, to_horizontal):
    """Return ``(new_config, changes)`` without mutating the input.

    ``changes`` is a list of ``(field, old, new)`` for reporting. Kept a plain
    function so it can be tested without a database.
    """
    if not isinstance(config, dict):
        return config, []
    changes = []
    updated = dict(config)
    for field, mapping in ((V_FIELD, to_vertical), (H_FIELD, to_horizontal)):
        value = updated.get(field)
        if isinstance(value, str) and value in mapping:
            updated[field] = mapping[value]
            changes.append((field, value, updated[field]))
    return updated, changes


def _apply(apps, schema_editor, to_vertical, to_horizontal, direction):
    UIItem = apps.get_model("djangocms_frontend", "FrontendUIItem")
    # Only rows that could possibly match, so this stays cheap on large sites.
    candidates = UIItem.objects.filter(config__has_any_keys=[H_FIELD, V_FIELD])
    touched, report = [], []
    for item in candidates.iterator(chunk_size=500):
        config, changes = remap_config(item.config, to_vertical, to_horizontal)
        if not changes:
            continue
        item.config = config
        touched.append(item)
        report.extend((item.pk, item.plugin_type, *change) for change in changes)
        if len(touched) >= 500:
            UIItem.objects.bulk_update(touched, ["config"])
            touched = []
    if touched:
        UIItem.objects.bulk_update(touched, ["config"])

    if report:
        print(f"\n  {direction}: rewrote {len(report)} alignment value(s)")
        for pk, plugin_type, field, old, new in report[:40]:
            print(f"    plugin {pk} ({plugin_type}) {field}: {old!r} -> {new!r}")
        if len(report) > 40:
            print(f"    ... and {len(report) - 40} more")


def forwards(apps, schema_editor):
    _apply(apps, schema_editor, TO_VERTICAL, TO_HORIZONTAL, "forwards")


# Deliberately not reversible. This repairs invalid data, and the forward
# direction is not injective: a `center` left untouched in the horizontal field
# is indistinguishable from one this migration would have written there, so
# "undoing" it corrupts values that were always correct. (A test caught exactly
# that: a naive inverse turned a valid horizontal `center` into
# `align-items-center`.) There is also nothing worth restoring -- the previous
# state is a value the field's own form rejects.
backwards = migrations.RunPython.noop


class Migration(migrations.Migration):
    dependencies = [
        ("djangocms_frontend", "0002_auto_20221212_1107"),
    ]
    operations = [
        migrations.RunPython(forwards, backwards, elidable=False),
    ]
