# Implementation Plan: the plugin directory check reads the directory

<!-- seal/specs/1791384161-the-plugin-directory-check-reads-the-directory/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved 2026-10-08 by the repository owner, when `smith` was spawned.

## Summary

Keep the observation, remove the guess, name the page. The command keeps
reading the two marketplace files and keeps every answer it can ground in them
— entry or no entry, the pinned commit, the three-valued ancestry — and stops
saying anything about the directory, which it never read and no script can.
Its closing block names the portal's Submissions page and the Console page by
the kind of listing each answers for. The checklist box and the two policy
sentences follow it, their pins move in the same commits, and `claude.ai`
enters the identifier allowlist on purpose. Three phases, each a commit that
stands on its own: the command, the documents, the records.

The owner's act — moving SpecSeal's Console listing to the portal — is
`questions.md` Q1 and blocks nothing: the box ships saying *Console, read
2026-10-07*, and a move changes that one dated sentence.

## Technical context

Coordinates are at 59998a32, the branch's routing commit.

- **The command**, `.github/scripts/plugin_directory_check.py`.
  Lines 80–85 hold the three constants: the two files, the manifest path, and
  PORTAL (the short link that now answers 302 to a docs page). Lines 190–234
  are the per-file answer; the two sentences that name PORTAL are at 205–206
  (absent entry) and 224–226 (pin behind `main`). Lines 254–257 print the
  closing sentence *Whether a submission has been ACCEPTED is readable from
  nowhere public*, which the new closing block replaces. The docstring's
  paragraph at 24–32 says no document tells how an update reaches a listed
  plugin and points at #417's Q1; both halves are false now (`spec.md`
  §*Vocabulary*). The comment at 75–79 names `CONTRIBUTING.md` §*House rules*,
  and `tests/test_the_rules_claude_md_names_have_one_home.py` lines 89–93 and
  108–112 require the command and its test module to keep naming that home.
- **Its test module**, `tests/test_the_plugin_directory_answers_the_box.py`.
  The absent-entry case at 108–126 pins PORTAL in the output. The end-to-end
  case at 269–285 pins *readable from nowhere public*, which is the sentence
  the closing block replaces; the pin moves to the new sentence. Every other
  case stays as it is (`spec.md` A2, A4).
- **The box**, `docs/release-checklist.md` lines 360–373, and its command
  block at 326–328. Pinned by
  `tests/test_the_release_tail_does_not_end_at_the_tag.py` lines 144–155
  (*reports and never fails*, *Not listed*, *pinning an older commit*) and
  by the command tuple at 47–53, which stays.
- **The two policy sentences**, `docs/branch-and-release.md`: the release-tail
  bullet at 79–85 inside the fold whose `Enforced by:` line is at 94–96, and
  the third-reader paragraph at 153–167. Pinned by the same test module at
  187–203 (three phrases, all kept) and 246–264 (*Nothing fires it*, kept).
- **The allowlist**, `tests/test_no_real_identifiers.py` lines 19–29. The
  TLD list at line 32 is why `clau.de` was never caught.
- **The paste ratchet**, `tests/test_no_passage_is_pasted_into_a_second_file.py`
  lines 200–219: its corpus is `*.md` under the top files and `docs/`, so the
  box and the bullet must share no run of words; the command is outside it.
- **The fold check**, `tests/test_a_folded_statement_names_what_enforces_it.py`:
  the bullet's fold keeps one live `Enforced by:` line, and a new case added
  for A7 is named there.
