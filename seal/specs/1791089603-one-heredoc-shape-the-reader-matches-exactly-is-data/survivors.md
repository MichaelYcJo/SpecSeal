# Survivors — one heredoc shape the reader matches exactly is data

Round 1's fix pass rewrote the reason `main`'s comment gives for keeping the
command as written in its plainness and consent reads. The fact the comment
states did not change: both reads still see the command as written. Only the
reason did, which used to claim both directions were safe.

| Path | Quote | Grounds |
|---|---|---|
| `seal/specs/1791089603-one-heredoc-shape-the-reader-matches-exactly-is-data/spec.md` | `is_plain`, the consent reads and everything that writes a record keep the command as written. | the frame's interface statement, and still true at the fix's tip: `main` hands `is_plain` and `has_marker` the command as written. It states no reason, so the corrected reason has nothing to contradict here; the direction the consent read runs is #773's |
