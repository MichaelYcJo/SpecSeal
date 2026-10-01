# a joined project's `specs/` is read and never taken — questions for the planner

<!-- seal/specs/<unix-epoch-seconds>-<slug>/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

## What the frame decided from the tree, so nobody reopens it

The ticket left these open and the repository answered each. The grounds are
in `spec.md` and in `plan.md` §*Alternatives considered*, where the next party
can overturn one by opening what the frame opened. None of them is a row below.

| Judgment | Answer | Grounds |
|---|---|---|
| Which marks prove a `specs/<id>/` is the plugin's | `routing.md` as a file, or `rounds/` as a directory, directly under an id-shaped directory. Not `spec.md`, `plan.md` or `overview.md`, which a team may use | measured at tag `v0.3.0` with `git ls-tree`: 13 of 13 work-item directories carried `routing.md`, 29 `rounds/` files among them; `routing.md` was the first file every work item got (`git log --diff-filter=A -- 'specs/*/routing.md'`, 2026-08-31, the initial commit's day) |
| Whether the explicit adopt command ships in this item (box 5) | refused in `spec.md` §*What is refused*, with its reason; the plan does not wait on it | a marked directory is already moved by the hook or by the READMEs' by-hand block; an unmarked one moved under `seal/specs/` meets `settle`'s rule arm (`unverified_check.py#retired_by_rule`) or sits ungrouped; what is still true in a team document is a fold into `docs/`, not a move |
| Which checks reach outside the root, counted before any is changed (rule 4) | two read a reference root as a record — `survivor-check` (pool, range, `WORK_ITEM_DIR`) and `unverified-check` under its default path; two reach outside as the tree or a citer and are left — `evidence-check`'s `tree_names`/`scan_candidates`, `settle`'s `citations`; `correction-check`, `chain_check.py`, `settle --retire`, `evidence-check`'s two arms and `hooks/routing.py` are pinned; `deferral-check`, `arm-check`, `fold-check`, `broad-gate` walk no `specs/` | `spec.md` §*The checks, counted*, each with its coordinate |
| The default when the `Reference specs` row is absent | every directory named `specs` outside the plugin's root, as the ticket says; `none` declares no reference root | the joined repository has no `config.md` yet, and the default reads LESS as a record, which is the safe direction; `templates/config.md`'s rule that an absent row means what every repository got before |
| Where the resolver lives | `hooks/config.py`, loaded by path by the shipped scripts | `fold_check.py` and `broad_gate.py` already read optional rows that way; `hooks/config.py`'s own docstring rules `optin.py` out |
| Whether `docs/one-root-by-lifetime.md` is edited | yes, one dated section in both editions, in the shape its 2026-09-22 and 2026-09-23 sections use; nothing above it is rewritten | the record's own precedent for a later work item correcting a row; the record's line 30 and `root-migrate.py`'s step 5 already say a project may have had `specs/` first, so no decision in it is overturned |
| Whether the survivor sweep's standing statement in `docs/review-chain-spec.md` changes | yes, by one clause, *outside the reference roots*, and its `Enforced by:` line gains the new case | the ticket is the owner's statement that a team document is read and never checked; the statement's purpose — a corrected sentence that still instructs somebody — never covered a document the plugin did not write |
| Whether the hook names what it left when nothing of the plugin's moved | no; it stays silent, as its *silent when there is nothing to do* boundary says. It names an unmarked id-shaped directory only in the run that moved something | the hook is once per repository and stamps when nothing old is left; a line printed at every session start about a directory the plugin will never touch is noise with no act behind it |
| Whether a `.ko.md` edition exists for the agent and skill documents phase 5 edits | no — `agents/*.md`, `skills/*/SKILL.md`, `skills/implement/orchestration.md` and `templates/*.md` have no Korean twin; `README.ko.md` and `docs/one-root-by-lifetime.ko.md` do | `ls` of the tree |

## Rows

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | Does the Bootstrap paragraph's new wording trip `tests/test_no_document_names_the_old_roots.py`? Its `OLD_ROOT` pattern refuses `specs/<` outside `seal/specs/<`, so spelling the marks as *a `specs/<id>/` that carries …* needs a `KEEP` entry with a reason, and spelling them as *a `specs/` entry named `<unix-seconds>-<slug>`* does not. The tree cannot answer it before the sentence is written | the work (phase 2) | spell around the pattern (no `KEEP` change) · spell `specs/<id>/` and add the entry with its reason (the list grows by one line that must stay in use) | spell around it | ✅ decided in `phases/phase-2.md`: spelled around — no line spells `specs/<`. The rewrap still tripped the pattern's other half, `.specseal/`, on the line the old `KEEP` key no longer matched, so one `KEEP` entry with its reason carries that line |
| Q2 | What is the survivor pool's examined count on this repository before and after reference roots leave it? The ticket's *530 files at #674's round 2* was not found in any `rounds/round-2*.md` under `seal/specs/`, so no figure stands here | a measurement (phase 3 runs `bin/survivor-check --range cd24f516..HEAD` in the worktree before and after its change, and the hand-back carries both numbers) | — | no number is written until measured | ✅ measured in `phases/phase-3.md`: `examined 555 files at 6fd620b` before the change and `examined 556 files at f0e626c` after, the one file being the new test module; at `f0e626c6` the pool is 556 with the predicate and 556 without, because no tracked path sits under a `specs` directory outside `seal/`. The ticket's 530 is not reproduced and is not this repository's figure |
| Q3 | Once reference roots are out of the pool, does `survivor_check.py#records_a_past_round`'s shape test (`"specs" in parts[: parts.index("rounds")]`) still need to match a team `specs/x/rounds/` at all, or is that branch unreachable for a reference root and left as is? The tree cannot say until the predicate and the exclusion sit side by side | the work (phase 3) | leave the shape test, since the path is already out of both sides · narrow it to `seal/specs` with `WORK_ITEM_DIR`, and re-read `seal/releases/0.9.3.md:90` | leave it; `WORK_ITEM_DIR` alone narrows | ✅ decided in `phases/phase-3.md`: left. Under the default a team's `specs/x/rounds/` is out of both sides by `a_reference_root` before the shape test is asked, so the branch decides nothing there; under `Reference specs \| none` it reads such a file as a past round, the shape it has matched since it shipped. Narrowing it would drift `seal/releases/0.9.3.md:90` for no reader |
| Q4 | The `.github/workflows/hygiene.yml` and `broad_gate.py` hand `unverified-check` the path `seal/specs/`, so the default-path prune in phase 4 reaches only a by-hand run. Does any shipped document tell a person to run `unverified-check .` or `unverified-check specs/`? The module's own docstring says `unverified-check specs/` as prose | a measurement (`grep -rn "unverified-check" README.md README.ko.md skills/ docs/ templates/` in phase 4; a hit is a sentence to correct in that phase, a miss is nothing to do) | — | the docstring's `specs/` is read as the 0.3.x spelling and reworded to `seal/specs/` in phase 4 | ✅ measured in `phases/phase-4.md`: three hits tell a person to run `unverified-check .` — `README.md`'s and `README.ko.md`'s command tables and `skills/verify/SKILL.md`'s example — so the by-hand run the prune reaches is a documented one; each sentence is true after the change and none is corrected. Nothing says `unverified-check specs/` but the module's docstring, reworded to `seal/specs/` |

**`Who can answer` takes one of three values and nothing else.** They were one
shape on the page before this, and #84's second comment measured all three
inside a single run's four rows.

- **a person** — what the product should be, or a value somebody has to be
  accountable for. This is the file's stated purpose, and the only kind of row
  that blocks the build. **This frame has none**: the ticket is the owner's
  own rule, and what it left open the tree answered above.
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
