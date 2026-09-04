# 1788472135-the-run-outlives-its-last-finding — review round 2

| Field | Value |
|---|---|
| Target SHA | 4adbb86 |
| PR | not yet opened |
| Broad gate | not yet |
| Fixes checked by | round-3 |
| Contract changes | `says_none` now answers False for any cell carrying a parenthesised depth marker, so a cell that used to mean *no units* can reach the entry walk → `fix_surface`, both its `Contract changes` arm and its `New units` arm |
| New units | `SPLIT_LIMIT` (depth 1); `_module` (depth 1); `_real_records` (depth 1) |
| Needs a fix | yes — 🔴 1 `round-1.md`'s own `Contract changes` cell fails the checker this branch strengthened, and CI runs that command on every pull request; 🟡 2 a constant named `NONE` reads as *no units*; 🟡 3 an empty `Needs a fix` cell prints empty backticks |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

**The verifying round.** Target was the diff of round 1's fixes — `git diff
02ec260..4adbb86` — and not the branch, which is what keeps it the cheapest
round of the run. Job: for each of round 1's nine verdicts, is it actually
closed.

Two rules were stated rather than assumed, because round 1 broke one of them.
`agent-contract` §6 — spawn no agent, and do not change what branch the shared
working tree is on: round 1's reviewer spawned two general-purpose subagents,
one of them ran `git checkout main` in the shared tree, and its proof block
then said the tree was never written to. §2 — the full suite, repository-wide
lint and typecheck are the orchestrator's.

The runner was handed over in full, exit codes to be read directly rather than
through a pipe, which is a mistake this session had already made once.

Six units named by `round-1.md`'s `New units` were named as the finding
surface, exempt from *answers, not new findings*. Five specific things were
named to try to break, in order: `run_reopened`'s unreadable-cell arm, the
count that stops at a reopening round, `NEEDS_FROM` against the other three
cutoffs, `depth_problems`' fourth arm, and `says_none` accepting `;`.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | `round-1.md`'s `Contract changes` cell is refused by `fix_surface`. It describes `says_none` accepting a trailing `;` and writes the character literally in a code span; both fix-surface rows split on `;` before looking at code spans, so the entry recording that very change was cut in half and refused for having no reach | `rounds/round-1.md:9` | fixed at `1a4ba52` | Executed by the reviewer in two trees and reproduced by the orchestrator: `chain_check.py --baseline main` → exit 1, and the line names the truncated entry. `.github/workflows/hygiene.yml:147` runs the same command on every pull request, so the branch would have opened red. The reviewer confirmed it is an error rather than a notice two ways — the arrow walk's `errors.append` has no `excused` arm, and a probe commit spelling the character as a word removed exactly that line |
| 🟡 2 | `says_none` reads `` `NONE` (depth 1) `` as *no units*. `EMPHASIS` strips the backticks, `.lower()` the case, and the following space is in `SEPARATORS`, so it parses as `none` with a reason and the depth walk is never reached | `chain_check.py:1459` | open | Executed: `says_none("`NONE` (depth 1)")` → `True`. `plan.md:132` declares the failure direction *blocks more*; this path permits more. The reviewer's guard — refuse `says_none` when `DEPTH_RE` matches — was applied in a clone and 98 cases stayed green |
| 🟡 3 | An empty `Needs a fix` cell prints ``is ``, which is neither answer``. The floor row two functions away gives an empty cell its own sentence, so two rows reading the same vocabulary answer the same state at different quality | `chain_check.py:1799` | open | Executed. `agent-contract` §14 is the clause — a line a person reads and acts on |
| 🟢 4 | Round 1's 🔴 1, the wall | `chain_check.py:1815-1827` | pass | Four sequences executed. A `no` record followed by a reopening round and the round that closes it → exit 0; three quiet rounds → exit 1, still refused, which is #81's shape; a reopening round followed by two quiet ones → exit 1 with the message on the reopening round, so a reopening does not absolve what precedes it and carries its own bound |
| 🟢 5 | Round 1's 🔴 2, the protocol | `docs/review-handoff-protocol.md` | pass | Field-table row, the depth and `;` on `New units`, the grandfathering sentence split, a `Loses a record or crashes` subsection, a 1.0 entry in the drafts log, and the title moved. Round 1's own `grep -c` returned 0 and now returns a value |
| 🟢 6 | Round 1's 🔴 3, `--strict` | `seal/ledger.md` | pass, partly — by agreement | `--strict` → exit 2, `476 ok · 1 drifted`, where round 1 measured 2. `:543` is closed; the remaining row is S8, which round 1 deferred to the repository owner with a name on it. Not this round's to reopen |
| 🟢 7 | Round 1's 🟡 4, 5, 7, 8 | four files | pass | Each re-executed: five hostile depth inputs all caught, a no-prefix work item gets four notices and exit 0, the three subsection pins cut sections rather than the file, the docstring names the floor table and the depth |
| 🟢 8 | Round 1's 🟡 6, the `none;` half | `chain_check.py:1459` | pass | `none;`, `none ;`, `none;;` → `True`; `none; unit (depth 1)` → `False`, correctly. The other half of that finding is 🟡 2 above |
| 🟡 9 | `COMMA_LIMIT`'s recorded sentence is narrower than what the code refuses. It names a comma inside a unit NAME; a comma inside a reason is caught too | `chain_check.py` | open — deferred | The refusal is right; the record of its limit is not. Rides the same fix pass as 🟡 2 |
| ❓ 10 | A `yes` with no reason in `Needs a fix` passes, and silently lengthens the floor's count by one round. Ledger F8 grounds the permissiveness on the verdict table being the reason, and does not reach this consequence | `chain_check.py` | out of scope | The repository owner |

## Executed probes

| What was run | Result |
|---|---|
| `chain_check.py --baseline main`, orchestrator's tree | exit 1 — 🔴 1 reproduced, read directly rather than grepped |
| the same after `1a4ba52` | the `Contract changes` line is gone |
| reviewer: `.venv/bin/pytest` × 5 files at `4adbb86` in a clone | 180 passed |
| reviewer: probe commit spelling `;` as a word | only that line disappears — error, not notice |
| reviewer: four floor sequences | exit 0 / 1 / 1, message placement as described in 🟢 4 |
| reviewer: 32 probes over depth, `none`, the four cutoffs | in the verdict grounds above |
| reviewer: the `says_none` guard applied in a clone | 98 passed — the proposed fix breaks no existing pin |
| `evidence_check.py --strict .` | exit 2, `476 ok · 1 drifted` (S8) |
| `fold_ledger.py --version 0.8.0 --dry-run` · `bin/unverified-check` | exit 0 · exit 0 |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round 1 | `chain_check.py:1690` — the `;` split in `fix_surface` | It produced 🔴 1 of this round, and the class is not closed: `New units` splits the same way and no document records the separator's own limit |
| round 1 | `seal/ledger.md` S8 | Still drifted, still the owner's, and `evidence-check --reverify` takes no row selector — one run on this tree re-stamps a false claim |
| round 1 | `agents/warden.md` §6 | Round 1's reviewer broke it. Round 2's prompt stated it and round 2 kept it: it worked in a `git clone --no-local` and left this tree untouched |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| S8's claim, and that `--reverify` cannot be narrowed to a row so running it here silently re-stamps a false claim | `overview.md` §Not verified, with the warning sentence the reviewer drafted | the repository owner |
| A `yes` with no reason lengthening the floor's count (❓ 10) | an issue, once this branch merges | the repository owner |
| Three `seal/ledger.md` rows carry 2026-09-04 hashes with older `Checked` dates. No claim went false; the date alignment is a judgment | `overview.md` §Not verified | the repository owner |
| That the reviewer of round 1 spawned agents and switched the shared tree, against `agent-contract` §6 | an issue of its own | the repository owner |
