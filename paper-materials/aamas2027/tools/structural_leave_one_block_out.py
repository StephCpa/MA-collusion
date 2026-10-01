"""Leave-one-block-out sensitivity for the registered structural primary."""
from __future__ import annotations

import json
import statistics
from pathlib import Path

import candidate_a_structural as ca


def main() -> int:
    T = ca.load()
    blocks = []
    for b in ca.BLOCKS:
        vals = []
        for init in ("LH", "HL"):
            n = T[(init, "natural", b)]
            h = T[(init, "hide_rival", b)]
            if not (ca.completed(n) and ca.completed(h)):
                vals = []
                break
            vals.append(ca.window_mean(n, ca.eq) - ca.window_mean(h, ca.eq))
        if vals:
            blocks.append((b, statistics.mean(vals)))
    xs = [x for _, x in blocks]
    loo = [statistics.mean(xs[:i] + xs[i + 1:]) for i in range(len(xs))]
    result = {
        "complete_blocks": len(xs),
        "full_mean": statistics.mean(xs),
        "leave_one_out_min": min(loo),
        "leave_one_out_max": max(loo),
        "leave_one_out_all_positive": all(x > 0 for x in loo),
        "most_influential_block": blocks[loo.index(min(loo))][0],
        "least_influential_block": blocks[loo.index(max(loo))][0],
        "interpretation": "Descriptive sensitivity check; it does not replace the registered block-t interval or completion range.",
    }
    print(json.dumps(result, indent=2))
    return 0 if result["leave_one_out_all_positive"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
