# Review round 1 — `chore/514-four-shipped-work-items-wait-unfolded`

Target SHA `d0282bf`, base `origin/release/v0.13.2` (`b0cbd34`). Reviewed in a
`git clone --no-local` at the target. This is a first round, so there are no
earlier `round-N.md` coordinates to carry.

How the findings relate:

```
① the folded release-tail rule says the tag push fires all three acts   (🔴, code says otherwise)
② the folded fold rules (a) and (b) give opposite answers for one hit    (🟡)
     └ and 1790076070 Q4, an open person's question, reached no durable home
③④ two folded sentences are slightly inexact                            (⬜)
⑤ this work item's own records still describe the b0cbd34 pin            (⬜ correction)
```

## Spec compliance

### 1. 🔴 The folded release-tail rule says the tag push fires the label acts, and it does not

`docs/branch-and-release.md:43-73`, the `1790076050` statement.

**What is wrong.** The headline reads *"Every act the release performs after
the tag belongs to a machine, and the tag push is what fires it."* The three
acts it lists are the note, the directory and the `size: now` label. The code
says otherwise for two of them:

- **The label acts.** `.github/workflows/close-issues-on-release.yml` fires on
  `push: branches: [main]`. It runs `tracker_labels.py --apply`, and
  `close_issues_on_release.py#spend_label` takes the label off. That is the
  merge, which happens before the tag exists. `docs/release-checklist.md` §6
  says so itself: *"The close-issues workflow has already run by now. It fires
  when `main` moves, which is the merge above."*
- **The directory check.** No workflow runs `plugin_directory_check.py`. It is
  typed by hand at §6's box, and the same paragraph calls submitting *"a
  person's act"*.
- **The closing sentence.** *"each box confirms that the machine acted"* is
  wrong for the directory box, where no machine acts.

**What the retired spec actually said.** `1790076050`'s own spec (judgment 2)
drew the opposite line: *"The trigger is the tag push, not the push to
`main`"* applied to the note only, because the close-issues workflow fires
before the tag. The destination row in this branch's `spec.md` wrote the
conflated sentence, and phase 3 carried it over.

**Why it matters.** This is the claim #359 removed, arriving again: that the
close-issues workflow runs on the tag. It is also what ledger row S9's note
calls *"the shape this claim exists to refuse"*. A standing rule in `docs/`
outranks every spec, and the only record that argued the other way left with
the directory.

