# 1790076050-the-release-tail-is-three-acts-no-document-names — round 1

| Field | Value |
|---|---|
| Round | 1 |
| Target SHA | `b29c86053b7092b24ac91ba756a39895be6c0599` |
| Base | `origin/release/v0.13.1` at `6d41002398bfeeb55db08cca9b441b68e0267049` |
| Pull request | #500 |
| Reviewed by | warden on claude-opus-5[1m] |
| Earlier rounds | none — this is round 1, nothing inherited |

Everything below was read in the worktree and every probe ran in a
`git clone --no-local` of it at the target SHA, removed afterwards. Nothing was
written in the worktree except this file.

## Stage 1 — spec compliance

Every scope item in `spec.md` §*In* is delivered and each acceptance scenario
has a case behind it. A1 through A13 each land in one of the four new or
changed test modules, and the two scenarios no case can reach — the
tag-triggered job firing and the live label write — are named in
`overview.md` §*Not verified* with the releasing session as answerer, which is
the right shape.

The three corrected frame facts hold up when opened rather than read:

- **The manifest path.** `.claude-plugin/marketplace.json` rather than the
  root path the ticket and `spec.md` name, pinned by
  `tests/test_the_plugin_directory_answers_the_box.py#test_it_reads_the_path_the_directories_actually_have`
  together with the assertion that the URL is built on an allowed host. The
  correction is right and the case holds it.
- **The entry shapes.** `phases/phase-3.md`'s table sums to 310 for official
  and 2,282 for community, and `pinned()` returns `(None, …)` for all three
  no-commit shapes with a parametrised case per shape. The frame's
  `source.url` plus `source.sha` would indeed have raised.
- **The ledger rows on the edited heading.** Three, as the build says — G5,
  S4 and R2 are the only rows anchored on
  `docs/issues-and-milestones.md#"## A label answers *what it is about*, and
  survives the move"`. Measured. What the closing memo omits is a **fifth**
  row this range also re-stamped, and that is finding 7.

Two frame files were edited, which a build normally must not do.
`overview.md` §*Not done* carries it with the reason and the evidence
(`git log -S` naming the frame commit as where the refused domain entered), and
nothing either sentence asserted was changed. That is the right call and it is
disclosed.

## Stage 2 — findings

### 🟡 1. An already-closed issue reports a label removal that did not happen, and says nothing at all under `DRY_RUN`

`.github/scripts/close_issues_on_release.py:263-272`

The open-issue path at line 296 guards its report on the write —
`if spent and drop_label(...)` — and the already-closed path three lines above
does not. It calls `drop_label` and prints unconditionally.

**Executed.** With an already-closed issue carrying `size: now` and a tracker
that refuses the edit, the job log reads:

```
#7 already closed (named by #100) — leaving it
could not remove 'size: now' from #7: HTTP 502 — the issue is closed either way
removed 'size: now' from #7
```

Two contradictory lines, and the second is the one a reader takes away. The
label is still on the issue. `close_issues_on_release.py`'s own docstring says
the failure is *reported and the run goes on*; here it is reported and then
denied.

The same three lines have a second symptom. `if spent and not dry` means a dry
run over an already-closed issue prints nothing about the label, while the
open-issue path at line 275 prints `would remove`. **Executed** — the dry run
says only `#7 already closed (named by #100) — leaving it`. A preview that
under-reports is the failure the `DRY_RUN` arm exists to prevent, by that
script's own stated reason for having one.

Why it matters: the job log is the only record of what the release did to the
tracker. `agent-contract` §14 — a change to what a person reads is pinned —
and nothing pins this path. No case in
`tests/test_a_declared_label_reaches_the_tracker.py` sets an issue closed
before `main()` runs, so neither symptom is covered.

### 🟡 2. `docs/branch-and-release.md` states counts that no record carries and that contradict the two places the same measurement IS recorded

`docs/branch-and-release.md:91-95`

The new paragraph says: *measured over one directory's 310 entries, 244 point
outward and every one of them carries a `sha`, against 88 that carry a `ref`
and exactly one of those 88 that names a tag.*

The same file, measured the same day, is written down twice elsewhere:

| Source | official / 310 |
|---|---|
| `phases/phase-3.md` §*An entry's `source` has four shapes* | 157 url+sha · 96 +path+ref · 5 +path · 52 plain string · 0 url+ref |
| `.github/scripts/plugin_directory_check.py:34-42` docstring | the same four numbers |

