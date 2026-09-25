# Repository config

What this repository says about itself, one row per item, read by the skills
that need it. It sits in the root the plugin maintains, beside `parity.md`,
in the same shape: a markdown table.

The root is at one of two places and whichever exists is the answer:
`<repo>/seal/`, which is committed, or `$(git rev-parse --git-common-dir)/seal/`,
which is not. This file goes wherever that root already is.

**This file is optional, and an absent row is not an error — with two
exceptions, `Mode` and `Broad gate`.** Every other item has a default, and
the defaults are what every repository got before the row existed. Create the
file when one of the answers is not the default; a file that restates the
defaults is a file nobody needs.

`Mode` is the exception, twice over. What every repository got before that row
existed is *the folder decides*, which is not a value, so it has no default at
all — an absent one is filled in from where the folder is, by the command that
reads it. And an absent one is not silent: a root with no `Mode` row is a root
nobody chose a mode for, so the first Bash call of a session in that
repository is denied and the second is asked, until `seal mode` writes the
row. Two prompts per session per repository, then silence, and nothing at all
once the row exists. The section on it below says how the command fills it in.

`Broad gate` is the other, and its absence is not a prompt but a refusal:
`broad-gate` names the row and exits 2 with nothing run, because a seal taken
over a command nobody chose seals nothing. The section on it below says why
there is no default.

| Item | Value |
|---|---|
| Commit and pull request language | English |
| Record language | English |
| Mode |  |
| Broad gate |  |

## Commit and pull request language

The language the **commit subject and body**, the **pull request title and
body**, and the **review report posted as a pull-request comment** are written
in. `commit-pr-convention` reads this row before writing any of them. The
value is a language's English name — `English`, `Korean`, `Japanese` —
because the reader is a model choosing prose, not a lookup table.

## Record language

The language the **prose** in the work-item records is written in:
`spec.md`, `plan.md`, `overview.md`, `questions.md`, `changelog.md`, the cell
contents of `rounds/round-N.md` and the prose beneath its tables, and the
claim and grounds of a ledger row.

**Independent of the row above.** Setting one does not carry the other, for
the reason stated at the top of this file: an absent row's default is what
every repository got before the row existed, and a row that silently inherits
another's value is not that. Someone who set the commits to Korean and left
this one alone did not ask for Korean records.

The records have a human audience too, and how large it differs by repository.
They are what somebody opens six months later to find out why a decision went
the way it did. Where the whole team reads them, English is a tax on every
reader; where the repository is aimed outward, English is the point. That is a
fact about the people rather than about the file, which is why it is a row and
not a rule.

**The review splits across the two rows on purpose.** The report posted to a
pull request is prose for whoever opens it, and follows the row above.
`rounds/round-N.md` is half structure — its field names and verdict vocabulary
are read literally by `chain_check.py` — and its prose follows this one.

## What no row governs

Changing a language changes prose and nothing else. These stay English in
every repository, whatever either row says:

- **The prefix vocabulary is not translated.** `feat:`, `fix:`, `docs:` and
  the rest are scanned in a log and parsed by tooling, and a translated
  prefix teaches neither.
- **Branch names.** Still `<prefix>/<kebab-case-slug>` in ASCII: a branch
  name is typed into a shell and pasted into a URL.
- **The field names, section headings and vocabulary a checker or a pinned
  case reads literally** — a round record's `Target SHA`, `PR`, `Broad gate`,
  `Fixes checked by`, `Contract changes`, `New units` and the `depth` its
  entries carry, `Needs a fix`, `Loses a record or crashes` with the `no` and
  `yes` its answer is written in, and the `Pass`
  checkbox; its `## Verdicts`, `## Executed probes`, `## Inherited
  coordinates` and `## Deferred` headings, and the `Verdict` column of the
  first; the verdict words `fixed`, `answered`, `withdrawn`, `not a defect`,
  `agreed, fixed`, `out of verified scope` and the `deferred` in
  `deferred <home>`; `round-N`, `none`,
  `no fixes to check` and `nobody` in
  `nobody — <why>`; `Ran by` with the `on` that joins its two halves and the
  `unknown` in `unknown — <why>`; an `overview.md`'s `## Not verified`
  heading with its
  `Item` and `Who must answer` columns. A translated field name is not a
  translation, it is a broken gate.
- **The markers and anchors.** `<!-- specs/<work-item-id> -->`, a release
  section's `## X.Y.Z — <date>`, a drained file's `drained` line, the `✅`
  that closes a row and the `🔴` that opens one, and a ledger anchor's
  `path#unit@hash`.
- **Code.** Identifiers, comments, docstrings, file names, and test function
  names.
- **The item column of this table**, which is a key rather than prose — the
  same rule `parity.md` already follows.
