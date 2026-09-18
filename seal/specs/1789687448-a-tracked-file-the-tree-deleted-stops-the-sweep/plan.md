# Implementation Plan: a tracked file the tree deleted stops the sweep

<!-- seal/specs/1789687448-a-tracked-file-the-tree-deleted-stops-the-sweep/plan.md — HOW, in
phases. This is the Design Gate's artifact: where the work alters observable
behaviour, approval of this plan is the gate. -->

Approved 2026-09-18 by the repository owner's `automation` routing answer, when `smith` was spawned.

## Summary

Five helpers in this repository's own suite build a corpus from `git ls-files`
and open every path from disk. `git ls-files` lists the index, so a tracked
file the working tree has deleted is on the list and not on disk, and the walk
ends there with a `FileNotFoundError` — no file after it is read and the rule
the cases hold reports nothing.

The repair is a guard inside each helper, not at each call site, and it is
counted rather than silent. Two cases in the suite read the corpus to prove an
entry is still alive, and to those a skipped file and a deleted entry are
indistinguishable — so the skip has to be visible to them or it buys two false
alarms. The last phase leaves a reader behind so the sixth helper cannot be
written without a guard.

## Technical context

Coordinates read on 2026-09-18 at `f8cf32e5`. Nothing below was executed.

**The defect.** `tests/test_no_real_identifiers.py:30` builds the corpus,
`:48` and `:64` do `open(os.path.join(ROOT, rel))` with no existence check.
The same shape at `tests/test_no_document_names_the_old_roots.py:75` (opened
at `:97` and `:146`), `tests/test_release_hygiene.py:29` (`:491`),
`tests/test_a_release_is_sized_by_a_criterion.py:138` (`:236`, through
`read` at `:103`), and
`tests/test_a_script_says_which_interpreter_it_needs.py:483` (`:512`).

**The guard already in the tree.**
`tests/test_a_new_returnable_value_is_a_contract_change.py:96` —
`return [p for p in out if os.path.isfile(os.path.join(ROOT, p))]`. One line,
silent, and this work's positive direction is that line.

**The fixture shape.** A case about a `git ls-files` call needs a real
repository, and this suite has the precedent with the reason written down:
`tests/test_the_pull_request_language_is_the_repositorys.py#test_the_templates_check_reads_prose_only_and_descends`
— *a fixture git never sees would report nothing and the case would pass
having exercised nothing.* `tests/conftest.py#_build_repo` is the existing
builder, and `GIT_TEMPLATE_DIR` is already emptied there so a `git init` is
cheap.

**The class reader.** `tests/test_a_corrected_sentence_survives_elsewhere.py:716`
declares `LISTS_PATHS = {"--name-only", "ls-files", "ls-tree"}` and walks the
AST per scope in `_path_list_words` / `_derives_a_path_list`, counting call
sites rather than naming functions — with the reasoning for counting rather
than naming written into its docstrings. Phase 4 copies that reader and asks a
different question of it.