Those give **258** entries carrying a `sha` and **96** carrying a `ref`, not
244 and 88. The figures 244, 88 and *exactly one names a tag* appear in no
phase record, no ledger row and no line of `overview.md` — `grep` over the
whole work item and `docs/` finds them in this paragraph and nowhere else.

Why it matters: this is a `docs/` policy document, which outranks the work
item, and the sentence exists to make an argument about who breaks when the
merge rule is broken. `agent-contract` §5 is the rule the repository bought
for exactly this — a count can be checked while the claim it stands for
cannot, and one such fact reached five documents before a round found it
false. Either the numbers are a narrower population nobody recorded, or they
are wrong; a reader has no way to tell.

### 🟡 3. `tracker_labels.py` is the one new script with no `console.to_utf8()`, and it prints an em dash

`.github/scripts/tracker_labels.py:135` (its `main`), printing at `:149` and `:164`

Both other new scripts call it —
`.github/scripts/publish_release_note.py:195` and
`.github/scripts/plugin_directory_check.py:238` — and `hooks/console.py`'s own
docstring says the call site is *each entry point's `__main__`*, because every
one of these is runnable on its own. `tracker_labels.py` prints
`DRY_RUN — nothing will be written` and a trailing `The workflow that runs
when \`main\` moves creates these:` block, the first of which carries U+2014.

Under a console that cannot encode it — cp949, cp932, cp936, or a bare
`LC_ALL=C` — `print` raises `UnicodeEncodeError` and the process dies. In the
workflow the runner is UTF-8, so the `--apply` arm is safe; the exposed arm is
`--check`, which this module's own case docstring calls *the arm a person
types*. Nothing pins the call:
`tests/test_console_is_not_utf8.py` enumerates `hooks/` only, and of the nine
scripts under `.github/scripts/` five call it and four do not, so the tree
gives no answer either.

### 🟡 4. A case named for the opposite of what it now asserts, and a ledger row anchored on that name

`tests/test_a_release_is_sized_by_a_criterion.py:226`

The body now asserts `**Nothing schedules from this label**` and
`One thing reads it, and only to spend it.` The function is still named for
the sentence that was deleted. The sibling case in `tests/test_release_hygiene.py`
was renamed in the same commit when the same thing happened to it, so the
build already took the other decision once.

It is not only a name. `seal/ledger/1790076050-the-release-tail-is-three-acts-no-document-names.md`
row T1 claims *one thing reads it* and anchors that claim on
`tests/test_a_release_is_sized_by_a_criterion.py#test_the_label_is_two_states_and_nothing_reads_it`.
The coordinate a reader opens to check the claim is named for its negation.

The cost of fixing it is one re-stamp of the branch's own fragment, which is
not a shared file.

### 🟡 5. The R2 removal is right and no document says so, and the record cites a section that says the opposite

`seal/specs/1790076050-the-release-tail-is-three-acts-no-document-names/phases/phase-4.md:61-69`

The record says the removal is what *the handoff and `CONTRIBUTING.md`
§*Running the checks* both route the same way.* §*Running the checks* is the
pytest-and-ruff section; the only thing it says about the ledger is a
command. The section that does carry a removal arm is §*House rules*, and read
literally it does not cover this case:

> - the claim still holds and you have re-read it — run `evidence-check --reverify .`
> - the claim went with the code — **remove the row and write the new claim into your own fragment.**
>
> So a claim leaves `seal/ledger.md` when the code it was about does.

R2's code went nowhere. Both its anchors still resolve — the build says so and
`evidence-check` confirms it. What happened is a third thing: the claim was
falsified by code this branch **added**. Neither arm applies, and
`CLAUDE.md`'s own copy of the rule is the same two arms.

I agree with the act. Re-stamping R2 with `--reverify` would leave a false
claim standing with a fresh hash, which is worse than any bookkeeping. What is
wrong is that the record points a reader at grounds that are not there, and
that the policy has no arm for a case a branch will hit again — the next
branch that makes an existing claim false by adding something has the same
choice to make with the same two documents silent.

### 🟡 6. The restated hygiene case checks its two flags against the whole file, not against the one call

`tests/test_release_hygiene.py:1083-1095`

`edits <= 1` binds the count to the call. The two assertions under it do not:
`'"--remove-label"' in folded` and `'"--add-label"' not in folded` are searches
over the whole folded source, so nothing ties either flag to the `issue edit`
that `edits` counted.

Concretely: a future `["gh", "issue", "edit", str(n), "--repo", repo,
"--remove-label", label, "--add-assignee", who]` passes every assertion. So
does an `issue edit` that gained `--milestone` or `--body`. The case's own
message says the property is *what makes a re-run and a force-push safe to
reason about*; a `--body` write is neither idempotent in the sense that
matters nor the removal the case says the one edit is.

