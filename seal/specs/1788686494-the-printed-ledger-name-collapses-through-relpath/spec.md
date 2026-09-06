# Feature Specification: the printed ledger name is the file that was read

<!-- seal/specs/1788686494-the-printed-ledger-name-collapses-through-relpath/spec.md -->

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CLAUDE.md` § *The goal a design is chosen against* | The name a person reads is what they open next; a wrong one costs an unattended run a human round trip |
| `skills/agent-contract/SKILL.md` §12 (enumerate the class) | The fix is one helper and every site in the class, not the four sites the issue happened to list |
| `skills/code-review/SKILL.md` § *A document claim gets a pin* | The docstring saying why `relpath` cannot be used for a display name is pinned by a case |

## Scope

**In.** Every place `evidence_check.py` turns a **ledger path** into a name a
person reads. One display helper, its docstring, every such site through it,
and a case that pins the printed header against the file actually read.

**Out.**
- Which file a pattern names. `resolve_patterns` already settles that by inode
  and returns the pattern's own spelling (#153 round 13); this work changes
  nothing about what is opened, only about what is printed.
- The exit code and the rows. Both are already right — the issue says so.
- Any path that is not a ledger. The scan-suggestion site at
  `evidence_check.py:627` prints a repo-relative path of a *scanned source
  file*, built by `os.walk` under `repo`, so it carries no `..` to collapse.
  It is judged and named here rather than left silent, and the judgement is
  the phase-2 record's to write down.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| The header names the file that was read | Given `x/lnk -> y` and a BROKEN row in `<root>/ledger.md`; when `evidence_check.py --ledger 'x/lnk/../ledger.md' .` runs on POSIX; then the printed header names the file the pattern named, never `x/ledger.md` | The integration case in `tests/test_a_narrowed_ledger_read_says_what_it_skipped.py`, POSIX branch, seen red against `relpath` first |
| The display helper collapses nothing | Given a path holding `..`; when the helper renders it; then no segment is folded away | Unit cases on the helper, seen red against `os.path.relpath` |
| An ordinary name is unchanged | Given `./seal/ledger.md` under root `.`; when the helper renders it; then it reads `seal/ledger.md` as it does today | Unit case, and the suite's existing output assertions staying green |
| Every site in the class goes through it | Given the property *a ledger path rendered for a person*; when the class is enumerated by that property rather than by a list; then no site is left calling `relpath` on a ledger | A case that reads the source and refuses a `relpath` on a ledger path |
| The reason survives the next editor | Given the helper; when it is read; then its docstring says why `relpath` cannot be used for a name | The source-reading case above pins the helper's existence; the docstring is its grounds |

## Data & interfaces

One new top-level unit in `skills/evidence-check/scripts/evidence_check.py`.
No CLI change, no exit-code change, no ledger-format change.

## Open questions → questions.md

None blocking. The one judgement call — what the helper renders when the path
does not sit under the root — is settled in `plan.md`'s Alternatives.
