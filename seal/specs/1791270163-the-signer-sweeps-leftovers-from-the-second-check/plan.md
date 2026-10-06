# Implementation Plan: the signer sweep's leftovers from the second check (#831)

<!-- seal/specs/1791270163-the-signer-sweeps-leftovers-from-the-second-check/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved 2026-10-06 by the orchestrating session under the owner's `per axis` answer (smith named), when `smith` was spawned.

## Summary

Three code edits and one records pass, each already executed once by the
second post-review check in a throwaway clone and written up as paste-ready
text in
`seal/specs/1791239490-a-repository-that-keeps-a-pact-is-a-signer/post-review-check-2.md`
§*Paste-ready fixes*. The build's work is to land them in the tree, see each
case red the way §15 asks, and write the records the frozen ledger requires.
Budget: about 45 minutes of smith time, three commits.

Order: the sweep first (finding 1), because it is self-contained and makes R6
true before the records pass reads it; then `read_table` and the S4 case
together (findings 3 and 2), because both edit the same case and the
`read_table` change is what the case's new expectations are written against;
then the fragment, the changelog and the memo.

## Technical context

- `tests/test_one_word_one_meaning.py#without_the_policy_span` (line 725;
  the `re.search` at 737). Ends the excluded span at `\n[ \t]*\n`, an ATX
  heading or a fold marker. The f1722cec version ended at any `---`; #830's
  version lost that, which is the one regression in the set. The two sweep
  cases that call it are `test_no_pact_text_names_a_signer_the_way_0_18_did`
  (756) and `test_no_live_text_says_the_word_0_19_0_renamed` (847). The
  module has 21 cases.
- `hooks/config.py#read_table` (line 1325; the glued sentence at 1364).
  `glued = holds_old and any(cells == old for _line, cells in rows)` is
  computed before `rows` is filtered; `named` is rebuilt from the old
  header's cells with spaces. `gfm_table` (the `lines = text.splitlines()`
  line and `rows.append((index + 1, found))`) numbers rows 1-based into
  `text.splitlines()`, so the as-written line is
  `text.splitlines()[line - 1]`. `read_table`'s strings are swept by
  `PACT_PRINTED` for the old word; the new f-string adds none.
- `tests/test_a_signer_declares_its_pact.py#test_s4_a_pact_holding_both_tables_reads_signer_and_refuses_the_old_one`
  (line 1216). The glued loop (1256–1265) iterates three `under` shapes, the
  first unspaced, and asserts the spaced `glued` sentence for all three; the
  last assertions (1269–1273) end the case. The module is one of six
  (`test_a_signer_declares_its_pact.py`, `test_pact_check.py`,
  `test_a_pact_review_takes_a_pact_change.py`,
  `test_one_table_walker_reads_what_gfm_renders.py`,
  `test_a_signers_ci_prints_its_pact.py`, `test_one_word_one_meaning.py`)
  that read `read_table`'s output or strings; the second check ran them at
  3447 passed.
- `seal/releases/0.19.0.md` lines 22 (`Corrected · P8`), 31 (`R1`) and 36
  (`R6`) are the released rows whose coordinates this work moves:
  `hooks/config.py#read_table` at hash `9a14e9d5` (P8, R1),
  `tests/test_a_signer_declares_its_pact.py#test_s4_…` at `c2600db0` (R1),
  `tests/test_one_word_one_meaning.py#without_the_policy_span` at `7398e765`
  (R6). `grep` over `seal/releases/*.md` and `seal/ledger.md` finds no other
  row citing those three units (read, 2026-10-06). `seal/ledger/` does not
  exist on the branch; the fragment's first row creates it.
