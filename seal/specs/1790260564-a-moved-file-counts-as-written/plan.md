# Implementation Plan: the survivor sweep's moved text, gathered reading, and local ownership (#563, #564, #554)

Approved 2026-09-24 by the orchestrating session under the owner's `automation` answer, when `smith` was spawned. Q1 builds on its default and is filed as #586.

## Summary

There are three phases, one per issue. The order is set by the code the phases
share. #564 goes first because it touches the read boundary and the fragment
reader inside `corrected`. #563 changes `corrected`'s counting on top of that.
#554 is independent and touches only `whole_range`. Each phase plants its cases
red first, fixes the code, corrects the docstring and docs sentences its change
makes false, re-reads the ledger rows it drifts, and closes on a commit.
`spec.md` holds the decisions and their grounds. This file holds the order,
the alternatives each decision was chosen over, and what each choice costs.

## Technical context

All coordinates are units in `skills/code-review/scripts/survivor_check.py`,
read at `c52e8350`.

- `read_blobs` decodes each blob and does nothing else to it. Every committed
  text reaches every reader through this function (`corpus`, `corrected`,
  `gathered_fragments`).
- `blank_released` / `only_released` are two loops over `split("\n")` that
  flip `released` at every `SECTION_HEADING`. `newly_released` reads through
  `only_released`, and `sentences` reads `CHANGELOG.md` through
  `blank_released`.
- `MARKER` is `^<!-- specs/(\S+) -->$` with `re.M`. `gathered_fragments`
  runs `findall` with it over the tip's `CHANGELOG.md`. `newly_released` uses
  `sub` with it.
- `a_gathered_fragment` accepts `<anything>/specs/<id>/changelog.md`. The
  reader in `corrected` (`fragments = [f"seal/specs/{item}/changelog.md" …]`)
  spells a single path.
- `corrected` has one per-path loop. It computes `gone` by counting (`seen`
  against `counted`), runs the `CHANGELOG.md` arm (`newly_released`, the
  `lost` guard, `held`/`split`), and adds `written.update` for every fresh
  sentence of `now + moved`. There is no step across paths, and that missing
  step is #563.
- `whole_range` finds the owner with `OWNER_DIR` and tests ownership by
  checking whether `changed` (a lazy `git diff --name-only --no-renames`) has
  a path under the owner. The owner dir is never in `changed` in local mode.
- `hooks/routing.py#parse` returns a dict with `branch`, or `None`.
  `chain_check.py` loads it by path through `ROUTING` / `load`.
  `hooks/optin.py#git_common_dir` and `#home_paths` are the existing readers
  for where local mode lives. `skills/verify/scripts/broad_gate.py#exemptions`
  hands every `<home>/specs/*/survivors.md` to the sweep, and `home` is the
  local root in local mode. That is how #554 is reached at the sealer.

**Failure scenario of the chosen approach ("what breaks in six months").**

- **#563.** A larger `wanted` can join two runs of shared wording into one,
  and a run scores by its rarest n-gram. So a survivor that scored over the
  floor on two runs, with a moved-and-written n-gram between them, can fall
  under it. This is exactly the score the same text gets when it has not moved,
  so it is not a regression of the policy. It is still a place where the
  verdict drops, and nothing measures it apart from the pinned real ranges
  (`questions.md` Q3).
- **#564 ⬜6.** A changelog that keeps a live section under a name other
  than `Unreleased` *below* a version heading will have that section read as
  released. It leaves the pool and the range, and a survivor inside it goes
  unreported. No convention this plugin names puts live prose there.
- **#554.** A local-mode declaration is excused over any range whose tip is
  on its work item's branch. If a person reuses a branch name for a second
  work item, and the first item's local `survivors.md` is still on disk, both
  items claim ranges on that branch. The first anchor still applies: the
  range must resolve to the row's own range. So the exposure is a relation
  spelling, re-resolved on a reused branch name.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| #563: keep counting moved text as written (today) | #563's probe. A split or move carrying a quote of a claim corrected in the same range hides every survivor of that claim. The #526 split is that shape | rejected. It contradicts the docs rule sentence *only wording the range itself wrote is subtracted* |
