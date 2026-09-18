# 1789687448-a-tracked-file-the-tree-deleted-stops-the-sweep — overview

📋 implement applied
· spec:     `spec.md`, `plan.md`, `questions.md`, `routing.md` of this work item · `CLAUDE.md` §*no real identifiers in examples or fixtures*, §*a change writes fragments, never the shared file*, §*a ledger coordinate names content, never a position*, §*a thing more than one party can have is named with whose*, §*The goal a design is chosen against* · `CONTRIBUTING.md` §*What a change to a gate must carry* · `seal/follow-up.md`, all rows · `docs/release-checklist.md` steps 2 and 3 · `skills/agent-contract/SKILL.md` §§1, 5, 7, 8, 9, 12, 14, 15 · `skills/implement/SKILL.md` §§1–4
· evidence: `seal/ledger/1789687448-a-tracked-file-the-tree-deleted-stops-the-sweep.md` — 5 rows added; 3 rows of `seal/ledger.md` re-stamped
· verified: see `## Not verified` below and each `phases/phase-N.md`

## Why this work exists

`git ls-files` lists the index, so a tracked file the working tree has deleted
stopped five of this suite's sweeps at the first missing path and every file
after it went unread — at the one documented moment, step 3 of a release, that
produces that tree on purpose.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| What a reader sees after a fold | `plan.md` §*Operational impact*: *Anyone reading a count line after a fold sees `… passed, N skipped` and should read the reasons rather than the number* | The checklist sentence says what was measured: a fold produces **no** skipped case, and a skipped case appears on a different deletion | Executed 2026-09-18. The fold's missing path is under `seal/ledger/`, which only `tests/test_no_real_identifiers.py#tracked_text_files` has in its corpus — the other four exclude `seal/` by their own prefix lists — and both of that helper's callers are positive sweeps that judge what remains. On the tree a fold leaves, the six modules print `84 passed` at exit 0. `phases/phase-3.md` carries the three readings |
| How far the class reaches | `spec.md` §*The reach, enumerated from the tree*: five helpers, seven opening call sites | Six helpers, eight opening call sites | The frame enumerated by grepping `git ls-files`. Phase 4's reader, which also matches `ls-tree` and `--name-only`, found `tests/test_a_finding_id_is_a_bare_integer.py#committed_records` — listing from `ls-tree HEAD` and taking its content from the working tree, as its own docstring states. §12 asks for the class rather than the coordinate, so it is guarded in phase 4's commit |
| How many cases read the corpus to prove something is alive | `spec.md` §*Is a skip a weakening*: two, at `test_no_document_names_the_old_roots.py:142` and `test_a_script_says_which_interpreter_it_needs.py:524` | Three. `test_no_document_names_the_old_roots.py#test_the_scan_covers_something` is the third | Q3 asked the work to read every case in the five modules and repair a third in the phase that found it. The case asserts two named paths are in the corpus, and `skills/implement/SKILL.md` leaving through an unstaged `git mv` makes it report lost coverage for a file that is merely somewhere else |
| Where the guard lives | `plan.md` phase 1: *a guard inside each helper* | The predicate is one shared function, `tests/conftest.py#on_disk`; each helper gains the `root` argument and calls it | Five copies of `os.path.isfile` is the same defect five times over, and §12 asks for the class rather than the instance. The helper is still the home in the sense the plan meant — the call sites gained nothing |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and the typecheck. `agent-contract` §2 keeps all three off an implementer; only the six modules this work touches were run, plus `uvx ruff check tests/` and `uvx ruff format --check tests/` | `specseal:sealer`, spawned by the orchestrator after the review rounds settle |
| #432's *staging the deletions makes the same tree green — 3736 passed*. The module baselines were measured (Q4) and the suite-wide total was not | `specseal:sealer`'s broad run |
| Whether `pytest.skip`'s reason renders in full in the release runner's `-q` output, or is truncated. The reason's TEXT is pinned by four cases; what a person actually sees in the terminal at step 3 is not | the repository owner, at the next release |

## Not done

**Q1 stays at its default and the branch builds the default.** A path missing
from disk is skipped rather than having its index content swept. The
staged-then-removed state — a file `git add`-ed with a real domain and then
removed from disk without staging the removal — is unswept after this work, as
it is unswept today. `questions.md` Q1 carries the trade and it is a person's
row, not a measurement.

**`tests/test_the_pull_request_language_is_the_repositorys.py#unreachable_templates`
keeps its silent `try/except OSError: continue`.** It guards, so it does not
crash, and its silence was argued at its own round 5. `spec.md` puts it out of
scope and phase 4's reader classifies it as guarded rather than repairing it.

**A `SyntaxWarning` at `tests/test_a_row_points_by_content.py:763` is left
standing.** That line carries a string escape python does not know, and
parsing the file raises it. It predates this branch — executed with this work
stashed, `bin/test -q tests/test_a_new_returnable_value_is_a_contract_change.py`
emits it at exit 0 — and it is a fact about a docstring rather than about a
git listing, so it is outside this work's scope. Phase 4's reader catches it
at its own `ast.parse` so it does not become a second source. It is one
character to fix and it belongs to whoever opens that file next.

**No `seal/follow-up.md` row was deleted.** All eleven were read on
2026-09-18; the framer's reading was re-checked and holds. Row 1 is the one
this work cites for its error direction and is about a different checker and a
different corpus.

## Fed back into the spec

Two clauses, both inferred during implementation and both overturnable:

- **A case whose verdict needs the whole corpus declines only when it has a
  finding.** `spec.md` says such a case declines; it does not say when. The
  rule the three call sites follow is *compute the finding; if there is one,
  decline over the missing paths; otherwise judge* — because a skip can only
  make an entry look unused, never used, so a run that finds everything in
  place has reached the right verdict whatever it skipped. Declining
  unconditionally would turn the check off on any mid-edit tree.
- **A vacuity floor does not decline.** `len(files) > 30` is what stops a
  sweep passing on an empty read, so it is the wrong half to turn off at the
  moment the corpus is actually short. Only the named-path half of
  `test_the_scan_covers_something` declines.
