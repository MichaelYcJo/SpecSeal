# Post-review check — #763's fix on #739's branch

This is not a numbered review round. It checks one commit, `38cdc0ec..a4d28eda`, which the repository owner took on the branch after round 3 capped the run. The target is `a4d28eda`. The reviewer read `rounds/round-3-report.md`, issue #763, the fix's diff, and the units it touches. It then judged constructed strings only through the gate's own functions: `heredoc_data`, `_quoted_delimiter`, `heredocs`, and `main()` fed a JSON payload in a repository that declares no work item. **No constructed gate string was run in a shell.** Two shell rules were measured on harmless strings that only print text, and `gh` and `ssh` were run with logging stand-ins and the network blocked (see *Executed probes*).

On purpose, this file records no command string that passes the gate. Each finding names the unit, the coordinate, and the shell rule the unit disagrees with.

## What the fix closes, and what it leaves

- **#763's 🔴 1 is closed for every shape it named.** A backslash-newline inside a delimiter word, between the two `<` of an opener, after `<<-`, or before the word now keeps every body on the line read. The gate stops each such line that carries a commit.
- **The same class has two more members that the new rules do not reach (🔴 1, 🔴 2).** The class is *the reader ends a quoted body at a line where the shell does not*. Both members existed in the shared splitter before #739. At the base they cost nothing, because the base read every body. The branch now trusts the reader's boundaries, so the text the shell runs after its real terminator can land inside a second body that the reader calls data. The base stops both shapes. The target is silent on both.
- **#763's 🟡 2 is closed for the programs it named, and one sibling is open (🟡 3).** `gh pr ready` and `gh pr edit` run `ssh` from `PATH` as well as `git`. The over-check adds only `git`.
- #739's three recorded shapes are still data, and the `gh api` narrowing holds. It is also better grounded than the commit says.

## 🔴 1 — a carriage return lets the reader end a body the shell keeps reading

**Unit:** `_heredoc_split`, `hooks/cmdline.py:620`. It is relied on by `heredoc_data` at `hooks/tokens.py:476-477`.

**Shell rule it disagrees with:** bash and zsh compare a heredoc line with the delimiter byte for byte, so a line that is the delimiter followed by a carriage return does not end the body. Measured on a harmless string in both shells: the body ran on past that line to the next exact match.

**What the reader does:** it strips trailing `\r` from each body line before it compares, so it ends the body one or more lines early. The lines between that point and the shell's real terminator are body text to the shell. The reader reads them as command lines, and one of them can be a second quoted `cat` opener. That opener's body then takes in the shell's real terminator and every line after it, until the second delimiter. The shell runs those lines as commands. The reader calls both bodies data, so neither the segment walk nor the body re-reading sees the commit.

**Measured (executed, gate decisions only):** a sink writing a file, one body line made of the first delimiter and a carriage return, then a second quoted `cat` opener, the first delimiter, a commit line, and the second delimiter. `heredoc_data` answered `[True, True]` and `main()` was silent at `a4d28eda` and at `38cdc0ec`. `main()` denied at `e141980a`. The same holds for the `<<-` form with a leading tab, and with no file written at all. A carriage return in the delimiter word itself fails closed, because the reader then finds no terminator.

**Why it matters:** this is the same failure #763's 🔴 1 named: the reader's view of where a body is differs from the shell's, and a body called data covers text the shell runs. The fix's new rules key on a backslash, and this member has none.

## 🔴 2 — a dropped comment turns a body line into a terminator the shell never sees

**Unit:** `heredoc_data`, `hooks/tokens.py:476-477`. It reads `heredocs` over `drop_comments(command)`, and the gate does the same at `hooks/commit-review-gate.py:406`.

**Shell rule it disagrees with:** a heredoc body is not tokenised, so a `#` inside a body line opens no comment, and the line is compared with the delimiter as written.

**What the reader does:** `drop_comments` runs over the whole command, bodies included. A body line whose tail after a blank starts with `#` loses that tail. The blank before it stays. When the quoted delimiter itself ends in a space or a tab, or is only blanks, the cut body line now equals the delimiter. The reader ends the body there, and the same second-opener construction as in 🔴 1 moves the shell's commands into a body the reader calls data.

**Measured (executed, gate decisions only):** three delimiters, one ending in a space, one ending in a tab, and one that is a single space. `heredoc_data` answered `[True, True]` and `main()` was silent at `a4d28eda` for all three. At `e141980a`, `main()` denied the first and asked on the other two. Both shells printed the cut line as body text on a harmless string.