- **The response language** — what the session says to *you*. That is a
  person's setting, not a repository's, and it stays in the user's own
  configuration. Two people working in one repository can want different
  answers there and the same answer here.

Where a translated pull-request body is wanted, it goes in the repository as
a file, named for **its own** language rather than the body's: the work item's
own folder holds `pr.ko.md` when the commit row says English, and `pr.en.md`
when it says Korean. A record has no mirror — there is one file and a checker
reads it, so its prose is whatever `Record language` says and nothing else.

That folder sits under the root, which is resolved rather than spelled — the
same two places this file is looked for. Where the root resolves under the
git directory, the mirror does **not** go there: nothing under it is ever a
commit candidate, so a reviewer cannot open the file and the merge carries
nothing. Put it beside the documents the pull request already touches.

## Mode

Which of the two places this repository's root should live at: `local` or
`shared`. Empty above on purpose — see *There is no default* below.

**This row is what the repository wants. The folder's location is what it
has.** They are separate on purpose, and the second is the only one anything
at runtime reads: every gate resolves the root by looking for `<repo>/seal/`
and then `$(git rev-parse --git-common-dir)/seal/`, and a gate that trusted
this row instead would go looking in a place with no folder. The row can be
edited by anyone with a text editor; the folder is where the files are.

`seal mode` is the only thing that reads it:

```bash
seal mode            # the folder, the row, and whether they agree
seal mode local      # switch to local mode, and write the row
seal mode shared     # switch to shared mode, and write the row
seal mode --apply    # switch to whatever this row says
```

So a disagreement is not an error state to be feared. It is the input the
command consumes: edit the row, run `seal mode --apply`, and the folder
moves. `seal mode --check` — which the pull-request checks run — exits
non-zero for a disagreement left standing, so the row cannot quietly become
a document that lies.

**There is no default, and an absent row is filled in from the folder.**
Every other item here falls back to what repositories got before the row
existed; for the mode, what they got is *the folder decides*. So the first
`seal mode` in a repository with no such row writes one from where the
folder actually is — an observation rather than an assumption — and says
that it did. A fixed default of `shared` would write a lie into every
local-mode repository that had not declared one.

That is also why the row above is empty in this template. A copied file that
declared `shared` would hand every local-mode repository a row that is wrong
from the moment it lands.

## Broad gate

The repository's own broad command — the full suite, the repository-wide
lint, the typecheck — as **one shell command line**, run from the repository
root by `broad-gate` once the review rounds settle. The plugin's own checks
(`evidence-check`, `unverified-check`, `chain_check.py`, `survivor-check`)
follow it and are not part of the row.

Two of those checks, the survivor arm and the correction arm, are left out
where the base names `main` and the repository's `.github/workflows/hygiene.yml`
carries their steps in its `release` job, because that workflow skips both
steps on a pull request into `main`; the gate prints one line saying so. The
skip is keyed on the spelling `main` or `origin/main` and on the step being
present in the workflow, not on the guard the step carries.

```markdown
| Broad gate | bin/test -q && uvx ruff check . && uvx ruff format --check . |
```

**An absent row is a refusal, not a default.** `broad-gate` names this row
and exits 2 with nothing run. It is a refusal rather than a prompt because
the command runs unattended — the sealer asks nobody anything — and a
refusal that names whose the row is and where it is answered reaches that
person through whoever read it, where a question stops a session that may
have nobody at the keyboard. It does **not** name a command to write: doing
that asked the one party that may not choose one, which is what #401
reported.

**There is no default, and the reason is the Seal Test.** `verify` names the
counterfeit: a check that cannot fail. A default of `pytest` seals a
repository that runs `npm test`; a default of `true` seals everything. The
sealer judges nothing, so it cannot pick a command either — a row is a
thing a person wrote, and what the sealer's seal covers is exactly that. What the
row's command does is the repository's own claim: a command that exits 0
without running anything gets a stamp over nothing, and *the narrow command
still has to be able to fail* is the reader's rule, not the gate's.

