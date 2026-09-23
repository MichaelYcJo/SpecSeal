# Round 1 report — 1790154759-the-review-arm-asks-where-no-reviewer-compares

| Field | Value |
|---|---|
| Round | 1 |
| Target | the whole branch, `f8f1c9de..17327c53` |
| Target SHA | 17327c53d3030d1efb7eb9449bba7d82125b9ebb |
| Reviewer | specseal:warden on claude-opus-5-5 |

## What this round was asked

Round 1 of #518 (PR #528), the whole branch against `release/v0.14.0`.
Stage 1: does the decision (the review arm keeps asking on a change
confined to `docs/` and `seal/`) follow from `spec.md`'s measurements, and
do M1 to M3 hold when re-derived from `git log` over the release branch.
Stage 2: do the new cases fail under the mutation the issue fears (the
parity arm's path line leaking into the review arm), does the wording-pin
case pin a rule or prose, do the four re-stamped `seal/ledger.md` rows still
hold, and does anything in the README pair or `CONTRIBUTING.md` now
disagree with the new §*Review arm* rows. The handoff labelled M4's
lower bound unverified and asked whether the paragraph citing it states only
what was measured. No full suite, lint or broad gate was run: those are the
sealer's.

## Summary

The decision holds, and the code half is sound: both behaviour cases go red
under two different shapes of the leak, and M1, M2 and M3 reproduce
exactly. Two things need a fix before the grounds ship.

- **The grounds paragraph describes the measurement wrongly** (🟡 1). It says
  every docs/seal-only change that reached a reviewer produced defects, with
  #514 as the example. M1 says no such change ever reached a reviewer, and
  #514 changed four test files. It also calls the never-reviewed commits the
  population that "measured empty", when nothing measured them. The decision
  survives on M3 and M4; the sentence that states why does not. The same
  claim sits in a shipped hook docstring and a test docstring.
- **Half of the parity line can leak and every gate case stays green** (🟡 2).
  The cases stage only a `docs/` file. A review-arm exemption for
  commits confined to `seal/` alone, the ledger-only commit #517's fold
  question is about, passes all 140 gate cases. Ledger row R1 claims the
  `seal/` half as executed.

## Findings

### 🟡 1 — The paragraph that justifies the decision misstates what was measured

`docs/review-chain-spec.md` §*Review arm — opt-in: `seal/` at the repo
root*, the paragraph **Why this arm has no document-root line** (read):

> Every docs/seal-only change that reached a reviewer produced real defects
> in `docs/`: #514's fold opened seven findings … The docs/seal-only commits
> that never reached a reviewer were planning bookkeeping in `docs/flow.md` …
> So the parity arm's line would exempt the one population that measured
> positive and buy nothing on the one that measured empty.

Three statements in it do not match `spec.md`'s own measurement, and I
re-derived each (executed, see probes):

- **No docs/seal-only change ever reached a reviewer.** M1 says so, and my
  probe agrees: 88 work items added a `round-1.md`, and the commit that added
  it touched a path outside the two roots in all 88. #514's squash
  `f2943c04` touched `tests/test_a_declared_label_reaches_the_tracker.py`,
  `tests/test_a_release_publishes_its_note.py`,
  `tests/test_the_plugin_directory_answers_the_box.py` and
  `tests/test_the_release_tail_does_not_end_at_the_tag.py`. `spec.md` M3 calls
  it "the nearest thing to" such an item; the paragraph promotes it to the
  item itself. "Every docs/seal-only change that reached a reviewer" is a
  statement about an empty set.
- **The unreviewed population did not measure empty.** It was never reviewed,
  so nothing measured it. "Measured empty" turns an absence of review into an
  absence of defects, which is the inference this work item exists to refuse.
- **Not all seventeen were planning bookkeeping.** 13 touch `docs/flow.md`.
  Three touch only `docs/one-root-by-lifetime.md` and its Korean edition, the
  design record for the document roots, and one (`b7e7dd44`) touches only
  `seal/specs/`.

Why it matters: this paragraph is the only place a future reader finds the
reason the review arm has no path line. A reader who checks it against M1
finds the example contradicts the claim, and the decision starts to look
arbitrary again, which is the situation the issue came from. The argument
that does hold is in M3 and M4: when review looks at `docs/` and the ledger,
it finds defects there. That is enough, and it is what the fix says.

The same misstatement is in shipped code and in a test docstring (read), so
the fix covers the class:

- `hooks/commit-review-gate.py#touches_code` docstring: "a docs-only change
  is exactly where the measured findings were". The findings were located in
  `docs/`; the changes that produced them were not docs-only.
- `tests/test_chain_hooks_hardening.py#test_the_review_arm_asks_on_a_document_only_commit`
  docstring: "the only docs/seal-only change that reached a reviewer (#514's
  fold)".
