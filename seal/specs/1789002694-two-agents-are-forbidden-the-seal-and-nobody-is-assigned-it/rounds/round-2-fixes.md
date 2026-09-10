## Fixes

| # | Verdict | Commit or grounds |
|---|---|---|
| 11 | fixed | 5a20202 — the two states are told apart by a discriminator the message carries, not by the exit code, and the refusal names which side it is on |
| 12 | fixed | 0cbd6ad — the third refusal reads the row's whole vocabulary rather than `nobody` alone, and names all three values in its message |
| 13 | fixed | bd08f52 — the suite row is read on an axis that is not a word list, so a linter's error count and an all-skipped run both stop landing on it |
| 14 | fixed | 67cdbda — the unit takes the platform as an argument so a case can turn it red on any machine, the quoting is `cmd.exe`'s rather than `CreateProcess`'s, and the residual it does not close is named in the docstring |
