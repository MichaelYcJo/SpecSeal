# the release tail is three acts no document names — overview

📋 implement applied
· spec:     `CLAUDE.md` (§*The goal a design is chosen against*, §*A change writes fragments, never the shared file*, §*Appended is the word, and a removal is not one*, §*no real identifiers in examples or fixtures*, §*the merge method is fixed per direction*) · `CONTRIBUTING.md` §*Running the checks* · `docs/branch-and-release.md` §*Cutting a release*, §*Which button, for each direction*, §*What breaks when the last row is squashed* · `docs/release-checklist.md` §§0, 2, 3, 5, 6 · `docs/issues-and-milestones.md` §*A label answers what it is about, and survives the move* · this work item's `routing.md`, `spec.md`, `plan.md`, `questions.md` · `skills/agent-contract/SKILL.md` §§1–3, 5–7, 9, 12, 14, 15 · `skills/implement/SKILL.md` · `seal/config.md` (no `Record language` row, so these records are English)
· evidence: `seal/ledger/1790076050-the-release-tail-is-three-acts-no-document-names.md` — T1, T2, T3 added (**14** anchors, 14 unique — `evidence-check` reports `14 ok` for that file and a count of its backticked coordinates agrees). This line first said 14 when the fragment held **13**, which round 1's finding on the closing records caught; the fix pass corrected it to 13 and then added a fourteenth anchor, `close_issues_on_release.py#spend_label`, in fixing finding 1. Re-derived after that, not carried. `seal/ledger.md` — R2 REMOVED, its claim carried forward corrected as T1; **four** rows re-read and re-verified: G5, S4, S3 and **S9**, whose `docs/release-checklist.md#"## 6. After the merge"` anchor moved when §6 gained the two boxes
· verified: **executed** — each phase's own module, the two directory files read live once, `gh label list` read live once, 47 mutations across the four phases each seen red at its own case, `evidence_check.py` unscoped (1452 ok · 0 drifted · 0 broken), `correction_check.py --range`, `ruff check`/`format` over every file touched. **Read, not executed** — the tag-triggered workflow's actual run on GitHub, and the reconcile step's actual write to the tracker. **Unverified** — the full suite, lint and typecheck over the whole tree, which is the sealer's single run (`agent-contract` §2); see the table below

## Why this work exists

