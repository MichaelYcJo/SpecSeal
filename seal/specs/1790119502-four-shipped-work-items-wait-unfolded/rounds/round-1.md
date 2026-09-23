# 1790119502-four-shipped-work-items-wait-unfolded — review round 1

| Field | Value |
|---|---|
| Target SHA | d0282bf |
| Written late | no |
| Ran by | warden on claude-opus-5-5 |
| PR | #516 |
| Broad gate | not yet |
| Fixes checked by | round-2 |
| Fix range | `3bbc2194e89f0e997d8e0450c050b20f0b5da040..96caaea8ef59ec39fe379405a17bdf991d2526e1`, 6 commits |
| Contract changes | none |
| New units | release_tail_rule (depth 1); test_the_label_acts_are_fired_by_the_merge_to_main_not_the_tag (depth 1) |
| Needs a fix | yes — finding 1 (the folded release-tail rule names the wrong trigger for the label acts) and finding 2 (folded rules (a) and (b) contradict each other, and 1790076070 Q4 lost its home) |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 1 at `d0282bf`, spec compliance then quality. Asked: whether every rule still governing in the four retired specs reached `docs/` and nothing overturned did; whether any open leftover vanished without a home; that the ledger moved only the four re-verified rows; that no floor was lowered; that nothing dangles into the retired directories; and the repository rules for identifiers, versions and line wrap. The orchestrator verified findings 1 and 2 by opening their coordinates: `close-issues-on-release.yml` fires on `push: branches: [main]`, no workflow runs `plugin_directory_check.py`, and rules (a) and (b) at `docs/the-evidence-ledger.md` answer a `rounds/` anchor opposite ways. The ❓ on G2's grounds is answered by the owner: the history rewrite is planned outside this repository's tree, and G2's change stands on `skills/settle/SKILL.md` §2 alone.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🔴 The folded release-tail rule says the tag push fires all three acts; the label acts fire on the merge to `main`, and nothing fires the directory check | `docs/branch-and-release.md:43-73` | **fixed** `71c33d1` | fixed at 71c33d1; Read: `close-issues-on-release.yml` `on: push: branches: [main]`; no workflow runs `plugin_directory_check.py`; `docs/release-checklist.md` §6; `1790076050` spec judgment 2 |
| 2 | 🟡 Folded rules (a) and (b) give opposite answers for a ledger hit before retirement, and `1790076070` Q4 lost its home | `docs/the-evidence-ledger.md:173-195` | **fixed** `4ee07f9` | fixed at 4ee07f9; Read: (a) keeps, (b) REMOVES; `plan.md` phase 5 step 2; `1790076070` G3 and Q4 at base |
| 3 | ⬜ *"every heading carrying the marker"* omits the `###` rows | `docs/the-agent-set.md:96-104` | **fixed** `e2ec58e` | fixed at e2ec58e; Read against `tests/test_every_orchestrator_act_names_its_delivery.py` |
| 4 | ⬜ The L6 paragraph omits `CAPPED_EXIT`'s `Fixes checked by` lag and the four prose carriers | `docs/review-chain-spec.md:299-309` | **fixed** `b6544f6` | fixed at b6544f6; Read `chain_check.py#CAPPED_EXIT`; `overview.md` §Not done |
| ⬜ | `spec.md` A3, `questions.md` Settled row and `plan.md` still describe the `b0cbd34` pin | `seal/specs/1790119502-four-shipped-work-items-wait-unfolded/` | correction | Read |
| 🟢 | Ledger: only S9, C1, C3, C4 moved | `seal/ledger.md` | confirmed | Executed: `evidence-check --strict .` 1468 ok · 0 drifted · 0 broken |
| 🟢 | Floors: no literal lowered | `tests/` | confirmed | Executed: nine floor-table modules 665 passed, 1 skipped |
| 🟢 | No dangling reference into the four directories | tree | confirmed | Executed: grep for the four ids |
| 🟢 | Markers live, top level, one per line; the removals read as folds | `docs/` | confirmed | Executed: `unverified-check --baseline` exit 0; `chain_check` four `retired:`; `settle` 0 unfolded |
| 🟢 | Repo rules: identifiers, version timer, line wrap | `docs/`, `tests/` | confirmed | Executed |
| ❓ | The history rewrite behind G2 is recorded nowhere durable | `spec.md` G2 | ❓ out of verified scope | the repository owner's |

## Paste-ready fixes

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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `skills/settle/SKILL.md` §*What a fold branch owes* says *"Nothing in `seal/ledger.md` moves"*; both folds moved it | a comment on #511 | the repository owner |