| #563: whole-file moves only, from git rename detection (`-M`) or identical blob oids | A split, where both files remain, is not a rename and is not an identical blob, so the shape #563 names as reachable here stays blind. `-M` also brings back what #551 removed | rejected |
| #563: pair the sentences removed at one path with identical sentences added at another, by key and count (**chosen**) | See the failure scenario above: a run merge can lower one score | chosen. It is the in-file counting rule that already exists, applied across paths, and it covers a move, a rename and a split |
| #563: pair by key, and also still write the moved grams | Same as today for #563's probe. Nothing changes | rejected |
| #564 ⬜5: narrow `a_gathered_fragment` to `seal/specs/` | It changes pool membership for every `<x>/specs/<id>/changelog.md`, which nobody measured and the issue does not ask for | rejected, and listed as Out in `spec.md` |
| #564 ⬜5: the reader asks the predicate over `tracked(root, a)` (**chosen**) | One more `ls-tree` per run. A larger `shipped` set only moves sentences from written to held | chosen |
| #564 ⬜6: a gathered block runs from its marker to the next marker or version heading | Depends on the marker, so a CRLF or misspelled marker brings the gap back. And `## Unreleased` directly after a fragment, which is where this gatherer puts it, reads as released | rejected |
| #564 ⬜6: only a version heading or an `Unreleased` heading changes the region once a version has opened it (**chosen**) | A live section under another name below a version heading reads as released | chosen |
| #564 ⬜6: refuse a `## ` line in a fragment at the gatherer | This is the release automation's fix, not the sweep's. It does not help a repository that copied the marker convention and not this gatherer | not this branch → `questions.md` Q1 |
| #564 ⬜7: `\r?$` in `MARKER` | Fixes one member. The next `$`-anchored reader repeats the defect | rejected (§12) |
| #564 ⬜7: normalise `\r\n` in `read_blobs` (**chosen**) | A lone `\r` still disagrees between `split` and `splitlines` | chosen |
| #554: ownership when the range's commits carry the id's `routing.md` | That file is never committed in local mode, so the test can never pass | rejected |
| #554: ownership when the checked-out branch equals the `Branch` row | It asks about the checkout, not the range, and a detached HEAD at the branch tip reads as foreign | rejected |
| #554: ownership when `b` is `refs/heads/<Branch>` or its ancestor (**chosen**) | See the failure scenario (a reused branch name) | chosen |
| #554: every local-mode declaration is `mine` | Local `survivors.md` files are shared by every worktree of the clone, so a relation-spelled row would excuse other branches' ranges. That is the defect the second anchor exists to stop | rejected |
| #554: apply the branch test in shared mode too | A CI pull-request checkout is a detached merge commit with no `refs/heads/<branch>`, so every shared-mode declaration would read as foreign in CI | rejected |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 · #564: the gathered reading reads one path, past a heading, over any line ending | `read_blobs` normalises `\r\n` to `\n`. One region helper sits behind `blank_released` and `only_released`, and after a version heading only a version heading or `^##\s+\[?unreleased\b` (case-insensitive) changes the region. The fragment reader in `corrected` reads the paths `a_gathered_fragment` accepts in `tracked(root, a)`. The module docstring's released-section paragraph and `blank_released`'s docstring lose *up to the next `## ` heading*. Ledger rows C1, H1, C2 and the others `evidence-check` names are re-read and corrected where false | G7, G8 and G10 each seen red at `c52e8350` with exit 0. G9 seen red against the region helper with the `Unreleased` exception deleted. G10 asserts that the committed blob holds `\r\n` under `core.autocrlf=false`. Narrow run: the test file's gathered/released/changelog/fragment cases (`-k` over `gather or releas or changelog or fragment`), all green. `evidence-check` names no BROKEN row | `cb7b8d10` |
| 2 · #563: a moved sentence is held and never written | `corrected` gets a step across paths after the per-path loop. It pairs sentences removed at one path with identical fresh sentences added at another, by key and count, and the paired sentences are neither `gone` nor `written`. The `CHANGELOG.md` arm keeps its per-file `lost`/`held`/`split` logic untouched. `corrected`'s rename paragraph is rewritten. S18 is renamed and rewritten to pin silence at `against 0 sentence(s)`. `docs/review-chain-spec.md` sentence 1 (per `spec.md`) is corrected in place. Ledger row R1 is corrected, U2 is re-read, and the rest follow `evidence-check` | M1 and M2 each seen red at `c52e8350` with exit 0. The old S18 assertion seen red under the new code, which is the reason it changes. S17 green, unedited. The whole test file green (it is this phase's module), including `RELEASE_RANGES`, with Q3's measurement recorded. Q2's measurement recorded | `ed5748ff` |
| 3 · #554: a local-mode declaration owns the range on its own branch | `whole_range` decides local mode lazily, only for a declaration that would have matched: real path under the real path of `<git-common-dir>/seal/specs/`, compared after `os.path.normcase`. Local mode reads the sibling `routing.md` through `hooks/routing.py#parse`, loaded by path, and asks `git merge-base --is-ancestor <b> refs/heads/<Branch>`. Shared mode is unchanged. The `whole_range` docstring and the `OWNER_DIR` comment are updated. `docs/review-chain-spec.md` sentence 2 is corrected in place. Rows E4, G5 and U1 are re-read | O1 seen red at `c52e8350`, printing `not yours`. O2 seen red against an ownership test reduced to `True`. The existing ownership cases green, unedited. Narrow run: the test file's `declaration or owner or exempt or unresolved or range_row` cases | `21248da1` |