- The pin in `test_the_review_arms_missing_path_line_is_written_where_it_is_met`
  asserts the phrase "the one population that measured positive", so it
  moves with the paragraph (see ⬜ 3).
- The work item's own records carry it too. Those are paperwork and are the
  correction row below, not this finding.

The fix was applied in the probe clone and the pin case, the line-wrap
case, the one-word case and the no-real-identifiers case passed with it
(executed).

### 🟡 2 — The `seal/` half of the parity line can leak into the review arm unseen

The issue fears the parity arm's line, `docs/` and `seal/`, reaching the
review arm. Both new behaviour cases stage `docs/policies/note.md` only
(read). Against the whole line they work: adding
`and touches_code(cwd, invocations)` to the review arm's condition turns both
red, and so does an early return in `judge` for a docs-only commit
(executed).

A partial leak is not caught. With the review arm exempting any non-empty
commit whose paths all start with `seal/`, the two gate modules report
`140 passed` (executed). That is not a contrived mutation. A ledger-only or
records-only commit is exactly what #517 item 3 asks about for the fold's last
step, and this work item's own paragraph cites 26 fixed ledger-only findings
as a reason not to draw that line. Nothing pins it.

Ledger row R1 in `seal/ledger/1790154759-the-review-arm-asks-where-no-reviewer-compares.md`
also claims, as **Executed**, that "a commit confined to `docs/` and `seal/`
… is stopped exactly as a code change is". Only the `docs/` half was
executed.

The fix parametrises the first case over one path per root. It was applied
in the probe clone: green on the clean hook, and the `seal/ledger.md`
parameter fails under the `seal/`-only mutation while the `docs/` one passes
(executed). The test's hash changes, so R1 needs a `--reverify`, and its
Verified-behavior cell should name the `seal/` mutation.

### ⬜ 3 — The prose pin holds one phrase of the argument, not the rule

`test_the_review_arms_missing_path_line_is_written_where_it_is_met` pins four
things (read). Three are statements of the rule: the `docs/` row's "this arm
reads no paths", the declaration row, and the wake cell's clause. §14 of the
agent contract asks for those, and pinning them is right. The fourth, "the
one population that measured positive", pins a phrase of the grounds. Any
rewording of the reasoning fails the case while the rule is unchanged, and
🟡 1 shows the reasoning does need rewording. The heading assertion
(`**Why this arm has no document-root line.**`) already proves the paragraph
exists. Dropping the phrase assertion, or pinning a fact the paragraph must
keep (such as "#514"), would pin the paragraph without pinning its wording.
The paste-ready fix under 🟡 1 swaps it for the new paragraph's phrase so
the case stays green. Either choice is acceptable.

### ⬜ Correction — the work item's records carry the same misstatement and a stale count

Paperwork, so it takes no fix row:

- `changelog.md`: "every docs-only change that reached a reviewer produced
  real defects in `docs/` … while the docs-only commits that never reached a
  reviewer were planning notes". This fragment is gathered into
  `CHANGELOG.md` at the release, so it should match whatever 🟡 1 settles on.
