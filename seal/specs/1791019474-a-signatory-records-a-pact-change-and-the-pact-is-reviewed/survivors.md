# Survivors — a signatory records a pact change, and the pact is reviewed

`survivor-check --range 2b1dcb1f...HEAD`, run over the whole branch at
`47116866`, reported five places. None of them is a claim the range corrected.
Two are released rows whose coordinate lists share old hashes with fragment
rows this branch re-stamped (a released file is never edited, and each is read
again through a `Re-read ·` row in this item's fragment); two pin a refusal the
walker still builds, now from its parts; one is the heading of the cases that
pin how the `Signatory` table's ends are refused, which the cases under it
still do.

| Path | Quote | Grounds |
|---|---|---|
| `seal/releases/0.5.0.md` | `templates/seal-README.md#"## Layout"@8bbcc8e6` | a released row's coordinate list; the overlap is the old hashes P6 carried in #735's fragment before this branch re-stamped it. The released row is not edited after its release, and this item's fragment re-reads it (`Re-read · S9`) |
| `seal/releases/0.16.0.md` | `.github/scripts/run_tests.py#MARKDOWN_IT@cdd27ddd` | a released row's coordinate list; the overlap is the old hashes R3 carried in #718's fragment before phase 1 re-stamped it. The released row is not edited after its release, and this item's fragment re-reads it (`Re-read · P1-1`) |
| `tests/test_a_signatory_declares_its_pact.py` | which is not a one-cell row written `\| … \|` | the pinned refusal `hooks/config.py#gfm_table` still prints for a one-column table, built from `shape` and `written` rather than spelled whole; the removed sentence is the old literal, and the case pins the same words |
| `tests/test_a_signatory_declares_its_pact.py` | # --- every way GFM ends or breaks the `Signatory` table (round 2 of #647) --- | the heading of the cases that pin each end's sentence; the removed sentence is the old docstring's bold rule, which `gfm_table`'s docstring and the property case now carry, and the cases under the heading still cover each way |
