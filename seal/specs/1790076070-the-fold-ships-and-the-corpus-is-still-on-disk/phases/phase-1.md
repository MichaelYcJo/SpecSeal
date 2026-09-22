# 1790076070-the-fold-ships-and-the-corpus-is-still-on-disk — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | fbd5da56 |
| Ran by | smith on claude-opus-5[1m] |

## What this phase was asked

The floor inventory. Re-run `grep -rn "seal/specs" tests/`, classify every
reader, re-measure F1–F16 against the retire set rather than estimating them,
and write the answers here. The retire set is the **88 named directories**,
never "what the tool finds" — three sibling branches are adding new
`seal/specs/` directories while this one runs.

## What this phase found

### The retire set partitions the tree exactly

`./bin/settle` reports **83 work items in 38 segments, 16 ungrouped, 0
skipped**, which is `plan.md`'s destination map unchanged. The 88 to retire
are the 83 grouped plus the five ungrouped `spec.md`: `1788212517`,
`1788224363`, `1788449488`, `1788735085`, `1789540097`. The 12 kept are the
other 11 ungrouped plus this work item's own directory.

Checked by name, both ways: no directory on disk falls outside the two sets,
and no member of either set is missing from disk. That is the check
`spec.md` S4 and A2 name, taken before anything is written.

### The corpus, measured rather than carried over

| | at `6d410023` | in the worktree at `5cde6dc5` | after the planned fold |
|---|---|---|---|
| directories | 99 | 100 | 12 |
| files | 1,379 | 1,383 | 38 |
| `round-N.md` records | 263 | 263 | 7 |
| `rounds/round-*` files | 476 | 476 | 7 |
| bytes | — | 13,265,097 | 151,888 |

**The handoff's "100 directories, 1,381 files at `6d410023`" is two moments
in one sentence.** This work item's own directory did not exist at that
commit; the frame's four files landed in `e80dea72` and `5cde6dc5`. Neither
number changes a decision.

**"263 round records" is right, and 476 is a different population.** The
walk F1 and F2 take matches `round-\d+\.md` and finds 263. `rounds/` also
holds 213 sidecars — 132 `-report.md`, 39 `-fixes.md`, 39 `-asked.md`, 3
`-closing.md` — which F4's looser `round-[^/]*\.md` pattern picks up and
`committed_records` then filters back out by name.

**`1788184145-…` holds nine files, not the eight `spec.md` G3 and `plan.md`
both name.** The trade G3 describes is unaffected.

### The class, re-enumerated

`grep -rn "seal/specs" tests/` → **145 hits across 44 modules**, matching the
handoff. Narrowing to the readers that reach the *real* corpus — a
`seal/specs` path joined to `ROOT`, or a `git ls-tree HEAD -- seal/specs` —
gives **14 modules**, also matching. Derived independently here rather than
taken from the prompt, because a count is not a coordinate.

### F1–F16, re-measured

| # | Coordinate | Population now | After | Verdict |
|---|---|---|---|---|
| F1 | `test_chain_check_at_the_pull_request.py:2649` | 263 | 7 | red — repair |
| F2 | `test_chain_check_at_the_pull_request.py:2825` | 263 | 7 | red — repair |
| F3 | `test_chain_check_at_the_pull_request.py:2852` `assert carrying` | 34 carriers | **0** | red — repair |
| F4 | `test_a_finding_id_is_a_bare_integer.py:752` | 263 | 7 | red — repair |
| F5 | `test_a_finding_id_is_a_bare_integer.py:775` `parsed > 100` | 262 | 7 | red — repair |
| F6 | `test_a_finding_id_is_a_bare_integer.py:776` `assert teeth` | 95 | **4** | **green — decline** |
| F7 | `test_the_set_a_work_item_always_has.py:342` | 6 | **0** | red — repair |
| F8 | `test_the_set_a_work_item_always_has.py:347` | 8 | **0** | red — repair |
| F9 | `test_the_reopening_is_one.py:325` `REOPEN_FROM` = `1788597030` | present | **removed** | red — repair |
| F10 | `test_the_record_is_held_to_the_floor_and_the_depth.py:1250` `FLOOR_FROM` = `1788472135` | present | **removed** | red — repair |
| F11 | `test_a_finding_id_is_a_bare_integer.py:707` `assert paths` | 263 | 7 | green — decline |
| F12 | `test_the_reopening_is_one.py:537` `assert records` | 263 | 7 | green — decline |
| F13 | `test_release_hygiene.py:1346` | 100 | 12 | green — decline |
| F14 | `test_routing_is_recorded.py:499` | 100 | 12 | green — decline |
| F15 | `test_the_pull_request_language_is_the_repositorys.py:229` | 17 | 4 | green — decline |
| F16 | `test_unverified_rows_close.py:1897` `>= 90` | over `seal/ledger.md` | unchanged | green — decline |

**F6 is the one the frame got wrong, and the measurement is why.**
`questions.md` Q3 named a measurement as its instrument and planned for the
fixture. Over the 7 surviving records, `FINDING_ID_RE` refuses a cell in four
of them — `1788395377`'s rounds 1 to 4, carrying `🟢 0b`, `r1 🔴 1`, `r2 1`,
`r3 1b` and others. The teeth survive, so the answer is **decline** and no
fixture is written. One case that phase 2 does not have to touch.

**F3 has no survivor at all.** All 34 records carrying `| Fix range |` are in
the retire set, because the row is younger than every kept work item. So the
`assert carrying` half has to move to a record built in `tmp_path` while the
real-corpus sweep keeps the *no record fails* half — `spec.md`'s answer,
confirmed by measurement rather than assumed.

**F9 and F10 are the same shape.** Each asserts that a cutoff constant's work
item directory is in the tree, and both cutoffs name retire-set directories.
`unverified_check.folded_items` draws exactly the distinction the repair needs
— the directory exists **or** the top level of `docs/` carries its marker on
a live line — so the repair reads the fold record rather than lowering
anything.

### The no-floor readers cannot go red, and one is red already

Every reader in `spec.md`'s no-floor list asserts *no offender* over a
population: `test_this_repositorys_own_overviews_are_all_readable`,
`test_spec_directories_carry_the_timestamp_prefix`,
`test_every_spec_directory_that_reached_the_ladder_has_an_overview`,
`test_no_korean_pr_body_claims_a_close_that_did_not_happen`, the
round-records-at-top-level guard and the routing-placeholder sweep. A
shrinking corpus makes each one weaker, never false. None needs an answer
under `skills/settle/SKILL.md` §3, and saying so is the answer.

**One of them is red in the worktree right now, and the frame is what turned
it red.** `test_every_spec_directory_that_reached_the_ladder_has_an_overview`
names every directory holding a `spec.md` or a `plan.md` and no
`overview.md`, and `5cde6dc5` created exactly that: this work item's own
directory. Writing `overview.md` closes it, which this phase does. It is not
a floor and not the fold's doing — it is what the closing memo being owed
looks like from inside a check.

### What `--retire` will actually remove

`settle.py#retire` takes `marked & present & released_at_base` minus the
items an open `evidence-todo.md` row holds, and `settle` reports 0 skipped.
So writing 88 markers retires 88 directories, and the keep-list is enforced
by not writing those ids — never by editing the script (`spec.md` G2). The
marker `FOLD_MARKER` accepts is the whole line, `^<!-- specs/(\S+) -->$`, on
a line `live_lines` calls live, at the top level of `docs/` only.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none — this phase measures and writes records only | none |
