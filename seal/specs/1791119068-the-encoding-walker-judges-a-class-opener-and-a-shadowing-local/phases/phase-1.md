# 1791119068-the-encoding-walker-judges-a-class-opener-and-a-shadowing-local — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 7227d29f |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

C1 (spec §*The classes*), by D1: move the `.open` method positions out of
the table the top of `judge` matches by dotted name, so no method row can be
reached there unshifted. Plant S1's three `UNNAMED` spellings of a
class-called `zipfile.Path.open(q, "r")`, S3's structural test over the
tables the top of `judge` reads, and show S2's existing `NAMED` case passing
for the right reason. Every new case seen red at the base first. Settle W1
(the shape of the split) and record it here. Re-derive round 3's paste-ready
🟡 1 diff rather than paste it (D6).

## What this phase found

**W1: a second table keyed by what `owner` resolves the receiver to.**
`OPENERS` keeps the four function rows. `OPEN_METHODS` holds `<expr>` and
`zipfile.Path`, and only the `.open` branch reads it: a receiver `owner`
resolves to a key gets that key's positions, every other receiver gets
`<expr>`'s. `judge_opener` now takes the positions and the opener's name
rather than a key into one table, so the two kinds it emits for a method,
`<expr>.open()` and `zipfile.Path.open()`, are spelled from the key exactly as
before, and `UNNAMED` pins both unchanged.

**S3 reads the tables from `judge`'s own source.** The spec asks for one test
over *the table the top of `judge` matches openers in*. A list of tables
typed into the test is a second list to keep in step with `judge`, so
`tables_matched_by_dotted_name` collects every name `judge` tests
`target in`, from the parsed source of `judge`. It finds `OPENERS`,
`ALWAYS_UNNAMED`, `BINARY_BY_DEFAULT`, `TEXT_ALWAYS` and
`TEXT_UNLESS_BINARY`, so a method row in any of the five fails the test by
name, and a table `judge` gains later is read without an edit here. The test
asserts `OPENERS` is among them, so a derivation that finds nothing fails
rather than passes empty.

**A structural check of a clean tree cannot fail on that tree.** Mutating
the filter in `methods_of_unbound_receivers` (a method key matched as
`key in UNBOUND_RECEIVERS`) first SURVIVED: after the fix there is no method
row left for it to name. The test now also runs the filter over a fixture
holding the moved row and a function row, and asserts it names exactly the
moved one. With that, the same mutation is red.

**Seen red (contract §15), each executed:**

| Case | How it was shown red |
|---|---|
| S1, three spellings: `zipfile.Path.open(q, "r")`, `Path.open(q, "r")` after `from zipfile import Path`, `z.Path.open(q, "r")` after `import zipfile as z` | Planted before the fix: each returned no site against the base's walker. `zipfile.Path.open(q)` there came back as `zipfile.Path.open(), mode not a literal`, `q` read as the mode, as round 3 reported |
| S3, `test_no_method_is_matched_by_its_dotted_name` | Planted before the fix: red naming `OPENERS['zipfile.Path.open']`. After the fix, `bin/mutation-check` restoring that row into `OPENERS`: red |
| S2, the `NAMED` case `zipfile.Path open unbound, 3rd positional` | `bin/mutation-check` deleting its `"utf-8"`: SURVIVED against the base's walker, which is the defect, and red after the fix |

**Mutations of the units this phase added, each through `bin/mutation-check`,
all red:** `OPEN_METHODS["zipfile.Path"]` moved to `(0, 2)`; the `.open`
branch sending every receiver to `<expr>`; `judge_opener` dropping `shift`;
`tables_matched_by_dotted_name` reading `made_by` instead of `target`; the
filter in `methods_of_unbound_receivers`, after the fixture above.

`bin/test` on the module: 124 passed (120 at the base, plus three S1 cases and
S3). Ruff check and format check clean on the module.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The `zipfile.Path.open` and `<expr>.open` rows of `OPENERS` | `OPEN_METHODS`, as `zipfile.Path` and `<expr>`, with the same positions and the comment on `zipfile.Path.open`'s signature |
