"""Tests for migration 0003: the background alignment vocabulary repair.

`remap_config` is deliberately a pure function so the correctness of the
mapping can be tested without a database or the full app environment.

Run:  python tests/test_background_alignment_migration.py
"""
import importlib.util
import pathlib
import sys

MIGRATION = (pathlib.Path(__file__).resolve().parent.parent
             / "djangocms_frontend" / "migrations"
             / "0003_fix_background_alignment_vocabulary.py")
# No stubbing: the migration only does `from django.db import migrations`,
# which needs no configured settings, so this exercises the real thing --
# including RunPython.noop, which a stub got wrong.
spec = importlib.util.spec_from_file_location("mig0003", MIGRATION)
mig = importlib.util.module_from_spec(spec)
sys.modules["mig0003"] = mig
spec.loader.exec_module(mig)

H, V = mig.H_FIELD, mig.V_FIELD
fwd = lambda cfg: mig.remap_config(cfg, mig.TO_VERTICAL, mig.TO_HORIZONTAL)
rev = lambda cfg: mig.remap_config(cfg, mig.TO_HORIZONTAL, mig.TO_VERTICAL)

results = []
def check(name, cond, detail=""):
    results.append((name, bool(cond)))
    print(("  ok   " if cond else "  FAIL ") + name + (f"   [{detail}]" if detail and not cond else ""))

print("-- the case found in real content ------------------------------")
cfg, changes = fwd({V: "center", "other": 1})
check("vertical 'center' -> 'align-items-center'", cfg[V] == "align-items-center", cfg)
check("the change is reported", changes == [(V, "center", "align-items-center")], changes)
check("unrelated keys are untouched", cfg["other"] == 1, cfg)
check("the input dict is not mutated", "center" == {V: "center"}[V])

print("\n-- the risky values: a REAL rendering change, reported ----------")
for old, new in (("start", "align-items-start"), ("end", "align-items-end")):
    cfg, changes = fwd({V: old})
    check(f"vertical {old!r} -> {new!r}", cfg[V] == new, cfg)

print("\n-- the inverse staleness (vertical vocabulary in horizontal) ----")
cfg, changes = fwd({H: "align-items-center"})
check("horizontal 'align-items-center' -> 'center'", cfg[H] == "center", cfg)

print("\n-- idempotent: already-correct values are left alone ------------")
cfg, changes = fwd({V: "align-items-center", H: "center"})
check("no changes on correct data", changes == [], changes)
check("values unchanged", cfg[V] == "align-items-center" and cfg[H] == "center", cfg)
cfg2, changes2 = fwd(cfg)
check("running it twice changes nothing further", changes2 == [], changes2)

print("\n-- NOT reversible, and that is deliberate -----------------------")
# A naive inverse corrupts data: forwards leaves a valid horizontal `center`
# alone, so an inverse that maps the horizontal field would rewrite it to
# `align-items-center`. This asserts the trap exists, which is why the
# migration's backwards is RunPython.noop.
start = {V: "center", H: "center"}
forward, _ = fwd(start)
check("forwards fixes only the vertical field",
      forward == {V: "align-items-center", H: "center"}, forward)
naive_back, _ = rev(forward)
check("a naive inverse WOULD corrupt the valid horizontal value",
      naive_back[H] == "align-items-center", naive_back)
from django.db import migrations as real_migrations
check("so the migration declares no reverse",
      mig.backwards is real_migrations.RunPython.noop, mig.backwards)

print("\n-- tolerates junk ----------------------------------------------")
check("a non-dict config is returned untouched", mig.remap_config(None, {}, {})[0] is None)
check("an unknown value is left alone", fwd({V: "middle"})[0][V] == "middle")
check("an empty string is left alone", fwd({V: ""})[1] == [])
check("a non-string value is left alone", fwd({V: 3})[1] == [])

passed = sum(1 for _, ok in results if ok)
print(f"\n==== {passed}/{len(results)} checks passed ====")
raise SystemExit(0 if passed == len(results) else 1)