What a phase finds while building goes in `phases/phase-N.md`, not here. Each
phase writes its rows into `seal/ledger/1790260564-a-moved-file-counts-as-written.md`
and its line into `changelog.md` at its own boundary, in the commit that closes
it.

**Per-phase gate items (`CONTRIBUTING.md` §*What a change to a gate must carry*).**
The phase record states each one, and the pull request body carries them.

| | Test seen red | Failure direction | Prompt budget | Platform |
|---|---|---|---|---|
| 1 | G7, G8, G10 at the base, G9 by mutation | The sweep holds more and writes less, so it reports more. ⬜6 also takes a fragment's post-heading text out of the pool, so it reports less *there*. That text is released, and a survivor inside it is not one anybody may correct. A wrong deny costs a red run and a `survivors.md` row. A wrong allow costs a round | zero. The sweep prints and exits | CRLF: the case asserts the committed bytes, because autocrlf differs between runners (§13). Three-OS matrix in `test.yml` |
| 2 | M1, M2 at the base | Reports more. `wanted` only grows, apart from the run-merge effect in the failure scenario. A wrong deny, a moved quote reported, is the report the policy asks for | zero | Pure Python over git output. No platform surface beyond what the module already has |
| 3 | O1 at the base, O2 by mutation | Allows more: an exemption now applies where it was refused. It is bounded by the branch-ancestor test (O2), and a declaration it cannot place prints `not yours` | zero | Real path and `normcase` for macOS's `/private` temp symlink, Windows drive-letter case and separators. `--git-common-dir` may be relative to `root`. O1 must run in a linked worktree or say why not |

## Operational impact

There are no migrations, environment variables or dependencies. A repository
whose ranges move text will see `against N sentence(s)` counts drop, and it may
see new survivors reported. That is #563's intended change, and the changelog
fragment says so. Local-mode users get their own range rows back. Nothing
changes at a CI checkout.
