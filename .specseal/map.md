# spec-to-code map

> Maps spec clauses to the code coordinates that ground them, so the next
> session opens a coordinate instead of re-searching — locating the code is the
> expensive half, and this file exists so it is paid once. Written and checked
> by machines (`evidence-check`); committed so it follows worktrees and other
> machines.
>
> This is SpecSeal's ledger for SpecSeal. It opens with the tree's first
> commit as its baseline, which is the only commit every row here can measure
> from.

## Baseline

| Item | Value |
|---|---|
| Baseline commit | `9829412277fa11f81b61df7850183ae3fa9d8a05` (2026-08-31) — the fallback for rows with no baseline of their own; open with `git show 9829412:<path>` when in doubt |
| Coordinate notation | `<path>:<line>` from the repo root |
| Trust exceptions | none |

Each row's **Checked** column carries the date AND the commit SHA it was read
at, and drift for that row is measured from there. Rows without one fall back
to the baseline above. Re-verify row by row; bumping the header instead
re-dates every claim without re-reading one.

**Quote a markdown row's name without its pipes.** Write `` `Fixes checked by` ``
and not `` `| Fixes checked by |` ``: a row of this table splits on every `|`
in it, so the second spelling makes a 5-cell row into a 7-cell one and slides
every column two to the right. Two rows below did that, and on one of them the
**Checked** column landed on prose instead of a stamp — which is not a typo but
a silent fall back to the header baseline, the exact thing the per-row stamp
exists to prevent. `evidence_check.py` reads coordinates out of the text and
never checks a row against its section's header, so it reported `24 ok` on
both. Whether it should is issue #31's, not this file's.

## Scope decisions

Judgments that don't follow from code or documents alone.

| Decision | Content | Grounds |
|---|---|---|
| The ledger opens at one commit | Every row below is stamped at this tree's first commit rather than left to the header alone | A row with no stamp of its own measures from the header, and a header nobody re-reads re-dates every claim at once. Stamping them all at the baseline costs nothing today and makes the first genuine re-verification visible |

## Routing declarations

| Clause | Code grounds | Verified behavior | Checked | Notes |
|---|---|---|---|---|
| The Review and Destination axes are strict; a value outside the vocabulary makes the file not a declaration | `hooks/routing.py:45`, `hooks/routing.py:49` | Read, not run. `parse` returns `None` unless both answers are members | 2026-08-31 `9829412` | The Implementation axis is deliberately lenient at the same coordinate |

## Rider stamps

| Clause | Code grounds | Verified behavior | Checked | Notes |
|---|---|---|---|---|
| Every `# RIDER:` carries the date and SHA it was verified at, and the SHA is an ancestor of HEAD | `tests/test_a_rider_reaches_its_file.py:111` | Executed: the suite passes on this tree, and the eleven riders are stamped at the baseline commit | 2026-08-31 `9829412` | The stamps were re-cut for this tree; the commits they named before do not exist here |

## Edits that reach the commit gate

