# Implementation Plan: every reader ends a line where GFM does

<!-- seal/specs/1790655302-every-reader-ends-a-line-where-gfm-does/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved 2026-09-29 by the orchestrating session, when `smith` was spawned.

<!-- The line above is the record that the gate happened. Fill it in at the
spawn: reading this plan and spawning the builder IS the approval, so nothing
extra is being asked for here — only that the approval stop living in a
transcript. -->

## Summary

One splitter, `gfm_lines`, moves into the shared reader,
`skills/verify/scripts/unverified_check.py`. Every reader of markdown or
record text outside work item F's files reads through it. Where two readers
share a text, both move in the same commit: `readable` with `round_record`'s
`raw` halves, `folded_items` with `fold_check`'s marker readers, and
`gather_changelog` with `survivor_check#gathered_fragments`. Two readers
whose partner is not GFM split at LF alone. `claude_block` matches `awk`, and
the worktree guard's transcript tails match JSON Lines. A last case lists
every `.splitlines(` left in shipped code with its reason, so the class
cannot quietly grow back.

## Technical context

- **The rule exists and is proven.** `evidence_check.py#GFM_LINE_RE` and
  `#gfm_lines` since C. Its docstring states what moving changes: a region
  holding one of the eight characters mid-line, and a `.py` unit below one.
  It does not change a region holding one only at a line end or on a blank
  line. `gfm_lines(text)` and `text.splitlines()` agree on every text
  without the eight characters, including `""`, a trailing newline and a
  final line with none.
- **How scripts reach the reader.** By path, through `importlib`. That is
  `gather_changelog.py#load_reader`, `fold_ledger.py#load_reader`,
  `correction_check.py#load_reader`, `survivor_check.py#reader`,
  `round_record.py#load`, `chain_check.py#load`, `fold_check.py#reader`,
  `settle.py#load`, `payload_meter.py`'s `_fence_rule` and
  `hooks/review-history-guard.py#reader`. `.github/scripts/` reaching into
  `skills/` is established (`rider_check.py#load_checker`,
  `fold_ledger.py#load_reader`). `issue_claims_check.py` does not load the
  reader today and gains the same `load_reader`.
