# reading is charged to a `read` family — questions for the planner

<!-- seal/specs/1790562541-reading-is-charged-to-a-read-family/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

**No open row needs a person, and none blocks the build.** Q1 is the one
question a person had to answer, and the owner answered it before the first
edit. Every other row has a default the build proceeds on.

**Judgments #642 left open that the tree answered.** They are listed here so
nobody reopens them. The grounds are in `spec.md` §*Decided from the tree*
and `plan.md`'s Alternatives table.

- A call is `read` only when every command word is a read word or a neutral
  word and at least one is a read word. One read word somewhere on the line
  is not enough (a pipe into `tail` behind a deploy), and neither is a read
  word as the first command after `cd` (`ls && rm -rf x`).
- The read words are #642's thirteen. The `FAMILIES` comment states the
  admission criterion for the next one.
- A write is never `read`: an output redirection except to `/dev/null`,
  `sed -i`, `sort -o`, `find`'s actions and `awk -i`. Ambiguity falls to
  `other`.
- A heredoc or here-string, a substitution, or a line the tokeniser refuses
  is not `read`. There is no fallback pattern.
- `read` is judged after the four existing families, so they keep every
  call they have today, the anywhere-match mirror included.
- `read` stays out of the repeats figures, and the `other`-leads note keeps
  its wording.
- #635's four deferred findings are in scope, and are phase 1.
- The name is `read`, the owner's.
- #640 as filed grades tools per turn and reads no family, so nothing here
  forecloses it.

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | Does a `python3 -` heredoc script get a family of its own beside `read` (#642, *What would fix it*, option 2: "The owner decides")? | a person | **a `read` family only**: heredocs stay in `other`, and `read` does not move when agents switch between `Edit` and shell edits · **both**: a heredoc row counts a vehicle rather than a kind of work, it moves with that switch, and it confounds 0.17.0's #640, which grades batching per segment kind | — | ✅ answered 2026-09-28 by the repository owner, in the pre-edit batch: **a `read` family only; no `python3 -` heredoc family.** Recorded in `routing.md` §*Why this way*. The spec's In §3 makes it mechanical: any `<<` on the line keeps it out of `read` |
| Q2 | How many calls, and how many seconds, move from `other` to `read` over the corpus, and what share of Bash calls does `other` hold after? | a measurement | the tree cannot answer it: the frame runs no code, and #642's 8,328 was taken at 2037cf0, before #377, under the looser *first after `cd`* rule, so it is an upper bound twice over. One probe answers it (`plan.md` phase 3) | the spec promises no figure. The ticket's *toward about 40%* is not an acceptance criterion | ✅ answered 2026-09-28 by phase 3's probe: 7,819 calls and 5,221 s move from `other` to `read` over 374 transcripts and 24,223 Bash calls, and `other` holds 24.7% of the Bash calls after, 57.0% before (`phases/phase-3.md`) |
| Q3 | Which command words most often keep an otherwise-read line in `other`, and which substitutions or heredocs do? | a measurement | the tree cannot answer it for the same reason. The answer is the candidate list for a later widening under the admission criterion (`cut`, `tr`, `jq` are the likely ones; `uniq` needs its output operand handled). The same probe prints it | the list stays #642's thirteen in this item. The counts go into `phases/phase-3.md` and the changelog entry, for whoever plans the widening | ✅ answered 2026-09-28 by phase 3's probe: `cut` 777 lines, `python3` 578, `evidence-check` 429, `python` 184, `survivor-check` 179, then `tr` 66, `rm` 64, `sleep` 58 and `uniq` 54; a heredoc or here-string keeps 2,502 lines out and a substitution or backtick 630 (`phases/phase-3.md`). Whether to widen the list is the owner's, from these numbers |
| Q4 | Which grammar and builtin words does the walk actually yield in command position beside a read word, beyond the neutral set the spec names? | the work | reading `command_words` answers the grammar words it yields (`for`, `done`, `fi`, `esac`, `}`) but not which ones the corpus writes. Phase 2 meets the rest while building, and phase 3's probe can list any word that blocks more than a handful of lines | the spec's neutral set. A word added to it is recorded as a divergence in `phases/phase-2.md`, with the reason it neither touches nor writes a file | ✅ answered 2026-09-28 by the build: no word was added, and `case` and `esac` were taken out, because a `case` arm's commands are never in command position (`phases/phase-2.md`). Among the 25 words that most often keep an otherwise-read line in `other`, the one builtin is `command` (16 lines), which runs the word after it and is a wrapper, so it stays out as `timeout` does; no grammar word is among them (`phases/phase-3.md`) |
| Q5 | Which ledger rows does the edit drift? | the work | the spec counts the expected set at 1fa25931, but item A lands between framing and building and re-stamps some of the same rows. Only `evidence-check` at the rebased tip answers it | re-read every row `evidence-check` names. A row outside the expected set is explained in `phases/phase-3.md` | ✅ answered 2026-09-28 by `evidence-check` at the tip: 26 rows over nine ledger files, each re-read and re-stamped, three corrected in place (`phases/phase-3.md`) |
| Q6 | The `read` family prints beside the `Read` tool's own row in the `by family` block and in `--json`'s `by_family` (round 1's ❓, executed on a real transcript: `read 29 calls` and `Read 1 calls`). Keep the name `read`? | a person | **keep `read`**: the owner's name, and the tool row is capitalised, so the two keys differ · **rename** (`reading`, `read-only`): no two rows differ only by case, and every sentence naming the family changes with it | `read` | ✅ answered 2026-09-28 by the orchestrating session, on the owner's pre-edit batch answer, *a `read` family only*, which names the family `read`; the tool row is capitalised. No change. The owner may overturn it, and a rename is a change to the family's name in the code, `SKILL.md`, the changelog fragment and this item's ledger rows |