On the question the prompt asks — whether the verb was let in under a
description of itself — the answer is **no, the restatement is sound in its
reasoning**: the five other verbs are still forbidden outright, the count is
capped at one, adding a label is refused, and the property named is genuinely
idempotency rather than the verb. The gap is in how tightly the two flag
assertions are bound, and it is cheap to close by pinning the argument tuple
the way the line above it already pins the close.

### ⬜ The closing records state three figures the tree contradicts, and omit a fifth re-stamped row

`seal/specs/1790076050-the-release-tail-is-three-acts-no-document-names/overview.md:5`
and `.../phases/phase-4.md:79-82`

- `overview.md:5` says the fragment adds **14 anchors**. **Executed**:
  `evidence-check` reports `13 ok` for that file, and a mechanical count of
  backticked coordinates in it returns 13, none duplicated. T1 has 5, T2 has
  5, T3 has 3.
- `phase-4.md:81` says `1452 ok … up from 1440 (R2's two anchors out, the
  fragment's fourteen in)`. **Executed**: the base is 1440 and the target is
  1452, so the total is right — but `seal/ledger.md` alone goes 1440 → 1439,
  which is **one** anchor out, not two. R2's document anchor is byte-identical
  to S4's, and the checker counts a file's coordinates once. The arithmetic
  lands on 1452 both ways, which is why nothing caught it.
- `overview.md:5` lists `G5, S4 and S3 re-read and re-verified`. A fourth row
  was also re-stamped and carries a new `Re-read 2026-09-22` note:
  **S9**, at `seal/ledger.md:2036`, whose
  `docs/release-checklist.md#"## 6. After the merge"` anchor moved when §6
  gained the two boxes. The row itself is correct and thorough; only the
  closing memo's list of what was touched is short by one.
- `questions.md:29` states, under a heading that says the tree answered it and
  dated the same day, *An external entry pins `source.url` plus `source.sha`* —
  which is the frame claim `phases/phase-3.md` measured false that afternoon.
  `overview.md` records the divergence; this sentence was not corrected while
  `spec.md` and `plan.md` were corrected for a different reason.

Left out of `Needs a fix`: these are the run's own paperwork rather than the
tool (`docs/review-chain-spec.md` §*The last round verifies*).

### ⬜ Two reads of the same issue where one would do

`.github/scripts/close_issues_on_release.py:257-258`

`issue_labels(repo, issue)` and `issue_state(repo, issue)` each call
`_issue_api`, which is one `gh api repos/{repo}/issues/{number}` each, and
`_issue_api` already returns the whole issue — state and labels together.
**Executed**: one pull request naming one issue produces reads `[100, 7, 7]`.

It costs one extra API call per closed issue per release and nothing else; the
workflow's own token gets 1,000 requests an hour against a repository and a
release closes a handful of issues. Naming it because the label read was added beside
an existing read of the same object rather than through it, and the sibling
module was just consolidated for exactly that reason (ledger row T3).

### ⬜ The release body goes to `gh` as one argv element

`.github/scripts/publish_release_note.py:179-191`

`create()` passes the whole section as a single `--notes` argument.
**Executed** over the real `CHANGELOG.md`: the largest released section is
0.9.1 at 33,553 characters, against a per-argument limit of 131,072 bytes on
Linux. Four times the headroom, so nothing is wrong today.

Naming it because the whole design of this script is that *a failed job at the
tag is a release that stops after `main` has already moved*, and this is the
one failure mode in it that grows with the size of a release rather than with
a convention anybody controls. `gh release create --notes-file -` takes the
body on stdin and has no such ceiling.

### ⬜ A real domain and two real organisation names enter the tree, and the checker cannot see any of them

`.github/scripts/plugin_directory_check.py:81-85`

`clau.de` and `anthropics/claude-plugins-official` /
`anthropics/claude-plugins-community` are all new to the tree in this branch —
`git grep` at the base finds none of them.

`tests/test_no_real_identifiers.py` passes, and it passes for a reason that is
not the reason the frame gives. Its `DOMAIN_RE` matches only
`com|io|net|org|ai|dev`, so `clau.de` is invisible to it; and it checks
domains and user paths only, so an organisation name is invisible to it by
construction. `CLAUDE.md`'s rule says *never make a test pass by inlining a
real domain, path, or org name*, and `ALLOWED_DOMAINS` already carries
`claude.com` as *official docs this plugin is built against*.

