# Migration config

This file's presence is the declaration: **this repository ports behavior from
another codebase.** It turns on three-way judgment (policy ↔ original ↔ new)
and lets the scribe fetch what the original actually does. Delete it and the
project is greenfield again.

Machine-local checkout paths never belong here — they differ per machine and
would be wrong for everyone else. They live in
`~/.claude/specseal/parity-paths.md`, keyed by this repo's origin remote URL.

| Field | Value |
|---|---|
| Original repo | `<org/repo>`, module `<path within it, or "whole repo">` |
| Baseline commit | `<SHA>` — the commit the evidence ledger's coordinates refer to |
| Policy root | `docs/policies/` |
| Coordinate-trust exceptions | none |

## Coordinate-trust exceptions

Paths whose recorded coordinates need re-verification before they can be
trusted, and why. Empty is the normal state — rows arrive when someone finds a
coordinate that moved without the ledger noticing.

| Path | Why it needs re-verification | Noticed |
|---|---|---|
| | | |

## Scope notes

What this migration does and does not cover, when that is not obvious from the
original repo alone. For example: endpoints being ported in a later phase, or
behavior deliberately left behind with the decision recorded in `docs/policies/`.
