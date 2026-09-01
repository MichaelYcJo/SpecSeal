# Questions — every branch appends to the same two files

Three decisions were settled by the repository owner in the routing batch and
are not re-opened here: the changelog is fragmented and gathered at release,
the ledger is fragmented and never gathered, and a ledger row stops carrying a
`Checked` SHA. What follows arrived during implementation.

## Q1 — a row stale on arrival — ANSWERED, by removing the cause

**Two branches, one cited file.** Branch A writes a row citing `code.py`;
branch B changes that code and squashes first; A squashes second. Every
time-window scheme misses it, because there is no interval in which the code
changed relative to A's row — A's row was born after B's change landed.

A content hash has no window to look at. It compares what the row recorded
against what is there, and the two differ on the first run. **Executed**: the
fixture builds exactly that merge order and the row reports `DRIFTED`, exit 1.

This was recorded as unreachable and marked for issue #31. It closes here as a
side effect of the coordinate naming content, which is the honest description —
nothing was built for it.

## Q2 — a SHA in a fragment's prose header — ANSWERED, by removing the cause

There is no header baseline for a prose SHA to be mistaken for. A ledger row
carries its own anchor and hash, so a fragment declares nothing at its head and
`find_baseline` no longer exists.

The narrower fixes that shipped for this in review round 2 — a two-pass header
scan, a bound on accidental prose — went with it.
