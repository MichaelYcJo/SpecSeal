# 1791163981-the-worktree-guard-asks-about-a-message-search-and-reads-no-body-token — questions for the planner

<!-- seal/specs/<unix-epoch-seconds>-<slug>/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

**Decided from the tree, so nobody reopens them.** Each has its grounds in
`spec.md` or in `plan.md` *Alternatives considered*.

- **Whether `hooks/cmdline_base.py` is reopened.** No. Neither defect lives
  there: `is_ref`, `classify` and `has_token` are in `hooks/worktree-guard.py`,
  and the byte pin and P4 stay as they are (`spec.md` §*The frozen reading*).
- **Whether the name lookup may be read past the base.** Yes, for C1 and C2:
  the owner reopened `classify`'s `checkout` arm on 2026-10-04 (1791119071,
  P1), #790's own fix text asks for the lookup "resolved the way git resolves
  it", and the owner placed #790 in this milestone. §*Which tree*'s first
  paragraph is amended to name it.
- **`:/` read outright, or resolved.** Resolved, with a tree (`plan.md` A, J).
- **One rule per broken syntax, or resolve-then-peel.** Resolve-then-peel for
  C1, a merge-base rule for C2 (`plan.md` B).
- **Replace the lookup, or OR onto it.** OR, so a base question never goes
  quiet by construction (`plan.md` C).
- **Which body reader `has_token` uses, and what happens when it cannot
  load.** `tokens.without_bodies`, AND-ed with the base read; the frozen
  `cmdline_base.drop_heredoc_bodies` when it cannot load (`plan.md` F–I).
- **Whether a note is added when a token sits only in a body.** No
  (`spec.md` §*Out*).
- **Whether the READMEs change.** Yes for #780 (both token rows, both
  editions); no for #790, which no README sentence describes.
