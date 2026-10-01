"""Remove provider/request identifiers from the public four-arm ledger.

The analysis only needs prices, outcomes, statuses, and aggregate usage fields
to reproduce the offline checks.  Provider request IDs, logical request IDs,
and system fingerprints are operational metadata and are not part of the
scientific record, so they are omitted from the public copy.
"""
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path


DROP = {"request_id", "logical_request_id", "system_fingerprint"}


def sanitize(value):
    if isinstance(value, dict):
        return {k: sanitize(v) for k, v in value.items() if k not in DROP}
    if isinstance(value, list):
        return [sanitize(v) for v in value]
    return value


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("input", type=Path)
    ap.add_argument("output", type=Path)
    args = ap.parse_args()
    obj = json.loads(args.input.read_text(encoding="utf-8"))
    out = sanitize(copy.deepcopy(obj))
    text = json.dumps(out, ensure_ascii=False, indent=2) + "\n"
    args.output.write_text(text, encoding="utf-8")
    if any(k in text for k in DROP):
        raise SystemExit("sanitization failed: provider identifiers remain")
    print(json.dumps({"output": str(args.output), "bytes": len(text.encode("utf-8")), "dropped_keys": sorted(DROP)}))


if __name__ == "__main__":
    main()
