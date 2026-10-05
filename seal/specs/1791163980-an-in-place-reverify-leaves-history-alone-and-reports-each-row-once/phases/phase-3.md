# 1791163980-an-in-place-reverify-leaves-history-alone-and-reports-each-row-once — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | e0c77f9c |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

#781 (D4) and the records (D5). The *dated note* sentence in
`docs/the-evidence-ledger.md`, its `RE_READ_SENTENCES` pin and the comment
above it, seen red with the old sentence in place. Then `survivor-check
--range a3aa139a..HEAD`, with a `survivors.md` row for each place it reports
that stays true. Then this item's fragment rows. Then `Re-read ·` rows through
`bin/evidence-check --reverify --into seal/ledger/<this id>.md --checked
2026-10-05`, each claim read against the edit first, and a `Corrected ·` row
over `seal/releases/0.18.2.md:91` and over any other released claim the edits
made false. Then the `changelog.md` fragment, describing what ships at the
branch's head.

## What this phase found

**D4 landed as the owner decided.** The pin was changed first and ran red
against the old sentence, then the sentence was corrected. The corrected
sentence is the questions' Q1 default.

**`survivor-check` reported two places, both true.** Both are in the 0.18.2
item's `post-review-check-2.md`, quoting the docstring of the case whose tree
phase 2 moved into a helper. `survivors.md` holds both with grounds. It
reported nothing for the removed *dated note* sentence: the earlier work
items' records that mention a dated note share too few words with it.

**The released rows these edits drifted: 31, each read against the diff.**
`bin/evidence-check .` after the doc edit owed them a re-read. The `--into`
run, on this branch's code, wrote one `Re-read ·` row per row into the
fragment, and the row over `seal/releases/0.18.2.md:91` was then rewritten as
a `Corrected ·` row. After that, `bin/evidence-check --strict .` read
`5696 ok · 0 drifted · 0 broken` and exited 0.

| Released row | Verdict | Grounds |
|---|---|---|
| `0.15.3.md:48` P2-1 | holds | the matches still come from `unquoted(text)`, so a fenced example is never re-stamped |
| `0.15.4.md:56` | holds | the `MALFORMED` `LEFT` line, what it writes and its exit are unchanged |
| `0.16.0.md:17` O3 | holds | `main`'s grading and totals are untouched |
| `0.16.0.md:18` O4 | holds | the clause says an `OVERFLOW` row does not stop its hashes being re-stamped, and it does not; a held coordinate on such a row is left for #785's reason, not for the overflow |
| `0.16.0.md:57` R1 | holds | the date is still written into every row whose hash moves; a left-alone coordinate moves no hash |
| `0.16.0.md:58` R2 | holds | a row whose hash did not move is still byte-identical and unnamed |
| `0.16.0.md:60` R4 | holds | the `--checked` refusals are untouched |
| `0.16.0.md:61` H1 | holds | every split still reads `gfm_lines` |
| `0.18.0.md:29` L9 | holds | no sentence of the home was copied into a carrier |
| `0.18.0.md:77` | holds | without the row a claim is still kept true where it stands |
| `0.18.0.md:158` N2 | holds | `family_view`'s naming of an outranked reading is untouched |
| `0.18.1.md:171` F1 | holds | `released_drift` still runs inside the plan; `reverify`'s own `family_view` runs there too, before any write |
| `0.18.1.md:174` W8 | holds | every line claiming a write still waits for it; a `left` line claims none, and the `LEFT` lines still print as before |
| `0.18.1.md:175` W9 | holds | the strict read is untouched |
| `0.18.1.md:176` W10 | holds | `apply_plan` and its `LEFT` line are untouched |
| `0.18.1.md:415` F2 | holds | the `--into` paragraph's and the usage text's sentences it names are kept; this item added beside them |
| `0.18.1.md:417` | holds | *without the row it re-stamps in place as before* compares with the freeze's arm, and a narrowed run still names each family whose newest reading it could not reach |
| `0.18.1.md:418` | holds | a narrowing to a file holding no member, and a run without `--ledger`, answer as before; the 144-cell case still passes, and the remedy's wording is not part of the claim |
| `0.18.2.md:86` E3 | holds | the walk order, the bounded re-walk, one line per coordinate and the narrowed citation `LEFT` line are unchanged |
| `0.18.2.md:87` E4 | holds | MOVES is folded by `walked_move` as before; `walked_outcome` reads the same fold |
| `0.18.2.md:88` E5 | holds | the five-things paragraph is unchanged |
| `0.18.2.md:90` | holds | as E5 |
| `0.18.2.md:91` | **false: corrected** | it ended *although without the freeze the ledger home says a released row is re-stamped in place with a dated note*; the home now names the date added to the `Checked` cell |
| `0.18.2.md:129` C1 | holds | what records a pact change is unchanged; a left-alone coordinate moves nothing. *Corrected in round 1's fix pass (⬜ 4):* at `0667af2e` a held coordinate no one place holds, on a row the run dates, handed MOVES no BROKEN part; since round 1's fix it does. *Corrected again in round 2's fix pass (⬜ 2):* at `930078de` a held two-place coordinate that one place still holds was handed a BROKEN part on a dated row; since round 2's fix it is not, and the row was re-read on 2026-10-05 after that fix |
| `0.18.2.md:138` O3 | holds | the skill's vendored sentence is unchanged; this item added a paragraph before another |
| `0.4.0.md:22` | holds | re-verifying is still a separate command, and the check still writes nothing |
| `0.4.0.md:29` | holds | the rename heal is unchanged |
| `0.4.0.md:59` | holds | every flagged row still gets a line; a coordinate its family holds is not flagged by `--strict` where the run does not date its row, so leaving it silently there contradicts no verdict. *Corrected in round 1's fix pass (⬜ 4):* on a row the run dates, a held coordinate no one place holds becomes the newest reading and reads BROKEN, and at `0667af2e` it was left with no line; since round 1's fix it is named `left`. *Corrected again in round 2's fix pass (⬜ 2):* at `930078de` a held two-place coordinate that one place still holds was named `left` and recorded BROKEN on a dated row, where `--strict` reads it OK; since round 2's fix it is not, and the row was re-read on 2026-10-05 after that fix |
| `0.4.0.md:281` | holds | the two entry points are unchanged |
| `0.8.3.md:13` | holds | the new lines name ledger paths through `built_name` |
| `0.9.0.md:92` R5 | holds | the records arm is untouched |

**The run itself is the build's code, and it shows D1.** The `--into` run
re-stamped only this item's six rows, which held placeholder hashes, and
wrote the 31 citing rows; no other fragment exists on this branch.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The ledger home's *re-stamps a re-read row in place with a dated note* | The same sentence, naming the date added to the `Checked` cell, and `RE_READ_SENTENCES` |
