### Fixed

- A `--reverify` narrowed with `--ledger` now answers for every family that
  a file it read holds a member of (#740). It used to answer only where the
  family's first row, the released row the others re-read, sat in a file it
  read. Narrowed to a release file holding a folded `Re-read ·` row, or to a
  fragment holding an older re-read, it wrote nothing and exited 0, while
  `--strict` with the same narrowing read that member DRIFTED. Now, without
  the freeze, it names the family's first row and exits 1; under the freeze,
  `--into` writes the re-read that row is owed, and a run without `--into`
  names it with the `--into` form. A narrowing to a file that holds no member
  of the family, and a run without `--ledger`, behave as before.
