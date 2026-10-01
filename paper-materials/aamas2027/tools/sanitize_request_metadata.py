"""Strip provider/request identifiers from a JSON artifact for public release."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

DROP = {
    "request_id", "request_ids", "logical_request_id", "logical_request_ids",
    "system_fingerprint", "system_fingerprints",
}


def clean(value):
    if isinstance(value, dict):
        return {k: clean(v) for k, v in value.items() if k not in DROP}
    if isinstance(value, list):
        return [clean(v) for v in value]
    return value


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input", type=Path)
    ap.add_argument("output", type=Path)
    args = ap.parse_args()
    out = clean(json.loads(args.input.read_text(encoding="utf-8")))
    text = json.dumps(out, ensure_ascii=False, indent=2) + "\n"
    args.output.write_text(text, encoding="utf-8")
    if any(k in text for k in DROP):
        raise SystemExit("provider identifiers remain")
    print(json.dumps({"output": str(args.output), "bytes": len(text.encode("utf-8"))}))


if __name__ == "__main__":
    main()
