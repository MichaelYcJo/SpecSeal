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

  **And the refusal now arrives.** A `#` cell of punctuation ending in a
  non-digit used to send the pattern exponential — 11.4 s to refuse 28
  characters, and each further character doubled it — so `close` and `new`
  produced nothing and never returned. That is worse than the confusing
  message the ticket opened for, on the tool that gates every record. The
  pattern reads one marker character per repetition instead of a run of them,
  which accepts and keys exactly the same set: checked over every `#` cell in
  every committed record and over 4368 constructed shapes, with no
  disagreement. A 100 000-character cell now refuses in three milliseconds.

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

  **Which file a def sits in decides two different things, and the first
  version of this asked only one of them.** Collection is two rules: which
  file becomes a test module and which def inside it is a case. A `test_*` def
  in `tests/helpers.py` satisfies the second and not the first, so pytest
  never runs it — and it was reading `pytest only`, which is the false
  sentence above pointing back again. It reads `no call site found` now. And a
  `conftest.py` is the opposite case: pytest loads it by name and documents
  the repository root placement first, so a fixture or a hook in a root
  `conftest.py` was reading `no call site found` — the reported defect, left
  standing at the commonest placement of all. Both now read what they should,
  and the boundary was re-derived by running the rule over every top-level def
  in the tree rather than by reading it.

  **A conftest is loaded by name, but the directory decides whether pytest
  loads it at all.** The first repair accepted the name from anywhere, which
  put the false sentence back: a `conftest.py` in a directory nothing is
  collected under — a vendored tree, an examples directory, `src/` in a
  repository whose tests live under `tests/` — is imported by nobody, so its
  fixtures are injected into nothing and the row was saying the runner covers
  them. The rule now asks whether a file pytest collects sits at or below the
  conftest's own directory, which is the question pytest itself asks, and it
  asks it inside `tests/` as well as outside.

- **A rider comment is now checked wherever this repository plants one.** The
  list of directories the rider checks walk left out `tests/`, so four riders
  were held to nothing at all — two carrying a measurement, one with no
  verification stamp in any form, and one whose own branch record said the
  stamp had been checked when nothing had checked it. Two of the four could
  not be given a stamp naming a commit, because the commits their measurements
  were taken at were discarded when their branches squashed, so a stamp may
  now name the content it was read against instead.

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
