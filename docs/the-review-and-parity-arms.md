# the review and parity arms — behavior spec

Authority for the two opt-in arms of the commit gate, the review arm and the
parity arm: what each wants before a commit, its mark, its waiver and where it
stays silent, and the routing declaration that moves the review arm's check
to the pull request. Where the arms are asked from is in two sibling
documents. `docs/the-commit-gate-inside-git.md` is what git decides inside
the commit, in a clone carrying this plugin's git hooks.
`docs/commit-review-gate-spec.md` is the PreToolUse reading that judges where
git cannot, and also holds the registration of the hooks, the review-history
guard and the implementer mark. The review run those hooks serve is
`docs/review-chain-spec.md`'s, and what the pull-request check reads of a
round record is `docs/round-record-spec.md`'s. Update spec and code together.

## The two arms of the commit gate

### Review arm — opt-in: `seal/` at the repo root

| Condition | Decision |
|---|---|
| `[no-review]` in the command | silent (explicit skip, visible in history). Typed in front of it: `: '[no-review]'; git commit …` — see below |
| a `routing.md` declaration names this branch, for either answer | silent — the routing question was answered before the first edit, and CI checks the answer at the pull request. See *The declaration* below |
| `specseal-reviewed` equals current HEAD | satisfied |
| the change confined to `docs/`, `seal/` | no different from any other change — this arm reads no paths. The parity arm's silence on the same roots is that arm's alone, and the paragraph below says why |
| otherwise | contributes an ask |

<!-- specs/1790154759-the-review-arm-asks-where-no-reviewer-compares -->
**The review arm reads no paths: a change confined to `docs/` and `seal/`
meets it as any other change does, and a lighter tier is declared, never
inferred.**

**Why this arm has no document-root line.** The two arms ask different
questions. The parity arm asks whether the original was consulted, and a
`docs/` file has no original, so its silence there is right. This arm asks
whether anybody reads the change before it lands, and here `docs/` is the
policy the code conforms to and `seal/ledger.md` is the verified evidence.
#518 measured whether review finds defects there before drawing any line,
and it does. Across every round record, at least 25 fixed findings sit in
`docs/` alone and 26 in the ledger alone. #514's fold, which changed `docs/`,
`seal/` and four test files, opened seven findings a later round verified as
fixed, all in `docs/`, one of them 🔴. No reviewed work item was ever confined
to the two roots, and the seventeen docs/seal-only commits on the release
branch never reached a reviewer, so nothing measured them either way. The
parity arm's line would stop asking exactly where the reviewed findings sit,
on the strength of a population nobody measured. A documentation pass that
should reach nobody is routed that way before the first edit, by declaring
`straight to the PR`; it is never inferred from the paths it touches.

The marker is decided when the work starts, not discovered at the commit
(`implement` §1) — and until the release that added `routing.md`, nothing
recorded it, so the gate had to
re-derive the answer at every commit and could only ask. The branch that
submitted to review was interrupted at every step; the branch that skipped
review was silent. The incentive ran backwards, and it ran backwards for
exactly the work the chain exists to serve.

Approving is still per commit and the marker still per command. What changed
is that the routing answer now has somewhere to live, and the check it
silences now happens at the pull request instead. See below.
Enforced by: tests/test_chain_hooks_hardening.py::test_the_review_arm_asks_on_a_document_only_commit

#### Where the marker goes, which is not where it is read

`has_marker` finds a bare word anywhere in the command. Where it can be *typed*
is a separate question, and the prompts answered it wrongly for three releases
After `git commit`, a bare word is a **pathspec**, so
`git commit -m x [no-review]` is rejected by git before the gate's advice can
help. The gate stopped the commit, the escape it named failed, and approving
the prompt was left as the only thing that worked — the outcome the wording
exists to offer an alternative to.

Measured in three shells:

| Form | bash | `zsh -c` | interactive zsh |
|---|---|---|---|
| `git commit -m x [no-review]` | rejected (pathspec) | rejected | rejected (unmatched glob) |
| `git commit -m x  # [no-review]` | commits | commits | **rejected** — `#` is not a comment there, so the marker globs |
| `: '[no-review]'; git commit -m x` | commits | commits | commits |

So the advised form puts the marker in front, inside a no-op `:` command. The
shell discards it, git never sees it, and the word stays in the command where
shell history keeps it — which is the whole point of a waiver that is supposed
to be visible.

`tests/test_the_waiver_can_be_typed.py` runs the advised form against real git
in every non-interactive shell present, and pins the rejected form too. The
interactive-zsh row is recorded rather than run: an interactive shell in CI
needs a tty and sources a user's rc.

#### The declaration, and where the check went instead

