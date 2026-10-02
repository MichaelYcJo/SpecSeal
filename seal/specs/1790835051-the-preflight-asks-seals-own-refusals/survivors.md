# 1790835051-the-preflight-asks-seals-own-refusals — survivors

Places `survivor-check` reports that still carry wording a range removed,
judged and kept.

| Path | Quote | Grounds |
|---|---|---|
| `seal/specs/1790815611-the-record-arms-run-before-the-sealer-is-spawned/spec.md` | It writes no cell, no values file and no stamp, runs no `round_record.py seal`, adds no worktree | #638's own spec, stating what #638's preflight did. It was true of that work item, and it is a past-state record this work does not edit (`spec.md` §Scope; `settle` folds released specs). The removed sentence was the same claim in `broad_gate.py`'s module docstring, where #702 made it false; the docstring now says the preflight runs `seal --check` and writes nothing. #638's changelog fragment, the text a release reader meets, carries a dated sentence naming #702 |
| `seal/specs/1790815611-the-record-arms-run-before-the-sealer-is-spawned/spec.md` | **Exit codes**, unchanged in meaning: 0 every arm passed · 1 an arm failed · 2 refused with nothing run. | #638's spec, true of #638's preflight, which asked no `seal --check`. The removed sentence was the docstring's exit-code line for `--preflight`, rewritten to count a `seal --check` refusal under 1. The meaning of each code is unchanged: 1 is still a finding about the record and 2 still means nothing ran |
| `docs/commit-review-gate-spec.md` | the same key the commit gate reads | True as it stands, and ratified policy this work does not edit (`spec.md` §Out). It names the commit gate alone, which does read the declarations the way `item_dir` does, from the working tree. The removed sentence, in `broad_gate.py`'s `gate`, named the chain arm too, and the chain arm reads only declarations committed at HEAD (round 1's ⬜ 3) |
