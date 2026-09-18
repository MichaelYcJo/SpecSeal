# Feature Specification: a tracked file the tree deleted stops the sweep

<!-- seal/specs/1789687448-a-tracked-file-the-tree-deleted-stops-the-sweep/spec.md — WHAT this
work delivers and how we'll know. The policy documents in docs/ outrank this
file; cite them, don't restate. -->

Two tickets, one branch. **#432 is the instance, at a coordinate a release
meets; #282 is the class, already written down.** #432's own body sends the
work to #282: *worth checking in the same pass whether any other case in the
suite opens a `git ls-files` path without the same guard.* Both tickets state
the repair as *skip a listed path that is not on disk*, and neither enumerates
the reach. This document enumerates it from the tree and corrects the shape in
one place.

## The reach, enumerated from the tree

Read on 2026-09-18 at `f8cf32e5`, by grep over every `git ls-files` and
`git ls-tree` call in `tests/`, `skills/`, `hooks/` and `.github/`, then by
opening each call site. Nothing below is executed.

**Five helpers build a corpus from `git ls-files` and open every path from
disk with no existence guard. Seven call sites open one.**

| Helper | Opening call sites | Corpus |
|---|---|---|
| `tests/test_no_real_identifiers.py#tracked_text_files` | `:48`, `:64` | the whole tree, minus three image suffixes and itself |
| `tests/test_no_document_names_the_old_roots.py#tracked` | `:97`, `:146` | `SCANNED` prefixes, `.md`/`.yml`/`.sh` |
| `tests/test_release_hygiene.py#tracked` | `:491` | `LOADED` prefixes |
| `tests/test_a_release_is_sized_by_a_criterion.py#tracked` | `:236` | `SCANNED` prefixes, `SUFFIXES` |
| `tests/test_a_script_says_which_interpreter_it_needs.py#shipped_python` | `:512` | `*.py` outside `tests/` and `seal/` |

**Only the first reaches `seal/ledger/`**, which is why the fold is what found
it. The other four are reached by any deletion under their own prefixes — a
`git mv` of a skill before staging, a `git rm --cached`, a half-applied patch.
So the class is not *the fold*, and #282 says so in its own *Not this*
section.

**Two helpers already guard, by two different rules, and neither was the
ticket's.**

- `tests/test_a_new_returnable_value_is_a_contract_change.py#tracked_python:96`
  filters with `os.path.isfile`, silently. This is the precedent the repair
  copies, and it is already in this suite.
- `tests/test_the_pull_request_language_is_the_repositorys.py#unreachable_templates`
  guards with `try/except OSError: continue`, silently. Its own round 5
  recorded that this silence dropped a document from the corpus and produced a
  false report. It is out of scope, and named below.

**Three shapes are immune by construction and are not touched.** Every shipped
script that walks a git listing reads the CONTENT from git as well —
`chain_check.py#read_record`, `survivor_check.py#read_blobs`,
`unverified_check.py#show`, all via `git show` or `git cat-file --batch`.
`chain_check.py#read_record`'s docstring states the rule: *the name comes from
`ls-tree`, so the content has to come from the same place*, and
`tests/test_chain_check_at_the_pull_request.py:1026` is the case that holds it
there. The fixture-repository helpers in `test_the_root_migrates_itself.py`,
`test_routing_is_recorded.py` and `test_the_mode_is_a_row_and_a_command.py`
list a repository the case built and not this one.
`tests/test_the_release_check_watches_what_ships.py:89` takes top-level names
and opens nothing.

**CI never meets this.** The workflows check out a clean tree, where the index
and the disk agree by construction, so every instance of this defect is a
LOCAL run — and step 3 of `docs/release-checklist.md` is the one documented
moment that produces the state deliberately.

## Is a skip a weakening of the no-real-identifiers rule

`CLAUDE.md` §*no real identifiers in examples or fixtures* notes that both
incidents that forced a history rewrite entered through it, so the question is
owed an answer a reader can check rather than an assurance.

**In the positive direction it is not a weakening, and it cannot be.** Today,
on a tree with one tracked file missing from disk, the two cases report
**nothing at all** about any file — the walk ends at the first missing path
and every file after it goes unread. A corpus of everything-but-the-missing-file
is strictly more than that. There is no tree on which the skip reports less
than the crash, which is what makes this a repair rather than a trade.

