# 1790076070-the-fold-ships-and-the-corpus-is-still-on-disk — phase 7

| Field | Value |
|---|---|
| Phase | 7 |
| Commit | 19b7959b |
| Ran by | smith on claude-opus-5[1m] |

## What this phase was asked

`docs/branch-and-release.md`, `docs/release-checklist.md` and
`docs/issues-and-milestones.md` — the release, the tickets, the rolling log.
Fifteen items across eight segments plus the ungrouped `1788735085`.
Verified as phase 3.

## What this phase found

### Nine of fifteen had a sentence waiting

| Item | Marked on |
|---|---|
| `1789172128` | issues §*A milestone answers when, and takes three shapes* |
| `1788486395`, `1788661274` | issues §*`flow-measurement` is a label that is not an index* |
| `1788844200` | issues §*A rolling log is titled after the version it rolled from* |
| `1789108681` | issues §*A label says a ticket is already in, before the release ships* |
| `1788844400` | issues §*A keyword claims the one number after it* |
| `1788326734` | checklist §2 *Gather, fold, bump* |
| `1789687448` | checklist §3, the paragraph about git listing files the disk does not have |
| `1788826000` | branch-and-release, the sentence naming the rider stamp |
| `1788302682` | branch-and-release, the sentence naming what ships |

`1788486395` and `1788661274` are two work items refining one invariant —
what the roll fires on, and what the issue it opens carries — so they take
one anchor, the paragraph that states the invariant.

### Two destinations moved, and both moved for the same reason

**`1788360817` and `1788420760` went to `docs/one-root-by-lifetime.md`, not
to `docs/branch-and-release.md`.** The plan sends the
`skills/commit-pr-convention/SKILL.md` segment to branch-and-release, which
is right about the subject those items look like — commit and pull request
language. But what they established is a pair of **`seal/config.md` rows**,
and phase 6 put the standing statement about that file, its rows, and what an
absent row means into `one-root-by-lifetime.md`.

Splitting it would have left a reader asking *what does this repository
decide for itself* two documents to check, with no rule saying which. This
repository's own rule is that a thing more than one party can have is named
with whose; the same instinct applies to a subject that could live in two
documents. So the config rows live where the config file does.

`plan.md` reserves exactly this: a destination may be wrong, and the phase
that reads the specs is what finds out. No new file was created and no area
gained a second document, which are the two things that would have needed
the plan reopened.

### Four needed prose, and one of them is a rule about ranges

`1788890000` is the one worth naming. Its standing statement — the survivor
check's unit is a **fix pass's range**, and a release pull request is a range
no fix pass ever writes — is directly about the check phase 11 of this very
work item has to satisfy. It landed in the checklist under a heading of its
own, *What a release pull request is not the right range for*, because a
reader meeting the check at a release needs it there rather than in a review
document.

The other three: the version-naming timer (`1788735085`, ungrouped, folded
here because the checklist's own table already names the case it wrote), the
contributor's base branch (`1789919879`), and the reload an update notice
costs (`1788789330`, under §6 where a person is told an update landed).

### `1788890000` has no `spec.md`, and its changelog fragment is the source

It is one of the two items in the retire set below the SDD ladder. Its
`changelog.md` states the rule in full, in the form a reader acts on, so
nothing was guessed. Recorded because *no `spec.md`* is the condition
`spec.md`'s own ungrouped rule uses to **keep** a directory — and it is not
the condition here, since this one carries a ledger row and a segment. The
two rules are about different questions.

### What was dropped rather than folded

**`1788360817`'s five coordinates** — the exact lines in the skill that said
English. Which lines changed is the commit; that the language is the
repository's answer is the rule.

**`1788844200`'s `#98` rider** — three places saying `-z` alone turns git's
path quoting off. True, narrow, and about a git flag rather than about
releases; it lives in the comments it corrected.

**`1789919879`'s surface table (S1–S6).** A list of six files one branch
touched. The rule is the sentence the table exists to produce.

**`1788302682`'s root list.** *Six roots* was true at that commit and is a
count, not a rule; the sentence in `branch-and-release.md` carries the list
and the marker sits on it, so the list stays where it can be kept true.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| nothing from the tree — prose and markers only | none |