The placement is defensible — `spec.md`'s grounding row reasons it through,
and a command that reads two specific public repositories cannot read them
without naming them. What is worth saying out loud is that the green build
is not what cleared it: a reader who sees the check pass will conclude the
rule was satisfied, and it was only not-checked. The honest form is to add
`clau.de` to `ALLOWED_DOMAINS` with the same one-line reason `claude.com`
carries.

### ⬜ The section says one thing reads the label; a second step in the same workflow also reads it

`docs/issues-and-milestones.md`, the paragraph beginning `**One thing reads it,
and only to spend it.**`

On the prompt's question — whether the replacement is true of the tree after
this branch — **it is, and the pair of paragraphs is well made.** *Nothing
schedules from this label* is exactly the property the deleted literal was
protecting, the new paragraph names the one workflow, and
`tests/test_a_release_is_sized_by_a_criterion.py` pins both halves.

One thing the sentence does not cover: `tracker_labels.py#missing` reads
whether `size: now` exists on the tracker to decide whether to create it, and
that step runs in the same workflow. *One workflow* stays exactly true; *one
thing* is the word used. Nothing turns on it — the section is about the label
on an issue — so this is a note rather than a request.

### ❓ The broad gate, and whether #499's class reaches further

The full suite, the repository-wide lint and the typecheck were **not run**.
`agent-contract` §2 makes the broad gate one act with one owner and
`agents/warden.md` hands it to nobody; it is the sealer's single run, after
the rounds settle. The spawn prompt agrees and asked for none, so nothing was
declined.

On #499: I looked for the class and did not find it reaching another case.
Four other assertions in the suite assert a word is absent from a tool's
output — `tests/test_the_seal_is_taken_once_by_the_sealer.py:2802` (`clean`),
`tests/test_the_payload_meter_says_what_it_measured.py:495` (`measured`),
`tests/test_local_mode_resolves_under_the_git_dir.py:261` (`uncommitted`),
`tests/test_session_cost.py:2766` (`resumed`). The exposure needs the asserted
stream to carry the checkout path, which reaches it through `sys.executable`
in a `Broad gate` row. #499's assertion reads `result.stderr`, where
`broad_gate.py` puts the command line; the sealer one reads `out.stdout`,
which on success carries the panel and the panel carries no path. **Read, not
executed** — I did not build a venv at a path containing `clean` to prove the
negative, and the answerer for the class as a whole is whoever owns
`tests/test_the_gate_names_every_step_ci_runs.py`, per #499.

## What would happen when the release actually runs

**Executed against the real tree**, since no case can run the job:

- `section_body` finds the section for 0.13.0, 0.12.3, 0.12.1 and 0.11.4 in
  the real `CHANGELOG.md` — 4,152 / 7,112 / 20,984 / 12,592 characters — and
  no body runs past the next `## ` heading.
- `title_from` over the real tagged commit messages produces
  `0.13.0 — a spec waited for a fold nobody built, …` for v0.13.0 and the same
  shape for v0.12.1 and v0.11.4, each `from the tagged commit's \`release:\`
  line`; v0.12.3, whose line carries no symptoms, falls back to the tag name
  and says so. That is A4's both branches on real data.
- `docs/release-checklist.md:176` prescribes the title line with U+2014, and
  every tagged commit in this repository's history carries U+2014. The regex
  matches what the tree has.
- The workflow's `fetch-depth: 0` is what makes `git log -1 <tag>` resolve:
  `actions/checkout` fetches `+refs/tags/*:refs/tags/*` on the all-history
  path, so the tag ref is local. **Read, not executed.**
- `permissions: contents: write` is the minimum `gh release create` needs and
  the job declares nothing else; the case forbids `issues:`,
  `pull-requests:` and `packages:`. The trigger cannot collide with the two
  workflows already in the tree — `close-issues-on-release.yml` is
  `push: branches: [main]`, `hygiene.yml` is `pull_request`, and neither fires
  on a tag.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | an already-closed issue reports a removal that failed, and a dry run over one says nothing about the label | `.github/scripts/close_issues_on_release.py:263-272` | open | Executed in a clone: the job log prints `could not remove …` and then `removed …` for the same issue, and the label survives. No case sets an issue closed before `main()` runs |