- **Where a copy must stay.** `evidence_check.py` runs alone in a user's
  `tools/` under `evidence-ci` (the comment above `VENDORED_FENCE_RE`), so it
  keeps its own `gfm_lines` as the vendored copy. A hook must not load a skill
  module on every call (`unverified_check.py#fence_opener`'s docstring), so F's
  `hooks/blocks.py#gfm_lines` stays F's copy. `arm_check.py#_lines` splits
  Python source for splicing and already ends lines where `ast` does. Scenario
  S17 holds all three equal to the reader's.
- **Two pins that will move.**
  - `tests/test_chain_hooks.py#reader_blanking_passes` counts every call
    `readable` makes BY NAME to a module-level function as a blanking pass.
    It must be taught that `gfm_lines` is the splitter and not a pass,
    explicitly and by name. Do not write `readable` differently to slip past
    it (spec M6).
  - `tests/test_a_document_has_room_for_the_next_fold.py`'s equality case
    names `fold_check.gfm_lines`, which this item removes. It becomes S17.
- **Ledger.** Moving the splitter moves no hash on this tree except where M1's
  file is cited, and nothing cites it. The edits themselves drift every row
  whose anchored unit they touch. Those rows are re-read against the edit
  and re-stamped where they stand, at each phase boundary. The row citing
  `fold_check.py#gfm_lines` is REMOVED where it stands and its claim written
  into this item's fragment.
- **F in flight.** F's branch edits other hunks of `unverified_check.py`,
  `evidence_check.py`, `broad_gate.py` and `seal.py` (spec M7). This item
  touches `unverified_check.py#readable`, `#folded_items` and a new unit, and
  only `evidence_check.py#gfm_lines`' docstring. Whichever of the two lands
  second rebases over the other and re-runs its own narrow cases.

**What breaks in six months.** A new reader is written with `splitlines`
because that is the idiom, and nothing notices until a record holds a U+2028.
Phase 5's case is the answer: a new call in an unlisted unit fails until
somebody says which kind of text it splits. The second failure is two designs
standing in one release. F keeps each hook reader's lines on `splitlines` and
maps them to GFM lines. This item puts the scripts' readers on GFM lines
outright. Neither file reads the other's texts today (routing's round reader,
`hooks/routing.py#rounds_unreadable`, does not pair with `readable`), so they
cannot disagree about one text. A later reader that reads a `config.md` or
`routing.md` line through both would have to choose, and the class case
names F as the reason those files are exempt.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| **A. The shared reader holds `gfm_lines`, and the checker keeps a vendored copy held equal by a case** | A copy drifts. S17 holds the reader's, the checker's and `arm_check._lines` equal over every character that matters, and adds F's copy once F lands | **chosen**. `fold_check.py#gfm_lines`' own docstring names the reader as where the single copy belongs, and the checker's copy exists for a reason the tree states |
| B. A new module, `skills/verify/scripts/lines.py`, loaded by every reader and by `unverified_check.py` itself | The shared reader starts loading a module, a new failure on every gate. Every script gains a second load-by-path and a second "copied alone" refusal sentence (`tests/test_a_script_copied_alone_exits_2.py`) | rejected: more mechanism for one regex |
| C. Each reader keeps a local copy | Seven more copies of one regex, each owed an equality case. C's temporary copy in `fold_check.py` becomes the permanent shape | rejected |
| D. Every reader loads `evidence_check.py#gfm_lines` | `evidence_check.py` loads the reader, so the reader loading the checker is a cycle. Scripts that never touch the ledger would load the checker | rejected |
| E. `live_lines` and `readable` take TEXT and split internally, so no caller splits | Changes a signature eight callers use. `fold_ledger.py` and `settle.py` feed `live_lines` `split("\n")` lines on purpose, for a byte-for-byte round trip | rejected for this item. It would be a refactor of its own |
| F. Move `readable` alone and leave the `raw` halves | `round_record.py#swallowed`'s `strict=True` zip raises on the first report holding one of the eight. Everywhere else `raw[i]` is the wrong line, and C's phase 5 recorded that before this frame | rejected: coupled readers move together |
| G. Move the `split("\n")` readers (`fold_ledger`, `settle`, `todo_open_rows`) to `gfm_lines` for one spelling | `gfm_lines` drops the trailing empty element that `"\n".join` needs to give the file back byte for byte, and those readers already end lines where GFM does on newline-translated text | rejected |
| H. Leave the readers #664 did not name (phase 3's extras and phase 4) for a follow-up | Contract §12 is "enumerate the class", and the routing record says this release fixes rather than files. Each is a few lines with a red case | rejected. The phases are separable, and a person may strike 3 to 5 without touching 1 and 2 (questions.md, D8) |

## Phases

