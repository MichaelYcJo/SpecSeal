# 1791076834-the-changelog-is-one-file-per-release — review round 1

| Field | Value |
|---|---|
| Target SHA | 516ed1d110f24f2b84b3e445244e742ccfea13cd |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #770 |
| Broad gate | not yet |
| Fixes checked by | no fixes to check |
| Fix range | `516ed1d110f24f2b84b3e445244e742ccfea13cd..9bc9f5faee60c1629277087a079e613c3d2ee256`, 1 commit |
| Contract changes | none |
| New units | none |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 1 of work item `1791076834-the-changelog-is-one-file-per-release` (#728, PR #770), target `516ed1d1`, against `release/v0.18.1` at `edee5ca2`. Spec compliance first: the byte-for-byte migration of 44 sections (the concatenation reproduces the old file), the index's shape and what the installed 0.18.0 update skill reads from it, `gather_changelog.py` writing and checking the release's own file, `publish_release_note.py` reading it, the survivor sweep reading both shapes, and every reader and writer of the changelog enumerated by construction (grep the name and every path that reads a section). The risk to weigh is the release this ships in: 0.18.1 is gathered and published by the new tooling, and a defect surfaces at the release tag, after every gate. Run the gather and the publisher's `section_body` in dry-run form against a scratch clone. Quality second. The orchestrator verified the changed modules plus hygiene (995 passed) and ruff on the changed Python files at the target.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| ⬜ 1 | eight added lines spliced into wrapped paragraphs without re-wrapping, 89 to 115 columns | `docs/branch-and-release.md:59` | answered | no change. The eight lines, 89 to 115 columns, lie outside `test_docs_line_wrap.py`'s scope and break no check. Rewrapping them now would commission a change that no round reads, after a round that opened nothing needing a fix; read; the other seven coordinates are in the prose above; no check covers these files |
| ⬜ 2 | release checklist §3 still describes the unstaged tree that §2 now stages | `docs/release-checklist.md:184` | answered | no change. The paragraph at `docs/release-checklist.md:184` explains a skipped-count line from the state before staging. §2's `git add -A` now prevents that state, so the paragraph describes a case that no longer arises. It does not direct any step, and a reader who meets the old state still gets a correct explanation. Its rewrite belongs with the next edit to §3; read against `:84` and `:89` of the same file |
| ⬜ 3 | the comment above `CHANGELOG` says a changelog under another name is read as any document, which `RELEASE_FILE` now contradicts | `skills/code-review/scripts/survivor_check.py:579` | answered | no change. `survivor_check.py:579`'s comment predates `RELEASE_FILE`, which is defined directly below it. The module docstring states the current reading, and the behaviour is pinned; read; the docstring at `:154-165` was updated and this comment was not |
| 🟢 | S1 holds: the release files joined reproduce the old changelog byte for byte | `changelog/` | confirmed | executed, 577,907 bytes both, against `edee5ca2` |
| 🟢 | the new gather writes 0.18.1 and its index line, and `--check` passes after it | `.github/scripts/gather_changelog.py:476` | confirmed | executed in the scratch clone; hygiene and gather modules green on the post-gather tree |
| 🟢 | the publisher's `section_body` reads the gathered release file | `.github/scripts/publish_release_note.py:151` | confirmed | executed on the gathered 0.18.1 file and on four migrated releases |
| 🟢 | the survivor sweep reads both shapes; build range excused, gather range clean | `skills/code-review/scripts/survivor_check.py:591` | confirmed | executed over both ranges |
| 🟢 | 0.18.0's update step 2b still names the landed version from the index | `CHANGELOG.md:11` | confirmed | read; the first `## ` line is the newest release's heading, before and after the probe gather |

## Paste-ready fixes

no paste-ready fix in the report

## Executed probes

| What was run | Result |
|---|---|
| Python byte compare: `changelog/*.md` newest first, joined under `# Changelog`, against `git show edee5ca2:CHANGELOG.md` | equal, 577,907 bytes both, 44 files |
| `git diff --quiet e141980a edee5ca2 -- CHANGELOG.md` | exit 0, identical |
| `gather_changelog.py --check` at the target | exit 1, names the four branch fragments (expected off a release) |
| `gather_changelog.py --version 0.18.1 --dry-run --date 2026-10-05` | exit 0, `into changelog/0.18.1.md:`, 4 markers, nothing written |
| `gather_changelog.py --version 0.18.1 --date 2026-10-05`, then `--check` | exit 0 both; index headed with `## 0.18.1 — 2026-10-05`; `57 changelog fragments, all gathered; 174 work items marked in changelog/` |
| `section_body` on `changelog/0.18.1.md`, and old-vs-new for 0.18.0, 0.17.0, 0.9.1, 0.0.1 | 9,162 characters; all four equal |
| `bin/test` on the release hygiene, gather and chain-hooks-hardening modules, post-gather tree, `plugin.json` at 0.18.1, all staged | 161 passed |
| `bin/test` on the publisher, survivor, GFM-reader and handoff modules at the target | 385 passed |
| `bin/test tests/test_docs_line_wrap.py` at the target | 38 passed |
| `survivor-check --range edee5ca2..516ed1d1` | exit 1, 4 places, all in `seal/releases/` |
| same with `--exempt` the work item's `survivors.md` | exit 0, all 4 excused |
| `survivor-check` over the target-to-gather probe commit | exit 0, no removed wording standing |
| 0.18.0's sweep (the `edee5ca2` blob, run once as a probe file and deleted) over `edee5ca2..516ed1d1` | exit 1, 3 places, none under `changelog/` |
| Python scan of `changelog/*.md` and every fragment for relative markdown links | 0 links of any kind |
| the full suite, repository-wide lint and typecheck | not yet; the sealer's, after the rounds settle |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
