# 1788229400-every-branch-appends-to-the-same-two-files — review round 7

The verifying round for round 6's fixes, and **the last round of this run.**
Round 6's two are closed. Three more opened, they were fixed, and nobody
reviewed those fixes — which is why `Fixes checked by` reads what it reads and
`Pass` is not checked.

| Field | Value |
|---|---|
| Target SHA | `19c338c` |
| Diff base | `f2f2ef0` — the state round 6's record was written at |
| Fixes for this round's findings | `a43ef64` · `3d7a297` |
| PR | opened as a draft — see below |
| Broad gate | not yet — deferred to CI, whose three-OS matrix answers five open items no local run can |
| Fixes checked by | `nobody — the run reached its bound at round 5 and ran two rounds past it; the orchestrator re-executed this round's three reproductions at 3d7a297 instead of spawning a round 8` |
| Needs a fix | yes — 🔴 L, 🔴 M, 🟡 N, all closed at `a43ef64` |

- [ ] Pass

## Round 6's two, answered

| # | Answer | Settled by |
|---|---|---|
| 🔴 J | **fixed** `6f564d3` — the moved `.js` unit reads `BROKEN … identical content at src/other.js#render (moved?)` at exit 2, and `--reverify` heals to the true destination instead of nailing the row to the call | executed, both trees |
| 🟡 K | **fixed** `6f564d3` — a source file inside the `--default-repo` checkout symlinked out of the tree is `BROKEN … path escapes the repository` at exit 2, where `f2f2ef0` read `1 ok`. A link-free `--default-repo` row still resolves | executed |

## What this round opened, and how each was closed

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 M | A blocked declaration could no longer be recorded in a ledger **at all**. `--reverify` refused it, and the check said `locator not found` while the unit sat at lines 1-2 — a false sentence — so a brace-language project could not bootstrap. `Known limits` prescribed a hand edit that no command made performable, because nothing printed the unit's hash. A regression against `f2f2ef0`, where the same row read `1 ok` | `evidence_check.py:1193` · `:871` | **fixed** `a43ef64` | Reviewer-executed both trees. **Orchestrator-executed after the fix**: a `.cs` file holding only `public new void Render(int x) {`, a row with a placeholder hash — the check answers `the declaration rule is unsure of the only place it found … 1-2@c4a9dd25; record one by hand if it is still the unit`, and recording that hash gives `1 ok`, exit 0 |
| 🔴 L | For languages without semicolons — Swift, Kotlin, Go, Ruby, Lua — a moved unit still anchored to its call site permanently. Identical to 🔴 J, which was closed for `.js`. **Not a regression**: the same in both trees | `evidence_check.py:384` → `:401` | **fixed** `a43ef64` | Reviewer-executed. **Orchestrator-executed after the fix**: Kotlin, `fun render` moved to `src/Other.kt` leaving `render(1)` — `BROKEN … identical content at src/Other.kt#render (moved?)`, and `--reverify` re-anchors to `src/Other.kt#render` |
| 🟡 N | Three sentences the round-6 commit introduced, none of them true: `generic_units` returned "resurrected" for a file with no candidate at all; `--reverify` called a row ambiguous that the check had resolved to `1 ok`, because the hash tie-break rounds 5 and 6 gave `check_ledger` was never given to `reverify`; and the coordinate dropped its `>"claim"` | `evidence_check.py:410` · `:1201` | **fixed** `a43ef64` | Reviewer-executed all four cases. **Orchestrator-executed after the fix**: a file with no candidate now reads `no place — the check calls this row BROKEN`, and a row the check calls `1 ok` draws no contradicting line from `--reverify` |

Five 🟢 the round also recorded — the phantom re-anchor on an unchanged blocked
row, the remaining silent paths in `--reverify`, `resolve`'s zero consumers,
`cross_repo_intent`'s dead parameters, and a ledger row claiming more than its
evidence — were all closed in the same commit.

## The implementer's one deliberate narrowing, and it stands

The brief said both writers refuse an unsure place. `--migrate` refuses **except
when `proved`**, and the grounds are that the two commands hold different
evidence: `--reverify` asks whether it may overwrite the row's recorded content
claim and has nothing but the place, while `--migrate` asks which unit contains
the lines the row already cites, and the old stamp proving those lines unchanged
makes the human-written line numbers evidence for that place. Without the
exception a `.cs` or `.kt` project could not migrate a pre-anchor ledger at all —
every row citing a blocked declaration would be left behind, and those are
exactly the rows the check accepts. Both directions are pinned, and reverting is
deleting `and not proved`, which reddens a case that names itself.

## Why there is no round 8

`docs/review-chain-spec.md:34-42` bounds this run at five rounds. It ran seven.
The structure signal at `generic_units` fired at round 5 and again at round 6,
and the run continued past both. Adding an eighth round to read a thirty-line
change would repeat the decision that produced the excess.

So the three fixes above were **not** read by a reviewer. What was done instead:
the orchestrator re-executed this round's three reproductions against the
committed fixes, independently of the implementer's report — the results are in
the Grounds column above. That is less than a round and it is recorded as less
than a round: `Fixes checked by` says `nobody`, `Pass` is not checked, and
`hygiene.yml` therefore requires this pull request to stay a **draft**. Marking
it ready needs somebody to read `a43ef64`, or a round 8 whenever one is cheap.

That refusal is `1788212517`'s own mechanism working as designed, on the work
item that came after it.

## Executed by the orchestrator, after the fixes

Three fixture repositories built with `&&` chains, run against the committed
tree at `3d7a297`: the Kotlin move (🔴 L), the `.cs` bootstrap round trip
(🔴 M), and two of `--reverify`'s message cases (🟡 N). Each is quoted in the
verdict table.

Not run here, deliberately: the full suite, tree-wide `ruff`, and any typecheck.
CI runs `pytest tests/ -q -n auto` and both `ruff` checks across
ubuntu · macos · **windows**, and the windows leg is the only thing that can
answer the five filesystem items `overview.md` still lists as unverified. A
local macOS run is a strict subset of that, so it was skipped rather than
deferred.

## The implementer's own verification, as reported

Eleven new cases, eight seen red against the unfixed tree first and three
controls discriminated by mutation instead. Twelve mutations, all killed —
**two survived at first and both were the pin's fault, not the mutant's**: a
control using `function render(x) {` never touched the span bound it was meant
to guard, and a case checking for the absence of the word `resurrect` did not
notice a message that no longer uses it. Both pins were strengthened until the
mutants died. 269 cases across eleven files green; this repository's ledgers at
`58 ok · 0 drifted · 0 broken`, exit 0.

## Deferred

Nothing from this round. What leaves this work item unfinished is written up
elsewhere and named in the pull request body: the regression-correction rows in
issue #57, the measured segment costs in #51, and the draft advisory for the
path-traversal finding, which publishes at release.