- **Whether `checkout <tree-ish> <path>`, a bare `--detach`, git config and a
  lookup timeout are in.** No, each with its reason (`spec.md` §*Out*).

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| P1 | Does the owner's placement of #790 cover the remote-tracking guess from a remote not named `origin` (C3)? #790's text names the `:/` search and "the other revision syntaxes"; a guess is how `git checkout` resolves a name, not a revision syntax. The tree records the owner's act for #790 as written, and §12 is the frame's reason to widen it — so whether the reopening of the frozen reading reaches this far is the owner's, as 1791119071's P1 was | **a person**: the owner. It is how far the frozen reading is opened, which P4 made the owner's to decide | **(a) Yes** — `classify` guesses over every remote; a guessed branch from `upstream` or a fork is asked over a dirty or shared tree (`plan.md` J). **(b) No** — the guess stays at `origin`, and §*Known limits* names the other remotes with M3's count; such a checkout keeps switching unasked (`plan.md` E) | (a). Answering (b) after the build removes the every-remote lookup, its cases and its policy clause, and adds the limit; C1 and C2 are untouched | ⬜ default (a) taken 2026-10-05 by the orchestrator under the owner's `automation` routing, relayed at the build's spawn; the build guesses over every remote. Open for the owner, who can still answer (b) at the pull request |
| M1 | For each C1–C3 form × carrier (`spec.md` §*The class*), does git 2.54.0 switch, detach or refuse, and what does `a3aa139a`'s `classify` answer? Which C1 forms, besides `:/<text>`, does the `^{commit}` suffix break? | **a measurement**: phase 1, one scratch repository with two commits, a branch, an annotated tag, a reflog, a second remote holding a branch no other remote holds, and two branches with one merge base | A form git refuses leaves the class and keeps the base's verdict. Every other form is a case in A2 | `:/<text>` (all three spellings) and `<a>...<b>` (all three, a side omitted or not) are the only silent forms; the guess is silent for any remote but `origin`; every range form is refused | ✅ measured 2026-10-05 by phase 1 (executed, git 2.54.0, a scratch repository): the base is silent on `:/<text>` and `:/!!<text>` under every `checkout` carrier, on every `<a>...<b>` form with one merge base, and on a branch guessed from a remote not named `origin`; `:/!-<text>` answers yes at the base by accident, and every range form and every non-commit form is refused (`phases/phase-1.md`) |
| M2 | Does resolve-then-peel (`rev-parse --verify --quiet <name>`, then the object name with `^{commit}`) answer "yes" for every C1 form git moves on, and does `merge-base --all` with exactly one line answer every C2 form git moves on? | **a measurement**: phase 1, the same repository | Yes: build `plan.md` J as written. A form it misses is recorded in `phases/phase-1.md` and gets the next narrowest rule, or a §*Known limits* line with its reason where none exists | yes | ✅ measured 2026-10-05 by phase 1 (executed): yes for both rules, and each answers no on every form git refuses (`phases/phase-1.md`) |
| M3 | Over the recorded runs, how many pairs does each change move, and is every moved pair a shape of the class and none quieter? Two cuts: the one 0.18.2 counted (Bash uses before 2026-10-03T11:06:22+09:00, 25,741 pairs on 2026-10-04, fewer if transcripts have left the disk since), and every pair up to the build day | **a measurement**: phase 1 (before) and phase 4 (after), a deleted probe over the transcripts. #780's read is tree-independent; #790's lookup is replayed tree-blind for the syntax forms and against each pair's directory as it stands on the build day for the guess, labelled so | A count per reader and per cut, carried by `phases/phase-4.md` and the pull request's prompt budget. A moved pair outside the class, or any pair that goes quieter, is a finding reported with its shape | the build proceeds; the counts are reported as found | ✅ measured 2026-10-05 by phases 1 and 4 (executed) over 25,741 pairs (cut 1) and 36,199 (cut 2): #790 moved no `checkout` segment in either cut; #780 moved two pairs' `[worktree-ok]` read, both a token in a body, neither reaching a row that reads it; no pair moved outside the class and none went quieter (`phases/phase-4.md`) |
| W1 | Which released ledger rows the change drifts, beyond D1, D4 and W1 (`seal/releases/0.18.2.md`), K6 and K7 (`0.18.0.md`) and M2 (`0.16.0.md`) | **the work**: phase 4, `bin/evidence-check --strict .` | Each drifted row is read against the change and gets a `Re-read ·` row in this work item's fragment; one that no longer holds gets a `Corrected ·` row | — | ✅ answered by phase 4's work (executed): D4 (0.18.2) and K7 (0.18.0) no longer held and are `Corrected · D4` and `Corrected · K7`; W8 (0.15.6), M2 (0.16.0), K6 and Corrected G17 (0.18.0), Corrected G1 and D1 (0.18.2) drifted and still hold, each re-read (`phases/phase-4.md`) |
| W2 | The exact words of §*Which tree*'s amended first paragraph, §*Choice sites*' body sentence and the two README rows in each edition | **the work**: phases 2 and 3 | Any wording that carries `spec.md` §*Scope* In 3 and In 5, agrees with the code clause by clause, and is pinned | the builder's | ✅ written by phase 2 at `7c0ae048` (§*Which tree*, §*Known limits*) and phase 3 at `f18bd16a` (§*Choice sites*, both READMEs), pinned by `test_the_guard_policy_says_what_it_reads_past_the_base` and `test_the_guard_policy_and_readmes_say_a_body_token_is_not_read`; read clause by clause against `_commit_named`, `_one_merge_base`, `tracked_in_any_remote` and `has_token` |

P1 blocks nothing. The build uses its default, and a different answer
removes one lookup and adds one limit; nothing else in the plan moves.

**`Who can answer` takes one of three values and nothing else.** They were one
shape on the page before this, and #84's second comment measured all three
inside a single run's four rows.

- **a person** — what the product should be, or a value somebody has to be
  accountable for. This is the file's stated purpose, and the only kind of row
  that blocks the build.
- **a measurement** — a probe, a command or a count settles it, so asking a
  person is the wrong instrument and queueing it behind one wastes a round
  trip. Measured: six probes at about three seconds each answered a row that
  had been written into the human batch, and they showed the ticket's own
  instruction was wrong.
- **the work** — unknowable at framing time. The phase that meets it decides
  it there and records a divergence row; it does not travel back to the
  framer, which would spend the interruption the framing phase exists to spend
  once.

**The framer opens rows and does not own their answers.** A row is a question
put to somebody else, so opening one costs little and closes nothing — and the
`Status` column is ticked by whoever answered, never by whoever asked. Sorting
the rows this way is also what keeps the batch short enough to answer in one
sitting: two of the three kinds never needed a person at all.

Answered rows feed back into docs/ (policy clause or open-questions section)
before this directory's work merges.
