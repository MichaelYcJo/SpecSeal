# Survivors — MALFORMED is graded like DRIFTED, and rule (a) reads prose as prose

`survivor-check --range origin/release/v0.15.5...HEAD`, run at `353224c2`
after the build's three phases, reported one place. It shares its wording
with the docstring of the renamed malformed case, which said `MALFORMED`
exits 2 "as OLD-FORMAT does". The standing sentence is about `OLD-FORMAT`,
which this work item leaves at exit 2 under both readings.

| Path | Quote | Grounds |
|---|---|---|
| `tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py` | OLD-FORMAT exits 2 with or without the flag, so both readers already agree and the remedy the run names is the migrator. | `test_an_old_format_row_is_silent`'s docstring; `OLD-FORMAT`'s grading did not move (`spec.md` §*Out*), so the sentence is true and the case beneath it still passes |

Round 2's fix pass, `survivor-check --range e9e23deb..HEAD` at `543ba180`,
reported three more places. Each shares a phrase with the example list of
what rule (a) gives up, which the fix replaced with the five rules. None of
them is a copy of that list, and each is still true.

| Path | Quote | Grounds |
|---|---|---|
| `seal/specs/1790381328-malformed-is-graded-like-drifted-and-reads-prose-as-prose/plan.md` | a path-less coordinate with an unquoted space between the marks (`#handler @abcdef12`) goes silent | the failure scenario of the glued-marks alternative in *Alternatives considered*, the record of why that alternative was chosen; the shape is still silent, under the third rule |
| `seal/specs/1790381328-malformed-is-graded-like-drifted-and-reads-prose-as-prose/spec.md` | `org/repo#299's`, `org/repo#299—see`, `“org/repo#299”`, `org/repo#299에서` and `[org/repo#299](https://example.com/org/repo/issues/299)` are prose. | *Scope* item 11, the issue-number shapes #614 named; each is still prose, under the second rule, and pinned by `test_an_issue_number_or_a_version_glued_to_a_word_is_prose` |
| `seal/specs/1790381328-malformed-is-graded-like-drifted-and-reads-prose-as-prose/spec.md` | Nothing shorter than six hex characters is a hash anybody was told to write, which is the grounds for `PATH_HASH_RE`'s lower bound (#614 item 3) | the grounding row for the first rule; the bound it gives grounds for is unchanged |
