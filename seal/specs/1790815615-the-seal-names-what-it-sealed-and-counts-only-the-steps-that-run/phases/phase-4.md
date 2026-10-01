# 1790815615-the-seal-names-what-it-sealed-and-counts-only-the-steps-that-run — phase 4

<!-- seal/specs/<unix-epoch-seconds>-<slug>/phases/phase-<N>.md — what this phase
of the build did, written by the implementer when the phase closes. -->

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | b8170ae5 |
| Ran by | specseal:smith on claude-opus-5-5 — set by the orchestrator, which spawned it with that model and did not name it in the prompt |

## What this phase was asked

`plan.md` phase 4 (S5, S6 for the count): `ONLY_AT_MAIN` beside
`SKIPPED_AT_MAIN` with the four names; `base_is_main(given)` shared with
`skipped_at_main`; `steps_for(workflow, given)`; `unanswered`,
`coverage_line` and `panel` keyed on it; the stderr line's clause naming how
many steps are left out for this base and why. Docs:
`skills/verify/SKILL.md` §*A seal says what it did not answer* and §*What
the count does not say*; `agents/sealer.md`'s release-pull-request
paragraph; `docs/the-broad-gate.md`'s #468 paragraph; `PARTITION`'s comment
block. The cases: a twin of the `SKIPS_AT_MAIN` guard case over `!= "main"`,
seen red by editing a guard in a fixture copy; the A6 case with
`FIXTURE_WORKFLOW` gaining a guarded step; `4 of 9` and `8 of 11` over the
real workflow's names, the stderr clause pinned. The spawn added: the ledger
rows of earlier releases this work drifts are re-read and re-stamped in
place, corrected where the edit made them false (`0.15.1` G2 named).

## What this phase found

- **The measured counts hold.** Over `.github/workflows/hygiene.yml` a base
  that is not `main` gives `4 of 9 not answered` and `main` (or
  `origin/main`) gives `8 of 11` (`test_a_feature_seal_counts_the_nine_steps_ci_runs_for_it`,
  `test_a_release_seal_counts_the_eleven_steps_ci_runs_for_it`), the four
  `!= "main"` guards at the step names `spec.md` §*What was measured* gives.
- **`given` None reads as not-`main`.** `steps_for`, `unanswered` and
  `coverage_line` take the base as an argument that defaults to None, and
  None is what `base_is_main` calls not-`main` — the same answer
  `skipped_at_main` has always given it. The gate always passes
  `base.given`; the default only keeps a caller that knows no base on the
  answer every feature pull request gets.
- **Q4's spellings, fixed by the cases that pin them:** `<k> more run only
  on a pull request into main, so this count leaves them out.` and `<k> more
  are steps CI skips on a pull request into main, so …`, singular forms for
  one; the main sentence now says *runs N steps for this base*, and the
  all-answered sentence names the steps *for this base* too.
- **The guard case shows itself able to fail.** Rather than a separate red
  run, `test_the_steps_left_out_off_main_are_the_steps_guarded_off_main`
  turns one `!= "main"` guard of the real workflow around in a copy and
  asserts the reader's set then differs from `ONLY_AT_MAIN`.
- **Not the case the plan named.** `plan.md` said
  `test_the_gate_reads_the_given_base_exactly_once` moves because
  `base.given` gains readers; it counts `args.base`, which is still read
  once, and it is green unchanged. What did move is `gate`'s own comment
  naming the readers of `base.given`, and `seal/releases/0.12.2.md` R2, which
  listed two and is corrected to name the count's.
- **`test_a_seal_that_answers_every_step_says_so` had a silent no-op.** Its
  fixture was built with a `str.replace` whose pattern the new guarded
  milestone step no longer matched, so the case would have kept passing over
  a workflow it did not build. It now asserts the pattern is present before
  replacing, and is keyed on the base as the plan asked.
- **The ledger pass for the whole work item ran here** (deferred from phase
  2, `phases/phase-2.md`). 27 rows of earlier releases cited an anchor this
  branch drifted or broke; each was read against the edit and given a dated
  note, and six were made false and corrected in place —
  `seal/releases/0.12.2.md` R2 (the readers of `base.given`) and R5 (*beside*
  became *under*), `0.15.1.md` G1 (*one row and one line* became *one line*)
  and G2 (the conditional `gate` row, its broken test anchor re-pointed at
  the renamed case, `copy_origin` added), `0.15.4.md` S3 (the count is no
  longer unchanged at `main`) and `0.15.7.md` N7 (the label's two shapes);
  `0.15.7.md` N5 was extended with `branch` and `pr`. `evidence-check
  --reverify --checked 2026-10-01` then re-stamped 29 rows, and
  `evidence-check --strict .` exits 0: `3205 ok · 0 drifted · 0 broken`.
- **A phrase a shipped skill may not carry.** The first draft of the new
  §*A seal says what it did not answer* sentence said *a feature seal of this
  repository*, which `seal/releases/0.15.1.md` N3 records the verify skill
  as not saying; it names SpecSeal instead.
- **Seen red (§15):** the 14 new and moved cases run against `986986f9`'s
  gate and documents (restored from kept bytes after): all 14 failed. 13
  mutations, one at a time, bytecode cleared between them; none survived.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
