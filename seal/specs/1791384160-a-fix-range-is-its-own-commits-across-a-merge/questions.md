# a fix range is its own commits across a merge (#860, #805) — questions for the planner

<!-- seal/specs/1791384160-a-fix-range-is-its-own-commits-across-a-merge/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

**Judgments the two tickets left open that the tree answered.** Each is
decided in `spec.md` §*In* or in `plan.md`'s *Alternatives considered*,
where a reviewer can overturn it by opening what was opened. None of them is
reopened here.

**Judgments the reframe after round 3 made from the round records**, with
the grounds in `spec.md` §*Reframed after round 3* and `plan.md`
alternatives M–R. None needs a person.

- **How the rule is stated so another shape cannot falsify it** — one owner
  sentence that is the test the code runs, no example phrased by merge shape
  or by time anywhere in prose, the shapes as test cases against
  `own_commits`, and a vocabulary guard over the home and the carriers.
  Alternatives M, N, O, R.
- **The branch-versus-CI claim (probe D)** — the equality is dropped and the
  notice's input is stated: on CI's checkout the range also holds the base
  commits with round 1's target as an ancestor. The notice is not changed to
  read the pull request's head in CI. Alternatives P, Q.
- **The `fixed` refusal's string** — unchanged and outside the guard; S6
  pins it and its clause is true of every commit it refuses by construction.
- **The three test names that state the old claim** — left; each is true of
  its own fixture, and a test name is not a carrier.

