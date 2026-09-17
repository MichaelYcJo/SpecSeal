# 1789598366-a-piped-broad-gate-row-takes-every-config-row-below-it — round 1 fixes

Target reviewed `028f71ad`. Fix commits `caaa4c11`, `8b3c41df`, `5d22c622`,
`7eadae72` and `1736936b`, over the range `c4e9c58b..HEAD`.

Every finding was re-executed here before anything was written: round 1's four
arrived as facts with coordinates, and each was opened rather than taken
(`agent-contract` §5). All four reproduce, and the measurement widened two of
them — the class behind 🟡 2 has a second member, and 🟡 4's second half is
worse than *repaired by nothing*.

## Fixes

| # | Verdict | Commit or grounds |
|---|---|---|
| 1 | fixed | `caaa4c11`. `hooks/config.py#refusal` answers whether the refused line is the one that ENDED the table, and the gate chooses its cost sentence from that instead of stating it flat. `skills/config/SKILL.md` and `skills/implement/orchestration.md` carry the condition, and `1736936b` reaches the two further copies the survivor check found |
| 2 | answered | Behaviour kept, claim corrected at `5d22c622` and `1736936b`. The new reading is the coherent one: once `\|` means an escaped pipe those bytes cannot also mean *backslash, then the delimiter*, and nothing becomes unwritable because a space before the closing pipe returns the same value byte for byte. `plan.md`, `questions.md` M3, `spec.md` §*What this repair cannot see* and the changelog now say so; the shape is pinned |
| 3 | fixed | `8b3c41df`. `hooks/config.py#rows_under` reports what a refused line took, so the gate asks whether its own row is among them. A file with no such row anywhere still gets the absent-row refusal, and the existing case for that file is the guard on the new branch |
| 4 | answered | Disclosure corrected at `7eadae72` and `1736936b`, and pinned. All four sites now say the second `Mode` row is closed for the escaped spelling only, and a file already two rows deep is recorded in `overview.md` §*Not done* |

**The ⬜ correction is closed by finding 1's fix**, as the report expected.
`refusal` stops at a second header or a stray separator once a row has been
found, exactly where `config_rows` breaks, so it can no longer quote a line
out of the table below this one; and the docstring now describes the
indentation rule the code has rather than the stricter one it claimed.

## The mutation behind each fix

Every one was restored from bytes the mutation script held, never from HEAD,
with `tests/__pycache__` cleared between runs. Exit codes read directly.

| Finding | Mutation | Result |
|---|---|---|
| 1 | the cost chooser wired to `True` — the sentence the build shipped | exit 1 · the first-row half red: *the refusal says they were lost* |
| 1 | the two sentences swapped | exit 1 · the second-row half red. **This is the one that matters**: a case asserting only that the conditional sentence EXISTS passes here |
| 1 | `skills/config/SKILL.md` put back to its flat sentence | exit 1 · `test_the_skill_says_how_a_value_carrying_a_pipe_is_written` |
| 1 | `skills/implement/orchestration.md` put back to its flat sentence | exit 1 · `test_a_candidate_carrying_a_pipe_is_escaped_where_candidates_are_derived` |
| 2 | `CELL` put back to `[^\|]`, the pattern that predates the escape | exit 1 · the narrowing case returns a row where it asserts none |
| 3 | the new branch made unreachable | exit 1 · the person's row is called absent again |
| 3 | the new branch widened to fire on every other-item refusal | exit 1 · the file that genuinely has no such row is sent looking for one |
| 4 | a greedy last cell, so the bare pipe parses | exit 1 · the limitation is gone and the case says which records have to change with it |

Restored after each: exit 0.

**Finding 1's case is red on the CONDITION and not on a string**, which is what
the pass was asked for. It builds both tables in one case — the piped line as
the table's second row and as its first — and asserts each gets its own
sentence, so it is red whichever way a single-answer chooser is wired.

**Finding 4's case pins a limitation, so its red direction is the limitation
being closed.** That is deliberate: the day the bare spelling is repaired, this
case goes red and its message names the records that then have to change.

## What the re-enumeration found

