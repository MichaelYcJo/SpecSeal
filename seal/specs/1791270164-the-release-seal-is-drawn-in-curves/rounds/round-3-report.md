# Round 3 report — 1791270164-the-release-seal-is-drawn-in-curves

| Field | Value |
|---|---|
| Target SHA | f94e262e0ff6a47285dc328a75727000f195d80d |
| Round kind | verifying round over round 2's fix range `1789de0b..b74041bb` (`cc900a0f`, `40a3a3f3`, `b74041bb`) |
| Pull request | #859 (draft) into `release/v0.20.0` at `559977a3` |
| Ran by | specseal:warden on claude-opus-5-5 |

HEAD did not move during the review: `f94e262e` at spawn, at hand-over,
and on the pull request's head. `559977a3` is an ancestor of it, so the
tree CI checks out as the merge is this tree. Every probe ran in a
`git clone --no-local` at the target under the session's scratchpad, and
nothing was written to the worktree but this file.

## Summary

Round 2's two fixes and its correction hold, and every workflow of the
pull request is green at this push.

```
round 2's findings                    what closed them, and how it was shown
  1  domain check red on 3 legs   ->  cc900a0f: www.w3.org allowed
                                       red without it, green with it; CI green
  2  apt-get update; under -e     ->  40a3a3f3: apt-get update || true;
                                       bash -e probe; case red against `;`
  3  spec.md foot refused         ->  b74041bb: foot ends at the Framed line
                                       chain_check exit 0 as a draft; release job green
  4  merge's units in New units   ->  deferred to #860 (0.21.0), open
```

