# 1790138190-settle-leaves-twelve-directories-with-no-way-out — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | eeab8b4 |
| Ran by | unknown — the spawn prompt named the agent (`smith`) and not the model, and the value is the spawning session's to give |

## What this phase was asked

The CI readers ask the same predicate. `unverified_check.py --baseline`
names a rule retirement apart from a fold and still refuses an open row or a
base `spec.md`; `chain_check.py --baseline` prints `retired:` for it;
`survivor_check.py` drops a retired directory's paths — either arm — from
both sides of the range. `docs/review-chain-spec.md` §*The declaration, and
where the check went instead*, `survivor_check.py`'s own §*A deletion is one
row* docstring and the two readers' help text say so. Verified by A6–A8 as
cases in `tests/test_unverified_rows_close.py`,
`tests/test_chain_check_at_the_pull_request.py`,
`tests/test_a_corrected_sentence_survives_elsewhere.py`, each seen red
first; a case that each reader calls the one predicate; A9 on a scratch
clone — `settle --retire` committed there, then the three readers against
its parent, every exit code read directly, the clone deleted.

## What this phase found

**Red first, per reader** (executed at `7cf44f4` with the cases added and the
readers untouched): unverified `2 failed, 3 passed`; chain `1 failed, 2
passed`; survivor `1 failed, 2 passed` — the last only after the fixture was
rebuilt twice (below). The passing ones are controls whose refusal already
held (an open row at the base, a spec at the base, a memo removed from a
directory that stays, a sentence corrected in `docs/` in the same range, a
spec-less directory with an open row); each earned its red from a mutation.

**The survivor fixture was vacuous twice, and a run of the unfixed code is
what showed it.** First, the marker was written into the same paragraph as
the standing sentence, which made that sentence "written" wording and it
cancelled itself. Second, a verbatim copy is one shared run and a run scores
at most 1.0 against the 1.6 floor, so a verbatim survivor can never be
reported — by design, `survivor_check.py#weigh` scores the rarest n-gram per
run. The fixture's `docs/` copies are therefore restated with one word
changed, which is also what a fold's standing prose looks like, over a pool
of fourteen files. Only then did the case go red against the unfixed sweep.

**A reader's removal is the whole directory.** Each CI reader asks the
predicate only when the directory is gone at `HEAD` (or at `b`): a memo, a
declaration or an edited file removed from a spec-less directory that stays
is not a retirement. Two mutations dropping that condition survived the
first pass — chain and survivor — and two cases closed them
(`6765abd`); unverified's was red from the start.

**An existing case changed its fixture, not its assertion.**
`test_a_deleted_declaration_with_no_marker_is_still_refused` built a
directory with a `routing.md` and a round record and no `spec.md`. Under D3
that directory IS retired by the rule, so the case went red; the fixture now
writes a `spec.md`, which is what the marker arm's work item always had, and
the refusal it pins is unchanged. That is G6's accepted direction — a hand
deletion of a spec-less directory with nothing open now passes.

**`tree_at` became public on the reader** so `survivor_check.py` can ask
whether a directory is gone at `b` without a new `ls-tree` call site of its
own, which `test_every_path_list_this_module_derives_from_git_is_filtered_or_named`
holds at a fixed count per function.

**A9, on a scratch clone of `2a6c406`** (executed, driven from python; clone
under the scratchpad, deleted at the end — `clone deleted: True`),
`--released-at 1bafeb7`, this repository's `origin/main`:

| Run | Exit | What it printed |
|---|---|---|
| `settle --retire` | 1 | removed exactly `1788217118`, `1788220055`, `1788276387`, `1788425222`, `1788824000`, `1788938400`, `1789024700`, `1789053786`, each *(no `spec.md` — retired by the rule, with no marker)*; kept `1788177600` and `1788395377` with their four rows; `retired 8 work items; 2 kept`. Left: `1788177600`, `1788184145`, `1788395377`, `1790119502`, `1790134781`, `1790138190` |
| `unverified_check.py --baseline HEAD^ seal/specs/` | 0 | `6 overviews · 10 open · 2 closed · 0 unreadable · 1 retired by the rule` — `1788276387` is the one of the eight with an overview |
| `chain_check.py --baseline HEAD^` | 0 | eight `retired: by the rule — …` notices, one per removed `routing.md` |
| `survivor_check.py --range HEAD^..HEAD` | 0 | `examined 340 files …, against 0 sentence(s) the range … removed` |

**Mutations** (executed, each restored from saved bytes): unverified —
predicate not asked, directory-gone not asked, arm never taken: all red;
chain — predicate not asked, arm never taken: red, directory-gone not asked:
green, then red after `6765abd`; survivor — nothing retired: red, gone-at-`b`
not asked: green, then red after `6765abd`.

**Slice** (executed on `eeab8b4`): the three reader modules, the settle
module and `tests/test_docs_line_wrap.py` — `445 passed`. `ruff check` and
`ruff format --check` clean on every changed `.py`.

**Rows.** `seal/ledger.md`'s *A `routing.md` this pull request RETIRED …*
(`1790076070`) **corrected**: its clause said the marker is *the only thing*
that tells a retirement from a deletion. Re-read and re-verified: rows on
`chain_check.py#main` (×3), `unverified_check.py#main` (×3),
`survivor_check.py#corrected` (×2), and the review-chain-spec opt-in heading
row. **The ledger anchors into itself once**:
`seal/ledger.md#"### 1788331011-two-roots-hold-three-lifetimes"` moved
because two re-read notes landed in that section, and a single `--reverify`
pass hashed it before rewriting them; a second pass converged. That row is
re-read too. `evidence-check --strict .` exit 0.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `seal/ledger.md`'s clause *the marker is the only thing that can tell a retirement from a deletion* — made false by the rule arm | the same row, corrected with a dated note |
| the premise that a fold owes the survivor sweep a range row — the sweep no longer reports a retired directory | `survivor_check.py`'s docstring §*A retirement is out of the range, so a fold owes no row*; `skills/settle/SKILL.md` loses the row in phase 6 |
