"""Tests for migration 0004: repairing values the current forms reject.

`repair_config` is a pure function so the mappings can be tested without a
database or the full app environment.

Run:  python tests/test_rejected_value_repair.py
"""
import importlib.util
import pathlib
import sys

MIGRATION = (pathlib.Path(__file__).resolve().parent.parent
             / "djangocms_frontend" / "migrations"
             / "0004_repair_rejected_field_values.py")
spec = importlib.util.spec_from_file_location("mig0004", MIGRATION)
mig = importlib.util.module_from_spec(spec)
sys.modules["mig0004"] = mig
spec.loader.exec_module(mig)

results = []
def check(name, cond, detail=""):
    results.append((name, bool(cond)))
    print(("  ok   " if cond else "  FAIL ") + name + (f"   [{detail}]" if detail and not cond else ""))

NONE_OFFERED = set()
SOME_OFFERED = {"primary", "info"}

print("-- withdrawn colour contexts are cleared ------------------------")
cfg, ch = mig.repair_config({"alert_context": "info"}, NONE_OFFERED)
check("a Bootstrap context the project no longer offers -> ''", cfg["alert_context"] == "", cfg)
check("the change is reported", ch == [("alert_context", "info", "")], ch)
cfg, ch = mig.repair_config({"badge_context": "secondary"}, NONE_OFFERED)
check("badge_context too", cfg["badge_context"] == "", cfg)

print("\n-- but only if the project really withdrew it -------------------")
cfg, ch = mig.repair_config({"alert_context": "info"}, SOME_OFFERED)
check("a still-offered value is LEFT ALONE", cfg["alert_context"] == "info", cfg)
check("and nothing is reported", ch == [], ch)
cfg, ch = mig.repair_config({"alert_context": "brand-teal"}, NONE_OFFERED)
check("a custom (non-Bootstrap) value is never touched",
      cfg["alert_context"] == "brand-teal", cfg)

print("\n-- card_outline: boolean -> choice ------------------------------")
cfg, _ = mig.repair_config({"card_outline": True}, NONE_OFFERED)
check("True -> 'transparent' (an outlined card)", cfg["card_outline"] == "transparent", cfg)
cfg, _ = mig.repair_config({"card_outline": False}, NONE_OFFERED)
check("False -> '' (no outline, NOT transparent)", cfg["card_outline"] == "", cfg)
cfg, ch = mig.repair_config({"card_outline": "transparent"}, NONE_OFFERED)
check("an already-migrated value is left alone", ch == [], ch)

print("\n-- tab_index below its minimum ---------------------------------")
cfg, _ = mig.repair_config({"tab_index": 0}, NONE_OFFERED)
check("0 -> 1", cfg["tab_index"] == 1, cfg)
cfg, ch = mig.repair_config({"tab_index": 3}, NONE_OFFERED)
check("a valid index is left alone", ch == [], ch)
cfg, ch = mig.repair_config({"tab_index": True}, NONE_OFFERED)
check("a bool is not mistaken for an int < 1", ch == [], ch)

print("\n-- idempotent and non-destructive -------------------------------")
start = {"alert_context": "info", "card_outline": True, "tab_index": 0, "keep": "me"}
once, ch1 = mig.repair_config(start, NONE_OFFERED)
twice, ch2 = mig.repair_config(once, NONE_OFFERED)
check("three repairs in one pass", len(ch1) == 3, ch1)
check("running again changes nothing", ch2 == [], ch2)
check("unrelated keys survive", once["keep"] == "me", once)
check("the input is not mutated", start["alert_context"] == "info", start)
check("a non-dict config is returned untouched",
      mig.repair_config(None, NONE_OFFERED)[0] is None)

print("\n-- not reversible, deliberately ---------------------------------")
from django.db import migrations as real_migrations
check("backwards is a no-op", mig.backwards is real_migrations.RunPython.noop)

passed = sum(1 for _, ok in results if ok)
print(f"\n==== {passed}/{len(results)} checks passed ====")
raise SystemExit(0 if passed == len(results) else 1)
