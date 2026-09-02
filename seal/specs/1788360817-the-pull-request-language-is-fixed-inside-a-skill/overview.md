# the pull request language is fixed inside a skill — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens rather
than reconstructed at the end.

Opened at phase 1, because `tests/test_chain_hooks_hardening.py` owes an
overview to every work item that reached the ladder, and a branch that leaves
that red for two phases is a branch whose reviewer reads a failure that is
not about the change. -->

📋 implement applied
· spec:     `seal/specs/1788360817-the-pull-request-language-is-fixed-inside-a-skill/{routing,spec,plan,questions}.md`; issue #82 (the done-when list is the acceptance criteria); `docs/one-root-by-lifetime.md#"## What the root is called"` (English for shipped artifacts, Korean as the owner's per-user setting); `CONTRIBUTING.md` (a change writes a fragment, never a shared registry); `README.md#"### Shared or local"` and `hooks/optin.py#home_at` (where the root is); `seal/follow-up.md` — nothing here was its prerequisite, and it gains nothing
· evidence: `seal/ledger/1788360817-the-pull-request-language-is-fixed-inside-a-skill.md`, thirteen rows in five groups, 36 coordinates — the last group is what round 1 changed. Two rows in `seal/ledger/1788354065-…md` were re-read and re-verified here (🟡 4), and each says so in its own Notes cell
· verified: **Executed** — `tests/test_the_pull_request_language_is_the_repositorys.py` (36 cases after round 1's four planted rows; 24 before, of which 6 were red until the document edits), `tests/test_docs_line_wrap.py`, `tests/test_first_setup_asks_once.py`, `tests/test_no_document_names_the_old_roots.py`, `tests/test_release_hygiene.py`, `tests/test_chain_hooks_hardening.py`, `tests/test_the_set_a_work_item_always_has.py`, `tests/test_one_word_one_meaning.py`, `tests/test_the_release_check_watches_what_ships.py`, `tests/test_no_real_identifiers.py`, `tests/test_unverified_rows_close.py` — 194 passed in the widest slice; `bin/evidence-check --strict .` over the whole tree after round 1's fixes, `335 ok · 0 drifted · 0 broken` — unscoped, for the reason the section below gives; `uvx ruff check` and `ruff format --check` on the two Python files this work touched. The two checks round 1 asked for were run against the pre-fix text as well: the old parser returned the row behind a foreign one, and four templates were unreachable at `1280de9` where none is now. **Read** — `hooks/optin.py#home_at` (no hook reads the new file, so nothing here executes it), `.github/workflows/hygiene.yml`'s version step (base is `release/v0.5.0`, so `plugin.json` is left alone). **Not run, on purpose** — the full suite, a repository-wide lint and a typecheck: the broad gate is the orchestrator's, once, after the rounds settle

## Why this work exists

The `commit-pr-convention` skill required English of every repository, which
was one user's convention promoted to a rule for all of them. A repository
now states its own pull request language in one row of `seal/config.md`, and
one that states nothing keeps English.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| The template's wording on the prefix | `spec.md` S4 says only that the exclusion is stated; the template said the prefixes "stay as they are, in every repository" | The template now says **not translated**, the same words as the skill | The case pinning S4 was red against the first draft. Two documents saying the same rule in words that do not overlap is how a check ends up asserting one of them and calling it both |
| Where the layout row sits in the READMEs | `spec.md` S9 asks only that the file be listed | Also added to the `seal/` row of each README's Root table, not the tree alone | A reader who scans the table and never the drawing is the reader who most needs to know a repository can answer here |

## Each fix's new unit carried the next round's finding

**Three rounds running, the finding was the same shape, and no single commit
contains it — which is why it is here rather than in the diff.** A round
found a prose fix that nothing pinned; the pass answering it wrote a helper
to pin the prose; the helper was new code nobody had reviewed, so the next
round found its defect instead.

| Round | What its fix added | What the next round found in it |
|---|---|---|
| 1 | `configured_language`, the templates check | both reproducing the defect they had just closed |
| 2 | `mirror_to_refuse`, a widened glob | the glob out of step with the corpus it is compared against |
| 3 | `as_language_name`, `ROUND_RECORD_FIELDS`, a `git ls-files` call | a missing `check=True`, and a list hand-copied from the file it is checked against |

The findings got smaller each time and did not stop, because the surface
producing them grew with every fix. That is the 3+ Fix Rule's signal — the
architecture talking rather than bad luck — and round 4 answered it by
forbidding this pass any new unit at all. Both findings closed by correcting
what existed: three arguments added to a subprocess call already there, one
assertion added to a case already there, and three claims narrowed to what
runs.

**What that costs, stated rather than left to be found.** Drift on the
`skills/code-review/SKILL.md` side of `ROUND_RECORD_FIELDS` is now
explicitly unpinned. Closing it needs a second list read in the other
direction, which is a new unit — the one thing this pass may not add.
Whether that check is worth having at all is a judgment for a later round,
not a gap to paper over here.

The pattern itself is deferred to issue #89, where the flow's measurements
live.

## What the scoped evidence check could not see

**A whole-document anchor makes any edit to that document another work
item's drift, and a fragment-scoped check cannot see it.** This branch added
three lines to `templates/seal-README.md`'s Layout tree. Two rows in
`seal/ledger/1788354065-…md` anchor on that document *whole*, so the tree
read `325 ok · 1 drifted` while the run this memo first recorded —
`--ledger 'seal/ledger/1788360817-*.md'`, this item's own fragment — read
`27 ok · 0 drifted` and was right about everything it was asked.

That is the sentence that would have caught it, and the rule it gives is:
scope the check to your fragment while you work, and run it unscoped once
before handing over, because the question *what did this branch do to
anybody else's rows* is not a question a scoped run is being asked. Both
claims were re-read here and both hold — only the hash moved — so
`--reverify` was the whole fix.

## Not verified

| Item | Who must answer |
|---|---|
| that a session in a repository whose row says Korean actually writes Korean | the repository owner, on the first non-English repository — nothing here can run it, since this repository's language is English and the row is prose rather than code |
| the full suite, a repository-wide `ruff check` and a typecheck at this branch head | the orchestrator's broad gate, once, after the review rounds settle — deliberately not run here (`agents/smith.md` §Verify) |

## Not done

**No `seal/config.md` in this repository.** Absence is the default and the
default is English, so the file would restate what absence already means.
`questions.md` Q1 carries the trade: what it costs is discoverability, and
what pays for that is `commit-pr-convention` being read before every commit
and every pull request — the moment the question matters.

**No hook.** `questions.md` Q3. A gate would have to judge what language a
commit message is in, and every detector is wrong somewhere on names,
identifiers and quoted English. A wrong stop blocks a correct commit, which
is the failure mode the whole hook design avoids.

**Nothing renamed.** The twelve `pr.ko.md` files under `seal/specs/` are
correct under the new rule, because this repository's pull request language
is English and the mirror is therefore Korean. A language-neutral name would
have cost twelve moves and staled every round record, overview and design
record that cites one (`questions.md` Q2).

**`docs/` untouched.** Issue #82 says so itself — *"Not in
docs/one-root-by-lifetime.md (PR #77…); recorded here."*

**`docs/flow.md` — two lines, and neither by this work item.** The memo said
the file was untouched; round 1 ❓ 8 found one line moving, and round 2 🟡 6
found the second, which is the same mismatch arriving twice.
`git log main..HEAD -- docs/flow.md` names both, and both are the
orchestrator's:

- `ec3e252` — the sealer moves from 0.5.0 to 0.6.0, a release-planning
  decision.
- `e71ed28` — the `#96` row, where round 1 deferred its 🟡 7. That is a
  review round's decision about what leaves this branch.

Both ride here because `release/v0.5.0` takes no direct push and a one-line
planning change does not earn a pull request of its own. This work item
still writes nothing in that file, and the `#82` checkbox belongs to whoever
merges. **Naming one of two is how a finding comes back**, so this line is
checked with the command above rather than from memory.

## Fed back into the spec

none — every clause this work needed was already in `spec.md` before the
first edit, and the two divergences above are recorded rather than promoted.
