"""Verify the anonymous supplement ZIP manifest and public metadata policy."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path

FORBIDDEN_KEYS = re.compile(r'"(?:request_id|request_ids|logical_request_id|logical_request_ids|system_fingerprint|system_fingerprints)"')


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("zip_path", type=Path)
    args = ap.parse_args()
    with zipfile.ZipFile(args.zip_path) as zf:
        manifest = json.loads(zf.read("package-manifest.json"))
        rows = manifest["files"]
        bad = []
        for row in rows:
            data = zf.read(row["path"])
            if len(data) != row["bytes"] or hashlib.sha256(data).hexdigest() != row["sha256"]:
                bad.append(row["path"])
        metadata_hits = []
        for name in zf.namelist():
            if name.endswith((".json", ".md", ".txt", ".csv")):
                text = zf.read(name).decode("utf-8", errors="replace")
                if FORBIDDEN_KEYS.search(text):
                    metadata_hits.append(name)
        result = {
            "passed": not bad and not metadata_hits,
            "archive_entries": len(zf.namelist()),
            "manifest_files": len(rows),
            "bad_hashes": bad,
            "metadata_key_hits": metadata_hits,
        }
        print(json.dumps(result, indent=2))
        return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