1. **The domain check is green, and the allowance is the narrowest one
   that works** (round 2's finding 1). The reason written beside it holds,
   with one sentence wider than what was measured (⬜ 1 below).
2. **A failed refresh no longer stops the install** (round 2's finding 2).
   The four places round 2 named now say the same thing as the step.
3. **`chain_check` accepts the corrected foot**, locally as CI calls it and
   in CI itself (round 2's finding 3).
4. **The fourth finding stays where round 2 sent it**, issue #860.

One thing could not be settled: on two legs one case that passed at round
2's push is skipped at this one (❓ below).

## Round 2's verdicts, one by one

### Finding 1, the SVG namespace host: closed

`tests/test_no_real_identifiers.py:28` adds `www.w3.org` to
`ALLOWED_DOMAINS`. The match in `domains_in` is `d == a or
d.endswith("." + a)`, so the entry admits that one host and its
subdomains. It does not admit the parent domain without `www`, or any
other host. The tree carries
the host in three places, all of them the SVG namespace URI or a record
quoting it: `.github/scripts/release-seal.svg:1`,
`tests/test_the_release_seal_is_drawn.py:38` and `round-2.md:38`.

- **Executed.** With the entry removed in the clone, the module fails on
  exactly those three lines. Restored, it passes.
- **Executed.** In CI, the ubuntu, macOS and Windows group 2 legs that
  round 2 saw red are green at this push.
- **The reason.** The comment says the namespace can be neither removed nor
  replaced because a renderer recognises an SVG by it. The conclusion
  holds: the repository's own SVG case parses the file by that namespace
  (`NS` at `tests/test_the_release_seal_is_drawn.py:38`), and a standalone
  `.svg` without it is not SVG to an XML parser. One clause is wider than
  what was measured, and ⬜ 1 says which.

### Finding 2, `apt-get update;` under `bash -e`: closed

`.github/workflows/publish-release.yml:116` now runs
`sudo apt-get update || true; sudo apt-get install …`. The step has no
`shell:` key and the job sets no `defaults`, so it runs under `bash -e`.
In bash a command on the left of `||` does not trigger `-e`, so the
install runs after a failed refresh.

- **Executed.** `bash -e -c 'false || true; echo reached'` printed and
  exited 0. `bash -e -c 'false; echo reached'` printed nothing and exited 1.
- **Executed.** With the step set back to `;` in the clone,
  `test_the_seal_job_installs_rsvg_convert_before_the_suite_and_the_draw`
  fails on the new assertion. Restored, it passes. The case's `steps`
  helper puts the comment lines above a step into the step before it, so
  the `run` line the case reads is the step's own and not the comment
  that also names `librsvg2-bin`.
- **Read.** The four places round 2 named agree with the step and with
  each other:
  - the comment above the step (lines 102–113);
  - the case's docstring;
  - ledger row `Corrected · W3`, whose first cell names
    `apt-get update || true;` and the step's `bash -e`, and whose new
    executed note says how the case was seen red;
  - the overview's divergence row (`overview.md:54`), which records both
    earlier shapes.
- **Read, and not a finding.** `phases/phase-8.md:21` still says the step
  runs `sudo apt-get update && `. It is phase 8's record, bound to commit
  `2753ce1d` in its own header, and it was true at that commit. The
  overview row is where the later shapes are recorded, and it records them.

The changelog fragment says only that the `seal` job installs
`librsvg2-bin` and that a failed install leaves the counts table. Both
are still true, so the notice `chain_check` prints about the fragment
owes nothing.

### Finding 3, the `spec.md` foot: closed

`spec.md` now ends with `Framed 2026-10-06 by framer, before the build.`.
The redraw after the owner's look at phase 2's stamp is a sentence two
lines above it. `frame_foot` reads the foot from the bottom, so the
`Framed` line is the mark. A sentence above the mark is not part of the
foot, and nothing reads it as a reframe.

- **Executed.** `chain_check.py --baseline origin/release/v0.20.0` in the
  clone, with the base and every `refs/pull/*/head` fetched as the
  `release` job fetches them and a `GITHUB_EVENT_PATH` saying draft,
  exits 0. It prints the draft notice about `Pass` beside `nobody` on
  `round-2.md`, which this round's record answers, and the changelog
  notice above.
- **Executed.** The same run judged as a ready pull request exits 1 on
  two rows of `round-2.md`: `Fixes checked by` is `nobody` and
  `Broad gate` is `not yet`. Both are owed by the run's next steps, this
  round's record and the sealer, and neither is a refusal of the
  correction.
- **Executed, in CI.** The `release` job passed at this push. Its log
  shows `chain-check: judged as a draft pull request`.
- **Read.** `plan.md:41-44` and `spec.md:73-77` now describe the redraw
  as a sentence above the mark, and no file of the work item still names
  a `Reframed` line at the foot.

### Finding 4, the merge's units in `round-1.md`: still deferred

Issue #860 is open on the 0.21.0 milestone. The fix range of round 2
holds no merge, and `round-2.md` lists `New units: none`, which is right
for this range: the diff adds a tuple entry, rewrites comments and a
docstring, and changes one assertion. It defines no new unit.

### Round 2's other rows

Its 🟢 rows confirm round 1's closures in `seal_stamp.py`,
`hooks/sealer-stamp.py` and the stamp's test modules. Round 2's fix range
touches none of those files, so they are carried and not re-derived
here.

## ⬜ 1 — one clause of the allowance's reason is wider than the renderer this repository uses

`tests/test_no_real_identifiers.py:25` says *a renderer recognises an SVG
by that namespace*. `rsvg-convert` 2.58.4, the renderer the `seal` job
installs, drew `release-seal.svg` with its `xmlns` attribute removed into
a PNG byte for byte identical to the one it drew from the file as
committed. So the clause is not what keeps the namespace in this file.

What does keep it is true and checkable. The SVG case reads the file's
elements under the namespace, and an XML parser does not treat a root
`svg` element outside the namespace as SVG. The entry stays right; only
its reason reads stronger than what was measured. A comment a reader
acts on is the cost, not the release, so this is ⬜ and commissions
nothing. A wording that says what was measured:

```python
    # The W3C's SVG namespace host. Every SVG carries the namespace URI in
    # its `xmlns`: an XML parser takes an element outside it for something
    # other than SVG, and `test_the_release_seal_is_drawn.py` reads the
    # release SVG's elements by it. So it can be neither removed nor
    # replaced with example.com: it is an identifier, not an address
    # anything fetches (#832).
    "www.w3.org",
```

## ❓ — one case is skipped on two legs where it ran at round 2's push

The totals are equal across the two pushes, so one case moved from passed
to skipped. Round 2's failing case moved to passed at the same time.

| Leg | `bf1a9447` | `f94e262e` |
|---|---|---|
| ubuntu | 1 failed, 12,738 passed, 80 skipped | 12,738 passed, 81 skipped |
| Windows group 2 | 1 failed, 6,706 passed, 35 skipped | 6,706 passed, 36 skipped |
| macOS | 1 failed, 12,730 passed, 88 skipped | 12,731 passed, 88 skipped |

The CI command is `pytest tests/ -q`, with no `-rs`, so its log names no
skipped case. I ran the nine modules that read round records or this
work item's `spec.md`, with `-rs`, at the target. The only skip was
`tests/test_the_reopening_is_one.py:578`, whose base is not fetched in the
clone, and that skip does not depend on this diff. None of the cases
round 2's fixes changed can skip. The pixel case skips only where
`rsvg-convert` is absent, and it was absent on both pushes. Which case
moved, and whether the change made it move, is not settled.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | round 2's blocking finding is closed — `test_only_neutral_domains` is green on every leg, with `www.w3.org` allowed and nothing wider | `tests/test_no_real_identifiers.py:28` | confirmed | executed: red on exactly the three lines that carry the namespace with the entry removed, green restored; the ubuntu, macOS and Windows group 2 legs pass at f94e262e. read: the match is exact host or subdomain |
| 🟢 | round 2's finding 2 is closed — a failed `apt-get update` no longer stops the install under the step's `bash -e`, and the comment, the case, ledger W3 and the overview row agree | `.github/workflows/publish-release.yml:116` | confirmed | executed: `bash -e` runs past `false \|\| true;` and stops at `false;`; the install case red with the step set back to `;`, green restored. read: no `shell:` and no `defaults` on the step; `phases/phase-8.md:21` is phase 8's dated record |
| 🟢 | round 2's finding 3 is closed — `spec.md` ends with the `Framed` line, and `chain_check` accepts it | `seal/specs/1791270164-the-release-seal-is-drawn-in-curves/spec.md:423` | confirmed | executed: `chain_check.py --baseline origin/release/v0.20.0` exit 0 judged as a draft, with the release job's fetches; the PR's `release` job passed. Judged as ready it exits 1 on `round-2.md`'s `nobody` and `not yet` alone |
| carried | round 2's finding 4 — `round-1.md`'s `New units` counts the merge's units | `seal/specs/1791270164-the-release-seal-is-drawn-in-curves/rounds/round-1.md:13` | deferred #860 | already deferred in round 2; #860 is open on the 0.21.0 milestone; round 2's range holds no merge and its `New units: none` is right |
| ⬜ 1 | the allowance's comment says a renderer recognises an SVG by its namespace, and `rsvg-convert` 2.58.4 draws the release SVG identically without it | `tests/test_no_real_identifiers.py:25` | open | executed: the PNG from the SVG with `xmlns` removed is byte for byte the PNG from the SVG as committed. The entry is right; the SVG case reads elements by the namespace |
| ❓ | on the ubuntu and Windows group 2 legs one case that passed at bf1a9447 is skipped at f94e262e; the CI log names no skipped case | `.github/workflows/test.yml` | ❓ out of verified scope | the nine modules that read round records skip nothing new; the orchestrator answers it, by reading skip reasons in the sealer's broad run |

## Executed probes

| What was run | Result |
|---|---|
| `gh pr checks 859 --watch` to the end at `f94e262e`, `gh pr view 859` | exit 0. Pass: `lint`, `ledger`, `release`, `arm-check-grammar` 3.13 and 3.14, pytest ubuntu, macOS and Windows groups 1–4. None failed, none pending. `MERGEABLE`, `CLEAN` |
| the `release` job's log | `chain-check: judged as a draft pull request` |
| the ubuntu, macOS and Windows group 2 job logs, here and at round 2's run | ubuntu 12,738 passed, 81 skipped; macOS 12,731 passed, 88 skipped; group 2 6,706 passed, 36 skipped. At `bf1a9447`: 1 failed on each, with 80, 88 and 35 skipped |
| `bin/test tests/test_no_real_identifiers.py tests/test_a_release_publishes_its_note.py -q` | exit 0, 31 passed |
| `www.w3.org` taken out of `ALLOWED_DOMAINS` and the step set back to `;`, both in the clone; the domain module and the install case | exit 1, 2 failed: the three namespace lines, and `'sudo apt-get update \|\| true;' in '… update; sudo apt-get install …'` |
| the same two, restored | exit 0, 6 passed |
| `bash -e -c 'false \|\| true; echo reached'` and `bash -e -c 'false; echo reached'` | exit 0 and printed; exit 1 and nothing printed |
| `rsvg-convert -w 32 -h 32` over `release-seal.svg` and over a copy with `xmlns` removed, then `cmp` | both exit 0; `cmp` exit 0, the two PNGs identical |
| `chain_check.py --baseline origin/release/v0.20.0` in the clone, base and `refs/pull/*/head` fetched, `GITHUB_EVENT_PATH` saying draft, then ready | draft: exit 0, with the `Pass` beside `nobody` notice and the changelog notice. Ready: exit 1, on `round-2.md`'s `Fixes checked by` and `Broad gate` |
| `bin/evidence-check --strict .` at the target | exit 0; this work item's ledger 287 ok · 0 drifted · 0 broken |
| the nine modules that read round records or the spec foot, `-q -rs` | exit 0, 639 passed, 1 skipped (`tests/test_the_reopening_is_one.py:578`, its base not fetched) |
| the full suite, lint and typecheck | not yet — the sealer's, once, after the rounds settle |

Needs a fix: no

Loses a record or crashes: no

Nothing this round found needs a fix, so the broad gate comes due: the
sealer's spawn at `f94e262e` against `release/v0.20.0`.

## Proof block

Files opened this round:

- `seal/specs/1791270164-the-release-seal-is-drawn-in-curves/rounds/round-2.md`
- `seal/specs/1791270164-the-release-seal-is-drawn-in-curves/rounds/round-2-report.md`
- `seal/specs/1791270164-the-release-seal-is-drawn-in-curves/spec.md` (its foot)
- `seal/specs/1791270164-the-release-seal-is-drawn-in-curves/changelog.md`
- `seal/specs/1791270164-the-release-seal-is-drawn-in-curves/phases/phase-8.md`
- `.github/workflows/publish-release.yml`
- `.github/workflows/hygiene.yml` (the `release` job's `chain_check` steps)
- `.github/workflows/test.yml` (searched)
- `tests/test_no_real_identifiers.py`
- `tests/test_a_release_publishes_its_note.py`
- `tests/test_the_release_seal_is_drawn.py` (the pixel case's `skipif`)
- `tests/conftest.py`, `tests/test_a_corrected_sentence_survives_elsewhere.py`,
  `tests/test_the_reopening_is_one.py`,
  `tests/test_a_narrowed_ledger_read_says_what_it_skipped.py`,
  `tests/test_the_pull_request_language_is_the_repositorys.py` (skip sites)
- `skills/code-review/scripts/chain_check.py` (searched for the foot and the draft reading)
- `CONTRIBUTING.md` §*Running the checks*
- the full fix diff `1789de0b..b74041bb`

`overview.md`, `plan.md` and the ledger row were read through that diff,
not opened whole.
