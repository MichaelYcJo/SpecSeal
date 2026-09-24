# 1790260564-a-moved-file-counts-as-written — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | ed5748ff |
| Ran by | specseal:smith on Opus 5.5 |

## What this phase was asked

#563: a moved sentence is held and never written. `corrected` gets a step
across paths after the per-path loop, pairing sentences removed at one path
with identical fresh sentences added at another, by key and count; paired
sentences are neither `gone` nor `written`. The `CHANGELOG.md` arm keeps its
per-file `lost`/`held`/`split` logic. `corrected`'s rename paragraph is
rewritten, S18 renamed and rewritten to pin silence at `against 0
sentence(s)`, `docs/review-chain-spec.md` sentence 1 corrected in place with
no fold marker, ledger row R1 corrected and U2 re-read. M1 and M2 seen red,
S17 green unedited, the whole test file green, and Q2's and Q3's
measurements recorded. The spawn added: keep the document's net growth small
(it stood at 950 lines of a 1000 ceiling).

## What this phase found

- **The frame's M3 proof does not hold as written.** `spec.md` scenario M3
  says the old S18 assertion (`against [1-9]\d* sentence(s)`) goes red under
  this phase. Executed from a deleted probe on the old fixture: it stays
  green. `moved_section` writes `# a` at the old path and `# b` at the new
  one, so the heading is a real removal and the count is 1, not 0 (43 at
  `c52e8350`). The rewrite is still needed, and for a different reason: to
  pin 0, S18 now moves a file whose bytes are identical, heading included.
  `moved_section` is left as it was, because S17 uses it and S17 stays
  unedited. The rewritten S18 was red at `fe4573d7` at `against 43
  sentence(s)`.
- **Mutating the new unit found two unpinned counts.** With M1–M3 planted,
  `paired_across_paths` survived both of its count mutations with the whole
  module green. Two cases were added: M6 (one copy moved, one corrected — the
  removal count) and M7 (one copy moved, a second written — the arrival
  count). Each is red under its own mutation. M6 is also red at `c52e8350`.
  `spec.md` lists M1–M5 and neither of these.
- **Mutations, one at a time over the whole module, the file restored from a
  copy after each:** the pairing call removed, M1, M2 and S18 red; the paired
  fresh copies still written (the rejected *pair by key, and also still
  write* alternative), M1 and M2 red; the removal count undecremented, M6
  red; the arrival count undecremented, M7 red.
- **M1 and M2 needed a larger pool than the other cases.** Two copies of the
  quote halve each phrase's weight, and with `FILLER`'s twelve files the two
  runs scored 0.75 each, 1.5 against the 1.6 floor. `MORE_FILLER` (48 files)
  puts each at about 0.83. That is arithmetic about the fixture, not about
  the rule; the case says so.
- **Q2 (executed): nothing new.** `82928fc6^..82928fc6` at `c52e8350` and
  at `ed5748ff` both exit 1 with the same three places at the same scores —
  `skills/evidence-check/scripts/correction_check.py:4`,
  `skills/code-review/scripts/chain_check.py:2394`,
  `tests/test_a_record_precedes_the_fixes_it_commissions.py:765` — and the
  removed count falls from 1291 to 245. No row goes to `seal/follow-up.md`.
- **Q3 (executed): unchanged.** `RELEASE_RANGES` passes unedited. The four
  ranges report the same coordinates at the same scores; the removed counts
  move from 60, 61, 35, 156 to 48, 60, 35, 120. The run-merge failure
  scenario did not fire on any of them.
- **Q4: the arm stays per-file.** The pairing runs after every path is
  counted, so the `lost` guard and `split` see each file's own loss first.
  The `#307` and `#557` blocks are green.
- **One record line named a name the tree no longer has.** `spec.md`
  judgment 3 names S18 by its old name, and `evidence-check --strict`
  refused it as NOT-IN-TREE. The line now carries the `NAME NOT IN TREE`
  marker, because it means the old name.
- **`docs/review-chain-spec.md`** sentence 1 is corrected in place and
  `paired_across_paths` joins `Enforced by:`. Net +1 line (951).
- **Gate items** (`CONTRIBUTING.md` §*What a change to a gate must carry*):
  - *Test seen red:* M1 and M2 at `fe4573d7`, whose `corrected` counts a
    move as the base does, each exit 0 with `against 3 sentence(s)`; M6 at
    `c52e8350`; M6 and M7 under their mutations.
  - *Failure direction:* reports more. `wanted` only grows, apart from the
    run-merge effect in `plan.md`'s failure scenario. A wrong deny, a moved
    quote reported, is the report the policy asks for.
  - *Prompt budget:* zero. The sweep prints and exits.
  - *Platform:* pure Python over git output, with no platform surface beyond
    what the module already has. Only macOS was run here.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| S18's old name, docstring and its positive-count assertion (*the old path was read*) | S17 carries that proof; S18 now pins `against 0 sentence(s)`; ledger row M1 in `seal/ledger/1790260564-a-moved-file-counts-as-written.md`, and row R1 of `seal/releases/0.15.1.md` corrected |
| the claim *a pure move writes every sentence back and is silent for that reason* (module docstring of `corrected`, `docs/review-chain-spec.md`) | the corrected sentence in the same places, and ledger row M1 |
