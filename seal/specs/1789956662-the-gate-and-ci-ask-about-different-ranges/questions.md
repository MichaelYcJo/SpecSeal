# the gate and CI ask about different ranges (#423) — questions for the planner

<!-- seal/specs/1789956662-the-gate-and-ci-ask-about-different-ranges/questions.md
— decisions only a human can make, extracted so nothing ships on a silent
assumption. Before adding a row, check the inheritance rule: if policy is
silent but existing behavior answers it, inherit and record — only genuinely
NEW rules belong here. -->

**This run is declared `Automation | yes`, so no row here stops it.** Every
row carries the assumption the build proceeds under, and a row answered later
is answered against a branch that already exists.

## What the tree answered, so nobody reopens it

These were open in the ticket and are closed from the repository rather than
by anybody. They are listed because a reader cannot tell a judgment that was
made from a question that was never met.

- **Which of the ticket's three directions.** Resolving, not refusing.
  `CLAUDE.md` §*The goal a design is chosen against* decides between two
  designs that catch the same defect by what an interruption costs, and
  #423's own non-goals already refuse the fetch that a refusal sends a person
  to perform. The argument is `plan.md` §*Alternatives considered*; P1 below
  is the owner's chance to overturn it.
- **Whether resolving reproduces CI's answer for the measured case.** Yes,
  recorded in the tree: work item `1789518345`'s `survivors.md` §*The merge
  with `release/v0.12.0`* holds a local run of
  `bin/survivor-check --range origin/release/v0.12.0...HEAD` reporting the
  seven places CI reported.
- **Whether the ticket's *a stale base can only narrow the range* holds.** It
  does not, and `spec.md` §*What is wrong* carries the correction:
  `survivor_check.py#parse_range` resolves through `git merge-base`, so the
  two spellings agree entirely unless HEAD already carries the base's newer
  commits. The ticket's diagnosis of the instance is right; its general claim
  about direction is not, and the frame does not build on it.
- **Whether the `Broad gate` cell should carry the ref.** No — two parsers
  read that cell and one refuses on what it finds. `spec.md` §*Out* has the
  grounds.
- **Whether `.github/workflows/hygiene.yml` should change.** No. A runner's
  checkout has no local branch, so `origin/<base>` is the only spelling that
  resolves there.
- **Which remote-tracking spelling to prefer.** `<base>@{upstream}` first,
  `refs/remotes/origin/<base>` second. A clone whose base tracks a second
  remote is the defect class being repaired, so the checkout's own answer
  wins where it has one.

## The rows

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| P1 | The ticket names a refusal — *refuse a base whose remote-tracking ref is ahead, naming both SHAs and the distance*. This frame drops it entirely and prints the same facts instead. Should a refusal survive anywhere in the gate? | a person | **(a) no refusal** — the gate resolves, prints where it moved, and runs; nothing stops. **(b) refuse when the remote-tracking ref is ahead** — the sealer's run ends at exit 2 with a report, and somebody fetches and pays the gate again; the ordinary release case (a sibling merges while this branch is open) fires it. **(c) refuse only where resolution found nothing and HEAD is ahead of the base** — a narrow refusal for a checkout with no remote at all, which is also every fixture in the suite and every local-only user | **(a)**, built under `plan.md` §*Alternatives*. Moving to (b) later is additive — the resolution stays and a refusal is a branch above it — so nothing built now is wasted | ⬜ |
| M1 | CI checks out the merge of the head into the base; the gate runs over the working tree. After this change, can a green gate still meet a red CI because the base moved after the branch last took it in? | a measurement | A fixture that moves the remote base after the branch's last merge, run through the gate and through the survivor arm at the merge of the two. Either it reproduces — and `spec.md` §*What this repair cannot see* is right to name it a standing limit — or it does not, and the limit comes out of the document | The limit is real and stays named. The build does not try to close it | ⬜ |
| M2 | Does any fixture or shipped test in this tree read differently once the gate resolves the base? Every gate fixture today is built by `build_repo`, which adds no remote, so the fallback should make the whole module byte-identical — but that is a measurement over a population, not a property | a measurement | Run the module before and after phase 2 and compare. A fixture whose reading moves is a divergence row in `overview.md` with the fixture named | Nothing moves; A3 is the case that says so | ⬜ |
| W1 | `origin/release/v0.12.0` is 22 characters and a panel value is cut at 23. What does the panel do with a ref that does not fit — a second row, an abbreviation, or the frame's cut with the full spelling on the printed line? | the work | Phase 3 decides it against the rendered output, which is the only place the cut is visible | The panel carries the short form and the printed line is authoritative, so a cut ref costs a reader nothing they cannot get | ⬜ |
| W2 | The child checks quote their baseline back in their own messages — `unverified_check.py#base_label` names the ref, and a bare commit makes that read *the merge-base of 58014fe4 and HEAD*. Is the commit handed to all six, or the ref spelling where the interface prints it? | the work | Phase 2 reads each message as it comes out and decides per call site, recording what it chose | All six take the commit, because `#423`'s comment asks that evidence name a commit rather than a ref. A message that reads worse for it is a note in `overview.md`, not a reason to pass a ref | ⬜ |

Answered rows feed back into docs/ (policy clause or open-questions section)
before this directory's work merges.