- `questions.md` preamble: "The only such changes that reached a reviewer
  (#514's fold)". `spec.md` §*What the measurement decides* and §*Out*, and
  `plan.md`'s summary, say the same.
- Ledger R1 and `overview.md` say the two gate modules passed with 139 cases.
  At `17327c53` they are 140 (executed). 139 was phase 1's count, before phase
  2 added the prose case, and R1 describes the prose case's mutations in the
  same sentence.

## What held (read and executed)

- **M1 reproduces** (executed): 88 work items with a `round-1.md` added on
  the release branch; 0 of the adding commits are confined to `docs/` and
  `seal/`.
- **M2 reproduces** (executed): 175 non-merge commits, 17 confined to the two
  roots, none adding a round record. 13 touch `docs/flow.md`, 4 touch
  `docs/one-root-by-lifetime.md` (one of them both), and one touches
  `seal/specs/` only. `spec.md` M2's figures are right; only the paragraph's
  summary of them is not (🟡 1).
- **M3 reproduces** (read): the three `## Verdicts` tables of
  `1790119502-four-shipped-work-items-wait-unfolded` hold four findings fixed
  in round 1 (🔴, 🟡, ⬜, ⬜) and three in round 2 (🟡, ⬜, ⬜), every Location
  in `docs/`. Round 3 fixed nothing.
- **M4's lower bound is consistent** (executed, with my own classifier, not
  the framer's): over 311 round records, 31 fixed non-🟢 findings are located
  in `docs/` alone, from 16 work items, and 26 in the ledger alone. My
  classifier differs from the framer's (I read every last-version record,
  and parse Location paths differently), so 31 against 25 is not a
  contradiction. "At least 25" and "26" in the paragraph are both at or below
  what I measured. The paragraph states only what the lower bound supports.
  `questions.md` Q3 can take my figures as a data point; it stays the
  measurement's to close.
- **The four re-stamped `seal/ledger.md` rows still hold** (read, and
  `evidence-check --strict` exit 0, `1481 ok · 0 drifted · 0 broken`,
  executed). Both opt-in headings still name `seal/` and the parity arm's
  silence row is unchanged. The orchestration routing section still places
  the asking in the spawning session. The phrase "two questions in ONE
  `AskUserQuestion` call" is unchanged, and `tests/test_review_axes.py`
  passes. No row under the `1788331011` heading gained an anchor into a
  retired `spec.md`.
- **The README pair and `CONTRIBUTING.md` agree** (read). Both READMEs'
  `commit-review-gate` rows name no paths for the review arm and call the
  parity arm's case a code commit (`코드를 커밋할 때` in the Korean edition).
  Neither contradicts the new rows. `CONTRIBUTING.md` says nothing about the
  review arm's paths. The only other statement of the path line in the tree
  is the `hooks/optin.py` comment on `WORK_ITEMS`, which calls `DOC_ROOTS` a
  classifier of `seal/` paths and says nothing about which arm uses it.
- **Q2's citation holds** (read): `routed` is computed in `judge` before any
  path is read, and the review arm's condition reads none, so
  `tests/test_routing_is_recorded.py#test_a_declared_direct_item_commits_without_a_prompt`
  covers A3.
- **The failure direction is "neither"** (read): the hook diff is two comment
  blocks and no code line.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🟡 The grounds paragraph says every docs/seal-only change that reached a reviewer produced defects, using #514 as the example. M1 says none ever did, and #514 changed four test files. It also calls the never-reviewed commits "measured empty". The same claim is in a shipped hook docstring and a test docstring | `docs/review-chain-spec.md` §*Review arm*, paragraph *Why this arm has no document-root line*; `hooks/commit-review-gate.py#touches_code`; `tests/test_chain_hooks_hardening.py#test_the_review_arm_asks_on_a_document_only_commit` | open | Executed: M1 probe (0 of 88 adders confined), `git show --name-only f2943c04` (four test paths), M2 probe (13 flow, 3 one-root only, 1 seal-only). Read: `spec.md` M1, M3 |
