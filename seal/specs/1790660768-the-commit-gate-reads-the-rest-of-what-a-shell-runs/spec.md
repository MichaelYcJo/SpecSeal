# Feature Specification: the commit gate reads the rest of what a shell runs (#674)

<!-- seal/specs/<unix-epoch-seconds>-<slug>/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| The spawn prompt's invariant, carried from work item `1790644505` | No command shape may read silent where the release branch's gate judges it. The base here is `86256492`, which is `origin/release/v0.16.0` with #671 merged. The local `release/v0.16.0` ref in this clone still points at `551c7967`, so every comparison names the SHA and never the branch. Stricter is the only permitted direction. Where the reader cannot be certain, it stops |
| `CLAUDE.md` §*The goal a design is chosen against* | Between two readings that catch the same commit, the one that stops a command committing nothing is the more expensive. That is why this frame reads by position and not by the presence of a word (§*How the controls stay unasked*) |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | The build owes a test seen red, a failure direction, a prompt budget and platform honesty. §*What a change to a gate must carry* below states them, so the pull request inherits them |
| `docs/commit-review-gate-spec.md` §*commit-review-gate*, the #670 paragraph (*A commit behind a wrapper, in a shell string or in a substitution is a commit*) | It says "a command word the shell would expand in the string a host runs (`sh -c "$CMD"`) counts as one that might commit", and that a body nested too deep "reads as one that might commit". The first sentence is false for every shape in §*The class, enumerated* marked *silent at base*. The second is true, but it answers only after about 330 rescans |
| `skills/agent-contract/SKILL.md` §12 | The finding names an instance and the fix is owed to the class. Round 2 of `1790644505` fixed the three `watch` placements its report listed, and round 3 found six more. This frame enumerates positions and redirection forms from the grammar, not from a report |
| `skills/agent-contract/SKILL.md` §13 | Today a deep nesting is answered by the interpreter's recursion limit. The depth bound makes the answer independent of it, and the case pins that |
| `skills/agent-contract/SKILL.md` §15 | Every new row is seen red at `86256492` before it is planted |
| `hooks/cmdline.py` module docstring, and the comment in `_heredoc_split` ("Two models of one question have to answer it the same way") | The gate and the worktree guard share one reading of a command word. A change to `command_word`, `_git_options` or `understood` reaches both, so this frame states what the guard sees (§*What the worktree guard sees*) and does not build a second reader for the gate alone. **Corrected 2026-09-30** by #689 (work item 1790745049): the guard no longer shares this reading. It reads through `hooks/cmdline_base.py`, the reader frozen at `86256492`, so none of this work item's changes reach it, and §*What the worktree guard sees* describes the guard before #689 |

## What the tree says, read before this frame

Everything in this section is **read**. The framer executed nothing. Each
*silent at base* claim is a reading of the code at `86256492`, and phase 1 or
the phase that owns the shape runs it red before building on it.

### Round 3's findings, opened

Round 3 of `1790644505` (`seal/specs/1790644505-…/rounds/round-3-report.md`)
reported four things. Each was opened at its coordinate:

- **🟡 1.** `hooks/cmdline.py#_is_the_program` returns False at the first
  token that is not an assignment, a list opener, `!`, `(` or a runner. A
  redirection, a `case` word, a pattern, a function definition and `coproc`
  are each such a token.
- **🟡 2.** In `hooks/cmdline.py#command_strings`, the shells' branch takes
  the first word after the flag that does not start with `-` or `+`. A
  redirection such as `2>/dev/null` is such a word. The `watch` branch joins
  its words with the redirection left in.
- **The deferred `2>&1`.** `split_segments_with_separators` runs `shlex` with
  `punctuation_chars=";|&"`. Every redirection operator holding `&` or `|` is
  therefore cut into a separator. That covers `>&2`, `2>&1`, `&>f`, `&>>f`,
  `<&0`, `>&-` and `>|f`.
- **⬜ 3.** `hooks/commit-review-gate.py#_hides_a_commit` recurses once per
  nesting level, and each level runs `drop_comments`, `drop_heredoc_bodies`,
  `split_segments`, `heredoc_bodies` and `substitution_bodies` over the whole
  remaining body. The only bound is the `except RecursionError`.