Vertical slices. Each phase is one or more commits, ends with its readers'
own modules green, its new cases seen red at `2e392d46`, its S20 comparison
executed, and its ledger rows re-read and written. The full suite, lint and
typecheck are not a phase's. They belong to the sealer after the rounds
settle.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | The splitter lives in the shared reader. `unverified_check.py` gains `GFM_LINE_RE` and `gfm_lines`, and `#readable` and `#folded_items` read it. In the same commit, every `round_record.py` pair (`#open_hider`, `#hiders_close`, `#swallowed`, `#inherited_rows`, `#reach_forward`, `#reach_back`, `#build`, `#fix_table`, `#close`, `#seal`) splits its `raw` with the reader's `gfm_lines`, and `fold_check.py#numbered_statements`, `#markers` and `#marker_digest` do the same. `fold_check.py#gfm_lines` is retired for the reader's. `reader_blanking_passes` learns the splitter by name, S17 replaces the old copy check, and `gfm_lines`' docstrings and `live_lines`' *What this may not touch* are corrected | S1–S4, S17 and S18, each seen red at base (S18 by a planted pass). The modules of `unverified_check`, `round_record`, `chain_check`, `fold_check` and `review-history-guard`. S20 for `unverified-check`, `fold-check` and `chain-check` over this tree | eb6cfa61 |
| 2 | The changelog readers. `gather_changelog.py#live_markers`, `#leaves_open`, `#section_lines`, `#insert` and `#main` read the reader's `gfm_lines`. `#insert`'s section index is taken on the same line list it indexes. `survivor_check.py#gathered_fragments`, `#segments` and `#removed_ledger_rows` move with them. `#live_markers`' docstring names the new shared rule | S5–S8, seen red at base. The modules of `gather_changelog` / release hygiene and `survivor_check`. S20 for `gather_changelog.py --check` and `survivor-check` over this tree | cbbac755 |
| 3 | The independent readers. `correction_check.py#rows`; `chain_check.py#frame_mark` and `#frame`; `payload_meter.py#heading_starts` with ends kept; `issue_claims_check.py#segments` with ends kept, loading the reader the way `gather_changelog.py#load_reader` does; `round_record.py#measure` and `#call_sites`; and `claude_block.py#read_lines`, which moves to LF alone with ends kept (`awk`'s cut, questions.md D6) | S9–S15, seen red at base (S15 per questions.md Q3). Each reader's module. S20 for `correction-check`, `chain-check`, `payload_meter` and `claude_block.py --check` | c7042fa4 |
| 4 | The transcript tails. `hooks/worktree-guard.py#last_user_snippet` and `#last_active_event_epoch` split at LF, as every other transcript reader here does by iterating the file | S16, seen red at base. The worktree guard's module | 2c253dce |
| 5 | The class is held closed. One case walks every `.py` under `hooks/`, `skills/` and `.github/scripts/`. It lists each `.splitlines(` call by enclosing unit with its disposition from spec §*The class, enumerated*, and exempts F's four files and `hooks/blocks.py` by path with F named. `overview.md` §*Not done* records `rider_check.py#inferred_anchor` for after F, with its answerer (questions.md Q1). Ledger fragment and changelog fragment are completed | S19, red with a planted unlisted call. S20 re-run across every moved reader against `2e392d46`. `evidence-check` names no row this item left DRIFTED | 1872352f |
| 6 | *Added by the milestone 49 orchestrator after work item F (#672) landed at `3fc0c5bd`, once phases 1–5 were built and the release branch merged in.* The two `rider_check.py` items #664 still owns. `#riders_in` steps over a marker that starts inside a GFM line, after a break `str.splitlines` makes and GFM does not, so a rider `region_lines` never cuts is no longer read and its stamp is no longer hashed into its own region (F's round 3, 🟡 3). `#inferred_anchor` compares a rider's lines with `py_spans` on `ast`'s numbering rather than `str.splitlines`'. S17 adds F's `hooks/blocks.py#gfm_lines`. `seal/releases/0.9.1.md` S2's claim that every rider block is cut before the hash holds again | Each case seen red before its fix, one mutant per changed branch, the rider modules, `rider_check.py` over this tree | 0fded909 |

This table is also where the work records how far it got. **Status is empty,
or the commit that closed the phase.** Re-read the column after any rebase.

## Operational impact

- **No migration, no new dependency, no new environment variable.** The
  splitter is stdlib `re`.
- **Only a text holding one of the eight characters behaves differently.**
  On this tree that is one closed report, whose two characters sit inside
  fenced blocks (spec M1). A consumer's repository can hold more.
- **Records and changelogs are no longer rewritten with a line break where
  the character stood.** `round_record.py`'s `close`, `seal` and the
  reach-back/reach-forward fills, and `gather_changelog.py#insert`, write the
  character back as they read it. Files written before the change keep what
  they hold.
- **Line numbers in refusals and annotations count at LF, CR and CRLF.**
  Below one of the eight characters a number printed by `round-record`,
  `unverified-check`, `survivor-check` or `gather_changelog.py`'s
  section check changes to the one `grep -n`, git and GitHub show.
- **`fold-check` may refuse once in a consumer's repository.** A document
  listed under `Over the ceiling` whose marker stood after one of the eight
  characters on its GFM line is counted with one marker fewer. The refusal
  prints the new digest to write into `seal/config.md`.
- **Two gates excuse less.** `unverified-check --baseline` no longer treats a
  marker GFM never shows as a fold, and `survivor-check` no longer treats one
  as a gathered fragment. A removal those used to excuse is now reported.
- **`fold_check.py` loads the shared reader on every run that reads a
  document.** A copy of it taken alone was already refused with exit 2 for a
  listed document, and now it is refused for any document.
