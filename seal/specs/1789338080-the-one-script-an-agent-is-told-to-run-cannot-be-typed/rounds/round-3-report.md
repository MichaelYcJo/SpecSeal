# Round 3 — the verifying round, against `git diff 74fb1aa..0d2066d`

Round 2 closed with four fixed and one answered. This round's job is the
answers: for each of those five, is it actually closed, and is the unit the
fixes created correct as code. The exec-bit residue was re-counted from the
tree rather than carried, and 🟡 9's answer was re-measured rather than
accepted.

All five of round 2's verdicts hold. Two things are open, and neither of
them is in the tool: one is a false count in the issue this branch filed its
residue into, and one is a hole in the new case's grip.

## Round 2's five verdicts, checked

**🟡 8 is fixed, and the fix is pinned against four ways of undoing it.**
`reachable` still refuses a hyphenless command, and the message a reader now
gets names the path and says why. I mutated the new case's subject four ways
in a clone and it went red on every one: the pre-fix message restored, the
branch inverted, the hyphen guard deleted, and the explanation dropped with
the path kept. The fifth mutation is finding 14 below.

**🟡 9's answer holds, re-measured rather than inherited.** All three of its
load-bearing facts are true of the tree at `0d2066d`:

- 43 shipped documents, which is what `agents/`, `skills/` and `templates/`
  hold.
- Six hyphenated commands appear as bare words in documents that name no
  script — `arm-check` in 1, `broad-gate` in 9, `deferral-check` in 1,
  `evidence-check` in 6, `survivor-check` in 3, `unverified-check` in 4.
  Six commands, `broad-gate` in nine, exactly as written.
- `agents/warden.md:247` reads *Carry the broad-gate state into your report*,
  and `skills/code-review/orchestration.md:442` reads *`evidence-check` takes
  `--ledger`*.

The flag-demanding alternative is worse for the reason given, and I checked
the instance rather than the assertion: `skills/code-review/orchestration.md`
names `evidence_check.py` at lines 448 and 449 and carries no path to it, so
its only locator is the bare command at line 442 — which a flag-demanding
reader would not accept, because *takes* sits between the command and the
flag. That document would go red for a script that is perfectly reachable.
The first alternative is dominated on its own terms: a reader that accepts
the bare command wherever something follows it still passes *the seal after
the rounds*, which is the prose the guard exists to refuse.

**⬜ 10 is fixed, and the count is right on the fourth attempt.** I counted
from the tree without reading round 2's list first, then compared. `bin/`
holds twelve pairs. Five have the bit asserted somewhere: `evidence-check`
(`tests/test_chain_hooks_hardening.py:279`), `deferral-check`
(`tests/test_deferral_check.py:178`), `round-record`
(`tests/test_the_record_is_generated.py:2638`), `unverified-check`
(`tests/test_unverified_rows_close.py:550`), and `session-cost` through the
new assertion in the class pin. Seven do not: `arm-check`, `broad-gate`,
`payload-meter`, `seal`, `seal-stamp`, `survivor-check` and `test`. The
ledger row and the memo name those seven and no others, and *newly covers
exactly one, `session-cost`* is right — the pin reaches only
`evidence-check`, `round-record` and `session-cost`, and the first two were
already covered.

**⬜ 11 is fixed.** The classification is now bounded to places outside
`tests/` and names the test modules as a class. I walked the tree for
`chain_check.py` outside `tests/` and `seal/`: the three hand-written
invocations are `.github/workflows/hygiene.yml:191`,
`templates/hygiene.yml:94` and `docs/release-checklist.md:100`, each with the
full path, and the two in code are `skills/verify/scripts/broad_gate.py:130`
and `skills/code-review/scripts/round_record.py:207`, each building it. No
sixth place invokes it.

**⬜ 12 is fixed.** The *Alternatives considered* table is seven contiguous
rows with no blank line in it, and the correction note sits below the table
naming the row it is about.

## The count round 2 discredited is still standing in #389

`overview.md:85` and the ledger row both hand the executable-bit residue to
#389, and that issue is where the residue lives once this branch merges. Its
title reads *four wrapper pairs carry an executable bit nobody asserts*, and
its body names `arm-check`, `broad-gate`, `payload-meter` and `seal-stamp` —
the four round 2 measured as wrong. `seal`, `survivor-check` and `test` are
missing from it.

The body already contradicts itself: its own repro line says *twelve POSIX
wrappers* while its narrative says four are unasserted and four modules
assert one each, which cannot both be true.

This is the number that has been wrong three times, wrong a fourth time in
the one place that outlives the branch. The memo in `overview.md` says the
number is recorded as names *because it was wrong three times*, and then
points the reader at a ticket carrying the discredited one.

The repair is an issue edit, not a commit — finding 13's fenced block below
is the replacement title and the two paragraphs that change.

