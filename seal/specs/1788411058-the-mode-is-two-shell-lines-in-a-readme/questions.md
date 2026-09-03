# Open decisions — the mode is two shell lines in a README

<!-- seal/specs/1788411058-the-mode-is-two-shell-lines-in-a-readme/questions.md
— decisions only a person can make. Each row says what was built to, so the
work continues and the answer can overturn it later. -->

Nothing here blocked the build. Each was decided in the first minutes, built
to, and written down where the owner can overturn it in one edit.

## Q1 — how does a person apply an edited row?

The issue's *What the command does* reads "`seal mode` prints the current
mode and the row … and with no argument after an edited row, applies the
row", which gives the bare command two behaviours. The spawn prompt resolved
it the other way and left the spelling to me.

**Built to:** `seal mode` reports and never moves a **folder**; `seal mode
--apply` applies the row.

It does write one thing: a `Mode` row that is absent, filled in from where
the folder is (the decision that arrived mid-build, `spec.md` §"The row has
no default at all"). That is not the behaviour this question rules out. What
must not happen is a bare command that moves directories; a row written from
an observation the command just made cannot be wrong, and the state it fixes
is the state every repository with a `config.md` is in today.

**Grounds.** A person types the bare command to find out where things stand,
and a command that answers a question by moving directories is the shape
nobody expects twice. It is also the rule the neighbouring subcommand already
follows: `seal export --check` writes nothing. The one-way-door in Q3 makes
this sharper — the bare command could otherwise move a local root into the
tree because somebody typed it to look.

**To overturn:** make `--apply` the default when a row disagrees, and add a
`--dry-run` for the report.

## Q2 — should the check fail a pull request, or only name the disagreement?

**Built to:** `seal mode --check` exits 1 on a disagreement, and the step is
added to `.github/workflows/hygiene.yml` and `templates/hygiene.yml`.

**Grounds.** The repository's own rule for a red build is whether the author
can always fix it — `unverified_check.py` never fails for an honest open row
and always fails for a section nobody can read. A mode disagreement is always
the author's and always one command from fixed, which puts it on the failing
side. It differs from `seal export --check`, which reports a state nobody did
wrong, and `spec.md` says so where a reader will meet the two together.

**To overturn:** print `::warning::` instead, the way the *both READMEs move
together* step does.

## Q3 — local → shared cannot be walked back. What does the command owe?

Going to shared puts the records in the tree; once that is committed they are
in the history, and `seal mode local` afterwards removes them from the tree
and not from the history. The direction local mode exists to prevent is
exactly the one that cannot be undone. Handed to me with the shape left open.

**Built to:** the command says it plainly, before it acts, and then acts. No
flag, no prompt.

**Grounds.** The point of no return is the **commit**, not the move: until
the person commits, `seal mode local` walks the whole thing back, and the
command stages rather than commits precisely so that moment stays theirs. The
line says that, names the commit as the door, and appears above the *now
commit* line rather than below it. A confirmation flag would ask the same
question twice — `seal mode shared` is already an explicit argument, and
`--apply` is already a person acting on a row they wrote — and `seal import`
sets the local precedent that these commands report rather than ask.

**To overturn:** require `--yes` for the local → shared direction, or refuse
when the tree has any commit whose message the person has not seen. The line
stays either way.

## Q4 — where does the disagreement check live?

Named by the prompt as mine to decide and defend.

**Built to:** `seal mode --check`, in `skills/implement/scripts/seal.py`,
called from both hygiene workflows. `spec.md` §"Where the check lives" is the
argument: a checker of its own would be a second reader of the root and of
the row, which is what `hooks/optin.py` exists as a module to prevent, and
neither `skills/verify/scripts/` nor `skills/evidence-check/scripts/` reads
the root's own config today.

**To overturn:** `skills/verify/scripts/mode_check.py`, importing the reader
from `seal.py` rather than writing a second one.

## Q5 — does `templates/config.md` ship a `Mode` value?

**Built to:** the template's table carries `| Mode |  |` — the row with an
empty value — and a `## Mode` section explaining it.

**Grounds.** The skill tells a person to copy the template into the root and
edit it. A template shipping `| Mode | shared |` would hand every local-mode
repository a row that lies from the moment it is copied, and the fix the
command then offers is `--apply`, which would move their root into the tree
through the door of Q3. An empty value is already this file's spelling for
*not declared* — it is one of the four ways the pull-request-language row
lands on its default.

**To overturn:** drop the row from the table and document it in prose only.

The mid-build decision in Q1 makes this self-correcting rather than merely
harmless: a copied template's empty value is *not declared*, and the first
`seal mode` fills it in from the folder the copier is actually in.

## Q6 — does first setup write the row?

**Built to:** no. Bootstrap creates the root and nothing else; the skill's
bootstrap section names `seal mode` as the way to change the answer later,
which is what the repository migrated from 0.3.x needs.

**Grounds.** `templates/config.md` says a file that restates the defaults is
a file nobody needs, and an absent row is not an error. Writing one at setup
would put a `config.md` in every repository that opts in, for a row whose
absence already means the right thing.

**To overturn:** write the row in the shared branch of bootstrap only, where
the file is committed anyway and CI can then read it.

## Q7 — a clone with more than one worktree

Measured 2026-09-03: switching shared → local from a linked worktree leaves
the main worktree holding the committed `<repo>/seal/` on its own branch, so
the two worktrees read two different roots until the commit reaches both.

**Built to:** a note naming every other worktree and what it will read, and
the switch completes.

**Grounds.** Nothing is lost and it heals itself: the other worktree's copy
is the committed one, still in the history, and it disappears from that tree
when the branch arrives. Refusals in this command are for states where
something would be lost or half-moved, and this is neither. `seal export`'s
`note:` for an output path inside the tree is the same weight of warning.

**To overturn:** refuse when `git worktree list` names more than one, with a
flag to proceed.
