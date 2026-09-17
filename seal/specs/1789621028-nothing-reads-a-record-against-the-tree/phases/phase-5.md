# 1789621028-nothing-reads-a-record-against-the-tree — phase 5

| Field | Value |
|---|---|
| Phase | 5 |
| Commit | 7616d187 |
| Ran by | specseal:smith on unknown — the spawn prompt named no model, and the template forbids a segment sourcing that value from its own idea of what it is |

## What this phase was asked

#344's five places, re-located against the tree and then corrected, in
`seal/specs/1789034970-the-contract-is-settled-against-the-agents-that-exist/`.
Q2 and Q3 are answered here. Where a bullet's premise does not hold today, the
record says what was found instead rather than being edited to match the
ticket. An HTML comment beside each correction says what it was read against
and when. Read-only, except Q3's re-measurement.

## What this phase found

**The ticket's five bullets describe a tree that no longer exists, and the
reason is the ticket's own thesis.** #344 was written from
`rounds/round-4-report.md`, whose findings 5 through 9 are the five bullets
with their coordinates. That report names three commits — `3b228f4`,
`8fd2f59` and `bab5c7d` — and **none of the three resolves in this repository
today.** They were the branch's later commits, and the squash into
`release/v0.10.0` kept none of them. So the ticket's evidence is a record
naming commits a merge destroyed, which is the class one level above the one
it filed, and it is the same fact `chain_check.fix_range` treats as a notice
rather than a failure for exactly this reason.

**Bullet by bullet, against the tree at 2026-09-17.**

| #344 says | What is there | Done |
|---|---|---|
| 1 · `rounds/round-3-fixes.md:3` says `ce0f9fe..HEAD` | It says `` `ce0f9fe..ce0f9fe`, empty ``, and one commit — `393da643` — has ever touched the file, so it has never said otherwise. The line the ticket describes existed at `bab5c7d` and was repaired before the branch shipped. **The moving range is one file over**: `rounds/round-2-fixes.md:3`, `` `de7d693..HEAD`, four commits at the time of writing `` | **Corrected** — pinned to `` `de7d693..371347c7` ``. `git rev-list --count` is 4, the count the line already claimed; `371347c7` is the commit that added the file. `de7d693..ce0f9fe` holds 5, which is the range round 3 was given |
| 1b · *round 2's table pinned its range for exactly this reason* | Round **1**'s did — `round-1-fixes.md:3`, `` `e972b5f..b8aa637`, seven commits ``, and `rev-list` confirms 7. Round 2's is the one that moved | Recorded. No edit — the claim is the ticket's, not a record's |
| 2 · `survivors.md:5` describes a set the check no longer produces; `overview.md:6` records *exit 0, 15 exempt* | Both lines say what the ticket says. **Q3 below** | **Corrected** — both commands pinned, with the re-measurement beside them |
| 3 · `rounds/round-2.md:32` points at `tests/test_broad_gate_rule.py:281`, a module constant, and the message begins at `:315` | The premise **holds** and the ticket's second number does not. `:281` is `COUNT_WORD = "One definition in this plugin does hand them over"`. The failure message begins at `:328`, *§2 no longer states the count this case checks, so the number and the sentence have come apart* — not `:315`, and not the `:319` the frame states. At `b8aa637`, the commit that wrote the row, `:281` already held `COUNT_WORD` and `:315` held `for path in agents`, so the Location was wrong when written | **Recorded, not re-pointed.** An HTML comment beside the cell says what was read and when. Re-pointing restarts the rot, and turning Locations into content anchors is `questions.md` Q1, refused across 227 records |
| 4 · `rounds/round-3.md:28` understates a hand-edit | `:28` is blank; `:27` is finding 3's verdict row. The hand-edit disclosure is at `:19`, inside the single-paragraph `## What this round was asked`, and the disclosure it describes is the HTML comment at `round-1.md:12`. The *five columns to two, Location and Verdict folded behind a `·`* the ticket describes is round 4's reading of `round-3-report.md` **at `bab5c7d`**; that file's closure table at `:172` has five columns today, and no two-column `·` row exists in any of the three records | **Recorded.** Nothing to correct: the state the bullet describes went with the commits |
| 5 · A verdict attributes a fix to a commit carrying half of it | **Q2 below** | **Recorded as unreproducible** |

