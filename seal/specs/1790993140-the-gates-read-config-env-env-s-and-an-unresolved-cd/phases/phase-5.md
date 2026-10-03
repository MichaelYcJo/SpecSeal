# 1790993140-the-gates-read-config-env-env-s-and-an-unresolved-cd — phase 5

| Field | Value |
|---|---|
| Phase | 5 |
| Commit | b68c404e |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

Write the ledger fragment for this work's claims. Re-read every existing row
`evidence-check` names as drifted, in the file it is in, correct it first
where an edit made it false, and re-stamp it with `--checked`. Write the
changelog fragment naming #716, #678 and #686, and `overview.md` with the
guard-strings shape in *Not done*. Draft the lines the pull request owes: the
test seen red, the failure direction, the prompt budget and platform honesty.

## What this phase found

**Evidence.** `evidence-check` named 13 drifted anchors after phase 4, cited by
22 rows across five release ledgers. All 22 were read against this work's
edits. Seventeen still held and took a dated *Re-read* note. Four claims had
gone false and were corrected in place in `seal/releases/0.16.0.md`: I9 and M2
said a redirected or zsh-prefixed git is in the group the guard says nothing
about, M1 said the guard never reads through `hooks/cmdline.py`, and M3 cited
a case that now asserts `ask`. M4's note, that `hooks/cmdline.py` has no diff
against `542f920b`, was corrected in its notes cell. `evidence-check
--reverify --checked 2026-10-03 --ledger` ran once per file over those five.
The fragment holds K1–K7.

**A record named removed code.** The records half of `evidence-check` refused
three names in `phases/phase-2.md`, which phase 4 deleted:
`unplaced_switch`, `_wider_walk` and `_places` (NAME NOT IN TREE). Each line
naming one now carries that marker, and the phase record keeps what phase 2
built. `phases/phase-4.md` named one of them too, and
`test_this_repositorys_own_records_state_nothing_the_tree_lacks` refused it in
the records run below; that line carries the marker as well.

**`survivor-check --range 233f0455..HEAD`** found one place: the wrapper test
module's docstring still said `env -S`'s string is read the way `eval`'s
argument is, and nothing more. It was corrected in `dcd87abd`, and the check
then reported no removed wording standing.

**Checks run, executed:** `bin/evidence-check` exit 0, 3616 ok and no
refusal; `rider_check.py` exit 0; `survivor-check` exit 0;
`unverified-check --baseline 233f0455` reads this overview's two open rows;
`correction-check` found no merge commit in the range. The 100 modules that
read the records, with `tests/test_no_real_identifiers.py`, the version timer
in `tests/test_release_hygiene.py` and the interpreter floor in
`tests/test_a_script_says_which_interpreter_it_needs.py`: 5819 passed, 2
skipped and 1 failed, the refusal above. The modules that read `phases/`
passed after it was corrected.

### Lines for the pull request

- **Test seen red.** Every new case failed before its fix: phase 1's 22 at
  `233f0455`, phase 2's against stubs returning the opposite, phase 4's against
  mutants that skip the question or make the last silent exit ask. Every unit
  added was broken once with `mutation-check`, and every break but one was
  red. The one, `switch -c` in `switch_kind`, showed that test was dead, and
  phase 4 removed it.
- **Failure direction.** The commit gate only gains commits it finds, so it
  stops more and never less. The guard only turns a silence into an `ask`,
  and only at an exit where it was about to say nothing, so it stops more and
  never less. Where `hooks/cmdline.py` fails to load, the guard keeps every
  row it had and asks nothing new.
- **Prompt budget.** Commit gate: a stop on a command holding a spaced
  `--config-env` or an `env -S` before a commit, which the base stopped
  nowhere. Guard: 0 added stops over D1's 27,351 recorded command and
  directory pairs, by phase 3's count. #686's ask would have added 9, so it
  was not wired.
- **Platform honesty.** String reading only, no process inspection. M1 ran on
  git 2.54.0 (Apple Git-157) alone; `--config-env` needs git 2.31 or later and
  `env -S` GNU coreutils 8.30 or later or macOS `env`. The count's corpus is
  one machine's transcripts. CI's Linux and Windows legs run the cases.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
