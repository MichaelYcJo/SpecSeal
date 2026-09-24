# 1790260563-the-fold-checks-run-only-as-this-repositorys-tests — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 2e7ed5c7 |
| Ran by | specseal:smith on Opus 5.5 |

## What this phase was asked

#530: `skills/settle/scripts/settle.py#first_cell` drops what stands before a
row's first pipe when it is container syntax only — `>`, `-`, `*`, `+`, `1.`,
`1)` and `<!--`, in any combination, spaced or not — and keeps anything else
as the label, as it did before. The new cases in
`tests/test_settle_reads_before_it_removes.py` were to be seen red against
the old `first_cell`, and the comment-opener and prose-prefix cases green
before and after. `open_rows` in the same file belongs to the #487 chain and
was not to be touched.

## What this phase found

- **The class is one pattern, `CONTAINER_RE`, and the empty run is in it.**
  The ordinary `| claim |` row has an empty prefix, and the same fullmatch
  takes it, so the old `not cells[0].strip()` arm is the pattern's zero case
  and no second arm is needed.
- **The comment-opener strip above the split is kept as it was.** Today
  `<!-- prose | claim |` is labelled `prose`, because the opener is stripped
  before anything else is read. Folding the opener into the pattern alone
  would have labelled that row `<!-- prose` instead, which is a change to a
  prefix that is not container syntax only, and the spec keeps those as they
  are.
- **Seen red (§15).** At `9ff20d3f` all eight container cases failed, the
  last of them `<!-- > |` labelled `>`, and the end-to-end case printed
  `seal/ledger.md:32  > -` where the claim belongs. The four keep-today cases
  (`<!-- |`, a prose prefix, `> note - |`, `1.5 |`) passed before and after.
- **Mutated at `2e7ed5c7`** from a Python script, the file restored from the
  bytes it read: bullets out of the pattern, 4 red; ordered-list markers out,
  2 red; `>` out, 6 red; the old blank-cell arm back in, 9 red.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `first_cell`'s `not cells[0].strip()` arm | `CONTAINER_RE`'s empty run, which matches the same prefix |
