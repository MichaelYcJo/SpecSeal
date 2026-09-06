# 1788661274-the-roll-names-the-next-version-by-guessing — overview

<!-- seal/specs/1788661274-the-roll-names-the-next-version-by-guessing/overview.md -->

📋 implement applied
· spec:     `spec.md`, `plan.md` (§Alternatives, §Phases row 3), `questions.md`,
            `routing.md`, `phases/phase-1.md`, `phases/phase-2.md`;
            `CLAUDE.md` §*a change writes fragments, never the shared file* and
            §*A ledger coordinate names content, never a position*;
            `seal/ledger.md` F5 and its `Coordinates` section;
            `docs/flow.md` §0.8.2; `templates/sdd-overview.md`,
            `templates/sdd-phase.md`, `templates/ledger.md`
· evidence: G1–G4 in
            `seal/ledger/1788661274-the-roll-names-the-next-version-by-guessing.md`;
            F5 in `seal/ledger.md` re-read rather than re-written
· verified: **executed** — `test_chain_hooks_hardening`,
            `test_the_set_a_work_item_always_has`, `test_unverified_rows_close`,
            `test_a_row_points_by_content`, `test_evidence_check`,
            `test_the_ledger_fragments_fold_at_release`,
            `test_the_changelog_is_gathered_at_release`,
            `test_no_real_identifiers`, `test_docs_line_wrap`, and both
            `evidence-check` forms. **Read** — the four units and six cases each
            ledger row cites, opened at `4695eae` before the row was written.
            **Unverified** — see §Not verified

## Why this work exists

The roll that opens each measurement log named it by predicting the next
version, and at the 0.8.1 release that prediction closed a log the next
release still needed; now the log is named after the version it rolled from,
which is a fact, and it rolls only where a new version has actually shipped.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| Whether a patch release rolls | `spec.md` §User scenarios & acceptance, row 1: *"A patch release rolls nothing \| Given the open log names a version the tree has not shipped · when the roll runs · then it exits **0**, says nothing was due, and closes no issue \| a case over `main` with a faked `gh`"*. What was built: a patch release **does** roll, and the run that closes nothing is *a push that shipped no new version* — `main`'s guard is `if not roll_is_due(title, shipped)`, and `roll_is_due` is `rolled_from(title) != shipped`, which compares two version strings for equality and asks nothing about minor versus patch | The implementation. `spec.md` is left exactly as written | The scenario was written in the losing shape's frame. `plan.md` §Alternatives row 3 — *predict, but only roll once the prediction is confirmed* — is where a title is a prediction and a patch release is therefore the case that must not fire; the winner is row 2, where the title names the version the log **rolled from**. Under the winner the log a patch release closes is named after the version before it and holds exactly the work that patch shipped, so closing it loses nothing and the 0.8.1 incident cannot recur. The scenario's substance is kept and pinned by `test_a_push_that_shipped_no_new_version_rolls_nothing` |

**Why `spec.md` was not edited to match.** Rewriting an acceptance row into
what was built is how a spec stops being worth reading: the row would then
record no decision, and the one decision this work item was delegated —
`questions.md` question 5, *"Named, not chosen — the trade is what the work
item settles"* — would be invisible in the file that asked for it. The
divergence is recorded here and in `phases/phase-1.md`, with both texts, so a
reader who opens the spec first has somewhere to go.

**What the scenario's literal example is still reachable through.** Two
things, and rolling is the correct act in both. A title written before this
change — `chore: flow measurement — 0.9.0` — names a version that has not
shipped, and it is due whatever the tree ships, which is what retires the old
convention at the first release rather than by hand
(`test_a_title_written_before_this_change_is_always_due`). And a title edited
by hand is read the same way, because a title this script cannot read as its
own falls toward *due* rather than toward silence
(`test_a_title_the_roll_cannot_read_is_due_rather_than_silent`).

## Not verified

| Item | Who must answer |
|---|---|
| The full suite | the orchestrator, at the broad gate after the review rounds (contract §2) |
| The repository-wide lint | the orchestrator, at the same gate |
| The typecheck | the orchestrator, at the same gate |
| The roll against real GitHub. Every case in the module fakes `subprocess.run`, so what is pinned is what the script asks `gh` for and what it does with the answers, never a live `gh issue list` or `gh issue create` | the 0.8.2 release itself, which is the first run of this code against the real tracker — and the run that rolls `#172`, whose title the old convention wrote |
| Whether the divergence above is accepted. It is the one judgment in this work item a person may want to overturn, and `phases/phase-1.md` says the reviewer settles it | the review chain |

## Not done

**`spec.md` is left as written**, for the reason above.

**Closed logs are not retitled**, and neither is the one open before this
change. `questions.md` assumption 6: #155 asks for the mechanism to stop
guessing, not for history to be rewritten, and a rewritten title falsifies
every comment that cites it. What the older titles mean is said in
`docs/issues-and-milestones.md` instead, and pinned by
`test_the_tracker_doc_says_what_a_title_written_before_this_means`.

**The one-open invariant and its single retry are untouched**, and so is the
durable `flow-baseline` log. `spec.md` §Out names all three, and one of them
caught a real fault on the run that measured this issue.

**`docs/flow.md`'s #169 box is not ticked.** That item is not this branch's
work, and the file's own rule is that a branch writes the rows its own work
created or closed.

**No row was written for `next_version`'s removal.** A row whose anchor a
change removes is removed rather than re-pointed, and there was none to
remove: `seal/ledger.md` cites that function in no row, which was confirmed
by reading rather than assumed — `grep -rn next_version seal/` returns only
an older work item's `spec.md`, `plan.md`, round record and phase records,
and this work item's own documents.

## Fed back into the spec

None. The one clause this work item was delegated — how the open log's
version is known, and what the next log is called — was settled in
`plan.md` §Alternatives before the first edit, which is where `spec.md` §The
fork this work item settles sent it. Nothing was inferred into `spec.md`
during implementation, and the one place the two disagree is recorded above
rather than folded back in.