Three acts a release performs after the tag — publishing the note, telling the
plugin directory, and spending the `size: now` label — were each assigned to
whoever was at the keyboard, written into no document and read by no machine;
after this each is performed or answered by something that cannot forget.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| **The handoff's count of drifted ledger rows** | The spawn prompt: "Five ledger rows anchor on the exact heading phase 4 edits … at lines 1134, 1649, 2044 and two more nearby" | three rows, and a fourth the handoff did not name | Measured in phase 1 over both checkouts, whose `seal/ledger.md` is byte-identical: exactly three rows carry that anchor — G5 (1134), S4 (1649), R2 (2044). The three other `issues-and-milestones.md` anchors sit on two *different* headings that phase 4 does not edit. A fourth row, S3, drifted from a code anchor the handoff did not mention. All four were re-read; §5 is why the count was opened rather than taken |
| **Where the directory manifest lives** | #417 and `spec.md` §*Data & interfaces*: "the directory's `marketplace.json` is a public file in both repositories" | `.claude-plugin/marketplace.json` | Executed 2026-09-22: the root path is 404 in both repositories. A reader at the stated path would report *could not be read* at every release forever — A7 working and A6 answering nothing |
| **The entry shape a directory reader may assume** | `spec.md`: "The entry shape it reads is `source.url` plus `source.sha`" | four shapes, two of which pin no commit | Executed 2026-09-22: 52 of official's 310 entries and 5 of community's 2,282 carry `source` as a plain string with no url and no sha; 3 more carry `url` and `ref` and no `sha`. `entry["source"]["sha"]` raises on 57 entries today, in a file this repository does not own |
| **How the raw-content host is kept out of the tree** | `plan.md` constraint 3: "if a raw host is needed, extend `ALLOWED_DOMAINS` consciously with the reason in a comment" | neither a raw host nor an allowlist change | The documented API serves a public file's body from `api.github.com`, a subdomain `test_no_real_identifiers.py` already allows. Spending the allowlist to read a file an allowed host already serves buys nothing. **The same sweep then refused the frame's own prose**: `spec.md`'s grounding row and `plan.md`'s constraint 3 each named the host while telling the reader not to. Both were reworded to name it by description, keeping every fact — which is the narrow reading of that constraint's own "never by rewording a document into a lie", since nothing stated became untrue |
| **A4's two branches** | `spec.md` A4: the prescribed line is readable, or it is not | three shapes take the fallback, not one | Measured over this repository's tags: `v0.12.3`'s line is `release: 0.12.3` with no symptoms. A title read from it is the version alone, which is the tag name minus one character, so the two branches would differ by a `v` and the log line saying which was taken would tell a reader nothing. Symptoms are required; absent, empty and wrong-version all fall back |
| **A6's ancestry answer** | `spec.md` A6: "whether that commit is an ancestor of `main`" — two values | three | A commit this clone does not have is not a commit that is unreachable. Folding them together tells a reader to resubmit to the portal because they had not run `git fetch` |
| **The label's colour** | `spec.md` §*Judgments* 11: "the colour joins the topic labels' family" | `d4c5f9`, which is `chain: capped`'s | The topic labels carry five different colours between them, so there is no one family colour to join. `chain: capped` is this repository's other `<subject>: <state>` label and the shape `size: now`'s name was explicitly taken from — the specifying section says so — so two labels of one shape read as one shape on the tracker. Judgment 11's own last sentence is "nothing turns on either" |
| **How many pinned sentences move** | `spec.md` §*Judgments* 10 names one: `test_the_label_is_two_states_and_nothing_reads_it` (NAME NOT IN TREE — round 1's finding 4 renamed it to `test_the_label_is_two_states_and_nothing_schedules_from_it`, because a case named for the sentence it had stopped asserting is the coordinate a reader opens to check the claim) | two | Found by running the suite, not by reading: `tests/test_release_hygiene.py#test_the_script_only_ever_closes` forbade `gh issue edit`, which A11 is. Its own message says the property is *only ever closes is what makes a re-run and a force-push safe to reason about* — the property was never the verb, and both new acts are idempotent. Restated rather than relaxed, in the same commit (§14) |
| **Phase order** | `plan.md` Phases table, phases numbered 1–5 | built 1, 3, 2, 4, 5 | `plan.md`'s phase 2 row sanctions it: "otherwise run 3 before 2 and say so". Building 3 first lets phase 2's case resolve every path a checklist box names against the tree, which is an assertion only that order permits |

## What CI found after the chain ended, and why nothing here could

**This section is not a review round.** The chain ended at round 3, the
sealer took the broad gate at `59a72d91`, and the branch was sealed. What
follows is the branch being made mergeable: CI went red on the pull request,
and the defect it found is one no party in this run was able to see.

**What CI said.** Two legs, ubuntu and macOS, the same three cases:

```
FAILED tests/test_release_hygiene.py::test_it_closes_the_issue_the_keyword_named_and_nothing_else
FAILED tests/test_release_hygiene.py::test_a_number_that_names_nothing_does_not_kill_the_run
FAILED tests/test_release_hygiene.py::test_dry_run_writes_nothing
E  SystemExit: gh api issues/88 failed: gh: To use GitHub CLI in a GitHub
   Actions workflow, set the GH_TOKEN environment variable.
3 failed, 4164 passed
```

**What this work item did to them.** Finding 1's repair needed `main` to know
whether the issue it is closing carries a spent `size: now`, so it gained
`spent = exists and SPENT_ON_CLOSE in carried`. That reads through
`issue_labels` and then `_issue_api`, which reaches the tracker. The three
cases stubbed `arrived`, `pull_request_body`, `issue_state` and `run` —
which was the complete set of readers `main` used before this change — so
they walked into a live `gh api` call that had not existed on their path.

**Why the local gate is structurally unable to notice.** `gh` is
authenticated on a developer's machine, so the call succeeds and the case
passes. The broad gate runs on that same machine, so it passes there for the
same reason. CI's pytest job has no `GH_TOKEN`, correctly, and it was the
first party in the entire run — three review rounds, a sealer and several
narrow runs — that *could* see it. The seal was not wrong about the tree; it
was taken with an instrument that cannot distinguish these three cases from
passing ones.

**Measured here, both directions**, because passing while authenticated is
exactly what proves nothing:

| Tree | `gh` | Result |
|---|---|---|
| before the repair | removed from `PATH` | **3 failed**, 31 passed — CI's three, exactly |
| before the repair | present and authenticated | 34 passed **in 9.39s** |
| after the repair | removed from `PATH` | 34 passed **in 0.41s** |

The nine seconds were the network. A case whose runtime is dominated by a
live API call is one whose verdict is about the network, and nothing in the
suite's output said so.

**The repair closes the class rather than the leak.** `_offline` shuts both
doors this script has — `_issue_api`, which every read goes through, and
`subprocess.run`, which `run` and `drop_label` reach for — and the second
**raises** rather than returning a stub. So a path that escapes in future
fails loudly and identically for everyone, instead of passing for whoever
holds a token. Stubbing only `issue_labels` would have fixed the instance
and left the next one to CI.

**The enumeration, and it is the whole tree.** The suite run with `gh`
removed from `PATH` entirely: **4170 passed, 9 skipped, exit 0** (12m16s).
So after this repair no case anywhere in the tree reaches a live `gh`, and
those three were the entire class. The instrument is worth keeping: it is
one environment variable away from being a CI step, and it answers a
question the ordinary run cannot ask.

**Were the cases this work item added ever at risk?** No — and not by luck:
`test_a_declared_label_reaches_the_tracker.py`'s `wire_closer` already
patched `mod.subprocess.run` alongside the named readers, which is the same
door `_offline` now shuts for the three older cases; the publish-note cases
stub `run` and `release_exists`, the directory cases stub `fetch`, and the
checklist cases drive no script at all.

## Not verified

| Item | Who must answer |
|---|---|
| **A1 as an observation rather than a case** — that a tag push actually fires `publish-release.yml` and a GitHub Release appears. Nothing in the suite can prove a tag-triggered job runs; the release that merges this branch is the first run | the session that cuts the release carrying this work item — `docs/release-checklist.md` §6's first new box is exactly this check |
| **That the reconcile step actually creates `size: now` on the tracker.** Verified against a fake tracker only; no agent in this chain may write to the tracker (`agent-contract` §6), so the live write happens on the first push to `main` after this merges | the same releasing session — `gh label list` after the merge |
| **The full suite, the repository-wide lint and the typecheck.** Not run: `agent-contract` §2 makes the broad gate one act with one owner, and every run here was the narrow module-level form | the `sealer`, in its single run after the review rounds settle |
| **`tests/test_the_gate_names_every_step_ci_runs.py#test_a_repository_with_no_hygiene_workflow_is_sealed_exactly_as_before` fails in any checkout whose path contains the word `release`.** It strips the fixture repository's path from stderr but not the interpreter's, and this worktree is `…/wt-release-tail/.venv/bin/python`. Measured, not inferred: the same commit runs green in a throwaway worktree at a neutral path, and that worktree was removed. **Not this branch's defect and outside its scope** | the `sealer` first — it decides whether the broad gate sees this from wherever it is standing — then whoever owns that module. It is a candidate for `seal/follow-up.md` if the sealer confirms it |
| **Whether an update reaches a plugin already listed in the directory automatically, or must be resubmitted** | a person — the repository owner, per `questions.md` Q1. It blocks nothing: the box reports the pinned commit against the released one and says to resubmit when it is stale, which is unnecessary under one answer and never wrong under either |

## Not done

**No backlog sweep applying `size: now`.** Within reach and deliberately not
taken — `docs/issues-and-milestones.md`'s own argument is that the judgment is
cheap at filing and expensive in a batch, and a sweep is the batch performed
once by the party the label exists to spare. The document now says so instead,
and `test_the_no_sweep_rule_carries_its_reason` keeps the verdict from
outliving its reason.

**The label was not created by hand.** `agent-contract` §6 withholds posting
from every agent, and the whole point of #450 is that an act assigned to a
person leaves no trace anything can read. The workflow performs it.

**No gate keyed to the plugin directory's state, and no check refusing a
release while the previous tag has no note.** Both are in `spec.md` §*Out*
with the tickets' own measurements behind them; the second's condition is
removed by phase 1 rather than reported.

**`tests/test_the_gate_names_every_step_ci_runs.py` was not repaired.** It is
another work item's module, the failure predates this branch, and the fix is a
judgment about what that assertion should strip. Named above with an answerer
rather than fixed quietly inside an unrelated branch.

**The `console.to_utf8()` call in `tracker_labels.py` is pinned by nothing,
and a later session deleting it gets no warning from this suite.** Review
round 1's finding 3 added it; no case was added with it, and that decision
stands — `tests/test_console_is_not_utf8.py` spawns each gate by hand under
four hostile encodings rather than reading a corpus, so covering this one
script is the coordinate fix `agent-contract` §12 warns against, and widening
it to `.github/scripts/` reds the seven standing non-callers at once. The
class is a row of `seal/follow-up.md` with the repository owner named. What
was missing until round 2 was this sentence: the fix was probed under a cp949
console and not pinned, so the evidence is a measurement in a record rather
than a check that runs. **The same standard is applied three paragraphs down
to the `DOMAIN_RE` reading, and applying it to one unpinned thing and not the
other is what round 2 caught.**

**A real domain and two real organisation names sit in
`plugin_directory_check.py:81-85`, and no check in this repository can see
them.** `clau.de` and `anthropics/claude-plugins-official` /
`-community` are in the tree deliberately: `spec.md`'s grounding row says the
directories' URLs belong in the script that reads them rather than in prose,
and I still think that is right — a reader checking what was actually read
needs the real values, and fixtures and examples elsewhere use neutral ones.

**What is worth saying is that the green build is not what cleared them.**
`tests/test_no_real_identifiers.py` was run and passed, and it would have
passed with anything: its `DOMAIN_RE` matches `com|io|net|org|ai|dev` and
`.de` is in none of them, and it checks no organisation names at all.
Confirmed by driving the pattern over both lines directly — zero matches, so
zero refusals. So the placement rests on the reasoning in `spec.md` and on a
reader agreeing with it, and on nothing mechanical. A later session that
moves either value somewhere the rule does mean to forbid — a fixture, an
example, a document — gets no warning from this suite either. Left as it is
rather than changed, and named here so the next reader knows which of the two
is holding it up.

**`spec.md` and `plan.md` were edited, which a build normally must not do.**
Two sentences of the frame were refused by `tests/test_no_real_identifiers.py`
— they named a host while instructing the reader not to. The base does not
carry the domain and `git log -S` names the frame commit `99168a43` as where
both entered, so it is this branch's red and this branch's to clear. Both
sides are quoted in the divergence table above, and nothing either sentence
asserted was changed.

## Fed back into the spec

Three clauses, all *inferred during implementation* and all overturnable by
opening what they cite:

1. **A directory entry's `source` has four shapes, two of which pin no
   commit.** `spec.md` §*Data & interfaces* states one. Measured over both
   live files 2026-09-22; the counts are in `phases/phase-3.md`.
2. **A pinned commit has three ancestry answers, not two** — reachable, not
   reachable, and not present in this clone. The third is what keeps an
   unfetched checkout from reading as a stale pin.
3. **The prescribed release title line exists in a symptomless form**, and it
   takes the fallback. `spec.md` A4's two branches are written as though the
   line is either there or not.

A fourth is about the frame rather than the tree, and belongs with them
because the next work item reading `spec.md` will meet it: **the handoff's
ledger-row count was wrong in the direction that costs nothing to check and
everything to assume.** Three rows, not five. The two "nearby" rows are on
headings this work does not touch.
