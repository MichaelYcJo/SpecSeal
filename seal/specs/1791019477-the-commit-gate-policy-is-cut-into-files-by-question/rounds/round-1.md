# 1791019477-the-commit-gate-policy-is-cut-into-files-by-question — review round 1

| Field | Value |
|---|---|
| Target SHA | e2f5270f20439ae9ec18b63fcad2fdefc0045ef7 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | 744 |
| Broad gate | not yet |
| Fixes checked by | round-2 |
| Fix range | `8410e123f4465cebf3b209c0bba304debe9b63a3..35a6d822e4539c5a9c7d6ff52154f6ddaa2e70c3`, 3 commits |
| Contract changes | none |
| New units | none |
| Needs a fix | yes — 🟡 1, the record layout's F1 says the `Over the ceiling` row goes away while the row stays at `none`. |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 1 targets `e2f5270f`, over the build's diff `2b1dcb1f..e2f5270f`. It was asked to check #727 against `spec.md` D1–D11, K1–K7 and S1–S10 and the approved plan, then quality. Because this is a move, it was asked to look hardest at what could break silently:
- whether the move is byte for byte;
- whether every reader of the old text still finds it (fold markers, pinned sentences, `REVIEW_CHAIN_DOCS`, every `§*…*` citation), re-derived by grep;
- whether each heading named outside `docs/` points at its new file;
- the ledger's two `Corrected ·` rows and 13 `Re-read ·` rows;
- whether `Over the ceiling` at `none` still runs the ceiling check;
- the record layout's D9.
The 9 rows #742 re-stamps were named as expected.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | the record layout's F1, marked built, still says the `Over the ceiling` row goes away; the row stays and reads `none` (D8), and the next split reading this policy turns half of `fold-check` off | `docs/the-record-layout.md:177` | **fixed** `ac858e6c` | fixed at ac858e6c; read: `seal/config.md` row `Over the ceiling` is `none`; `docs/the-evidence-ledger.md:305-309` says the entry went; D8 says why an absent row is a different state |
| ⬜ 2 | ledger row C1 says seven base lines changed and each now cites a file and section; base 153 differs too (re-wrapped), and 91, 199, 273, 274 name no section | `seal/ledger/1791019477-the-commit-gate-policy-is-cut-into-files-by-question.md` (C1) | answered | corrected at `e92f01c3`; executed: the S1 probe found base 153 changed beside 152; read: the seven lines as they stand. A record, so a correction |
| ⬜ 3 | three re-pointed locators cite the parent by path alone, not D5's file-and-section shape, and no divergence row records it | `docs/the-commit-gate-inside-git.md:176` | answered | corrected at `35a6d822`; read: lines 176, 251, 252 against D5 and line 128; `overview.md` has no row for it. Behaviour and facts are right |
| 🟢 | the moved spans equal the base except the three preambles, base 91, 152–153, 199, 273, 274, 283, 284 | `docs/the-commit-gate-inside-git.md`, `docs/the-review-and-parity-arms.md`, `docs/commit-review-gate-spec.md` | confirmed | executed: `difflib` probe against `git show 2b1dcb1f:docs/commit-review-gate-spec.md` |
| 🟢 | no other positional or italic reference crosses the cut | the three files | confirmed | executed: a wider word list over the base by part, and an italic-to-heading and italic-to-bold probe across the three files |
| 🟢 | every `§*…*` citation of a heading in the three files names the file holding it, in docs, hooks, skills, READMEs and tests | live tree | confirmed | executed: resolver probe, 21 citations, 17 resolved, 4 are worktree-guard's own heading; `git grep` of the moved headings' words |
| 🟢 | the ceiling check still runs with `Over the ceiling` at `none` | `skills/settle/scripts/fold_check.py#ceiling_problems` | confirmed | executed: an arms file padded past 1,000 lines fails `fold-check` with exit 1; the real tree exits 0 |
| 🟢 | the 9 DRIFTED rows reach 0 once the integration chore is merged | `seal/ledger/`, `seal/releases/` | confirmed | executed: `evidence-check --strict` exit 2 at e2f5270f (9 drifted, 4 refused), exit 0 after merging 5463fd82 (0, 0) |
| 🟢 | G17 and the two opt-in headings carry every coordinate; the 13 `Re-read ·` rows hold against their edits; P11 is re-stamped in place; no released file changed | `seal/ledger/1791019477-the-commit-gate-policy-is-cut-into-files-by-question.md` | confirmed | read: each row against the released row and the diff; executed: `evidence-check`, `correction-check` |
| 🟢 | the record layout marks F1 built, drops the gate from the over-target list, adds both files to its table and states 586, 254, 250 | `docs/the-record-layout.md` | confirmed | read against `wc -l` at the target; the one stale sentence is finding 1 |

