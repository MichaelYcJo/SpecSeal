# Survivors — a ledger row's claim is the test that enforces it

`survivor-check --range origin/release/v0.21.0...HEAD` named four places that
still carry wording this item's range removed, read at 124cd1a. None is a
sentence: the removed "wording" is two coordinates' old hashes, `reverify`
at `49940c1b` and `reverify_into` at `fc55dab7` in `evidence_check.py`, which
`--reverify` re-stamped in a sibling's fragment row
(`seal/ledger/1791384156-config-rows-coordinates-and-headings-have-one-reader.md`,
`Corrected · C1`). The same two coordinates stand at those hashes in four
released rows of `seal/releases/0.19.0.md`, which `Ledger frozen from` keeps
as they are; `bin/evidence-check --strict .` reads every one of their
families clean at that head, through the re-reads named below.

| Path | Quote | Grounds |
|---|---|---|
| `seal/releases/0.19.0.md` | `seal/releases/0.18.1.md#"### 1791076833-the-reverify-writer-records-before-it-restamps">"W8 · every line"@dbadd619` | a released row, frozen; this item's fragment re-reads its family (`Re-read · Corrected · W8`), the claim read against the diff to `reverify` and `reverify_into` |
| `seal/releases/0.19.0.md` | `seal/releases/0.18.2.md#"### 1791128260-a-pact-row-is-read-in-one-plain-spelling">"Corrected · C1 ·"@19242e07` | a released row, frozen, superseded by `1791384156`'s `Corrected · C1` row, which this item's run re-stamped in place after reading its claim against the same diff |
| `seal/releases/0.19.0.md` | `seal/releases/0.18.2.md#"### 1791119072-one-reverify-leaves-the-ledger-clean-and-records-only-a-real-move">"E1 ·"@62e3ab5e` | a released row, frozen; this item's fragment re-reads its family (`Re-read · Corrected · \`evidence-check --reverify --into\` records each move`) |
| `seal/releases/0.19.0.md` | `seal/releases/0.18.3.md#"### 1791163980-an-in-place-reverify-leaves-history-alone-and-reports-each-row-once">"Corrected · the"@38b8f501` | a released re-read, frozen, in the family of `seal/releases/0.18.3.md`'s `Corrected · the \`Checked\` date` row, which this item's fragment re-reads |
