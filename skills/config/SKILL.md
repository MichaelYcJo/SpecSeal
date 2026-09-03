---
name: config
description: Show what this repository decided for itself and change any of it — the languages it writes in, and where its records live. Reads seal/config.md, and routes a change to whatever owns that row.
disable-model-invocation: true
---

# /specseal:config — what this repository decided, and how to decide otherwise

`seal/config.md` holds what a repository says about itself. Every row has a
default, an absent row is not an error, and until now the only way to see any
of it was to open a file nobody has a reason to open.

First setup asks its questions once and never again. This is how to ask them
later.

## Where the file is

`<repo>/seal/config.md` where that directory exists, and
`$(git rev-parse --git-common-dir)/seal/config.md` otherwise — local mode,
where the root sits under the common git directory. Resolve it that way rather
than spelling the first place and stopping.

**No root at either place** means this repository has not been set up. Say so,
name the `implement` skill's bootstrap as what does it, and stop. Do not
create the file: its presence at one of those two places is what opts a
repository in, and creating it here would opt somebody in from a command they
ran to look.

## Procedure

**1. Show every row, present or not.** Read the file, and print all three with
their current values — including the ones the file does not carry, with the
default and where it comes from. A row a repository never set is the most
likely one somebody wants to change, and showing only what is present hides
exactly those.

| Row | Default | What it governs |
|---|---|---|
| `Commit and pull request language` | English | the commit subject and body, the pull request title and body, and a review report posted as a pull-request comment |
| `Record language` | English | the prose in `spec.md`, `plan.md`, `overview.md`, `questions.md`, `changelog.md`, a round record's cells, and a ledger row's claim and grounds |
| `Mode` | *the folder decides* | which of the two places the root should live at |

**Every way of not naming a language lands on English** — no file, no such
row, an empty value, a file that does not parse. Say the default and the
reason rather than showing a blank.

**2. For the mode, show what is true as well as what is written.** That row is
what the repository *wants*; the folder's location is what it *has*, and the
two are separate on purpose. Run `seal mode` and report what it says — the
folder, the row, and whether they agree. Do not read the row yourself for this
one: `seal mode` is what the pull-request checks run, and a second reader is a
second answer.

**3. Take a change, and route it.**

- **A language row** is only a row. Edit the value in place, leaving the rest
  of the file as it is. If the file does not exist, copy
  `$CLAUDE_PLUGIN_ROOT/templates/config.md` into the root first and edit that
  — it carries every row's documentation, which is the half a person reads.
- **The mode row moves files.** Run `seal mode local` or `seal mode shared`.
  It moves the root, stages the change, carries
  `.github/workflows/hygiene.yml` in or out, and writes the row, so the file
  and the folder agree afterwards. Do not do any of that by hand.

**4. Say what happened beyond the row.** A language row changes a row. The
mode row moves a directory, stages a commit and installs or removes a
workflow file, and the person needs to see that list rather than *done*.

## Before switching to shared, say what cannot be undone

Going to shared puts the records in the tree. **The commit is the point of no
return, not the move**: afterwards they are in the history, and taking them
out of the tree later does not take them out of it. Until that commit,
`git reset -- :/seal :/.github/workflows/hygiene.yml` and then
`seal mode local` walk the whole thing back.

Say it before running the command, not after. Local mode exists for the
repository whose tree must not carry this plugin's files, and shared is the
direction that cannot be walked back.

Going the other way costs something different and it is not a secret either:
every other clone loses the records at the next pull. `seal export` here and
`seal import` there is how a teammate gets a copy.

## What this does not do

- **It does not define a schema.** It reads the rows that are there and routes
  them. A generic setter would be a parser for a file people edit by hand, and
  would invite a short document to drift into key-value settings.
- **It does not start over.** Discarding the records means discarding the
  evidence chain every gate here reads. That stays a deliberate act done by
  hand, and `seal export` first is the order.
- **It does not replace the file.** A person can still open `config.md` and
  edit it. This is a door to the room, not a gate in front of it.