**🟡 2's class has a second member the report did not name.** The narrowing is
a backslash standing immediately against a cell-ending pipe — not only the
closing one. `| C:\tools\| x |` was the row `('C:\tools\', 'x')` under the old
pattern and is no row under the new, for the same cause at the pipe between
the cells. Both are in the case and in `spec.md` (`agent-contract` §12).

**Its reach in this tree is one line.** Measured line by line over 1,460
tracked files with both patterns: 84 lines read differently, 83 of them lines
that were not rows before and are now, and **one** that was a row and is not —
a fixture inside `rounds/round-1-report.md`, quoting this very shape. So M3's
own measurement stands unchanged; what was wrong was only the generalisation
drawn past its population.

**🟡 4's second half is worse than the comment says.** `seal.py:1437` says no
command brings a two-deep file back into agreement. Executed: the next
`seal mode local` sets the FIRST row to `local` and leaves the person's own
row two lines down reading `shared`, so the file states two modes and every
reader takes the first. It is not that the file stays broken — it is that the
command makes it disagree with itself, silently. That is what `overview.md`
§*Not done* now records.

**Why `overview.md` §*Not done* and not the two homes the round offered.**
§*Not verified* is for what nobody ran, and this was run, so a row there would
be a verified fact on the shelf for unverified ones — and `unverified-check`
counts those rows, so it would be a row nothing can ever close.
`seal/follow-up.md`'s own opening sends anything tied to a coordinate to a
`# RIDER:` at the line instead, and this is tied to `seal.py#with_row`. §*Not
done* is the section for what was deliberately left, which is what this is:
the repair belongs to the WRITER and this work item's scope is the reader.

## The survivor check

```
survivor-check --range c4e9c58b..HEAD --exempt seal/specs/1789598366-…/survivors.md
```

**Five places, and three were real survivors of the very claims this pass
corrected** — which is §12 arriving one file over, exactly as `agents/smith.md`
predicts for a range that corrects a claim:

| Place | What it still said | Done |
|---|---|---|
| `spec.md:137`, the A6 paragraph | *a regex that widens what parses can only ever make more lines into rows* — 🟡 2's own false generalisation, in a third copy | corrected |
| `questions.md:15`, W1's cell | the refusal *says every row below it is lost too*, with no condition | corrected |
| `changelog.md:45` | the same sentence, in the bullet a release-notes reader meets | corrected |

The other two are in `survivors.md` with the quote each is anchored on:
`questions.md` M3 keeps a sentence the correction in `plan.md` keeps too, and
`config_rows`'s walk is the loop `refusal` exists to stay in step with.

**Those two exemption rows turn out not to be load-bearing, and that is worth
saying.** After the three corrections landed, the check is clean over the same
range with no `--exempt` flag at all (exit 0 both ways). That is the second
silencing path `seal/follow-up.md` already tracks as #371 and #308 — an
exemption row's quote joins the range's own added text — so the rows are kept
for the judgment they record rather than for anything they do at the gate.

## What was run

| What | Result |
|---|---|
| `bin/test` over `test_the_seal_is_taken_once_by_the_sealer.py`, `test_the_mode_question_is_asked_once.py`, `test_the_settings_have_a_front_door.py`, `test_first_setup_asks_once.py`, `test_the_broad_gate_row_is_asked_for_and_runs_as_written.py`, `test_the_pull_request_language_is_the_repositorys.py` | exit 0 · 343 passed |
| the eight mutations above, each restored from bytes | exit 1 each · exit 0 restored |
| `bin/evidence-check --strict .` | exit 0 |
| `bin/evidence-check --reverify .` | 32 rows re-verified across the four passes, each claim re-read first |
| `bin/unverified-check seal/specs/` | exit 0 |
| `bin/survivor-check --range c4e9c58b..HEAD` | exit 0 after the corrections |
| `ruff check` and `ruff format --check` over the touched files | exit 0 · exit 0 |
| the full suite, the repository-wide lint, the typecheck | **not run** — the sealer's one broad run, after the rounds settle (`agent-contract` §2) |
