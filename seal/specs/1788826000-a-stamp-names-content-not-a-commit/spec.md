# 1788826000-a-stamp-names-content-not-a-commit — spec

## Why this exists

A `# RIDER:` comment carries a `Verified <date> at <sha>` line, and
`tests/test_a_rider_reaches_its_file.py#test_every_rider_stamp_names_a_commit_this_branch_can_reach`
requires that SHA to be an ancestor of HEAD.

The repository's merge rule squashes a feature branch into its release branch.
A fix pass runs on a feature branch, so the only commits it has to name are
that branch's, and the squash destroys exactly those. The check then fails on
the **release branch**, so whoever repairs it is never whoever caused it, and
every pull request into the release branch fails until they do. **No mistake is
required.**

The direction was decided already, and the riders are the evidence it was
decided on. `skills/evidence-check/SKILL.md` cites the riders' orphaned SHAs as
one of the four grounds for deriving a ledger anchor from content, and
`CLAUDE.md` states the rule that came out of it — *a row carries no line number
and no commit SHA*. This work item is the migration that decision never got.

## Scope

**In.** Every rider stamp in the tree moves from naming a commit to naming
content. The check that guarded the old form is replaced by one that guards the
new form, and it is seen red against the unmigrated corpus first. A `--reverify`
path exists so re-stamping is a command rather than a hand-computed hash.

**Out.** `Target SHA` in round records — answered below, and the answer is that
it stays. The rider convention itself: what a rider is, where it lives, and that
`grep -rn "RIDER:"` is the list, are unchanged.

## The corpus, re-derived

The handoff said 13 stamps across 10 files. Measured on this branch at
`3292e43`, that is false in both numbers, and the file list it gave sums to 15
rather than 13.

Executed — a walk of the whole tree splitting on `# RIDER:` and matching
`Verified \d{4}-\d{2}-\d{2} at ([0-9a-f]{7,40})`:

| Where | Riders with a canonical stamp |
|---|---|
| under the roots the test scans (`hooks`, `skills`, `agents`, `templates`) | **17**, across 12 files |
| `.github/scripts/fold_ledger.py` | 1 |
| `tests/test_the_printed_ledger_name_is_the_file_that_was_read.py` | 1 |
| **real riders in the tree** | **19**, across 14 files |
| quoted inside a round record (`seal/specs/1788184145-…/rounds/round-2.md`) | 1 — a record, not a rider |

Per file: `hooks/cmdline.py` 2 · `hooks/worktree-guard.py` 3 ·
`skills/code-review/scripts/round_record.py` 3 · `agents/smith.md`,
`hooks/dispatch.py`, `hooks/optin.py`, `hooks/review-history-guard.py`,
`hooks/review-skill-gate.py`, `hooks/root-migrate.py`,
`skills/evidence-check/scripts/evidence_check.py`, `skills/implement/SKILL.md`,
`templates/evidence-check.yml`, `.github/scripts/fold_ledger.py`,
`tests/test_the_printed_ledger_name_is_the_file_that_was_read.py` 1 each.

**Two more instances of the same class surfaced while counting**, and §12 of the
contract makes them this change's:

1. **The enforced corpus is smaller than the corpus that exists.**
   `RIDER_ROOTS = ["hooks", "skills", "agents", "templates"]` never sees
   `.github/scripts/fold_ledger.py` or the two riders under `tests/`. Three
   riders are guarded by nothing at all — the same shape as the `templates`
   root having been missing until someone noticed.
2. **A rider with a non-canonical stamp is invisible.**
   `tests/test_the_records_can_be_carried_out_and_in.py:1415` is a real rider
   whose staleness line reads *"green at 3f8f846, measured 2026-09-03"*. It
   matches no stamp pattern, sits outside the scanned roots, and is therefore
   held to nothing.

## Question 1 — what a rider stamp names instead

### The form

```
Verified <YYYY-MM-DD> against <anchor>@<hash>
```

`<anchor>` is the ledger's own anchor vocabulary, resolved by
`evidence_check.resolve_unit` against the rider's **own file**: a dotted Python
symbol name, a markdown heading path, or a quoted distinctive line. `<hash>` is
`evidence_check.content_hash` of the anchored region.

**The path is left off, and that is the one place this departs from the ledger's
`path#major@hash`.** A ledger row is not in the file it cites, so it needs the
path. A rider *is* the coordinate — `seal/follow-up.md` puts it there precisely
so it arrives at whoever opens the file — so writing the path would restate a
fact the comment's own location already carries, and a rename would then need
two edits for one move.

### The residual, and how it is resolved

A rider is a comment inside the file it is about, so its own text is part of
that file's content. If the hash covered the rider, the hash would be written
into the region it hashes and no fixed point would exist.

**Measured, not assumed: 12 of the 19 riders sit inside the AST span of the unit
they are about.** `fold_ledger.demote`, `cmdline._git_options`,
`cmdline.parse_git`, `dispatch.run_gate`, `optin.repo_root`,
`review-skill-gate.already_asked`, `worktree-guard._tokenize_with_separators`,
`worktree-guard.main`, `round_record.swallowed`, `round_record.fix_table`,
`evidence_check.unread_items`, and one in
`tests/test_the_printed_ledger_name_is_the_file_that_was_read.py`. This is the
dominant case, not a corner.

**The resolution: every rider block in the region is removed before the region
is hashed.** Not merely this rider's — all of them.

Three properties, and the second and third are why the rule is *every* block
rather than *this* block:

- the stamp sits inside a rider block, so it is excluded, so the hash does not
  cover itself and the fixed point exists;
- **editing a rider's own prose does not drift it.** A rider's wording is not
  what it verified. Clarifying the sentence would otherwise report that the code
  changed, which is false;
