# Feature Specification: every rule CLAUDE.md restates has one home (#730)

<!-- seal/specs/<unix-epoch-seconds>-<slug>/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

#730 is F4 of `docs/the-record-layout.md` §*What is decided and not built yet*.
It has two boxes. First, the three rules `CLAUDE.md` restates each get one home,
and the other files link to it. Second, a method that finds restated rules
across the repository, and the method's result.

`Record language` is absent from `seal/config.md`, so this file is English.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `docs/the-record-layout.md` (lead, lines 8–11): *A file that states a rule this index gives another home links to that home and does not restate it … Where a copy is found, the copy is the defect.* | The rule this work applies. Each restated rule keeps one home, and every other carrier links to it. |
| `docs/the-record-layout.md` §*The root records*: `CLAUDE.md` holds *the rules a session in this repository must hold, each linking to its home* | `CLAUDE.md` keeps a row for each rule a session must hold, and the row links. Removing a row is not on offer. |
| `docs/the-record-layout.md` §*What is decided and not built yet*, F4 | This work's scope: *the merge-direction table, no real identifiers, the commit cadence, and every restated rule outside `CLAUDE.md` and `CONTRIBUTING.md`*. The F4 row is the only part of that document this work edits (D8). |
| `CLAUDE.md` §*Repo rule — a thing more than one party can have is named with whose* | The precedent for a link row: *`<home>` states this rule and holds the reasoning; this row is the link, and it is here because a session … has no other reason to open that file.* D2 generalises it. |
| `tests/test_the_ledger_rules_have_one_home.py` (#715) | The precedent for pinning a moved rule. It uses needles only the home writes, which no carrier may contain, and a link check of path plus section. Its `LINKED["CLAUDE.md"]` needs `CLAUDE.md` to keep naming three `docs/the-evidence-ledger.md` sections and one `docs/the-record-layout.md` section. The commit-cadence row carries three of the four, so the rewrite must keep them. |
| `tests/test_a_moved_rule_leaves_its_definition.py` docstring | The precedent for detecting text that was copied. It matches verbatim, uses `WINDOW = 15` words, and measured the margin between the longest kept application (10 words) and the smallest real copy (25 words). It also explains why it does not try to catch a paraphrase: no constant can separate a paraphrase from an application. D5 and D6 rest on both points. |
| `tests/test_the_claude_md_block_has_one_source.py`, and #292's owner answer Q1 | `CLAUDE.md`'s generated region is a copy that is checked against `templates/claude-md-block.md`. It is a sanctioned copy and is out of scope (O1). |
| `skills/implement/SKILL.md` §2, *Commit at the smallest step that stands on its own* | The commit-cadence rule and its two conditions: squash, and a declaration. It also says *read both off the repository before leaning on them*. That is the part the `CLAUDE.md` row carries for this repository (D3). |
| `docs/review-chain-spec.md` §*Where a leftover goes — the ladder, and why a new issue is not the default*; #223 | A new issue is not the default home for a leftover. The method's large result becomes one issue, cut by cluster, and does not become one issue per pair (D7). |
| `agent-contract` §12, §15 | Enumerate the class by construction, not by example. A new case is not planted until it has been seen red. |

## Scope

**In:**

1. **The merge method per direction.** The home is `docs/branch-and-release.md` §*Work accumulates on a release branch*, which holds the *Which button, for each direction* table. `CLAUDE.md` §*Repo rule — the merge method is fixed per direction…* becomes a link row in D2's shape. It drops the table, the incident and the ruleset paragraph, because the home holds all three. The home itself does not change.
2. **No real identifiers.** The home is `CONTRIBUTING.md` §*House rules*, in the bullet *No real identifiers*. `CLAUDE.md` §*Repo rule — no real identifiers in examples or fixtures* becomes a link row. One sentence moves into the home: the reason the rule is held hard (*both incidents that forced a history rewrite entered this way*). Four code comments currently cite `CLAUDE.md` for this rule. They are repointed to the home:
   - `.github/scripts/plugin_directory_check.py`, the comment above `DIRECTORIES`
   - `tests/test_the_plugin_directory_answers_the_box.py`, module docstring
   - `tests/test_a_workflow_is_read_the_one_way.py`, the comment about neutral values
   - `tests/test_the_gate_asks_the_range_ci_will_ask.py`, the comment about neutral values

   These four came from `git grep -n -i 'real identifier'` outside the records.
3. **The commit cadence.** The home is `skills/implement/SKILL.md` §*2. Implement, and feed evidence back where you verified it*, at its *Commit at the smallest step…* paragraphs. `CLAUDE.md` §*Repo rule — commit early…* becomes a link row. The row carries only what §2 tells a reader to look up in their own repository: this one squashes feature branches, and every work item commits a `routing.md` first, so both of §2's conditions hold here. Its last paragraph, *Commit freely: a ledger row names no commit…*, is already a link added by #715. It stays as it is.
4. **The fourth restatement in `CLAUDE.md`**, found by going through `CLAUDE.md`'s sections one at a time (D1). The last paragraph of §*The goal a design is chosen against*, *Questions a person genuinely has to answer go in one batch before the first edit…*, restates `skills/implement/SKILL.md` §1's batch rule. The paragraph before it already links §1. The restatement is folded into that link.
5. **A check, shipped.** It is a repository-wide verbatim ratchet (D5). Any run of `WINDOW` words that two files in the rule corpus share, beyond a baseline recorded per file pair, fails the check. The baseline is the method's recorded result. It shrinks as later work moves copies to their homes.
6. **A one-off result, recorded here.** The method's paraphrase pass (D6) cannot become a check. Its result is the table in §*The method and its result*.
7. **The F4 row of `docs/the-record-layout.md`** now says it is built, and records four things: the three homes, the link-row shape (D2), the check, and where the remainder went (D7).
8. **Pins.** A sibling of the #715 module covers the three rules (D4), and the ratchet module (D5). Each is seen red (§15).

**Out:**

| Item | Why it is out | Where it goes |
|---|---|---|
| O1. `CLAUDE.md`'s generated region, `<!-- specseal:start -->`…`<!-- specseal:end -->`. It restates agent-contract §2 and §10, and the routing procedure of `skills/implement/orchestration.md`. | It is the block `install.sh` distributes, and `claude_block.py --check` holds it equal to its source (#292, owner Q1). It is what a user's session holds in a repository where the plugin's skills are never opened. Rewording it changes every install, so it is a product decision and not a layout one. | Not filed. The block is a sanctioned copy, and this row records why. |
| O2. The 219 verbatim runs and 58 paraphrased sentence pairs the method found outside the three rules. More than half sit in the review-chain cluster. | Moving them is wording work across about 50 files, under the review cap, with sibling branches in flight. The grounds #715 gave for leaving the three rules alone hold here too. Collapsing two copies also means choosing which one is the rule, and in the review-chain cluster that is the substance of a document, not a link. | One issue, cut by cluster (D7). The ratchet's baseline keeps the verbatim half visible in the tree. |
| O3. `docs/release-checklist.md` step *Press Create a merge commit, never squash*, and `CONTRIBUTING.md` §*Cutting a release*'s *which merge method each direction takes*. | Both apply the merge rule at the moment the act happens and point at the home. Neither carries the table. They are applications, not restatements. | Nothing. This row is the record. |
| O4. Every file that uses *a feature branch squashes into its release branch* as a premise, including scripts, `chain_check.py` and `unverified_check.py`. There are about 20, from `git grep -n -i -E 'squash(es\|ed)? (in)?to'`. | They reason from the fact, and none of them says which method to choose. | Nothing. |
| O5. `docs/the-record-layout.md` outside the F4 row, including the lead sentence of §*What is decided and not built yet* (*F1 is built; the other three are not yet*). | #728 and #729 edit the same document in this release. Editing their lines or the shared count sentence would make a three-way conflict at the squash. | questions.md Q3: whichever of #728, #729 and #730 squashes last fixes the count sentence. |
| O6. A `CONTRIBUTING.md` bullet announcing the new check. | It would restate the record-layout rule a fourth time. The check's failure message names the home and says what to do. | Nothing. |
| O7. `README.ko.md` and every `*.ko.md`. | Korean editions are sanctioned mirrors (`CONTRIBUTING.md` §*House rules*, *Both READMEs move together*). They are never a copy in English words. | Excluded from the corpus. |

## The decisions, with their grounds

**D1. What `CLAUDE.md` restates, enumerated by construction.** Each repository-local section of `CLAUDE.md` was read and given one of three states: home, link, or restatement.

| `CLAUDE.md` section | State | Home |
|---|---|---|
| *The goal a design is chosen against* | home of the goal; its last paragraph is a restatement | `skills/implement/SKILL.md` §1 (Scope 4) |
| *the merge method is fixed per direction* | restatement, **and the copy has drifted** (below) | `docs/branch-and-release.md` |
| *no real identifiers* | restatement | `CONTRIBUTING.md` §*House rules* |
| *a thing more than one party can have is named with whose* | link | `skills/writing-style/SKILL.md` |
| *commit early* | restatement, apart from its last paragraph, which is a link | `skills/implement/SKILL.md` §2 |
| *a change writes fragments* | link (#715) | `docs/the-record-layout.md` |

**The merge copy has already drifted, and the drift is a false statement.**
- `CLAUDE.md:52–56` says *two things point at those commits by SHA: the `Verified … at <sha>` stamp on every `# RIDER:` comment, and the `Target SHA`*.
- The home says the reverse. `docs/branch-and-release.md` §*Work accumulates on a release branch* reads: *A `# RIDER:` comment's stamp names content, never a commit … The stamp used to read `Verified … at <sha>`*. Work item `1788826000` made that change, and `tests/test_a_rider_reaches_its_file.py::test_no_rider_stamp_names_a_commit` holds it.
- `CLAUDE.md`'s table is also missing two of the home's six rows: the release-prep branch and a hotfix branch.

This was read at e141980a. It is #715's prediction (*one rule today and two after the first edit to either*) observed in the tree, and it is the grounds for removing the table from `CLAUDE.md` instead of re-synchronising it.

**D2. What a link row in `CLAUDE.md` must still carry.** `CLAUDE.md` is loaded into every session. The home files are not. A row that holds only a path and a section would send a session to open the home at the very moment it needs to act. In an unattended run that moment is a merge the session performs itself, or a fixture it writes. So a link row carries three things and nothing else:

1. **The home's path and section**, so that a reader opens one file.
2. **The trigger**: the moment in a session when the rule applies. That is why the row lives in an always-loaded file. This is the precedent row's clause *it is here because a session … has no other reason to open that file*.
3. **The act, in one sentence of the row's own words.** It must be enough that a session acting on the row alone, without opening the home, does the right thing. Where the act needs a value (`example.com`, `/Users/x/`, *squash* into `release/*`, *merge commit* into `main`), the value is part of the act.

A link row carries **no table, no reasoning, no history, no incident, and none of the home's sentences.**
- Grounds for the line: the parts that drifted in D1 were a table and a piece of reasoning. An act sentence is too short to carry either.
- What it costs: the act sentence still states the rule, in other words. A later change to the rule's *values* has to update the row as well as the home. Only the home's sentences are pinned (D4), so a stale value in a row is a reviewer's finding. No check catches it.
- Why this is accepted: the alternatives are worse. A bare link sends the session to a file it will not open. A full copy has already drifted.

The decision is recorded in the F4 row (Scope 7), which is where the record layout keeps decided shapes.

**D3. Commit cadence: the row applies the rule, it does not restate it.** §2 states the rule generically and tells the reader to *read both off the repository*. The `CLAUDE.md` row is this repository's answer to that:
- feature branches squash, which is `docs/branch-and-release.md`'s table;
- every work item commits `routing.md` before its first edit, which is the `CLAUDE.md` block's own routing row.

So the row's act sentence is *commit as soon as a step stands on its own* and does not need §2's reasons. It keeps its third paragraph, the #715 link to the three `docs/the-evidence-ledger.md` sections, word for word. `tests/test_the_ledger_rules_have_one_home.py::test_the_two_first_reads_link_each_rule_to_its_home` reads that paragraph.

**D4. The per-rule pin is a sibling module, not an extension of #715's.** `tests/test_the_ledger_rules_have_one_home.py` is named for the ledger rules, and adding the merge method to it would make its name false. The sibling module uses the same shape:
- `RULES`: for each rule, the home, the section, and needles that only the home writes;
- `LINKED`: `CLAUDE.md` must name each home's path and section;
- `CARRIERS`: the files from Scope 1–3 and D1, none of which may contain a needle;
- one case that plants a needle into a copy and shows the check naming it.

The builder chooses the needles from the home's text as it stands after phase 1. Each needle must be a sentence the link row does not need.

**D5. The method, part one, ships as a check: a verbatim ratchet over the rule corpus.**
- **Corpus.** Every tracked `*.md` under `docs/`, `skills/`, `agents/` and `templates/`, plus `CLAUDE.md`, `CONTRIBUTING.md` and `README.md`. Excluded: `*.ko.md` (O7), everything under `seal/` (records, and the `seal/README.md` that `hooks/root-migrate.py` writes from `templates/seal-README.md`), and `CHANGELOG.md`.
- **Normalisation.**
  - Drop `CLAUDE.md`'s generated region (O1), fenced code blocks, and heading lines.
  - Replace a quoted section name, `§*…*` or `<path>.md` followed by `*…*`, with a single token. A link shares its heading's words by design. **The name may wrap across a line**, and the probe's first regex missed exactly that case.
  - Lowercase. Strip `` ` ``, `*`, `|`, `>` and `#`. Split into words.
- **Unit.** For each unordered pair of corpus files, count the distinct `WINDOW`-word windows the two files share.
- **`WINDOW`** is `tests/test_a_moved_rule_leaves_its_definition.py`'s `WINDOW = 15`, imported or moved to one shared place, never typed a second time. That number was measured between a kept application (10 words) and a real copy (25 words). The same question is being asked here, across more files.
- **Baseline.** A table in the module, keyed by pair, with the count measured at the build's base after phase 1. Every entry is debt, apart from one: the agent-definition preamble that `tests/test_every_agent_reads_the_contract.py` requires in every `agents/*.md`. Its entries are marked sanctioned and name that test.
- **It fails when** a pair that is not in the baseline shares any window, or when a pair's count goes above its baseline. The failure names the pair, the count, the longest shared run, and the act: *link to the home instead of copying it, per `docs/the-record-layout.md`*.
- **It passes when a count goes down.** The baseline does not have to be tightened in the same change. The reason is that every branch editing a duplicated passage would otherwise edit one shared table, and that is the shared-file conflict `docs/the-record-layout.md` §*A change writes fragments, never a shared file* exists to stop. The cost is slack: a pair that has drained can take a later copy up to its old count. The work that drains a pair lowers its count on purpose (D7).
- **Seen red** by planting a sentence copied from one corpus file into a copy of another.

*Why a check and not only a one-off.* A one-off list rots on the day it is written (contract §7: *every enumeration in this repository has rotted*). A paste is the measured failure, and it has happened four times: #107's paste-back into `agents/warden.md`, #292's block that was 95 % identical, #715's `CLAUDE.md`/`CONTRIBUTING.md` pair that disagreed, and D1's merge table. A ratchet stops the next paste without asking anyone, which is the first goal in `CLAUDE.md`.

*What it does not catch, stated plainly.* It was measured against the three restatements #730 names. **It finds 1 of 3.** It finds the merge table, through its identical rows: a 17-word run. It does not find *no real identifiers* or the commit cadence, because both are restated in fresh words. The check stops copies from growing. It does not find a paraphrase.

**D6. The method, part two, is a one-off: a paraphrase pass, with its result recorded and not checked.**
- Split each corpus file into sentences: on sentence punctuation, on blank lines, and on list, table and heading lines. Keep sentences of 10 words or more.
- Take each sentence's set of word 3-grams. Report each cross-file pair with a Jaccard similarity ≥ 0.35 that shares no 12-word run.
- 3-grams that occur in more than 40 sentences are ignored as stock phrases.

It cannot be a check, for three reasons:
- At 0.35 it also matches a heading against a sentence that links that heading, and a table row against its prose twin.
- Its recall on #730's three rules is 0 of 3. The *no real identifiers* pair scores below 0.35.
- #107's docstring already explains why no constant separates a paraphrase from an application.

A check that goes red on those cases would hand every false red to a person, which `CLAUDE.md`'s goal ranks as the most expensive design. So the pass runs once, here, and its result goes to the remainder issue (D7) for a reader to judge.

**D7. Where the remainder goes.** Rung 3 of the ladder: one new issue, because the owner plans the milestones and so has a reason to act on it. It is not one issue per pair, because #223 already measures a pile of 80 open issues. The issue's body:
- the clusters of §*The method and its result*;
- the paraphrase table;
- the instruction that the work item which drains a pair lowers that pair's count in the ratchet's baseline.

The framer cannot file it, and neither can the smith (contract §6). **The orchestrating session files it, from the text in this spec**, and the F4 row and the changelog fragment name its number. Until it has a number, the F4 row says *the remainder issue*, and the orchestrator fills the number in before the pull request is marked ready.

**D8. Edits to `docs/the-record-layout.md` stay inside the F4 paragraph.** The paragraph is rewritten the way F1's was when F1 was built:
- *Built by #730.*
- The three homes.
- The link-row shape from D2, in one or two sentences.
- The check, named by module, with what it does not catch.
- The remainder issue.

Nothing else in the document is edited (O5).

## The method and its result

This was measured by the framer at `07aec0f2` (= `e141980a` plus `routing.md`), with a probe that ran in the framer's scratchpad and was then deleted (contract §7). The labels are `executed`. The builder re-measures after phase 1, because the corpus moves.

- **Corpus:** 67 files, 180,375 words after normalisation.
- **Verbatim, `WINDOW` = 15:** 229 shared runs across 108 file pairs.
  - 10 runs are the sanctioned agent preamble.
  - **219 runs, 99 file pairs, 50 files and 4,689 words are restatement debt.**
  - Runs by length: 115 of 15–19 words, 52 of 20–24, 28 of 25–29, 10 of 30–34, 7 of 35–39, 2 of 40–44, 2 of 45–49, 1 of 50–54, 1 of 55–59, and 11 of 60 or more.
- **Where the debt sits, by number of runs a file takes part in:**

  | File | Runs |
  |---|---|
  | `skills/code-review/orchestration.md` | 55 |
  | `templates/sdd-round.md` | 43 |
  | `docs/review-handoff-protocol.md` | 40 |
  | `docs/round-record-spec.md` | 36 |
  | `docs/review-chain-spec.md` | 32 |
  | `skills/implement/SKILL.md` | 18 |
  | `agents/smith.md` | 17 |
  | `skills/code-review/SKILL.md` | 16 |
  | `README.md` | 16 |
  | `skills/implement/orchestration.md` | 16 |
  | `docs/the-evidence-ledger.md` | 14 |
  | `skills/evidence-check/SKILL.md` | 12 |

- **The clusters, for the remainder issue:**
  - **(a) The review-chain documents.** The five files at the top of the table, with `skills/code-review/SKILL.md` and `agents/warden.md`. This is more than half of the debt. Examples: *one depth per finding*, a 55-word run in `agents/warden.md` ↔ `skills/code-review/SKILL.md` ↔ `docs/round-record-spec.md`. *A round that opens nothing needing a fix does not consume the cap*, a 42-word run in `docs/review-chain-spec.md` ↔ `skills/code-review/orchestration.md`.
  - **(b) Agent definitions ↔ skills.** `agents/smith.md`, `agents/warden.md` and `agents/sealer.md` ↔ `skills/implement/SKILL.md`, `skills/code-review/orchestration.md` and `skills/verify/SKILL.md`. Examples: the 62-word run smith ↔ warden about who owns the full suite. The contract's §5 aggregate sentence, a 36-word run in `skills/agent-contract/SKILL.md` ↔ `skills/implement/SKILL.md`.
  - **(c) Template comments ↔ the skill or doc that owns the rule.** Examples: `templates/sdd-spec.md` ↔ `agents/framer.md`, the mark comment (34 words). `templates/ledger.md` ↔ `docs/the-evidence-ledger.md` and `skills/evidence-check/SKILL.md`.
  - **(d) `README.md` ↔ docs and skills.**
  - **(e) The policy-document preamble.** *It is a policy document: it outranks the SDD set, and a work item that finds it wrong corrects it…* appears in five `docs/` files. That is a 25-word formula restating `skills/implement/SKILL.md` §1's precedence.
- **Paraphrase pass (D6):** 58 sentence pairs across 43 file pairs that share no 12-word run. Heading lines are excluded. Sorted by best Jaccard:

| File | File | Pairs | Best J |
|---|---|---|---|
| `skills/agent-contract/SKILL.md` | `skills/implement/SKILL.md` | 2 | 1.0 |
| `agents/warden.md` | `templates/sdd-round.md` | 1 | 1.0 |
| `skills/code-review/orchestration.md` | `templates/sdd-round.md` | 6 | 1.0 |
| `docs/one-root-by-lifetime.md` | `skills/settle/SKILL.md` | 2 | 1.0 |
| `skills/implement/SKILL.md` | `templates/sdd-overview.md` | 1 | 0.73 |
| `docs/commit-review-gate-spec.md` | `docs/worktree-guard-spec.md` | 1 | 0.72 |
| `docs/review-handoff-protocol.md` | `skills/code-review/orchestration.md` | 3 | 0.67 |
| `skills/code-review/SKILL.md` | `templates/sdd-round.md` | 3 | 0.65 |
| `docs/the-evidence-ledger.md` | `templates/ledger.md` | 3 | 0.62 |
| `skills/implement/orchestration.md` | `templates/config.md` | 1 | 0.62 |
| `docs/round-record-spec.md` | `skills/code-review/SKILL.md` | 1 | 0.6 |
| `docs/one-root-by-lifetime.md` | `templates/config.md` | 1 | 0.6 |
| `skills/implement/SKILL.md` | `templates/config.md` | 1 | 0.6 |
| `docs/round-record-spec.md` | `templates/sdd-round.md` | 1 | 0.56 |
| `agents/scribe.md` | `skills/verify/SKILL.md` | 1 | 0.55 |
| `skills/implement/SKILL.md` | `templates/sdd-round.md` | 1 | 0.53 |
| `docs/the-commit-gate-inside-git.md` | `docs/the-review-and-parity-arms.md` | 1 | 0.52 |
| `docs/the-evidence-ledger.md` | `skills/settle/SKILL.md` | 1 | 0.5 |
| `skills/code-review/orchestration.md` | `skills/implement/SKILL.md` | 1 | 0.5 |
| `docs/the-record-layout.md` | `templates/config.md` | 1 | 0.5 |
| `skills/implement/orchestration.md` | `templates/sdd-routing.md` | 1 | 0.5 |
| `skills/commit-pr-convention/SKILL.md` | `templates/config.md` | 1 | 0.5 |
| `README.md` | `skills/update/SKILL.md` | 1 | 0.5 |
| `skills/implement/orchestration.md` | `skills/parity-setup/SKILL.md` | 1 | 0.47 |
| `README.md` | `skills/settle/SKILL.md` | 1 | 0.47 |
| `README.md` | `templates/config.md` | 1 | 0.47 |
| `README.md` | `skills/code-review/orchestration.md` | 1 | 0.45 |
| `docs/the-record-layout.md` | `skills/evidence-check/SKILL.md` | 1 | 0.45 |
| `README.md` | `templates/ledger.md` | 1 | 0.44 |
| `agents/smith.md` | `skills/code-review/orchestration.md` | 3 | 0.42 |
| `README.md` | `skills/verify/SKILL.md` | 1 | 0.41 |
| `docs/review-chain-spec.md` | `docs/round-record-spec.md` | 1 | 0.39 |
| `docs/the-evidence-ledger.md` | `skills/evidence-check/SKILL.md` | 1 | 0.39 |
| `agents/sealer.md` | `skills/code-review/orchestration.md` | 1 | 0.38 |
| `docs/one-root-by-lifetime.md` | `docs/the-evidence-ledger.md` | 1 | 0.38 |
| `skills/code-review/orchestration.md` | `skills/legacy-parity/SKILL.md` | 1 | 0.38 |
| `docs/round-record-spec.md` | `skills/code-review/orchestration.md` | 1 | 0.37 |
| `skills/agent-contract/SKILL.md` | `skills/config/SKILL.md` | 1 | 0.36 |
| `docs/review-handoff-protocol.md` | `templates/sdd-round.md` | 1 | 0.36 |
| `skills/code-review/orchestration.md` | `skills/evidence-check/SKILL.md` | 1 | 0.36 |
| `docs/the-commit-gate-inside-git.md` | `README.md` | 1 | 0.36 |
| `docs/the-agent-set.md` | `skills/agent-contract/SKILL.md` | 1 | 0.35 |
| `docs/review-chain-spec.md` | `skills/code-review/orchestration.md` | 1 | 0.35 |

The rows at 1.0 are sentences of 10 or 11 words that are identical, too short for the 12-word cut. An example is *Never record something as passing that you did not run*, which appears in both the contract and `implement`. The rows at the low end include links whose wording comes close to the sentence they point at. Telling those apart is the reader's job that D6 leaves open.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 | **Given** a session that holds only `CLAUDE.md`, **when** it is about to merge a feature pull request into `release/vX.Y.Z`, or the release branch into `main`, **then** the merge row tells it to squash into the first and make a merge commit into `main`, and names `docs/branch-and-release.md` §*Work accumulates on a release branch*. The row carries no table, and no claim about `# RIDER:` stamps. | read by the warden; the D4 module's link case and its needle-absence case, executed |
| S2 | **Given** the same session writing a fixture or an example, **then** the identifiers row names `example.com` and `/Users/x/` and links `CONTRIBUTING.md` §*House rules*. The home bullet carries the history-rewrite reason, and `CLAUDE.md` does not. | D4 module, executed; read |
| S3 | **Given** the same session after an edit, **then** the commit row says that both of §2's conditions hold in this repository, tells it to commit as soon as a step stands on its own, and links `skills/implement/SKILL.md` §2. Its #715 link paragraph is unchanged. | D4 module and `tests/test_the_ledger_rules_have_one_home.py`, executed |
| S4 | **Given** the goal section, **then** its batch sentence is folded into the existing §1 link and is not stated as a second rule. | read; the D4 module if the builder pins it |
| S5 | **Given** any of the four code comments from Scope 2, **then** each one cites `CONTRIBUTING.md` §*House rules* and none cites `CLAUDE.md` for the rule. | `git grep -n 'CLAUDE.md. §\*no real identifiers'` returns nothing; executed |
| S6 | **Given** a pull request that pastes 15 or more consecutive words from one corpus file into another, **then** the ratchet fails and names the pair, the count, the longest run, and the home-link act. | the module's planted case, seen red (§15) |
| S7 | **Given** a pull request that removes a copy, **then** the ratchet passes without a baseline edit. | a planted case that deletes a run from a copy |
| S8 | **Given** the ratchet module on the built tree, **then** it passes, and its baseline equals the counts measured after phase 1. `CLAUDE.md` ↔ `docs/branch-and-release.md` is no longer a pair in the table. | executed: the module alone |
| S9 | **Given** `docs/the-record-layout.md`, **then** the F4 paragraph says built, names the three homes, the link-row shape, the check and its blind side, and the remainder issue. No line outside that paragraph has changed from the base. | read; `git diff` of the file is confined to the F4 paragraph; the docs line-wrap and fold checks on the file |
| S10 | **Given** `CLAUDE.md`'s generated region, **then** it is byte-identical to the base. | `python3 .github/scripts/claude_block.py --check`, exit 0 |

## Data & interfaces

- **New test modules.** Two of them. The builder names them in the repository's sentence style, for example `tests/test_the_rules_claude_md_names_have_one_home.py` (D4) and `tests/test_no_passage_is_pasted_into_a_second_file.py` (D5). The ratchet's docstring holds the method's reasoning: the corpus, the normalisation, why the match is verbatim, why it ratchets, and the blind side. That is the precedent #107's module set.
- **The `WINDOW` constant has one source.** Either both modules import it, or it moves to `tests/conftest.py`.
- **The ratchet's baseline** is a table literal in its module: `{("a.md", "b.md"): count}`, with the pair ordered and the sanctioned entries commented. It is measured once, after phase 1.
- **Ledger.** Rows go into `seal/ledger/1791076836-every-rule-claude-md-restates-has-one-home.md`, one for each home section this work states or relies on. **Changelog.** `seal/specs/1791076836-…/changelog.md`.
- No hook, script, workflow or config row changes.

## Open questions → questions.md

Every row there has either been decided by this frame, with its grounds written in, or belongs to the work or to the orchestrator. None blocks the build.

<!-- The line below is the framer's mark, and it is the only evidence in the
     TREE that the framing happened — the existing framer mark lives in the
     repository's git dir, and a git dir does not travel, so CI cannot see it.
     Fill in the date and `<who>`; `<who>` takes the two values the `Planning`
     row of `routing.md` takes, `framer` or `the session`, and a mark that
     disagrees with that row is refused at the pull request rather than
     guessed at.
     The shape — verb, date, who, the moment — is the one `routing.md` and
     `plan.md` already end with, which is what keeps three feet-lines from
     becoming three conventions. -->

Framed 2026-10-04 by framer, before the build.