**Why it matters:** this is the same class as 🔴 1, reached through a different unit. Comparing the reader's boundaries on the raw text with its boundaries on the comment-dropped text closes it without touching `drop_comments`, whose callers depend on its current output.

## 🟡 3 — `GH_NOTHING_LOCAL`'s two subcommands run `ssh` from `PATH`, and the over-check adds only `git`

**Units:** `GH_NOTHING_LOCAL` and its comment at `hooks/tokens.py:268-275`, and the program set in `heredoc_data` at `hooks/tokens.py:495-497`. The same claim appears in `docs/commit-review-gate-spec.md:221` and in the *As built* note of `spec.md:64` (R2f).

**What was claimed:** the comment says the two subcommands "provably run nothing local". The fix commit adds `git` to the programs a written file may not be named after, wherever `gh` stands on the line.

**What was measured (executed):** gh 2.100.0 was run in a scratch repository that has an ssh-form remote. Logging stand-ins for `git`, `ssh`, a pager and an editor sat first on an absolute `PATH` entry, the token was a dummy, and the network was blocked through a closed proxy port. `pr ready` with a number, `pr edit` with a flag, and `api` each ran `git remote -v`, `git config --get-regexp` for the resolved remote, and `ssh -G` for the remote's host. Before any network call, `pr ready` with no number also ran `git symbolic-ref`, `git rev-parse` for the push ref, and three more `git config` reads. No pager or editor ran.

**What the gate answers:** a sink writing a file named `ssh` into a directory, with `gh pr ready` after it. `heredoc_data` answered `[True]` and `main()` was silent at `a4d28eda`. The `git`-named variant of the same line stops. `main()` asked at `e141980a`. Go's `PATH` lookup refuses a relative result, so this needs a writable absolute `PATH` directory, the same precondition round 3 recorded for #763's 🟡 2.

**Why it matters:** it is the instance one name away from the one the fix added (§12). The comment's "nothing local" is also false as measured. A later editor who trusts it can remove the `git` addition too.

## ⬜ 4 — `pr edit` counts any dash word as a flag that names what to edit

**Unit:** `_runs_what_it_reaches`, `hooks/tokens.py:436-438`. The comment above `GH_NOTHING_LOCAL` says `pr edit` prompts only when no flag names what to edit. The code accepts any word starting with `-`, which includes `-R`, `--repo` and a bare `--`. None of those names a field, and `gh` opens its interactive editor path there when it can prompt. Measured as gate decisions: both shapes are data. It is ⬜ because the agent's Bash tool gives `gh` no terminal, so `gh` cannot prompt there. A fix would accept only the edit-field flags, or leave `pr edit` out of the data shape.

## The questions the caller asked