## The new case passes when the bad repair is offered in other words

`test_the_failure_message_offers_a_repair_that_actually_works` decides
whether the message offers a repair the rule rejects by looking for one exact
phrase, `the command \`seal\``. A message that offers the same bad repair in
any other wording passes it.

Measured in a clone: with the message changed to `` Add `seal` or the path
`skills/implement/scripts/seal.py`. … ``, the case is green. That is the
defect §14 asks the pin to prevent, reintroduced, and nothing goes red.

The cheapest tightening pins the head of the offer rather than the absence of
a phrase, and I checked it both ways before writing it down: it holds against
today's message and goes red against that mutation. Finding 14's block below.

## Three smaller things

**The hyphenless message's last clause attaches to the wrong half.** The
assert appends `, once` to whatever `forms` produced, and the hyphenless arm
now ends in a sentence of its own, so a reader gets *… does not read the bare
command as a locator -- see `reachable`, once*. The instruction is still
followable; the sentence is not one.

**`command_name`'s docstring still says *all eleven existing pairs*** at
`tests/test_a_document_that_names_a_script_says_how_to_reach_it.py:109`,
while `bin/` holds twelve and the ledger row and the memo both now say
twelve. It is outside the fix diff, but it is the same number in the same
file, which is what §12 asks a fix to sweep.

**A line number is being used as a coordinate.** The guard's comment and
`overview.md` both cite `agents/warden.md:247`. It is correct today — I
opened it — but `CLAUDE.md` writes down why this repository stopped pointing
at positions, and `agents/warden.md` is a file the plugin edits often.

## What has to happen at the close, and what has not been run

`chain_check.py --worktree` at `0d2066d` exits 1 on two rows, and both are
expected states rather than findings:

- `Broad gate` is `not yet` on the last record. That is the sealer's single
  act, and this round did not take it.
- `Pass` is checked on `round-2.md` beside `Fixes checked by: nobody — the
  fixes are not yet written`. This round is the verifying round that clears
  it, so closing it has to write `round-3` into that cell. If the close
  writes `round-3.md` and leaves that cell at `nobody`, the pull request
  stays red for the reason this round exists to remove.

