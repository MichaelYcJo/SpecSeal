# 1790550713-what-the-0.15.5-rounds-deferred — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 48c36b1 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

Close #626. Re-run `spec.md`'s glued-rule enumeration first. Rewrite
`refused_coordinate`'s third bullet so it states that the `@` comes after its
`#`. It must stay true of `@alice#299@abcdef12`, which is named (S2), and it
names `@alice#299` among the silent shapes. Put the same condition into
1790381328's `spec.md` trade list, with a dated note naming this work item and
#626. Keep the framer's decision that `CHANGELOG.md` §0.15.5 and 1790381328's
gathered fragment are not rewritten.

Restore `docs/a.md#1.2`, `src/a.py#1>"x"` and `Makefile#1x` to `GIVEN_UP` and
add `@alice#299`. Pin the two named examples, `docs/a.md#1장@abcdef12` and
`src/a.py#handler @abcdef12`, in `TAKEN_UP` or in a sibling dict, depending
on what a ledger run prints for them (Q1). Stop the comment and the case
docstrings from saying "one or two" and "the verdicts #614 moved". Add one
completeness case, and see it red by removing a parameter before trusting it
green. Re-read and re-stamp S8–S12 and the `MALFORMED` row, and write two new
rows in the fragment.

## What this phase found

- **The glued-rule enumeration matched `spec.md`'s table.** A `git grep` for
  *glued*, *both marks*, `` `@` follows ``, `` `@` after a `#` `` and
  `@lru_cache  # memoized`, rounds excluded, turned up the same copies and no
  new one (executed 2026-09-28).
- **Q1: both named examples print `MALFORMED <shape>  `.** A ledger run with
  each shape in a code span beside a good anchor printed that, at exit 1
  (executed). So both went into `TAKEN_UP` and no sibling dict was needed.
  `TAKEN_UP`'s case now holds more than the dotless openers, so it was renamed
  `test_what_the_rules_still_name_is_named_and_says_so`. S8–S12, the only row
  that cited it, now cites the new name.
- **S2: `refused_coordinate("@alice#299@abcdef12")` is True**, and
  `@alice#299` and `@types/node#1` are False (executed). The bullet says an
  `@` before a `#` is not glued to it, and that `@alice#299@abcdef12` is named
  by the `@` that follows its `#`. It does not say that an `@` before the `#`
  makes the text silent. That shape is pinned in `TAKEN_UP` too.
- **The completeness case found nine missing shapes, not five.** Against the
  dicts as they stood at `0e475b1` it was red and named `chart.js@4`,
  `org/repo#299's`, `@lru_cache  # memoized` and `Makefile#"all: build"`
  beside the frame's five. `spec.md` §*Scope* placed those four in the
  docstring's first paragraph only. They are also examples inside the rules
  section, where the case reads. Older cases already hold their verdicts, so
  they were added to the dicts under their rules rather than excluded from the
  case. The dicts now hold all 21 examples of the section: 13 silent and 8
  named. A lone `` `#` `` or `` `@` `` in the section is notation and the case
  skips it.
- **Two named examples are each named by two branches.** Seen by mutation,
  one at a time, restored from bytes kept before the loop:
  - `docs/a.md#1장@abcdef12` stays named with `GLUED_MARKS_RE` not searched,
    because the path-hash branch names `docs/a.md#1장` followed by `@abcdef12`.
    It goes red only with both branches off.
  - `src/a.py#handler @abcdef12` stays named with the per-word path test off,
    because the dotless-name test also takes `y#h`. It goes red only with both
    off.

  So S4's "the named branch it relies on disabled" needed two branches for
  each shape. The case's docstring now says which branches name which shape.
- **The rest of the mutation record** (executed, each mutant applied alone
  over the whole of `tests/test_a_row_points_by_content.py`):
  - round 3's three mutants each turn only their own restored parameter red:
    `isalnum` gives `Makefile#1x`, `.` in the lookahead gives `docs/a.md#1.2`,
    `>` gives `src/a.py#1>"x"`;
  - `GLUED_MARKS_RE` not searched turns `@alice#299@abcdef12` red, beside five
    older glued cases;
  - deleting `docs/a.md#1장@abcdef12`, `src/a.py#handler @abcdef12` or
    `@alice#299` from the docstring turns its own parameter red;
  - dropping `Makefile#1x` or `docs/a.md#1장@abcdef12` from a dict turns the
    completeness case red;
  - before the bullet was edited, `@alice#299` and `@alice#299@abcdef12` were
    red on `the list omits it`, and were green after.
- **The ledger.** `evidence-check` named the rows the frame expected: S8–S12
  of `0.15.5.md` (three of its anchors, one of them BROKEN by the rename) and
  the `MALFORMED` row of `0.15.4.md`. S8–S12's Notes said a case holds "one or
  two examples of each". That was false, so it is corrected in place with a
  dated note, and the row now cites the completeness case too. The
  `MALFORMED` row's claim holds and takes a `Re-read` note. After
  `--reverify`: 2469 ok, 0 drifted, 0 broken, 0 malformed (executed).
- **Verified by** (executed): `bin/test` over the four reader modules, 239
  passed; `tests/test_no_real_identifiers.py`,
  `tests/test_a_merge_cannot_silently_drop_a_correction.py` and
  `tests/test_one_word_one_meaning.py`, 75 passed; `uvx ruff check` and
  `uvx ruff format --check` on the two Python files, clean.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the case name `test_what_the_dotless_openers_take_up_is_named_and_says_so`, NAME NOT IN TREE since this phase renamed it | `test_what_the_rules_still_name_is_named_and_says_so`, the same case under a name for what it holds; S8–S12 of `seal/releases/0.15.5.md` cites the new name |
| `GIVEN_UP`'s comment "One or two examples of each rule … for the verdicts #614 moved" | the rewritten comment above `GIVEN_UP`, which says every example the rules section gives |