| 2 | `docs/branch-and-release.md`'s 244 / 88 / *exactly one names a tag* are recorded nowhere and contradict the 258 / 96 the phase record and the script docstring carry for the same file on the same day | `docs/branch-and-release.md:91-95` | open | Read: `phases/phase-3.md`'s table sums to 310 and gives 157+96+5 with a `sha`; `grep` over the work item and `docs/` finds 244 and 88 in this paragraph alone |
| 3 | the one new script with no `console.to_utf8()`, printing U+2014 from an arm a person types | `.github/scripts/tracker_labels.py:135` | open | Read: both sibling new scripts call it at `:195` and `:238`; `hooks/console.py` says each entry point carries the call; `tests/test_console_is_not_utf8.py` enumerates `hooks/` only |
| 4 | a case named for the sentence it no longer asserts, and ledger row T1 anchors its claim on that name | `tests/test_a_release_is_sized_by_a_criterion.py:226` | open | Read: the body asserts `One thing reads it`; the sibling case in `tests/test_release_hygiene.py` was renamed in the same commit for the same reason |
| 5 | the R2 removal cites `CONTRIBUTING.md` §*Running the checks*, which says the opposite, and the arm that exists is conditioned on code that went away | `seal/specs/1790076050-the-release-tail-is-three-acts-no-document-names/phases/phase-4.md:61-69` | open | Read: §*House rules* gives two arms, both about the code leaving; R2's anchors still resolve and `evidence-check` agrees. The act is right; the grounds are not there |
| 6 | the restated hygiene case checks `--remove-label` and `--add-label` against the whole file rather than against the one `issue edit` it counted | `tests/test_release_hygiene.py:1083-1095` | open | Read: an `issue edit` carrying `--remove-label` plus `--add-assignee` passes every assertion. The restatement's reasoning is sound; the binding is not |
| ⬜ | the closing records state 14 anchors (13), `R2's two anchors out` (one), and omit S9 from the re-stamped list; `questions.md:29` keeps a measured-false frame claim | `seal/specs/1790076050-the-release-tail-is-three-acts-no-document-names/overview.md:5` | answered | ⬜ — a correction to this run's own paperwork, not to the tool, so `Needs a fix` does not count it. The measured figures are in the finding above |
| ⬜ | two `gh api` reads of the same issue where `_issue_api` already returns both fields | `.github/scripts/close_issues_on_release.py:257-258` | answered | ⬜ — executed: reads `[100, 7, 7]`. One extra call per closed issue per release, against a 1,000/hour budget. Raised for the record, not commissioned |
| ⬜ | the release body reaches `gh` as one argv element; largest real section 33,553 of a 131,072 limit | `.github/scripts/publish_release_note.py:179-191` | answered | ⬜ — executed over the real `CHANGELOG.md`. Four times the headroom today. `--notes-file -` removes the ceiling if anybody wants it |
| ⬜ | `clau.de` and two real organisation names enter the tree and `tests/test_no_real_identifiers.py` cannot see any of them | `.github/scripts/plugin_directory_check.py:81-85` | answered | ⬜ — read: `DOMAIN_RE` covers `com\|io\|net\|org\|ai\|dev` only and checks no organisation names. The placement is reasoned in `spec.md`; the green build is not what cleared it |
| ⬜ | *One thing reads it* — the reconcile step in the same workflow also reads the label, to decide whether to create it | `docs/issues-and-milestones.md` §*A label answers what it is about, and survives the move* | answered | ⬜ — *one workflow* is exactly true and the section is about the label on an issue. The rewording IS true of the tree, which is the question the prompt asked |
| ❓ | the broad gate — the full suite, the repository-wide lint and the typecheck | `skills/verify/scripts/broad_gate.py` | out of verified scope | `agent-contract` §2 and `agents/warden.md` hand it to the sealer; the prompt asked for none, so nothing was declined. Answerer: the `sealer`, in its single run |

## Executed probes

