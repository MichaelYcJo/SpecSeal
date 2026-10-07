# 1791270164-the-release-seal-is-drawn-in-curves — review round 3

| Field | Value |
|---|---|
| Target SHA | f94e262e0ff6a47285dc328a75727000f195d80d |
| Written late | no |
| Ran by | warden on Opus 5.5 |
| PR | #859 |
| Broad gate | 18f023f7 against 559977a3 |
| Fixes checked by | no fixes to check |
| Fix range | `f94e262e0ff6a47285dc328a75727000f195d80d..f94e262e0ff6a47285dc328a75727000f195d80d`, 0 commits |
| Contract changes | none |
| New units | none |
| Fix of a fix | no |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 3 of #832 is the verifying round for round 2's fixes at `1789de0b..b74041bb`. It was reviewed at f94e262e.

The reviewer was asked to open each fix:
- the `www.w3.org` allowance;
- `sudo apt-get update || true;` under `bash -e`, and the four places that describe it;
- the corrected `spec.md` foot, and `chain_check` as the PR's CI judges it.

It was also asked to read every workflow of `gh pr checks 859` once each had finished. It did not run the full suite.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | round 2's blocking finding is closed — `test_only_neutral_domains` is green on every leg, with `www.w3.org` allowed and nothing wider | `tests/test_no_real_identifiers.py:28` | confirmed | executed: red on exactly the three lines that carry the namespace with the entry removed, green restored; the ubuntu, macOS and Windows group 2 legs pass at f94e262e. read: the match is exact host or subdomain |
| 🟢 | round 2's finding 2 is closed — a failed `apt-get update` no longer stops the install under the step's `bash -e`, and the comment, the case, ledger W3 and the overview row agree | `.github/workflows/publish-release.yml:116` | confirmed | executed: `bash -e` runs past `false \|\| true;` and stops at `false;`; the install case red with the step set back to `;`, green restored. read: no `shell:` and no `defaults` on the step; `phases/phase-8.md:21` is phase 8's dated record |
| 🟢 | round 2's finding 3 is closed — `spec.md` ends with the `Framed` line, and `chain_check` accepts it | `seal/specs/1791270164-the-release-seal-is-drawn-in-curves/spec.md:423` | confirmed | executed: `chain_check.py --baseline origin/release/v0.20.0` exit 0 judged as a draft, with the release job's fetches; the PR's `release` job passed. Judged as ready it exits 1 on `round-2.md`'s `nobody` and `not yet` alone |
| carried | round 2's finding 4 — `round-1.md`'s `New units` counts the merge's units | `seal/specs/1791270164-the-release-seal-is-drawn-in-curves/rounds/round-1.md:13` | deferred #860 | already deferred in round 2; #860 is open on the 0.21.0 milestone; round 2's range holds no merge and its `New units: none` is right |
| ⬜ 1 | the allowance's comment says a renderer recognises an SVG by its namespace, and `rsvg-convert` 2.58.4 draws the release SVG identically without it | `tests/test_no_real_identifiers.py:25` | answered | the allowance stands: the release-seal case reads the SVG's elements by that namespace, and an XML parser needs it, whatever `rsvg-convert` tolerates; the comment's one clause about renderers is imprecise and changes nothing the entry allows; executed: the PNG from the SVG with `xmlns` removed is byte for byte the PNG from the SVG as committed. The entry is right; the SVG case reads elements by the namespace |
| ❓ | on the ubuntu and Windows group 2 legs one case that passed at bf1a9447 is skipped at f94e262e; the CI log names no skipped case | `.github/workflows/test.yml` | ❓ out of verified scope | the nine modules that read round records skip nothing new; the orchestrator answers it, by reading skip reasons in the sealer's broad run |

## Paste-ready fixes

no paste-ready fix in the report

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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | PR #859 against `release/v0.20.0` at `559977a3`; `seal/ledger/1791270165-the-windows-test-leg-is-measured-and-cut.md` | round 1's 🔴 1 — fixed |
| round-1 | `skills/verify/scripts/seal_stamp.py:486` | round 1's 🟡 2 — fixed |
| round-1 | `tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py:343` | round 1's 🟡 3 — fixed |
| round-1 | `tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py:551` | round 1's 🟡 4 — fixed |
| round-1 | `skills/verify/scripts/seal_stamp.py:506` | round 1's 🟡 5 — fixed |
| round-1 | `hooks/sealer-stamp.py:40` | round 1's ⬜ 6 — fixed |
| round-1 | `skills/verify/scripts/seal_stamp.py:330` | round 1's ⬜ 7 — fixed |
| round-1 | `.github/workflows/publish-release.yml:111` | round 1's ⬜ 8 — fixed |
| round-1 | `.github/scripts/release-seal.svg:21` | round 1's 🟢 — confirmed |
| round-1 | `skills/verify/scripts/seal_stamp.py:323` | round 1's 🟢 — confirmed |
| round-1 | `skills/verify/scripts/seal_stamp.py:462` | round 1's 🟢 — confirmed |
| round-1 | `skills/verify/scripts/broad_gate.py:2976` | round 1's 🟢 — confirmed |
| round-1 | `.github/scripts/publish_release_note.py:393` | round 1's 🟢 — confirmed |
| round-1 | `seal/ledger/1791270164-the-release-seal-is-drawn-in-curves.md:1` | round 1's 🟢 — confirmed |
| round-1 | `seal/specs/1791270164-the-release-seal-is-drawn-in-curves/spec.md:1` | round 1's ❓ — out of verified scope |
| round-1 | the tree at the last round's target | round 1's ❓ — out of verified scope |
| round-2 | `.github/scripts/release-seal.svg:1` | round 2's 🔴 1 — fixed |
| round-2 | `.github/workflows/publish-release.yml:114` | round 2's 🟡 2 — fixed |
| round-2 | `seal/specs/1791270164-the-release-seal-is-drawn-in-curves/spec.md:419` | round 2's ⬜ 3 — answered |
| round-2 | `seal/specs/1791270164-the-release-seal-is-drawn-in-curves/rounds/round-1.md:13` | round 2's ⬜ 4 — answered |
| round-2 | `seal/ledger/1791270161-the-broad-gate-reads-a-record-its-pytest-plugin-wrote.md:1` | round 2's 🟢 — confirmed |
| round-2 | `skills/verify/scripts/seal_stamp.py:492` | round 2's 🟢 — confirmed |
| round-2 | `tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py:321` | round 2's 🟢 — confirmed |
| round-2 | `tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py:553` | round 2's 🟢 — confirmed |
| round-2 | `skills/verify/scripts/seal_stamp.py:514` | round 2's 🟢 — confirmed |
| round-2 | `hooks/sealer-stamp.py:41` | round 2's 🟢 — confirmed |
| round-2 | `skills/verify/scripts/seal_stamp.py:332` | round 2's 🟢 — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