| 2 | 🟡 Both behaviour cases stage only a `docs/` file, so a review-arm exemption for `seal/`-only commits passes every gate case. R1 claims the `seal/` half as executed | `tests/test_chain_hooks_hardening.py#test_the_review_arm_asks_on_a_document_only_commit`; `seal/ledger/1790154759-the-review-arm-asks-where-no-reviewer-compares.md` R1 | open | Executed: `seal/`-only mutation in `judge`, two gate modules `140 passed`. The parametrised fix fails `[seal/ledger.md]` under it, and passes clean |
| 3 | ⬜ The prose pin asserts a phrase of the argument ("the one population that measured positive"), not the rule, so rewording the grounds fails it with the rule unchanged | `tests/test_chain_hooks_hardening.py#test_the_review_arms_missing_path_line_is_written_where_it_is_met` | open | Read. The other three assertions pin the rule and are right |
| ⬜ | The work item's records repeat 🟡 1's misstatement (`changelog.md`, `questions.md` preamble, `spec.md` §*What the measurement decides* and §*Out*, `plan.md` summary); R1 and `overview.md` say 139 gate cases where HEAD has 140 | `seal/specs/1790154759-the-review-arm-asks-where-no-reviewer-compares/` | correction | Read; count executed at `17327c53` |
| 🟢 | M1, M2 and M3 reproduce from the release branch | `spec.md` M1–M3 | confirmed | Executed: scratch probe over `f8f1c9de` (88 / 0; 175 / 17 / 13 flow). Read: the three verdict tables of `1790119502-four-shipped-work-items-wait-unfolded` (4 + 3, all `docs/`, one 🔴) |
| 🟢 | M4's "at least 25 / 26" is no larger than an independent count | `docs/review-chain-spec.md` §*Review arm* | confirmed | Executed: own classifier, 311 records, 31 `docs/`-only from 16 items, 26 ledger-only |
| 🟢 | The two behaviour cases fail under the whole-line leak, in two shapes | `tests/test_chain_hooks_hardening.py` | confirmed | Executed: `touches_code` added to the review arm's condition, and an early return in `judge` on a docs-only commit; both cases fail under each |
| 🟢 | The four re-stamped `seal/ledger.md` rows' claims still hold | `seal/ledger.md` | confirmed | Read each claim against the tree. Executed: `evidence-check --strict .` exit 0, 1481 ok; `tests/test_review_axes.py` green |
| 🟢 | The README pair and `CONTRIBUTING.md` do not disagree with the new rows | `README.md`, `README.ko.md`, `CONTRIBUTING.md` | confirmed | Read: no path named for the review arm in any of them |
| 🟢 | Q2: A3 is covered by the existing declaration case | `hooks/commit-review-gate.py#judge` | confirmed | Read: `routed` decided before any path is read |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_chain_hooks_hardening.py -k "document_only_commit or missing_path_line"` in a `--no-local` clone at `17327c53` | 4 passed |
| Same, with `and touches_code(cwd, invocations)` added to the review arm's `if` | 2 failed (both new behaviour cases), 2 passed |
| Same, with `if not touches_code(cwd, invocations): return [], git_dir` after `routed` in `judge` | 2 failed (both new behaviour cases), 2 passed |
| `tests/test_chain_hooks_hardening.py` and `tests/test_gate_judges_the_repo_it_commits_to.py`, review arm exempting non-empty commits confined to `seal/` | 140 passed: the leak is not caught |
| Same two modules, unmutated | 140 passed |
| 🟡 2's parametrised case, clean hook, then under the `seal/`-only mutation | 4 passed; then `[seal/ledger.md]` failed, the other 3 passed |
| 🟡 1's paragraph and pin swap applied, then the pin case, `tests/test_docs_line_wrap.py`, `tests/test_one_word_one_meaning.py`, `tests/test_no_real_identifiers.py` | 56 passed |
| `bin/evidence-check --strict .` at `17327c53` | exit 0, `1481 ok · 0 drifted · 0 broken` |
| The two gate modules plus `tests/test_review_axes.py` | 148 passed |
| Scratch probe over `git log f8f1c9de`: M1, M2, M4 | M1 88 items, 0 confined; M2 175 non-merge, 17 confined, 13 flow / 4 one-root / 1 neither; M4 311 records, 31 `docs/`-only (16 items), 26 ledger-only |
| The full suite, repository-wide lint and typecheck (the broad gate) | not yet: not run in this round; the sealer's, after the rounds settle |

Every mutation was made in the probe clone and restored with
`git checkout`; the clone and the probe script were deleted before handover.
The work item's worktree was not written, except for this report.

## Paste-ready fixes

🟡 1: `docs/review-chain-spec.md`, replace from "#518 measured it before
drawing any line." up to, not including, "A documentation pass that":

```
#518 measured whether review finds defects there before drawing any line,
and it does. Across every round record, at least 25 fixed findings sit in
`docs/` alone and 26 in the ledger alone. #514's fold, which changed `docs/`,
`seal/` and four test files, opened seven findings a later round verified as
fixed, all in `docs/`, one of them 🔴. No reviewed work item was ever confined
to the two roots, and the seventeen docs/seal-only commits on the release
branch never reached a reviewer, so nothing measured them either way. The
parity arm's line would stop asking exactly where the reviewed findings sit,
on the strength of a population nobody measured. A documentation pass that
should reach nobody is routed that way before the first edit, by declaring
`straight to the PR`; it is never inferred from the paths it touches.

