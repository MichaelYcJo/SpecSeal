# round 3 — the reopening's verifying round, and the last record of this run

| | |
|---|---|
| Target | the **diff of round 2's fixes**, `99005ba..64d830b` — not the branch |
| Review at | `64d830b` |
| Base of the branch | `origin/release/v0.11.1` = `f9c6907` |
| Draft pull request | #360 |
| Ran by | specseal:warden on Opus 5 |
| Previous record | `rounds/round-2.md`, closed — 3 fixed, 0 answered, 0 deferred |

## This is the last record, and that is decided before you start

Round 1 met the floor. Round 2 was its verifying round and reopened the run
on finding 16, which is the **one** reopening the chain allows. So this record
ends the run whatever it finds: if it opens something, that finding becomes an
issue with the verdict `deferred #N`, this record's `Fixes checked by` reads
`no fixes to check`, and the pull request is labelled `chain: capped`.

Nothing about that changes what you should report. Report what you find.

## The job

**The answers, not new findings** — for each of round 2's three verdicts, is
it actually closed. `rounds/round-2.md` holds the verdict table,
`rounds/round-3-fixes.md` holds what the fix pass says it did, and
`rounds/round-2-report.md` holds the reasoning the verdicts came from.

**There is no finding surface this time, and the record says so.**
`round-2.md`'s `New units` row reads `none`, derived from the fix diff by
`round_record.py close` rather than typed. The pass added no unit on purpose:
findings 16 and 17 both sit inside round 1's fix surface, where a case to pin
them would be depth 2 and is refused. So every surface in this diff is a
verification surface, and the round is three prose lines across three files.

## The three verdicts, and the half of each that is a decision

The diff is small; the judgments inside it are not. Each fix took part of a
paste-ready text and declined part, and the decline is the half worth checking
rather than inheriting.

- **Finding 16** — `.github/scripts/release_completeness_check.py:48-52`. The
  `Environment:` line now names `HEAD_SHA` with its default and one clause
  saying its absence is the silent one. **The pass declined to restate the
  merge-ref argument in full**, on the grounds that it already stands twice in
  the file — `merge_base`'s docstring and the comment above `point` — and a
  third copy would add a third place to keep in step, which is the failure
  mode finding 16 is itself an instance of. Judge whether the pointer it left
  instead actually reaches that argument, and whether the enumeration is now
  exhaustive against `grep -n environ` over the file.
- **Finding 17** — `tests/test_a_release_cannot_ship_an_untrue_milestone.py:488`.
  *all four* → *every entry*, taken over the arithmetic correction *all five*,
  on the grounds that the tuple can gain a sixth member and *five* would rot
  exactly as *four* did. Judge both halves.
- **Finding 5** — `overview.md:31`, *Eight* → *Nine*. The pass reports it swept
  the class rather than the coordinate, which is what produced the finding in
  the first place: four hits outside `rounds/`, two already correct and two
  counting a different subject, and the `rounds/` records deliberately left
  saying *eight* because they are past-state documents true at their own
  target SHA. **That sweep is the claim worth re-deriving**, since a sweep
  reported and not done reads identically to one done.

## Executed by the orchestrating session at `64d830b`

Exit codes read directly, no pipe. Re-derive rather than inherit:

- Eight modules, one per call — `test_a_release_cannot_ship_an_untrue_milestone`
  29 · `test_ci_gives_the_checks_what_they_need` 2 ·
  `test_a_merged_ticket_says_so_on_the_tracker` 23 · `test_docs_line_wrap` 23 ·
  `test_release_hygiene` 32 · `test_one_word_one_meaning` 13 ·
  `test_no_real_identifiers` 2 · `test_a_record_states_what_the_tree_has` 58 →
  **182 passed, exit 0 each**.
- `uvx ruff check` and `uvx ruff format --check` on the two changed Python
  files → **exit 0** each.
- The diff read line by line: three files, nine lines.
- `git status --porcelain` → empty.

## The form the commands take in this checkout

- **`ruff` is not installed here.** `uvx ruff check` / `uvx ruff format --check`.
- **Read exit codes directly, never through a pipe.** `cmd > /tmp/x 2>&1; echo $?`.
  This shell is `zsh`; `${PIPESTATUS[0]}` is not it.
- `bin/test`, narrow, one module at a time.
- `evidence_check.py .` **unscoped for reading** — no `--ledger`.

## Still unverified, and they stay that way

Round 1's finding 8 — whether `issues: read` reaches a pull request body — is
deferred to `overview.md` §*Not verified* with the repository owner as
answerer, at the 0.11.1 release pull request. Do not settle it by writing to
the tracker.

**The broad gate is the `sealer`'s. Do not run it.** No `bin/broad-gate`, no
whole-suite run, no repository-wide `ruff`. It comes due when this record
closes.

## Not a finding

The gate run against the live tracker refuses naming **#359 and #361**. Both
are in `release: 0.11.1` deliberately and ship in this release, so the
milestone is true as planned and the refusal is the gate seeing work that is
not merged yet. Do not report it and do not write the pair into anything.

## The two lines the run ends on

Answer each in a line of its own:

- `Needs a fix: no`, or `yes` and what does. A 🟡 answered with grounds is `no`.
  A finding located under `seal/specs/` is a correction and does not count.
- `Loses a record or crashes: no`, or `yes` and what does.

## Where the report goes

Write your report to `rounds/round-3-report.md` in the working tree,
uncommitted. Do not commit it and do not touch the tracker. The orchestrating
session verifies your highest-severity coordinates itself before any of it is
recorded.