| Clause | Code grounds | Verified behavior | Checked | Notes |
|---|---|---|---|---|
| The gate reads a heredoc body as commands, so a heredoc that only patches a file is judged by what its body says | `hooks/commit-review-gate.py:151` | **Executed**, twice independently: a body carrying a commit on its own line returns True under both `cat > f <<'EOF'` and `python3 - <<'PY'`, and False for a body carrying none | 2026-08-31 `f1cd65d` | Deliberate, per legacy #75: a commit hidden in a body used to walk straight past. The agent files now route file edits through the `Edit` tool, so no command line reaches the reader at all. Whether the reader should skip a body being written to a file is Q1 of `specs/1788184145-the-gate-stops-the-session-editing-its-tests/questions.md` |
| Only a segment whose command word is `git` with the `commit` subcommand is counted, so a commit sitting inside a string literal is not | `hooks/commit-review-gate.py:144-147`, assembled in `commit_invocations` at `hooks/commit-review-gate.py:262-286` | **Executed**, round 1's probe. Whole fixture files handed to `_hides_a_commit` are clean — `tests/test_gate_judges_the_repo_it_commits_to.py` and `tests/test_what_the_reader_understands.py` both — while `agents/smith.md` and `README.md` TRIP, each only on its own `[no-review]` waiver example | 2026-08-31 `f1cd65d` | This refutes both readings that preceded it. It is NOT "the fixtures are shell command strings, so the reader finds a commit in them", and it is NOT "the documents are what trip it": issue #34's eight-line PARTIAL patch of a fixture trips as well. A fragment is judged on its own quoting, not on the file it came from |
| A segment the reader cannot expand counts as a commit, so a body with no `git` in it at all can stop the session | `hooks/commit-review-gate.py:148-150`, resolved by `_eval_hides_a_commit` at `hooks/commit-review-gate.py:176-188`, against `EXPANDS` at `hooks/cmdline.py:678` | **Executed**, four bodies: `eval "$CMD"` TRIPS · `eval $(cat f)` TRIPS · `eval "echo hello"` clean (no expansion character) · `print('hello')` clean | 2026-08-31 `f1cd65d` | Fail-closed by design — the docstring says nothing can tell *reduces to a commit* from *reduces to something else* without running the shell. This is the branch a reader misses: searching a patch for a commit and finding none does not clear it. `tests/test_what_the_reader_understands.py:89` is an `eval` fixture, so a partial patch of that file is exactly the case |
| Prose added to a document can flip the gate's verdict on that whole document without containing a commit at all | `hooks/commit-review-gate.py:144-147` | **Executed** while fixing round 1. `agents/warden.md` is clean as a whole; adding one paragraph with a single apostrophe (`the fragment's own quoting`) made it TRIP, because the odd quote flipped the reader's state and put the `[no-review]` row in its probe table into command position. Removing the apostrophe restored `clean`. Round 2 confirmed the parity at the same coordinate: 0 → clean · 1 → TRIPS · 2 → clean · 3 → TRIPS | 2026-08-31 `f1cd65d` | **What is parity-sensitive is the apostrophes ADDED above the waiver row, not the file's absolute count** — measured after round 2's edit, `agents/warden.md` holds 11 apostrophes above that row, an odd number, and the file is still clean. Backticks and double quotes interact, so only the whole-file verdict answers this; a raw count does not. Measure above the waiver row, never below, because quote state flows forward. Pinned by `tests/test_edits_go_through_the_edit_tool.py::test_the_warden_file_does_not_itself_trip_the_commit_gate`. `agents/smith.md` is deliberately not pinned — it has tripped at its own waiver example since before this work |

## Who checked the last round's fixes

| Clause | Code grounds | Verified behavior | Checked | Notes |
|---|---|---|---|---|
| The last round's fixes are read by nobody, and the box saying the review passed is ticked by the session that wrote them | `specs/1788184145-the-gate-stops-the-session-editing-its-tests/rounds/round-3.md:12` | **Read**, in the record's own comment: four findings *raised by the reviewer, verified by the orchestrator and fixed by the orchestrator* in one commit *rather than by a fourth round*, beside `- [x] Pass` | 2026-09-01 `46b66d9` | The second measured case, one work item after issue #33's own. The first is `1788137177-the-axis-nobody-was-asked`, where round 2 found seven defects inside round 1's fixes and round 2's own then went in unread — the whole hit rate on the one set anybody opened. The fixing commit is named in round 3's own record rather than here: `row_baseline` takes the FIRST resolvable SHA-shaped word in a row, so a second hex word anywhere in this line would silently become the row's drift baseline in place of the stamp |
| Reading `Fixes checked by` on the last record alone makes `round-N` unreachable | `skills/code-review/scripts/chain_check.py:1069` | **Executed**, by mutation: with the read scoped to `records[-1]`, breaking the sibling lookup outright (`if name in siblings`) left `test_a_later_round_that_exists_is_a_checker` GREEN, because the last record's cell is the only one opened and it can never hold a `round-N` | 2026-09-01 `46b66d9` | A checker has to be a LATER round; the last record is the highest-numbered one, so no such record exists. The value is dead under that scope, which is why this read is per-record where `Pass` is not. The trade is Q2 of this work item's `questions.md` |
| A cell inside an HTML comment is not the row, because the shared reader strips comments before splitting | `skills/code-review/scripts/chain_check.py:1098`, through `skills/verify/scripts/unverified_check.py:105` | **Executed**: a record whose only such row sits inside `<!-- … -->` fails with the *no `Fixes checked by` row* error, and replacing `reader.readable(text)` with `text.splitlines()` turns that exit 1 into exit 0 | 2026-09-01 `46b66d9` | The template explains the field in a comment beside it, so a record that keeps the template's comment is the ordinary case rather than a contrived one. Pinned from both sides — `test_a_cell_inside_a_comment_is_not_the_row` and `test_the_template_row_is_a_row_and_not_an_explanation` |
| An unrecognised value is refused rather than read as a checker | `skills/code-review/scripts/chain_check.py:1054`, `skills/code-review/scripts/chain_check.py:303` | **Executed**: `the session that wrote them` exits 1 naming the three values. The separator set had to include the SPACE — without it `nobody — <why>`, the one spelling every document shows, was itself refused, which the case asserting it passes is what found. The set is also what makes `nobodys fault, really` an unrecognised value rather than a `nobody` with a reason | 2026-09-01 `46b66d9` | The direction `CLOSED_WORDS` already takes for a verdict cell, at `skills/code-review/scripts/chain_check.py:234`. Read loosely, a session's own name would answer a field whose whole purpose is refusing it |
| Not one verdict cell in this repository is spelled the way `CLOSED_WORDS` and `FIX_WORDS` are, so both refusals that read one had never fired | `skills/code-review/scripts/chain_check.py:881` | **Executed**, by counting the cells and then by mutation. All fourteen closed verdicts across `specs/1788184145-…/rounds/round-{1,2,3}.md` read `**fixed**`, ten of them with a commit after the word; zero read the bare `fixed` the sets hold. So `closed_with_a_fix` answered False on every record that exists, and `open_blocking` read a 🔴 closed as `**fixed** \`sha\`` as still open. Reverting the normalizer to its lowercase-and-strip form turns three new cases red | 2026-09-01 `46b66d9` | The cut is AT the citation rather than a search for a fix word inside the cell. The other direction is pinned too: `answered — the finding it confirms was **fixed** in \`sha\`` must stay out of `FIX_WORDS`, and a substring reader turns that case red. Round 1's 🔴 1 |
| A round number being higher is not evidence that the round read the fixes | `skills/code-review/scripts/chain_check.py:972` | **Executed**: two records committed together carry one `Target SHA`, and round 1 naming round 2 exited 0 before this. Now the same fixture fails, and so does a checker whose `Target SHA` is an ancestor of this record's | 2026-09-01 `46b66d9` | Only positively established inversions are refused — the same commit, or the checker's tree an ancestor of this one's — because a squash discards the commits a round reviewed and *cannot be compared* is the ordinary state of a merged record. Round 1's 🟡 5 |
| A refusal that would go red on merged history nobody can repair is one people learn to skip, so `Pass` beside `nobody` is grandfathered | `skills/code-review/scripts/chain_check.py:286`, `skills/code-review/scripts/chain_check.py:1189` | **Executed**: a work item whose directory name begins with a second at or after the cutoff fails on `Pass` beside `nobody`; one before it prints and exits 0, and `specs/1788184145-…/rounds/round-3.md` is that case in this repository. Inverting the comparison turns five cases red in both directions at once | 2026-09-01 `46b66d9` | Q1's answer, and the option is the repository owner's rather than either the row's or the reviewer's. One constant serves every repository, because a fresh install creates every work item after it |
| The answer a run ends on had no field, in either the reviewer's report format or the record | `agents/warden.md:66`, `templates/sdd-round.md:16` | **Read**: `agents/warden.md` told the reviewer to say plainly whether it opened anything needing a fix, and neither the Report section nor the record template had anywhere for that answer to go | 2026-09-01 `46b66d9` | The `Needs a fix` row now carries it, copied from the reviewer's line rather than re-derived from the verdict table — a 🟡 answered with grounds is a finding that needs no fix. No check reads the row; enforcing it is Q4's neighbour. Round 1's 🟡 10, and `agents/warden.md` refuses this shape in its own words: *a question with no field to sit in becomes a seal taken over an axis nobody decided* |

## Evidence drift

| Clause | Code grounds | Verified behavior | Checked | Notes |
|---|---|---|---|---|
| A row reads DRIFTED when its range was touched since the row's own baseline | `skills/evidence-check/scripts/evidence_check.py:202` | Read, not run | 2026-08-31 `9829412` | Every row here shares the baseline, so nothing can drift until the second commit |
