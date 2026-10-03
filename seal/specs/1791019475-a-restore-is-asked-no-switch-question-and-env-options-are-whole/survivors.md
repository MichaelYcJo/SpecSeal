# Survivors — a restore is asked no switch question, and env's options are whole

`survivor-check --range 2b1dcb1f...HEAD` reported three places that still
carry K3's old wording, that the table was built from the two synopses and
lacked two rows. The comment above `ENV_SPELLINGS` was this branch's to fix,
and it was fixed. The two below belong to records this branch may not
rewrite.

| Path | Quote | Grounds |
|---|---|---|
| `seal/releases/0.16.0.md` | of both synopses' options (all but two, BSD's `-` and GNU's `--env0-from`, deferred to #737 — Corrected 2026-10-03) | E14's round-2 note, dated and in a released file, which is never edited after its release (`seal/config.md` `Ledger frozen from`). The `Re-read · E14` row in `seal/ledger/1791019475-a-restore-is-asked-no-switch-question-and-env-options-are-whole.md` says the table now holds both rows |
| `seal/specs/1790993140-the-gates-read-config-env-env-s-and-an-unresolved-cd/overview.md` | built from GNU coreutils env's and BSD/macOS env's synopses | a closed work item's account of its own build at its own commit, which `spec.md` §*Out* keeps unrewritten; K3, the live claim, is corrected |