<!-- specs/1789518345-who-asks-the-routing-question-and-what-checks-the-answer -->
**The gate reads `seal/specs/<work-item-id>/routing.md` before it reads anything
else.** Where a declaration is in force the review arm stays silent — for
**either** answer, because the routing question was answered before the first
edit and asking for `[no-review]` as well is asking for the same answer twice.

| The declaration says | At the commit | At the pull request |
|---|---|---|
| through the review chain | silent | a committed `rounds/round-N.md` is required, every commit its `Target SHA` names being REACHABLE — an ancestor of HEAD, or of the branch `routing.md` declares — its last round's `Pass` **checked**, that claim consistent with its own verdict table, and its `Fixes checked by` naming a checker the repository can confirm. A record this pull request does not touch keeps every requirement except reachability: its commits are expected to be gone, and the review it records was enforced at the pull request that added it. A record it RESTORES byte-for-byte from the merge base's own history — the same bytes at the same path in any commit the merge base reaches — is judged the same way, because an earlier pull request added those bytes. One byte changed and the record is this pull request's claim again |
| straight to the PR | silent | the sealer's `broad-gate.md` in the work item's directory, for a work item begun at or after `chain_check.py`'s `DIRECT_GATE_FROM` — the one broad run, at a SHA the tree can see, against the base — and nothing else: the answer turns off the reviewer alone. A draft pull request is excused the file, an earlier work item is excused and prints, and the declaration is printed either way, because a decision nobody sees is not a record |
| nothing readable, or no file | today's behavior — deny once, then ask | pass, with a notice saying nothing was checked |

What the check reads of each round record under the first answer, and what
each refusal costs, is `docs/round-record-spec.md` for the record's rows, and
`docs/review-chain-spec.md` for the floor, `Needs a fix`, the reopening and
when the record was written.
Enforced by: tests/test_routing_is_recorded.py::test_a_declared_chain_item_commits_without_a_prompt, tests/test_routing_is_recorded.py::test_a_declared_direct_item_commits_without_a_prompt, tests/test_chain_check_at_the_pull_request.py::test_a_record_restored_from_the_bases_history_makes_no_reachability_claim

<!-- specs/1790173106-a-bare-yes-sets-the-run-length-and-a-session-review-has-no-row -->
**`straight to the PR` owes the sealer's `broad-gate.md` and turns off the
reviewer alone, and `Review` has two answers, not three.**

