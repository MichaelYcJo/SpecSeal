# Repository config

What this repository says about itself, one row per item, read by the skills
that need it. It sits in the root the plugin maintains, beside `parity.md`,
in the same shape: a markdown table.

The root is at one of two places and whichever exists is the answer:
`<repo>/seal/`, which is committed, or `$(git rev-parse --git-common-dir)/seal/`,
which is not. This file goes wherever that root already is.

**This file is optional, and an absent row is not an error.** Every item has
a default, and the defaults are what every repository got before the row
existed. Create the file when one of the answers is not the default; a file
that restates the defaults is a file nobody needs.

`Mode` is the exception that proves it: what every repository got before that
row existed is *the folder decides*, which is not a value, so it has no
default at all. An absent one is filled in from where the folder is, by the
command that reads it. The section on it below says how.

| Item | Value |
|---|---|
| Commit and pull request language | English |
| Record language | English |
| Mode |  |

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
  `Fixes checked by`, `Contract changes`, `New units`, `Needs a fix` and its
  `Pass` checkbox; its `## Verdicts`, `## Executed probes`, `## Inherited
  coordinates` and `## Deferred` headings, and the `Verdict` column of the
  first; the verdict words `fixed`, `answered`, `withdrawn`, `not a defect`
  and `agreed, fixed`; `round-N`, `none`, `no fixes to check` and
  `nobody` in `nobody — <why>`; an `overview.md`'s `## Not verified` heading with its
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