- **The released rows this moves.** `docs/release-checklist.md#"## 6. After
  the merge"` is anchored by S9 (`seal/releases/0.11.1.md:23`), P1c
  (`seal/releases/0.15.0.md:35`) and W4 (`seal/releases/0.18.0.md:117`), each
  last re-read in `seal/releases/0.20.0.md` (lines 165, 169, 181) at
  `@49db8639`; W4 also anchors `docs/branch-and-release.md#"## Cutting a
  release"` at `@98986adf`. Both units change here, so the three families
  drift and are re-read into this work item's fragment
  (`docs/the-evidence-ledger.md` §*A released row is read again in the
  branch's fragment*).

**What breaks in six months, and what is done about it.** The owner moves the
listing to the portal and the box's dated *Console* sentence stays. A releaser
who trusts it skips the portal. Two things bound that: the sentence says whose
reading it is and when, so a reader can see it has aged, and the command's
closing block names both pages whatever the kind, so the terminal never depends
on the sentence. Second: Anthropic changes a marketplace file's shape or a
page's address. The reader already reports a shape it cannot read as *could not
be read* and exits 0, and the two addresses are two constants in one file.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| Read the directory from the command | Measured 2026-10-07: HTTP 403 with a challenge page to a plain client and to a browser user agent, on three paths; no page in `claude.com/docs/llms.txt` describes an API. A reader that scraped past a challenge is red on somebody else's schedule — the gate #417 refused | refused, by measurement |
| Read the marketplace website's sitemap (341 plugin pages, public XML) | A third catalog beside the directory, with no documented relation to it; 341 pages against 2,284 entries says it is not the same list; SpecSeal is in neither today. Adds a reader whose format nobody here owns and changes no answer | not added; named so the counts travel with the refusal |
| Delete the command; the box becomes a person's look at the portal | A box with no command is the shape #386 measured skipped three releases running. And the files' pin and ancestry are true observations — the commit a Claude Code install from that marketplace carries, and the squash rule's guard | refused |
| Read the portal or the Console page with the owner's session from CI | A credential nobody asked for, for one person's page; `CONTRIBUTING.md` §*What a change to a gate must carry* has no row for it | refused |
| Drop the official file's read and keep the community mirror alone | Nothing lost today. But the official README takes external entries through the same submission link, so it is a second public output of the same pipeline, at one HTTPS call; dropping it makes the command blind to the one place a curated entry would appear | kept, both files read |
| Carry the page addresses in the box as well as the command | Two copies of an address drift the way two copies of a rule do, and the command is already the home for real identifiers (its comment above the constants says why). The box names the pages by their documented names and says the command prints the addresses | the addresses live in the command; the box names the pages |
| Keep the command's inputs, remove the inference, name the page (chosen) | The dated sentence above goes stale at the owner's move; bounded as stated | **chosen** |

## Phases

Vertical slices — each phase ends with something runnable and verified.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **The command stops claiming, and its pins move.** The constant PORTAL and the two sentences naming it go; the per-file absent line becomes *not an entry in <file> (<N> entries)* and nothing follows it; the closing block says the directory was not read, that no script can read it, and names the portal's Submissions page and the Console page by the kind of listing each answers for, with one line that a portal listing takes new versions from the tracked branch on its own; the docstring's paragraph at 24–32 is replaced by the three facts from the docs, dated; the vocabulary of `spec.md` §*Vocabulary* in the docstring and every printed line. `claude.ai` enters `ALLOWED_DOMAINS` with its comment. The test module loses the PORTAL pin, moves the *readable from nowhere public* pin to the new closing sentence, and gains the cases for A1 and A3 — the constant is absent, the output carries neither *submit* nor *resubmit*, the closing lines carry *was not read*, *Submissions* and *Console*. Each moved or new pin seen red against the command at 59998a32, the mutation named in the phase record (§15). The command run once live against `main`, its output pasted into the phase record as executed | `uv run --frozen pytest -q -p no:cacheprovider tests/test_the_plugin_directory_answers_the_box.py tests/test_no_real_identifiers.py tests/test_the_rules_claude_md_names_have_one_home.py`; `python3 .github/scripts/plugin_directory_check.py` with exit code read directly | |
| 2 | **The box and the two policy sentences, with their pins.** The box per `spec.md` §*Scope* item 2 — *reports and never fails* kept; what the command reads and that the directory is readable from nowhere a script can reach; the two pages by name and which kind each answers for; a portal listing updates on its own; the dated Console sentence; the docs page for the move; no *resubmit*; the open-question sentence gone. The release-tail bullet per item 3, its `Enforced by:` line naming the new A7 case. The third-reader paragraph names a marketplace file, keeps its measurement and pinned phrases, adds the directory as a reader of the tracked branch's scanned commit. The box case stops pinning *Not listed* and *pinning an older commit* and pins A5 and A6; one new assertion on the bullet for A7. Each pin seen red against the documents at 59998a32. The box and the bullet share no run the ratchet counts | `uv run --frozen pytest -q -p no:cacheprovider tests/test_the_release_tail_does_not_end_at_the_tag.py tests/test_no_passage_is_pasted_into_a_second_file.py tests/test_a_folded_statement_names_what_enforces_it.py tests/test_docs_line_wrap.py tests/test_a_document_that_names_a_script_says_how_to_reach_it.py tests/test_the_rules_claude_md_names_have_one_home.py tests/test_no_real_identifiers.py` | |
| 3 | **The records.** `changelog.md` in this directory (one entry: what the command stopped claiming and what the box now says, #858). The ledger fragment `seal/ledger/<this work item>.md`: S9, P1c and W4 read against the new text — S9's claim is about §0 and §6's trigger and input, P1c's about the closer's refusal paragraph, W4's about the seal bullet, and none of the three is about the directory box, so each is expected to hold — then written as `Re-read ·` rows with `--checked 2026-10-<dd>`; no row for the command (grounds in `spec.md` §*Data & interfaces*). `overview.md` from `templates/sdd-overview.md` with `## Not verified` naming Q2's answerer. `phases/phase-N.md` for each phase, the §15 mutations recorded in 1 and 2 | `evidence-check --reverify --into seal/ledger/<this work item>.md --checked <date>` after the three reads, then the plain run; `uv run --frozen pytest -q -p no:cacheprovider tests/test_the_ledger_fragments_fold_at_release.py tests/test_a_record_states_what_the_tree_has.py tests/test_a_question_says_who_can_answer_it.py` | |

Phase 1 and phase 2 are separate commits because each changes a line a person
reads and pins it in the same commit (§14); neither depends on the other's
text, so the order is only the order a reviewer reads them in. The allowlist
change rides phase 1 because the command's closing block is the first line in
the tree to name `claude.ai`.

**Siblings.** No unit another 0.21.0 frame names is touched: not
`chain_check`, `round_record`, `evidence_check`, `broad_gate`, `generic_units`
nor any hook. `docs/release-checklist.md` §6 is the one shared document, and
the brief's table shows no sibling in it.

This table is also where the work records how far it got. There is no separate
task list: a list of tasks is mutable progress, and a stale one asserts a state
that is not true, which is the failure the evidence ledger exists to prevent.

**Status is empty, or the commit that closed the phase.** A tick is refused,
and so is `done`: both can be typed without anything having happened, and both
assert a present state that nobody can check. A commit hash asserts a past one
— someone can open it — which is the same trick that lets a round record live
beside the contract rather than in tool state.

Fill it in as each phase closes, not at the end. A phase reconstructed
afterwards is reconstructed from the diff, which is where it already was.

What a phase discovers while it is being built, and needs the next phase to
know, does not fit in this table's cells. Write it to
`seal/specs/<work-item-id>/phases/phase-N.md`, from `templates/sdd-phase.md`,
when the phase closes.

One caveat, so nobody builds on it, and it has two halves. Where feature
branches squash, these commits stop resolving at the merge — and **a rebase
during the work does the same thing earlier and far more quietly**, because the
orphaned object still answers `git cat-file` in the worktree that wrote it.
The quiet half is the one that bites: this column was wrong on its own first
use, nine SHAs deep, and only a reviewer opening them found it. **Re-read the
column after any rebase**, or it names commits that resolve in one clone and
nowhere else. That is tolerable because nothing measures from this column.
The evidence ledger had the same problem and no such tolerance. It no longer
has it at all: a ledger row names a symbol and a content hash, so there is no
commit in it for a rebase to orphan.

## Operational impact

None to deploy. No workflow changes, no dependency, no environment variable.
The command still needs the network to reach `api.github.com`, as it did. One
domain enters a test's allowlist. The release checklist's last box reads
differently, and the release that ships this work is the first to run it.
