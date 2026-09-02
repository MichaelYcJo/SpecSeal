---
name: commit-pr-convention
description: |
  Format rules for commit messages, PR titles, PR bodies and branch names —
  the prefix vocabulary, where a translated body lives, and how to check a
  title against the repository's own history.
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

## Commit messages

`<prefix>: <one line, starting lower-case>`, English.

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

**English, in the subject and in the body.** Where feature branches squash,
the commit body becomes the pull request body, so the two cannot be in
different languages without one of them being wrong at the merge.

## Pull request titles

**The same prefix vocabulary as the commits, and English.**

```
good  fix: the commit gate has three ways out and its prompt named two
bad   The commit gate has three ways out and its prompt named two   ← no prefix
bad   fix: improve gate messaging                                    ← a category
```

**A title states the symptom, not the technique or the category.** Someone
reading only the list of titles should learn what happened. `writing-style`
carries this at length; this file carries the prefix in front of it.

## Pull request bodies

**English.** The prose and structure rules are `writing-style`'s, and it is
read **before** writing, not after — structure that came out wrong is not
recovered by fixing sentences.

Where a translated body is wanted, **put it in the repository as a file and
link it from the body.**

- **Where** — the work item's own folder, as `pr.ko.md` (for example,
  `seal/specs/<work-item-id>/pr.ko.md`). Where a repository has no such structure,
  put it beside the documents the pull request already touches.
- **Why there** — its permissions are the repository's, so anyone who can
  read the pull request can open it; it is versioned with the code; and it
  survives the merge.
- **Not a hosted document or artifact.** One was tried and failed three ways
  at once: default-private, so the link in a public pull request opened for
  nobody but its author; kept alive only by a manual share each time; and
  living outside the repository, so the merge left it behind.

**A translation keeps the terms the repository invented.** Render the prose,
not the vocabulary: a coined term stays in its original spelling and is
unpacked once, at first use. `writing-style` has the reasoning and the
incident.

## Branch names

`<prefix>/<kebab-case-slug>`, the same prefix vocabulary as the commits.

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
3. Are the title and body English?
4. If there is a translation, is it a file in the repository — not a hosted
   document?
5. Does the title alone say what happened?
