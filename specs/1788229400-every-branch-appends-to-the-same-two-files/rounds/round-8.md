# 1788229400-every-branch-appends-to-the-same-two-files — review round 8

The verifying round for round 7's fixes, and the round that read what
`round-7.md` had recorded as read by nobody. Its three findings are closed;
round 7's are confirmed closed with it.

| Field | Value |
|---|---|
| Target SHA | `3d7a297` |
| Diff base | `19c338c` — the state round 7's record was written at |
| Fixes for this round's findings | `a88f5bb` |
| PR | #65, `release/v0.2.0` → `main` |
| Broad gate | not yet — CI's three-OS matrix answers it, and the windows leg is the only thing that can settle five items `overview.md` still lists |
| Fixes checked by | `nobody — the orchestrator wrote `a88f5bb` itself and planted three cases seen red without it; no round has opened them` |
| Needs a fix | yes — 🔴 A, 🔴 B, 🔴 C and 🟡 F, all closed at `a88f5bb` |

- [ ] Pass

## Round 7's three, answered

| # | Answer | Settled by |
|---|---|---|
| 🔴 M | **fixed** `a43ef64` — the check names the unsure place and its hash (`1-2@ea700c86`), and recording that hash by hand gives `1 ok`, exit 0. `--migrate` refuses without a stamp and anchors with one | executed, both trees |
| 🔴 L | **fixed** `a43ef64` for one-line calls — Kotlin `render(1)` left behind reads `BROKEN … identical content at src/Other.kt#render (moved?)` and `--reverify` heals to the destination. A call whose arguments are wrapped across lines is untouched, and was untouched before: 🟡 E below | executed |
| 🟡 N | **fixed** `a43ef64`, two of three — a file with no candidate says `no place — the check calls this row BROKEN`, and a row the check calls `1 ok` draws no contradicting line. The third survived in one branch: 🟡 F | executed |

## Verdicts

What this round opened. 🔴 A and 🔴 B are both regressions from `a43ef64`,
and both break a rule this repository wrote down for itself.

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 A | Round 7 dropped a `not claim` guard from the tie-break, so a claim row on a place the declaration rule is unsure of is called GONE and reported BROKEN — while the anchored statement is still there, in the file, at the lines the message disowns. `CLAUDE.md` is explicit: *an anchor degrades to DRIFTED, never to BROKEN. Only the major level can be BROKEN.* It also turns exit 1 into exit 2, which `test.yml` reads as a red build, and puts the row in every commit's advisory | `evidence_check.py:890` · `:902` | **fixed** `a88f5bb` | Reviewer-executed on both trees, `.cs` fixture. **Orchestrator-executed after the fix**: the same fixture reads `DRIFTED … re-verify`, exit 1, with no BROKEN in the output. §Q3 licensed BROKEN for *several* places, on grounds that invert here — a single place's DRIFTED is one `--reverify` answers |
| 🔴 B | The other direction, and worse. `places = hit[:1]` breaks a tie with the row's recorded hash — but a claim row's hash is the **minor region's**, which two unrelated units share the moment they hold one identical line. Two C# overloads of one name went from `BROKEN … ambiguous`, exit 2, to a silent `1 ok`, exit 0, arbitrarily anchored to the first. Delete that overload later and the row points at the other one, still green | `evidence_check.py:899` | **fixed** `a88f5bb` | Reviewer-executed both trees. **Orchestrator-executed after the fix**: exit 2, `ambiguous` restored. This is the silent pass §Q3 refused at the major level, arriving at the minor one |
| 🔴 C | The printed remedy for 🔴 M is the **major** unit's hash, while a claim row is compared against the minor region's. Recording the printed hash reproduces the same BROKEN, and the line then also carries `— identical content at #Render (renamed?)`, asserting in one sentence both that nothing holds the content and that something does. No command or edit could make such a row pass | `evidence_check.py:925-934` | **fixed** `a88f5bb` | Reviewer-executed. Closed by 🔴 A's fix, which removes claim rows from that path entirely — no separate change |
| 🟡 F | `--reverify`'s `path escapes the repository` line dropped `>"claim"` from the coordinate, so two claim rows on one unit print as one line. Every other line it prints carries the claim | `evidence_check.py:1211` | **fixed** `a88f5bb` | Reviewer-executed. `left_as` was computed four lines below its first use; it moved up |

