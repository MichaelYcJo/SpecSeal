# 1788229400-every-branch-appends-to-the-same-two-files — review round 6

The verifying round for round 5's fixes. All nine are closed. Two of the
fixes opened something, and one of those is the third 🔴 at a site two
earlier rounds already closed.

| Field | Value |
|---|---|
| Target SHA | `d0dfd4e` |
| Diff base | `5bf9ce2` — the state round 5's record was written at |
| Fix commits under review | `43fab14` · `8f61cd6` · `4784d04` · `d0dfd4e` |
| PR | not yet |
| Broad gate | not yet — slices only; a 🔴 is open, so it is not yet the time for it |
| Fixes checked by | `round-7` |
| Needs a fix | yes — 🔴 J and 🟡 K |

- [ ] Pass

## Round 5's nine, answered on this round's grounds

| # | Answer | Settled by |
|---|---|---|
| 🔴 A | **fixed** `43fab14` — `git show <sha>:./<rel>` resolves against `-C`. Removing the `./` turns the pin red, and the new pin is red against `5bf9ce2` too | executed |
| 🔴 B | **fixed** `43fab14`, all three commands — `check` BROKEN at exit 2, `--migrate` counts it in `left` at exit 1, `--reverify` exits non-zero. Verified with a real `chmod 000` ledger rather than a monkeypatch | executed |
| 🔴 C | **fixed** `43fab14` for the two directions it named — and a third opened, 🔴 J | executed |
| 🔴 D | **fixed** `43fab14`, both halves — the symlink survives, the file behind it is updated, mode `0664` is preserved | executed |
| 🔴 I | **fixed** `43fab14` for direct escapes; one placement branch was missed, 🟡 K | executed |
| 🟡 E | **fixed** `43fab14` — the hook carries `unproven`, and removing it kills the pin | executed |
| 🟡 F | **fixed** `43fab14` for the `--map` half; the rest **answered** — a `parity.md`-only repository keeps the scan off and reports `BROKEN … file not found`, which is not round 4's 🔴 3 (`EXTERNAL` at exit 0) | executed |
| 🟡 G | **answered** `8f61cd6` — Known limits names the one-line constant as the cheapest twin, with the `TIMEOUT` / `RETRIES` example, pinned | read |
| 🟡 H | **fixed** `8f61cd6`, all four documents — three carry regex pins, the advisor's docstring an `ast` pin | read |

## The new units, judged as code rather than as fixes

This is the axis round 5's record named as the one that would have caught four
of its nine a round earlier. It was walked here, and it is what found 🟡 K.

- **`contained(repo, rel)` `:645` — correct.** Both sides go through
  `os.path.realpath`, so a citation that leaves by symlink is caught too, and
  `full == inside or full.startswith(inside + os.sep)` rules out the
  `/repo` / `/repo-other` prefix collision. An absolute `rel` is rejected
  because `os.path.join` takes it and leaves the tree.
- **`cross_repo_intent(root, maps, default_repo, raw_path)` `:694` — behaves
  correctly, but its new `foreign` term is dead.** What fixed 🟡 F was the
  removal of `bool(maps)`. 🟢, recorded below.
- **`place` `:658`, reworked — one branch short.** 🟡 K.
- **`check_ledger`'s tie-break `:813-838` — correct.** It slices the region
  the same way the OK path at `:864` does, so a reconstruction really is one;
  `want` is always present by `ANCHOR_RE`.
- **`write_atomic` `:609` — correct.** `realpath` before `mkstemp` keeps the
  temp file beside the real one, so the rename stays atomic.
- **`content_at` `:904`, `migrate` / `reverify`'s unreadable handling, and
  `hooks/ledger-migrate.py:170-177` — correct**, each confirmed by a mutation.

## The three judgements the implementer asked for

**The Q3 divergence stands, and the reviewer supports it.** Where no place
reconstructs the recorded hash, §Q3 said DRIFTED and the code says BROKEN.
The implementer's grounds were that `--reverify` refuses a row resolving to
several places, so an unhealable DRIFTED is exit 1 forever. Confirmed in the
code at `:1147` and executed: `check` says BROKEN-ambiguous at exit 2 while
`--reverify` says `0 rows re-verified` at exit 0. Told to re-verify, a person
would get silence. BROKEN means *go and look*, which is the act that case
needs.

**`STATEMENT_WORDS` may only narrow — the reasoning holds, two of its three
claims do.** That `--reverify` makes the hash and so cannot use it to break a
tie is true in the code, and keeping the narrow structural guard follows from
it. Old and new modules were run side by side on nine inputs: `public new void
Render(int x)` and `case loading(String)` now resolve to their own spans, and
`render(1);` is no longer a declaration. The third claim — that `return
render(y);` is still not a declaration — **holds only while a real declaration
remains in the file**, and the case where none remains is 🔴 J.

**Both scope decisions were inside their permissions.** The `.specseal/map.md`
edit corrected one prose sentence this branch had made false, which is the
removal-not-append case `CLAUDE.md` names; the row count is unchanged at
`29 ok` on both sides. Rewriting three fragment rows rather than removing them
was right because their anchors all survive and only the hashes moved; the one
row whose claim reversed keeps a Notes cell saying so, which removing and
re-adding would have erased.

