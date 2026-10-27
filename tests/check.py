#!/usr/bin/env python3
"""Re-run the exporter on the worked example and compare with what the repository carries.

Passes when the graph has the same number of triples, the three queries give the same answers, and the committed
summary.json is what the exporter writes. Exit code 0 when it passes, 1 otherwise."""
import json
import pathlib
import shutil
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
import dps_to_prov  # noqa: E402

EXAMPLE = ROOT / "examples" / "invoice-approval"


def main():
    committed = json.loads((EXAMPLE / "summary.json").read_text(encoding="utf-8"))
    with tempfile.TemporaryDirectory() as tmp:
        work = pathlib.Path(tmp) / "example"
        shutil.copytree(EXAMPLE, work)
        result = dps_to_prov.export(work, committed["base"])
        same_jsonld = (work / "provenance.jsonld").read_bytes() == (EXAMPLE / "provenance.jsonld").read_bytes()
    bad = []
    if result != committed:
        bad.append("summary.json differs from what the exporter writes")
    if not same_jsonld:
        bad.append("provenance.jsonld differs from what the exporter writes")
    for key in ("every_attempt_traced", "full_stage_chain_found", "negative_control_finds_no_one"):
        if not result.get(key):
            bad.append(f"{key} is not true")
    print("PASS: the example is what the exporter writes, and the three queries answer as stated." if not bad else
          "FAIL: " + "; ".join(bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
