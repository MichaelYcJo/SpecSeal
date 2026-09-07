- **A round record's finding id is now a bare integer, and a record that
  numbers findings any other way is refused with the format named and the row
  quoted (issue #227).** A reviewer numbered eight findings `R2-1` … `R2-8` —
  the round in the id, so a finding stays unambiguous when three rounds are
  read side by side. The generator read the first digit run anywhere in the
  cell, so all eight collapsed toward `2`, and what came back was *the fix
  table has two rows for finding 2* about a table holding one `R2-1` and one
  `R2-2`. The first read is that the table is malformed, not that the ids
  are, and with eight rows and no coordinate the pair had to be found by
  hand. Both tables now read the cell through one pattern, and a genuine
  duplicate quotes both rows.

  **The refusal was chosen over accepting a prefix, and the corpus is why.**
  Every committed record was run through both rules first: of 130 that parse,
  82 pass under either, 46 already refuse today, and 2 pass today only by
  miscounting — `r3 🟡 2` keys as finding **3**, out of the `3` in `r3`, and
  `🟢 round 2's finding (🟡 4)` keys as **2** where the cell names 4. So the
  rule takes away two wrong answers and no right one. The round is already in
  the record's own file name, which is what a prefixed id was reaching for.

  **The format is now stated where reviewers pick numbers**, not only at the
  point of refusal — the ticket's own last line. The reviewer chooses the
  numbering and the fix pass copies it, so the refusal used to surface at the
  orchestrator, one hop from either agent that could have avoided it.

- **`Contract changes` no longer reports `no call site found` for a unit
  pytest itself reaches (issue #211).** A collected test function is called by
  the runner and never by name, so the only `test_thing(` in the tree is its
  own `def` line and the reach came back empty — the row said *this unit is
  dead* about a case that runs on every CI leg. It reads `pytest only` now,
  which is the value that already existed for a unit reached only from
  `tests/`.

  **The class was enumerated by running the derivation, not by reading it.**
  Over every top-level def under `tests/`: 1892 of 1947 `test_*` defs read
  `no call site found`, and so did 8 of 42 fixtures — the member the ticket
  had left in its own *Not verified* section. A fixture is injected by
  parameter name and a `conftest` hook is dispatched by the plugin manager,
  so neither is ever written as `name(` either.

  **It is those three shapes and not everything under `tests/`.** One helper
  there reads `no call site found` correctly, because it is passed by name as
  a value and never called, and a wider rule would say the runner covers a
  unit nothing covers — the same false sentence pointing the other way. One
  limit is recorded rather than closed: the hook arm reads `conftest.py`
  alone, where pytest also dispatches hooks from collected test modules.

- **`Contract changes` now sees a unit that gains or loses a returnable
  value, and the shape it still cannot see is written down (issue #194).** The
  derivation compared parameters and return arities, so a unit returning the
  same shape with a meaning it could not return before changed neither and the
  row read `none` — on the row that exists for the largest regression class
  #57 measured. The measured instance returned 0 for a mean it cannot compute,
  and the one call site interpreting that 0 was never revisited: it takes the
  charged 0 as a baseline and reports growth on a run whose input collapsed.
  The contract now carries the set of returnable constant literals, keyed by
  type as well as value — Python hashes `0` and `False` into one key, and
  those are two different things to return.

  **A real instance the old rule missed, found by construction:** between
  v0.8.0 and v0.8.3, `chain_check.py#read_record` began returning an explicit
  `None` with signature and arity unchanged. The old contract read it as
  unchanged.

  **The hole is the other half of the deliverable, not a gap left over.** A
  changed input→value mapping — a unit that keeps returning exactly the values
  it already returned and changes which inputs reach which one — is invisible
  to a literal-set comparison by construction. `docs/review-chain-spec.md` now
  says so, names the measured instance, and says the residual is the
  reviewer's. Documentation alone had been refused as an answer, because it
  moves the work to a person; the check ships and the paragraph states where
  it stops, so a later session widening it is removing a stated limit rather
  than closing a gap.