1. **#763's 🔴 1 and 🟡 2.** 🔴 1 is closed for its instances. 🟡 2 is closed for `git`, for a `PATH` program the line runs, and for every `gh` subcommand but the two. One sibling is open (🟡 3).
2. **A way past a new rule, of the same class.** Yes, two. The backslash-newline rule does not reach a boundary moved by a carriage return (🔴 1) or by a dropped comment (🔴 2). The over-check does not reach `ssh` (🟡 3). Enumerated by construction: the places the reader and the shell can disagree about a body are (a) whether a `<<` opens one, (b) where the delimiter word ends, (c) whether it is quoted, (d) where the body starts, and (e) which line ends it. (a) to (d) fail closed at the target: through `_commands`' rejection of `$`, backticks, parentheses, braces and backslash-newline, through `_quoted_delimiter`, and through the one-for-one opener check. An empty delimiter fails closed on the opener count. (e) is the open one, through the two units above.
3. **#739's three recorded shapes.** All three are still data. The pull request body and the Python program are silent. The third shape is silent in a declared repository and denied in an undeclared one, without the unplaceable-construct text. This holds at the target and with the candidate fixes applied.
4. **The `gh api` narrowing.** It is acceptable. `gh api` runs `git` and `ssh -G` exactly as the two admitted subcommands do, so the old exemption rested on a false premise. What it costs: a body written to a file and then sent with `gh api --input <file>` now stops. A body piped straight into `gh api --input -` stays data, because no file is written. None of #739's recorded calls used `gh api`.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | The reader strips a trailing carriage return before it compares a body line with the delimiter, and the shell does not. A second quoted opener then hides the lines the shell runs inside a body the branch calls data | `hooks/cmdline.py:620` (`_heredoc_split`), trusted at `hooks/tokens.py:476` (`heredoc_data`) | open | executed: gate decisions silent at `a4d28eda` and `38cdc0ec`, deny at `e141980a`. Shell rule measured in bash and zsh on a harmless string |
| 🔴 2 | `drop_comments` cuts a body line's `#` tail before the split. With a delimiter that ends in a blank, the cut line becomes a terminator the shell never sees, and the same second-opener construction follows | `hooks/tokens.py:476` (`heredoc_data`); the gate's same read at `hooks/commit-review-gate.py:406` | open | executed: three shapes silent at `a4d28eda`; deny or ask at `e141980a`. Shell rule measured in bash and zsh on a harmless string |
| 🟡 3 | `gh pr ready` and `gh pr edit` with a flag run `ssh -G` from `PATH`. The over-check adds `git` and not `ssh`, and the comment's "provably run nothing local" is false | `hooks/tokens.py:268` (`GH_NOTHING_LOCAL`), `hooks/tokens.py:495`; `docs/commit-review-gate-spec.md:221`; `spec.md:64` | open | executed: gh 2.100.0 under logging stand-ins, network blocked. Gate decision silent at the target, ask at the base |
| ⬜ 4 | `pr edit` counts a dash word that names no field (`-R`, `--repo`, `--`) as a flag | `hooks/tokens.py:436` (`_runs_what_it_reaches`) | open | executed as gate decisions; that `gh` prompts there is read from its help, and it needs a terminal the agent's tool does not give |
| 🟢 | #763's blocking finding is closed — a backslash-newline in the word, between the two `<`, after `<<-` or before the word keeps every body read | `hooks/cmdline.py:409` (`_quoted_delimiter`), `hooks/tokens.py:331` (`_commands`) | confirmed | executed: those shapes with a commit ask at the target. The module's quoting cases pass |
| 🟢 | #763's second finding is closed for the programs it named — a write over a program the line runs, `git` where `gh` runs it, and every `gh` subcommand but the two | `hooks/tokens.py:424` (`_runs_what_it_reaches`), `hooks/tokens.py:495` | confirmed | executed as gate decisions; the one sibling left is 🟡 3 |
| 🟢 | #739's three recorded shapes are still data, and the third is judged where it lands | `tests/test_a_heredoc_body_nothing_runs_is_data.py` | confirmed | executed: through the module's own builders at the target and with the candidate fixes |
| 🟢 | The `gh api` narrowing is acceptable | `hooks/tokens.py:268` | confirmed | executed: `gh api` runs `git` and `ssh -G` like the admitted two; a body piped into it, with no file written, stays data |
| ❓ | Whether a repository configuration written by the line can make the `git` subcommands `gh` runs (`remote -v`, `config --get-regexp`, `symbolic-ref`, `rev-parse`) run a program | `hooks/tokens.py:495` | ❓ out of verified scope | read only: none of them is known to run hooks or a configured program, and nothing here ran them against a hostile configuration. The repository owner answers it |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` on `tests/test_a_heredoc_body_nothing_runs_is_data.py` at `a4d28eda`, in a scratch clone | 130 passed |
| `heredoc_data`, `heredocs` and `main()` on constructed strings at `a4d28eda`, `38cdc0ec` and `e141980a` | as in the verdicts; no gate string ran in a shell |
| bash and zsh on harmless `cat` strings: a carriage-return line and a commented line under a blank-ending delimiter | both shells kept reading the body past the line the reader ends on |
| gh 2.100.0 with logging stand-ins first on an absolute `PATH` entry, dummy token, network blocked | `pr ready`, `pr edit` with a flag and `api` each ran `git` and `ssh -G`; no pager or editor ran |
| `ssh -G` with a scratch configuration holding a `Match exec` that creates a marker file | the marker was created: `ssh -G` runs `Match exec` |
| The candidate fixes below, applied in the scratch clone: `bin/test` on the heredoc module and `tests/test_what_the_reader_understands.py` | 258 passed. Every 🔴 shape and the 🟡 shape stop, and the recorded shapes stay data. Reverted afterwards |
| ruff check and format on the fixed `hooks/tokens.py` | clean |
| The broad gate: the full suite, repository-wide lint and typecheck | not yet. This is the sealer's run, and nothing here ran it |

## Paste-ready fixes

### 🔴 1 — fail closed on a carriage return

In `heredoc_data`, `hooks/tokens.py`, directly after `unread = [False] * len(records)`:

```python
    # The shell compares a heredoc line with its delimiter byte for byte and
    # strips no `\r`; the reader strips one, so it can end a body early.
    if "\r" in (command or ""):
        return unread
