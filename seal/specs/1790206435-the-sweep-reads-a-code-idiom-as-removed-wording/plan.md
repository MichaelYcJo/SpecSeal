# Implementation Plan: the sweep reads a code idiom as removed wording

<!-- seal/specs/1790206435-the-sweep-reads-a-code-idiom-as-removed-wording/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved 2026-09-24 by the orchestrating session on the owner's `automation` answer, when `smith` was spawned.

## Summary

Four phases, one ticket each and then the records, in the order the harm is
met. Phase 1 changes what a sentence is in a Python file (#543): comments,
docstrings and string literals are read, code is a separator, and the same
reader serves the range and the pool. Phase 2 puts a released changelog
section and a gathered fragment in the class the sweep already leaves out
(#307), by heading and by marker rather than by path. Phase 3 asks the
ownership question of an unresolved declaration before printing it (#439),
which is the second anchor applied one step earlier than today. Phase 4 is
the records: the ledger re-stamp over the drifted rows, the fragments, the
closing memo, the counts the measurements produced, and the branch's own
sweep.

Nothing in the arithmetic moves. `wanted`, `carriers`, `runs`, `weights`,
`weigh`, `score`, `exempted`, `read_exemptions` and `FLOOR` are not edited,
and the founding cases over the two fixture tags are the check that the
reader took nothing it should have kept.

## Technical context

- `skills/code-review/scripts/survivor_check.py#sentences` — `Sentence`
  objects from `segments(blank_struck(text))`. Both `corrected` (the range,
  at `a` and at `b`) and `corpus` (the pool, at `b`) build every sentence
  through it, so a reader placed here or in front of it holds on both sides
  by construction.
- `#blank_struck` — the model for a region blank that keeps line numbers:
  every character of the span becomes a space, every newline stays.
- `#segments` — two passes: `BLOCK` per line, then `END` inside a block.
  `END` includes `|`, which is what a blanked code token can leave behind to
  end a sentence between two literals. `BLOCK` reads a `# ` line as a
  heading, which is why a comment block is one sentence per line today and
  stays so (`spec.md` §*Out*, first row).
- `#corrected` — `git diff --name-only` filtered by `records_a_past_state`,
  then by `retired_directories`; `read_blobs` at `a` and `b`; `gone` and
  `written`. `#corpus` — `tracked(root, b)` filtered by the same predicate.
  The gathered-fragment test needs `CHANGELOG.md` at `b` in both, one
  `read_blobs` call.
- `#records_a_past_state` — a pure path predicate, anchored by E1–E3 and
  named as `PREDICATE` in the test module, which asserts `corrected` and
  `corpus` mention it. A sibling that takes the gathered set, or a
  parameter with a default, both keep that assertion green.
- `#reader` loads `skills/verify/scripts/unverified_check.py`, whose
  `FOLD_MARKER` is `^<!-- specs/(\S+) -->$` — the marker shape a gathered
  fragment carries in `CHANGELOG.md`. `.github/scripts/gather_changelog.py#marker`
  writes it and `#ungathered` reads it by whole-text membership; the sweep
  reads the same marker itself, because a shipped script does not import
  release automation (the fold's own `survivors.md` row says so of
  `fold_ledger.py`).
- `#whole_range` — resolves each declaration first; an unresolved one is
  appended and the loop continues; ownership is asked only of a resolved
  match, with `changed` computed lazily from `git diff --name-only`. The
  test module's `NAMED_EXCEPTION` grounds require `foreign` to stay in the
  body and the function to stay unfiltered by the predicate.
- `#report` — prints `unresolved`, `not yours`, `declared`, `exempt`, the
  standing rows and the two closing sentences. Phase 3 changes what reaches
  it, not what it prints.
- The module docstring §*What is excluded, by construction rather than by
  list* — `EXCLUSIONS` in the test module lists the three openers in order
  and asserts each paragraph names `pool`, `range` and `both sides`.
- `tests/test_a_corrected_sentence_survives_elsewhere.py` — `build`, `run`,
  `over`, `resolves`, `paths_in`; the two fixture tags; the probe pattern of
  lines 444–530; `one_survivor` and `base_and_item_a` for the range-row
  cases. The founding case asserts `named == [PIN_CARRIER]`, so any new
  false positive on that range is red there.
- The standard library's tokenizer: on 3.12 an f-string is FSTRING_START,
  FSTRING_MIDDLE and FSTRING_END with the expression parts as ordinary
  tokens; below 3.12 it is one STRING. The repository's floor is 3.12
  (`round_record.py#FLOOR`), and the sweep declares none, so the kept kinds
  are read off the module by name with a fallback for the older shape. A
  tokenizer error — an unterminated string, a bad dedent — is caught whole
  and the file is read as prose, which is today's reading.
- The four fixture ranges and every count: `spec.md` §*The measured state*.
- `.github/workflows/hygiene.yml`'s survivor step and the sealer's
  `survivors` arm pass every `seal/specs/*/survivors.md` over
  `origin/<base>...HEAD`. Unchanged.

**Failure scenario of the chosen approach, six months out.** A survivor
hides where the reader stops looking. Two shapes, both named rather than
prevented: a rule pinned in a workflow file's shell block or a JSON hook
table, which was never Python and is read as it always was; and a rule
stated in a `.py` file in a form the tokenizer calls code — a long
identifier, a dict of bare names — which no longer reads as words. The
first is `spec.md` §*Out*; the second has no measured instance and every
pin this repository writes is a string. The changelog rule's own failure is
a repository whose released heading takes a shape the version pattern does
not know, so its sections stay live and are reported as today — the
direction that costs a row, not a defect. The ownership rule's is a
declaration whose work item directory is renamed while it lives, which then
prints nothing to anybody; no directory has been renamed in this
repository's history and `settle` retires rather than renames.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| Read only comment and docstring tokens of a `.py` file (#543's first candidate as written) | #269's survivor is two adjacent string literals in a test's dict — not a docstring — and the founding case goes red. Every pin this repository writes is a string constant | Refused; string literals are kept, and a code token between two of them ends the sentence |
| Weigh an n-gram by document frequency (#543's second candidate) | Already done: `weights` is `log2(F / df) / log2(F)`, and the six instances cleared the floor under it because a specific three-word run of code is rare the way a specific three-word run of prose is. Making common runs score near zero means re-scoring runs by something other than their rarest n-gram, which reopens the 77-range calibration S1 and S2 record | Refused |
| A per-file-kind floor (#543's third candidate) | The loops scored up to 2.77 and #269's real `.py` survivor scores 1.89; no floor separates them. A constant calibrated against six instances is the `SHARED_FLOOR` mistake S1 records | Refused |
| Skip `.py` files entirely | A docstring is exactly where a removed rule survives (#543 §*What a fix has to keep*); A's real survivor is a removed comment; #269 is a `.py` file | Refused |
| Exclude `CHANGELOG.md` whole by path, in `records_a_past_state` | Right for this repository, where the file is all released sections. Wrong for a repository following `agents/smith.md`'s *let the entry accumulate unreleased*, where the sweep would stop reading live prose | Refused; the released region is read off the heading, and here the two agree |
| Import `gather_changelog.py#ungathered` for the gathered test | A shipped script depending on this repository's release automation, which the fold's `survivors.md` row already refuses for `fold_ledger.py` | Refused; the marker is read once more, the shape `FOLD_MARKER` already spells |
| Print unresolved declarations once, as a count | Reports less loudly rather than to the right reader: the count still reaches every run and still names nothing a reader can act on | Refused |
| Leave the `unresolved` lines as they are and close #439 on R7's note alone | The three lines print on every pull request into a release branch and on every seal until three shipped directories retire, addressed to runs that could never have used them | Refused; the second anchor is asked first |
| A `settle` change retiring a shipped work item's range row | Not the sweep's, and the directory retires whole at the fold already; the line's cost is the sweep printing it to the wrong run | Refused |

## Phases

Vertical slices — each phase ends with something runnable and verified.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **A Python file's prose is its comments, docstrings and string literals** (#543). The reader in front of `segments`, keeping COMMENT, STRING and FSTRING_MIDDLE text in place with a sentence end where every other token stood, line numbers intact; a tokenizer error falls back to today's reading; the docstring gains a section stating the rule. Cases S1, S2, S4, S5, S6 (the four real ranges, skip-when-absent), each seen red first; S3's existing case unchanged and its score recorded | `bin/test tests/test_a_corrected_sentence_survives_elsewhere.py -q` — the module's case count read directly; S6's counts against `spec.md` §*The measured state*: A 5 → 1, 0 5 → 4, C 2 → 1, B 9 → 9, prose coordinates unchanged; `questions.md` Q1, Q2 and Q6 filled | 476af109 |
| 2 | **A released changelog section and a gathered fragment are records** (#307). The region blank over a root `CHANGELOG.md` keyed on version headings, and the gathered set from the tip's `CHANGELOG.md` applied in `corrected` and `corpus`; the docstring paragraph with pool, range and both sides; `EXCLUSIONS` extended. Cases S7, S8, S9, S10 (two), S11, S12, the red-first ones seen red | The same module; S12's counts: B 9 → 8, C 1 → 0; `test_every_path_list_this_module_derives_from_git_is_filtered_or_named` green with no new path list; `questions.md` Q3 and Q4 filled | 93acc277 |
| 3 | **An unresolved declaration prints only to the run it addresses** (#439). `whole_range` asks ownership of an unresolved declaration with the same lazy `changed` list; the docstring's *A spec that will not resolve is REPORTED* paragraph says to whom. Cases S13 and S14, S13 seen red first; the existing G6 case unchanged | The same module; `bin/survivor-check --range origin/release/v0.15.1...HEAD` with every `seal/specs/*/survivors.md` prints zero `unresolved` lines (S15, read at the seal too); `questions.md` Q5 filled | 78610546 |
| 4 | **The records.** `evidence-check --reverify .` over the rows `spec.md` §*Data & interfaces* names, each re-read first; the ledger fragment's new rows anchored on the phase 1–3 units; `changelog.md`; `overview.md` with its `## Not verified` table; the count of existing `survivors.md` rows of the two classes (Q3) in `overview.md`; the branch's own sweep and its `survivors.md` for the docstring sentences this branch rewrites that ledger rows quote | `evidence-check --strict .` exit 0; the branch's sweep at exit 0 with every report either corrected or under `exempt`; the three narrow modules the edited files are read by | |

This table is also where the work records how far it got. There is no separate
task list: a list of tasks is mutable progress, and a stale one asserts a state
that is not true, which is the failure the evidence ledger exists to prevent.

**Status is empty, or the commit that closed the phase.** A tick is refused,
and so is `done`: both can be typed without anything having happened, and both
assert a present state that nobody can check. A commit hash asserts a past one
— someone can open it — which is the same trick that lets a round record live
beside the contract rather than in tool state.

Fill it in as each phase closes, not at the end. A phase reconstructed
afterwards is reconstructed from the diff, which is where it already was.

What a phase discovers while it is being built, and needs the next phase to
know, does not fit in this table's cells. Write it to
`seal/specs/<work-item-id>/phases/phase-N.md`, from `templates/sdd-phase.md`,
when the phase closes.

One caveat, so nobody builds on it, and it has two halves. Where feature
branches squash, these commits stop resolving at the merge — and **a rebase
during the work does the same thing earlier and far more quietly**, because the
orphaned object still answers `git cat-file` in the worktree that wrote it.
The quiet half is the one that bites: this column was wrong on its own first
use, nine SHAs deep, and only a reviewer opening them found it. **Re-read the
column after any rebase**, or it names commits that resolve in one clone and
nowhere else. That is tolerable because nothing measures from this column.
The evidence ledger had the same problem and no such tolerance. It no longer
has it at all: a ledger row names a symbol and a content hash, so there is no
commit in it for a rebase to orphan.

## Operational impact

No migration, no new dependency, no environment variable. The sweep is a
gate — it can refuse a pull request into a release branch and it is one arm
of the seal — so each phase carries `CONTRIBUTING.md` §*What a change to a
gate must carry*:

| Phase | Test seen red | Failure direction | Prompt budget | Platform |
|---|---|---|---|---|
| 1 | S1 at exit 1 naming the second loop; S4 with the line named; S5 with the fallback deleted | The gate **reports less**, and only for tokens the tokenizer calls code. The wrong allow is a rule stated as bare identifiers in a `.py` file, which has no measured instance; the wrong deny is what stands today, six instances on four ranges and one red hygiene job on a merge | zero | the tokenizer is the standard library's, the same on every platform; a tokenizer error falls back rather than refusing |
| 2 | S7 at exit 1; S9 naming a released line as corrected; S10's gathered case at exit 1 | The gate **reports less**, and only for prose no branch may correct. The wrong allow is a released note going stale, which is what a released note is; an ungathered fragment and an unreleased section are still reported, which is the half that must not move (S8, S10) | zero | file reads only |
| 3 | S13 with the line printed | The gate **prints less**: an unresolved declaration of a work item the range touches nothing of. It excuses nothing whether printed or not, so the wrong allow is empty; the wrong deny was three lines on every seal of one release | zero | one `git diff --name-only`, already made lazily today |
| 4 | none — records | none | zero | none |

Every open branch of 0.15.1 that carries a `survivors.md` may see a report
disappear at its next CI run; none can see a new one from phases 1–3 except
through the weighting — dropping code carriers raises the weight of every
phrase they held, the direction S6 measured as 1.69 → 1.79. S6 of this spec
reads the four real ranges coordinate for coordinate so that movement is
seen rather than assumed.
