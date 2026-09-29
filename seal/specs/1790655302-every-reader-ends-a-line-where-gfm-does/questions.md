# every reader ends a line where GFM does — questions for the planner

<!-- seal/specs/1790655302-every-reader-ends-a-line-where-gfm-does/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

**No row below needs a person.** The ticket left several judgments open, and
the tree answered each of them. They are listed here so nobody reopens them.
Each one names its grounds so a reviewer can overturn it by opening the same
place.

## Decided from the tree

| # | Judgment | Grounds | What overturning it changes |
|---|---|---|---|
| D1 | The one `gfm_lines` lives in `skills/verify/scripts/unverified_check.py`, the shared reader | `fold_check.py#gfm_lines`' docstring: "the one reader every script shares is where a single copy belongs". Every in-scope script already loads the reader by path, and `.github/scripts/` loading `skills/` is established (`rider_check.py#load_checker`) | `plan.md` §*Alternatives considered* rows B–D |
| D2 | `evidence_check.py#gfm_lines` stays, as the vendored copy for a checker run alone | The comment above `evidence_check.py#VENDORED_FENCE_RE`: `evidence-ci` puts the checker alone in a user's `tools/` | Removing it breaks `evidence-ci` in every repository that vendored the checker |
| D3 | Readers of one text move in one commit: `readable` with `round_record`'s `raw` halves; `folded_items` with `fold_check`'s `#markers`, `#marker_digest` and `#numbered_statements`; `gather_changelog.py#live_markers` with `survivor_check.py#gathered_fragments` | C's `phases/phase-5.md` table recorded the first two as coupled. `gather_changelog.py#live_markers`' docstring states the third. `round_record.py#swallowed`'s `strict=True` zip raises if only one half moves (spec M5) | Plan row F |
| D4 | `fold_check.py#gfm_lines` is retired, and `fold_check` asks the reader | D1. `fold_check.py#load` already refuses a copy taken alone with exit 2 | `fold_check` keeps a second copy and S17 holds it |
| D5 | The `split("\n")` readers stay: `fold_ledger.py`, `settle.py#coordinates`, `unverified_check.py#todo_open_rows`, `survivor_check.py#released_lines` and `#python_prose` | They split newline-translated text at LF, which is where GFM ends a line. `fold_ledger.py#demote`'s docstring requires the byte-for-byte round trip that `gfm_lines` would break | Plan row G |
| D6 | `claude_block.py#read_lines` splits at LF alone with ends kept, not with `gfm_lines` | Its module docstring: the region is cut the way `install.sh`'s `awk` cuts it, and `awk`'s record separator is LF. The two rules differ only on a lone CR | A lone CR in `CLAUDE.md` would end a line for the script and not for the installer |
| D7 | The worktree guard's two transcript tails split at LF | JSON Lines ends a record at LF, and JSON permits a raw U+2028 in a string. Every other transcript reader here iterates the file, which splits at LF (`worktree_consent.py`, `payload_meter.py#_rows`, `session_cost.py`) | Phase 4 is dropped, and the two sites are listed in the class case as out |
| D8 | The readers #664 did not name are in scope: phase 3's extras, phase 4, and the class case in phase 5 | `routing.md` §*Why this way* says this release fixes the class rather than filing it. Agent contract §12 is "enumerate the class". C's phase 5 recorded these as "members by the same cause" | A person may strike phases 3–5 without touching phases 1 and 2. Each struck reader then goes into the class case as out, with "deferred" and a home |
| D9 | `git` output whose lines carry file content (`round_record.py#measure`'s diff and `#call_sites`' `git grep -n`) is in the class. `git` output of paths, refs and subjects is not | Git numbers those content lines at LF. A split at a form feed drops the `+` or `path:line:` prefix from the second half | Those two sites move to "out" |
| D10 | A case holds the class closed. It lists every `.splitlines(` by enclosing unit, and exempts F's files by path | Memory and routing both favour a mechanism over a written rule. The last three work items each rediscovered members of this class by hand | The class is held by this frame's table alone |
| D11 | C's `rounds/round-1.md` is left holding the line break its copy wrote (spec M2) | `skills/implement/SKILL.md` §6: "The records themselves stay". A round record asserts a past state | — |
| D12 | `rider_check.py#inferred_anchor`, and the `config.md` readers in `broad_gate.py` and `seal.py`, are F's | The spawn's instruction and `routing.md`. F's PR rewrites the `broad_gate.py` and `seal.py` functions against its own reader (spec M7) | — |
| D13 | `reader_blanking_passes` is taught by name that `gfm_lines` is the splitter, not a pass | Its own docstring says `text.splitlines()` "drops out" because it is an attribute call. The pin exists to catch an added pass, so it stays and gains an exception instead of being dodged | — |