**Q2 — answered, and the answer is that no row matches.** The question was
which verdict row the coordinate-less bullet means. Two measurements, both
executed 2026-09-17:

- Every `fixed` row of the three records — 10 in `round-1.md`, 7 in
  `round-2.md`, 0 in `round-3.md`, which closes all three of its findings
  `deferred`. For each, the commit it names resolves, and **the commit touches
  the file its `Location` names, in all 17 cases.**
- For each fix commit, the commit that follows it on the branch, checked for
  lines the fix added. **No successor reverts any substantive line.** The one
  hit across the whole branch is a lone `)` between `463a6f68` and `60c352e0`,
  a formatting coincidence rather than a revert.

The bullet's real subject is `round-4-report.md:135`, finding 5, which does
carry a coordinate the ticket dropped — `rounds/round-3.md:47`, with `3b228f4`
extending a row and `8fd2f59` reverting it byte for byte. **Today's
`round-3.md` has no `fixed` row at all and no line 47**, and neither commit
resolves. So the claim is not false; it is **unverifiable against this tree at
this date**, because the record it describes and the commits it names were
both destroyed by the squash that shipped the work. That is the outcome
`questions.md` Q2 named as its second option, reached with a reason rather
than by exhausting a search.

**Q3 — answered, and it is the third outcome, plus one the question did not
anticipate.** `survivors.md:5` states
`survivor-check --range origin/release/v0.10.0...HEAD`.

- **The range does not resolve.** Executed: `bin/survivor-check` exits **2**,
  `` `origin/release/v0.10.0` does not resolve in … ``. The release branch was
  deleted after merging, so the command as written reads nothing at all. That
  is Q3's third outcome — the same defect one level up.
- **Pinned to what the ends named** — `d35c874`, the release tip that branch
  was reviewed against per `round-3.md:19`, and `ce0f9fe`, its last commit —
  the run works: 836 files examined at `ce0f9fe` against 88 removed sentences.
- **The instrument moved too, and that is the finding Q3 did not ask for.**
  Over the same pinned range, `survivor_check.py` **as it stood at `d35c874`**
  reports **three** places — which is exactly what #344 claims a re-run gives.
  The script **as it stands today** reports **two**. The difference is 60
  insertions and 11 deletions in that script since (#365 and the added-side
  exclusion). So **pinning a range is necessary and not sufficient**: a
  measurement is reproducible only against a named range AND a named version
  of the thing that measured it.
- **The sixteen was never one run's output**, and the row says so two
  sentences further down: fifteen at the head it was first run against, and a
  sixteenth once a later commit landed. No re-run reproduces an accumulation.
  With `survivors.md` passed as `--exempt`, both readings are exit 0.

**What this phase deliberately did not do.** It did not edit `spec.md` or
`plan.md` of this work item, whose three corpus counts phase 3 measured wrong.
A frame is another party's record of a moment, and the finding belongs in the
build's records and in what the build ships — which is where phases 3 and 4
put it — rather than in an edit to somebody else's document. It did not
re-point a single `Location`. And it did not touch `survivors.md`'s exemption
rows: `survivor-check` matches those against surviving text, so rewriting a
quote there would silently release an exemption. Re-run after the edits with
the pinned range and the file as `--exempt`: **exit 0**.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| Three moving range ends — two `HEAD`s and one deleted branch name — from an earlier work item's records | The pinned commits that replace them, each with an HTML comment saying what it was read against and when. Nothing else owned those ends: the prose around them is unchanged |
