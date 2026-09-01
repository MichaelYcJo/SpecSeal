# 1788229400-every-branch-appends-to-the-same-two-files — review round 4

The first review of the redesign span. Everything after round 3's target was
built under an explicit owner waiver with executed proof in place of review;
the owner then ordered this round, so the waiver is spent.

| Field | Value |
|---|---|
| Target SHA | `76e61a402f26cb2b21f95e00ac716c3d111ae779` (opened at `9eadcba`, widened mid-round) |
| Diff base | `0d2a73b` — round 3's target |
| PR | not yet |
| Broad gate | not yet — slices only this round; the windows leg answers the one ❓ |
| Fixes checked by | `round-5` |
| Needs a fix | yes — four 🔴 and ten 🟡, all closed at `38802bc` |

- [ ] Pass

## How the findings relate

```
① the generic unit rule reads a USE as a DECLARATION
     ├─ a brace-language `return f(x)` makes an ambiguous BROKEN     [1] 🔴
     └─ .py falls back to that rule when a symbol is gone, and
        --reverify anchors the row to a leftover call site           [2] 🔴
② green lights where none belong (the #28 lens)
     ├─ deleting a directory turns its rows EXTERNAL, exit 0         [3] 🔴
     ├─ a second row at the same coordinate is never checked         [5] 🟡
     └─ OLD-FORMAT is absent from the totals line and the advisory   [6] 🟡
③ --reverify writes where it should not
     ├─ --default-repo is dead, and cross-repo rows are re-anchored
        by scanning the WRONG repository                             [4] 🔴
     ├─ a deleted unit's boilerplate twin "proves" a rename          [7] 🟡
     └─ a heading-path locator can never receive the rename hint     [8] 🟡
④ --migrate's limits, now fired automatically at session start
     ├─ --map / --default-repo silently ignored                      [9] 🟡
     └─ a stale line number is trusted against the current tree     [10] 🟡
⑤ documents that disagree with the code                        [11-13] 🟡
⑥ the session-start hook: judged sound, two small fixes        [14] 🟡 · ❓
```

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | The generic declaration rule accepts statement keywords in `pre`, so `return render(y);` reads as a second declaration of `render` and an ordinary one-declaration-one-call file is `BROKEN locator is ambiguous`, exit 2. Non-Python projects — the rule's whole audience — hit this on their commonest shape | `evidence_check.py:274` | **fixed** `38802bc` | Reviewer-executed on a JS fixture; orchestrator confirmed by reading the regex — `pre` is `[\w\s*&]*?`, and only the `:` delimiter carries a stricter pre check. The existing pin at `tests/test_a_row_points_by_content.py:393` covers `const r = handler(1);` (an `=` in pre) and not this |
| 🔴 2 | `.py` falls back to the generic rule whenever `ast` finds no symbol — including when the parse SUCCEEDED and the unit is simply gone. A function moved to another module with a call left behind reads DRIFTED instead of BROKEN-with-hint, and `--reverify` rewrites the hash to the call site: the ledger is permanently anchored to a call, and the true heal (the scan finding the moved unit) can never run | `evidence_check.py:236-240` | **fixed** `38802bc` | Reviewer-executed end-to-end: move `helper` to `lib.py`, leave `    helper(x)` — check says `DRIFTED content changed at 5-5`, `--reverify` rewrites, recheck `1 ok`. Fix shape: fall back only on `SyntaxError` |
| 🔴 3 | Deleting or renaming a top-level directory turns every row citing it EXTERNAL — "not in this repo; pass --map/--default-repo" — and `--strict` exits 0. The message is false and CI is green. `--reverify` heals the same row happily, so the two commands disagree about one row, which is the proof the guard is drawn wrong | `evidence_check.py:545-552` | **fixed** `38802bc` | Reviewer-executed: `pkg/` → `lib/`, check green, reverify heals. The `:544` comment's own claim — a deleted file must fail the build — collapses at directory granularity |
| 🔴 4 | `reverify()` takes `default_repo` and never reads it. A migration ledger's drifted rows cannot be re-verified (`0 rows re-verified`, silently), and worse: the row's file is absent from root, so the graded scan searches THIS repository and re-anchored a cross-repo row onto a local unit whose content happened to reconstruct | `evidence_check.py:749` | **fixed** `38802bc` | Orchestrator confirmed the dead parameter by grep; reviewer executed both halves, including `src/api.py#fetch → copycat.py#grab (content moved intact)` against the wrong repo |
| 🟡 5 | The dedup key is the coordinate without the hash, so a second row citing the same unit at a different time — one of the two is necessarily stale — is silently skipped. Two-row fixture reads `1 ok`, exit 0 | `evidence_check.py:521-523` | **fixed** `38802bc` | Reviewer-executed; orchestrator confirmed the key by reading. Fix is one line |
| 🟡 6 | OLD-FORMAT is missing from the totals line (a red build whose summary reads all zeros) and from the advisory's filter (`broken_rows` only), so the commit that needs the migration line most gets silence from the hook | `evidence_check.py:897,905-908` · `hooks/evidence-advisor.py:108` | **fixed** `38802bc` | The totals half was independently measured by the orchestrator during the `--migrate` demo, before this round reported it |
| 🟡 7 | The reconstruction proof cannot distinguish a rename from a deletion beside a boilerplate twin: deleting `class C` while `A.init_state` has an identical normalised body yields `renamed?` and `--reverify` re-points C's row at A. Realistic for `__init__`s, getters, trivial wrappers. Not in Known limits | `evidence_check.py` reconstruction path · `skills/evidence-check/SKILL.md:208-212` | **fixed** `38802bc` | Reviewer-executed. At minimum a Known-limits line; better, output wording that does not assert "moved intact" |
| 🟡 8 | A heading-PATH locator never receives the rename hint: the md reconstruction substitutes the candidate's first line with the WHOLE locator string, but the recorded hash's first line is the last part's heading alone. The parent-qualified form the skill recommends is the one that loses healing | `evidence_check.py:492` | **fixed** `38802bc` | Reviewer-executed both forms. Fix: substitute the path's last part |
| 🟡 9 | `--migrate` ignores `--map` and `--default-repo`; a legacy-parity project's ledger — first-class in this plugin — can never migrate, and OLD-FORMAT's prescription line is circular for them | `evidence_check.py:663,886-892` | **fixed** `38802bc` | Reviewer-executed: mapped file, `LEFT … file not found` |
| 🟡 10 | `--migrate` trusts the cited line numbers against the CURRENT tree; a row written when `handler` sat at 1-2 anchors to whatever sits there now, reported `1 row migrated · 0 left`. The old stamp — the one evidence that could catch this — is discarded unused. The session-start hook now fires this without a user's choice, and its stated safety ("wrong-write is visible in git diff") only helps a reader who knows the original claim | `evidence_check.py` migrate path · `hooks/ledger-migrate.py` | **fixed** `38802bc` | Reviewer-executed. Direction: with git present, check the cited range against the stamp's commit and LEAVE rows whose content changed since; at minimum, the limit stated in Known limits and the notice |
| 🟡 11 | The skill's frontmatter still sells the removed mechanism — "ranges touched since the baseline demand re-verification" | `skills/evidence-check/SKILL.md:4-5` | **fixed** `38802bc` | Read |
| 🟡 12 | Known limits' first entry contradicts the code twice: a bare filename is claimed EXTERNAL-never-guessed, but executes as BROKEN with a `moved?` hint and a successful `--reverify` re-anchor. The behavior looks right; the document is what needs the fix | `skills/evidence-check/SKILL.md:204-206` | **fixed** `38802bc` | Reviewer-executed |
| 🟡 13 | Three small doc/code mismatches: the changelog fragment's generic-rule quote omits `=`; the fragment and skill say the dirty guard covers "uncommitted `.specseal/` changes" while the code guards the three ledger globs (which is the RIGHT scope — fix the documents and the hook's message, not the code) | `changelog.md:32,59` · `SKILL.md:226` · `hooks/ledger-migrate.py:111-114,151` | **fixed** `38802bc` | Reviewer, read against code |
| 🟡 14 | The ledger write in `migrate` is truncate-then-write, so a mid-write crash leaves a torn file (recoverable only because the dirty guard guarantees a committed baseline); and a ledger `read()` returning None crashes `migrate` and `check_ledger` — swallowed under dispatch, a traceback in CI | `evidence_check.py:681,513,517` | **fixed** `38802bc` | Reviewer, read. `tempfile` + `os.replace`, and a None guard |