The broad gate has not run. Nothing in this report needs a fix in the tree,
so it has come due: the sealer's spawn is the next act, not a run for the
session reading this.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 8 | The locator failure message named a repair the guard made impossible | `tests/test_a_document_that_names_a_script_says_how_to_reach_it.py:294-303` | answered | Closed. **Executed** 2026-09-14 in a clone at `0d2066d`: the message now names the path and says why, and the new case goes red against four separate ways of undoing it — the pre-fix message restored, the branch inverted, the hyphen guard deleted, the explanation dropped. The comment beside the guard no longer calls a wrapped script reachable by path only |
| 🟡 9 | The hyphen is not what separates a command from prose | `tests/test_a_document_that_names_a_script_says_how_to_reach_it.py:147-160` | answered | The answer stands, re-measured rather than accepted. **Executed** 2026-09-14: 43 shipped documents; six hyphenated commands appear as bare words in documents naming no script (`arm-check` 1, `broad-gate` 9, `deferral-check` 1, `evidence-check` 6, `survivor-check` 3, `unverified-check` 4). **Read** 2026-09-14: `agents/warden.md:247` and `skills/code-review/orchestration.md:442` say what the comment quotes, and `orchestration.md` names `evidence_check.py` at 448-449 with no path, so a flag-demanding reader would red it. The bound is written at the guard and in `overview.md` |
| ⬜ 10 | The executable-bit residue is seven, not four | `tests/test_a_document_that_names_a_script_says_how_to_reach_it.py:249` | answered | Closed in the tree. **Executed** 2026-09-14, counted from `bin/` before reading round 2's list: twelve pairs, five asserted (`evidence-check`, `deferral-check`, `round-record`, `unverified-check`, `session-cost`), seven not (`arm-check`, `broad-gate`, `payload-meter`, `seal`, `seal-stamp`, `survivor-check`, `test`). The pin reaches exactly `evidence-check`, `round-record` and `session-cost`, so *newly covers exactly one* is right. The ledger row and the memo name the same seven. See finding 13 for where the old count survives |
| ⬜ 11 | *Every place that invokes it* read as a closed list | `tests/test_a_document_that_names_a_script_says_how_to_reach_it.py:73-79` | answered | Closed. **Executed** 2026-09-14, walking the tree outside `tests/` and `seal/`: five invocations, all accounted for — `.github/workflows/hygiene.yml:191`, `templates/hygiene.yml:94`, `docs/release-checklist.md:100` by hand, `skills/verify/scripts/broad_gate.py:130` and `skills/code-review/scripts/round_record.py:207` in code. No sixth |
| ⬜ 12 | The correction note orphaned the last row of the alternatives table | `seal/specs/1789338080-the-one-script-an-agent-is-told-to-run-cannot-be-typed/plan.md:76-83` | answered | Closed. **Read** 2026-09-14: seven contiguous rows, the comment below them, and it names the row it corrects |
| 🟡 13 | #389 carries the count round 2 discredited, and names three wrappers short | GitHub issue #389, pointed at by `seal/specs/1789338080-the-one-script-an-agent-is-told-to-run-cannot-be-typed/overview.md:85` | open | **Executed** 2026-09-14: `gh issue view 389` returns the title *four wrapper pairs carry an executable bit nobody asserts* and a body naming `arm-check`, `broad-gate`, `payload-meter`, `seal-stamp`. `seal`, `survivor-check` and `test` are absent, and the body's own repro line says twelve wrappers while its narrative says four. The memo says the residue is filed there, so this is the number's durable home. The repair is `gh issue edit`, not a commit |
| 🟡 14 | The new case is green when the bad repair is offered in other words | `tests/test_a_document_that_names_a_script_says_how_to_reach_it.py:361` | open | **Executed** 2026-09-14 in a clone: with the hyphenless arm changed to `` Add `seal` or the path `…` ``, the case passes. The assertion looks for one exact phrase rather than for what the rule accepts, so §14's pin does not hold against a rewording. The proposed tightening was checked both directions — green today, red against that mutation |
| ⬜ 15 | The hyphenless message ends *see `reachable`, once* | `tests/test_a_document_that_names_a_script_says_how_to_reach_it.py:303` | open | **Read** 2026-09-14: the assert appends `, once` to `forms`, and the hyphenless arm ends in a second sentence, so the trailing clause modifies *see `reachable`*. The hyphenated arm reads correctly. Behaviour and fact are right; the sentence is not |
| ⬜ 16 | `command_name`'s docstring says *all eleven existing pairs* | `tests/test_a_document_that_names_a_script_says_how_to_reach_it.py:109` | open | **Executed** 2026-09-14: `bin/` holds twelve pairs. Outside the fix diff, but the same number in the same file the fix corrected twice elsewhere |
| ⬜ 17 | A line number is used as a coordinate | `tests/test_a_document_that_names_a_script_says_how_to_reach_it.py:150` · `seal/specs/1789338080-the-one-script-an-agent-is-told-to-run-cannot-be-typed/overview.md:96` | open | **Read** 2026-09-14: `agents/warden.md:247` is correct today. `CLAUDE.md` §*A ledger coordinate names content, never a position* is this repository's own reasoning for not doing it, and `agents/warden.md` is edited often |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_a_document_that_names_a_script_says_how_to_reach_it.py -q`, in a `git clone --no-local` at `0d2066d` | **exit 0** — 31 passed, 8 skipped |
| Five mutations of the message and the guard, one at a time, the file restored from bytes read before the first write, the case re-run for each | Four **red** (pre-fix message, branch inverted, guard deleted, explanation dropped); one **green and not caught** (the bare command offered in other words) — finding 14 |
| The proposed tightening for finding 14, against today's message and against the missed mutation | **holds** today, **red** against the mutation |
| Wrapper pairs in `bin/` counted against every exec-bit assertion in `tests/` | twelve pairs, five asserted, **seven not**: `arm-check`, `broad-gate`, `payload-meter`, `seal`, `seal-stamp`, `survivor-check`, `test`. The pin newly covers exactly one, `session-cost` |
| Every wrapped command matched as a bare word across all shipped documents that name no script | 43 documents; **six** commands, `broad-gate` in **nine** |
| Every `chain_check.py` mention outside `tests/` and `seal/`, read for invocations | **five**, each carrying or building the full path |
| `python3 skills/evidence-check/scripts/evidence_check.py .` | **exit 0** — 1181 ok, 0 drifted, 0 broken; the fragment's 7 rows all resolve, including the two anchors this diff re-stamped |
| `python3 skills/code-review/scripts/survivor_check.py --range 74fb1aa..0d2066d` | **exit 0** — 16 removed sentences, no removed wording still standing |
| `python3 skills/code-review/scripts/chain_check.py --worktree --baseline origin/release/v0.11.4` | **exit 1** on two expected rows — `Broad gate: not yet`, and `Pass` checked beside `Fixes checked by: nobody`. Both are what this round and the sealer close |
| `gh issue view 389` | title and body carry **four**; `seal`, `survivor-check`, `test` absent — finding 13 |
| Broad gate — the full suite, the repository-wide lint, the typecheck | **not yet**, and not this round's. Contract §2 assigns it to the sealer, and nothing in this report needs a fix in the tree, so it is now due |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Seven `bin/` wrapper pairs have no exec-bit assertion, and closing them needs a case walking `bin/` | #389 | whoever takes #389; finding 13 is that the ticket's own count is wrong |
| Eleven `seal/ledger.md` rows re-stamped with unmoved `Checked` dates | #387 | whoever takes #387; unchanged by this diff, as round 2 left it |