| What was run | Result |
|---|---|
| `git clone --no-local` of the worktree, checked out at `b29c8605`; every probe below ran there and the clone was removed afterwards | the worktree was never written to except for this report |
| probe: `close_issues_on_release.main()` over an issue already closed, carrying `size: now`, with a tracker that refuses the edit | `could not remove 'size: now' from #7: HTTP 502 — the issue is closed either way` followed by `removed 'size: now' from #7`; the label is still on the issue |
| probe: the same issue under `DRY_RUN=1` | `#7 already closed (named by #100) — leaving it` and nothing about the label; the open-issue path prints `would remove` |
| probe: counting `_issue_api` reads for one pull request naming one issue | `[100, 7, 7]` — the same issue read twice |
| probe: `publish_release_note.section_body` over the real `CHANGELOG.md` for 0.13.0 / 0.12.3 / 0.12.1 / 0.11.4 | 4152 / 7112 / 20984 / 12592 characters, and no body contains a later `## ` heading |
| probe: `publish_release_note.title_from` over the real tagged commit messages of v0.13.0 / v0.12.3 / v0.12.1 / v0.11.4 | three read the `release:` line; v0.12.3 falls back to the tag name and says which it used |
| probe: largest released `CHANGELOG.md` section, against the per-argument limit | 33,553 characters (0.9.1) of 131,072 |
| `python3 skills/evidence-check/scripts/evidence_check.py .` in the clone at `b29c8605` | `1452 ok · 0 drifted · 0 broken`; the work item's fragment reports `13 ok` |
| the same at `6d410023` | `1440 ok`; `seal/ledger.md` alone goes 1440 → 1439 across the range |
| mechanical count of backticked coordinates in the ledger fragment | 13 total, 13 unique |
| `correction_check.py --range 6d410023...b29c8605` | `no merge commit in 6d41002..b29c860, so no correction can have been dropped at one` — exit 0 |
| `bin/test tests/test_a_script_says_which_interpreter_it_needs.py tests/test_a_document_that_names_a_script_says_how_to_reach_it.py tests/test_one_word_one_meaning.py -q` — the three constraints `plan.md` named that the handoff's eight modules do not cover | `76 passed, 7 skipped` |
| the eight modules the orchestrating session already ran, `ruff check` and `ruff format --check` | not re-run — `agent-contract` §3, the handoff carries them |
| the broad gate — the full suite, the repository-wide lint, the typecheck | **not yet.** It is the sealer's single run, after the rounds settle, and this round did not take it |
| the tag-triggered job running on GitHub, and the live `gh label create` on the tracker | **not run here and not runnable here** — `agent-contract` §6 withholds both from every agent. `overview.md` names the releasing session |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| The arm neither `CONTRIBUTING.md` §*House rules* nor `CLAUDE.md` carries: a `seal/ledger.md` claim falsified by code a branch ADDED, whose own anchors still resolve. The act taken here is right and undocumented | `seal/follow-up.md` | the repository owner, at the next change to `CONTRIBUTING.md` §*House rules* |
| Whether `console.to_utf8()` is owed by every `.github/scripts/` entry point as a class — five of nine call it and nothing pins any of them. Finding 3 fixes the one instance this branch introduced; the class is bigger than this branch | `seal/follow-up.md` | whoever owns `hooks/console.py`'s convention |
| `tests/test_the_gate_names_every_step_ci_runs.py#test_a_repository_with_no_hygiene_workflow_is_sealed_exactly_as_before` reddening in any checkout whose path contains `release` — **already deferred**, as issue #499, by the build. Not re-litigated here; I looked for the class reaching a second case and did not find one | issue #499 | whoever owns that module; the `sealer` first, since it decides whether the broad gate meets it from where it stands |

## Paste-ready fixes

### 1 — `.github/scripts/close_issues_on_release.py`, the already-closed branch

```python
        if state == "closed":
            print(f"#{issue} already closed (named by #{source}) — leaving it")
            # A closed issue still carrying it is one a previous run closed
            # before this line existed, or one closed by hand. The label is
            # spent either way and the removal is idempotent, so taking it
            # off here costs one call and leaves no stale ones behind.
            #
            # The report is guarded on the write, the way the open-issue path
            # below is. Unguarded, a refused removal printed `could not
            # remove …` and `removed …` for the same issue, and the second is
            # the line a reader believes. The dry arm prints here too, because
            # a preview that is silent about half the act is the failure
            # `DRY_RUN` exists to prevent.
            if spent and dry:
                print(f"would remove {SPENT_ON_CLOSE!r} from #{issue}")
            elif spent and drop_label(repo, issue, SPENT_ON_CLOSE):
                print(f"removed {SPENT_ON_CLOSE!r} from #{issue}")
            continue
```

Two cases to plant in `tests/test_a_declared_label_reaches_the_tracker.py`,
under the A11 heading:

```python
def test_an_already_closed_issue_reports_no_removal_that_failed(monkeypatch, capsys):
    """The path no case reached. An issue already closed and still carrying
    the label is the ordinary re-run and force-push case, and the report
    there was unguarded — so a refused write produced `could not remove …`
    and `removed …` in one job log, with the tracker in the state the first
    line describes and the second denies."""
    tracker = Tracker(issues={7: [LABEL]}, pulls={100: "Closes #7"}, refuse={7})
    tracker.states[7] = "closed"
    mod = wire_closer(monkeypatch, tracker, ["feat: a thing (#100)"])
    mod.main()
    out = capsys.readouterr().out
    assert "could not remove" in out
    assert f"removed {LABEL!r} from #7" not in out, (
        "the log says the label came off an issue it is still on"
    )
    assert LABEL in tracker.issues[7]


