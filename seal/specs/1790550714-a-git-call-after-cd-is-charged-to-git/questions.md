# a `git` call after `cd` is charged to `git` — questions for the planner

<!-- seal/specs/1790550714-a-git-call-after-cd-is-charged-to-git/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

**No row needs a person, and none blocks the build.** Every row below has a
default the build proceeds on.

**Judgments #377 left open that the tree answered.** They are listed here so
nobody reopens them. The grounds are in `spec.md` §*Decided from the tree* and
`plan.md`'s Alternatives table.

- The shape is candidate 1, command position, for `git` alone. `test`,
  `lint/type` and `build` stay unanchored (0.9.4 S1's shapes).
- The negative direction holds by tokenising: a `git` inside a quoted string
  or as an argument is not a command word. A command substitution is not a
  command position.
- A two-family line is charged as today, first match in `FAMILIES` order.
  `cd x && git add . && pytest` is `test`.
- Newline-separated commands and commands after a heredoc's closing line are
  in scope, and the heredoc body removal applies to every family.
- `hooks/cmdline.py` is not reused: the two trees do not import each other.
- The `other` note keeps its wording.
- A family for `python3 - <<'EOF'` is out, and so is `broad-gate` joining
  `test`. Both are recorded with numbers in `spec.md` §*Out* for the owner's
  0.16.0 planning.
- `payload_meter.py` shares no family code and is not absorbed.

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | How do the 0.15.5 run's own segment readings (#619) move under the new rule? | a measurement | the tree cannot answer it: the transcripts are on the machine that ran 0.15.5 (#619's paths are under another user's home directory), and none of the 349 SpecSeal transcripts on this machine is dated 24–27 September (searched 2026-09-28). What #619 printed was read instead: 8 of its 104 listed `slowest` commands move `other` → `git`, and no warden round's do. One command answers it on that machine after the build: `session_cost.py --segments <the 0.15.5 run's transcript>` at 2037cf0 and at the tip, then compare the family rows | not claimed. `overview.md` §*Not verified* carries it with its answerer: whoever next works on the machine that holds the 0.15.5 transcripts, which is the owner's | ⬜ |
| Q2 | Does a test build a call dict for `analyse` without going through `load`, so that the new key is absent? | the work | the frame found no direct `analyse(` call in `tests/` (read, `grep`), but `--spawns` and `--segments` slice `load`'s calls, and a synthetic path may exist that the grep missed | `analyse` reads the new key with `command` as the fallback, so a hand-built dict classifies as today | ⬜ |
| Q3 | Which ledger rows does the edit drift? | the work | the frame's expected set is in `spec.md`'s enumeration: `#analyse` ×7, `#load` ×4 if edited, `#FAMILIES`, `#family` and `#HEREDOC` through 0.9.4 S1 and S2, and any `tests/test_session_cost.py#…` anchor on a case whose docstring is edited. Only `evidence-check` at the tip answers it | re-read every row `evidence-check` names. Where one is outside the expected set, the phase record says why | ⬜ |
