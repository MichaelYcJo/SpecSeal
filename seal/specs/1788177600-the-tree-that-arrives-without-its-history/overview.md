# 1788177600-the-tree-that-arrives-without-its-history — overview

📋 implement applied
· spec:     `docs/branch-and-release.md`, `skills/implement/SKILL.md` (document layout)
· evidence: `.specseal/map.md` — baseline established, three rows opened
· verified: the suite was executed; the ledger rows below were read, not run

## Why this work exists

The plugin was built in a different repository and arrives here as one commit,
so that nothing in this tree points at a history it cannot reach. Every rule
written from an incident still cites one — the incidents were re-filed as
issues here so the citation resolves — and the prose that named a commit or a
pull request by number now names what happened instead.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| A round-record count pinned to 25 | `tests/test_handoff_outlives_the_merge.py` required 25 nested records, guarding a move that had already happened | Dropped the bound, kept `assert not flat` | The number was a fact about one migration, not a rule; this tree carries no records, so the assert would fail on a truth. The rule it sat beside still holds |
| Rider stamps naming unreachable commits | Eleven `# RIDER:` comments carried SHAs from the other repository | Re-stamped against this tree's first commit | `tests/test_a_rider_reaches_its_file.py:153` requires an ancestor of HEAD, and a stamp nobody can resolve is not a stamp |

## Not verified

| Item | Who must answer |
|---|---|
| whether the hooks fire on Windows from this tree | a maintainer with a Windows machine |
| the conformance evals | `claude plugin eval` is early access; the suite awaits enablement |

## Not done

The compatibility paths that read a `_ai/` home and a `.specseal/handoff/`
record directory are kept. They exist for repositories that adopted the plugin
earlier, and this tree starting at 0.0.1 does not change what those
repositories hold. Removing them is a decision about who is still supported,
which is not this work item's to make.

## Fed back into the spec

none.
