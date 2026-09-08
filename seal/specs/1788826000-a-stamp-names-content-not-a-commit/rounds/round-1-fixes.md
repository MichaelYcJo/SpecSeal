# 1788826000-a-stamp-names-content-not-a-commit — round 1, the fix pass

Fix commits: `7ff1e63..HEAD` on `fix/239-a-stamp-names-content-not-a-commit`
— `bdf65df`, `eaa8030`, `923f86c`, `e1b83b8` and the commit carrying this
file. The round's target was `404dd4d`; its record is committed at `7ff1e63`.

## Fixes

| # | Verdict | Commit or grounds |
|---|---|---|
| 1 | fixed | `eaa8030` — the twelve dates restored, each proved against the commit its pre-migration stamp named; `bdf65df` is the writer that erased them |
| 2 | fixed | `bdf65df` — `--reverify` skips on the hash alone, and the drift message says `--only` takes a file |
| 3 | fixed | `bdf65df` — the same change; a hash that has not moved is no longer re-stamped, so no ledger row drifts for a unit nobody edited. `phase-4.md`'s steady-state paragraph corrected in `e1b83b8` |
| 4 | fixed | `bdf65df` for the `#` form, `923f86c` for the HTML form and the opener that was looser than its own docstring |
| 5 | fixed | `eaa8030` — `agents/smith.md` and `skills/implement/SKILL.md` re-anchored to their headings. `templates/evidence-check.yml` answered rather than changed: see below |
| 6 | fixed | `bdf65df` for `content_at`, `e1b83b8` for `phase-4.md`'s bullet and ledger row S4 |
| 7 | fixed | `e1b83b8` — `questions.md` C1 and `overview.md` both say two, and name the second |
| 8 | fixed | `e1b83b8` — `phase-3.md` gains the two missing rows, both marked NAME NOT IN TREE |
| 9 | deferred the orchestrator | contract §2 reserves the full suite, the repository-wide lint and the typecheck for one run after the rounds settle |

## Where finding 5 was answered rather than changed

`templates/evidence-check.yml` keeps its quoted-line anchor. Three grounds,
and the measurement is the first of them.

- **The alternative loses the alarm.** Executed: the quoted line resolves to
  lines 1–18, which is the header comment the rider makes its claim about;
  `"name: evidence-check"` resolves to line 20 alone. Re-anchoring there
  leaves a rider hashing a line it says nothing about.
- **A YAML file has no heading structure.** `text_regions`'s own docstring
  says the heading rule is markdown-only, and says it was found by migrating
  this repository's ledger rather than reasoned about. The two markdown
  riders had a heading available and now use it; this one has none.
- **BROKEN's advice happens to be right here.** The rider says two phrases
  promise a softer mode the file does not deliver. Correcting either phrase
  spends the rider, and BROKEN's text is *re-anchor it or delete the rider*.

`overview.md` already defers this rider to the repository owner as half
spent, and that row is unchanged.

## What the re-enumeration found

Finding 4 was a class applied in one place, so the same question was put to
every rule this branch introduced, by construction rather than by reading.

| Constructed | Result |
|---|---|
| two riders sharing ONE HTML comment, the second before the `-->` | **the same defect** — one block, one stamp read, the second carrying `deadbeef` unresolved. Fixed in `923f86c` |
| two HTML riders in two comments, back to back | already two blocks; unaffected |
| a line holding both `<!--` and the marker inside a string literal | **became a rider held by nothing** — the HTML opener asked only that `<!--` appear on the line, where the `#` side asks for a comment head and the docstring says both do. Found when this file's own fixture constant became one. Fixed in `923f86c` |
| a `#` comment DESCRIBING the convention inside a scanned root | becomes a rider with no stamp — BROKEN, loud. The design's intent, and it fired on the fix pass's own explanatory comment |
| a rider written as a TRAILING comment, in **both** forms — `value = 1  # RIDER: …` in a `#` file and `some text &lt;!-- RIDER: … --&gt;` in a markdown one | **read by nothing, and silent about it**, in either form. This pass constructed the `#` half only; round 2 constructed the markdown half and got the same `0 ok · 0 drifted · 0 broken`. Not in the tree: at `2f0dd02` a grep of the six roots finds 33 marker lines against the reader's 20 riders, so 13 extras, all prose or string literals — 36 and 16 at `677e10f`, where round 2's fix pass planted three more in the case file. The count names the commit it was taken at because an aggregate is not a coordinate (round 2, findings 12 and 13). Closing it needs a rule comparing the two corpora, which a fix pass may not add — deferred to the repository owner in `overview.md` |
| `evidence_check.py#reverify`, the writer this one was copied from | does **not** have finding 2's defect: it skips on the hash alone and never touches the `Checked` column. The rider writer had diverged from its own model |
| every rider's pre-migration stamp, replayed | a second stamp naming a commit that predates its own file — `hooks/root-migrate.py` at `4f78074`, the same shape as `881fb0f`. Recorded in ledger row S4 |

## What this pass did not touch

`rounds/round-1.md` and `rounds/round-1-report.md`. The records arm of
`bin/evidence-check` refuses eight names in them and exits 2, and that state
is executed against a `git archive` of `7ff1e63` — it predates this pass.
They are the orchestrator's records, and `hooks/review-history-guard.py` is
why a fix pass does not edit review history. `overview.md`'s *Not verified*
names the orchestrator as the answerer.
