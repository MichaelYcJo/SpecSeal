# 1790138190-settle-leaves-twelve-directories-with-no-way-out — phase 5

| Field | Value |
|---|---|
| Phase | 5 |
| Commit | be1579e |
| Ran by | unknown — the spawn prompt named the agent (`smith`) and not the model, and the value is the spawning session's to give |

## What this phase was asked

An empty root is green. `settle` and `settle --retire` exit 0 with a
sentence on an empty or absent `seal/specs/` under a present root;
`unverified_check.py` does the same for that root's `specs` path and still
refuses any other missing path; every floor in `spec.md` G8 answered by
`skills/settle/SKILL.md` §3 — an independent listing that holds at any size,
or its property moved into a corpus built in `tmp_path` — and none lowered.
Verified by A10 on a scratch clone with every directory under `seal/specs/`
removed and committed: the G8 modules, `settle`, `settle --retire` and
`unverified_check.py --baseline <parent> seal/specs/`; the same modules on
this branch's tree; each re-pointed floor shown red with its defect planted
(A11); clone deleted.

## What this phase found

**Red first** (executed at `3103415`, cases added, readers untouched):
`settle` `4 failed` (report and retire, over an empty and an absent root);
`unverified_check.py` `4 failed` (with and without `--baseline`, empty and
absent); the two *any other missing path is still a typo* cases green — they
are the controls that keep the settled path from becoming a way past.

**Each floor's answer** (Q5), and the defect planted to see it red (executed,
each restored from saved bytes; the loose directory planted and removed):

| Floor | Answer | Planted defect → red |
|---|---|---|
| F1–F2 `_the_walk_found_every_committed_record`'s `assert listed` | independent listing: `conftest.committed_round_records_on_disk` (a disk walk plus `git cat-file -e` per file) has to find nothing the listing lacks; the guard takes a `root`, and `test_the_walk_guard_names_what_either_route_missed` runs both directions over a built corpus | the chain module's `RECORD_PATH_RE` matching nothing; the guard's listing half removed |
| F3 `test_this_repositorys_own_round_records_pass_the_per_record_checks`'s `assert records` | the same independent listing | `RECORD_PATH_RE` matching nothing |
| F4 `_the_corpus_covers_every_work_item_that_has_rounds`'s `assert with_rounds` and its `os.listdir` | the existing disk-against-listing comparison stays, guarded for an absent root; the helper returns what it saw and the built-corpus case asserts it saw the item | the helper returning `set()` |
| F5 `test_the_corpus_is_records_only`'s `assert paths` | independent listing on the real tree; the shape moves to `test_the_filter_keeps_a_record_and_drops_its_three_siblings`, over a built `rounds/` | the filter taking everything |
| F6 `assert teeth` | a `tmp_path` corpus: `test_the_census_has_teeth_over_a_corpus_it_builds`, one record whose id is `R2-1` | the census never counting a refusal |
| F11 `assert parsed` | kept in the form that holds at any size, `parsed or not paths`, with every unparsed record still named; the loop is `_census`, shared with the built corpus | `id_cells` never parsing |
| F12 `test_this_repositorys_own_records_are_not_refused_by_the_reopening_walk`'s `assert records` | independent listing | the reopening module's `RECORD_PATH_RE` matching nothing |
| F13 `assert items` and its `os.listdir` | stronger at any size: where `seal/specs/` exists, every entry carries a `routing.md`; absent is the laid-out state, as `seal/ledger/` already is | a directory with no `routing.md` planted under `seal/specs/` |
| F14 `assert found` and `assert sum(omitted.values())` | a second listing by `os.listdir` has to equal the glob; the omitted-row property moves to `test_an_absent_optional_row_reads_as_nothing_over_a_built_declaration` | the glob matching nothing; an omitted row never counted |
| F15 `assert mirrors` | a second listing has to equal the glob; the naming rule's teeth move to `test_a_mirror_named_for_a_country_is_refused_by_the_same_rule` via `unknown_mirrors` | the glob matching nothing; the rule refusing nothing |
| F17 three `os.listdir(specs)` | guarded for an absent directory, which holds no offender | the pre-phase clone below |

