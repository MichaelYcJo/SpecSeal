# Feature Specification: the worktree guard allows a listed shape and asks the rest

<!-- seal/specs/1791270162-the-worktree-guard-allows-a-listed-shape-and-asks-the-rest/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate.
Issue #826, for release 0.20.0. Framed by `specseal:framer` on Fable 5.1. -->

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `docs/worktree-guard-spec.md` §*Premise* | What the guard protects: concurrent work in one folder, where a switch lands another session's next edits on an unintended branch. So *leaves the tree where it is* means **HEAD names the same branch, or stays detached where it was, when the command ends**. Content moved on the same branch (`reset`, `stash`, `rebase`, `merge`, `pull`) is not the guard's subject and never was |
| `docs/worktree-guard-spec.md` §*A. Branch switch* | The five rows and their verdicts stay word for word. What changes is WHICH command reaches them: today a predicted switch, after this work a `git switch` or an unrecognised shape in a tree where the row would matter |
| `docs/worktree-guard-spec.md` §*B. Worktree creation*, §*Creation consent*, §*Decided before git runs (#692)* | Out of this work's scope and unchanged: a creation is read by the frozen reading and judged before git runs, with consent read first (owner's answer P6 of work item 1790815613) |
| `docs/worktree-guard-spec.md` §*Which tree, when the command walks to it* | Which segments are git, each `-C`, where every `cd` lands: the frozen reading of `hooks/cmdline_base.py` stays (owner's answer P4 of 1790815613, pinned by `tests/test_the_frozen_reading_never_grows.py`). The two rules read *past* the base (#764/#738's option reading, #790's lookups) and candidate C (#678, #737, #745) are what this work removes |
| `docs/worktree-guard-spec.md` §*Unknowns resolve conservatively* | The direction: a wrong deny costs a prompt, a wrong allow breaks another session's tree, and a deny on EVERY invocation is an outage. The clean single-stream silence (In 2 below) is what keeps an allow-list from being that outage |
| `docs/commit-review-gate-spec.md` §*Why a deny, and why only once* | Under the person's `automation` press a stop is a **deny to the model** whose reason names the ways on, and puts no question to anybody. The new stop (In 3) takes this shape, through the same reader, `hooks/worktree_consent.py#automation_answered` |
| `hooks/tokens.py#is_plain`, `PLAIN_GIT` | The construction the ticket points at: a positive list, each entry carrying the count it was measured at over the recorded runs, and everything unrecognised judged rather than passed |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | A test seen red, a stated failure direction, a prompt budget in the pull request body, platform honesty |
| `CLAUDE.md` §*The goal a design is chosen against* | Between two designs that catch the same defect, the one that stops to ask a person is the more expensive. This decides Alternatives B and C in `plan.md` |
| `docs/the-evidence-ledger.md` §*A released row is read again in the branch's fragment* | Every released row citing a symbol this work removes gets a `Corrected ·` row in `seal/ledger/1791270162-….md`; no released file changes |
| `seal/specs/1790815613-…/questions.md` P4, P6 and M1 | No git refuses a switch before the tree moves (M1, four gits), so the switch arm predicts from the command's text, permanently, through the frozen reading (P4). This work keeps that reading and changes what is asked OF it |

## Scope

### The question turned around

Today the switch arm answers *does this command switch a branch?* from the
command's text, and 0.18.x grew four readings on that question (#733's
candidate C, #745, #788's reopened `classify`, #803's `_refs`/`_fetched_as`)
without the findings converging: eight missed spellings, five ordering
findings, four DWIM predictions, three policy sentences that could not list
the asked set (issue #826). After this work the arm answers *is this command
positively known to leave the tree where it is?* and treats everything else
as a possible switch, in the one place a switch would matter.

### In

1. **Three shapes, read by the frozen reading's words alone.** Every segment
   `walk_command` yields whose `cmdline_base.parse_git` reads it as git is one
   of:
   - **listed** — the subcommand is in `LEAVES_THE_TREE` (the allow-list,
     In 5), or it is `checkout` or `restore` carrying a `--` with at least one
     word after it (a restore by construction: `git checkout -- README.md`,
     `git checkout feature/x -- README.md`, `git restore -- .`); `restore`
     without a `--` is listed too, since `git restore` never moves HEAD.
     `worktree` and `stash` are listed only where the first word bash hands
     git after them is not `add` or `branch`, so a redirection in front of,
     glued to or cut away from that word hides nothing (*inferred during
     implementation*, phase 3: `git worktree 2>/dev/null add ../wt b` was
     listed at `9c03ae85`). `rebase` is listed only where it has fewer than
     two words that are not options, and none beside `--root`: `git rebase
     <upstream> <branch>` switches to `<branch>` before it rebases
     (*inferred during implementation*, round 1 of the review, red 3). A
     lone `-` and every word after a `--` count as words, since git reads
     each as a revision: `git rebase - <branch>` switches too (*inferred
     during implementation*, round 2, red 1);
   - **a switch** — the subcommand is `switch`, whatever its words;
   - **a creation** — `cmdline.adds_a_worktree(tokens)`, judged by §B as
     today and untouched here;
   - **unrecognised** — any other git: `checkout` without `-- <word>` (a
     branch, a path without `--`, `-b`, `--detach`, a name git could guess,
     a message search, every form #790 and #764 enumerated), and every
     subcommand not on the list.

   And a segment the frozen reading does NOT read as git is unrecognised
   where it hands a string to a shell that holds the bare word `git`
   (`sh -c '…'`, `bash -c`, `zsh -c`, `eval "…"`, `env -S '…'`, the class
   #732 names), where the whole
   command could not be tokenized and its text holds the bare word `git`, or
   where a word of it is `git` behind a redirection or a zsh precommand word
   (`2>/dev/null git switch x`, `noglob git switch x`, `git 2>&1 worktree
   add …`), which is the whole class candidate C read. A non-git program
   that runs git from inside itself (`python3 -c "…"`, `make`, a script)
   is not read, as it never was.

   **A substitution body is read through these same shapes, recursively**
   (the owner's answer P2 (a), 2026-10-06; fed back during phase 2, and it
   replaces the clause that made any body holding the bare word `git`
   unrecognised). The body of every `$( … )`, backtick pair and `<( … )` in
   the command, whether the segment around it is git or not, is read as a
   command: a body of listed git is listed and says nothing, and a body
   holding a switch, a creation, a `checkout` without `-- <word>`, an
   unlisted subcommand or any other unrecognised shape stops with that
   shape's own plain spelling, run outside the substitution. A body nested
   deeper than the commit gate reads (32 levels) stops as one it could not
   finish. A body belongs to no one segment, so it is judged in the
   session's own tree, the fallback #686 gives a directory the walk cannot
   place.

2. **The tree decides whether anything is asked.** A listed shape is silent
   in every tree state and spawns no git. A switch takes the §A ladder as
   today, in the tree its segment names. An unrecognised shape is judged
   only where **the tree matters** for the tree its segment names: another
   session is ACTIVE or IDLE there, detection is unusable, or tracked changes
   are present (§A rows 1–4). Where the tree is single-stream and clean (§A
   row 5) the guard says nothing about it, which is what row 5 says of a
   switch today and what the base said of every shape. A command holding
   both a switch and an unrecognised shape is judged by the ladder for the
   switch, with the unrecognised stop taken first where the tree matters,
   since a stop there stops the whole line. That stop is a `deny`, because
   approving an `ask` would run the switch past the ladder, and every tree on
   the line is read before the stop is taken, so a shape in a tree another
   session is ACTIVE in makes it a `deny` too (*inferred during
   implementation*, round 1 of the review, red 1). The stop's reason names
   each tree on the line that matters and why, or the ACTIVE ones where
   there are any, since approving runs the line in all of them (*inferred
   during implementation*, round 2, yellow 4).

3. **The stop for an unrecognised shape, and its two readers.** Where the
   tree matters, the guard stops BEFORE the ladder, with one reason text
   that names the shape it read and the plain spelling that it reads:
   `git switch <branch>` or `git switch --detach <rev>` for a switch,
   `git checkout -- <path>` or `git restore <path>` for a restore,
   `git worktree add …` for a creation, the un-strung command for a string
   handed to a shell, and `git -C <dir>` for another tree. An unlisted
   subcommand is its own plain spelling, and the text names running it with
   `git -C <scratch clone>` or after the other session ends (the owner's
   answer P3 (a)); an untokenizable command's text names splitting it and
   writing a commit message with `git commit -F <file>` (P4 (a)); a
   redirection read as the subcommand (`git 2>/dev/null status`) is moved
   to the end. Those three were fed back during phase 2. Where the
   session's person pressed `automation` on the routing question, read by
   `hooks/worktree_consent.py#automation_answered` on the session's own
   clone exactly as `hooks/commit-review-gate.py#automation_pressed` reads
   it, the stop is a **`deny`**: the model gets the turn, rewrites in the
   plain spelling, and the retry meets today's rows (a `git switch` in a
   dirty tree still asks the person about the changes; in an ACTIVE tree it
   is still denied and steered to a worktree). Without the press the stop is
   an **`ask`** with the same text, which is what #678's question is today,
   except in a tree another session is ACTIVE in, where it is a `deny`
   either way: `docs/worktree-guard-spec.md` §A row 1 denies a branch-form
   `checkout` there with nobody asked, and an `ask` would let one approval
   take the branch out from under that session (*inferred during
   implementation*, phase 2; `questions.md` P5 puts it to the owner). On
   the `ask` path a creation on the same line is judged first, as `choose`
   judges it, because approving an ask runs every segment of the line.
   The consent *record* (`specseal-worktree-consent/<session>`) is not the
   press and is never read for this stop: a creation having run says nothing
   about whether anybody is at the keyboard.

4. **The readings go.** Removed from `hooks/worktree-guard.py`: candidate C
   (`wider_only_kinds`, `_bare_words`,
   `ask_what_only_the_wider_reading_finds`); `switch_kind`; the option table
   and its reader (`SWITCH_OPTIONS`, `_Options`, `_long_option`, · NAME NOT IN TREE
   `read_switch_words`, `handed_words`, `_redirection_width`,
   `_REDIRECTION`); `classify`'s name lookups and guesses (`is_ref`,
   `_verified`, `_commit_named`, `_object_named`, `_one_merge_base`,
   `_OBJECT_NAME`, `tracked_in_any_remote`, `_refs`, `_fetched_as`, · NAME NOT IN TREE
   `_the_bases_lookup`, `_no_guess`, `base_only`), with `classify` itself
   reduced to the three shapes of In 1 or replaced by a function that names
   them. `main`'s walk keeps the first switch and the first creation in
   either order (#620) and gains every unrecognised shape, each judged in
   the tree its own segment names, first one first, each tree looked up
   once; a git only the wider reading reads is judged in the tree its own
   `-C` names (*inferred during implementation*, phase 3: In 2 speaks of
   each shape, and the first-only reading was silent on a hidden switch in a
   dirty second tree, which candidate C had asked about). A git an `&` cut
   is one command, judged in the tree its own `-C` names from where its first
   part runs, and with the reader broken in the tree the part before the cut
   names (*inferred during implementation*, round 2 of the review, red 2 and
   yellow 3: both were placed by the last part, which carries no `-C`).
   `hooks/cmdline_base.py`, `hooks/cmdline.py`, `hooks/worktree_consent.py`'s
   writer and `walk_command` are untouched; the §B ladder, `choose`, the
   tokens, `sessions_in_tree`, `tracked_changes` and every reason text of §A
   are untouched.

5. **The list is measured, not guessed.** `LEAVES_THE_TREE` holds every git
   subcommand the recorded runs hold (In 7's corpus) whose plain invocation
   leaves HEAD's branch where it was, each with its count in a comment, the
   way `hooks/tokens.py#PLAIN_GIT` carries its counts. A subcommand the
   corpus never recorded is not on the list (the ticket's convergence
   argument: a list grows by a measured row and never by a reading), unless
   `questions.md` P1 is answered (b). Which recorded subcommands leave the
   branch is read off `git help <sub>` for each, and the judgment is written
   beside the list: `rebase`, `merge`, `pull`, `cherry-pick`, `revert`,
   `reset`, `stash` (not `stash branch`), `restore`, `rm`, `mv`, `clean`,
   `fetch`, `push`, `branch`, `tag`, `worktree` other than `add`, and every
   read-only subcommand leave it; `switch`, `checkout`, `bisect`,
   `symbolic-ref`, `update-ref`, `stash branch`, `worktree add` and a
   `rebase` naming a branch do not (the last *inferred during
   implementation*, round 1 of the review, red 3, where git 2.50.1 left HEAD
   on the named branch).
   A `rebase` detaches HEAD while it runs and comes back; that window is a
   known limit, named.

6. **Tests, policy and records follow the code.**
   - New cases, each seen red first: the three shapes over the five tree
     states and both readers of In 3 (a sampled product, bounded in seconds,
     never the full cross product the 165 s case walked); the string-handed
     class; the segment's tree; the press read and the record not read;
     no git spawned for a listed shape.
   - Cases whose subject is removed are retired with the subject:
     `test_no_twin_is_asked_unless_an_operator_cuts_the_segment` (164.9 s
     on macOS, #841), `test_nothing_the_base_read_as_a_switch_goes_quiet`
     (24.9 s), `test_no_constructed_switch_is_silent`, the `KINDS`,
     `WIDER_ONLY`, `CREATIONS`/`SWITCHES`/`TWINS`/`DASHED` generators and
     every case over them, the `MOVES`/`GUESSED`/`REFUSED` tables and their
     `a_history` fixture, `test_the_option_table_binds_the_installed_git`,
     `test_every_shape_the_wider_reading_asks_is_one_the_policy_rule_covers`, · NAME NOT IN TREE
     and the policy pins on #745's rule sentence. Cases about the ladder,
     the tree the walk names, the tokens, the creation arm and consent stay
     and stay green (`test_the_guard_is_never_silent_where_the_writer_records`
     included).
   - `docs/worktree-guard-spec.md`: §A gains the shape as what reaches its
     rows and the stop of In 3 with its two readers and its failure
     direction; §*Which tree* loses the two rules read past the base and
     candidate C's paragraphs, keeping the frozen-reading paragraphs and the
     #686 fallback; §*Known limits* loses the option-table, lookup and
     guess bullets and gains three: the clean single-stream silence on a
     hidden creation, the `rebase` window, and Windows, where every tree
     state reads *detection unusable* so every unrecognised shape stops.
     Every `Enforced by:` line names a case that exists.
   - `seal/ledger/1791270162-….md`: one row per acceptance scenario below,
     and a `Corrected ·` row for each released row whose grounds cite a
     removed symbol — grep count, executed 2026-10-06 by the framer:
     `switch_kind` 7 citations in 4 files, `_bare_words` 6 in 3, `classify`
     4 in 2, `wider_only_kinds` 3 in 2, `ask_what_only_the_wider_reading_finds`
     2, `tracked_in_any_remote` 2, `_commit_named` 2, `handed_words` 2, and
     one each for `_refs`, `_fetched_as`, `is_ref`, `_object_named`,
     `_one_merge_base`, `read_switch_words`, `SWITCH_OPTIONS`; D1 of
     `seal/releases/0.18.2.md` §1791119071 cites the 165 s case by name and
     is owed its `Corrected ·` row by the retirement (#841's second comment).
   - `seal/specs/1791270162-…/changelog.md`: one `### Changed` entry a
     reader of the release notes can act on, naming #732 and #734 as closed
     by this change and the numbers of In 7.

7. **Measure before building, and the measurement shared with #841.** Phase
   1 of `plan.md` replays the recorded command and directory pairs through
   the shapes of In 1, tree-blind (a transcript records no tree, so the
   count is an upper bound on stops, as every count since 1790993140's phase
   3 has been), over two cuts: cut 1, Bash tool uses timestamped before
   `2026-10-03T11:06:22+09:00` (25,741 pairs on disk at 0.18.2, 27,351 when
   D1 of 1790993140 fixed it, read at `v0.18.0:seal/specs/1790993140-…/
   phases/phase-3.md`), and cut 2, every use recorded to the build day
   (36,199 at 1791163981's phase 1). The project directories read are every
   `~/.claude/projects/*SpecSeal*/` on the maintainer's machine, each named
   with its transcript count, because the main transcripts of this
   repository's own directory fell from 34 to 23 between 2026-10-03 and
   today (`ls` count, executed by the framer) and the earlier counts may not
   be reproducible.

   **What is shared with #841, and who owns it.** #841 owns the suite's
   wall-time measurement (`bin/test -q --durations=40`, executed by its
   orchestrator on 2026-10-06: 456 s wall, the 164.9 s case) and the
   sampling of the slow guard cases that keeps their properties; this work
   reads those numbers from #841's body and does **not** re-run
   `--durations` at the base. This work owns the corpus stop count, which
   #841 does not take. The 165 s case is #841's to sample and this work's
   to retire: its subject (`switch_kind`, candidate C) leaves the tree in
   phase 3, so **#841's change lands first and this work's phase 3 rebases
   over it**, deleting the sampled case rather than the original, and the
   `Corrected ·` row for D1 of 0.18.2 is written here once, by this work.
   Phase 3 reports the `--durations` of the module it rewrote, after, as a
   delta #841's record can carry; it reports nothing about the rest of the
   suite.

### Out

- **The creation arm.** §B, `guard_worktree_creation`, `judge_creation`,
  consent, the record, the Agent/Task path: unchanged (P6). A creation only
  a hidden spelling holds (`git 2>&1 worktree add …`) is an unrecognised
  shape: it stops where the tree matters and is silent in a clean
  single-stream tree, which is 0.16.0's standing before #678 and is named in
  §*Known limits*. #734's defect — the consent read against the wrong clone
  for such a creation — no longer exists, because the stop reads no consent
  and the plain retry reads its own clone; the issue is closed by this
  change and says so.
- **The frozen reading and the walk.** `hooks/cmdline_base.py`, its byte
  pin, which segments are git, each `-C`, where a `cd` lands, the #686
  fallback to the session's own tree, the #689 cost of a `cd` behind a
  redirection: unchanged (P4). A switch behind an unresolved `cd` is judged
  in the session's tree as today.
- **The §A rows, their texts, the choice sites, the tokens.** Unchanged. In
  particular the dirty-tree `ask` for a genuine `git switch` stays an ask of
  a person under `automation`, as today: the plain retry of In 3 meets it.
- **Programs that are not a shell and not git.** `python3 -c`, `uv run`,
  `make`, a script file: not read, as never.
- **Content-moving commands on the same branch.** `reset --hard`, `stash`,
  `rebase`, `merge`, `pull`: listed where recorded (In 5). The Premise is
  about which branch the next edit lands on, not about content.
- **Windows.** Every tree state there reads *detection unusable* (§*Known
  limits*), so every unrecognised shape stops there — a `deny` to the model
  under the press, a choice-site `ask` otherwise. Named, not fixed.
- **The durations measurement and the sampling of #841's other slow
  cases** (the heredoc oracle, the sealer's cases, #823's two): #841's.
- **A `rebase`'s detached window.** Named as a limit; not judged.
- **`hooks/cmdline.py`'s readers.** Reused where In 1 needs a shell
  string's words (`command_strings`, `reparsed_texts`,
  `substitution_bodies`); not changed. Where that module fails to load, the
  text test of In 1 (the bare word `git` in a string, body or untokenizable
  command) still stops, so a broken reader costs a stop and never a silence.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 a listed shape is silent everywhere | Given each of the five §A tree states (ACTIVE, IDLE, unusable, dirty, clean) and the session with and without the press; when `git status`, `git diff`, `git add -A`, `git commit -m x`, `git log`, `git rev-parse HEAD`, `git fetch`, `git checkout -- README.md`, `git checkout feature/x -- README.md`, `git restore README.md`, `git -C W status` run, with a redirection at a sampled position and glued or spaced; then the guard says nothing and spawns no git | new case in `tests/test_worktree_guard.py`, a sampled product bounded under 5 s, `subprocess.run` monkeypatched to count calls |
| S2 `git switch` meets today's rows | Given the five states; when `git switch feature/x`, `git switch -c y`, `git switch -`; then verdict and reason are those of today's §A rows, character for character | the existing ladder cases stay green unchanged; one new case diffs the reasons against fixtures taken at the base |
| S3 an unrecognised shape stops where the tree matters | Given ACTIVE, IDLE, unusable and dirty trees, without the press; when `git checkout feature/x`, `git checkout README.md`, `git checkout -b y`, `git checkout --detach HEAD~1`, `git checkout ':/fix'`, `git bisect start`, `git <unlisted>`, `sh -c 'git switch x'`, `bash -c "git checkout x"`, `eval "git switch x"`, `echo $(git switch x)`, `2>/dev/null git switch x`, `noglob git switch x`, `git 2>&1 worktree add ../wt b`, and `git switch x && echo "unclosed` (untokenizable) run; then the guard answers `ask` (`deny` in the ACTIVE tree, In 3, fed back during phase 2), and the reason names the shape and the plain spelling of In 3 | new case; each shape red at `a9d7b0e5` (the base is silent on `git checkout README.md`, `sh -c`, `bisect`, and asks a different question on the hidden gits) |
| S4 the same shapes are silent in a clean single-stream tree | Given a clean tree with no other session and detection reliable; when every S3 shape runs; then the guard says nothing | new case; `git checkout ':/fix'` and `2>/dev/null git switch x` are red at the base, which asks there |
| S5 under the press the stop is a deny to the model | Given a dirty tree and a transcript holding the harness-written `automation` answer from this clone (`tests/test_the_guard_asks_once_per_session.py#write_transcript`); when an S3 shape runs; then the decision is `deny`, the reason names the plain spelling, and nothing in it asks for `AskUserQuestion` | new case; red at the base (which asks) |
| S6 the plain retry meets today's rows | Given S5's tree; when the model retries `git switch feature/x`; then the dirty-tree `ask` of today, and in an ACTIVE tree today's `deny` with the worktree steer | existing cases cover the rows; one new case runs the pair |
| S7 the record is not the press | Given a consent record on disk and no `automation` answer; when an S3 shape runs in a dirty tree; then `ask`, not `deny` | new case; red with the stop reading `worktree_consent.consent` instead of `automation_answered` (mutation) |
| S8 the segment's tree is the one that matters | Given the session's tree clean and a second clone `W` dirty; when `git -C W checkout x` or `cd W && git checkout x` runs; then the stop; and with `W` clean and the session dirty, silence. Given `cd "$W" && git checkout x` with `W` unset, the session's tree decides (#686, unchanged) | new case over `judgeable`'s two directories |
| S9 both kinds on one line | Given a dirty tree; when `git checkout README.md && git switch feature/x` runs; then the unrecognised stop comes first (it stops the whole line) as a `deny` (round 1, red 1); when `git status && git switch feature/x` runs; then today's dirty-tree ask alone | new case |
| S10 the list carries its counts and nothing unmeasured | Given `LEAVES_THE_TREE`; then every entry's comment carries a count from phase 1, every recorded branch-leaving subcommand is present, and `switch`, `checkout`, `bisect`, `symbolic-ref`, `update-ref`, `worktree` are absent | new case reading the module beside phase 1's table, the way `test_the_option_table_binds_the_installed_git` read git's `-h`; and a reader's check of the comment against `phases/phase-1.md` |
| S11 the readings are gone | Given `hooks/worktree-guard.py` after phase 3; then none of In 4's symbols is defined, `grep -c "rev-parse"` in the switch arm is 0, and `tests/test_the_frozen_reading_never_grows.py` is green | `test_a_rider_reaches_its_file.py` and a one-line case asserting the symbols are absent; `ruff` for unused imports |
| S12 the policy says what the code does | Given `docs/worktree-guard-spec.md`; then §A names the three shapes and the two readers of the stop, §*Which tree* holds no option table, no lookup rule and no candidate C, §*Known limits* holds the three new bullets and none of the four removed, every `Enforced by:` resolves | `tests/test_a_folded_statement_names_what_enforces_it.py`, `tests/test_docs_line_wrap.py`, and the existing `test_the_guard_policy_says_*` cases rewritten to the new sentences |
| S13 the records | Given the fragments; then one `Corrected ·` row per released row citing a removed symbol (the counts of In 6), D1 of 0.18.2 §1791119071 among them; `evidence-check` reports no drift and no broken citation | `evidence-check` executed in the sealer's run; `correction-check` |
| S14 the numbers reach the pull request | Given the pull request body; then the prompt budget carries, per cut: pairs holding a git segment, pairs stopped tree-blind by shape, pairs stopped that today's guard does not stop, and the zero person-stops under the press | the body, read by the warden against `phases/phase-1.md` |

## Data & interfaces

- `hooks/worktree-guard.py`: `LEAVES_THE_TREE: frozenset[str]` with a
  counted comment; `shape_of(tokens) -> "listed" | "switch" | "creation" |
  "unrecognised" | None` (None for a segment that is not git and holds no
  string or hidden git with `git` in it; a substitution body is read at the
  command's level, `_command_findings`, where the quoting the segment's
  tokens lost is still there); `tree_matters(top,
  session_id, eff_cwd, seen=None) -> tuple` returning what `main` needs for
  the ladder so `sessions_in_tree` and `tracked_changes` run once;
  `stop_unrecognised(findings, trees, pressed, before_ask=None,
  switch_on_line=False)`, every unrecognised shape on the line listed with
  its own plain spelling, and every tree on the line that matters (`trees`,
  each `(top, state)`) described, or the ACTIVE ones where there are any;
  `switch_on_line` makes it a `deny` (round 1, red 1; `trees` round 2,
  yellow 4, *inferred during implementation*); the
  press read `worktree_consent.automation_
  answered(top_of_session, session_id, transcript_path)` wrapped as the
  commit gate wraps it, every failure False. `main` keeps its two silent
  exits and its ladder.
- No new hook, no new file under `hooks/`, no change to `hooks/hooks.json`,
  `hooks/cmdline_base.py`, `hooks/cmdline.py` or `hooks/worktree_consent.py`.
- Records: `seal/specs/1791270162-…/phases/phase-N.md` per phase from
  `templates/sdd-phase.md`; `seal/ledger/1791270162-….md`;
  `seal/specs/1791270162-…/changelog.md`.
- Failure direction, for the pull request: the change makes the guard
  **stop more** (every unrecognised shape where the tree matters) and
  **allow more** in one place (a hidden creation in a clean single-stream
  tree, where the base allowed it too). The first is the cheaper mistake
  under a deny to the model; the second protects nothing the Premise names.
- Prompt budget, for the pull request: **zero new person-stops under the
  press**, by construction; without the press, one `ask` per unrecognised
  shape in a tree that matters, bounded by phase 1's tree-blind count.

## Open questions → questions.md

`questions.md` holds P1 (the list's seed, a person's), the measurements M1–M4
that phase 1 answers, and W1–W3 for the phases that meet them. Everything the
ticket left open that the tree answered is listed at its head.

Framed 2026-10-06 by framer, before the build.
