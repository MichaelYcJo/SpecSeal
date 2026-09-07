# Feature Specification: round-record says which interpreter it needs

<!-- seal/specs/1788789985-round-record-dies-on-python-3-9/spec.md — WHAT this
work delivers and how we'll know. The policy documents in docs/ outrank this
file; cite them, don't restate. -->

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CONTRIBUTING.md` §*Running the checks* — "**Python 3.12 is the supported floor**, held as `FLOOR` in `.github/scripts/run_tests.py` so this sentence and the code state one number" | Settles the ticket's two suggested repairs against each other. 3.9 is not a version this repository supports, so dropping `strict=True` would not make the script run there — it would move the death to the next 3.10+ construct while deleting an invariant the code states on purpose |
| `CONTRIBUTING.md` §*Running the checks*, same paragraph — "Check `python3 -V` before using it, since nothing here holds the floor for you: macOS ships 3.9 under that name" | The repository already knows this failure exists and already answers it with a sentence a person has to read first. The ticket is that answer arriving too late, from a document rather than from the command |
| `CLAUDE.md` §*The goal a design is chosen against — verification that runs unattended* | Between a guard that states the floor and a guard that asks, the one that states it is the cheaper. Nothing here stops to ask anybody |
| `skills/agent-contract/SKILL.md` §12 — a defect belongs to a class | The ticket names one coordinate. What is owed is every script this plugin ships that a person or the harness runs with whatever `python3` is on PATH |

## Scope

**In.** A version guard at the top of `skills/code-review/scripts/round_record.py`
that refuses an interpreter below the floor with a sentence naming the floor,
the version it found and the interpreter it found it at — before argument
parsing, before the sibling checker is loaded, and before anything is read or
written. The regression tests that pin the sentence and the refusal. The
enumeration of every other member of the class, recorded with an answerer.

**Out, and each for a stated reason.**

- **The four `strict=True` sites stay exactly as they are.** The comment above
  the first of them, in `round_record.py#swallowed`, says what it states: both of the
  reader's passes keep indices intact, so the two reads are the same file line
  for line, and a length that differed would truncate the hidden set — which is
  the guard reporting clean because it read less. Removing it to buy 3.9
  compatibility trades a real invariant for a platform this repository does not
  support.
- **`skills/code-review/scripts/chain_check.py` and
  `skills/implement/scripts/seal.py` are not edited.** Two other work items in
  this release hold those files, and a conflict costs a second broad gate.
  `seal.py` is a member of the class (`datetime.UTC`, 3.11) and goes to
  `seal/follow-up.md` instead.
- **The other members are not fixed here.** They are enumerated, measured and
  deferred with an answerer named. Fixing them would put five more files into a
  diff two other branches are already touching.
- **`round_record.py:982`'s `removesuffix`** is 3.9 and is not part of this.

## The class, enumerated by construction

**The property**: *a Python file this plugin ships that a person or the harness
invokes with whatever `python3` resolves to on PATH* — as opposed to one that
runs under `bin/test`'s virtualenv or under CI's `actions/setup-python`, both of
which hold the floor for it.

**How the set was built, not read.** Three constructions, each executed, none of
them a walk through the tree looking for problems:

1. **The entry points.** `grep -rln '__name__ == "__main__"'` over `git ls-files
   '*.py'`, less `tests/` and `seal/` — 25 files.
2. **Which interpreter each one gets.** `hooks/hooks.json` invokes every hook
   through `python3 "${CLAUDE_PLUGIN_ROOT}/hooks/dispatch.py"`, so all twelve
   hooks are in. `docs/release-checklist.md` §3, `CONTRIBUTING.md:15,128-131` and
   `docs/branch-and-release.md` name six scripts after a literal `python3 `.
   `.github/workflows/*.yml` pin their own interpreter, and `bin/test` builds a
   virtualenv at the floor or refuses.
3. **Which of them actually breaks below the floor.** Syntax by construction:
   `/usr/bin/python3 -m py_compile` (3.9.6) over every shipped `.py` — one
   failure, and it is a test file, so **no shipped script carries 3.10+ syntax**
   and a guard placed after the imports is always reached. Runtime API by a
   scan for the names 3.10, 3.11 and 3.12 added.

**The scan's own spelling has been wrong twice, and that is the part worth
recording.** Both times it was an instance the pattern could not reach, and
both times the class was one member larger than the enumeration said.

1. `zip\([^)]*strict=` hid the site in `round_record.py#inherited_rows`, where
   an inner `verdict_words(reader, rows)` closes a parenthesis before `strict=`
   is reached. Three of four sites answered; the fourth did not.
   `zip\(.*strict=` finds all four, at any depth of nesting on one line.