## Rows still open

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | Has work item F (#672) squashed into `release/v0.16.0` by the time phase 5 starts? | the work. The tree can only answer this at phase 5, not when the frame was drawn | **Landed:** S17 adds `hooks/blocks.py#gfm_lines`, and this build still leaves `rider_check.py#inferred_anchor` alone. **Not landed:** S17 goes without it, and whichever of F and G lands second adds it | In either case, `overview.md` §*Not done* records that `rider_check.py#inferred_anchor` should slice `checker.gfm_lines(text)` once F lands. Its answerer is the milestone 49 orchestrator, the session that spawned this frame | ✅ Not landed, answered by the work at phase 5: `origin/release/v0.16.0` was still `2e392d46` and PR #672 open. S17 goes without `hooks/blocks.py#gfm_lines`, and `overview.md` §*Not done* names both follow-ups for whichever of F and G lands second |
| Q2 | Does any moved reader's output change on this tree (S20)? | a measurement: each phase runs its readers over this tree at `2e392d46` and at the phase's commit, and compares the bytes | **No change:** as expected from spec M1. **A change:** the phase names it in `plan.md` §*Operational impact* before it closes | No change, apart from `readable`'s indices inside the fenced blocks of M1's report | ✅ No change, measured by the work: over every tracked file the two splits differ in M1's report alone, and `fold-check`, `chain-check`, `gather_changelog.py --check`, `survivor-check`, `correction-check`, `claude_block.py --check` and `payload_meter.py --sections` printed the same bytes at `2e392d46` and after phase 5. `unverified-check` printed this item's own overview in addition, which is not a moved reading (`phases/phase-5.md`) |
| Q3 | Can S15, the `claude_block.py` case, be made red at `2e392d46`? | the work: phase 3 finds out when it writes the case | **Red:** it is a defect fix with a pinned case. **Not red:** the move is for agreement with `awk` only. The phase says so and does not claim a defect, and the case pins the agreement | Red is expected (read, `claude_block.py#write` and `#bare`). `splitlines(keepends=True)` cuts a template line after a mid-line U+2028. `bare` strips only CR and LF, and `write` then appends the target's ending to each piece, so the written copy gains a line break the template does not have | ✅ Red, answered by the work in phase 3: at `2e392d46` `--write` wrote the template line as two lines. The move is a defect fix, pinned by `test_the_claude_md_block_is_cut_where_awk_cuts_it` (`phases/phase-3.md`) |

**`Who can answer` takes one of three values and nothing else.**

- **a person** — what the product should be, or a value somebody has to be
  accountable for. This is the file's stated purpose, and the only kind of row
  that blocks the build.
- **a measurement** — a probe, a command or a count settles it, so asking a
  person is the wrong instrument.
- **the work** — unknowable at framing time. The phase that meets it decides
  it there and records a divergence row.

**The framer opens rows and does not own their answers.** The `Status` column
is ticked by whoever answered, never by whoever asked.

Answered rows feed back into docs/ (policy clause or open-questions section)
before this directory's work merges.
