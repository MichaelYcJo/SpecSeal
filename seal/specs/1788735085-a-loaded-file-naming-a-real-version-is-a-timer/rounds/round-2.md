# 1788735085-a-loaded-file-naming-a-real-version-is-a-timer — review round 2

| Field | Value |
|---|---|
| Target SHA | 27c36fea9785313a6ad7eca051d8baf2bd28e4e3 |
| Ran by | specseal:warden on claude-opus-5 |
| PR | 201 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Contract changes | none |
| New units | refusal (depth 1); test_the_exemption_list_does_not_depend_on_the_order_it_is_written_in (depth 1); test_the_declared_token_is_the_one_the_refusal_printed (depth 1) |
| Needs a fix | yes — findings 4, 5, 6 and 7 |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 2, the verifying round, spawned against `27c36fe` with the fix diff
`579a916..e0cb595` as its subject and round 1's closed record to inherit.

The prompt carried one prediction and told the round to test it: that **both of
round 1's paste-ready fixes had carried the defect their own finding was about,
one layer down** — the reviewer's `(?!\w)` with no case behind it, and the
`DATED_RECORD` search over the whole path that left a dated directory exempting
everything under it — and that the same should be assumed of the repairs to the
repairs. It also carried the orchestrator's own re-execution of eight token
shapes and three paths, so the round could start from measurements rather than
from the fix pass's word.

Two rows of that table were flagged as judgements nobody had argued, and the
round was asked to settle them: `0.9.0rc1` answering `[]`, and `0.9.0.md`
reading as a version.

Four axes beyond the table: the three new cases against the three fixes, asking
what each would still pass with; `Contract changes | none` on a round whose
fixes changed a meaning, as a live instance of #194 to confirm or refute rather
than fix; the message as a deliverable, judged on what a refusal actually
prints rather than on a function's return value; and the ledger fragment read
**unscoped**, since the fix pass had only ever run the check `--ledger`-narrowed
on writes.

The prediction is what the round returned. It holds a third time, on the same
lookaround.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | round 1 finding 1 — a version at the end of a sentence is invisible | `tests/test_release_hygiene.py:58` | answered | closed by `ea02184`. Executed: reverting `(?!\w)(?!\.\d)` to `(?![\w.])` turns `test_a_version_that_ends_a_sentence_is_still_a_version` red, so the new case observes its own fix; `right for 0.8.3.`, `- #179 goes into 0.9.0.` and `ships in 0.9.0...` all answer the version again |
| 2 | round 1 finding 2 — the `docs/experiments/` prefix exempted the directory's own READMEs | `tests/test_release_hygiene.py:114-125` | answered | closed by `e25ff8b`. Executed: reverting the basename read to a whole-path search turns three cases red, and reverting the exemption to a plain prefix turns `test_the_experiments_prefix_covers_only_a_dated_record` red. The exempt set in the loaded tree is now exactly five files, and `docs/experiments/README.md` and `README.ko.md` are scanned — both carry no version token at all, so the widening costs nothing today |
| 3 | round 1 finding 3 — the refusal offered no route for a token that is not a release | `tests/test_release_hygiene.py:159-183` | answered | closed by `e0cb595`. Executed: an offender planted in `README.md` and the real `AssertionError` read — the printed text is `what_to_write_instead()` verbatim, so the extraction is faithful. Deleting the date route and deleting the another-product route each turn the case red |
| 4 | 🟡 the comment above `VERSION_TOKEN` states that `(?!\w)` protects `v1.2.30`, which this branch measured false and says so in two other places | `tests/test_release_hygiene.py:52-58` | **fixed** `4ea09f2` | fixed at 4ea09f2 — ``; executed: `v1.2.30` matches whole with and without the lookahead, because `\d+` is greedy. The module's own comment at `:476` and the ledger's R1 row both say so; the constant's comment, which a reader meets first, still asserts the disproven grounds |
| 5 | 🔴 `(?!\w)`'s only remaining effect is to hide a letter-suffixed prerelease of the unshipped version, which the substring check this branch replaced caught — and a new case pins the hole open with no argument behind it | `tests/test_release_hygiene.py:58` and `:476-482` | **fixed** `4ea09f2` | fixed at 4ea09f2 — ``; executed at running `0.9.0`: `0.9.0rc1`, `0.9.0b1`, `0.9.0a`, `0.9.0_final` and `v0.9.0rc1` all answer `[]` while the substring test is True for every one, and the dash spelling `0.9.0-rc1` is refused. Same grounds round 1's finding 1 was rated on. The shape is not present in the tree today |
| 6 | 🟡 the `VERSIONS_OF_ANOTHER_PRODUCT` route cannot be taken on the token the refusal prints — the message reports `v9.9.9` and the lookup reads `9.9.9` | `tests/test_release_hygiene.py:152` and `:170-171` | **fixed** `373b090` | fixed at 373b090 — ``; executed: declaring `(rel, "v9.9.9")` exactly as printed leaves the file refused; only the `v`-stripped key works, and nothing says so. This is the wall #179's *Done when* makes the deliverable, reached by following the message's own instruction |
| 7 | 🟡 the recorded limit — that no assertion can pin which expression an `assert` uses as its message — is false, and it is written into the ledger as a measured fact | `tests/test_release_hygiene.py:196-206` and the fragment's R3 notes | **fixed** `4616577` | fixed at 4616577 — ``; executed: replacing `+ what_to_write_instead()` at `:292` with a literal leaves all 28 cases green, so the gap is real. Extracting the refusal into a builder, exactly as `what_to_write_instead` was already extracted, closes it with an ordinary assertion and no source reading |
| 8 | ⬜ replacing `any()` with a loop that returns on the first prefix match made `RECORDS_OF_A_MOMENT` order-dependent | `tests/test_release_hygiene.py:117-125` | **fixed** `ad1e364` | fixed at ad1e364 — ``; executed: an exact entry, or a narrower prefix, written after `docs/experiments/` is unreachable — `False` where `any()` answered `True`. No instance today, and the failure direction is loud (a red check), but appending at the end of that list is the natural act |
| 9 | ⬜ `DATED_RECORD`'s shape is unpinned — two mutations leave every case green, one of them silently widening the exemption | `tests/test_release_hygiene.py:114` | **fixed** `7349afc` | fixed at 7349afc — ``; executed: dropping the trailing `-` makes `docs/experiments/2026-09-03.md` exempt where it is scanned today, and loosening the component widths changes nothing any case can see. The pattern as written is faithful to the README's prescribed name, so this is case strength rather than a wrong pattern |
| 10 | ⬜ round-1.md's `Fixes checked by` still reads "nobody" in the very commit that filled all three verdict cells with fix SHAs, and those three grounds cells each carry an empty inline code span | `rounds/round-1.md:9,50-52` | answered | the generator answered the first half itself: writing `round-2.md` set `round-1.md`'s `Fixes checked by` to `round-2`, which is the field's designed answer. The empty inline code spans are the orchestrator's own input — the fix table's `Commit or grounds` cell was handed a commit AND its grounds, and the generator re-serialised the pair. Round 1's record is left as committed rather than corrected in place, which is the hazard #159 names |
| 11 | ✅ `Contract changes: none` is correct under the definition and blind to what these fixes changed — #194, confirmed as a measured instance | `docs/review-handoff-protocol.md:124`, `tests/test_release_hygiene.py:117` | answered | `is_a_record_of_a_moment` answers `False` where it answered `True`, with signature, arity, return type and returnable-value set all unchanged. Confirmed, not fixed — #194 is live at `docs/flow.md:55` |
| 12 | ✅ the ledger fragment's three rows all resolve, unscoped | `seal/ledger/1788735085-a-loaded-file-naming-a-real-version-is-a-timer.md` | answered | executed `./bin/evidence-check .` with no narrowing: 718 ok · 0 drifted · 0 broken · 0 external · 0 old-format, exit 0. The fragment contributes 16 anchors, up from round 1's tree-wide 713 |
| 13 | ✅ the widening and the narrowing left the loaded set clean | the nine `LOADED` prefixes at `27c36fe` | answered | executed: 64 files walked, no offender. `docs/experiments/README.md` and `README.ko.md` are inside the checked set for the first time and hold no version-shaped token at all |