- **First-parent or ancestry-path** (#805: *decide that first*) —
  ancestry-path. The parent order of a merge is set by whoever ran `git
  merge` and no party here controls it; descent from the range's start is a
  fact git holds. Alternatives B and G say what the other reading costs.
- **The order of a branched history** (what #805 says ancestry-path gives
  up) — a commit is named when no owned commit that changed the fragment
  descends from it. On a linear history that is the walk the notice already
  did; on a branched one it is a rule a person can state. Alternative F.
- **Which of #860's two closings** — neither as written. The measurement in
  `spec.md` §*Measured in this frame* found a file an own commit touched
  carrying 22 of the merged side's units, so the filter is per unit, not per
  path or per parent side. Alternatives C, D, E.
- **Whether the `-z` readers are this item's** — yes, all three, under one
  fixture. Alternative L.
- **Whether `call_sites`' textual reach is this item's** — no; only its path
  parse. `spec.md` §*Out*.
- **The `Fix range` count** — stays git's `a..b` count. Alternative H.
- **A new `*_FROM` cutoff** — none. `spec.md` §*Old records, and the
  `*_FROM` cutoffs*; alternative I.
- **The rule's home under the 1000-line ceiling** —
  `docs/the-record-layout.md`. Alternative K.
- **The `fixed` guard** — asks the owned commits. Alternative J.
- **`survivor_check`'s range** — out, with its answerer named in `spec.md`
  §*Out*.

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | What exact bytes does `git log --ancestry-path --no-merges --no-renames --name-status -z --format=%x01%H %h --reverse a..b` emit between the header, each status letter and each path? The tree cannot answer it: `commits_after` parses the `--name-only -z` form, and `--name-status -z` interleaves status and path with NUL in a way nobody here has written down | a measurement — one `od -c` over a scratch repository, by the smith in phase 1 before the parser is written | (a) `status\0path\0` per entry after the header's newline, parsed as pairs; (b) some other interleaving, parsed as measured. Either way the parse is written once in `own_commits` | (a), to be replaced by what the measurement shows | ✅ (a), measured on git 2.50 in phase 1: `\x01<full> <short>\0`, then `\n` before the first entry, then `<status>\0<path>\0` per entry; an empty commit is its header alone. Parsed positionally in `own_commits` (`phases/phase-1.md`) |
| Q2 | Does `git rev-list --ancestry-path --no-merges ^<target> F1 F2` with several positive refs list every owned commit that any `F` descends from, `F` included? The tree cannot answer it: the current code never passes more than one positive ref under `--ancestry-path`, and git's documentation defines the bare form by the excluded side alone | a measurement — the S9 case in phase 1, which plants two fragment-changing commits on two lines of history | (a) yes, one call; (b) no, one call per `F` and a union. Same answer, one or several calls | (a) | ✅ (a), measured in phase 1 and pinned by `test_a_fragment_brought_along_on_each_of_two_lines_clears_both`, which goes red with the call narrowed to the newest `F` |
| Q3 | Does `git grep -n -z` on the Windows leg emit the `<rev>:<path>\0<line>\0<text>` shape measured here on git 2.54 for macOS? The frame measured one platform | a measurement — the S10 fixture on CI's Windows shards | (a) yes; (b) a different separator on Windows, and the parse keys on what both emit | (a) | ⬜ |
| Q4 | `test_a_merge_on_the_branch_keeps_the_branch_as_the_tip` and `test_of_several_merged_heads_the_one_descending_from_round_one_is_the_tip` pin `walk_tip` by name and by premise · NAME NOT IN TREE. With `walk_tip` gone the first's side-topic commit is now named too. Which assertions and names do the two cases keep? Unknowable until the walk exists | the work — phase 1, when the cases run against the new walk; the phase record says what was renamed | (a) keep the shapes, rewrite the docstrings and add the new assertion (S9 is the first case's new half); (b) replace them with S8's three shapes under new names | (a) | ✅ (a), in phase 1, with the names changed as well: a name stating `walk_tip`'s premise would pin a mechanism that is gone. `test_a_topic_merged_into_the_branch_names_the_branchs_fix_and_the_topics_commit` (S9's first half, the topic's commit now asserted) and `test_of_several_merged_heads_only_the_commits_descending_from_round_one_are_named` (S8); shapes unchanged |
| Q5 | What does the new entry in `tests/test_the_rules_have_one_owner.py` look like — the home's exact section title, and which of the two scripts' docstrings and `orchestration.md`'s sentence count as carriers the test holds to a link? The tree answers the shape (rule 15 is the model) and not the words, which do not exist until phase 1 writes the home | the work — phase 2, after phase 1 has written the home | (a) one entry naming the home and three carriers; (b) the two docstrings left as prose that names no section, and one carrier | (a) | ✅ (a), in phase 2, with a fourth carrier: rule 17, owner §*A range owns the commits that descend from its start*, carriers `chain_check.py`, `round_record.py`, `skills/code-review/orchestration.md` and `docs/round-record-spec.md` (`phases/phase-2.md`) |
| Q6 | *(reframe)* Which words make up the guard's list? The frame proposes `sibling`, `topic`, `fork`, `back-merge`, `squash`, `made after`, `made before`, `once the`, `and not before` — the words rounds 1–3's false examples used. The tree cannot answer it: the texts the guard reads are the ones phase 6 writes, and a word on the list may be needed by a sentence that states no example (the home's account of #860 and #805, for one) | the work — phase 6, when the rewritten texts are run under the guard | (a) the proposed list, with the home's #860/#805 account reworded around it; (b) a shorter list, each removal named in the phase record with the sentence that needed the word. Either way the guard is red with round 3's 🟡 2 sentence pasted in | (a) | ⬜ |
| Q7 | *(reframe)* Where do the shape cases live — a module of their own, or `tests/test_the_fixes_close_the_record.py`, whose `_build` already makes `base` and `feature`? The tree cannot answer it: the close module's helper runs the generator with `--range`, and the shape cases assert `own_commits` directly, so whether its fixture serves is known when the first shape is built | the work — phase 5 | (a) a module of its own, which the home names by path; (b) the close module, which the home names by path and section. Same cases either way | (a) | ✅ (a), in phase 5: `tests/test_a_range_owns_what_git_lists_for_it.py`, whose cases call `own_commits` and `touched` directly (`phases/phase-5.md`) |

No row above is a person's. Every judgment a person could have been asked
was answered from the tree, with its grounds in `plan.md`'s table, and the
build does not wait on this file.

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