def test_a_dry_run_over_an_already_closed_issue_names_the_label_too(
    monkeypatch, capsys
):
    """A preview that is silent about half the act. The open-issue path says
    `would remove`; this one said nothing, so a person reading a dry run
    concluded the label was not in scope."""
    tracker = Tracker(issues={7: [LABEL]}, pulls={100: "Closes #7"})
    tracker.states[7] = "closed"
    mod = wire_closer(monkeypatch, tracker, ["feat: a thing (#100)"])
    monkeypatch.setenv("DRY_RUN", "1")
    mod.main()
    assert f"would remove {LABEL!r} from #7" in capsys.readouterr().out
    assert LABEL in tracker.issues[7]
```

Shown red first: run both against the file as it stands at `b29c8605`. The
first fails on the `removed …` line, the second on the missing `would remove`.

### 2 — `docs/branch-and-release.md:91-95`

Restate from the figures the tree actually records, or record the measurement
that produced 244 / 88 with the command that produced it. The first form:

```markdown
**A third reader points at those commits now, and it is outside this
repository.** A plugin directory lists an external plugin by pinning a commit
of its source repository — measured 2026-09-22 over one directory's 310
entries, 258 carry a `source` object and every one of them carries a `sha`,
while 52 carry `source` as a plain in-repository string and pin nothing at
all; 96 of the 258 also carry a `ref`. The counts and how they were taken are
in `seal/specs/1790076050-the-release-tail-is-three-acts-no-document-names/phases/phase-3.md`.
So the rule above stopped
```

If 244 and 88 are a narrower population — outward-pointing entries only — then
the sentence has to say so and `phases/phase-2.md` has to carry the
measurement, because a figure in a `docs/` policy document with no record
behind it is the class `agent-contract` §5 exists for.

### 3 — `.github/scripts/tracker_labels.py`

```python
import argparse
import importlib.util
import os
import sys

sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "hooks")
)
import console

