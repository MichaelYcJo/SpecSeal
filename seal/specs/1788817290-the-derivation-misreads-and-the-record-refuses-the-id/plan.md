# Implementation Plan: the derivation misreads and the record refuses the id

<!-- seal/specs/1788817290-the-derivation-misreads-and-the-record-refuses-the-id/plan.md
— HOW, in phases. This is the Design Gate's artifact. -->

## Summary

Three changes inside `skills/code-review/scripts/round_record.py`, each with
its own documentation edit and its own cases, built in the order that puts the
self-contained one first.

`#227` is a parser rule and touches nothing the other two touch. `#211` and
`#194` are two halves of the same row: `#194` decides which units enter
`Contract changes`, `#211` decides what the reach half says once one has. So
`#211` lands before `#194`, or the new units `#194` admits arrive in a row
whose reach vocabulary is still wrong.

## Technical context

**The corpus is what settled #227's shape.** The ticket offers two repairs —
accept a round prefix, or refuse with the format spelled out — and the
handoff names bare integers as the format in force. Before choosing the
refusal, every committed record was run through the module's own
`table_body`/`verdict_rows` path with both rules:

```
records parsed:                     130
pass today AND under the new rule:   82
pass today, refused under it:         2
already refused today:               46
```

The two are not regressions but miscounts made visible. `r3 🟡 2` reads as
finding **3** today, because `NUMBER_RE.search` takes the first digit run and
that is the `3` in `r3`. `🟢 round 2's finding (🟡 4)` reads as **2**, where
the cell names finding 4. Both currently key a fix onto the wrong row, in
silence. The other 46 already refuse — `🔴 A` as *names no number*, `🟢 1-1`
beside `🟢 1-2` as a duplicate `1` — so the new rule adds no refusal to a
record that reads correctly today, and it replaces a confusing message on the
46 with one that names the format and the row.

**Where the miscount comes from.** `NUMBER_RE = re.compile(r"\d+")` with
`.search`, at `round_record.py:1774` (`fix_table`) and `:1826`
(`verdict_rows`). `R2-1` and `R2-2` both search to `2`, which is the exact
collapse #227 reports.

**#211's class is wider than the ticket's instance,** measured by running
`call_sites` over every top-level def under `tests/` at `ba22b28`:

| Kind under `tests/` | Total | Reading `no call site found` |
|---|---|---|
| `test_*` function | 1947 | **1892** |
| fixture | 42 | **8** |
| other helper | 483 | 1 |
| class | 2 | 0 |

The ticket names the first row and its *Not verified* section asks about the
rest. A fixture is a member by construction — pytest injects it by parameter
name, so no `name(` ever exists for one whose only consumer is a test. A
`conftest` hook is a member for the same reason, by pytest's plugin dispatch;
this tree holds none today, which is why the case for it is written against a
built repo rather than found here. The one helper, `floor_record` at
`tests/test_the_reopening_is_one.py:164`, is **not** a member: it is passed by
name as a value at five call sites and never called, so `no call site found`
has a different cause and a different repair. It is out of scope and named in
`overview.md`.

**#194's mechanism, and the hole it does not cover.** The contract tuple is
`(signature(node.args), return_arities(node))` at
`round_record.py#top_units`. Adding the set of returned constant literals
catches a new sentinel without reasoning about types. It does not catch
`is_a_record_of_a_moment`, which changed which inputs map to which of the two
values it already returned — signature, arity, return type and returnable set
all unchanged, confirmed at
`seal/specs/1788735085-a-loaded-file-naming-a-real-version-is-a-timer/rounds/round-2.md:60`.
That is the paragraph's subject, and widening the check to reach it is
explicitly out of scope.

**Literals are keyed by type and repr,** not by value. Python hashes `0` and
`False` to the same key and `1` and `True` likewise, so a unit that stopped
returning `0` and started returning `False` would read as unchanged under a
plain set of values. `(type(v).__name__, repr(v))` keeps them apart, and it
costs one tuple per literal.

