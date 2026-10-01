"""Validate the machine-readable claim--evidence matrix without inference."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ALLOWED_STATUS = {
    "supported",
    "supported_as_descriptive",
    "supported_boundary",
    "partially_supported",
    "unclear",
}
REQUIRED_FIELDS = {"id", "claim", "evidence", "result", "status", "boundary"}


def validate(root: Path, matrix_path: Path) -> dict:
    payload = json.loads(matrix_path.read_text(encoding="utf-8"))
    claims = payload.get("claims")
    if not isinstance(claims, list) or not claims:
        raise ValueError("claims must be a non-empty list")

    ids: list[str] = []
    missing_fields: list[dict] = []
    missing_paths: list[dict] = []
    invalid_status: list[dict] = []
    for claim in claims:
        if not isinstance(claim, dict):
            raise ValueError("every claim must be an object")
        claim_id = str(claim.get("id", "<missing-id>"))
        ids.append(claim_id)
        missing = sorted(REQUIRED_FIELDS - set(claim))
        if missing:
            missing_fields.append({"id": claim_id, "fields": missing})
        if claim.get("status") not in ALLOWED_STATUS:
            invalid_status.append({"id": claim_id, "status": claim.get("status")})
        evidence = claim.get("evidence", [])
        if not isinstance(evidence, list) or not evidence:
            missing_paths.append({"id": claim_id, "path": "<empty evidence list>"})
        else:
            for rel in evidence:
                path = root / str(rel)
                if not path.exists():
                    missing_paths.append({"id": claim_id, "path": str(rel)})

    duplicate_ids = sorted({item for item in ids if ids.count(item) > 1})
    if missing_fields or missing_paths or invalid_status or duplicate_ids:
        raise ValueError(
            json.dumps(
                {
                    "missing_fields": missing_fields,
                    "missing_evidence_paths": missing_paths,
                    "invalid_status": invalid_status,
                    "duplicate_ids": duplicate_ids,
                },
                indent=2,
            )
        )
    return {"passed": True, "claims": len(claims), "ids": ids}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument(
        "--matrix",
        type=Path,
        default=Path(__file__).resolve().parents[1]
        / "analysis"
        / "claim-evidence-matrix-20261002.json",
    )
    args = parser.parse_args()
    print(json.dumps(validate(args.root, args.matrix), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