**What breaks in six months.** The guard is per helper, so a sixth helper
written without one is the defect again. That is what phase 4 exists for, and
phase 4 is itself the thing that can rot: an AST reader that stops matching a
call spelled a new way answers *no offender* and nobody hears. It is written
to fail toward naming a scope it cannot classify rather than toward silence,
and its own vacuity assertion — that it finds the five guarded helpers — is
what keeps it from passing on an empty read. The second risk is the skip
reasons: three of the repository's own review rounds have found a refusal
whose second half nothing pins, so each reason gets a case in the same commit
(`agent-contract` §14, and `seal/follow-up.md`'s seventh row is that omission
in an earlier release).

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| `os.path.exists` in each helper, silent, and nothing else | Two liveness cases read a skipped file as a deleted entry and go red on an ordinary mid-edit tree. The release runner trades a traceback for a red build one module over, and the cause is further from the symptom than it was | **Rejected.** It is both tickets' stated shape, and the tree contradicts it at `test_no_document_names_the_old_roots.py:142` and `test_a_script_says_which_interpreter_it_needs.py:524` |
| The guard at each of the seven call sites | The next call site is written without it — the defect has already reproduced once inside one module, which is why `tests/test_no_real_identifiers.py` has it twice. It also drifts more shared ledger rows: the call sites are anchored and three of the five helpers are not | **Rejected.** #432 names the helper for the first reason; the ledger is the second |
| Read the index for a missing path, via `git cat-file --batch` | The sweep then reports a violation in a file that is not on disk, and the message has to say which source it read. It closes the staged-then-removed hole, which no other shape does | **Deferred to Q1**, default off. Strictly stronger and strictly more surface; the hole it closes is unswept today as well, because today the sweep crashes on that tree |
| Read the index for every path, so the corpus is the index throughout | The sweep stops catching an unstaged edit that adds a real domain — which is most of what it catches, since it runs before `git add` at step 3 | **Rejected.** It trades the common catch for the contrived one |
| Fail on a shrunken corpus, naming the unreadable file | A deleted-unstaged file is a normal state mid-edit, so the case fails on ordinary work and gets deleted or worked around | **Rejected**, and #282 refuses it in its own words |
| Exclude `seal/ledger/` from the corpus | The fold is only what reached the state first. Every other prefix reaches it through a `git mv`, a `git rm --cached` or a half-applied patch | **Rejected**, and #282's *Not this* says so |
| Change `docs/release-checklist.md` to stage the deletions before step 3 | It is a rule a person has to remember, at a moment nobody is watching, in place of a repair. `CLAUDE.md`'s first goal decides between exactly this pair | **Rejected.** The checklist still gains the one sentence about the skip count, which is a reading aid rather than an instruction |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | The instance and the fixture shape: `tests/test_no_real_identifiers.py#tracked_text_files` takes a root, skips a listed path that is not on disk, counts the skip; both callers keep judging what remains. The module's first can-fail case, on a fixture repository with a tracked-and-deleted file and a real-looking domain in a file that is present | `bin/test -q tests/test_no_real_identifiers.py`, exit read directly (§1); each new case seen red against the unguarded helper and the reason recorded (§15); the module's baseline pass count recorded, which is also what settles Q4 | `195877f0` |
| 2 | The other four helpers, same guard, same fixture shape: `test_no_document_names_the_old_roots.py`, `test_release_hygiene.py`, `test_a_release_is_sized_by_a_criterion.py`, `test_a_script_says_which_interpreter_it_needs.py` — seven call sites closed in total | `bin/test -q` over the four modules in one command (§10); one red-first case per helper; the vacuity assertions each module already carries read at their present values | `c20ef824` |
| 3 | The inverse direction: `test_every_keep_entry_is_still_in_use` and the `gone` assertion decline to judge when the corpus shrank, and say which paths are missing. Q3 is answered here — every case in the five modules is read for whether its verdict depends on the corpus being whole | The two cases seen red with phase 1's bare skip and no liveness guard, then green; each skip reason pinned by a case in the same commit (§14) | `bb5a6c36` |
| 4 | The class reader: no scope in `tests/*.py` lists paths from git and opens one from disk without a guard. Modelled on `test_a_corrected_sentence_survives_elsewhere.py#_derives_a_path_list`, with the two already-guarded helpers and the fixture-repository helpers classified rather than exempted by name | The reader at exit 0 over the tree and exit 1 over a planted unguarded scope; a vacuity assertion that it finds the guarded helpers, seen red by emptying the corpus | `073fcb26` |
| 5 | The documents and the records: one sentence in `docs/release-checklist.md` step 3's preamble; `changelog.md`; `seal/ledger/1789687448-a-tracked-file-the-tree-deleted-stops-the-sweep.md`; the re-stamp of the three drifted shared rows; `overview.md` | `python3 skills/evidence-check/scripts/evidence_check.py --strict .` before and after the re-stamp, exit read directly; `docs/release-checklist.md` read for the version-naming rule | `1688010d` |

Phases 1 and 2 are one act at two reaches on purpose. Phase 1 establishes the
fixture shape all four of phase 2's cases copy, and it is the phase that can
still discover the shape is wrong while only one module has been edited.

## Operational impact

No migration, no new environment variable, no new dependency. One thing a
deployer must not miss, and it is about this repository's own workflow rather
than about the plugin:

- **The suite's output changes shape on a tree mid-edit.** Where it raised, it
  now reports skipped cases with reasons. Anyone reading a count line after a
  fold sees `… passed, N skipped` and should read the reasons rather than the
  number. Step 3 of `docs/release-checklist.md` says so, which is the whole of
  phase 5's document change.
- **Three rows of the shared `seal/ledger.md` are re-stamped.** That file is
  otherwise reserved for a removal, and the grounds are in `spec.md`
  §*Data & interfaces*.