The report's paste-ready fixes are a starting point, not the design. Four
places where they fall short are in §*The class, enumerated*:

- They read no redirection in front of `git` or `eval`.
- Their `REDIRECTION` pattern does not fullmatch a spaced `<<`.
- Their `watch` filter drops a bare operator but keeps its spaced target.
- They leave the `su`, `runuser`, `script` and `env -S` branches as they are.

### What the class holds beyond the report

Reading the positions from the grammar, rather than from the report, found
these. Each is **read** and silent at base:

1. **A commit behind a leading redirection:** `2>/dev/null git commit -m x`.
   `command_word` stops at the first word it does not know, so it returns the
   segment from `2>/dev/null` on. `parse_git` then takes
   `os.path.basename("2>/dev/null")`, which is `null`, not `git`. This is the
   instance round 3 found for `watch`, one reader over and one level worse: it
   is a plain commit.
2. **A redirection between `git` and its subcommand:** `git 2>/dev/null commit
   -m x`. `_git_options` stops at the first word that does not start with
   `-`, so the subcommand reads as `2>/dev/null`.
3. **`eval` behind a leading redirection:** `2>/dev/null eval "$X"`.
   `_eval_argument` finds its word through `command_word`, which stops at the
   redirection.
4. **A `cd` behind a leading redirection:** `2>/dev/null cd W && git commit
   -m x`. `_cd_target` does not see a `cd`, and `understood` answers True
   because `2>/dev/null` holds no `EXPANDS` character. The walk says nothing
   moved. From a declared session directory with `W` opted in and undeclared,
   the commit is judged against the session alone and reads silent, while bash
   commits in `W`. `understood` already refuses a `cd` behind a prefix
   (`return at == 0`, "Behind a prefix it is the pair above, and
   unreadable"). A redirection is one more thing in front of it.
5. **A host or `watch` glued to a subshell opener:** `(sh -c 'git commit -m
   x')` and `(watch -g "$CMD")`. `strip_subshell` takes the `(` off for
   `command_word`, but `reparsed_texts` and `command_strings` compare
   `os.path.basename(tok)` on the raw token, which is `(sh`.
6. **The string's own command word, behind the same positions.**
   `names_an_unknown_command` asks `command_word(toks)[0]`. So `sh -c
   '2>/dev/null $CMD'`, `sh -c 'f() { $CMD; }; f'` and `sh -c 'case a in a)
   $CMD;; esac'` read as nothing expanding.
7. **The other string pickers take a redirection for the string.** The `su`,
   `runuser` and `script` branch of `command_strings` appends `rest[j + 1]`.
   The `env -S` branch of `reparsed_texts` does the same. So `su -c
   2>/dev/null "$CMD" root` and `env -S 2>/dev/null "$CMD"` read as silent.
8. **Hosts among `RUNNERS` that hand an operand to a shell and are not in
   `STRING_HOSTS`:** `sudo -s` and `sudo -i` with a command, `flock … -c`, and
   `parallel`. `sudo -s 'git commit -m x'` reads silent at base: `sudo` is a
   runner, the stand-in finds no token equal to `git` (the whole string is one
   token), and `sudo` is not a string host. What each program does with its
   operand comes from its manual, **nobody's finding** here, and phase 3
   confirms it from `man`.

## The decisions this frame makes

### 1. Every changed unit keeps the base's answer and adds to it

This is the property that makes the invariant hold by construction, and every
phase is built to it:

- A reader that found something at base, a `git`, an `eval`, a program, a
  string, returns that same answer.
- The new reading is asked only where the base found nothing, and what it
  finds is added.
- A boolean reader is ORed with its base answer (`_is_the_program`,
  `names_an_unknown_command`, `_hides_a_commit`).
- `understood` is ANDed with its base answer, because False is its stopping
  direction.

A reviewer can check each unit for this shape in the diff. The differential
corpus in phase 6 measures it across the class.

This rule also covers an edge the report's fix did not see. A redirection
whose target's basename is `git` (`2>/x/git commit`) reads at base as a git
invocation. Reading past every redirection would read it as none. Keeping the
base's answer where it found one keeps that stop.

### 2. One position reader, three consumers

Where a program word can stand is one question. It is asked by the reader of
`git` and `eval` (`command_word`, `_git_options`), by the test for `watch` as
the program (`_is_the_program`), and by the reader of the string's own command
word (`names_an_unknown_command`). They share one reading of redirections and
headers. The two rules that differ by consumer are stated in §*The class,
enumerated*:

- the stand-in inside compound headers;
- what follows a runner's own options.

### 3. The split operators are rejoined as a view, and the splitter stays

`split_segments_with_separators` is not changed. A merged view glues an
operator back together wherever the split cut it:

- the segment before ends in a bare operator (`>`, `<`, `2>`, `{fd}>`) and
  the separator is `&` or `|`;
- or the separator is `&` and the segment after begins with `>` (`&>`,
  `&>>`).

A chain folds into one segment. The gate's readers read the view **beside**
the original segments, and it **adds only what neither part found on its
own**. So `git commit -m x 2>&1 | tail -1` finds its commit in the first part,
exactly as at base, and the view adds nothing. `2>&1 git commit -m x` finds
nothing in either part and one commit in the view. An addition takes the
directory of the part that holds the command word or the host.

### 4. A depth bound, named and pinned

`NESTING_READ = 32` in `hooks/commit-review-gate.py`. `_hides_a_commit`
returns True for a body read deeper than that, and the `except
RecursionError` stays as the backstop. The value is the one round 3 measured
(1.8 s and 3.3 s for 4000 and 6000 nested `<(`, against 30.8 s and 31.4 s at
its HEAD). It is far above any nesting this repository's commands reach: the
commit-message form `"$(cat <<'EOF' … EOF)"` is two levels. Returning True
at the bound only adds stops. Phase 5 measures the time before and after.

## The class, enumerated

Four readers ask where a program word stands:

- **git**: `parse_git` through `command_word` and `_git_options`, which
  decides whether a commit is found.
- **eval**: `_eval_argument`.
- **watch**: `_is_the_program`, whether `watch` is the program whose words
  run through `sh -c`.
- **word**: `names_an_unknown_command`, the string's own command word, asked
  whether it expands.

A host word (`sh`…`ash`, `su`, `runuser`, `script`, `env`) is found anywhere
in its segment at base, so position matters for it only in P10.

| # | Position | Example | git | eval | watch | word |
|---|---|---|---|---|---|---|
| P1 | segment start, after assignments | `X=1 watch -g "$CMD"` | reached | reached | reached | reached |
| P2 | after `!`, `time`, `time -p`, a list opener (`do then else elif if while until {`), a separate `(` | `if true; then watch -g "$CMD"; fi` | reached | reached | reached | reached |
| P3 | directly after a runner | `nice watch -g "$CMD"` | reached | reached | reached | reached |
| P4 | behind a runner's own options or operands | `nice -n 5 watch -g "$CMD"` | stand-in (base) | stand-in (base) | any later word (base) | **base: missed. After: stand-in, a later word that expands** |
| P5 | behind a redirection, target glued or spaced: `<f` `>f` `>>f` `<>f` `2>f` `2> f` `<<<w` `<<EOF` `<< EOF` `<<-EOF` `{fd}>f`, zsh `>!f` `>>!f` | `2>/dev/null git commit -m x` | **base: missed. After: reached** | **missed → reached** | **missed → reached** | **missed → reached** |
| P6 | behind a redirection the splitter cut: `>&2` `2>&1` `&>f` `&>>f` `<&0` `>&-` `>\|f` | `2>&1 watch -g "$CMD"` | **missed → reached, merged view** | **missed → reached** | **missed → reached** | **missed → reached** |
| P7 | a `case` arm: `case W in P)`, a later arm `P)`, `(P)`, `P\|Q)` (split at `\|`), `P )` | `case a in a) watch -g "$CMD";; esac` | stand-in (base) | stand-in (base) | **missed → positional** | **missed → positional** |
| P8 | a function body: `f()`, `f ()`, `f(){`, `function f`, `function f()`, `function f ()`, then `{` or `(` | `f() { watch -g "$CMD"; }; f` | stand-in (base) | stand-in (base) | **missed → positional** | **missed → positional** |
| P9 | a coprocess: `coproc CMD`, `coproc NAME {`, `coproc {` | `coproc watch -g "$CMD"` | stand-in (base) | stand-in (base) | **missed → positional** | **missed → positional** |
| P10 | a word glued to `(` | `(sh -c 'git commit -m x')`, `(watch -g "$CMD")` | reached (`strip_subshell`) | reached | **missed → reached** | host **missed → reached** |
| P11 | a line continuation | `watch \` at a line's end, `-g "$CMD"` on the next | reached (the splitter joins the lines) | reached | reached | reached |
| P12 | inside a substitution, a heredoc body, a shell string, an `eval` argument | `echo $(2>/dev/null git commit -m x)` | P1–P11 by recursion, and the merged view applies inside too | | | |
| P13 | not a program position: the `for` and `select` word list, `case`'s word, `in`, `[[ … ]]`, `(( … ))`, any argument of another program | `grep -n watch *.py`, `for f in "$@"` | never | never | never | never |

The walk's reading of `cd` is its own row, because it decides where rather
than whether:

| # | Position | Base | After |
|---|---|---|---|
| W1 | a `cd`, a relocator (`pushd`, `source`, `eval`…), a reserved word or an expanding word behind a leading redirection: `2>/dev/null cd W` | `understood` is True and the walk does not move | `understood` is False, so the directory is `Unresolved(CONSTRUCT)`. This is the rule `understood` already applies to a `cd` behind a prefix |

The string, once its host is found:

| Host | How the string is picked | Base | After |
|---|---|---|---|
| `sh`…`ash` with a `c` cluster | the first operand after the flag, past options, `VALUED` values and `--` | a redirection after the flag is taken for the string | a redirection after the flag (glued, spaced, merged) is asked **and** read past, so the base's word is still asked. A spaced target is skipped with its operator |
| `su`, `runuser`, `script` with `-c` or `--command` | the word after the flag | a redirection there is taken for the string | the same rule as the shells |
| `env -S`, `--split-string` | the word after the flag | a redirection there is taken for the string | the same rule |
| `watch` where it is the program | its non-option words, joined | a redirection in the join | the join as at base, **and** the join without redirections, with a spaced target dropped alongside its operator |
| `sudo -s` / `sudo -i` with a command; `flock … -c` / `--command` | not a host at base | none | a host. The string rule is the shells'. The value-taking options are taken from `man sudo` and `man flock` |
| `parallel` | not a host at base | none | every non-option word is read **for a commit** (`reparsed_texts`), which costs nothing without a commit written out. Its expansion question is out (§*Scope*) |

**Two stand-ins, and why they differ by consumer.** Inside a compound header
the base reads the first `git` or `eval` word as the command word (E11 in
`seal/ledger/1790644505-….md`). That costs little, because a false stand-in
needs the literal word. For `watch` and for the string's command word, a
false stand-in needs only a word that expands somewhere after it, and
`grep -n watch *.py` in a function body is exactly that. So both read the
header by position: the pattern closed by `)`, the definition up to its `{`
or `(`, and `coproc`'s optional NAME. The stand-in is used only where a
header's spelling cannot be placed, which is the stopping direction.

Behind a runner's own options, P4, the reader cannot tell an option's value
from the program. `sh -c 'nice -n 5 $CMD'` reads as nothing expanding at
base. Under "where the reader cannot be certain, it stops", a later word that
expands counts there. This is the rule the base already applies to `watch`
behind a runner, and to `git` there through the stand-in.

## How the controls stay unasked

Round 1 of `1790644505` planted seven controls in
`tests/test_a_commit_behind_a_wrapper_or_in_a_substitution_is_judged.py#CONTROLS`.
They are positional parameters no shell runs, and `watch` as a searched-for
word. Round 2's smith narrowed the report's fence for their sake. This frame
keeps them unasked in attended sessions three ways:

1. **Position, never presence.** Every addition is a position a program word
   occupies. A word something else was handed stays P13. `grep -n watch *.py`
   in a function body, a case arm, a coprocess, behind a redirection or
   before `2>&1` stays a search word.
2. **The stand-in only where the position cannot be placed.** A header
   spelling the reader does not know falls to the stand-in. The spellings in
   P7–P9 are read by position.
3. **The controls are planted in the new positions.** Each round-1 control is
   rewritten into P5, P6, P7, P8, P9 and P10, and after `2>&1` at its end.
   Each is silent in a declared repository after the change, as at base.

What does become a stop on a command that commits nothing is named here, so
the prompt budget below is a count and not a hope:

- **(a)** A header spelling the positional reading cannot place, holding
  `watch` or a shell string, with an expanding word after it.
- **(b)** P4 inside a shell string: `sh -c 'timeout 5 wc -l "$1"' _ f`.
- **(c)** A nesting of `NESTING_READ` levels or more with no commit in it.
- **(d)** W1 into a declared repository: `2>/dev/null cd W && git commit`
  where both are declared. It is a stop where base was silent. It is correct
  wherever `W` is undeclared.
- **(e)** A `sudo -s`, `sudo -i` or `flock -c` string whose command word
  expands.

`questions.md` Q2 counts (a)–(e) over this repository's recorded commands.

## Scope

**In:**

1. **The position reader, and redirections before the program**, in
   `hooks/cmdline.py`:
   - one recognizer for every redirection form in P5 and P6;
   - `command_word` reads past leading redirections, for `git`, `eval` and the
     string's command word;
   - `_git_options` reads past a redirection before the subcommand;
   - `understood` refuses W1;
   - `_is_the_program` reads past redirections and a glued `(`;
   - host words glued to `(` are recognized (P10).

   Each unit follows decision 1.
2. **Compound headers**, P7–P9, for `watch` and for the string's command word,
   by position, with the stand-in as the fallback. **P4 inside a string**:
   the stand-in, a later word that expands.
3. **Strings past redirections**, in all four pickers, and the hosts
   `sudo -s`/`-i` and `flock -c`, and `parallel` for a commit only.
4. **The merged view**, in `commit_invocations`, `_reads_a_commit` and
   `names_an_unknown_command`, adding only what neither part found.
5. **The depth bound**, `NESTING_READ = 32`, with the time measured at
   `86256492` and after.
6. **Proof and records.** A differential corpus, the prompt budget, the
   policy paragraph, the ledger fragment, rows drifted by these edits re-read
   in their own files, and the changelog fragment.

**Out, each with its reason and who answers it:**

- **The splitter itself.** Treating `>&`, `&>` and `>|` as words in
  `split_segments_with_separators` moves every segmentation in both gates and
  in the walk. `cd W 2>&1 && git commit -m x` would then be judged in `W` alone
  where the base also judged the session directory, and a declared `W` reads
  silent where the base stopped. That breaks the invariant. The merged view
  gets the reading without the move (`plan.md` Alternatives B).
- **A command word that expands at the top level**: `"$CMD"`, `"$SHELL" -c
  …`, `nohup "$CMD"`. Read: no reader asks it at base, and the #670 paragraph
  scopes the expansion question to "the string a host runs". Reading it would
  stop every line that forwards `"$@"`. That is a new rule with its own
  prompt cost, not the rest of #670's class. The orchestrator decides whether
  to file it.
- **`parallel`'s expansion question.** Its option grammar has many options
  that take a value, and a template ends at `:::` or `::::`. Placing its
  command word is a parser, the refusal `phases/phase-5.md` of `1790644505`
  made for runner options. The commit reading is in. The orchestrator decides
  whether to file the rest.
- **A timeout in `hooks/hooks.json`.** A harness that kills a hook produces no
  output, and no output is silence, the fail-open direction. The bound
  shortens the answer, and a kill would discard it. `questions.md` Q1 asks
  what the harness does today.
- **Everything `1790644505`'s overview leaves under *Not done*.** Script and
  remote runners, the two other hooks' `WRAPPERS` copies, and the guard's
  reading of strings and substitutions. Nothing here changes them.
- **Narrowing anything the base stops.** The base's P4 stand-in for `watch`
  (`timeout 5 grep watch "$f"` stops at base) stays. Removing it would read
  silent where the base judges, however benign the command.

## What the worktree guard sees

**Corrected 2026-09-30** by #689 (work item 1790745049): this section describes
the guard as this work item built it. Since #689 the guard and the consent
writer read through `hooks/cmdline_base.py`, the reader frozen at `86256492`,
so none of the bullets below holds for them any more; the commit gate keeps
every reading this frame asks for.

`command_word`, `_git_options` and `understood` are shared. So:

- **The guard now classifies a git behind a redirection**
  (`2>/dev/null git switch x`, `git 2>/dev/null worktree add …`). At base it
  was silent there. With consent, a token holding `>` still fails the allow
  test in `hooks/worktree-guard.py` (`ELSEWHERE`), so the answer stays with
  the user's own settings.
- **The consent writer records such a creation once it ran**, after the guard
  asked. That is the flow a plain creation already has.
- **W1's `Unresolved`** reaches the guard's switch judgment and the consent
  writer as the session's own directory. `hooks/worktree-guard.py` maps an
  `Unresolved` to `cwd`, and so does `hooks/worktree_consent.py`'s creation
  walk. The walk adds it BESIDE the directory the base's walk gave, so
  neither loses that directory. **Corrected 2026-09-29**, round 1's 🔴 1: this
  bullet said the `Unresolved` WAS the base's directory, so neither moves. At
  `befe53cd` it replaced that directory, and it is the session's own only
  where no `cd` came before it. The guard went silent on four switches the
  base asked about (`2>/dev/null cd .; cd w && git switch -c nb`), and
  `creation_directory` filed a creation in a nested clone under the
  session's clone.

A guard case that pins a redirected git as unread moves group, as
`1790644505`'s phase 5 moved `nice git`. `docs/worktree-guard-spec.md` says
so if it names such a word.

## User scenarios & acceptance *(mandatory)*

"Stops" means `deny`, then `ask` on a re-issue, in an attended session, and
`deny` under the `automation` press. "Silent" means no output. Every row is
seen red at `86256492` unless it is marked a control, and a control passes
there.

| # | Scenario | Given / When / Then | Verifiable how |
|---|---|---|---|
| S1 | P5 for each reader | From an opted-in undeclared repository: `2>/dev/null git commit -m x`, `2> /dev/null git commit -m x`, `<<<x git commit -m x`, `git 2>/dev/null commit -m x`, `2>/dev/null eval "$X"`, `2>/dev/null watch -g "$CMD"`, `sh -c '2>/dev/null $CMD'` → stops. `2>/dev/null git commit -m x` in a **declared** repository → silent, as a plain commit there is | Through `main()`, planted in `tests/test_a_commit_behind_a_wrapper_or_in_a_substitution_is_judged.py`, red at `86256492` |
| S2 | W1 | From a declared session directory, `W` opted in and undeclared: `2>/dev/null cd W && git commit -m x` → stops. At base it is silent | Through `main()`, a row in `tests/test_no_shape_the_base_stops_reads_silent.py`'s neighbourhood, red at `86256492` |
| S3 | P7–P9 | Round 3's six `watch` shapes, plus `sh -c 'f() { $CMD; }; f'` and `sh -c 'case a in a) $CMD;; esac'` → stop | `STILL_HANDED` rows, red at `86256492` |
| S4 | Strings past redirections | Round 3's five shapes, plus `watch -g 2> /dev/null "$CMD"`, `su -c 2>/dev/null "$CMD" root`, `runuser -c 2>/dev/null "$CMD" u`, `env -S 2>/dev/null "$CMD"` → stop | `STILL_HANDED`, red at `86256492` |
| S5 | P10 and the new hosts | `(sh -c 'git commit -m x')`, `(watch -g "$CMD")`, `sudo -s 'git commit -m x'`, `sudo -i "$CMD"`, `flock /tmp/l -c "$CMD"`, `parallel ::: 'git commit -m x'` → stop | `HANDED` or `STILL_HANDED`, red at `86256492` |
| S6 | P6, the merged view | `sh -c 2>&1 "$CMD"`, `sh -c &>/dev/null "$CMD"`, `bash -c >\|/tmp/f "$CMD"`, `>&2 watch -g "$CMD"`, `2>&1 git commit -m x` and `git 2>&1 commit -m x` from an undeclared repository → stop. Control: `git commit -m x 2>&1 \| tail -1` in a declared repository → silent, and `commit_invocations` returns exactly the invocations it returns at base | Rows red at `86256492`. The control is an invocation-list equality case |
| S7 | The invariant | (a) `tests/test_no_shape_the_base_stops_reads_silent.py` passes before and after. (b) A generated corpus, positions P1–P13 × redirection forms × readers × {commit, `"$CMD"`, nothing}, has no row silent at head where `86256492` stops | (a) a case. (b) executed once by phase 6, with the counts in its phase record; the generator is a probe and is deleted (contract §7) |
| S8 | The controls | Round 1's seven `CONTROLS`, and each rewritten into P5–P10 and followed by `2>&1` → silent in a declared repository, and `test_the_controls_read_no_hidden_commit` holds for all of them | `CONTROLS` rows. Each passes at `86256492` and after, and each is seen red by a mutant that reads `watch` or the string by presence |
| S9 | The depth bound | A commit beside 4000 and 6000 nested `<(`, `$(` and backticks → deny. `_reads_a_commit` runs at most `NESTING_READ + 1` times on each. With the recursion limit lowered below what the bound needs, the answer is still deny | The call count is a case, red at `86256492` (about 330 calls). The time is measured before and after and recorded, not asserted. The lowered limit is run once in a subprocess and recorded (§13) |
| S10 | The policy says what the code does | The #670 paragraph of `docs/commit-review-gate-spec.md` names the positions, the redirection rule, the merged view, the hosts and the bound. Its `Enforced by:` line names the new cases | Read at review. The rider and survivor checks pass |

## Data & interfaces

- **No payload field** is new. The gate reads `tool_input.command` and `cwd`
  as before.
- **New names in `hooks/cmdline.py`:** the redirection recognizer and the
  merged view. The positional header reading may be its own unit or live
  inside the position reader. The phase names them. The existing units keep
  their signatures, so the guard's imports do not change.
- **New name in `hooks/commit-review-gate.py`:** `NESTING_READ`.
- **Ledger rows these edits drift**, to be re-read in their own files:
  - in `seal/ledger/1790644505-the-commit-gate-stops-asking-about-commits-that-are-not-there.md`,
    E10, E11, E13, E14, E15, E18 and E19, which cite `command_word`,
    `parse_git`, `reparsed_texts`, `names_an_unknown_command`,
    `command_strings`, `commit_invocations` and `_hides_a_commit`;
  - in `seal/ledger.md` §*Edits that reach the commit gate*, the rows citing
    `_hides_a_commit@a0ff25af` and `commit_invocations@9eb0b156`.

  `evidence-check` names the full list, and `questions.md` Q5 is that run.

## What a change to a gate must carry

- **Failure direction: it blocks more, never allows more.** Decision 1 makes
  every changed unit a superset of its base answer. A wrong read costs a stop
  on a command that commits nothing. A missed read is a real commit nobody
  judged, and bash lands it: round 3 ran four of these shapes and each one
  committed.
- **Prompt budget.**
  - *Attended session:* a stop is one refusal, then a prompt per re-issue, as
    at base. The new stops on commands that commit nothing are (a)–(e) in
    §*How the controls stay unasked*, and Q2 counts them over the recorded
    commands.
  - *`automation` session:* the same shapes are refusals the model handles,
    and no person is asked (`1790644505`, E1).
  - The depth bound adds none a person would write.
- **Why nothing cheaper reaches the same guarantee.** Leaving the shapes
  unread is a real commit nobody judged. The stand-in everywhere is cheaper to
  build and puts search words in front of a person, the cost round 1 of
  `1790644505` ruled a defect. Changing the splitter breaks the invariant
  (§*Scope*, Out).
- **An outage is excluded.** Every added stop needs a program, a string or a
  redirection at a position a shell runs. `git -C <absolute path> commit` in
  a command of its own has none of them.
- **Platform honesty.** This is string reading, with no process inspection.
  bash 3.2.57 on macOS is what round 3 ran. `{fd}>` is bash 4.1 and later,
  and `>!` is zsh, so both are read without being run here. Windows is CI's
  `windows-latest` leg.

## Open questions → questions.md

No row needs a person. `questions.md` lists the judgments the ticket left
open that the tree answered, then two measurements and four rows for the
work.

Framed 2026-09-29 by framer, before the build.
