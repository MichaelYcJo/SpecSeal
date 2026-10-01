# Survivors — a joined project's `specs/` is read and never taken

Round 1's fix pass (🟡 1) narrowed the marks from "a `rounds/` directory" to
"a file under `rounds/`, as git tracks it", and corrected every place that
instructs somebody. What stays is the approved frame, which records what the
owner approved and is not rewritten; `overview.md` §*Where spec and
implementation diverged* holds the narrowing and its grounds.

| Path | Quote | Grounds |
|---|---|---|
| `seal/specs/1790815614-a-joined-projects-specs-is-read-and-never-taken/spec.md` | directory, or a `rounds/` directory directly under it | the framer's `spec.md`, approved by the owner as written; the build narrowed it in round 1's fix pass, and the divergence row in this work item's `overview.md` names both sides and the grounds |