No literal was made smaller and no comparison against a literal removed
(A11, read from the diff): the nine non-empty assertions that went —
`listed`, `records` (×2), `with_rounds`, `paths`, `found`, `mirrors`,
`teeth`, `sum(omitted)` — were each a floor of one, and each is replaced by
the listing or the built corpus in the table.

**A10 and Q4, on two scratch clones** (executed, driven from python; four
clones made and all deleted — `clones deleted: True` each time). Every
directory under `seal/specs/` removed and committed; the tree that ran it
keeps an empty `seal/specs/`, and a fresh clone of the commit has none. Then
a second commit, *the next pull request*, based on the emptied one.

| | at `3103415` (before) | at `be1579e` (this phase) |
|---|---|---|
| `settle` / `settle --retire`, empty dir | exit 0 / 0 (zeros; *The fold is complete.*) | exit 0 / 0, *holds no work item … A complete fold ends here* |
| `settle` / `settle --retire`, absent (fresh) | **exit 2 / 2**, *has no seal/specs/* | exit 0 / 0 |
| `unverified_check.py --baseline <emptied> seal/specs/`, empty / absent | **exit 2** *no overview.md found* / **exit 2** *no such path* | exit 0 / 0, *holds no work item and its `seal/` root is there* |
| `chain_check.py --baseline <emptied>` | 0 / 0 | 0 / 0 |
| `survivor_check.py --range <emptied>..HEAD` | 0 / 0 | 0 / 0 |
| the 44 `test_*.py` modules naming `seal/specs`, empty / absent | **exit 1: 10 / 13 failed** | **exit 0 / 0** |

The thirteen at `3103415` on the absent tree are G8's F1–F3 (three cases),
F4–F6 and F11 (two cases), F12, F13, F14, F15, F17 (three cases) — and one G8
did not list: **`tests/test_unverified_rows_close.py::test_this_repositorys_own_overviews_are_all_readable`**,
which runs `unverified_check.py seal/specs/` on the real tree and asserts 0.
That is Q4's answer: G8 was one short, and the missing reader needed no
edit of its own — it is green at `be1579e` because the reader it runs learned
the settled state, which is the answer `plan.md` §*Alternatives* gave for the
workflow step.

**Against the removal's own parent, all three readers refuse, and that is
right.** The probe removed every directory by hand, including four the rule
cannot retire — `1788184145`, `1790119502` and this one hold a `spec.md` with
no marker, `1790134781` has open rows — so `unverified_check.py`,
`chain_check.py` and `survivor_check.py` each exit 1 on that commit, at both
`3103415` and `be1579e`. A10's sentence expected exit 0 there; that is the
divergence recorded in `overview.md`. The state a complete fold reaches is
the next pull request's, and that is green.

**On this branch's tree** (executed on `be1579e`): the G8 modules plus
`tests/test_a_shrunken_corpus_declines_to_judge.py`, the settle and
unverified modules and `tests/test_docs_line_wrap.py` — `801 passed, 1
skipped`; the skip is `test_the_whole_check_names_no_earlier_items_record`
(`origin/release/v0.8.1 is not fetched here`), which predates this work. The
new helper adds no path-listing scope, so the shrunken-corpus guard is green
without a new classification.

**Rows** re-read and re-verified: S1 of the root move (`one_root_laid_out`),
`unverified_check.py#main` (×3, the local-mode S7 among them — `settled_root`
requires `<repo>/seal/` to exist, so local mode still exits 2 there), the
mirror rows (×3), the row *F12 · the separator's limit is the third of three*, R1 of the finding-id
rows, R1 and R2 on `settle.py#main`. The ledger's self-anchor on
`### 1788331011` moved again with them and converged on the second pass.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| nine non-empty assertions over the real corpus: `listed`, `records` (×2), `with_rounds`, `paths`, `found`, `sum(omitted)`, `mirrors`, `teeth` | the independent listing `conftest.committed_round_records_on_disk` or a second listing in the same case, and four cases over built corpora, per the table above |
| `settle`'s exit 2 *has no seal/specs/ — nothing was read* for a present root | exit 0, `settle.py#SETTLED`; a repository with no root at either place still exits 2 |