2. `datetime\.UTC` hid `skills/verify/scripts/session_cost.py`, which spells
   the module `import datetime as dt` and writes `dt.UTC`. Found by review
   round 1, which re-derived the class from the AST instead of from this
   table. `\b\w+\.UTC\b` matches whatever the module was named.

A class enumerated with a pattern that cannot match every instance is a class
enumerated by reading, wearing a command's clothes.

**What the pattern still cannot see, stated rather than left to a third
round**: a `zip(` whose `strict=` is on a later line, and `from datetime
import UTC` used bare. Neither is in the tree — measured, not assumed. A third
widening would move the blind spot a third time, so the honest next step is
the AST walk the ledger fragment's R3 names, and that is a change to a gate
rather than a line in this work item.

| # | File | What it does below the floor | Needs | Invoked with | Verdict |
|---|---|---|---|---|---|
| 1 | `skills/code-review/scripts/round_record.py` `#swallowed`, `#inherited_rows`, `#signature` (two sites) | `zip(..., strict=True)` → `TypeError: zip() takes no keyword arguments`, after the report has been read | 3.10 | the orchestrator's `python3` | **fixed here** |
| 2 | `.github/scripts/gather_changelog.py:151` | `datetime.UTC` → `AttributeError`, at the moment it writes the dated heading | 3.11 | a person, at a release — `CONTRIBUTING.md:128,130`, `docs/release-checklist.md:39,46,64`, `docs/branch-and-release.md:163` | deferred, `seal/follow-up.md` |
| 3 | `.github/scripts/fold_ledger.py:358` | `datetime.UTC` → `AttributeError`, same moment | 3.11 | a person, at a release — `CONTRIBUTING.md:129,131`, `docs/release-checklist.md:40,47,65`, `docs/branch-and-release.md:184` | deferred, `seal/follow-up.md` |
| 4 | `skills/implement/scripts/seal.py:324,436` | `datetime.UTC` → `AttributeError`, on `seal export` and on `seal mode` | 3.11 | a person, and `.github/workflows/hygiene.yml:170` | deferred — another branch holds the file |
| 5 | `hooks/root-migrate.py:425` | `zip(..., strict=True)` → `TypeError`, while migrating a 0.3.x layout | 3.10 | the harness, `hooks/hooks.json` session-start | deferred, `seal/follow-up.md` |
| 6 | `skills/verify/scripts/session_cost.py:89` | `dt.UTC` → `AttributeError`, when a transcript carries a zone-less timestamp. **Missed by this table's first pass**: the construct is `datetime.UTC` behind `import datetime as dt`, and the scan matched the literal spelling only. Executed on 3.9.6, end to end: exit 1 with a bare traceback | 3.11 | a person, ending a run — `docs/review-handoff-protocol.md` §*After a run* | deferred, `seal/follow-up.md` |
| 7 | `skills/code-review/scripts/chain_check.py` | nothing — no 3.10+ construct. Its `strict=True` at `:2737` is a parameter default, not `zip`'s keyword | — | a person, `docs/release-checklist.md:71` | left alone |
| 8 | `skills/evidence-check/scripts/evidence_check.py` | nothing found | — | a person, `CONTRIBUTING.md:15` | left alone |
| 9 | `skills/verify/scripts/unverified_check.py` | nothing found | — | a person, `docs/release-checklist.md:69` | left alone |
| 10 | `skills/verify/scripts/deferral_check.py` | nothing found | — | a person | left alone |
| 11 | the other eleven `hooks/*.py` | nothing found | — | the harness | left alone |
| 12 | `.github/scripts/close_issues_on_release.py`, `roll_flow_measurement_issue.py`, `run_tests.py` | not measured against the floor | — | CI pins it; `run_tests.py` IS the floor | out of the class |

**Rows 7 to 12 are here on purpose.** A table listing only the offenders is a
list of findings; a table with the rest in it is an enumeration, and it is what
the next round can check rather than repeat. Row 6 is what that is worth: it
sat among these as *nothing found* for a whole build, and the round that
checked the table instead of repeating it is what moved it up.

**Count: 25 entry points, 6 members that break, 1 fixed, 5 deferred.**

## Where the floor number lives, and why it is not imported

The handoff asked this to be argued rather than assumed: how does a stdlib-only
script under `skills/` reach `FLOOR` in `.github/scripts/run_tests.py`?

**It can, and it should not.** `importlib.util.spec_from_file_location` is
already in this file — `round_record.py:118-128` loads `chain_check.py` that
way — and the plugin ships `.github/` into the cache, verified at
`~/.claude/plugins/cache/specseal/specseal/0.9.0/.github/scripts/`. So the
import would work today. Three things say not to:

1. **A guard that can fail to load is not a guard.** Its whole job is to replace
   a traceback with a sentence. Reaching three directories up into a dot
   directory to find the number gives it a second way to die, on the exact
   machine that has no other way to be told what is wrong.
