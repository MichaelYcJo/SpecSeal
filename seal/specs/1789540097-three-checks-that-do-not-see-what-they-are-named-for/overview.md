# three checks that do not see what they are named for — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens rather
than reconstructed at the end. Facts that must outlive this work item go to the
evidence ledger, not here. -->

📋 implement applied
· spec:     `seal/specs/1789540097-…/spec.md`, `plan.md`, `questions.md`,
            `routing.md`; `seal/config.md` (no `Record language` row, so the
            records are English); `CLAUDE.md` §*a change writes fragments*,
            §*a ledger coordinate names content*; `agent-contract` §5, §12,
            §15; `skills/implement/SKILL.md` §3, §4
· evidence: `seal/ledger/1789540097-three-checks-that-do-not-see-what-they-are-named-for.md`,
            and one row re-read in
            `seal/ledger/1789518345-who-asks-the-routing-question-and-what-checks-the-answer.md`
· verified: see `## Not verified` below; each phase record names what it ran

## Why this work exists

Three checks this release wrote were each passing while the axis they are
named for was free to be wrong; each now goes red under the mutation its own
issue had already measured green.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| How many members `flat` folds across both sweeps | `spec.md` scope item 2: *`flat` folds only `.py` members, and there are four across both sweeps*; `spec.md` A5: *the comment names the `.py`-only fold and the four members* (found by round 1 — a fourth statement of the same number); `plan.md` §*Technical context*: *Two sweeps search four folded members between them*; #418: *Across both sweeps exactly four members are `.py`* | **Five**, derived from the module's own lists in phase 2 | Measured: `seal_stamp.py`, `round_record.py` and `broad_gate.py` in `SEAL_SWEPT`; `session_cost.py` and `tests/test_session_cost.py` in `SEGMENT_SWEPT`. The closure ARGUMENT is untouched — `swept` is still every phrase either sweep searches for in the folded members — so only the count was wrong, and it had reached three documents unopened. The case now pins the list itself rather than a number beside it (`agent-contract` §5: an aggregate is not a coordinate) |
| How many documented widths in the wrap module have drifted | #422 reports one: `agents/smith.md` at 148 where 109 is measured. `spec.md` scope item 7 carries that one | **Two**, plus one restatement of the first | `skills/implement/SKILL.md` is documented at 99 and measures 90; nobody reported it. `COVERED`'s own comment restates the stale 148 a second time. `agent-contract` §12 — the fix is owed to every instance the cause produces, and the cause is a measurement written down by hand |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and the typecheck. Every phase ran only its own module; the broad gate is one act with one owner | the sealer, spawned by the orchestrator after the rounds settle (`agent-contract` §2) |
| Whether the `cmd.exe` half of the two `&` cells is TRUE. Phase 1 pins that the document attributes each behaviour to a shell, never that the behaviour is that shell's | the `windows-latest` job, as work item `1789445605-…` already records |
| **The #422 sweep's own call**, as opposed to its read. Round 2's 🟡 7: with the read and the loop now reported and asserted, `batch_instructions("")` — the function called on something other than what was read — is still exit 0. Closing it means observing the call, which means a walk a case drives with a planted definition file; that is mechanism a fix pass may not add on top of a unit an earlier fix pass created, and a planted corpus is a change to what the suite guards that `CONTRIBUTING.md` asks a separate argument for | the repository owner, as a new issue — the paste-ready `definitions_with_batch_instructions` and its case are in this work item's `rounds/round-2-report.md`, measured at 52 passed | <!-- NAME NOT IN TREE: a name proposed for the walk this row declines to build, not a unit that exists. The row is about why it is not here. -->
| Whether `skills/code-review/scripts/chain_check.py:668` — *Named for the COMMAND that writes it, not for the seal* — should be brought under `SEAL_SWEPT` with an exclusion. Surfaced by phase 2's second mutation; it discusses the word rather than using it, which is the shape both existing exclusions have. **And whether `agents/scribe.md` joins the same list** — round 1 found it the one definition absent from it, pre-existing rather than this branch's, with zero occurrences of the swept phrase today | the repository owner, as a change to what a test guards (`CONTRIBUTING.md`) |

## Not done

**`chain_check.py` was not added to `SEAL_SWEPT`.** Phase 2's second mutation
is exactly that addition, and under it the sweep case went red on a real
occurrence. Reading it settles that the occurrence discusses the word rather
than leaving an instance anonymous, so bringing the file under the sweep needs
a `SEAL_EXCLUDED` entry — which is a change to what a test guards and a
separate argument. It is in `## Not verified` above with an answerer rather
than done quietly here.

**No assertion that the sweep cases read the phrase constants** —
`questions.md` Q3, answered `leave it` with the two reachable shapes and why
each is refused. The risk is written beside `SEAL_BARE`.

**#422's window still crosses headings, and that is deliberate.** `spec.md`
§*Out* rules it out with grounds: narrowing it is a third change with its own
failure direction, where an instruction split across a heading passes. It is
recorded as residue beside the case instead.

**No case pins the wrap module's documented numbers, and round 1's 🟡 5
corrected the reason.** The build's reason was that planting a reader is
mechanism aimed at the file `seal/follow-up.md` already holds open — and that
follow-up row is about a different act, whether `agents/smith.md` and
`agents/scribe.md` join `COVERED`, which widens what the test guards. Pinning
a number the module states about itself against the module's own helpers
widens nothing. **The reason that is true**: a mutation WAS available and was
run — changing a documented width reddens nothing in the repository — and the
work item is scoped by `spec.md` §*Out* to correcting the numbers, not to
adding a case. What stands in its place is that the numbers were re-derived
from `prose_lines` and `display_width` twice, and that the ledger row is now
anchored on the three lines that state them, so corrupting any one of them is
exit 2 rather than silence.

## Fed back into the spec

None. The two divergences above are corrections to measurements the frame
carried, not clauses this work added.