What the suite stops catching is one state and it is worth naming: a file
staged with a real domain in it and then removed from disk without staging the
removal carries that content in the INDEX, so a commit would ship it while the
sweep skips it. That state is reachable and it is unswept today as well,
because today the sweep crashes on the same tree. Closing it is Q1, not this
work's default.

**In the inverse direction a bare skip IS a hazard, and neither ticket says
so.** Two cases read the corpus to prove an entry is still ALIVE, and to those
a missing file and a deleted entry are the same evidence:

- `tests/test_no_document_names_the_old_roots.py#test_every_keep_entry_is_still_in_use`
  (`:142`) asserts every `KEEP` allowlist entry still occurs somewhere in the
  corpus. Skip the one file that carries an entry and the case reports that
  entry as dead and turns red.
- `tests/test_a_script_says_which_interpreter_it_needs.py:524` asserts that no
  `CLASSIFIED` file has stopped carrying the construct it was classified for.
  Skip a classified file and the case says the classification is of nothing.

Both are false alarms bought by the repair, and both are the direction
`seal/follow-up.md`'s first open row calls the one a checker of claims must not
fail in — a claim removed from the corpus without a word. **So the skip is
counted, and a case whose verdict depends on the corpus being whole says it is
not judging rather than judging wrongly.** In pytest's own vocabulary that is
`pytest.skip` with a reason naming the missing paths, which the release
runner reads in the count line as `… passed, N skipped` instead of a
traceback. That is #282's second option realised in the runner already in use,
and it is why the answer is not simply `os.path.exists`.

**The positive sweeps do not skip themselves.** They run on what remains and
report on it. A whole sweep that declines to judge at the moment a release is
about to be committed is the silent nothing the paragraph above refuses; a
sweep reporting on everything still on disk is the claim the rule is for.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CLAUDE.md` §*no real identifiers in examples or fixtures* | The rule these cases hold. The section above answers whether a skip weakens it, in both directions, and the answer is the shape of the repair |
| `CLAUDE.md` §*The goal a design is chosen against — verification that runs unattended* | A crash at a documented release step is a stop that needs a person. Every decision here is taken toward the run that does not stop |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | These cases are gates: the full suite decides whether a commit proceeds at step 3. The pull request body owes a test seen red, a stated failure direction, and a prompt budget. The direction is stated here: the change makes the gate **allow more** (a skipped path is unjudged), and that is the cheaper mistake because the state it allows reports nothing today |
| `agent-contract` §12 | The defect belongs to a class. Five helpers, seven call sites, and a case that re-enumerates the class so the sixth helper cannot be written without a guard |
| `agent-contract` §15 | Every case planted here is shown red before it is committed, and the handover says how. The fixture-repository shape phase 1 builds is what makes that possible for a `git ls-files` call |
| `agent-contract` §14 | A skip reason is text a person reads at a release and acts on. Each one is pinned by a case in the same commit |
| `agent-contract` §5 | Both ticket bodies' counts are claims. The reach table above replaces them; #432's *3736 passed* is carried unverified and settled by phase 1's baseline |
| `skills/implement/SKILL.md` §3, top rung | This alters what a check refuses and what a person reads at a release, so `spec.md` and `plan.md` are owed before the first edit. `routing.md`'s `Planning` row records that a framer drew them |
| `skills/verify/SKILL.md` — a check that cannot fail is a counterfeit seal | `tests/test_no_real_identifiers.py` has no can-fail case today, where three of its four siblings do. The guard it gains is a second thing that has to be shown able to fail |
| `CLAUDE.md` §*a change writes fragments, never the shared file* | `seal/specs/<id>/changelog.md` and `seal/ledger/<id>.md`. `seal/ledger.md` is touched only for the re-stamp named below |
| `CLAUDE.md` §*a ledger coordinate names content, never a position* | Rows this work adds carry `path#unit@hash` |
| `CLAUDE.md` §*a thing more than one party can have is named with whose* | More than one helper now skips. Any name this work introduces says whose corpus it is; `tests/test_one_word_one_meaning.py` is the check |
| `docs/review-chain-spec.md` §*The fix surface — `Contract changes` and `New units`* | Each helper gains a parameter so a fixture repository can exercise it. That narrows nothing and adds an argument, and the round record carries it |

## Scope

### In

1. **The instance, at its own coordinate.** `tests/test_no_real_identifiers.py#tracked_text_files`
   skips a listed path that is not on disk, counts what it skipped, and both
   callers at `:48` and `:64` keep judging what remains.