2. **A fallback-safe read still needs a literal.** Wrap the read in
   `try/except` and the `except` branch has to name a floor — so the second
   spelling exists either way, and the read buys nothing but the machinery.
   That is the argument that settles it: there is no version of the import that
   removes the second number.
3. **This repository already answers "one number, several carriers" with a
   test, and does it twice.** `ruff.toml`'s `target-version`, both READMEs,
   `.github/workflows/test.yml`'s matrix, `CONTRIBUTING.md`'s sentence and
   `run_tests.py`'s `FLOOR` are five spellings of `3.12` today, held together by
   `tests/test_release_hygiene.py#test_the_python_floor_is_the_same_number_everywhere`
   and by
   `tests/test_the_suite_has_a_command_that_is_cheap_twice.py#test_the_section_and_the_runner_state_the_same_floor`.
   A sixth carrier joins under the rule the other five already live by.

**So `round_record.py` holds `FLOOR = (3, 12)` and a test pins it to
`run_tests.FLOOR`.** The number cannot drift, because the drift is a test
failure at the commit that causes it rather than a wrong sentence on somebody's
terminal months later.

**Those two existing tests never compare their own two authorities to each
other** — one reads `ruff.toml`, the other reads `run_tests.py`, and nothing
reads both. The new test asserts against both, which closes that gap as a side
effect rather than as a new mechanism.

## The guard is a block, not a shared helper

The handoff asked where it lives so the two work items holding `seal.py` and
`chain_check.py` can adopt it without inventing a third spelling.

**It is a copyable block of about fifteen lines in the file it guards**, and
the reason is the one above: a helper means an import, an import means a second
way for the guard to die, and every candidate location for a shared module is
further from `skills/code-review/scripts/` than `chain_check.py` is. The block
needs `sys` and nothing else.

`skills/code-review/scripts/round_record.py#below_floor` is the spelling to
copy. What has to travel with it: the constants `FLOOR`, `FLOOR_TEXT` and
`BELOW_FLOOR`, the function, and the four-line `if` that runs it at module
level after the imports and before any other module-level work. What must not
travel is a fresh wording of the sentence — the new test reads the sentence
from the module, so a second file adopting the block joins the same pin.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| An operator on macOS's system Python | Given `python3` is 3.9 · When they run `round_record.py new --item … --round 1 …` · Then the process exits 2 having printed a sentence naming the floor, the version found and the interpreter's path, and nothing was read or written | `tests/test_a_script_says_which_interpreter_it_needs.py#test_the_script_refuses_at_entry_on_a_below_floor_interpreter` — the real script, a real sub-floor interpreter, a subprocess |
| The failure arrives at entry, not mid-run | Given the same · When the arguments are otherwise valid enough to get past `argparse` · Then no traceback appears and nothing about the item directory is mentioned, because the guard ran before argument parsing and before `chain_check.py` was loaded | the same case asserts the absence of `Traceback` and of the item path; `#test_the_guard_precedes_every_other_module_level_act` reads the module's AST |
| Above the floor nothing changes | Given `python3` is at or above 3.12 · When any command runs · Then behaviour is byte-identical to before | `#test_the_floor_and_above_are_let_through` on the boundary and one above it; the existing `tests/test_the_record_is_generated.py` is the wider proof |
| The sentence names both numbers | Given an interpreter below the floor · When the guard fires · Then the text names the floor AND the version found — a floor without the found version cannot be checked by the person reading it | `#test_an_interpreter_below_the_floor_gets_a_sentence` |
| The floor stays one number | Given someone raises the floor in `run_tests.py` or `ruff.toml` · When the suite runs · Then it fails until `round_record.py` states the same number | `#test_the_floor_is_the_number_the_runner_and_the_linter_hold` |
| The class does not grow in silence | Given someone adds a `zip(..., strict=)` or a `datetime.UTC` to a shipped script · When the suite runs · Then it fails naming the new coordinate and asking for it to be classified | `#test_no_shipped_script_needs_more_than_the_floor_without_saying_so` |

## Data & interfaces

No schema, no payload. Two surfaces change:

- **A new exit path**, code `2`, from a module-level `SystemExit` before
  `main()`. `round_record.py`'s docstring already documents 2 as "the input was
  unusable and nothing was written"; the sentence is extended to cover the
  interpreter, because a code whose meaning is written down and then quietly
  widened is a code nobody can read.
- **A new stderr sentence**, `BELOW_FLOOR`, pinned by a test per
  `skills/agent-contract/SKILL.md` §14.

Ledger rows go to `seal/ledger/1788789985-round-record-dies-on-python-3-9.md`.

## Open questions → questions.md

None block the build. `questions.md` carries the one decision that is the
repository owner's and is not this work item's to take.