## Executed probes

| What was run | Result |
|---|---|
| `./bin/test tests/test_release_hygiene.py -q` at `27c36fe`, fresh `--no-local` clone | 28 passed, exit 0 |
| 10-mutation matrix over the module, one at a time, `tests/__pycache__` cleared between | 8 caught, 2 survived — `DATED_RECORD` losing its trailing dash, and `DATED_RECORD` with unbounded component widths. Each of the three new cases went red on its own fix's reversion |
| 22 token shapes through `timers_in` at running `0.8.3` | matches the orchestrator's table row for row, plus `0.9.0-rc1` refused, `0.9.0b1` / `0.9.0a` / `0.9.0_final` allowed, `x0.9.0` allowed, `v0.9.0.` and `CHANGELOG-0.9.0.md` refused |
| `VERSION_TOKEN` with and without `(?!\w)`, over `v1.2.30` and `0.9.0rc1` | `v1.2.30` identical either way; `0.9.0rc1` is the only difference |
| nine prerelease and sentence-final shapes through `timers_in` at running `0.9.0`, beside the substring check this branch replaced | five shapes the substring check caught and `timers_in` does not, all letter-suffixed |
| an offender planted in `README.md`, the real case run, the `AssertionError` read | three offender lines, then `what_to_write_instead()` verbatim — the extraction is faithful to what a person sees |
| `VERSIONS_OF_ANOTHER_PRODUCT` declared with the token as the refusal printed it, then with the `v` stripped | still refused, then exempt |
| `is_a_record_of_a_moment` with an exact entry and a narrower prefix appended after `docs/experiments/` | `False` in both, where `any()` answers `True` |
| `DATED_RECORD` over six basenames | `2026-09-03.md` and `2026-09-03` are not exempt; `README-2026-09-03-c.md` is not; `9999-99-99-x.md` is |
| the loaded-set enumeration at `27c36fe`, and the two newly-scanned READMEs read for tokens | 64 files, no offender; both READMEs hold no version-shaped token |
| `./bin/evidence-check .` unscoped at `27c36fe` | 718 ok · 0 drifted · 0 broken · 0 external · 0 old-format, exit 0 |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `tests/test_release_hygiene.py:56` | round 1's 1 — fixed |
| round-1 | `tests/test_release_hygiene.py:82` and `:102-107` | round 1's 2 — fixed |
| round-1 | `tests/test_release_hygiene.py:196-215` | round 1's 3 — fixed |
| round-1 | `62287e9` and `86a6e20` | round 1's 4 — answered |
| round-1 | `tests/test_the_pull_request_language_is_the_repositorys.py:764-786`, `seal/ledger.md:562`, `rounds/round-5.md:68,80` | round 1's 5 — answered |
| round-1 | `seal/ledger.md:550,562` | round 1's 6 — answered |
| round-1 | the nine `LOADED` prefixes at `579a916` | round 1's 7 — answered |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `Contract changes` reads `none` for a unit whose meaning changed | #194, already open at `docs/flow.md:55` | the session that takes #194 — not this branch |
