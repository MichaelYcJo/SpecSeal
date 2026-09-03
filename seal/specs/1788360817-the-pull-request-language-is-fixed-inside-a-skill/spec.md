# Feature Specification: the pull request language is fixed inside a skill

<!-- seal/specs/1788360817-the-pull-request-language-is-fixed-inside-a-skill/spec.md
— WHAT this work delivers and how we'll know. The policy documents in docs/
outrank this file; cite them, don't restate. -->

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `docs/one-root-by-lifetime.md#"## What the root is called"` — *"English stays for every shipped artifact… Korean is the owner's per-user setting: the response language and `pr.ko.md`"* | Names the two things that are the OWNER's setting and must stay out of the repository file. It is also why this repository keeps English: its shipped artifacts are read by strangers |
| Issue #82, done-when 3 — *"The response language is not in this file; it is a person's setting"* | The same boundary, stated for the new file |
| `README.md#"### Shared or local"` and `hooks/optin.py#home_at` | Where the root is. Anything under it is `<repo>/seal/` where that exists and `$(git rev-parse --git-common-dir)/seal/` otherwise, so a skill that spells one place leaves local mode unable to say anything |
| `CONTRIBUTING.md` — a change writes a fragment, never a shared registry | `changelog.md` and `seal/ledger/<id>.md` here, not `CHANGELOG.md` and not `seal/ledger.md` |

## Scope

**In.** One new template, `templates/config.md`, producing `seal/config.md`:
a `| Item | Value |` table in the root the plugin owns, in the shape
`parity.md` already uses. Its first row is `Pull request language`. The
`commit-pr-convention` skill reads it and stops requiring English of
everyone — at the five places that say English today
(`skills/commit-pr-convention/SKILL.md:47`, `:68-70`, `:74`, `:88`, `:131`).
The mirror file's name is generalised from `pr.ko.md` to `pr.<lang>.md`. The
root's README and both top-level READMEs list the new file. Tests pin all of
it.

**Out, and each for a reason a reader can check.**

- **No hook enforces the language.** Nothing can read a commit message and
  judge what language it is in without being wrong about names, code
  identifiers and quoted English. The skill is the mechanism, the way it is
  for the prefix vocabulary, which no hook enforces either.
- **No `seal/config.md` in this repository.** Absent means the default and
  the default is English, so a file restating it is a file nobody needs
  (`questions.md` Q1).
- **The twelve existing `pr.ko.md` files are not renamed.** Under the new
  rule the name is the mirror's own language, and this repository's pull
  request language is English, so `pr.ko.md` is what those files should be
  called (`questions.md` Q2).
- **No row but the first.** The table is open for more items later; adding a
  second one now would be inventing a question nobody asked.
- **`docs/` gains nothing.** Issue #82 says so itself: *"Not in
  docs/one-root-by-lifetime.md (PR #77…); recorded here."*

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 · the row is what the skill reads | Given a repository with `seal/config.md` whose `Pull request language` row says Korean · when a session loads `commit-pr-convention` before a commit · then it writes the commit subject and body and the pull request title and body in Korean | the skill names the path, the row and what the row governs; a case asserts each of the five surfaces stopped saying English |
| S2 · absent fails toward today | Given no `seal/config.md`, or one with no such row · then the language is English, exactly as before this work | the skill states the default in the same paragraph as the path; a case asserts both halves of the sentence |
| S3 · the root is resolved, never spelled | Given a local-mode repository, whose root is under the common git directory · when the skill sends a session to read the config · then it is sent to the resolved root, not to a literal `<repo>/seal/config.md` | a case asserts the skill carries the two-place sentence |
| S4 · the prefix vocabulary is not translated | Given a Korean repository · when a commit is written · then the subject is `feat: <Korean>`, not `기능: <Korean>` | the skill excludes the prefix in so many words; a case asserts the exclusion is present |
| S5 · branch names stay ASCII | Given the same repository · when a branch is named · then it is still `<prefix>/<kebab-case-slug>` in ASCII | the skill excludes branch names; a case asserts it |
| S6 · the response language stays out | Given the same repository · when someone looks for where to set the language the session ANSWERS in · then the config file says it is not here and points at the person's own configuration | the template says it; a case asserts the template and the skill both say it |
| S7 · the mirror is named for its own language | Given a repository whose pull request language is Korean · when a translated body is wanted · then it is `pr.en.md`; in an English repository it is `pr.ko.md`, which is what the twelve files here already are | the skill gives both directions with the `pr.<lang>.md` rule; a case asserts the rule and both examples |
| S8 · the file is machine-readable in the shape already used | Given `templates/config.md` · when a reader parses it the way `parity.md` is parsed · then it yields one `Item → Value` mapping whose first key is `Pull request language` and whose value is `English` | a case parses the template's table and asserts the first row |
| S9 · a new permanent file in the root is listed where the root is described | Given `templates/seal-README.md`, `seal/README.md`, `README.md`, `README.ko.md` · then each names `config.md` in its layout | a case per file; `seal/README.md` must stay the template verbatim, which `tests/test_first_setup_asks_once.py` already pins |

## Data & interfaces

`seal/config.md`, at the resolved root:

```markdown
| Item | Value |
|---|---|
| Pull request language | English |
```

The value is a language's English NAME (`English`, `Korean`, `Japanese`),
not a code. A name needs no lookup table, and the reader is a model, which
does not have one to consult. Nothing in `hooks/` reads this file, so no
resolver function is added to `hooks/optin.py`: `parity_config()` exists
because three gates call it, and a function with no caller is a claim that
something reads the file.

## Open questions → questions.md

Q1 (is the file created at setup), Q2 (the mirror's name), Q3 (whether
anything but the skill enforces it).