## Verdicts

What this round opened.

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 J | `return out or blocked` brings keyword-blocked candidates back when none survives — and those include pure call statements, not only the C#/Swift declarations the resurrection was written for. Move a `render` out of `src/app.js` leaving `return render(y);` and the row reads DRIFTED instead of BROKEN-with-destination; `--reverify` then anchors the claim onto the call site and every later check reads `1 ok`, exit 0, permanently. **This is round 4's 🔴 2 returning for every file that is not `.py`** — most of what adopts this skill | `evidence_check.py:380` | **open** | Reviewer-executed old and new side by side; orchestrator confirmed by reading `:359` and `:380` — the narrow guard requires an empty `pre`, so `return render(y);` never reaches it. Not caught by this repository's CI: its own ledger cites only `.py` (the `ast` path) and `.md`/`.yml` (the text path) |
| 🟡 K | `place`'s `--default-repo` branch returns without a containment test, where the `--map` and root branches have one. With a source file in the other checkout symlinked outside the tree, the row is read and reported `1 ok`, exit 0 — the direction 🔴 I closed. `place`'s own docstring claims the test is against the repo it returns, which is false for this branch | `evidence_check.py:690` | **open** | Reviewer-executed; orchestrator confirmed by reading all three branches. 🟡 rather than 🔴 because it needs `--default-repo` passed explicitly and a symlink inside the other checkout |

## 🔴 J is the structure signal, for the second time in this run

`docs/review-chain-spec.md:41` fired at round 5 and fires again here, and
`CLAUDE.md`'s 3+ Fix Rule is now satisfied exactly: round 4's 🔴 1, round 5's
🔴 C and this are three attempts at one rule. The two failure modes are one
ambiguity — drop `or blocked` and 🔴 C returns, keep it and 🔴 J stands — so a
keyword list cannot separate them and a fourth patch there was not written.

The question went to the repository owner, who chose the level above for the
second time in this work item: **carry the uncertainty out of `resolve`
instead of trying to remove it.** `resolve` discards which candidates were
blocked, which is why neither consumer can act on it. Returned alongside the
places, `check` answers BROKEN with the repo-wide scan where the places are
blocked-only and none reconstructs the recorded hash — round 4's 🔴 2's own
answer, arriving at the path that never had it — and `--reverify` refuses to
bless a blocked-only place and says why. The two cases then stop needing to be
told apart, and the classifier is allowed to stay wrong because being wrong
stops being expensive. Recorded as Q4 in `questions.md`.

The narrow widening the reviewer also offered — dropping `not pre.strip()`
from `:359` — was **not** taken. It closes the C family and leaves Go, Ruby,
Kotlin and Lua, and it would have been the fourth patch at the same site.

## Recorded without a fix (🟢)

- `cross_repo_intent`'s `foreign` term can never be true: both call sites
  (`:752`, `:1093`) sit inside `repo == root`, and a `--map` prefix makes
  `place` return `mapped`. Harmless, and handed over to remove or defend.
- `--reverify` prints nothing for a row `check` called BROKEN-ambiguous
  (`:1147`). A person told to go and look, who runs the heal command, gets
  silence.
- `test_no_document_claims_the_checker_never_calls_git` covers three documents
  and not `.specseal/map.md:26`, which carries the same corrected sentence.
- The unreadable-ledger BROKEN line is printed by the advisory hook with the
  `--reverify` prescription attached, which is not that row's prescription.
  The line itself is true and names the file.

## The verification, verified — and it came out above the implementer's own count

Run from a separate tree (`git archive d0dfd4e`), leaving the working tree
untouched.

| Check | Implementer reported | Measured here |
|---|---|---|
| New pins red against the unfixed code | 15, of which 11 failed | **17 test functions, of which 14 failed** |
| Mutations | 5, all killed | **12, all killed** — one per fix site, each killing exactly one pin |
| Cases | 256 across 12 files | 119 across the 4 files covering changed code · 89 across 4 document-shape files |
| This repository's ledgers | `56 ok · 0 broken` | `56 ok · 0 drifted · 0 broken · 0 external · 0 old-format`, exit 0 |
| ruff on changed files | — | 6 files, `All checks passed` |

The three that passed on the unfixed tree are legitimate controls, one of them
the round 5 finding that had no pin at all — reverting `(identical content)`
to `(content moved intact)` reddens exactly that case. **The implementer
undercounted rather than overclaimed**, which is the honest direction for a
report to be wrong in.

## Not verified, with the answerer named

- The three Windows legs in `overview.md`'s table — `dirty()`'s pathspec,
  `--migrate`'s `git show <sha>:./<rel>`, and `write_atomic`'s symlink half.
  Confirmed to be NAMED; not confirmed to pass. The broad gate's windows leg
  answers them.
- The full suite, tree-wide lint and typecheck — the orchestrator's, once,
  and not yet, because a 🔴 is open.
- Whether `hygiene.yml`'s new step fires on a release pull request — read, not
  run; the orchestrator answers it at the release PR.

## Deferred

Nothing. 🔴 J and 🟡 K go to the implementer with the owner's answer, and
round 7 verifies the diff of those fixes.