## Paste-ready fixes

Finding 13 — the new title for #389:

```
test: seven wrapper pairs carry an executable bit nobody asserts, and the class pin cannot see them
```

Finding 13 — the two paragraphs of #389's body that change:

```
A `bin/` wrapper pair is a POSIX script and a `.cmd` twin, and the POSIX half
has to carry the executable bit or it resolves on PATH and then refuses with a
permission error. Four modules assert that bit, and each asserts it of its own
wrapper only: `bin/evidence-check`, `bin/deferral-check`, `bin/round-record`
and `bin/unverified-check`.

After #318 planted one more pair and one more assertion, seven of the twelve
have nobody asking: `arm-check`, `broad-gate`, `payload-meter`, `seal`,
`seal-stamp`, `survivor-check` and `test`. The assertion #318 added covers
exactly one that was not already covered, `session-cost`. All seven are
`100755` in the tree today, so nothing is broken. What is missing is anything
that would notice a thirteenth pair committed `100644`, or one of these seven
losing the bit in a move.

The number is recorded as names because it has been wrong three times: round 1
of #318 said eight, its first fix pass said four, and both counted by matching
filenames in any module that mentions them rather than opening each
`os.access` call. Round 2 opened all twelve pairs against every exec-bit
assertion in `tests/` and got seven.
```

Finding 14 — replace the first assertion of
`test_the_failure_message_offers_a_repair_that_actually_works` so it pins what
the message offers rather than one spelling of what it must not:

```python
    assert f"Add the path `{seal}`." in message, (
        "the message offers something before the path, so a reader meets a "
        "repair the rule rejects before the one it accepts. The bare command "
        f"is not one this rule reads as a locator -- {message}"
    )
```

Finding 15 — move `, once` inside both arms so it attaches to the offer:

```python
    forms = (
        f"the path `{script}`, once. `{command}` has no hyphen in it, so this "
        "rule does not read the bare command as a locator -- see `reachable`"
        if "-" not in command
        else f"either reachable form, once: the command `{command}`, or the "
        f"path `{script}`"
    )
    assert reachable(text, script), (
        f"{document} names {os.path.basename(script)} and never says where it "
        f"is. A reader who goes looking finds nothing, which is #318. Add "
        f"{forms}"
    )
```

Finding 16 — `tests/test_a_document_that_names_a_script_says_how_to_reach_it.py:109`:

```python
    Underscores to hyphens, which is what all twelve pairs in `bin/` do and
```

Needs a fix: no

Loses a record or crashes: no

Findings 13 and 14 are both real and both carry a paste-ready repair, and
neither is a fix to the tool that a fix pass would commission. 13 is a
`gh issue edit` on a ticket this run filed — outside the tree, and outside
anything `survivor-check --range` or the record chain can verify. 14 is a
tightening of a pin whose subject is correct today, which the smith can answer
with grounds: four of the five mutations are caught, and the fifth needs
somebody to deliberately reword the message. 15, 16 and 17 are corrections.

Nothing found here leaves a record outside the root and nothing crashes.

If the reader's convention is that any owed correction counts against that
first line, finding 13 is the one, and it is owed before this branch merges —
the memo sends the next person to #389 for a residue the ticket undercounts by
three.

## Proof

Opened and read in full or in the named range:

- `tests/test_a_document_that_names_a_script_says_how_to_reach_it.py` (whole)
- `git diff 74fb1aa..0d2066d`, and the four commit messages
- `seal/ledger/1789338080-the-one-script-an-agent-is-told-to-run-cannot-be-typed.md`
- `seal/specs/1789338080-the-one-script-an-agent-is-told-to-run-cannot-be-typed/overview.md` (the added memo), `plan.md:70-100`, `rounds/round-1.md:1-20`, `rounds/round-2.md`
- `agents/warden.md:246-248`, `skills/code-review/orchestration.md:441-449`
- `templates/sdd-round.md:100-130`
- `bin/test`, `bin/` listing with modes
- `tests/test_docs_line_wrap.py:1-60`
- `README.md` (searched for every form the new fixture depends on)
- GitHub issues #389 and #387

Not opened: the rest of the branch before `74fb1aa`, which rounds 1 and 2
reviewed, and `skills/verify/scripts/broad_gate.py` beyond the two lines
named.

Work was done in a `git clone --no-local` at `0d2066d` under the session
scratchpad, with the virtual environment the repository's own runner builds
for reuse. Nothing was written in the checkout except this file. The clone and
three throwaway probe scripts, named as the contract asks, were deleted before
this report was handed over.

