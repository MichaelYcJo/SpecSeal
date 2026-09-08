# 1788844300-the-guards-cases-cannot-observe-what-they-guard — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here. -->

📋 implement applied
· spec:     `docs/review-chain-spec.md` (the reopening bound, why both findings
            left round 3 as issues), `seal/ledger.md` F1 (the self-reading
            parametrization standard) and R5 (the reader's arm count, corrected
            here), `CONTRIBUTING.md` (`bin/test` as the runner), the work item's
            own `routing.md`, issues #209 and #210 in full, and round 3 of
            `1788749195-the-record-drops-the-fix-and-a-pipe-truncates-the-row`
· evidence: `seal/ledger/1788844300-the-guards-cases-cannot-observe-what-they-guard.md`
            T1, T2, T3 — added; `seal/ledger.md` R5's arm count corrected from
            three reachable paths to four
· verified: EXECUTED — `bin/test tests/test_chain_hooks.py -q`, 30 passed at
            `57e9603`; seven mutations, one per arm, each read for which cases
            it killed; the `spec.loader is None` sweep over nine inputs; the
            #210 control reproducing the ticket's green run.
            READ — round 3's record and the warden's report on PR #208, to
            establish what the fenced fixes actually were.
            UNVERIFIED — the full suite, the repository-wide lint and the
            typecheck; the review orchestrator answers those.

## Scope confirmation

Second-rung work: two case-strength tickets and one arm found beside them.
Nothing observable changes — no gate verdict, no hook output, no instruction a
session reads. Three cases and one parameter pair are added, and two false
sentences in the evidence ledger are corrected. No `spec.md` and no `plan.md`.

## Why this work exists

Three arms of the pre-merge guard could have been deleted without a single case
going red, and one of them would have raised out of a `PostToolUse` hook into
somebody's Bash call; each now has a case that fails when its arm goes.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| Where the reviewer's fixes are | The spawn prompt and both tickets say *the reviewer's version is fenced in `rounds/round-3.md`* and to take the fenced block from there | Wrote both cases from the tickets' prose instead, after establishing what the round actually produced | Round 3's record reads `no paste-ready fix in the report` under `## Paste-ready fixes`, and it is right: the warden's round-3 report on PR #208 has no such section at all — round 2's report does, which is the likely source of the mix-up. Checked every committed version of the record (`c7fe663`, `341be0b`, `6de1bca`, `70c272c`); none carries a fence |
| How many arms `reader()` has | #209 tables **four** arms and names `SyntaxError` as the only unpinned reachable one | Pinned `SyntaxError` **and** `ImportError`, and recorded five arms of which four are reachable | Walking `reader`'s AST for `ExceptHandler` and `If` nodes gives five, because `except (OSError, ImportError, SyntaxError)` has three members. `ImportError` is reachable — a reader that parses and imports a missing module — and deleting it left all 29 cases green. Enumerating by construction is what the spawn prompt asked for, and this is what it returned |
| Whether `is_closed` was in scope | Both tickets are about `reader` and `readable`; the prompt's coordinates name `#is_closed` as well | Enumerated `is_closed`'s arms too, and added a case for the one that was unwatched | Contract §12 — the finding names an instance, the fix is owed to every instance the same cause produces. The cause here is *arms read off the page rather than enumerated*, and `is_closed` sits in the same file with the same shape |

## Not verified

| Item | Who must answer |
|---|---|
| the full suite, the repository-wide lint and the typecheck — contract §2 leaves the broad gate to one run after the rounds settle | the review orchestrator |
| `evidence-check` unscoped over `seal/ledger.md` — this run was narrowed to the work item's own fragment, and the correction to R5 was not re-hashed because it changes a Notes cell rather than an anchor | the review orchestrator, at the pull request |
| whether `blank_fences` and `strip_comments` have unwatched arms of their own — enumerated here (three and four respectively) but not mutated, because they belong to `unverified_check.py` and its own test module | the review orchestrator, or a follow-up work item |

## Not done

**`spec.loader is None` gets no case, deliberately.** Nine inputs were executed
against `spec_from_file_location` and none makes `spec` truthy while its loader
is falsy. A case would have to reach past that call and assemble a spec by
hand, which pins the test's own construction rather than the hook's behaviour.
The docstring says so and names the inputs that proved it — #205 is a ticket
about exactly this kind of stated limit, so it is stated with its evidence
rather than asserted.

**`blank_fences`' and `strip_comments`' own branches were enumerated and left.**
Three arms and four respectively, all inside `skills/verify/scripts/unverified_check.py`,
which has its own test module. Mutating them from this module would report on
coverage that is not this module's to hold, and widening the change to a second
test file is scope the tickets did not ask for. The enumeration is in the Not
verified table above so it does not go missing.

**The test ids for the hidden-word case changed** from `a fenced block` and
`an HTML comment` to `blank_fences` and `strip_comments`. That is the cost of
keying the constant by the pass's own name, which is what makes the tie
possible at all; the prose moved into the comment above the constant.

## Fed back into the spec

None. Three ledger rows were added and one existing row corrected, which is
evidence rather than spec.
