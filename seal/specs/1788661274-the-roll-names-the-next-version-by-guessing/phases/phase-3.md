# 1788661274-the-roll-names-the-next-version-by-guessing — phase 3

<!-- seal/specs/1788661274-the-roll-names-the-next-version-by-guessing/phases/phase-3.md -->

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | `181e17b` |
| Ran by | |

## What this phase was asked

The closing set, in this order. `overview.md` first, because
`test_every_spec_directory_that_reached_the_ladder_has_an_overview` is red on
this branch and that file is what closes it; its §*Where spec and
implementation diverged* has a real row, `spec.md`'s first acceptance scenario
against what was built, with both sides quoted verbatim and `spec.md` left
alone. Then the ledger fragment — not appended to `seal/ledger.md`, no header,
and every claim this work item makes is in it, because neither earlier phase
wrote a row. `seal/ledger.md`'s F5 is a re-read rather than a new row: its
`Checked` date moves and a clause names what moved. Then the changelog
fragment, matching the shape and heading level of
`seal/specs/1788632199-…/changelog.md`, carrying what a title means now and
what the older ones mean, since it reaches the release notes. Then
`docs/flow.md`'s #155 box and nothing else.

Both `evidence-check` forms are run and read: the scoped `--reverify --ledger`
for the fragment's own rows, then the **unscoped** read to see what this
branch drifted elsewhere. One drift, `templates/config.md#"# Repository
config"`, is pre-existing at the branch base and is not this branch's to
touch. `--reverify` cannot narrow below a file, so a shared row nobody here
read must not be re-stamped by a blanket run — the new hash comes from a copy
and the row is edited by hand.

## What this phase found

**The unscoped read found six drifted rows, and the handoff named one.**
The prompt named F5 and the pre-existing `templates/config.md` drift, and
`seal/ledger.md` also carried F1, F2, F4 and F6 — four rows from work item
1788486395 about the roll script — while another work item's fragment,
`seal/ledger/1788613827-…`'s R3, carried the same skill-section anchor F5
does. Phase 1 changed `open_issue`, `issue_body` and `main`; phase 2 changed
the skill section; neither phase reached the ledger at all, so every one of
those rows had been left saying *re-verify* by a branch that never opened it.

That is #153's own lesson arriving from the other side. Its work item is in
`docs/flow.md` for the case where the scoped form reports a clean ledger while
the branch has broken rows in the shared one — three rounds clean, fifteen
drifted rows at the broad gate. Here the scoped form reported `19 ok · 0
drifted` for this work item's fragment, correctly, on a branch with seven
drifted rows elsewhere. **The unscoped form is what makes the difference
visible, and it belongs in a phase's verification rather than in the broad
gate**, because at the broad gate a fix is an edit after a run that was
supposed to be the last one.

**Each of the six was judged rather than re-stamped, and the scratch copy is
what made that possible.** The hashes were taken by copying the coordinates
into a file outside the tree and running the scoped write form against it, so
the new value arrived without any row being rewritten. What the same run also
said is which anchors did **not** drift, and that is the half that decides the
judgment: `landed_create` (F1's guard, with the exclusion, the retry and the
sleep in it), `try_run` (F2's contrast), and F5's other two coordinates all
answered `ok`. So in every case the drift is in a unit the claim mentions and
not in the sentence the claim makes:

| Row | What moved | What the claim rests on |
|---|---|---|
| F1 | `open_issue`'s version parameter renamed, its title moved behind `log_title` | `landed_create`, unchanged |
| F2 | the same rename, and the case's expected title | the last rung still calls `run`, the two above it `try_run` |
| F4 | `issue_body`'s opening sentence, and the case reading it | `ledger` is still a separate string joined in, not a conditional inside one f-string |
| F6 | `main` gained the guard and two printed lines; the recovery message names `log_title(shipped)` | the hedge — check the label first, the create may have landed — is word for word |
| F5 | the skill's two-logs sentence | the section still names no issue number, no milestone, no label existing here alone |
| R3 (another fragment) | the same sentence | the run-level table, its nine rows and their sources, untouched |

**F5 turned out to have decided something rather than only recorded an
absence, and its re-read clause says so.** The title the roll now writes is
tracker state existing in this repository alone, which is exactly what that
row keeps out of the shipped skill — so the format went to
`docs/issues-and-milestones.md` and the skill got the boundary alone. G5 in
this work item's fragment is the presence F5 is the absence of, and each row
now names the other.

**Five rows, and the fifth is not a second copy of F5.** Phase 2 named four
candidates. Three became rows on their own because each is a decision between
two things that both look correct in the file — the condition (G1), the
direction an unreadable title takes (G2), and the writer/reader constant (G4)
— and a fourth was split out of G1 rather than folded into it: both outcomes
exit 0, so the two printed lines are the only thing telling a release that
rolled from a mechanism that stopped, and the tidy-up that deletes a `print`
as noise is a different one from the tidy-up that deletes the guard (G3). The
fifth, the two documents, earns a row for the same reason the others do and
in the opposite direction from F5: F5 refuses a sentence in the skill, G5
requires two in the tracker document, and neither is derivable from the other.

**One candidate earned no row, and the check was a read rather than an
assumption.** `next_version`'s removal: a row whose anchor a change removes is
removed rather than re-pointed, and there was none to remove. `grep -rn
next_version seal/` returns an older work item's `spec.md`, `plan.md`, round
record and phase records, and this work item's own documents — no ledger row
anywhere, which is what `phases/phase-1.md` asserted and what this phase
confirmed by running it.

**`## Not verified` carries five rows and the prompt named three.** The three
are the orchestrator's broad gate. The fourth is that this script has never
run against real GitHub: every case in the module fakes `subprocess.run`, so
what is pinned is what the script asks `gh` for and what it does with the
answers, and the first live run is the 0.8.2 release itself — the one that
rolls `#172`, whose title the old convention wrote. The fifth is the
divergence: `phases/phase-1.md` says the reviewer settles it, so it is an
open item with an answerer rather than a decision this phase can close.

**Nothing was mutation-tested in this phase, and nothing needed to be.** It
adds no unit and no case; the one check it closes,
`test_every_spec_directory_that_reached_the_ladder_has_an_overview`, was seen
red at `4695eae` before `overview.md` existed and green after it, which is
the same evidence in the opposite direction.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `docs/flow.md`'s open `- [ ] #155` row, ticked here. That section is deleted outright at the release, by the file's own rule | The changelog fragment, which reaches the release notes; the issue itself; and this work item's records. All three are the durable copies the flow file defers to |
| Nothing else. No prose, no code and no case left the tree in this phase | none |
