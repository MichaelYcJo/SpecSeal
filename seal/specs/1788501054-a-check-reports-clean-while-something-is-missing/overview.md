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

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and the typecheck | The orchestrator — `skills/agent-contract/SKILL.md` §2 gives the broad gate to one run after the rounds settle. What this session ran is every suite that reads the two checkers or the four documents it edited, named in the phase records |
| `seal/ledger.md`'s S8 row, whose claim is false | The repository owner. Work item `1788472135`'s memo deferred it there by name. This branch's unscoped `--reverify` re-stamped it from `45edf260` to `75242cc8`, and **it was restored by hand to `45edf260` in the same commit** — so `evidence-check .` still reports exactly one drifted row on this tree, as it did on the base |
| Whether the ordering refusal behaves on a CI checkout rather than a local one — a shallow clone, or a `--baseline` that resolves to a tag | The orchestrator, at the hygiene workflow's own run on this pull request. It is bounded rather than open by reading: `main` already refuses when `--baseline` does not resolve, and the ordering check adds one `git log` inside a range `changed()` was already spending. *Bounded* is a reading, and the workflow is the run |

## Not done

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