# hooks/commit-review-gate.py, touches_code docstring, last paragraph:
    Only the parity arm calls this. The review arm's question is not about an
    original, and `docs/` is where a measured share of the review chain's
    fixed findings sit (`docs/review-chain-spec.md` §*Review arm*, #518).

# tests/test_chain_hooks_hardening.py,
# test_the_review_arm_asks_on_a_document_only_commit docstring, middle:
    conforms to. #518 measured it: #514's fold, which changed `docs/`,
    `seal/` and four test files, produced seven fixed findings, all located
    in `docs/`, one of them 🔴. So a commit confined to `docs/` meets the

# tests/test_chain_hooks_hardening.py,
# test_the_review_arms_missing_path_line_is_written_where_it_is_met:
-    assert "the one population that measured positive" in review_arm, (
+    assert "exactly where the reviewed findings sit" in review_arm, (
```

🟡 2: `tests/test_chain_hooks_hardening.py`, the first behaviour case,
then `evidence-check --reverify` for R1 with the `seal/` mutation named in
its Verified-behavior cell:

```
@pytest.mark.parametrize("path", ["docs/policies/note.md", "seal/ledger.md"])
def test_the_review_arm_asks_on_a_document_only_commit(repo, path):
    """...docstring unchanged except as 🟡 1 says..."""
    (repo / "seal").mkdir(exist_ok=True)
    (repo / path).parent.mkdir(parents=True, exist_ok=True)
    stage(repo, path, "text\n")
    out = run_hook("commit-review-gate.py", payload("git commit -m x", repo))
    assert decision_of(out) == "deny", (
        f"a commit confined to {path} passed the review arm with no declaration, "
        "no review mark and no waiver"
    )
    reason = json.loads(out)["hookSpecificOutput"]["permissionDecisionReason"]
    assert "[no-review]" in reason
```

Needs a fix: yes — 🟡 1 (the grounds misstate what was measured) and 🟡 2 (the `seal/` half of the line can leak unseen)
Loses a record or crashes: no


## Proof block

Files opened: `seal/specs/1790154759-the-review-arm-asks-where-no-reviewer-compares/`
`spec.md`, `questions.md`, `overview.md`, `changelog.md`, `plan.md` (grep),
`phases/phase-1.md`, `phases/phase-2.md`, `phases/phase-3.md`;
`seal/ledger/1790154759-the-review-arm-asks-where-no-reviewer-compares.md`;
the branch diff of `docs/review-chain-spec.md`, `hooks/commit-review-gate.py`,
`seal/ledger.md`, `skills/implement/orchestration.md`,
`tests/test_chain_hooks_hardening.py`; `hooks/commit-review-gate.py#judge`
and the parity arm's condition; `hooks/optin.py` (the `WORK_ITEMS` comment);
`tests/conftest.py` (`run_hook`, `decision_of`, `repo`);
`docs/review-chain-spec.md` lines 655–705 and the parity row;
`README.md` and `README.ko.md` `commit-review-gate` rows;
`seal/specs/1790119502-four-shipped-work-items-wait-unfolded/rounds/round-{1,2,3}.md`
verdict tables; `bin/test`.