HERE = os.path.dirname(os.path.abspath(__file__))
```

and, as the first line of `main`, matching both sibling scripts:

```python
def main(argv=None):
    console.to_utf8()
    parser = argparse.ArgumentParser(
```

Shown red first: run `--check` with `PYTHONIOENCODING=cp949 PYTHONUTF8=0` and
a tracker missing the label; it raises `UnicodeEncodeError` on the
`DRY_RUN — ` line, or on `\nThe workflow that runs when \`main\` moves creates
these:` with `DRY_RUN` unset.

### 4 — `tests/test_a_release_is_sized_by_a_criterion.py:226` and the ledger fragment

```python
def test_the_label_is_two_states_and_nothing_schedules_from_it():
    """`size: now` is where the sizing judgment stops being made again from
    scratch. A reader has to be able to apply it without asking, which takes
    the meaning, the absence, and the fact that no automation SCHEDULES from
    it.

    The name moved with the literal. It used to say `nothing_reads_it`, and
    after #450 one thing does — so a case named for its own negation was the
    coordinate `seal/ledger/…` row T1 pointed a reader at to check the claim
    *one thing reads it*.
    """
```

Then, in
`seal/ledger/1790076050-the-release-tail-is-three-acts-no-document-names.md`,
T1's fourth coordinate takes the new unit name, and the hash comes from the
scoped write form the fragment's own header names:

```bash
python3 skills/evidence-check/scripts/evidence_check.py --reverify \
  --ledger seal/ledger/1790076050-the-release-tail-is-three-acts-no-document-names.md .
```

`overview.md`'s divergence row and `phases/phase-4.md`'s mutation table each
name the old unit once in prose and take the new name with it.

### 5 — `seal/specs/1790076050-the-release-tail-is-three-acts-no-document-names/phases/phase-4.md:61-69`

```markdown
**R2 is the case the handoff described and the only one that arose.** Its
claim ended *and **nothing reads it***, which this phase makes false. Both of
its anchors still resolve, so this is not the anchor-removal case `CLAUDE.md`
names — and it is not `CONTRIBUTING.md` §*House rules*' removal arm either,
which is conditioned on *the claim went with the code* and closes with *a
claim leaves `seal/ledger.md` when the code it was about does*. This claim's
code went nowhere. What went false is the claim, falsified by code this branch
**added**, and no document carries an arm for that.

The row is removed and the corrected claim rewritten in the branch's own
fragment, because the only alternative the documents offer is
`--reverify`, which would leave a false claim standing under a fresh hash.
The missing arm is a deferral rather than a silent precedent: it is in
`seal/follow-up.md` with the owner named.
```

and a row in `seal/follow-up.md`:

```markdown
| `CONTRIBUTING.md` §*House rules* and `CLAUDE.md` §*A change writes fragments* give two arms for a drifted `seal/ledger.md` row — the claim holds, or the claim went with the code. A claim falsified by code a branch ADDED, whose own anchors still resolve, is a third case and both documents are silent. 1790076050 took the removal arm on its own reasoning; the next branch in that position has the same choice with the same silence | the repository owner |
```

### 6 — `tests/test_release_hygiene.py:1083-1095`

```python
    edits = folded.count('"gh", "issue", "edit"')
    assert edits <= 1, (
        f"{edits} `issue edit` calls; there is one, and it is the removal of "
        "a spent sizing label"
    )
    if edits:
        # The whole argument tuple, not two flags looked for anywhere in the
        # file. Unbound, an `issue edit` that gained `--add-assignee` or
        # `--body` passed both assertions as long as `--remove-label` still
        # appeared somewhere — and the property this case protects is that
        # every write here is idempotent, which is about the call rather than
        # about which words the file contains.
        assert (
            '"gh", "issue", "edit", str(number), "--repo", repo, '
            '"--remove-label", label,' in folded
        ), (
            "the script's one `issue edit` is not the label removal spelled "
            "argument for argument. Adding a label here is the sibling's act "
            "at the squash, and a second writer is how two scripts disagree "
            "about the current answer"
        )
        assert '"--add-label"' not in folded, "the script adds a label"
```

Shown red first: append `"--add-assignee", "someone",` to `drop_label`'s
argument list and run the case. It passes at `b29c8605` and fails after this
change.

Needs a fix: yes — findings 1, 2, 3, 4, 5 and 6. Finding 1 is the one that
changes what the release writes; 2 is a figure in a policy document that no
record supports; the other four are a crash path, two records that misname
what they point at, and a case whose two assertions are not bound to the call
they judge.
Loses a record or crashes: no — finding 1 writes a false line into a job log
rather than losing a record, and finding 3's crash is reachable only from a
local console the release does not use. Nothing found leaves the root, and no
path this release exercises crashes.

## Proof

Opened and read in full:

- `seal/specs/1790076050-the-release-tail-is-three-acts-no-document-names/` —
  `routing.md`, `spec.md`, `plan.md`, `questions.md`, `overview.md`,
  `survivors.md`, `changelog.md`, `phases/phase-4.md`; `phases/phase-1.md`,
  `phases/phase-2.md` and `phases/phase-3.md` in the regions the findings cite
- `seal/ledger/1790076050-the-release-tail-is-three-acts-no-document-names.md`
- `seal/ledger.md` — the five rows this range changed (G5, S4, S3, S9, R2),
  before and after
- `.github/scripts/publish_release_note.py`,
  `.github/scripts/plugin_directory_check.py`,
  `.github/scripts/tracker_labels.py`
- `.github/scripts/close_issues_on_release.py` and
  `.github/scripts/label_merged_on_release_branch.py` — the diff and the
  enclosing functions
- `.github/workflows/publish-release.yml`,
  `.github/workflows/close-issues-on-release.yml`, `.github/workflows/hygiene.yml`
  (head), `.github/workflows/label-merged-on-release-branch.yml` (trigger and
  permissions)
- `tests/test_a_release_publishes_its_note.py`,
  `tests/test_the_plugin_directory_answers_the_box.py`,
  `tests/test_a_declared_label_reaches_the_tracker.py`, and the diffs of
  `tests/test_release_hygiene.py` and
  `tests/test_a_release_is_sized_by_a_criterion.py`
- `tests/test_no_real_identifiers.py`, `tests/test_console_is_not_utf8.py`
  (the binding case), `tests/test_the_gate_names_every_step_ci_runs.py` (the
  #499 region and the fixture config)
- `docs/branch-and-release.md` (the new paragraphs),
  `docs/release-checklist.md` §§5–6, `docs/issues-and-milestones.md` (the
  rewritten section), `CLAUDE.md`, `CONTRIBUTING.md` §*House rules* and
  §*Running the checks*, `hooks/console.py`
- `skills/verify/scripts/broad_gate.py` and
  `skills/code-review/scripts/chain_check.py` — the panel and the verdict
  vocabulary, read to place this report's own rows
