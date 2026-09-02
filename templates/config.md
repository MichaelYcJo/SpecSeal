# Repository config

What this repository says about itself, one row per item, read by the skills
that need it. It sits in the root the plugin maintains, beside `parity.md`,
in the same shape: a markdown table.

**This file is optional, and an absent row is not an error.** Every item has
a default, and the defaults are what every repository got before the row
existed. Create the file when one of the answers is not the default; a file
that restates the defaults is a file nobody needs.

| Item | Value |
|---|---|
| Pull request language | English |

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
for **its own** language rather than the body's: `seal/specs/<work-item-id>/`
holds `pr.ko.md` when this row says English, and `pr.en.md` when it says
Korean.
