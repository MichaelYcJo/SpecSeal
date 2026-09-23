# 1790138190-settle-leaves-twelve-directories-with-no-way-out — phase 7

| Field | Value |
|---|---|
| Phase | 7 |
| Commit | 0f73c35 |
| Ran by | unknown — the spawn prompt named the agent (`smith`) and not the model, and the value is the spawning session's to give |

## What this phase was asked

Close. `overview.md` finished; `changelog.md`; the ledger fragment written
in one pass with every row the phases drafted; `survivors.md` only for what
`bin/survivor-check --range origin/release/v0.14.0...HEAD` reports and a
person judges correct where it stands (`questions.md` Q6); every row phases
1–6 drifted re-read and re-verified; the final `./bin/settle` report on this
branch written here as what the post-release fold will face. Verified by
`bin/evidence-check --strict .`; `bin/survivor-check --range
origin/release/v0.14.0...HEAD` with this branch's `survivors.md`;
`bin/unverified-check --baseline origin/release/v0.14.0 seal/specs/`;
`skills/code-review/scripts/chain_check.py --baseline origin/release/v0.14.0`
— every exit code read directly. The broad gate is the `sealer`'s, after the
rounds.

## What this phase found

**The four closing commands, on `0f73c35`** (executed, exit codes read
directly, no pipe):

| Command | Exit | What it printed |
|---|---|---|
| `bin/evidence-check --strict .` | 0 | `total: 1527 ok · 0 drifted · 0 broken · 0 external · 0 old-format` |
| `bin/survivor-check --range origin/release/v0.14.0...HEAD --exempt …/survivors.md` | 0 | `examined 360 files at 0f73c35, against 161 sentence(s) the range f8f1c9d..0f73c35 removed`; seven places printed under `exempt` |
| `bin/unverified-check --baseline origin/release/v0.14.0 seal/specs/` | 0 | `7 overviews · 14 open · 3 closed · 0 unreadable` |
| `chain_check.py --baseline origin/release/v0.14.0` | **1** | `…/routing.md:0  declares through the review chain and …/rounds/ holds no round-N.md` |

**The chain check's 1 is the state this branch is in, not a defect.** The
declaration routes the work through the review chain and no round has run
yet; the round record is what the check reads as evidence of review, and
the orchestrator's first round is what writes it.

**Q6: the sweep reported fifteen places, and every one is correct where it
stands** — judged one by one and written to `survivors.md` with a quote and
grounds. What this branch removed is the range row's use *by a fold* and two
`settle.py` passages that moved; the range row itself, which the reported
places describe, still ships for every branch that deletes a shipped section.

**A finding outside this work's scope, measured here.** Once `survivors.md`
was committed, the sweep over the same range reported **seven** places, not
fifteen — with `--exempt` and without it (executed, `7 place(s)` at exit 1
with no `--exempt`). The eight quotes that went quiet are in the range as
wording the range added, so `survivor_check.py#wanted` subtracts them as
wording the fix wrote, and their survivors vanish rather than printing under
`exempt`. That is #365's shape — a record that quotes the wording disarming
the check — arriving through `survivors.md` instead of `rounds/`. It predates
this branch, and closing it is new mechanism in the sweep, so it is named in
`overview.md` §*Not done* for the repository owner to file rather than fixed
here.

**The final `./bin/settle` on this branch** (executed, exit 0) — what the
post-release fold will face, with `--released-at origin/main`:

- `released and unfolded: 0 work items in 0 segments, 2 ungrouped, 0 skipped`;
  `2 unreleased and untouched` (`1790134781` and this one); `no spec.md: 8 to
  retire by the rule, 2 kept by it`.
- ungrouped, each with a spec to fold: `1788184145`, `1790119502`.
- retired by the rule: `1788217118`, `1788220055`, `1788276387`,
  `1788425222`, `1788824000`, `1788938400`, `1789024700`, `1789053786` —
  each *nothing open, and nothing outside seal/specs/ cites into it*.
- kept by the rule: `1788177600` (*whether the hooks fire on Windows from
  this tree*, *the conformance evals*) and `1788395377` (*The guard refusing
  a real release with a real open row …*, *The broad gate*).
- no `anchored` heading: the one row G4 answered is gone.
- 45 `tests/` files under the readers heading.

Once released, this work item and `1790134781` join that list: this one with
a spec to fold, `1790134781` kept by the rule until its three open rows
close.

**Rows.** The fragment was written in one pass at this phase: twelve rows
beside phase 2's G4, every anchor outside `seal/specs/`, hashes computed by
`--reverify`. `evidence-check --strict` refused two things on the way, both
mine and both fixed: `seal/ledger.md:78` written as prose in a row read as
an old `path:line` coordinate, and a retired case name on a phase record's
line, which now carries `NAME NOT IN TREE`.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
