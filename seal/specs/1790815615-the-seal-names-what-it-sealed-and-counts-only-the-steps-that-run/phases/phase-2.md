# 1790815615-the-seal-names-what-it-sealed-and-counts-only-the-steps-that-run — phase 2

<!-- seal/specs/<unix-epoch-seconds>-<slug>/phases/phase-<N>.md — what this phase
of the build did, written by the implementer when the phase closes. -->

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | 998adaea |
| Ran by | unknown — the spawn prompt named the agent (`smith`) and not the model; the orchestrator fills this row |

## What this phase was asked

`plan.md` phase 2 (S3, S6 for the panel): `panel` gains the continuation rows
for `tree`/`base` with head/tail elision and an `item` row; `gate` becomes
conditional on a byte comparison, the installed path handed over by `main`'s
redirect in the environment; `from` and `row` are removed; `suite` gains its
`exit N` continuation; `ledger_counts` carries `drifted` and `ledger`
continues; `failure_lines` ends a failing `ledger` with its `total:` line; a
width guard at the point rows are built. `SAMPLE_ROWS` mirrors the panel.
Docs: `agents/sealer.md` (the `gate` paragraph, *base beside `from`*),
`docs/the-broad-gate.md`'s #475 paragraph, `skills/verify/SKILL.md`'s *names
the ref beside the commit* sentence, the `broad_gate.py` module, `panel` and
`gate_copy` docstrings, the `SAMPLE_ROWS` comment. Ledger: `0.12.2` R5
re-read, `0.15.1` G2 corrected in place, `0.15.7` N5 extended. The owner's
answer to Q1, carried by the spawn: the panel keeps its width, a value that
does not fit continues on an unlabelled row beneath its label, and a branch
or ref name is elided at the frame.

## What this phase found

- **The width guard is a pass, not an assertion.** Every value `panel`
  returns goes through `fit` on the way out, so no row can be wider than
  `PANEL_VALUE_WIDTH` and none is cut by the frame without a marker; the
  names are fitted earlier with the side that matters kept (head for the
  branch, tail for the ref). An `assert` in the gate would end a sealed run
  on a traceback over a label, which is the largest possible change to a run
  that passed.
- **`gate_copy` split in two.** The stderr line every run prints still names
  the copy as `tree <version>` or `plugin <version>`; that is `copy_origin`
  now, and `gate_copy` is the panel row, None wherever it says nothing. The
  renamed case `test_the_stderr_line_says_tree_under_the_gated_root_and_plugin_elsewhere`
  breaks the anchor `seal/releases/0.15.1.md` G2 cites by the old name, which
  the phase-4 ledger pass corrects.
- **The invoked path is taken out of the environment, not read from it.** A
  redirected child inherits the variable, and so would every check it runs —
  including a `Broad gate` row's test suite, whose in-process cases of
  `gate_copy` would then be answered for a redirect they never made. `main`
  pops it into `args.invoked_as`; `gate_copy` takes it as an argument and
  reads no environment at all (`test_the_gate_takes_the_invoked_path_out_of_the_environment`).
- **One reading of *the ref is the commit*.** `seal_stamp.ref_is_commit` is
  what `sealed_names` (phase 1) and the row under `base` both ask, so a bare
  SHA as `--base` collapses on the line and on the panel alike. `panel`
  reaches it through a cached `stamp_module()`, which `gate` now uses too.
- **The panel is 22 lines against the disc's 20** at the 0.90 default with
  every conditional row present (rendered from `SAMPLE_ROWS`, 81 columns
  wide, unchanged). `beside` tops both blocks, so the panel runs two lines
  below the disc. That is Q1's answered trade, named here so the first real
  stamp is not a surprise.
- **Seen red (§15):** 25 new and moved cases run against `fb643953`'s
  scripts and documents (restored from kept bytes after): 23 failed. The two
  that passed pin `seal_stamp.letter`, which this phase does not change —
  `test_the_panel_renders_its_rows_and_its_blanks` (the `""` continuation
  lands under the value column) and `test_the_panel_value_width_is_what_the_stamp_actually_gives`
  — and both went red under a mutation of `letter` that stops padding an
  empty label. 24 mutations in all, one at a time, bytecode cleared between
  them; none survived.
- **Ledger, deferred to one pass.** `evidence-check --strict` names 40
  drifted rows and one broken anchor after this phase, most of them on
  `panel`, `gate`, `main` and the documents phases 3 and 4 edit again. R5, G2
  and N5 are re-read, corrected and re-stamped in one pass at the phase-4
  boundary rather than twice (`skills/implement/SKILL.md` §2, *draft as you
  go, write in one pass*).

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The panel's `from` row | The row under `base` (`""`), `broad_gate.py#panel`; `agents/sealer.md`'s exit-0 bullet names it |
| The panel's `row` row | The row under `suite` (`""`), `broad_gate.py#panel` |
| The `gate` row on every stamp, and `plugin <version>` on the panel | `gate_copy` prints `tree <version>` only where the copies differ; the stderr line keeps both words (`copy_origin`) |
| `SAMPLE_ROWS`'s `lint clean` | nowhere — it asserted a check no run makes |