**Two answers, and not three.** A session that wrote a change and then checked
it itself has asked for a third — *reviewed by the session* — with a record of
its own (#241). There is none, and the reason is what the chain's record is
worth: something, only because somebody other than the author wrote it.
`Fixes checked by` refuses *the session that wrote them*
(`docs/review-chain-spec.md` §*Two records, and what each of them says*),
`Ran by` is the spawning
session's row and never the agent's own, and the contract names a review that
certifies itself as what the commit gate exists to catch. What the author's own
check leaves that CI can read is what it RAN — the broad gate at a SHA against
a base — and that is the sealer's stamp, which `straight to the PR` already
owes in the row above. The reading half, *here is what I checked*, is prose,
and prose is not evidence. So a change its author checked declares `straight
to the PR` and takes the broad run; what that answer turns off is the reviewer,
and nothing else. A change belonging to no work item at all is the routing
question's third answer, `no work item`, whose recorded form is `[no-review]`
in front of each commit — there is no value meaning no enforcement anywhere.
Enforced by: skills/code-review/scripts/chain_check.py::direct_seal

<!-- specs/1789518345-who-asks-the-routing-question-and-what-checks-the-answer -->
**A declaration the pull request RETIRED is not one it made**, and neither is
one it only renamed. Both are ways a `routing.md` leaves a diff without
anybody declaring anything, and both are excluded: the rename because the
root move renames every declaration in the repository at once, the
retirement because `settle --retire` removes a released work item's directory
after a `docs/` policy has absorbed its spec, and that work item was reviewed
at its own pull request. The first fold put 88 retired declarations in one
diff, and this check failed all 88.

**The marker is what tells a retirement from a deletion**, because both leave
the file absent at `HEAD` and nothing else can. Where `docs/` carries the
work item's `<!-- specs/<work-item-id> -->` comment on a live line, the check
prints `retired: …` and reads no further; where it does not, the refusal stands —
that is a directory removed with nothing absorbing it, which is what the
refusal was written for. It is the same distinction
`unverified_check.folded_items` draws for a removed `overview.md`, and this
reader had not grown it.

**The rule is the other way a declaration is retired, and it carries no
marker.** `settle --retire` also removes a released directory that held no
`spec.md` and nothing open in its record, because a record of a moment states
no rule to fold (#517). So a declaration absent at `HEAD` whose directory is
gone is asked one more question of the merge base: did the directory hold no
`spec.md` there, and nothing open in its `overview.md` or `evidence-todo.md`?
Where it did not, the check prints `retired: by the rule — …`; where the merge
base held a spec or an open row, the refusal stands. The question is
`unverified_check.retired_by_rule`, the one predicate `settle`,
`unverified_check.py --baseline` and the survivor sweep ask too, so the four
cannot disagree about the same tree the way the marker arm once did. Asked of
the merge base rather than of the tree the branch left, and asked whether the
directory's history ever held a `spec.md`, a spec deleted in one commit — or
in an earlier pull request — and the directory in the next is still a
deletion.

Every record is read as git carries it at `HEAD`, never as the working tree
holds it: a tree that differs from `HEAD` is what CI never sees, and a local
run reading it would be the more permissive of the two. `--worktree` reads the
working tree instead, for the check `round_record.py` runs on a record before
its commit. The flag is local only, and CI keeps the default.

Which declaration applies is settled by the branch it names, looked up from
the checked-out branch. Every way that lookup can fail — a renamed branch, a
detached HEAD, two declarations naming one branch, a file that will not parse
— resolves to *no declaration*, and therefore to **asking**. There is no path
from a missing or ambiguous declaration to silence: a fail-open here would be
a gate that a corrupt file switches off, and a failed read is not a decision
anyone made.

**This is a reversal, and of this document.** The paragraph below the review
arm's table used to say there is deliberately no standing waiver, because
"a gate that can be turned off for a session has nothing left to do but stay
quiet". That was correct while the commit was the only place a check could
live: with one enforcement site, recording the answer necessarily removes the
check.

A waiver removes a check; a routing record moves it. Both answers stay
enforced — the chain at the pull request against the round record, the direct
route by `[no-review]` in every commit command, unchanged. There is no third
value meaning "no enforcement anywhere". What makes the reversal possible is
the second site, which did not exist when that paragraph was written:
`gh pr create` passed no gate at all, so enforcement sat entirely on every
commit and was absent at the moment the work actually left.

What it costs, stated rather than buried:

- A commit on an unreviewed branch is no longer stopped as it is typed.
  Between the declaration and the pull request, nothing local blocks.
- A branch that declares the chain and never opens a pull request is checked
  by nothing. Today the gate would have stopped every commit. The
  destination axis is what turns that from an accident into a state someone
  declared and can be shown.
- A repository that adopts the declaration and not the workflow has traded a
  prompt for a convention, and the plugin cannot detect that state.
- Deleting the routing file restores today's behavior exactly, because the
  fallback for a missing declaration is today's decision table.

Enforced by: tests/test_chain_check_at_the_pull_request.py::test_a_declaration_this_branch_retired_is_not_one_it_made, tests/test_chain_check_at_the_pull_request.py::test_a_declaration_the_rule_arm_retired_is_not_one_it_made

### Parity arm — opt-in: `seal/parity.md` at the repo root

Ported behavior follows the original where policy is silent, so a commit that
changes code should carry a record that the original was consulted. Mark:
`<git-dir>/specseal-parity`, written by the `legacy-parity` skill after an
actual comparison.

| Condition | Decision |
|---|---|
| `[no-parity]` in the command | silent (explicit skip, visible in history). Same placement as `[no-review]` |
| the change confined to `docs/`, `seal/` | silent — nothing there can be compared against an original, and a gate that fires where no comparison was possible teaches people to click through it |
| `specseal-parity` equals current HEAD | satisfied |
| otherwise | contributes an ask |

"The change" there is every path the commit would carry, not the index alone:
`changed_paths()` reads the staged diff, and also what `-a` and a trailing
pathspec pick up, because two of the three forms never touch the index. A
document-root row that said *staged* would describe a narrower silence than
the gate actually keeps, and a reader would expect a prompt where none comes.

The mark says a comparison was recorded, not that it was a good one. Writing
it for work nobody compared converts "nobody checked" into "someone checked
and it was fine" — the one claim the parity methodology exists to keep honest.

`ask` was chosen over `deny` here originally, on these grounds: the gate
cannot know whether the user already accepted the risk, and *a deny with no
override path forces workflow contortions* (measured on the worktree guard's
earlier design). That reasoning stands — it is the override path that changed,
so the premise no longer holds:

| The old worry | What answers it now |
|---|---|
| a deny repeats, and the user cannot get past it | the question fires once per session per repository; every attempt after it is the same `ask` as before |
| the gate cannot know the user already accepted the risk | it no longer has to guess — the deny's reason puts the choice to the user, and their answer comes back as `[no-parity]` (or the comparison itself) |
| nowhere to record the risk being accepted | the marker, and the token in the command, which stays visible in shell history |

What the deny buys is the half the `ask` could never deliver: the reason
string could *name* both ways on, but only the model can put them up as
options, and an `ask` never gives the model the turn.
