# 1791384157-the-hooks-read-the-session-waiver-and-creation-one-way — questions for the planner

<!-- seal/specs/1791384157-the-hooks-read-the-session-waiver-and-creation-one-way/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

**Judgments the tickets left open that the tree answered.** Listed so nobody
reopens them; each has its grounds in `spec.md` In or `plan.md` Alternatives.

- **#856's choice between (a) expanding braces and (b) a known limit.** The
  tree gives a third answer: `docs/worktree-guard-spec.md` §A stops a shape
  the guard does not recognise where the tree matters, and a word bash
  expands before git reads it is one. #856 was filed before the inventory;
  #834 part 8 is why (a) is refused (the family did not converge on
  prediction), and the Premise is why (b) is (both measured commands switch
  HEAD silently in an ACTIVE tree). Decided (c), `spec.md` In 5.
  **Confirmed by the repository owner on 2026-10-08:** (c) — an unquoted
  brace expansion in a git word is an unrecognised shape, and the guard
  stops on it.
- **How far the consolidation goes** (#868's last paragraph). The four facts
  with a measured or traced disagreement, and the copies a change to one of
  them touches (`crg.git`); the listed-for-scope copies stay (`spec.md`
  Out).
- **Whether `hooks/cmdline_base.py` is reopened.** No. The brace rule reads
  the frozen words and the judgment text inside the guard; the placement
  function reads the frozen walk's answer. Nothing below the rider changes.
- **Which placement rule is the one.** The guard's, because it is where bash
  runs the segment on both shapes that disagreed (the framer's probe,
  `spec.md` In 1) and the base's on the three pinned chains.
- **Whether `$CLAUDECODE` stays in the stub.** No; the verdict is unchanged
  in every state (`plan.md` Alternatives), and the name exists in
  `steps_around_hooks` only because the stub read it.
- **Whether `answers.given`'s match by `ps` text is in scope.** No; a named
  limit with no owned input to replace it (`spec.md` Out, measured).

**Judgments the reframe made from the records (2026-10-08, after round 3).**

- **Whether the command-word reading gets a third fix.** No. Three rounds,
  each finding the next shape of what bash builds from a brace, are the
  class `skills/code-review/SKILL.md` §*Verdicts that close too early*
  names and #692 stopped; round 3's paste-ready text is the fourth
  enumeration and is declined (`plan.md` Alternatives). `spec.md` In 5.
- **What a brace anywhere means.** A word holding an unquoted brace
  expansion, in any segment, is the brace shape; nothing about its
  position or its alternatives is read. Decided from §A (an unrecognised
  shape stops where the tree matters) and from the records (every
  narrower rule reopened). `spec.md` In 5, the reframed paragraph.
- **Whether an assignment word is exempt** (round 3's ⬜ 5). No: the
  exemption needs a carve-out for git segments (`git rebase A={main,x}`),
  which is a position read again, and no recorded pair holds one. The
  cost is named in In 5 and counted by M4.
- **Which tree a non-git brace segment is judged in** (round 2's 🟡 2).
  The tree `place` puts it in and every tree a `-C <dir>` word pair in it
  names, the union; a `-C` a brace hides is the named limit the `sh -c`
  bullet already states. `spec.md` In 5, S20.
- **Whether the 34,775 figure is trusted.** Not as the figure for the
  reframed rule, which stops more; phase 7 measures the reframed rule by
  phase 1's method with the self-check first, and that figure, with its
  method, replaces the 34,633 in §A, the changelog and S11b (round 3's
  ⬜ 6).
- **Whether the lease case is the redesign's** (round 3's ⬜ 4). Yes, as
  phase 8, taken as round 3's paste-ready case: the finding is that the
  case cannot be red, and a case that cannot fail is §15's counterfeit.

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| M1 | Does a hook process the harness spawns (`session-lease.py` at PostToolUse, the three git stubs' Python through a Bash child's git) see `CLAUDE_PID` in its environment? Measured in a Bash child it is exported and equals the `claude` ancestor's pid; `ps -E` on the session's own `claude` process showed no `CLAUDE_*` variable, so the hook side is unread — NAME NOT IN TREE | a measurement | **yes**: the lease records an observed pid for every session, extension hosts included, and `from_lease` matches it with no `ps` run. **no**: the lease side keeps the walk and only the git-hook side reads the variable (git inherits the Bash child's environment). Either answer builds the same code, because the walk stays under the variable (§13); the answer decides only which route S5 exercises live | **no** is assumed; phase 1 measures it where it can (a Bash child's `env`, read; a hook's environment, by a lease written after phase 4 compared with the walk's answer on a host whose process is not named `claude`, or left `unverified` with the repository owner named) | ⬜ The Bash-child half answered by phase 1 (executed: exported, and equal to the `claude` ancestor's pid); the hook half stays open, `unverified` in `overview.md` with the repository owner named, because no hook of a session can be made to print its environment without changing the installed configuration |
| M2 | How many recorded (command, cwd) pairs hold a git segment with an unquoted brace expansion, by subcommand — In 5's new stop class, tree-blind? | a measurement | a count. It goes into §A's failure-direction paragraph and the changelog; it changes no code. A count above the pairs the rule exists for (`rebase`, `stash`, `worktree`) says which listed subcommands pay the over-stop | none needed; phase 1 counts it by 1791270162 phase 1's method, with the self-check first | ✅ one: `git add` of a path holding `{plan,questions}`, from a 2026-09-23 transcript, under `add`, which is not one of the three. Phase 1 answered zero of 32,431 pairs after a self-check that found all four S11 forms and none of the three S12 forms (`phases/phase-1.md`); round 4 found the pair its count missed (`phases/phase-7.md`, corrected in round 4) |
| M3 | How many recorded pairs do not split and carry `[no-review]` or `[no-parity]` as a substring — In 3's cost, the commands that waived through `has_marker`'s fallback and will meet the refusal? | a measurement | a count, for the changelog. It changes no code: the refusal names the git-native spelling either way | none needed; phase 1 counts it in the same probe | ✅ six pairs under the framed rule, four of them the guard's comment form with an apostrophe after the token; one pair under the rule phase 5 builds, the words read before the split fails (`phases/phase-1.md`, `overview.md`'s divergence row) |
| W1 | How does S10 make `git diff --name-only --cached` fail in a test: a `git` shim first on `PATH` that exits 128 for `diff` and execs the real git otherwise, or an index git cannot read? | the work | the shim is portable and names the failure; a broken index depends on the git version's message. Either way the case is red at 5623d728 | the shim; phase 5 records which | ✅ the shim, a POSIX script exiting 128 for any `diff`; the cases skip on Windows (`phases/phase-5.md`) |
| W2 | Which cases retire with the guard's `has_token` body and `_without_bodies`, and which are rewritten against `tokens.given` (released row T1's four cases in `tests/test_guard_resolves_the_tree_it_judges.py`, and the `base_marker` helper of `test_one_heredoc_shape_is_data_to_the_commit_gate.py`)? | the work | a case whose subject is the removed splitter retires; one that pins the token rule moves to the one reader. `test_s6_neither_read_honours_a_token_the_base_did_not` keeps its `base_marker`, because it asserts the new read is no wider than the base's, which still holds | phase 5 names each in `phases/phase-5.md` | ✅ none retired; T1's four cases pass unchanged through the one reader, and `test_s6_neither_read_honours_a_token_the_base_did_not` compares against both base reads together, because the one reader reads what `has_marker` read and the strict base `given` did not (`phases/phase-5.md`) |
| P1 | On 2026-10-08 the owner confirmed #856's (c) as *an unquoted brace expansion in a git word is an unrecognised shape*. The reframe widens the word to every word of every segment, so `cat {.gitignore,README.md}`, `ls seal/specs/<id>/{spec,plan}.md` and `for f in x/{a,b}.md` stop where the tree matters (a `deny` the model rewrites under the press; one `ask` otherwise), where the confirmed sentence stopped only a git word. Three rounds showed that any rule narrower than *every word* has to read where the brace stands, and each such reading was found incomplete by the next round. Does the owner take the wide rule and its over-stop, measured at 33 recorded pairs tree-blind by phase 1 and re-counted by phase 7? | a person | **yes**: phases 7–10 as written. **no, keep it to git words and the command word**: the only narrower rules are the three that reopened, so *no* means accepting the round-3 spellings as a known limit, which the Premise refused in (b) — it reopens the frame, not a phase | **yes**; the build ships on it. The tree answers the price (§*Unknowns resolve conservatively*: a wrong deny is one prompt; `CLAUDE.md`'s goal: a stop that asks nobody is cheap), and the row is here because the sentence the owner confirmed is narrower than the one built | ⬜ built on its default, **yes**, in phase 9 under `Automation \| yes` (the orchestrator's direction of 2026-10-08); the over-stop is 42 of 33,287 recorded pairs, 41 a command that is not git and one a git `git add` the confirmed sentence stops too; since round 5 the brace is read off the text with no word boundary, which adds `${a,}`, `echo {a, b}`, a brace group holding a comma and a reflog range across two braces to the price (`phases/phase-7.md`, corrected in rounds 4 and 5). Open for the owner, whose answer it still is |
| M4 | How many recorded (command, cwd) pairs does the reframed rule stop tree-blind — a brace in any word of any segment, outside quotes — split by whether the stopping segment's command word is `git`, with the assignment-word pairs (`A={a,b} cmd`) and the quoted-beside-unquoted pairs counted apart? | a measurement | a count for §A's failure-direction paragraph, the changelog and ledger row S11b; it changes no code. Phase 1's M2 found 0 in git words and 33 outside them, under a narrower reading; this re-counts under the reframed one, over the corpus as it stands, after the self-check on S17's thirteen and S19's quoted forms | none needed; phase 7 counts it by phase 1's method and records the method | ✅ 42 of 33,287 pairs under the rule as round 5 left it, 41 a segment that is not git and one a git segment; seven a brace group judged as the command's, two on an assignment word alone, one a quoted brace beside an unquoted one. Corrected in round 4 (phase 7 gave 31 of 32,498, none git, by a probe that read the judgment text twice) and in round 5 (34 of 32,715 under round 4's reading, after a self-check of 21 and 15 forms the record did not keep). Round 5's self-check stopped all 57 must-stop forms and none of 20 must-not forms, both lists written in `phases/phase-7.md` with the method |
| M5 | Do bash and zsh expand a brace in an assignment word (`A={a,b}`), the ❓ row of round 3 that the permission layer refused? | a measurement | **neither does**: In 5's assignment cost is a stop on a word the shell leaves alone, as written. **zsh does**: the cost sentence says so, and nothing else changes, because the rule reads no position either way | the bash manual's reading (no expansion) is assumed for both; phase 7 runs `bash -c 'A={a,b}; printf %s "$A"'` and the zsh form in a scratch directory and records the output; where zsh is absent, the zsh half is `unverified` in `overview.md` with the repository owner named | ✅ neither does: executed in a scratch directory, bash and zsh each printed `{a,b}`, exit 0 (`phases/phase-7.md`) |
| W3 | How does a finding carry more than one tree for S20's union — one finding per `-C <dir>` tree beside the placed one, with the stop's reason naming the shape once, or a tree list on the finding — and is a glued `-C<dir>` a pair the frozen `parse_git` reads, so the scan reads it too? | the work | both shapes give S20's verdicts; the first reuses `main`'s existing per-finding tree lookup and dedupes in the reason, the second changes `_finding_tree`'s signature. The glued form is read as `parse_git` reads it for a git segment, or not at all, and the phase record says which | one finding per tree, dedupe in the reason; the glued form as `cmdline_base.parse_git` reads it; phase 9 records which in `phases/phase-9.md` | ✅ one finding, several trees (`_finding_trees`), each looked up once and the shape named once; a glued `-C<dir>` is not read, as `cmdline_base.parse_git` does not read it (`phases/phase-9.md`) |
| W4 | Which brace cases keep their names and gain parameters, and which are rewritten: `test_a_brace_in_no_git_word_stays_silent` (its claim inverts), `test_a_brace_that_makes_the_command_word_is_unrecognised` (round 3's thirteen join), `test_a_brace_command_word_is_judged_in_the_tree_its_c_names` (the `S`-dirty direction, the runner forms and the hidden-`-C` limit join), and the `Enforced by:` lines of §A that name them? | the work | a case whose claim inverts is rewritten under a name that says the new claim (S18 proposes one); a case whose claim widens keeps its name. The policy pin fails on a renamed case until the `Enforced by:` line follows | S18's name for the inverted case; the other two keep theirs; phase 9 names each in `phases/phase-9.md` | ✅ the inverted case is `test_a_brace_in_any_word_is_the_brace_shape`; the other two keep their names and gain parameters; two cases are new; §A's `Enforced by:` line follows (`phases/phase-9.md`) |

**`Who can answer` takes one of three values and nothing else.**

- **a person** — what the product should be, or a value somebody has to be
  accountable for. The only kind of row that blocks the build. Before the
  reframe this file held none: #856's choice is decided from policy above,
  with the grounds where a reader can overturn them. Since the reframe it
  holds P1, which widens the sentence the owner confirmed; it carries a
  default the build ships on, under `Automation | yes`.
- **a measurement** — a probe, a command or a count settles it, so asking a
  person is the wrong instrument.
- **the work** — unknowable at framing time. The phase that meets it decides
  it there and records a divergence row; it does not travel back to the
  framer.

**The framer opens rows and does not own their answers.** The `Status`
column is ticked by whoever answered, never by whoever asked.

Answered rows feed back into docs/ (policy clause or open-questions section)
before this directory's work merges.
