"""Create a public, request-metadata-free view of the original ledger.

The raw controlled-initial run is intentionally not copied into the public
package because it contains provider request IDs and per-request metadata.
This tool retains the logical cell, round, prices, rewards and settlement
welfare needed to reproduce descriptive state/transition summaries.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List


def sanitize_event(event: Dict[str, Any]) -> Dict[str, Any]:
    keep = {"round", "source", "prices", "rewards", "total_welfare"}
    result = {k: event[k] for k in keep if k in event}
    # Keep prices as values plus public observation tags, but never request
    # metadata or model-call records.
    if "prices" in result:
        result["prices"] = {
            seller: {
                k: v for k, v in details.items()
                if k in {"price", "policy_tag", "prompt_variant", "observation_mode"}
            }
            for seller, details in result["prices"].items()
        }
    return result


def sanitize(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    cells = []
    for row in rows:
        cells.append({
            "block": row["block"],
            "cell": row["cell"],
            "status": row["status"],
            "events": [sanitize_event(e) for e in row.get("events", [])],
        })
    return {
        "schema": "controlled-initial-cells-public-v1",
        "source_scope": "original controlled-initial history run",
        "request_metadata_included": False,
        "cells": cells,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    rows = json.loads(args.input.read_text(encoding="utf-8"))
    result = sanitize(rows)
    blob = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if "request_id" in blob or "model_calls" in blob or "api_key" in blob.lower():
        raise SystemExit("sanitization failure: request metadata remains")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(blob, encoding="utf-8")
    print(json.dumps({"cells": len(result["cells"]), "bytes": len(blob.encode("utf-8"))}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