## Judged, and both stand

**The `--migrate` `proved` exception** is sound and stays. Executed both ways: a row without a stamp is refused with the same prescription and the ledger stays byte-identical; with a stamp vouching for the cited lines it anchors as before, and deleting `and not proved` reddens exactly one case. Two limits are recorded rather than fixed — `proved` sits behind `repo == root`, so a `legacy-parity` project pointing at its original with `--default-repo` never receives the exception although it is the likeliest holder of a pre-anchor ledger; and the message it gets says the stamp cannot vouch for the lines when the code never read that stamp.

**The span bound** works as claimed — `render() {` with an indented body stays a sure declaration, and `generic_units(["render(y)"], "render")` is the discriminating half. Its boundary is *is this one line*, not *is this a call*, which is what 🟡 D and 🟡 E below are.

## Recorded as limits rather than fixed (🟡)

- **🟡 D — every one-line declaration is now unsure, and the cost is wider than the document admits.** `SKILL.md` says a one-line bare-name declaration is unsure; it does not say that an ordinary edit to a one-line JS method then goes DRIFTED → BROKEN, that CI turns red for it, that `--reverify` cannot undo it, or that `--migrate` refuses the row so the prescribed recovery does not terminate. It is the price of closing 🔴 L, and reverting it brings 🔴 L back. The premise that one-line declarations are rare does not hold for JS, Ruby, Lua or GNU-C.
- **🟡 E — 🔴 L does not reach a call whose arguments are wrapped across lines.** `j == i + 1` sees one-line calls only. Identical on both trees, so not a regression; it is the hole left open since round 5's 🔴 C, and it narrows 🔴 L's sentence rather than reopening it.

## Recorded without a fix (🟢)

`SKILL.md:122-124` and `:248-249` say `--reverify` refuses to write onto an
unsure place at all; it refuses on the place alone and writes where the
recorded hash reconstructs, which is what the code and `overview.md`'s *What
was NOT changed* both describe. `overview.md:417-420` credits round 7 with
`file_units` no longer calling `resolve`, which was already true at
`19c338c`. `overview.md:483-485` overstates by a clause. `cross_repo_intent`'s
summary still names three inputs it no longer takes, and `resolve_unit`'s
docstring still explains its flag as keyword-blocking alone. `plan.md:73` says
eleven new cases where there are ten. Three arms of `--reverify`'s
left-behind reporting are unpinned — deleting them leaves the suite green.

## Executed by the orchestrator, after the fixes

Three fixture repositories, `&&` chains, run against the committed tree: the
`.cs` stale-claim case (🔴 A), the two-overload case (🔴 B), and the escaping
row's `--reverify` line (🟡 F). All three were **first run against the tree
without the fix and seen red**, then green with it, and they are planted in
`tests/test_a_row_points_by_content.py` rather than deleted. 218 cases across
seven files green; `ruff check` and `ruff format --check` clean on the two
changed files; this repository's ledger at `58 ok · 0 drifted · 0 broken`.

One ledger row was **narrowed rather than re-pointed**: the row claiming the
recorded hash decides a tie and an unsure place now says *at the major level
only*, because 🔴 A and 🔴 B are the discovery that it never held for a claim
row. Its claim reversed, so the sentence is what had to change.

## Why `Pass` is not checked

`a88f5bb` was written by the orchestrator and read by nobody. Three cases seen
red without it is evidence that the fixes do what they say; it is not a second
person checking. The field says `nobody` and the box stays empty, which holds
this pull request as a draft until somebody opens that diff — thirty lines, in
one file, plus its three cases.

That is `1788212517`'s mechanism working on the work item that came after it,
for the second time in this run.

## Deferred

🟡 D and 🟡 E stay open as recorded limits, named in #65's body. The
documentation mismatches under 🟢 go with them.
