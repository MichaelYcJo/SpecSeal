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
| Pull request language | English |
| Mode |  |

## Pull request language

The language the **commit subject and body** and the **pull request title and
body** are written in. `commit-pr-convention` reads this row before it writes
any of the four. The value is a language's English name — `English`,
`Korean`, `Japanese` — because the reader is a model choosing prose, not a
lookup table.

Three things it does **not** govern, so that changing it changes only the
prose:

- **The prefix vocabulary is not translated.** `feat:`, `fix:`, `docs:` and
  the rest stay as they are, in every repository. They are scanned in a log
  and parsed by tooling, and a translated prefix teaches neither.
- **Branch names.** Still `<prefix>/<kebab-case-slug>` in ASCII: a branch
  name is typed into a shell and pasted into a URL.
- **The response language** — what the session says to *you*. That is a
  person's setting, not a repository's, and it stays in the user's own
  configuration. Two people working in one repository can want different
  answers there and the same answer here.

Where a translated body is wanted, it goes in the repository as a file, named
for **its own** language rather than the body's: the work item's own folder
holds `pr.ko.md` when this row says English, and `pr.en.md` when it says
Korean.

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
