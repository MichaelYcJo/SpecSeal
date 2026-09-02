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
· evidence: `seal/ledger/1788360817-the-pull-request-language-is-fixed-inside-a-skill.md`, nine rows in four groups, 27 coordinates
· verified: **Executed** — `tests/test_the_pull_request_language_is_the_repositorys.py` (24 cases; 6 red before the document edits, all green at `56ec644`), `tests/test_docs_line_wrap.py`, `tests/test_first_setup_asks_once.py`, `tests/test_no_document_names_the_old_roots.py`, `tests/test_release_hygiene.py`, `tests/test_chain_hooks_hardening.py`, `tests/test_the_set_a_work_item_always_has.py`, `tests/test_one_word_one_meaning.py`, `tests/test_the_release_check_watches_what_ships.py`, `tests/test_no_real_identifiers.py`, `tests/test_unverified_rows_close.py` — 194 passed in the widest slice; `bin/evidence-check --ledger 'seal/ledger/1788360817-*.md' --strict .` 27 ok · 0 drifted · 0 broken; `uvx ruff check` and `ruff format --check` on the two Python files this work touched. **Read** — `hooks/optin.py#home_at` (no hook reads the new file, so nothing here executes it), `.github/workflows/hygiene.yml`'s version step (base is `release/v0.5.0`, so `plugin.json` is left alone). **Not run, on purpose** — the full suite, a repository-wide lint and a typecheck: the broad gate is the orchestrator's, once, after the rounds settle

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

**`docs/flow.md` untouched.** Its `#82` checkbox belongs to whoever merges,
and the file already carried an uncommitted edit from an earlier session
when this branch began. That edit is not this work item's and was left where
it was found.

## Fed back into the spec

none — every clause this work needed was already in `spec.md` before the
first edit, and the two divergences above are recorded rather than promoted.