- `bin/evidence-check --reverify --into <fragment> --checked <date>` writes
  one `Re-read ·` row per released row with a drifted coordinate, citation
  computed by `citation_for`, and re-stamps fragments in place
  (`skills/evidence-check/scripts/evidence_check.py#reverify_into`, read).
  A `Corrected ·` row supersedes its family and must carry every coordinate
  the claim still rests on, because a coordinate it leaves out is never
  checked again (`docs/the-evidence-ledger.md` §*A released row is read
  again in the branch's fragment*).
- Record language: `seal/config.md` has no `Record language` row, so every
  record is English.

**What breaks in six months.** The widened span end lists GFM's
paragraph-interrupting blocks by hand. A new shape nobody listed — the next
block kind, or a line of `docs/the-pact.md` that happens to begin with `<`
or `>` inside the statement — either leaves text exempt again or turns the
baseline red. The first reads as a quiet gap, the second as a loud one; the
sweep module's own cases catch neither, and the next post-review check is
what has caught each so far. Rendering the statement through `cmarkgfm`
(which `tests/gfm_table_oracle.py` already imports) and cutting at the end of
its first `<p>` would replace the list with the renderer, and is the
alternative refused below for size.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| Widen the regex to every block GFM lets interrupt a paragraph (the second check's fence) | a block kind not listed stays exempt; a statement line starting with a listed marker ends the span early and the baseline goes red. Stricter, never looser, than today | **chosen** — executed once already (six plants red, continuation green, 21 passed), fits the 45 minutes, and the docstring's sentence becomes true as written |
| Render `docs/the-pact.md` with `cmarkgfm` and cut the span at the end of the statement's `<p>` | the test module takes a renderer dependency the sweep did not have; mapping rendered output back to source offsets is new code with its own cases | refused for this item — a mechanism, not a fix, and `skills/implement/SKILL.md` §5 says a fix pass adds none; filed in `overview.md` §*Not done* if the smith judges the regex too brittle, naming the owner |
| Quote the glued line from `text.splitlines()[line - 1]` (the fence) | a reader whose line numbers came from another split would quote the wrong line; both `gfm_table` and the quote use `splitlines()`, so none does today | **chosen** — read against `gfm_table`; the S4 case's first shape pins it |
| Change the glued sentence's noun from `line` to `header` and keep the spaced quote | the stray-row refusal already quotes the same header as written, so the two sentences would still disagree with each other and with the file | refused — the person deletes a line, and the sentence should name the line they will find |
| Pin finding 2 by a new `def` | `docs/the-pact.md`'s `Enforced by:` line lists the S4 case by name; a new `def` changes nothing there but splits one shape's pins across two cases | refused — the fence's assertions go at the end of the S4 case, as the second check placed them |
| Finding 4: turn the `Re-read · R1` row `--into` writes into the `Corrected ·` row, carrying every R1 coordinate | a coordinate dropped from the `Corrected ·` row is never checked again | **chosen**, with the check: the row's coordinate list is R1's list, each at its current hash (the run re-stamps a stale one in the fragment in place); `bin/evidence-check` at exit 0 afterwards |
| Finding 4: re-read R1 and leave its claim | the claim "refused once, as a line inside that table" is false for finding 2's shape, and a `Re-read ·` dates a false claim as read true | refused — the 1791239490 precedent for P11 and E6 (`overview.md` there, the two drift-only rows) |
| Changelog fragment names only finding 3 | a reader of 0.20.0's note does not learn the sweep moved; the issue title leads with it | partly refused — one `### Fixed` entry, the printed quote first, the sweep in a second sentence, the two test gaps and the ledger correction unmentioned because a release note is for what a user observes |

## Phases

Vertical slices — each phase ends with something runnable and verified.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | `without_the_policy_span` ends where GFM ends the statement's paragraph (finding 1): the `re.search` from the fence replaces line 737; the docstring stands | each of the six block plants seen red (W1 says how) and the lazy continuation line green, then `bin/test tests/test_one_word_one_meaning.py -q` exit 0 read directly | ee631b6b |
| 2 | `read_table` quotes a glued old header as written (finding 3); the S4 case's glued loop expects the as-written quote and gains finding 2's shape at its end | red first, twice: the S4 case against `read_table` with the two fence lines reverted (the first glued shape fails on its spaced expectation), and the new assertions with the `rows = […]` filter moved back inside the `if holds_old and not any(…)` branch; then green, and `bin/test` over the six modules in §*Technical context* exit 0 read directly | 94f22603 |
| 3 | The records: `seal/ledger/1791270163-….md` from `bin/evidence-check --reverify --into seal/ledger/1791270163-the-signer-sweeps-leftovers-from-the-second-check.md --checked 2026-10-06` (M1: three `Re-read ·` rows expected, P8, R1, R6), R1's row turned `Corrected · R1 ·` with ⬜ 4's wording, all of R1's coordinates and the notes fact; `changelog.md` under `### Fixed`; `overview.md` with `## Not verified` naming the broad gate's answerer; `phases/phase-1..3.md` | `bin/evidence-check` exit 0 with `0 drifted · 0 broken`; `git diff --stat origin/release/v0.20.0 -- seal/releases/ seal/ledger.md` empty; `python3 .github/scripts/gather_changelog.py --dry-run --version 0.20.0` exit 0; `unverified-check` shape by reading `overview.md` against `skills/implement/SKILL.md` §4 | |

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

One caveat, so nobody builds on it: feature branches squash into their release
branch here, so these commits stop resolving at the merge, and a rebase during
the work orphans them earlier and more quietly. **Re-read the column after any
rebase.** Nothing measures from this column; the ledger names no commit, so it
has no such problem.

## What the smith does not do

- Runs no broad gate. `routing.md` routes this item `straight to the PR` and
  `stop before the pull request`; the full suite, lint and typecheck are the
  pull request's CI, named in `overview.md` §*Not verified*.
- Edits nothing under `seal/releases/`, `seal/ledger.md`, `changelog/` or
  `docs/the-pact.md`.
- Adds no mechanism: no renderer in the sweep, no new checker, no new `def`.
- Leaves no probe behind (§7): a `test_tmp_*` file used for phase 1's red is
  deleted before the commit, and a plant made in the working tree is
  reverted, which `git status` shows clean.

## Operational impact

None. No migration, no environment variable, no dependency, no compatibility
break: `read_table`'s signature and return are unchanged, and a pact or
review record that read before reads the same, with one refusal sentence
quoting its line as written.
