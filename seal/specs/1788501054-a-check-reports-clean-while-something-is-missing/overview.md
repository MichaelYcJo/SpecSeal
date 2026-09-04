# 1788501054-a-check-reports-clean-while-something-is-missing — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens rather
than reconstructed at the end. -->

📋 implement applied
· spec:     `seal/specs/1788501054-…/{plan,spec,questions,routing}.md`;
            `docs/review-handoff-protocol.md` §*The handoff before round 1*;
            `docs/review-chain-spec.md`, the five cutoff subsections;
            `CLAUDE.md` §*a ledger coordinate names content* and §*a change
            writes fragments, never the shared file*; `CONTRIBUTING.md`
            §*What a change to a gate must carry*; issues #153 and #150 with
            its comment
· evidence: `seal/ledger/1788501054-a-check-reports-clean-while-something-is-missing.md`,
            five rows (R1–R5), stamped by `--reverify`
· verified: **executed** — the two new suites and every suite reading the two
            checkers or the four documents; nineteen mutations, none
            surviving; the refusal seen red against #150's two real records.
            **unverified** — the broad gate; see below

## Why this work exists

Two checks reported clean while something was missing, and in both the missing
thing left no trace: a ledger read narrowed to one work item's fragment cannot
see the rows a branch broke in the shared file, and a round record written
after the fixes it commissioned is indistinguishable from one written before
them.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| Where the rebase caveat is settled | `plan.md`: *"read the record's first commit on the branch rather than in the whole history, **or** accept that a rebase can turn a passing record failing and say so in the message"* | Both halves, not one | Reading `<baseline>..HEAD` closes the direction that fails an honest record, and it does not close the other one: a rebase rewrites the fix commit too, so the SHA in the verdict cell resolves to nothing and no claim is made. That hole is real and it is the safe direction, so it is stated in `docs/review-chain-spec.md` rather than left for someone to discover by being confused. The plan's `or` reads as a choice between two answers; the two turn out to answer different halves |
| Whether the handoff protocol's draft moves | Nothing in `plan.md` or `spec.md` says | Moved, 1.1 → 1.2, with a Status paragraph | The protocol's own `Status` section is what a conformance reader opens, and every previous change that added a requirement moved the draft. `tests/test_the_handoff_before_round_one.py` already refuses a title and a Status naming different drafts, so half-moving it is refused; not moving it at all would leave a fourth requirement under a draft that documents three |
| One work item, one test file | The repository's habit is prose cases and execution cases in sibling files | Two files for #153, one for #150 | #153's prose landed in phase 1 and its output in phase 2, and a phase-1 commit carrying phase 2's red cases does not stand on its own. #150's prose and execution landed in the same phase, so they share a file |
| Which add `added_on_branch` reads | Phase 3's docstring: *"the LAST line is the first add. A file added, removed and re-added is judged on the first of those, which is when its author committed it"* | The **latest** add, `found[0]`, and the docstring rewritten | Round 1's 🟡 8 mutated the index and all twenty cases stayed green, so the file documented a decision nothing held. The reasoning in it was also wrong: the version anybody reads was authored at the LAST add, so a stub committed on time, deleted, and rewritten after the fixes passed on the strength of a commit holding none of its content. The declared failure direction is *blocks more*, and the cost — a record accidentally deleted and restored is refused — is named in the docstring and visible in the failure |
| The direction a checker takes for a value it cannot read | `CONTRIBUTING.md` §*What a change to a gate must carry* and this branch's own `plan.md`: **failure direction: blocks more** | **Allow**, for the pending fix-surface arm alone | The alternative refuses an honest custom reason (`none — the fixes deleted a line`) for its wording, and a rule about which English sentences mean *not yet* is the enumeration over an unbounded domain `docs/review-chain-spec.md` declines twice already. What is caught is the measured failure — the template's own words left standing — and the phrase is a checker constant the template prints, tied by a case, so the two cannot drift. The cost is what escapes, which is written into the spec and the ledger row rather than left to be found — and round 3's 🟡 5 measured it wider than a rewording: three spellings carry the template's words unchanged (a dash outside the separator set, a doubled space inside the phrase, any clause in front of it), and only the first of the three is punctuation, so widening the separator set would close one and leave the sentence false about the other two. The arm's key is a second cost of the same shape: it reads `Fixes checked by`, so it reaches the session that filled that cell and stopped, and neither `nobody` nor `no fixes to check` beside a pending row is refused |
| Round 1's count of the bare fix cells | `round-1.md`'s 🟡 7 and its probe table: *"231 fix-word verdict cells, 212 carrying a SHA, 19 carrying none"* | **235 · 215 · 20**, re-measured | An aggregate is not a coordinate (`docs/review-handoff-protocol.md`), so the number was re-taken through the checker's own `verdict_table`, `verdict_of`, `FIX_WORDS` and `SHA_RE` over every record git carries — identical at the round's target `15278db` and at HEAD. The finding's direction is untouched and only its number moved, so the fix stands and the measured figure is what went into the template and the spec |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and the typecheck | The orchestrator — `skills/agent-contract/SKILL.md` §2 gives the broad gate to one run after the rounds settle. What this session ran is every suite that reads the two checkers or the four documents it edited, named in the phase records |
| `seal/ledger.md`'s S8 row, whose claim is false | The repository owner. Work item `1788472135`'s memo deferred it there by name. This branch's unscoped `--reverify` re-stamped it from `45edf260` to `75242cc8`, and **it was restored by hand to `45edf260` in the same commit** — so `evidence-check .` still reports exactly one drifted row on this tree, as it did on the base |
| Whether the ordering refusal behaves on a CI checkout rather than a local one — a shallow clone, or a `--baseline` that resolves to a tag | The orchestrator, at the hygiene workflow's own run on this pull request. It is bounded rather than open by reading: `main` already refuses when `--baseline` does not resolve, and the ordering check adds one `git log` inside a range `changed()` was already spending. *Bounded* is a reading, and the workflow is the run |
| Whether `st_ino == 0` actually occurs on `windows-latest`. What was executed is what the checker does with a zero — it went silent, and now names the file by path instead — not that a zero arrives there | The windows CI leg, at this pull request. Round 2 deferred it there by name, and the fix is correct either way: a platform that never produces a zero never reaches the branch |
| **What `normcase` in the skipped-set fallback does on Windows.** Round 4's fix pass corrected the reason this guard was recorded unreachable: it is unkillable off Windows because `normcase` is the identity there, and on Windows it is both reachable and load-bearing. The corrected reason is measured off Windows only — one inode, two identities on a case-insensitive macOS volume — so what stays unverified is the pairing the guard exists for, on the one platform that has it | The windows CI leg, at this pull request. It is `agent-contract` §13 stated rather than closed: no run here removes the platform guarantee, so the guard is recorded rather than deleted. The direction is safe either way — the fallback over-reports, and a named ledger is the state this notice exists to produce |