**What breaks in six months.** The literal set makes `Contract changes` wider,
so a fix that swaps a returned message string now puts its unit in the row
with a full reach walk behind it. That is more rows and more `git grep` calls
per `close`. The trade is deliberate: the row exists for the largest
regression class #57 measured, and a message a caller compares against is
exactly the reach a person misses. If it becomes noisy, the narrowing to reach
for is *literals other than strings*, not a retreat to arities.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| **#227** — accept an optional round prefix, keying on the digits after it | Two rounds' findings in one table would then be legal, and the fix table's key would have to carry the round too. Every consumer of `{number: ...}` in `close` — `unknown`, `missing`, `already`, `depth_two` — becomes a two-part key for a shape no record in the corpus actually uses | rejected |
| **#227** — refuse a non-bare id, naming the format and the row | 46 committed records already refuse; 2 more stop miscounting. A reviewer who wants the round in the id loses that, and gains a message that says so at the moment it costs one rename | **chosen** — and it is the contract the handoff put in force for this release run |
| **#227** — leave the parser and document bare integers only | The refusal stays the one the ticket calls unreadable: *two rows for finding 2* on a table with one `R2-1` and one `R2-2`. Documentation that only a person who already knows will find | rejected |
| **#211** — classify anything under `tests/` with no caller as `pytest only` | `floor_record` would read `pytest only` and it is reached by neither pytest nor a call. The row would then say *the runner covers this* about a unit nothing covers | rejected |
| **#211** — classify a `test_*` def under `tests/` only, as the ticket proposes | Leaves the 8 fixtures reading `no call site found`, which is the same false sentence the ticket opened for. §12: the finding names an instance, the fix is owed the class | rejected |
| **#211** — `test_*`, fixture-decorated, and `pytest_*` in a `conftest` | A pytest config that collects under another name or another prefix reads as unreached again. That config does not exist here and the three rules are pytest's own defaults | **chosen** |
| **#194** — a new reach value, e.g. `runner`, for #211 | Adds a sixth word to the reach vocabulary, so `docs/review-chain-spec.md`'s enumeration and the test that derives it both move, for a distinction no reader of the row needs. `pytest only` already means *the runner is the reach* | rejected |
| **#194** — documentation alone | Refused by the owner before the first edit: it moves the work to a person, which this repository's first goal treats as the more expensive design | rejected — it is the floor, and the floor ships beside the check |
| **#194** — literals from returned tuple elements as well as bare returns | A sentinel added to one slot of a returned tuple is the same shape as a bare one, and `return_arities` already treats a returned tuple element-wise | **chosen**, included |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | #227 — a finding id is a bare integer, in `fix_table` and `verdict_rows`; the refusal names the format and quotes the row; a duplicate quotes both rows; the format stated in `skills/code-review/SKILL.md` §Findings format and `templates/sdd-round.md` | `bin/test tests/test_a_finding_id_is_a_bare_integer.py -q`, each case seen red first; the 130-record corpus case | 051ebfa |
| 2 | #211 — `call_sites` reads a runner-reached unit as `pytest only`; `docs/review-chain-spec.md`'s five-value paragraph says when | `bin/test tests/test_a_runner_reached_unit_reads_pytest_only.py -q`, four kinds built in a real repo, each seen red first | db58253 |
| 3 | #194 — the contract carries the returnable literal set; the stated hole written into `docs/review-chain-spec.md` | `bin/test tests/test_a_new_returnable_value_is_a_contract_change.py -q`, plus the AST-derived cross-check over a real diff | 58c7ce2 |
| 4 | The records — changelog fragment, ledger fragment, phase records, overview, `docs/flow.md` | the fragment and record checkers in the narrow modules they belong to | |

## Operational impact

No migration, no new dependency, no new environment variable.

**One compatibility break, deliberate and bounded.** A round record whose
verdict table numbers findings anything but a bare integer, and a fix table
that copies such a numbering, now refuse at `close` with a message naming the
format. The 46 records in the tree that already refuse are unaffected in
outcome and get a better message; the 2 that pass today by miscounting stop.
No committed record's content is rewritten by this branch.

**`Contract changes` rows get longer.** A unit whose returned constant
literals changed now enters the row and pulls a `git grep` reach walk with it.
Expect more entries per record and a slower `close` on a fix range that
touches messages.