2. **The fixture shape the rest of the work copies.** The helper takes the
   repository root as an argument, so a case can build a repository with a
   tracked-and-deleted file and watch the guard work. `tests/test_the_pull_request_language_is_the_repositorys.py#test_the_templates_check_reads_prose_only_and_descends`
   is the precedent and states the reason: *a fixture git never sees would
   report nothing and the case would pass having exercised nothing.*
3. **The other four helpers**, from the reach table: `test_no_document_names_the_old_roots.py`,
   `test_release_hygiene.py`, `test_a_release_is_sized_by_a_criterion.py`,
   `test_a_script_says_which_interpreter_it_needs.py`.
4. **The inverse direction.** The two liveness assertions named above stop
   reading a skipped file as a deleted entry, and say so when they decline to
   judge.
5. **A case that re-enumerates the class.** No corpus built from a git path
   listing is opened from disk without a guard — enforced by a reader over
   `tests/*.py` rather than by a list somebody maintains. `tests/test_a_corrected_sentence_survives_elsewhere.py`'s
   `LISTS_PATHS` / `_derives_a_path_list` is the machinery this repository
   already wrote for finding path-listing git calls by scope.
6. **One sentence in `docs/release-checklist.md` step 3**, in the preamble that
   already says what that tree looks like — that the fold leaves tracked files
   the disk does not have, and that a non-zero skip count there is the
   expected reading rather than something to debug.
7. **The fragments and the closing memo** — `changelog.md`,
   `seal/ledger/1789687448-a-tracked-file-the-tree-deleted-stops-the-sweep.md`,
   `overview.md`, and the re-stamp of the shared rows this work drifts.

### Out, and why

| Left out | Why |
|---|---|
| A row in `docs/release-checklist.md`'s table of *what each check has caught at a release* | That table exists so a failure is recognised rather than debugged. After this work the failure cannot occur, so a row would teach a reader to recognise a state the tree cannot reach. What the reader WILL meet is the skip count, and that belongs in step 3's preamble beside the two sentences already describing that tree |
| Reading the INDEX for a path missing from disk | Q1. It closes the staged-then-removed hole and costs one more content source and a message saying which. The default is the skip, and the grounds are that the hole is unswept today too |
| Failing on a shrunken corpus | #282's third option, and it refuses itself: a deleted-unstaged file is a normal state mid-edit, so a case that fails on it fails on ordinary work |
| Adding `seal/ledger/` to an exclusion list | #282's *Not this*. The path is incidental; the fold is only what reached the state first |
| `tests/test_the_pull_request_language_is_the_repositorys.py#unreachable_templates`'s silent `except OSError: continue` | It guards, so it does not crash, and its silence was already argued at its own round 5. A different defect in the same neighbourhood; the phase 4 reader names it as guarded rather than repairing it |
| Every shipped script that walks `ls-tree` | Immune by construction — the content comes from git, by a rule `chain_check.py#read_record` states and a case holds |
| `tests/test_a_new_returnable_value_is_a_contract_change.py#tracked_python` | Already guarded. It gains nothing but the counted skip, and only if phase 4's reader asks for one |
| Any `seal/follow-up.md` row | See below |

### Whether a `seal/follow-up.md` row was waiting on this

