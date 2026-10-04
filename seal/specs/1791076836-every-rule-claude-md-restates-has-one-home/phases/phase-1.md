# 1791076836-every-rule-claude-md-restates-has-one-home — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 9e2dbbdf |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

Give the three rules `CLAUDE.md` restates one home each. Its merge,
identifiers and commit rows become link rows in spec D2's shape (path and
section, the trigger, one act sentence), the commit row applying
`skills/implement/SKILL.md` §2 rather than restating it (D3). The goal
section's batch sentence folds into its §1 link (Scope 4). `CONTRIBUTING.md`'s
*No real identifiers* bullet gains the history-rewrite reason. The four code
comments from Scope 2 cite `CONTRIBUTING.md` §*House rules*. Add the sibling
pin module (D4) with needles taken from the homes as they stand after the
edit, two per rule (Q2). The generated block stays untouched, and the
*Commit freely* paragraph and the fragment row stay word for word.

## What this phase found

**The base had not moved.** `origin/release/v0.18.1` was `e141980a` at the
start of the build, so there was nothing to merge in before phase 1.

**The module pins four rules, not three.** The goal section's batch sentence
is a fourth row of `RULES` (`batch`, home `skills/implement/SKILL.md`
§*1. Read the spec before the code*), so S4 is executed rather than read.
Its needles are not the sentence the old `CLAUDE.md` paraphrased (*The cost
of a question is not its difficulty, it is when it arrives*), because
`CONTRIBUTING.md` §*What a change to a gate must carry* quotes that clause
as the reasoning behind its prompt budget. That quotation is an application
and stays; the needles are two other sentences only §1 writes.

**`LINKED` holds the four code comments too.** Each must name
`CONTRIBUTING.md` and `House rules`, so S5 is held by the module and not
only by a grep. S5's grep, `git grep -n 'CLAUDE.md. §\*no real
identifiers'`, is empty outside `seal/`. Inside it, it matches the
Grounding table of work item `1790993139`'s `spec.md`, a record of what that
work read at its time. Records are not rewritten, so that hit stays.

**A home is a carrier of the other rules.** `CONTRIBUTING.md`,
`docs/branch-and-release.md` and `skills/implement/SKILL.md` are each a home
and each a carrier, so `restated` skips only the rule's own home rather than
leaving the homes out of `CARRIERS`, as #715's module could.

**`section` reads a heading at any level** and stops at the next heading of
the same level or above. Two of the homes are `###` sections and #715's
reader split on `## ` only.

**Seen red (§15), executed.**
- Against the base tree's files, through a scratch script fed by
  `git show e141980a:<file>`: the link half named all eight linked files and
  the needle half found nothing. The old copies were in fresh words, which is
  spec D5's 1-of-3 finding seen from this side.
- `mutation-check` on the tree: the old table's row planted into `CLAUDE.md`
  red; `§*House rules*` replaced in `CLAUDE.md` red; the old citation put
  back in `.github/scripts/plugin_directory_check.py` red.
- `mutation-check` on the module's own units: the home skip removed red; the
  heading half of the link check removed survived, and so did the section's
  stop at its sibling. `test_a_removed_link_is_named` gained a heading-only
  case and `test_a_section_stops_at_its_sibling` was added; both breaks then
  went red, as did the heading match replaced by the file's first heading.

**Narrow runs, executed.** The seven modules the plan names gave 99 passed;
`python3 .github/scripts/claude_block.py --check` exited 0. The 37 modules
that read `CLAUDE.md` or `CONTRIBUTING.md`, with the hygiene set, gave 1988
passed and 1 failed: this work item had no `overview.md` yet, which
`test_every_spec_directory_that_reached_the_ladder_has_an_overview` requires.
It is opened in the commit that carries this record.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `CLAUDE.md`'s merge table, the rider-stamp incident and the ruleset paragraph | `docs/branch-and-release.md` §*Work accumulates on a release branch*, which already held the fuller table, the correct stamp history and the rulesets' effect |
| `CLAUDE.md`'s identifiers paragraph, with its history-rewrite reason | `CONTRIBUTING.md` §*House rules*, *No real identifiers*, which now carries the reason |
| `CLAUDE.md`'s commit-cadence reasoning and the worktree-guard paragraph | `skills/implement/SKILL.md` §*2. Implement, and feed evidence back where you verified it*, which already held both |
| `CLAUDE.md`'s goal-section batch sentence | `skills/implement/SKILL.md` §*1. Read the spec before the code* |