```

The regression case for `test_the_rule_answers_per_body` is built as follows. Write a quoted sink body whose second line is the delimiter plus `\r`. Follow it with a second quoted `cat` opener, the bare first delimiter, any plain line, and the second delimiter. The case expects `[False, False]`. It is green with the guard and red at `a4d28eda`, where the answer is `[True, True]`.

### 🔴 2 — compare the reader's boundaries on the raw text

A helper beside `_writes_a_file`, and a second clause on the guard above:

```python
def _boundaries(records):
    """Where each body ends, as the reader found it: enough to tell two
    readings of one line apart without comparing body text a comment changed."""
    return [(r.delimiter, r.dashed, r.terminated, r.text.count("\n")) for r in records]
```

```python
    # The shell ends a body on the raw text: it strips no `\r` from a line
    # and drops no comment from a body line. Where either could move a
    # terminator, the reader's boundaries need not be the shell's, so no body
    # on the line is data.
    if "\r" in (command or "") or _boundaries(heredocs(command or "")) != _boundaries(
        records
    ):
        return unread
```

The regression cases are three. Each has a quoted sink delimiter that ends in a space, ends in a tab, or is a single space. The body line after the opener is that delimiter followed by `#x`, and the rest of the line follows 🔴 1's construction. Each expects `[False, False]` and answers `[True, True]` at `a4d28eda`. The PY_BODY recorded shape, whose `#` line `drop_comments` empties, stays data, because the line count does not change.

### 🟡 3 — count `ssh` where `gh` runs, and correct the claim

In `heredoc_data`, `hooks/tokens.py:495-497`:

```python
    programs = {c.program for c in commands}
    if "gh" in programs:
        # gh runs `git` and, for an ssh remote, `ssh -G`, both from `PATH`
        # (measured at gh 2.100.0, #763 post-review).
        programs |= {"git", "ssh"}
```

The comment above `GH_NOTHING_LOCAL` should replace "provably run nothing local" with what was measured:

```python
# The `gh` subcommands whose body file nothing they run can execute, read
# from `gh <group> <sub> --help` at gh 2.100.0 and measured with logging
# stand-ins: each runs `git remote -v`, `git config` and, for an ssh remote,
# `ssh -G` from `PATH`, and no pager, browser or editor. Every other
# subcommand can run local git that runs hooks (`questions.md` Q4), or a
# pager, browser or editor its configuration names (#763). `heredoc_data`
# counts a file written over `git` or `ssh` wherever `gh` stands.
```

`docs/commit-review-gate-spec.md:221` and the *As built* note at `spec.md:64` then say "`git` and `ssh` included where `gh` runs them". The regression case: the 🟡 shape expects `[False]`, and it answers `[True]` at `a4d28eda`.

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| A body written to the user's ssh configuration, holding a `Match exec` command, then `gh` against an ssh remote. `ssh -G` runs the command. The gate is silent at the base too, because a body read as shell finds no commit inside that quoted string, so this predates #739 and its data verdict changes nothing | this file; a new issue if the owner wants it tracked | the repository owner |

Needs a fix: yes — 🔴 1 at hooks/cmdline.py:620 and hooks/tokens.py:476, 🔴 2 at hooks/tokens.py:476, 🟡 3 at hooks/tokens.py:268 and hooks/tokens.py:495

Loses a record or crashes: no

## Proof block

Files opened: `hooks/tokens.py` (lines 220-508), `hooks/cmdline.py` (lines 155-633), `hooks/commit-review-gate.py` (lines 370-459), `tests/test_a_heredoc_body_nothing_runs_is_data.py` (lines 1-110 and 150-215), `tests/conftest.py` (the helpers `run_hook`, `decision_of`, `load_hook_module` and `declare_routing`), `bin/test`, `rounds/round-3-report.md`, issue #763, and the diff of `a4d28eda`, docs and spec included. Target `a4d28eda`, read in a `git clone --no-local` scratch clone. The worktree's HEAD was not moved.
