# 1791384160-a-fix-range-is-its-own-commits-across-a-merge — review round 5 report

Reviewer: specseal:warden on Opus 5.5. Target SHA
551efb7a8140ca078255b7698f8462c5559dfa72 (draft PR #878 into
`release/v0.21.0`, labelled `chain: reframed`). This is a verifying round.
Its target is round 4's fix diff `6445933a..76de29c3` (f2d7d9ab, 76de29c3),
plus a8dfbe63 (the fix table), d01d4016 (two `survivors.md` rows) and
551efb7a (the close).

## What this round was asked

Answer round 4's five verdicts, and judge round 4's one new unit,
`test_a_sentence_linking_the_home_uses_no_listed_word`, as code. No new
findings about derived wording beyond what the fixes themselves wrote. Run
the eight guard modules once.

Coordinates were carried from `rounds/round-4.md`, `round-4-report.md` and
`round-4-fixes.md` and opened where they pointed. No verdict was carried as a
conclusion.

## How the findings relate

All five of round 4's findings are closed, each by removing a claim, as the
orchestrator directed. Nothing opened here needs a fix.

What this round found comes from one change in the fix. The guard used to
read the four range readers' docstrings whole and checked that each one
existed. It now reads only the sentences that link the home. That narrowing
fixed round 4's ⬜ 3 and ⬜ 4, but it also dropped the only per-docstring
check:

1. The guard's docstring and ledger row 16 say each of the four docstrings
   reaches the word list through its own linking sentence. Nothing checks
   that a docstring keeps its link (⬜ 1).
2. Ledger row 16 now rests that claim on the linking case, and the row's
   anchors do not carry that case (⬜ 2, a correction to paperwork).

## Findings

### ⬜ 1 A docstring that drops its link leaves the guard, and nothing notices

Executed. `tests/test_the_range_rule_states_no_shape.py:12–15` now says every
carrier, "the docstrings of `own_commits`, `fragment_left_behind`,
`fix_pass_units` and `touched`", reaches the list "through its linking
sentence." Ledger row 16 repeats this as "(the four docstrings' among
them)." That is true at this SHA. All four docstrings contain the link, and I
listed every sentence `linking_sentences` yields.

Nothing keeps it true. `linking_sentences` asserts only that each file links
the home at least once, and both scripts link it more than once. Rule 17 of
`tests/test_the_rules_have_one_owner.py` needs `RANGE_OWNER` once per file.
That is the "§*…* owns" form, which `own_commits` carries and
`fragment_left_behind`'s "Which commits those are is §*…*;" does not. The
fix deleted the per-docstring case and its check that the four units exist
(the case name is NAME NOT IN TREE: test_a_reader_of_a_range_defines_no_shape).

I replaced `touched`'s link with "the rule (a sibling's squash made after the
fork is never owned)". The guard module and rule 17 stayed green, 69 passed.
The same edit to `own_commits` went red, because rule 17 catches that one.
`fragment_left_behind` and `fix_pass_units` sit where `touched` does
(`fragment_left_behind` by read).

This is ⬜ because the release ships true text. It costs a guard that the
module's own docstring overstates, and that is round 4's ⬜ 3 again, one
sentence over. The paste-ready case below passes at this SHA and goes red
when `touched` drops its link (executed).

### ⬜ 2 Ledger row 16 rests on the linking case and does not anchor it