**No row was, and all eleven were read on 2026-09-18.** Row 1 comes closest
and is the one this work cites: *the one direction a checker of claims must
not fail in*. It is about `evidence-check`'s `ANCHOR_RE` dropping a malformed
coordinate, which is a different checker and a different corpus; this work
neither supplies nor consumes it, and the row stays open. Row 5 names
`tests/test_a_script_says_which_interpreter_it_needs.py`'s subject — the
five scripts below the supported floor — and not its corpus builder, so
editing `shipped_python` neither closes nor blocks it. No row is deleted.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| The sweep survives a tracked file the tree deleted | Given a repository where a tracked text file has been removed from disk and the removal is not staged · When `test_only_neutral_domains` runs · Then it reads every remaining file and reports on them | A fixture repository built by the case, exit read directly (§1); and the same case red with the guard removed |
| The sweep still catches what it is for, on the same tree | Given that repository, with a real-looking domain in a file that IS on disk · When the sweep runs · Then it names that file and that line | The can-fail case `tests/test_no_real_identifiers.py` does not have today |
| Both cases in the module are repaired, not one | Given the same tree · When `test_only_fixture_user_paths` runs · Then it behaves the same way | One case per call site; §12 |
| The four sibling helpers behave the same | Given a deletion under each helper's own prefixes · When that module runs · Then it judges what remains | One fixture repository per helper, each case seen red against the unguarded helper |
| A skipped file does not read as a dead allowlist entry | Given the only file carrying a `KEEP` entry is missing from disk · When `test_every_keep_entry_is_still_in_use` runs · Then it declines to judge and names the missing path, rather than reporting the entry unused | The case seen red with the bare skip in place and no liveness guard |
| A skipped file does not read as a lost classification | Given a `CLASSIFIED` path is missing from disk · When `test_no_shipped_script_needs_more_than_the_floor_without_saying_so` runs · Then `gone` does not name it | The same shape, one module over |
| The shrink is visible in the runner's own output | Given any of the above · When the module runs under `-q` · Then the count line reports skipped cases with reasons naming the paths | Read the output of `bin/test -q <module>`; the reason text pinned by a case (§14) |
| A sixth helper cannot be written without a guard | Given a new `tests/*.py` scope that lists paths from git and opens one from disk · When the enumerating case runs · Then it names the scope and the call site | The case run against the tree at exit 0, and against a planted unguarded scope at exit 1 |
| The repository's own tree is unaffected when nothing is missing | Given a clean checkout · When the five modules run · Then the corpora are the sizes they are today and nothing is skipped | The vacuity assertions each module already carries — `len(files) > 30`, `len(paths) > 50`, `assert files` — kept and read |
| The release runner is told what a skip count means | Given step 3 is worked down straight after the fold · When the suite reports skipped cases · Then the checklist says that is the expected reading | Read `docs/release-checklist.md` step 3; a case is not owed, and none is claimed |

## Data & interfaces

Nothing on the wire and no schema. Three shapes change, and all three are read
by machines or by a person at a release:

- **Each helper's signature.** A repository-root argument with a default, so a
  fixture repository can exercise a `git ls-files` call. An added optional
  argument narrows nothing; `docs/review-chain-spec.md` §*The fix surface*
  is where the round record carries it.
- **What the suite reports.** Skipped cases with reasons, where there were
  passes or a traceback. `agent-contract` §14 applies to every reason string.
- **`docs/release-checklist.md` step 3's preamble.** One sentence. It must not
  name a version — `tests/test_release_hygiene.py#test_no_loaded_file_names_a_version_at_or_above_the_running_one`
  scans `docs/`.

**Ledger rows this work drifts, read from `seal/ledger.md` on 2026-09-18.**
Putting the guard inside each helper rather than at each call site is what
keeps this list to two, because no helper in the list below is itself
anchored:

| Anchor | Why it drifts |
|---|---|
| `tests/test_a_script_says_which_interpreter_it_needs.py#shipped_python@93cd0906` | the helper this work guards |
| `tests/test_a_script_says_which_interpreter_it_needs.py#test_no_shipped_script_needs_more_than_the_floor_without_saying_so@1a78a9a2` | the `gone` liveness assertion |
| `tests/test_no_document_names_the_old_roots.py#test_every_keep_entry_is_still_in_use@7e1cc02e` | the `KEEP` liveness assertion |

Re-reading and re-stamping them with `evidence-check --reverify` writes
`seal/ledger.md`, which `CLAUDE.md` otherwise reserves for a removal. That is
the established act rather than an exception: `seal/follow-up.md`'s ninth row
records a branch that drifted seven shared rows and whose fix pass re-stamped
them, and step 3 of the release checklist expects exactly that sequence. Rows
this work ADDS go in its own fragment.

`tests/test_no_real_identifiers.py` carries no ledger anchor at all today,
which is worth one row in the fragment rather than a finding.

**The three stamps above are refreshed to what those units hold after the
work,** because the records arm of `evidence-check` resolves a stamp in a live
work item as it resolves a ledger row, and a stamp naming content that moved
takes `--strict` to exit 2 — the reading `broad-gate` reports as NOT SEALED.
The refresh is bookkeeping and nothing else. What actually drifted, how far,
and on what grounds is the build's to state: `overview.md` §*Where spec and
implementation diverged* and `phases/phase-5.md` carry it.

## Open questions → questions.md

Four rows, and one of them is a person's. `questions.md` in this directory
carries them, and its head lists what the tickets left open that the tree
answered — so nobody reopens the two shape decisions above without reading why
they went the way they did.

<!-- The line below is the framer's mark. -->

Framed 2026-09-18 by framer, before the build.