## Paste-ready fixes

```
Each part answers one question — what git decides, what the text reading
decides, what each arm wants. Built, the parent is 586 lines, the commit gate
inside git 254 and the arms 250, each under the ceiling of 1,000. Fold markers
went across whole, and the `Over the ceiling` entry went with the cut in the
same change. The row stays and reads `none`, so `fold-check` still holds every
document to the ceiling (`docs/the-evidence-ledger.md` §*The fold, and what
tells it from a deletion*).
```
```
| `seal/specs/1790993138-every-record-has-one-home-and-a-released-ledger-file-never-changes/spec.md` | The `Over the ceiling` row goes away in the same change | work item 1790993138's frame, recording F1 as #715 decided it; #727 kept the row at `none` (D8) and corrected the present-tense statement in `docs/the-record-layout.md`, and `spec.md` §*Scope* leaves every other work item's records untouched |
```
```
The moved text is the base's, byte for byte, but for the seven lines that pointed across the cut by position, which now name the file that holds what they pointed at (152 and 283–284 name its section too), and base line 153, re-wrapped beside 152 with no word changed
```
```
the three preambles and base lines 91, 152, 153 (re-wrapped, same words), 199, 273, 274, 283 and 284
```
```
| D5's citation shape | Spec D5: "A positional reference that crosses the cut becomes a citation by file and section". Base 91, 199, 273 and 274 name the file alone; 152 and 283–284 name file and section | the file alone for those four | 91 means the whole arms file. 199, 273 and 274 say *the PreToolUse reading*, which is what the parent chiefly holds, and 199 sits inside the unit G17 anchors, so a section there would move G17's re-pointed hash again |
```

## Executed probes

| What was run | Result |
|---|---|
| S1 probe (a scratch file, run once, deleted): `difflib` of each moved span and the parent against the base | only the three preambles and base 91, 152, 153, 199, 273, 274, 283, 284 differ; 153 is a re-wrap |
| base lines by part, grepped for a wider set of positional words | crossing: 152, 283 and the K6 lines; nothing new |
| italic references across the three files, against headings and bold statement openings | none crosses |
| citation resolver over the live tree | 21 citations of a heading in the three files; 17 resolve to the holder; 4 are `docs/worktree-guard-spec.md` §*Known limits* |
| `bin/evidence-check --strict .` at e2f5270f | exit 2: the 9 named DRIFTED rows, 4 NOT-IN-TREE refusals in 1790993137's records, nothing BROKEN |
| the same after merging 5463fd82 into the clone | exit 0: 0 drifted, 0 refused |
| `bin/correction-check --range 2b1dcb1f...HEAD`, before and after the merge | exit 0 both; no released ledger file changed |
| `bin/fold-check --root .` | exit 0: 157 statements, 18 documents, 0 listed over the ceiling |
| `bin/fold-check --root .` with the arms file padded to 1,450 lines | exit 1, the arms file named over the ceiling of 1000; file restored |
| `bin/survivor-check --range 2b1dcb1f...HEAD` | exit 1, one place (1790815613's overview line 49); with `--exempt` this item's `survivors.md`, exit 0 |
| `python3 .github/scripts/rider_check.py --root .` | 20 ok, 0 drifted, 0 broken |
| `bin/test -q` over 14 modules: hooks hardening, the direct answer, the reopening, the waiver, release hygiene, a gate that fails, the handoff, line wrap, fold room, one word, ledger rules, changelog, no real identifiers, one owner | 462 passed, 1 skipped |
| `bin/test -q` over the other four `REVIEW_CHAIN_DOCS` consumers and the agent contract module | 306 passed |
| the broad gate: full suite, repository-wide lint, typecheck | not yet — the sealer's, once, after the rounds settle; nothing in this round ran it |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