## The session-start hook — judged, and it stands

The four ordered attack axes, answered by the reviewer with execution or a
stated reading:

- **The ownership analogy holds, but the dirty guard is what carries it** — every write lands on a committed baseline, so a hand-edited committed row survives (only the coordinate cell is rewritten) and an uncommitted one blocks the write. Without the guard the analogy would not have stood.
- **The once-per-repo marker fails toward noise in every mismatch case** — a re-clone at the same path skips silently but keeps the loud OLD-FORMAT failure; a different path or worktree is a fresh attempt; a user who reverted the migration commit is not overwritten again, which is the right direction.
- **The dirty scope is the three ledger globs, and that is correct**; the documents claiming `.specseal/`-wide are finding 13's.
- **The crash path converges**: dying between ledgers leaves a half-migration uncommitted and no marker, and the next start's dirty guard walks the user to commit-then-continue. The within-one-file window is finding 14.
- **Cost passes**: ~24 ms per opted-in session start against a command a person must remember — the project's first goal decides that trade.

**❓ one item is outside this round's reach: `dirty()` on Windows.** `os.relpath` produces backslash paths fed to git as pathspecs; if git rejects them the hook reads permanently dirty and the migration never runs, with a wrong reason printed. The broad gate's windows leg answers it; the defensive fix is one `.replace(os.sep, "/")`.

## Also settled this round

- Round 3's deferred 🟡 E (the template's `--strict` advice) was closed by this span's template rewrite — verified. 🟡 C was superseded by the redesign; its live successors are findings 4 and 9, inherited here rather than reopened.
- The attack-6 answer: the states `UNMEASURED` and `AMBIGUOUS` used to name became inexpressible rather than silent — no stamps are read and no baseline exists. The quiet spots this span did create are findings 3, 5 and 6, all listed.
- Not judged: `README.ko.md`, individual rows of `.specseal/map.md` (the checker's `49 ok` stands in), and the 14 delta lines of `templates/sdd-plan.md` · `templates/specseal-README.md` — a five-minute check for round 5.

## Executed probes

Thirteen scenario probes (S1-S13b), three targeted mutations proving the pins
for the reconstruction and grade-order paths discriminate (2/1/2 cases killed
exactly), the dispatch end-to-end for the session-start hook under an isolated
HOME, slices of 56 + 22 tests, ruff clean, and the real ledgers at
`49 ok · 0 drifted · 0 broken · 0 external`. The orchestrator independently
confirmed findings 1, 4 and 5 by reading the cited lines and finding 6's
totals half by execution before the round reported it. The full suite did not
run; it is the orchestrator's, once, after round 5 settles.