## Not done

**Round 4's 🟡 7 ships as issue #159, not as a rule.** Round 4's fix pass
answered that finding by inventing a rule — a field cell corrected after its
record is committed leaves a trace in the trailing HTML comment — and a
checker that walked each record's git history to enforce it. No spec asked for
either. It was the only thing on this branch keying on git history, a feature
branch squashes into its release branch, and round 5 executed the squash: all
four records collapse to one commit each, the walk compares nothing, and its
own guard fires. This repository has already paid a patch release for that
class, in `tests/test_a_rider_reaches_its_file.py`. The repository owner chose
to revert rather than build a second reader — the third on one finding — so
the rule, its two cases and its four helpers are gone, and issue #159 carries
the finding with the measurement a design has to answer. The traces already in
`round-1.md` … `round-4.md` stay: they are true, they cost nothing, and the
two that cited the template as the rule's home now say it was reverted.

**The pending arm was not widened to key on the sibling records**, which is
what would answer both of round 3's heaviest findings at once. A non-terminal
record carrying `nobody` is false by construction — a later record exists, and
round N+1 reviews round N's fixes — so the sibling map `Fixes checked by`
already receives would reach the session that filled nothing, and the same
signal answers the terminal `no fixes to check` pair. It was declined for two
reasons and both are written where a reader meets the refusal: it is a change
to a gate, with its own cutoff, cases and spec subsection, which a fix pass is
not the place for; and it gives the arm a second source of truth, which ledger
row R7 records as the property that makes the narrow key defensible at all.
It is `questions.md` Q4, with three options and the repository owner as the
answerer, and Q3 is its sibling for the terminal value.

**Four mutation survivors were recorded as unreachable, and re-deriving all
four found three of the four reasons false.** Round 3's fix pass wrote a
paragraph for each; round 4 reopened two of them and the fix pass re-measured
every one, because a recorded limit that is wrong is worse than one that is
missing — it tells the next battery that a live line is dead. What the four
say now:

| The guard | What was recorded | What re-deriving it found |
|---|---|---|
| `says_not_yet`'s `none` prefix | duplicates `says_none`'s and cannot change the answer | **Stands.** Both of `says_none`'s True routes imply the prefix, and deleting the guard leaves the suites green |
| `says_not_yet`'s separator boundary | the same sentence covered both | **False.** `says_none` answers True for a bare `none` by `s == NONE_WORD`, so a value reaches here with nothing after the word — the spelling `templates/sdd-round.md` itself produces. Dropping the `not rest` conjunct alone turns **20** cases red; only deleting the guard WHOLE is answer-neutral |
| `normcase` in the skipped set's path fallback | reachable only where CPython zeroes an inode, which is the one platform where `normcase` is not the identity | **The conclusion stands and the reason is false.** The fallback is reached by `OSError` on EVERY platform; only the zero-inode route is Windows-only. What is Windows-only is `normcase` differing from the identity, so it is unkillable off Windows and load-bearing on it. The fallback sentence one paragraph up was false the same way, and that one is round 1's 🟡 9 restated — measured on a case-insensitive volume, one inode and two identities |
| `seal_home`'s `SKILL.md` conjunct | needs a vendored copy inside a tree that has a plugin above it, which no fixture builds | **False, and now closed.** The state is constructible, the two answers differ against a local-mode repository, and `test_a_copy_under_a_plugin_tree_without_a_skill_beside_it_is_still_vendored` builds it. The mutation that survived every evidence suite now dies |

So one limit of the four survives as written, one keeps its conclusion with a
new reason, one was a real hole that is now held by a case, and one is a guard
whose halves behave differently. Both `# RIDER:` comments are gone: each stood
in for a case, and both cases exist. What each surviving limit says is in the
docstring that carries it, because a mutation battery cannot tell an
unreachable guard from an unheld decision and the next one will find them
again.

**No issue was opened for the row selector `--reverify` does not have.** Phase
1 tells every round to run the unscoped read, so from now on every branch will
SEE the rows it drifted in `seal/ledger.md` — and the only way to re-stamp
them is to re-stamp the whole file, which takes S8's false claim along and has
to be undone by hand. This branch did exactly that, above. It is written as Q2
in `questions.md` with three options and the repository owner as the answerer,
because opening an issue is an outward-facing act and `agents/smith.md` gives
this session the pull request and nothing beyond it.

**The rebase hole is left open knowingly**, with the reasoning in
`docs/review-chain-spec.md`: closing it would mean matching rewritten commits
by patch id, a second mechanism for a case nobody has met, where the cost of
the other direction is an honest record refused for a rebase its author never
connected to the failure.

**`docs/flow.md` gained no new numbered row**, because the only ticket this
work opens is the one above and it has no number.

**Round 1's ⬜ 10 is left as it stands, with grounds.** A verdict cell naming
two late commits prints the failure once per commit, because the grouping key
is the resolved commit — seven cells naming one commit is solved and one cell
naming two is not. It over-reports on a shape nobody has produced, and both
paragraphs would be true. Collapsing further means putting two commits and two
row lists into one 90-word failure, which is harder to read than two of them,
for a message rewrite and a case. The direction is stricter, which is the
declared one.

**One mutation survives the battery and no case kills it.** Making
`commissioned_fixes` substitute `HEAD` for a cell that names no commit leaves
all 23 cases green, because `HEAD` is the last record's own commit and not an
ancestor of the earlier record's. It is a mutation with no plausible author —
nothing in the file reads a missing SHA as a commit — and the property that
matters is pinned instead by running the SAME late record twice, once with the
commit in the cell and once without: refused, then passed. That is the reach's
limit measured rather than an exit code that could have come from anywhere.

## Fed back into the spec

- `docs/review-handoff-protocol.md`'s fourth handoff requirement — *a command
  with more than one form names the form, and says what the other one is for*
  — is inferred during implementation. `spec.md` asked for the two forms to be
  named; that they generalise to any command whose flag changes what it reads
  is this work's own reading, and a planner may overturn it.
- `docs/review-chain-spec.md` §*What the record carries* records that three
  candidate checks were tried and rejected. The rejections are reasoning, not
  measurement, and the third of them (*the content cannot be in a diff at the
  moment the record is written*) is the one a later design could route around
  by asking for the block to be added at the update pass.
