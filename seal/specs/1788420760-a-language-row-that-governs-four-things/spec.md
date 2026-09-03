# A language row that governs four things — spec

<!-- seal/specs/1788420760-a-language-row-that-governs-four-things/spec.md —
issue #106. Written before the first edit. -->

## The problem, stated from the repository's side

`seal/config.md`'s first row is `Pull request language`, and #82 built it to
govern four things: the commit subject and body, and the pull request title
and body. Everything else this plugin writes into a repository is English
whatever that row says — `spec.md`, `plan.md`, `overview.md`, `changelog.md`,
the round records' prose, the ledger rows' sentences, and the review report a
person posts.

So a repository whose people work in Korean gets Korean pull requests and
English specifications. That is a pull-request setting wearing a language
setting's name.

**The row ships in this release.** Widening it later renames a key every
repository that wrote the file already has, which is the one change a config
file cannot absorb quietly.

## Two rows, and why not one and not seven

The combinations people want are three: everything English, the commits and
pull requests in the team's language with the documents in English, and both.
One row cannot express the middle. One row per document kind — spec, plan,
overview, changelog, rounds, ledger, the posted report — is seven rows where
nobody sets the sixth differently from the fifth.

| Row | Governs | Default |
|---|---|---|
| `Commit and pull request language` | the commit subject and body, the pull request title and body, and the review report posted as a pull-request comment | English |
| `Record language` | the prose in `spec.md`, `plan.md`, `overview.md`, `questions.md`, `changelog.md`; `rounds/round-N.md`'s cell contents and the prose beneath its tables; the ledger rows' claim and grounds | English |

**The first row is renamed as well as widened.** It has governed the commit
subject and body since it shipped, so `Pull request language` has always
understated it.

**The review splits across both, and that is what having two is for.** The
first draft of #106 put the posted report with the records, on the grounds
that it is a copy of `round-N.md` and one text cannot be two languages. That
premise is false: `skills/code-review/SKILL.md` writes the three files
*"right after posting the report"*, so posting and recording are separate acts
producing different texts, and it says elsewhere that the user does the
posting. They
divide by what they are — a report is prose for a person who opens the pull
request, and a round record is half structure, its field names and verdict
vocabulary read literally by `chain_check.py`.

**Independent, with no coupling.** Setting one to Korean does not carry the
other. `templates/config.md` already fixes that: *an absent row is not an
error, every item has a default, and the defaults are what every repository
got before the row existed.* A row that silently inherits another's value
breaks that sentence, and the person who set one and not the other did not ask
for the second.

## Acceptance criteria

| # | Given / when / then | Verifiable how |
|---|---|---|
| S1 | Given `seal/config.md` with `Commit and pull request language \| Korean`, when a session writes a commit or a pull request, then it writes Korean | S1 case: the skill names the row and defers to it |
| S2 | Given `Record language \| Korean`, when a session writes any of the SDD documents or a ledger row's prose, then it writes Korean | S2 case: the implement skill and both agents name the row |
| S3 | Given one row set and the other absent, when either surface is written, then the absent one is English | S3 case: no coupling in either direction |
| S4 | Given no file, no such row, an empty value, or a file that does not parse, when either surface is written, then it is English and nothing stops | S4 case, four shapes × two rows |
| S5 | Given any value, when anything is written, then the commit prefix vocabulary, branch names, code, identifiers, docstrings, file names and test function names stay English | S5 case, unchanged from #82 and widened |
| S6 | Given `Record language \| Korean`, when a round record is written, then its field names, verdict vocabulary, `Pass` checkbox and `<!-- -->` markers stay English and only the cell prose is Korean | S6 case: the checkers read those strings literally |
| S7 | Given the ledger, when a row is written, then the anchors `path#unit@hash` stay as they are whatever the row says | S7 case |
| S8 | Given the response language, when anything is written, then it is not in this file — it stays the person's own setting | S8 case, unchanged from #82 |

## Fail directions

| What goes wrong | What happens | Why that and not something else |
|---|---|---|
| A row names a language this plugin's reader does not recognise | the prose is written in it anyway | The reader is a model choosing prose, not a lookup table. A list of permitted languages would be a list somebody has to maintain |
| A row is translated into the language it names | it is not read | The row's own name is a key. `templates/config.md` says the item column is English, as `parity.md`'s already is |
| A record's field name is translated | `chain_check.py` stops reading the record | Which is why the exclusion list is longer than #82's and says which strings are read literally |
| Both rows are set to different languages | each surface follows its own | That is the middle case the second row exists for |

## What this does not change

`skills/writing-style/SKILL.md` already carries independent norms per language
and says the sentence-level rules follow the output language. It needs the
least of any file here.
