# the one script an agent is told to run cannot be typed — questions for the planner

<!-- seal/specs/1789338080-the-one-script-an-agent-is-told-to-run-cannot-be-typed/questions.md
— decisions only a human can make, extracted so nothing ships on a silent
assumption. Before adding a row, check the inheritance rule: if policy is
silent but existing behavior answers it, inherit and record — only genuinely
NEW rules belong here. -->

The routing batch was answered before the first edit and is committed in
`routing.md`: review through the review chain, the pull request opens, the
framer plans and `smith` builds. None of the four axes is re-asked here.

**Two rows reach a person and neither blocks the build.** One is settled by a
three-second probe at the top of phase 2, and one by the phase that meets it.
Sorting them this way is what keeps the batch answerable in one sitting — a
person's time is the wrong instrument for a question a command answers.

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | Should phase 3's pin bind the repository generally — *every* shipped script a shipped document names must be reachable from that document — or should it assert only today's nine documents and this one script? | **a person** — the repository owner. `CONTRIBUTING.md` §*Proposing a new gate or skill* makes a new always-on rule the owner's call, and this one binds every document written from now on, not only the ones this branch fixes | **General** (the plan's choice) — the pin enumerates `skills/*/scripts/*.py` and every `.md` under `agents/`, `skills/`, `templates/`, so the tenth document and the thirteenth script are caught the way `bin/` was not. It costs a rule the repository is bound by, and its cheapest wrong repair is deleting a mention rather than adding a locator. **Targeted** — the pin names `round_record.py` and asserts its nine documents. Cheaper to reason about, and it closes exactly the instances that exist today; the next script to arrive without a wrapper is then a gap somebody notices while writing something up, which is the state `bin/` itself was in before work item `1788302682` | **General** — answered by the repository owner on 2026-09-14, in the same batch as Q2, confirming the default. `skills/agent-contract/SKILL.md` §12 asks for the class rather than the coordinate, and the targeted form cannot see the instance the ticket itself missed. **Either answer leaves the nine documents fixed** — this decides the pin's reach, not the sweep's | ✅ |
| Q2 | Should `round-record` get a row in the README cheat sheet, in both editions? | **a person** — the repository owner. There is no written rule for what the cheat sheet holds, and the owner is who decides what a reader outside an agent is shown | **Out** (the plan's choice) — the cheat sheet lists five of the eleven wrappers, and `broad-gate`, `survivor-check`, `seal-stamp` and `arm-check` are all absent; those five are commands a person runs against their own repository without an agent, which `round-record` is not. **In** — two rows, one per edition, and the command a review orchestrator types becomes discoverable without opening a skill. Work item `1789296300`'s own `questions.md` recorded the opposite lean for `--segments`, on the grounds that the READMEs are where a person outside an agent learns a command exists, so this is a live convention rather than a settled one | **Out** — answered by the repository owner on 2026-09-14, in the same batch as Q1, confirming the default. Neither README names `round_record.py` today, so the rule that both editions move together is not reached, and adding the rows is additive whenever the owner wants them | ✅ |
| Q3 | Is `round-record` free as a bare-word command — does anything already on a normal PATH, or anywhere in the plugin, answer to that name? | **a measurement** — `command -v round-record` and a search of `bin/` and the plugin manifest, at the top of phase 2, about three seconds | A collision would mean the wrapper resolves to something else on some machine, which is the same class of failure as not shipping it. The probe reports what answers, on this machine and in the tree. `ls bin/ \| grep round` is already **executed** and returns nothing, exit 1, so the in-tree half is settled; the PATH half is not | The name is free and `round-record` ships as planned. It is the name the script's own `--help` already prints, so a collision would be an argument for renaming something else | ⬜ |
| Q4 | Where in each of the nine documents does the locator go, and does any of them need more than one? | **the work** — the phase 3 edit of each file decides it there and records a divergence row if the plan's single-sentence assumption does not hold | The property phase 3 has to reach is that the document names the command or the path at least once. Whether that is a clause on the first mention, a sentence beside it, or a line in a table is a per-document judgment, and four of the nine are under `tests/test_docs_line_wrap.py` at 88 columns, which constrains the wording rather than the placement | One reachable form per document, attached to or beside its first mention. It does not travel back to the framer | ⬜ |

## Decided here rather than asked, with what each was chosen over

All three are argued in full in `spec.md` and `plan.md`. They are listed so a
reader of this file alone does not take silence for an open question.

- **#318's two fixes are both taken, because they repair different halves.**
  The wrapper repairs the two places a command is typed; the locator repairs
  the thirty-four places a reader goes looking. Three of the four segments in
  the incident were `warden`, which is never told to run the script at all —
  so the wrapper alone would not have reached them. `plan.md` §*Alternatives
  considered* holds both rejections.
- **`chain_check.py` is classified rather than wrapped.** It is named 23 times
  in shipped documents and never as a command — **executed**, `grep -rn
  'chain_check\.py -' --include='*.md' agents/ skills/ templates/` returns
  nothing — and all three places that invoke it carry its full path. Wrapping
  it would change `templates/config.md`'s user-facing broad-gate row for a
  defect that does not exist. The pin asserts the property the classification
  rests on, so it degrades to red rather than standing as a note.
- **`docs/` is out of the sweep.** It stays home under
  `tests/test_the_release_check_watches_what_ships.py`'s own classification,
  no agent's startup payload contains it, and its readers hold the clone.

## Assumptions taken, because a different answer would not change the build

- **The command is spelled `round-record`.** The script's `--help` already
  prints `usage: round-record`, and every sibling wrapper is the script's name
  with underscores turned to hyphens. This is an observation, not a choice.
- **The documents show the bare command, not `bin/round-record`.**
  `survivor-check` and `broad-gate` are both spelled bare where a document
  shows a command, and the incident was in an installed repository, where
  `bin/` is on the Bash tool's PATH. A session working inside a clone of this
  repository with the plugin disabled reaches the script by the path the same
  sweep is adding.
- **The `.cmd` twin ships with LF endings**, because `.gitattributes` is
  `* text=auto eol=lf` and the existing eleven twins ship that way. Nothing new
  is being decided.
- **The wrapper carries no version guard of its own.** `round_record.py`
  refuses at entry with a sentence naming the floor (#226), and no sibling
  wrapper guards anything.
- **The locator names the repo-relative path**, `skills/code-review/scripts/round_record.py`,
  where a path rather than the command is the reachable form chosen for a
  document. A path relative to the document would differ per file for no gain.

Answered rows feed back into `docs/` (policy clause or open-questions section)
before this directory's work merges.