- **planting a second rider in a unit does not drift the first.** Three files
  already carry more than one rider, and a design where riders perturb each
  other gets worse as the convention is used.

What that gives up, stated rather than left to be found: a change consisting
only of adding or removing a comment inside the unit goes unnoticed. For
`# RIDER:` blocks specifically that is the intent; for an ordinary comment
adjacent to a rider it is over-exclusion, because a block is read as the run of
comment lines starting at the `RIDER:` line, and an unrelated comment butted
against one is absorbed. The failure is conservative — fewer alarms, never a
false one.

### The rejected alternative, and why

**Move riders outside the unit they are about.** Then the AST span excludes the
comment and nothing needs removing. Rejected: `evidence_check.py`'s rider is
about one `except OSError` inside a 43-line function and `worktree-guard.py`'s
is about one `if tool in ("Agent", "Task")` inside a 335-line `main`. Hoisting
either to the top of its function is the rider arriving somewhere other than at
its coordinate, which is the whole of a rider's value.

**Widen `normalise()` to drop rider lines.** Rejected: `normalise` is shared
with every ledger row, so the change would move hashes for units that carry a
rider and reach a file vendored into other repositories' CI. The rider region is
a rider-local reading and is computed rider-locally.

### The degradation

| State | Verdict | What it tells the reader |
|---|---|---|
| anchor resolves once, hash matches | OK | the claim is measured against the code as it stands |
| anchor resolves once, hash differs | **DRIFTED** | the unit changed — re-read the rider, then re-stamp |
| anchor absent, ambiguous, or resurrected | **BROKEN** | the rider's subject is gone — re-anchor it or delete the rider |

The ledger's DRIFTED-not-BROKEN degradation is right here, and for a sharper
reason than that it is right there. A drifted rider is *the rider firing*: it
says somebody edited the unit and did not answer the comment sitting in it,
which is the arrival `seal/follow-up.md` moved riders to their coordinates to
get. BROKEN stays reserved for the one case where re-reading cannot help,
because the subject no longer exists.

**Drift fails the check rather than warning.** The ticket's own bound requires
it — *whatever replaces the SHA must be checkable the same way* — and
`evidence_check` already exits 1 on drift, so a softer rider would be the
looser of two rules about the same thing. The cost is bounded in a way the old
form's was not: answering a drifted rider is re-reading a comment in the file
you just edited and running one command, where answering an orphaned SHA was
bookkeeping with no reading in it at all.

**Resurrection is refused outright, where the ledger tolerates it.** A
resurrected place is a candidate the keyword blocklist dropped and the
declaration rule put back, and `evidence_check` carries that uncertainty out to
its caller. The ledger tolerates it because its rows were bulk-migrated from
line numbers. A rider is hand-written by somebody standing at the coordinate,
who can pick a better anchor, so a resurrected place is BROKEN here.

## Question 2 — `Target SHA` moves or stays

**It stays, it is exempt, and `templates/sdd-round.md` says why.**

Three grounds, in the order that decides it:

1. **A round record's SHA already has a squash-survivable resolution path, and
   a rider's did not.** Executed by reading `chain_check.py#reachable`: after
   `HEAD` and the declared branch, it falls back to
   `carried_by_a_pull_head`, which scans `refs/pull/<N>/head`. Nothing but a
   pull request writes that namespace and a squash does not touch it, so the
   commit a feature branch's round reviewed stays reachable there. The rider
   test has one call, `git merge-base --is-ancestor <sha> HEAD`, and no
   fallback. The two mechanisms are not the same mechanism with a different
   corpus; only one of them was ever built to survive the merge rule.

2. **They are different objects.** A `Target SHA` records a moment — *this
   round reviewed this tree*. A rider stamp is a live pointer — *the claim
   below is measured against the state under it*. `skills/implement/SKILL.md`
   turns that difference into the reason round records may live beside the
   contract at all: *a round record carries the SHA it reviewed, so it never
   asserts a present state*. Re-anchoring it to content would make it assert
   one, which is the property being relied on, removed.

3. **Content anchoring cannot express what the row means.** The reviewed tree
   is a whole commit across every file, not a region of one. There is no
   anchor to write, so the migration is not merely unnecessary here — it has no
   target.

The third cause the ticket lists — a `feature → release` squash — therefore
reaches the two mechanisms differently: it orphans a rider stamp outright and
leaves a `Target SHA` resolvable through the pull-request namespace. That
asymmetry is the answer, and it is written into the template so the next person
who notices 135 records carrying a SHA does not re-open it.

## Acceptance

1. `grep -rn "Verified [0-9-]* at [0-9a-f]"` returns nothing anywhere a rider
   lives. Every one of the 19 carries the new form.
2. A checker resolves every rider anchor and reproduces every hash, and it is
   **seen red against the unmigrated corpus** before the corpus moves.
3. The scanned corpus covers every rider in the tree, including the three that
   nothing guarded, and a rider whose staleness line matches no stamp form is
   refused rather than skipped.
4. Re-stamping is one command. No hash is written by hand.
5. `templates/sdd-round.md` states the `Target SHA` exemption and its grounds.
6. No rider planted by this change names a commit from this branch.

## User scenarios

- **A fix pass squashes into the release branch.** Nothing about a rider
  changes, because no rider names a commit. The check that used to go red on
  the release branch has nothing to go red about.
- **Somebody edits a unit carrying a rider.** The check goes red naming that
  rider. They read it — which is what it was planted for — then either fix what
  it asks and delete it, or re-stamp with one command.
- **Somebody deletes the unit a rider is about.** The check goes red as BROKEN,
  saying the subject is gone. The rider goes with it.
