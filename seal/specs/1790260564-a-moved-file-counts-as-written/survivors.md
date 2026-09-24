| Path | Quote | Grounds |
|---|---|---|
| `hooks/review-skill-gate.py` | answers relative from a main tree | That comment describes the gate's own `rev-parse --git-dir` reader, which it joins onto `cwd`, and it is true of that code. Round 1's fix pass removed `local_specs`'s copy of the same observation because the reader moved to `hooks/optin.py#git_common_dir` (⬜ 6); the fact itself was not corrected |