**Which shell runs the row, and what it is handed.** `/bin/sh` on macOS and
Linux. On Windows it is whatever `%COMSPEC%` names, which is `cmd.exe` unless
somebody changed it, and `cmd.exe` reads a `/` inside a command name as the
start of a switch: handed `bin/test -q`, it runs a command called `bin` and
fails before any test does (#448). So where the shell is `cmd.exe`, the gate
hands it the row with `/` written `\` inside a command name that starts in a
directory, and nowhere else. A command name is the word at the start of the
line, or the first word after `&&`, `||`, `&`, `|` or a `(` that opens a
block. It starts in a directory where the part before its first `/`, with its
quotes and carets removed and every leading `@` dropped, names a directory
that exists where the row runs; a name that begins with `/` starts at the
drive's root, which always exists. A `%VAR%` in that part is expanded from the
gate's own environment first, as `cmd.exe` expands it before it reads the
name, so `%CD%/bin/test` is still rewritten. `bin/test` then runs as `bin\test`, which
`cmd.exe` resolves to `bin/test.cmd`. Arguments, quoted
paths, `%VAR%`, operators and `^`-escaped characters reach the shell as
written. Every other position is handed as written, and `cmd.exe` reads it
exactly as before — the definition above is the rule, and these are
examples of it rather than the whole list: a path after `call`, `start` or
`if`, or after `else`, `for … do` and `cmd /c`; a command name after a
redirection that opens its command (`>out.txt bin/test`); and a `/` written
straight after one of `cmd.exe`'s own commands, which is that command's
switch (`rd/s/q build`). A `/` written straight after any other program's
name reaches `cmd.exe` as written too, because no directory carries the
program's name: `xcopy/e/i` stays `xcopy/e/i`. A blank before the switch
(`xcopy /e`) works as well, and is never rewritten. The directory is judged
where the row starts, and that has two bounds. A directory an earlier command
in the row makes, or one a `cd` earlier in the row enters, is not seen, so
that name is handed over as written, which is what `cmd.exe` got before the
gate rewrote anything. And a directory at the root named like a program the
row calls with a glued switch (an `xcopy/` directory) makes `xcopy/e` read as
a path; `cmd.exe` itself cannot tell the two apart in that tree, so write the
blank there. Any other
`COMSPEC`, and every POSIX shell, is handed the row as written. Where the
two differ, the gate prints one line saying what `cmd.exe` was handed, and
that check's kept output carries it under the row as written.

### What is refused, and what stays allowed

**A value that would not run as the command it reads as is refused, not
repaired.** `broad-gate` looks at the row before it hands it to a shell,
and three forms come back exit 2 with nothing run — the same shape an
absent row gets. The criterion is one sentence with two halves, and a form
is refused only for breaking one of them:

> **The value must run as the command it reads as, and the exit code the
> gate reads must be that command's.**

| Refused | Written as | What a shell does with it |
|---|---|---|
| the whole command wrapped in backticks | `` `bin/test -q && ruff check .` `` | runs the content, **discards its exit status**, then executes its OUTPUT as a command. The same content exits 1 bare and 0 wrapped, with the failure still on the screen |
| the whole command wrapped in `$(…)` | `$(bin/test -q && ruff check .)` | the same semantics in the spelling somebody who knows shell reaches for first |
| a trailing `&` that is not part of `&&` | `bin/test -q &` | `/bin/sh` backgrounds the whole line and answers 0 before any check has finished. `cmd.exe` separates two commands instead, so what the gate reads is the second one's status. Two different wrong answers, refused for the same half of the criterion |

**Nothing is stripped.** A value quietly repaired here would leave the file
still wrong and teach the next person that the way they wrote it was right,
so the refusal names the form, quotes the row as written, and shows it as
meant. Rewriting it is the person's act, and `/specseal:config` is the door
to the row.

**A table inside a code fence is an example of this format and never a
repository's own answer.** The live table is the first `| Item | Value |`
table that stands outside every fenced code block, and a line inside a fence
is not part of any table: not a header, not a separator, not a row, and not a
line somebody wrote as a row. One rule says so and all three walks of this
table read through it — the gates' reader, the mode gate's reader, and
`seal mode`'s writer — so the reader and the writer can never disagree about
which row is the row.

A fence opens at a line indented at most three spaces whose first run is three
or more backticks or three or more tildes, and closes at the next line of at
least as many of the same character with nothing after it but spaces. **A
fence that is never closed runs to the end of the file**, so everything under
it — the live table included — reads as undeclared: `broad-gate` exits 2 with
a message and the mode question comes back. That is loud rather than quiet,
which is the trade this rule is written for.

What it prevents is quiet and was reachable by following this plugin's own
procedure. The block `/specseal:config` copies out of this file carries the
fenced example row above, and nothing said where in `seal/config.md` it had to
land; pasted above the live table, or above a table with no parseable row yet,
the example WAS the table every gate read — the sealer's seal taken over a
plausible command nobody chose (#429). **`broad-gate` says so by name**: where
this gate's row exists only inside a fence, the refusal quotes that line and
says where it has to move to, rather than reporting the row absent.

**Everything else stays legal**, because the row is an arbitrary shell
command line by design. A gate that could tell a status-discarding `;` from
one inside a quoted argument would need a shell parser, whose own failure
modes would make legitimate rows unwritable. What each costs is stated here
rather than paid for by a refusal:

| Stays legal | What it costs |
|---|---|
| `$(…)` **inside** a longer line | nothing. `pytest -n $(nproc)` still runs as the command it reads as |
| `;`, `\|\|`, quotes, redirection, variables, globs | the row answers with whatever the composition the repository wrote answers with. That is the repository's own claim about itself, which is what this row already is |
| a pipe, **written `\|`** | the same, and one thing more. A piped row exits with the pipe's LAST status, so `bin/test -q \| tee out.txt` is green whenever `tee` is — the repository's own claim about itself. **This file is markdown and a cell of it ends at a bare pipe**, so `\|` is how the value carries one, the way every other cell of this table already writes it. The reader reduces exactly those two characters to a plain pipe before any shell sees it, so a value holding Windows path separators is untouched. **A BARE pipe still parses as no row**, and `broad-gate` quotes that line back and names the escape rather than reporting the row as absent. **A line that does not parse still takes every row below it** where a row above it already parsed — `config_rows` stops reading the table there, so a `Mode` row written under it is invisible and `seal mode` writes a second one into the file. Measured 2026-09-17; the row's own fragment carries it. Written LAST in its table it takes nothing, because nothing is under it to take, and `broad-gate`'s refusal asks what was written below the line before it says anything was lost (#430) |
| an `&` anywhere but at the end | the command before it is backgrounded and its status discarded, exactly as a `;` discards one — and unlike a `;`, it may still be running when the gate stamps, writing into the tree the stamp is about. That is `/bin/sh`; `cmd.exe` sequences the two commands instead, so nothing is left running and the status read is the second command's. Telling an operator `&` from a `2>&1` or a quoted `&` needs the shell parser this list exists to avoid, so it stays the row author's own composition. The **trailing** form is refused, because nothing composes after it and the whole line goes to the background |

### Choosing a value — the criterion

Three rules, and this section is their one home. Every other document that
mentions the row points here instead of restating them, because a rule
written in three places is three places for it to disagree with itself.

| # | Rule | Why |
|---|---|---|
| 1 | A check that is red repository-wide for reasons unrelated to any branch does not belong in the row | It would block every future work item for something none of them caused, and a gate that always fails is read as noise and then ignored |
| 2 | A command that **fixes** the tree — `--fix`, `--write`, a formatter in write mode — is not a gate command | A gate asks what is wrong. One that changes the answer while reading it can only come back green, which is the counterfeit `skills/verify/SKILL.md` §*The Seal Test* names |
| 3 | The suite runner comes first | On a failing test the gate re-runs the row's first command on the failing files alone, at the base, in a scratch worktree it removes afterwards, and labels each `new` or `failing on base too`. That first command is what stands before the row's first `&&`, so a row whose suite runner comes first is a row the comparison can use |

Rules 1 and 2 were derived under pressure by the session that met the gate's
refusal after its review rounds had settled, and were written nowhere until
#401. Rule 3 was already here and in the config skill, and it is folded into
this table rather than copied into a third place.

## The fold's values

Three rows, read by `fold-check`, which holds `settle`'s two fold rules over
the top level of `docs/` (`skills/settle/SKILL.md` §2). The plugin sets no
value for either rule; these rows are where a repository states its own.

```markdown
| Fold shape from | 1790154761 |
| Document line ceiling | 1000 |
| Over the ceiling | none |
```

| Row | Value | Absent |
|---|---|---|
| `Fold shape from` | a work-item id's epoch prefix. A statement whose marker holds an id at or above it has the fold's shape; `0` binds every statement | the shape is not checked |
| `Document line ceiling` | a positive whole number of lines, which no top-level `docs/*.md` may exceed unless it is listed below | no length is checked |
| `Over the ceiling` | `none`, or entries separated by `;`, each `<path> frozen at <n> markers <digest> until <home>` | nothing is listed |

**An absent row means not declared, and the command says so rather than
refusing.** That is what every other optional row here means, and a
repository that never folds has not asked for either check. The cost is
stated rather than hidden: a row deleted while tidying this file turns its
check off, and the only trace is the one line `fold-check` prints about it.

**A value that will not parse is refused.** A cutoff or a ceiling that is not
a whole number, or an entry out of shape, exits 2 naming the row, and nothing
is checked. A flag, `--shape-from` or `--ceiling`, overrides its row for one
run.

**A listed document's markers are frozen, not its length.** The count is how
many fold markers it may carry, and the digest is which ones: the first 12 hex
digits of a SHA-256 over its sorted live marker ids. Nobody computes it by
hand. When the count or the ids disagree, `fold-check` prints the digest the
file has now, to be written into the entry in the commit that changed them.
The entry names its home, the issue or document that will split the file,
and it fails once the file is back under the ceiling, so it cannot outlive the
split.