**Two smaller overclaims in the same bullet, folded into the fix.**
- *"falls back to the tag name when the title line is missing"*: the code also
  falls back when the line carries no symptoms (`1790076050`'s A4 divergence).
- *"goes red only when the changelog has no section"*: `main` also returns 1
  for a tag that is not `vX.Y.Z`, and `run` / `release_exists` call `sys.exit`
  on a failed `gh` call.

Nothing pins this paragraph. `tests/test_the_release_tail_does_not_end_at_the_tag.py`
pins the third-reader and fixed-name sentences only.

### 2. 🟡 The folded fold rules give opposite answers for a ledger hit, and 1790076070 Q4 lost its home

`docs/the-evidence-ledger.md:173-195`, rules (a) and (b).

- Rule (a): *"a permanent ledger row anchored inside it … holds the directory
  until the row is answered — so a work item with a row anchored in its
  `rounds/` stays on disk."*
- Rule (b): *"An anchor into a work item's `spec.md` or its round records …
  Each such row is decided by the rule `CLAUDE.md` gives: a row whose only
  anchor went is REMOVED … So a fold branch greps the ledger for its
  directories before it retires anything."*

For a row anchored in `rounds/`, (a) says keep the directory and (b) says
remove the row. (b) tells the next fold to grep before retiring, then gives no
answer for a hit. This branch's own `plan.md` phase 5 step 2 reads it the
REMOVED way; `1790076070` G3 kept `1788184145` for its `rounds/` anchor.

`1790076070`'s `questions.md` Q4 was an open person's question — keep the
directory, or remove the row and retire it — status ⬜. The G4 table (L1–L11)
enumerated overview rows only, so Q4 left with the directory and (a) now states
its default as a plain rule with no answerer.

**The fix** makes (a) state its default and who can overturn it, and orders
(b) so that a hit found before the removal keeps the directory, and the
REMOVED rule decides only what the grep missed.

### Checked and confirmed

- **1790076060.** Four markers sit on the item's own sentences in
  `docs/review-chain-spec.md`; the rules read against
  `chain_check.py#CAPPED_EXIT`, `round_record.py#DEPTH_EXIT` as described.
- **1790076080.** The `docs/measuring-a-run.md` paragraphs match
  `session_cost.py#post`. L10's rule matches `CONTRIBUTING.md` §*Hooks stay
  local and quiet*.
- **L1–L11.** Each is homed as `spec.md` G4 says.
- **Retired round records' `## Deferred` rows.** Every one is homed.

## Quality

### 3. ⬜ The agent-set sentence counts the marked headings, and the table also covers the `###` beneath them

`docs/the-agent-set.md:96-104`. *"tables every heading carrying the
`Orchestrator:` marker"* describes only half the row rule; the test also
covers every `###` directly beneath a marked `##`. So *"an act written without
the prefix is counted by nobody"* is false for a `###` inside a marked section.

### 4. ⬜ The L6 paragraph names half of what `CAPPED_EXIT` lags, and none of the prose twins

`docs/review-chain-spec.md:299-309`. `CAPPED_EXIT` also says the record's
`Fixes checked by` reads `no fixes to check`, which the cap subsection now
contradicts for a capped record that wrote fixes; and the four prose carriers
named in this item's §Not done are not in the paragraph, so the next fold
retires the only list of them.

### ⬜ correction: this work item's own records still describe the `b0cbd34` pin that G2 replaced

`spec.md` A3; `questions.md` Settled table; `plan.md` phase 2 row and the
alternatives row.

## ❓ Checked and not settled: the history rewrite

G2's grounds — the history is rewritten into a new repository after this
release — are recorded in no policy document, issue, `seal/follow-up.md` or
ledger row. The citation change stands on `skills/settle/SKILL.md` §2 alone.
The plan collides with `docs/branch-and-release.md`'s third-reader paragraph
if the plugin is ever listed in an outside directory that pins commits by SHA;
that is the repository owner's to answer.

## Regression tests to plant

- `tests/test_the_release_tail_does_not_end_at_the_tag.py`: a case asserting
  that the folded paragraph names the merge to `main` as what fires the label
  acts, and does not attribute them to the tag push. Seen red first.

## Facts for the evidence ledger

None.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🔴 The folded release-tail rule says the tag push fires all three acts; the label acts fire on the merge to `main`, and nothing fires the directory check | `docs/branch-and-release.md:43-73` | open | Read: `close-issues-on-release.yml` `on: push: branches: [main]`; no workflow runs `plugin_directory_check.py`; `docs/release-checklist.md` §6; `1790076050` spec judgment 2 |
| 2 | 🟡 Folded rules (a) and (b) give opposite answers for a ledger hit before retirement, and `1790076070` Q4 lost its home | `docs/the-evidence-ledger.md:173-195` | open | Read: (a) keeps, (b) REMOVES; `plan.md` phase 5 step 2; `1790076070` G3 and Q4 at base |
| 3 | ⬜ *"every heading carrying the marker"* omits the `###` rows | `docs/the-agent-set.md:96-104` | open | Read against `tests/test_every_orchestrator_act_names_its_delivery.py` |
| 4 | ⬜ The L6 paragraph omits `CAPPED_EXIT`'s `Fixes checked by` lag and the four prose carriers | `docs/review-chain-spec.md:299-309` | open | Read `chain_check.py#CAPPED_EXIT`; `overview.md` §Not done |
| ⬜ | `spec.md` A3, `questions.md` Settled row and `plan.md` still describe the `b0cbd34` pin | `seal/specs/1790119502-four-shipped-work-items-wait-unfolded/` | correction | Read |
| 🟢 | Ledger: only S9, C1, C3, C4 moved | `seal/ledger.md` | confirmed | Executed: `evidence-check --strict .` 1468 ok · 0 drifted · 0 broken |
| 🟢 | Floors: no literal lowered | `tests/` | confirmed | Executed: nine floor-table modules 665 passed, 1 skipped |
| 🟢 | No dangling reference into the four directories | tree | confirmed | Executed: grep for the four ids |
| 🟢 | Markers live, top level, one per line; the removals read as folds | `docs/` | confirmed | Executed: `unverified-check --baseline` exit 0; `chain_check` four `retired:`; `settle` 0 unfolded |
| 🟢 | Repo rules: identifiers, version timer, line wrap | `docs/`, `tests/` | confirmed | Executed |
| ❓ | The history rewrite behind G2 is recorded nowhere durable | `spec.md` G2 | ❓ out of verified scope | the repository owner's |

## Executed probes

| What was run | Result |
|---|---|
| `./bin/settle --released-at origin/main` | exit 0 · 0 unfolded · 11 ungrouped |
| `./bin/evidence-check --strict .` | exit 0 · 1468 ok · 0 drifted · 0 broken |
| `./bin/unverified-check --baseline origin/release/v0.13.2 seal/specs/` | exit 0 · four overviews folded |
| `chain_check.py --baseline origin/release/v0.13.2` | exit 1 · four `retired:` · one error: this item's absent `round-N.md` |
| `./bin/survivor-check --range origin/release/v0.13.2...HEAD --exempt …/survivors.md` | exit 0 |
| `./bin/correction-check --range origin/release/v0.13.2...HEAD` | exit 0 |
| `bin/test -q` over 13 modules pinning the edited documents | exit 0 · 298 passed |
| `bin/test -q` over the nine floor-table modules | exit 0 · 665 passed, 1 skipped |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `skills/settle/SKILL.md` §*What a fold branch owes* says *"Nothing in `seal/ledger.md` moves"*; both folds moved it | a comment on #511 | the repository owner |

## Paste-ready fixes

Finding 1 — replace `docs/branch-and-release.md` from its first `1790076050`
marker through the §6 sentence:

```markdown
<!-- specs/1790076050-the-release-tail-is-three-acts-no-document-names -->
**Every act the release performs once it reaches `main` belongs to a machine or
to a command that answers it, and none of them waits on somebody remembering.**
Three acts used to follow the merge that were assigned to whoever was at the
keyboard, written into no document and read by nothing — publishing the release
note, telling the plugin directory, spending the `size: now` label — and a step
a person can skip is a step that gets skipped: the note was missed three
releases running. Two different pushes fire them, and the difference is the
point. The merge to `main` fires the close-issues workflow, so the label is
created and spent before any tag exists. The tag push, the maintainer's last
act, fires the note, because a note has to name a tag.

- **The release note publishes itself.** `.github/workflows/publish-release.yml`
  fires on the `v*` tag push and publishes the `CHANGELOG.md` section the
  preparation commit already gathered, titled from the tagged commit's
  `release: X.Y.Z — <symptoms>` line (`docs/release-checklist.md` §5). It never
  republishes a release that exists, and falls back to the tag name when that
  line is missing or carries no symptoms. The red it exists to raise is a
  changelog with no section for the tag, which is the release shipping
  unexplained.
- **The plugin directory is read by a command that never fails a release.**
  `.github/scripts/plugin_directory_check.py` says, per directory, whether the
  plugin is listed, which commit the entry pins and whether that commit is on
  `main`, and it exits 0 whatever it finds: the directories sync on somebody
  else's schedule, and a red nobody here can act on is what `CLAUDE.md`'s first
  goal is against. Nothing fires it; a person runs it at the checklist's box.
  Submitting or resubmitting is a person's act.
- **A label a document specifies is created and spent by a workflow.** When
  the release reaches `main`, the close-issues workflow runs
  `.github/scripts/tracker_labels.py --apply`, which creates every declared
  label the tracker lacks, and takes `size: now` off each issue it closes.
  `docs/issues-and-milestones.md` owns what the label means; this says only who
  performs the acts. It states the design and not the tracker's state — whether
  the label exists is what `gh label list` says.

`docs/release-checklist.md` §6 carries a box for each of the first two. The
first confirms the workflow fired and is not where the note gets written; the
second is where the command is run.
```

Finding 2 — replace the first two `1790076070` paragraphs of
`docs/the-evidence-ledger.md`:

```markdown
<!-- specs/1790076070-the-fold-ships-and-the-corpus-is-still-on-disk -->
**A released work item that wrote no `spec.md` states no rule, and it is kept
by name.** `settle` names what it cannot group rather than guessing, and such
an item was below the SDD ladder: a release entry, a renumbering, a CI repair,
a pull request's record. Those are records of a moment, and a moment states
nothing to fold. An ungrouped item that did write a `spec.md` is folded where
that spec's rule belongs. One more reason keeps a directory: **a permanent
ledger row anchored inside it**, which holds the directory until the row is
answered — so a work item with a row anchored in its `rounds/` stays on disk,
and the fold does not remove it to tidy the list. Keeping the directory rather
than removing the row is a default, and the repository owner is who can trade
it the other way: remove the row, carry its claim into the prose it evidences,
and let the next `settle --retire` take the directory.

<!-- specs/1790076070-the-fold-ships-and-the-corpus-is-still-on-disk -->
**A retirement breaks every ledger row anchored inside the directory it
removes, and nothing refuses the removal first.** An anchor into a work item's
`spec.md` or its round records is a file path like any other, so after
`settle --retire` the checker reports it broken (#511 is the missing refusal).
So a fold branch greps the ledger for its directories before it retires
anything, and the frame that says *no row anchors there* is a count to open. A
hit found then is answered by the rule above: the directory stays. What the
grep missed is decided after the removal by the rule `CLAUDE.md` gives: a row
whose only anchor went is REMOVED, never re-pointed, and its claim is written
anew where a work item still holds it. A row that keeps a live anchor beside
the dead one loses only the dead one, and whether it should be removed instead
is the repository owner's question, recorded against the ledger row that first
met it.
```

Finding 3 (⬜, optional) — replace the `1790076080` paragraph of
`docs/the-agent-set.md`:

```markdown
<!-- specs/1790076080-every-orchestrator-rule-is-a-sentence -->
**The orchestrator's acts are counted, each against what delivers it.** An
agent's rules arrive by mechanism, while the orchestrator has no spawn for a
preload to attach to, so each of its acts is a sentence until something
refuses when the act did not happen. `skills/implement/orchestration.md`
tables every `##` heading carrying the `Orchestrator:` marker in both
orchestration files, and every `###` directly beneath one, against its
delivery — a command, a check, part of its parent's act, or still a sentence
with its grounds — and a test holds the table against both files from both
sides. That test reads the marker and not the meaning, so an act written
outside a marked section is counted by nobody.
```

Needs a fix: yes — finding 1 (the folded release-tail rule names the wrong trigger for the label acts) and finding 2 (folded rules (a) and (b) contradict each other, and 1790076070 Q4 lost its home)
Loses a record or crashes: no
