---
name: commit-pr-convention
description: |
  Format rules for commit messages, PR titles, PR bodies and branch names —
  the prefix vocabulary, the language the repository states in `seal/config.md`,
  where a translated body lives, and how to check a title against the
  repository's own history.
  Use when: writing a commit message, opening a pull request, naming a
  branch, or titling either.
  NOT for: the prose and structure of a PR body or review comment
  (writing-style), code comments and docstrings, a project's response
  language.
---

# commit-pr-convention — commit, PR and branch format

`writing-style` declares `NOT for: … branch/commit format` and hands the
question here. This is where it lands.

The split is worth stating once, because both skills are about writing.
`writing-style` governs what a PR body **says** and how it is built. This one
governs the **envelope**: the prefix, the title's shape, the branch name, and
where a translation lives. A body can satisfy one and violate the other.

## First — check your title against the history

```
gh pr list --state all --limit 10
```

**The history is the rule even where no document states it.** Everything below
was read off a repository's log, and repositories differ. When your title does
not look like the ones in that list, yours is the one that is wrong.

This step is first because the failure happens here. In one session the prefix
rule and the language rule were each broken once, and **both times the list
was already on screen.** Having run the command is not the same act as
comparing your own title to what it returned. Do the comparison out loud, in
one line, before you open anything.

**An empty list is an answer, not a blocker.** A repository with no pull
requests yet has no history to outrank anything, so the table in the next
section is what you use, unchanged, and the first title you write becomes the
history the next one is compared against.

## The language is the repository's, and it says so in a file

**Read `config.md` in the root before writing any of the four things below.**
The root is `<repo>/seal/` where that directory exists and
`$(git rev-parse --git-common-dir)/seal/` otherwise, which is where local
mode keeps it — resolve it that way rather than spelling the first place and
stopping.

```markdown
| Item | Value |
|---|---|
| Pull request language | Korean |
```

That row governs the **commit subject and body** and the **pull request title
and body** — all four, because a squash makes them one text.

**Every way of not naming a language lands on English**, which is what every
repository got before the row existed. There are four of them and they are
one rule: no file, no such row, an empty value, and a file that cannot be
read or does not parse as that table. A config nobody can read must not stop
a commit, so a session meeting any of these writes English and carries on
rather than asking.

**To create it, copy `templates/config.md` from this plugin into the root and
edit the row you mean.** It ships more than one. The mode's row is written
by `seal mode` from where the folder is, and edited by hand only to ask for
a move — `seal mode --apply` then moves the folder to what you wrote. That
file repeats the exclusions below, because the person who writes a
repository's config reads it and never reads this one.

It governs nothing else, and the three exclusions are what make it safe to
change:

- **The prefix vocabulary is not translated.** `feat:`, `fix:`, `docs:` stay
  as they are in every repository. They are scanned in a log and parsed by
  tooling, and `기능:` teaches neither.
- **Branch names stay ASCII** — `<prefix>/<kebab-case-slug>` — because a
  branch name is typed into a shell and pasted into a URL.
- **The response language is not in that file.** What the session says to
  you is a person's setting and lives in the user's own configuration. Two
  people in one repository can want different answers there and the same one
  here.

This file used to require English of everyone, which was one user's
convention promoted to a rule for all of them. A repository whose team writes
another language now says so in one row; one that says nothing is unaffected.

## Commit messages

`<prefix>: <one line, starting lower-case>`, in the repository's language.
The prefix is not part of that — it stays as the table below spells it.

| prefix | when |
|---|---|
| `feat:` | behaviour that did not exist now does |
| `fix:` | behaviour existed, was wrong, and is corrected |
| `docs:` | documentation or comments only |
| `test:` | tests only |
| `refactor:` | same behaviour, different structure |
| `perf:` | same behaviour, faster |
| `chore:` | release preparation, configuration, dependencies |

This table is the working default and it is what a repository with no history
gets — a first commit has nothing to compare against, and a skill that only
said "follow the log" would have nothing to offer there.

**A repository's own log outranks the table.** Where it uses a prefix of its
own for its workflow, use that one too; where it spells a shared one
differently, follow it. Do not invent one — a prefix nobody has used before
teaches a reader nothing, and the log is how they learn what it means.

**One language, in the subject and in the body — the one the row names.**
Where feature branches squash, the commit body becomes the pull request body,
so the two cannot be in different languages without one of them being wrong
at the merge. That is why one row answers for all four surfaces rather than
one row each.

## Pull request titles

**The same prefix vocabulary as the commits, and the same language.**

```
good  fix: the commit gate has three ways out and its prompt named two
bad   The commit gate has three ways out and its prompt named two   ← no prefix
bad   fix: improve gate messaging                                    ← a category
```

**A title states the symptom, not the technique or the category.** Someone
reading only the list of titles should learn what happened. `writing-style`
carries this at length; this file carries the prefix in front of it.

## Pull request bodies

**The language the row names.** The prose and structure rules are
`writing-style`'s, and it is read **before** writing, not after — structure
that came out wrong is not recovered by fixing sentences.

Where a translated body is wanted, **put it in the repository as a file and
link it from the body.**

- **Where** — the work item's own folder under the root, as `pr.<lang>.md`,
  and `<lang>` is the mirror's **own** language rather than the body's. An
  English repository keeps a Korean mirror at
  `<root>/specs/<work-item-id>/pr.ko.md`; a Korean one keeps an English
  mirror at `pr.en.md`. Resolve `<root>` the way the language section above
  resolves it, and read the next bullet before you write there.
- **Why there** — its permissions are the repository's, so anyone who can
  read the pull request can open it; it is versioned with the code; and it
  survives the merge.
- **So not under the git directory.** Where the root resolves to
  `$(git rev-parse --git-common-dir)/seal/`, nothing under it is ever a
  commit candidate, which takes away all three reasons above at once: a
  reviewer cannot open it, no version of it exists, and the merge carries
  nothing. Put the mirror beside the documents the pull request already
  touches instead — the same place a repository with no work-item structure
  puts it.
- **Not a hosted document or artifact.** One was tried and failed three ways
  at once: default-private, so the link in a public pull request opened for
  nobody but its author; kept alive only by a manual share each time; and
  living outside the repository, so the merge left it behind.

**A translation keeps the terms the repository invented.** Render the prose,
not the vocabulary: a coined term stays in its original spelling and is
unpacked once, at first use. `writing-style` has the reasoning and the
incident.

## Branch names

`<prefix>/<kebab-case-slug>`, the same prefix vocabulary as the commits, and
**ASCII whatever the repository's language is.** The row does not reach here:
a branch name is typed into a shell and pasted into a URL.

```
fix/the-way-out-the-gate-does-not-name
docs/the-merge-rule-is-enforced-now
perf/403-repositories-built-one-git-call-at-a-time
```

**The slug states the symptom too.** A name carrying only a ticket number
(`fix/issue-88`) tells a reader nothing in a list of branches, which is the
one place branch names are ever read.

## Before you open it

Answer these, rather than assuming them.

1. Did you run `gh pr list` **and compare your title to what it returned**?
2. Does the title carry a prefix, from the vocabulary the commits used?
3. Did you **open `config.md` in the root** — and are the title and body in
   the language its `Pull request language` row names? No file and no such
   row both mean English.
4. If there is a translation, is it a file in the repository — not a hosted
   document — and is it named for its own language?
5. Does the title alone say what happened?
