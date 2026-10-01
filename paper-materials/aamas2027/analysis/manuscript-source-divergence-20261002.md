# Manuscript source divergence audit — 2026-10-02

Two manuscript copies exist in the broader workspace. They are not byte
identical and must not be merged implicitly.

| copy | SHA-256 | bytes | role |
|---|---|---:|---|
| `papers/aamas2027/history-display-observability.tex` | `E546DA418BE8A413E8821971A9C32D880D82EE045DB3C97D0BC4AA6B393B4CF2` | 41,101 | older standalone workspace draft |
| `github-upload/github-upload-submission/paper-materials/aamas2027/latex/history-display-observability.tex` | `456895AA68C21B2FE788E11D52CB06E0210071D4E67B6DDCA8639412ADE6A72C` | 42,583 | canonical submission staging source |

The candidate source is canonical because it is the source compiled into the
8-page staging PDF, carries the current replication and bounded-claim text,
and is tracked on branch `submission-candidate-20261002`. The older standalone
copy predates the candidate package and should only be consulted through an
explicit line-by-line review.
