# 1791119071-the-worktree-guard-reads-a-glued-value-and-a-redirection — questions for the planner

<!-- seal/specs/<unix-epoch-seconds>-<slug>/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

**Decided from the tree, so nobody reopens them.** Each has its grounds in
`spec.md` or in `plan.md` *Alternatives considered*.

- **Where `classify` is frozen, and what the owner reopened.** The byte pin
  covers `hooks/cmdline_base.py` alone; `classify` is frozen by P4's *no rule
  added* and §*Which tree*'s first paragraph. The owner's 2026-10-04 act
  reopens the per-subcommand rule, not the pinned file (`spec.md` §*The
  frozen reading*).
- **Whether git switches on a stuck, aggregated or abbreviated creating
  option.** `git help cli` §*Enhanced option parser* (git 2.54.0) documents
  all of them, so the frame treats them as switches; M1 confirms each one.
- **Fence in C or a fix with a tree.** With a tree, in `classify`: the fence
  cannot reach #764 and asks on a stuck restore (Alternatives A, H).
- **Whether `hooks/cmdline_base.py` changes.** No (P4, S11; Alternative E).
- **Whether C gets a tree for the R& shapes.** No; named in §*Known limits*
  with its count (Alternative F).
- **Whether the `worktree` arm, `-p`/`--pathspec-from-file`, aliases and
  quoted `>` are in.** No, each with its reason (`spec.md` §*Out, and why*).
- **What a word git would refuse reads as.** An option that takes nothing,
  which is today's reading of any `-` word (`spec.md` §*Scope*, In 1).

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| P1 | Does the reopening of `classify` the owner gave for #764 cover #738 too? The tree records the owner's act for #764 alone (milestone placement, #764's text); `routing.md`'s *Why this way* says both sit in `classify`, and that line is the orchestrator's, so the tree cannot settle whether the owner meant it. #738 itself offers two options, the fence or a named limit, and neither reaches into `classify` | **a person**: the owner. It is how far the frozen reading is opened, which P4 made the owner's to decide | **(a) Yes** — `classify` reads past redirections with its tree: the R1–R5 switches are asked and their restore twins stay silent (`plan.md` H). **(b) No** — `classify` reads git's option table only; #738 is named in §*Known limits* with its count (`plan.md` B), and its R1–R5 shapes keep switching unasked | (a). Answering (b) after the build removes the reduction from `classify`'s and `switch_kind`'s frozen side and adds the limit; the option table stays | ✅ answered (a) 2026-10-04, relayed by the orchestrator at the build's spawn: the owner's milestone batch for `release: 0.18.2` offered one bundle, "Gate·guard", holding #773, #764 and #738 together, and its option text said choosing it consents to reopening the frozen `classify`. The owner chose it, so the reopening covers #738 as well, and `classify` reads past the redirection with its tree |
| M1 | Does git 2.54.0 create or switch on every Axis 1 × Axis 2 spelling in `spec.md` (S1–S4, L1–L4, V), and which, if any, does it refuse? | **a measurement**: phase 1, one scratch repository, one command per spelling | A spelling git refuses leaves the class and its `KINDS` row reads `None`; every other spelling is a switch | every spelling switches, as `git help cli` documents | ✅ measured 2026-10-04 by phase 1 (executed, git 2.54.0, a scratch repository): every S1–S4 and L1–L4 spelling of every creating option switches (`switch --orphan` on a clean tree; it refuses over local changes), and so does every `--conflict` V shape. Two leave the class: `switch --c y`, an ambiguous prefix git refuses, and `checkout -U`/`--unified`/`--inter-hunk-context`, which git refuses without `-p` (`phases/phase-1.md`) |
| M2 | How many of the 27,351 recorded command and directory pairs (1790993140's corpus, cut 2026-10-03T11:06:22+09:00) does the build newly ask, and how many hold a quoted `<` or `>` in a checkout's name, or an R& operator inside a checkout or switch? | **a measurement**: phase 1 (before) and phase 3 (after), a deleted probe over the transcripts | A count, which the pull request's prompt budget and §*Known limits* carry. A nonzero new-ask count is reported with its shapes, not absorbed | the build proceeds; the counts are reported as found | ✅ measured 2026-10-04 by phases 1 and 3 (executed) over the 25,741 pairs still on disk of D1's 27,351: the build newly asks none and stops asking none; none holds a quoted `<` or `>` in a checkout's or switch's word; 81 hold an `&`- or pipe-led operator inside one, and in every one the frozen segment already holds the switch, so C fires on none (`phases/phase-1.md`, `phases/phase-3.md`) |
| W1 | Do C's views keep every answer when `_bare_words` reads through the local reduction instead of `wide.unglued` and `wide._without_redirections`? | **the work**: phase 2, by comparing the two reductions over `_shapes` for every verb | Equal everywhere: switch, one reduction. Any difference: keep `_bare_words` on `wide`, and record the shape as a divergence in `overview.md` | switch, after the comparison holds | ✅ answered by phase 2's work (executed): the two reductions gave the same words for all 50,568 views of the generated shapes, so `_bare_words` reads through `handed_words` (`phases/phase-2.md`) |
| W2 | Which released ledger rows the change drifts, beyond K5 and N1 (`seal/releases/0.18.0.md`) and G1 and its K5 re-read (`seal/releases/0.18.1.md`) | **the work**: phase 3, `bin/evidence-check --strict .` | Each drifted row is read and gets a `Re-read ·` row in this work item's fragment | — | ✅ answered by phase 3's work (executed): M2 (0.16.0), K5, K6, K7, N1 and `Corrected · G17` (0.18.0) drifted and still hold, each re-read; G1 (0.18.1) no longer holds and is `Corrected · G1` in this item's fragment (`phases/phase-3.md`) |
| W3 | The exact words of §*Which tree*'s first paragraph and of the #678 sentence | **the work**: phase 2 | Any wording that carries `spec.md` §*Scope*, In 4, and agrees with `switch_kind` clause by clause, pinned | the builder's | ✅ written by phase 2 at `332c0023` and pinned by `test_the_guard_policy_says_a_hidden_file_checkout_is_asked` and `test_the_guard_policy_says_what_it_reads_past_the_base`; read clause by clause against `switch_kind` |

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
