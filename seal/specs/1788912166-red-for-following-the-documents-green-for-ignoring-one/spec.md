# Feature Specification: red for following the documents, green for ignoring one

Three checks that run at a pull request into `release/*` are wrong about what
they are reading. Two of them fire on a session that did exactly what a
document told it to do; the third stays silent on a rule written in five
places. All three were found by this release's own run.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CONTRIBUTING.md` §*What a change to a gate must carry* | Every phase below answers four things: a test seen red, a stated failure direction, a prompt budget, platform honesty. The prompt budget is zero for all three — these are CI checks with no interactive path — and that is the answer, not an omission |
| `skills/code-review/scripts/chain_check.py:2868` and `:3079` | The `Pass` arm says *"Open it as a draft while the rounds run"*; the record-count arm a hundred lines later has no draft state in it. Both are in one function's walk |
| `skills/code-review/orchestration.md:405` | *"The draft pull request opens at the end of the build, before round 1"* — the instruction whose obedience the arm above fails |
| `docs/flow.md` §*A shipped version's section is deleted, not kept* | Names the durable copies that are supposed to survive a deletion, which is what `survivor-check` counted 153 of |
| `.github/workflows/hygiene.yml:221` | Already exempts one range, and states the reason as a property of the range rather than as a special case: *"which is not a range a fix pass wrote"* |
| `templates/sdd-round.md:33` | The `Broad gate` cell — `not yet`, or the SHA the one full-suite run happened at and the base it was compared against |
| `chain_check.py:127` and `:135` | The cutoff idiom and its reason: *"A check whose first production act is red on history nobody can fix is a check people learn to skip"* |
| `CLAUDE.md` §*verification that runs unattended* | Decides against any answer that adds a question. None of the three does |

## Scope

**In, one ticket per arm.**

- **#296** — the record-count arm becomes draft-aware in the way the `Pass`
  arm already is: on a draft it prints the state instead of appending an
  error. Pressing *Ready for review* fires `ready_for_review`, the workflow
  re-runs, and the arm applies, so nothing that can reach `main` is exempt.
- **#295** — `chain_check` reads the `Broad gate` cell of the work item's last
  round record at a **ready** pull request. `not yet` is the run that never
  happened; a SHA that precedes that record's own `Target SHA` is the run
  that was spent before the round it was meant to seal. Both fail, and each
  names which of the two it is.
- **#297** — `survivors.md` gains a whole-range form: one row with grounds
  covering a range, instead of one row per surviving sentence. A documented
  deletion then costs one written sentence rather than 153.

**Out.**

- **Making the seal block's `broad gate:` line the source.** The round record
  already carries the cell; that is why #295 is cheap. Whether the seal block
  becomes load-bearing is a separate question and is recorded.
- **The 1.6 similarity threshold** `survivor-check` scores against. #297's
  153 were reported at 1.60–1.62, so the threshold is implicated and changing
  it moves every future run's verdict. Recorded, not taken.
- **Changing `orchestration.md`'s sequence.** The document is right — a
  reviewer needs a pull request to review — and the check is what is wrong.
- **#30 and #120.** A `sealer` that owns the run is the structural answer to
  #295's premature half and it is 0.10.0's, behind #120's §2 rewrite. The
  check here does not wait for either and keeps working after both.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| The instruction the check gives can be followed | Given a draft pull request, `Review = through the review chain`, and `rounds/` empty / when `chain_check` runs / then it reports the state and exits 0 | a case with an event payload naming a draft |
| A draft is not a way past the record | Given the same tree and a **ready** pull request / when it runs / then it fails as it does today, with the message unchanged | the existing case, still green |
| A run that never happened is caught | Given a ready pull request whose last round record's `Broad gate` reads `not yet` / when it runs / then it fails, naming the missing run | a case over a fixture record |
| A run spent before its round is caught | Given `Broad gate` naming a SHA that precedes that record's `Target SHA` / when it runs / then it fails, naming the premature run and both SHAs | a case with two commits in a fixture repository |
| A run taken after the rounds settled passes | Given `Broad gate` naming a SHA at or after the `Target SHA` / when it runs / then it passes | the same fixture, one commit later |
| The rounds are allowed to still be running | Given a **draft** pull request whose last record reads `not yet` / when it runs / then it passes | a case pairing the draft payload with `not yet` |
| Work items already in flight are not failed retroactively | Given a work item whose id precedes the new cutoff / when it runs / then the `Broad gate` arm does not apply to it | a case with an id below the cutoff, and one above |
| A documented deletion costs one sentence | Given a range that deletes a shipped section whose sentences stand in `CHANGELOG.md`, and one whole-range row in `survivors.md` with grounds / when `survivor-check` runs / then it passes, naming the declaration | a case built from #293's own range |
| An undeclared deletion still fails | Given the same range with no such row / when it runs / then it fails as it does today | the same fixture without the row |

## Data & interfaces

No schema. Three behaviour changes inside two scripts, and one new cutoff
constant. The facts each rests on, opened at the coordinate rather than
assumed:

| Fact | Coordinate | Label |
|---|---|---|
| `strict = state != "draft"` reaches the `Pass` arm and nothing else | `chain_check.py:2973` | read |
| `chain_check.py` contains no occurrence of `broad` — nothing reads the cell | the whole file | executed (`grep -n broad`) |
| `BROAD_GATE` and `GATE_NOT_YET` are defined in `round_record.py` alone, written at creation and updatable at close, and no code validates the cell's value | `round_record.py:325, 331, 1698, 2809, 2854` | executed |
| `round_record.py:1541`'s *"chain_check.py enforces that at the broad gate"* is about the reopening **bound**, not this cell | `round_record.py#bound_line` | read — and it is the near-miss this specification exists to not repeat |
| Every record ever written defaults to `not yet`, so the new arm needs a cutoff | `round_record.py:1698` | read |
| The cutoff idiom already has seven instances | `chain_check.py:555, 582` | read |
| `survivor-check` reported 153 survivors at similarity 1.60–1.62 on #293's range | the failing `release` job of #293 | executed |
| A pull request into `main` already skips the survivor step | `hygiene.yml:221` | read |

## Open questions → questions.md

Three assumptions, and one thing that is genuinely the owner's: whether the
`Broad gate` cell's vocabulary should be validated where it is written, now
that something reads it.