Read. `seal/ledger/1791384160-a-fix-range-is-its-own-commits-across-a-merge.md:16`
says the guard refuses the listed words "in every sentence linking the home
(the four docstrings' among them)". Its anchors carry `SHAPE_WORDS`, the
home case and the list case, and not
`tests/test_the_range_rule_states_no_shape.py#test_a_sentence_linking_the_home_uses_no_listed_word`.
After the fix, that case is the one that reads the four docstrings. A change
to it would not show up as drift on this row. The row lacked this anchor
before the fix too, but the fix moved the weight onto that case.

This is the run's paperwork, so it is a correction and is not counted in
`Needs a fix`. Add the anchor, stamped the way `evidence-check` stamps it.

## Round 4's findings, answered

- **🟡 1, every reader of a range imports `own_commits`.** Closed. The
  clause is gone from `docs/the-record-layout.md:122–123` and nothing
  replaces it (read). No sentence anywhere in the tree outside the round
  records says "every reader of a range" (executed: `git grep`). Pasting the
  clause back turns nothing red (executed). That is expected, because the
  fix removed a claim and pinned nothing in its place.
- **⬜ 2, the gloss includes `a`.** Closed. The owner sentence now stops at
  "lists." in the home, in rule 17's pin and in ledger row 16 (read). With
  the gloss pasted back, rule 17 goes red (executed). Outside the round
  records, the gloss survives only in `spec.md`, which a `survivors.md` row
  excuses. `survivor-check` accepts that row (executed). The row's grounds
  rest on the framer owning `spec.md` (`agents/framer.md:29`, read).
- **⬜ 3, the guard's docstring claims more than a word list.** Closed. The
  docstring says it is a word list: other words pass it, and review is what
  keeps shapes out (read). The linking case was renamed to match. The home
  case keeps its old name, but its message was narrowed. What the docstring
  newly says about the four carriers is ⬜ 1 above.
- **⬜ 4, "gone from this clone once its branch merged".** Closed. The row at
  `skills/code-review/scripts/chain_check.py:4585` says "squashed away, or
  off the branch after a rebase" again (read). The guard reads only
  `fragment_left_behind`'s linking sentence, at `chain_check.py:4559–4561`,
  which does not contain the row. A listed word pasted into that sentence is
  red, and the same word outside a linking sentence passes, as the ledger
  row says (both executed). `phases/phase-6.md`'s correction matches.
- **⬜ 5, the shape clause in the fragment section.** Closed.
  `docs/the-record-layout.md:99–102` ends "and CI can name a commit a branch
  checkout does not" (read). Outside the round records, the clause survives
  only in `spec.md:170`, which `survivors.md` excuses (executed).

Round 4's ❓ asked whether `close` would list the test helpers under
`Contract changes`. `round-4.md` now reads `none` there (read).

## The new unit, judged as code

`test_a_sentence_linking_the_home_uses_no_listed_word` is the old linking
case, renamed, with a new assertion message. Its logic is unchanged. It was
seen red at this SHA (executed): "After a squash" pasted into
`fragment_left_behind`'s linking sentence fails it. The sentence split in
`linking_sentences` is coarse. In `round_record.py` it yields one span that
starts in a preceding table. That only makes the guard read more text, never
less, so it is not a finding. The case's one gap is the per-docstring check,
which is ⬜ 1.

## What the account claimed, and what I found

- **"🟡 1's clause dropped; ⬜ 5's clause dropped."** Confirmed by read and
  by `git grep`.
- **"⬜ 2 the owner sentence is the git command alone."** Confirmed. Home,
  rule 17 and ledger row 16 agree.
- **"⬜ 4 the guard narrowed to the home section and each docstring's linking
  sentence (a listed word elsewhere in a docstring now passes, by design)."**
  Confirmed by execution. It now passes in every docstring, and that is
  ⬜ 1.
- **"`spec.md`'s two framer sentences excused in `survivors.md`."**
  Confirmed. With the exemptions `survivor-check` exits 0. Without them it
  names exactly those two places.
- **"13 modules 602 passed; `evidence-check --strict`, `survivor-check`
  exit 0."** I did not rerun the smith's 13 modules. I ran the eight guard
  modules and both checkers, listed below.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | round 4's finding 1 is closed — the home's clause saying every reader of a range imports `own_commits` is gone, and nothing replaces it | `docs/the-record-layout.md:122` | confirmed | read: the section; executed: no tree sentence outside the round records says "every reader of a range"; pasting it back turns nothing red, which a removal needs no pin for |
| 🟢 | round 4's note 2 is closed — the owner sentence is the git command alone, in the home, rule 17's pin and ledger row 16 | `docs/the-record-layout.md:121` | confirmed | executed: the gloss pasted back turns rule 17 red; the gloss survives only in `spec.md`, excused in `survivors.md` and accepted by `survivor-check` |
| 🟢 | round 4's note 3 is closed — the guard's docstring says it is a word list that other words pass | `tests/test_the_range_rule_states_no_shape.py:17` | confirmed | read; what the docstring newly says about the four carriers is this round's note 1 |
| 🟢 | round 4's note 4 is closed — the silent-state row says "squashed away" again, outside the guard's reading | `skills/code-review/scripts/chain_check.py:4585` | confirmed | executed: a listed word in `fragment_left_behind`'s linking sentence is red, and outside it passes |
| 🟢 | round 4's note 5 is closed — the fragment section's input sentence carries no shape clause | `docs/the-record-layout.md:100` | confirmed | read; the clause survives only in `spec.md:170`, excused and accepted by `survivor-check` |
| ⬜ 1 | The guard's docstring and ledger row 16 say each of the four range readers' docstrings reaches the list through its linking sentence; nothing checks that a docstring keeps its link, and `touched` dropping it leaves the guard and rule 17 green | `tests/test_the_range_rule_states_no_shape.py:12` | open | executed: `touched`'s link replaced by a shape sentence, 69 passed; the paste-ready case passes at the target and is red under that edit |
| ⬜ 2 | Ledger row 16 rests "every sentence linking the home (the four docstrings' among them)" on the linking case and does not anchor it | `seal/ledger/1791384160-a-fix-range-is-its-own-commits-across-a-merge.md:16` | open | read: the anchors carry `SHAPE_WORDS`, the home case, the list case and `RULES`; a correction to the run's paperwork, not counted in Needs a fix |

## Executed probes

| What was run | Result |
|---|---|
| a `--no-local` clone of the worktree at the target, in the round's scratch directory | HEAD 551efb7a8140ca078255b7698f8462c5559dfa72 |
| `bin/test` over the eight guard modules the spawn named, in the clone | exit 0; 435 passed |
| every sentence `linking_sentences` yields, and whether each of the four docstrings contains the link | 8 sentences; all four docstrings link; `fragment_left_behind`'s whole docstring holds "squash" outside its linking sentence |
| `test_tmp_round5.py` in the round's scratch directory, run once and deleted — NAME NOT IN TREE | exit 0; results in the rows below; the clone clean after each restore |
| baseline, the guard module | exit 0; 3 passed |
| "After a squash" in `fragment_left_behind`'s linking sentence, the guard module | exit 1; 1 failed |
| "A sibling's units are a fork's." at the head of `touched`'s docstring, outside its linking sentence | exit 0; 3 passed |
| `touched`'s link replaced by a shape sentence, the guard module and rule 17's module | exit 0; 69 passed |
| `own_commits`'s link replaced by a shape sentence, the same two modules | exit 1; 1 failed |
| round 4's 🟡 1 clause pasted back into the home, the same two modules | exit 0; 69 passed |
| round 4's ⬜ 2 gloss pasted back after "lists", rule 17's module | exit 1; 1 failed |
| ⬜ 1's paste-ready case added to the guard module, then `touched`'s link removed, in a `python3 -` script | exit 0, 4 passed; then exit 1, 1 failed |
| `git grep` for the five removed phrases outside the round records | the gloss and the ⬜ 5 clause only in `spec.md` and `survivors.md`; "squashed away" in the restored row; "gone from this clone" only in `phases/phase-6.md`'s record of the rewording |
| `bin/evidence-check --strict` in the clone | exit 0 |
| `bin/survivor-check --range 6445933a..551efb7a --exempt` the item's `survivors.md` | exit 0; 2 excused, both `spec.md` |
| the same without `--exempt` | names `spec.md:70` and `spec.md:170`, the two places the rows excuse |
| `round-record new` over this report, in the clone only, its output discarded | exit 0; all three tables and both lines parsed; the fragment notice names `f2d7d9a`, and the item's `changelog.md` carries none of the five removed phrases (read), so it needs no change |
| `gh pr checks 878`, read twice, the last after this report was written | head 551efb7a: 5 pass (release, lint, ledger, both arm-check-grammar legs), 8 pending (every pytest leg), none failed |
| broad gate (full suite, repository lint, typecheck) | not yet — the sealer's, after the rounds settle; never run in this round |

## Paste-ready fixes

### ⬜ 1 — `tests/test_the_range_rule_states_no_shape.py`, a case per carrier

Add `import ast` to the imports, and this case after the linking case:

```python
# The units whose docstrings carry the rule, by file: each reaches the list
# only through its linking sentence, so each must keep one.
CARRIERS = {
    "chain_check.py": ("own_commits", "fragment_left_behind"),
    "round_record.py": ("fix_pass_units", "touched"),
}


def test_each_reader_of_a_range_keeps_its_linking_sentence():
    missing = []
    for name, units in CARRIERS.items():
        module = ast.parse(read(os.path.join(SCRIPTS, name)))
        found = {
            node.name: flat(ast.get_docstring(node) or "")
            for node in module.body
            if isinstance(node, ast.FunctionDef) and node.name in units
        }
        missing += [f"{name}#{u}" for u in units if LINK not in found.get(u, "")]
    assert not missing, (
        "a docstring of a unit that reads a range no longer links the home, "
        f"so the list no longer reads it ({LINK}): " + ", ".join(missing)
    )
```

### ⬜ 2 — ledger row 16's anchors

```text
`tests/test_the_range_rule_states_no_shape.py#test_a_sentence_linking_the_home_uses_no_listed_word@<stamp>`
```

Add it beside the home case's anchor, with the stamp `evidence-check` computes.

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

## Regression tests to plant

- ⬜ 1's case, in `tests/test_the_range_rule_states_no_shape.py`. Show it red
  by removing one docstring's link, as the probe above did.

## Facts for the evidence ledger

- Row 16: the guard reads a docstring only through its linking sentence. A
  listed word elsewhere in a docstring passes by design (executed this
  round). With ⬜ 1's case planted, the row can say each of the four
  docstrings is held to keep its link, and anchor that case and the linking
  case.

## Broad gate

`not yet`. Nothing this round opened needs a fix, and both findings are ⬜.
Once the orchestrator closes this round, the sealer's spawn comes due.

Needs a fix: no
Loses a record or crashes: no

## Proof — files opened

- `seal/specs/1791384160-a-fix-range-is-its-own-commits-across-a-merge/rounds/round-4.md`,
  `round-4-report.md`, `round-4-fixes.md`
- the diff `6445933a..551efb7a`: `docs/the-record-layout.md`,
  `skills/code-review/scripts/chain_check.py`,
  `tests/test_the_range_rule_states_no_shape.py`,
  `tests/test_the_rules_have_one_owner.py`, the item's `phases/phase-6.md`,
  `survivors.md` and its ledger fragment
- `tests/test_the_range_rule_states_no_shape.py`, whole
- `tests/test_the_rules_have_one_owner.py` (lines 300–380, and `RANGE_OWNER`)
- `docs/the-record-layout.md:96–135`
- `skills/code-review/scripts/chain_check.py:4555–4592`
- `seal/specs/1791384160-a-fix-range-is-its-own-commits-across-a-merge/survivors.md:1–40`
- `seal/ledger/1791384160-a-fix-range-is-its-own-commits-across-a-merge.md:16`
- `agents/framer.md:29`
