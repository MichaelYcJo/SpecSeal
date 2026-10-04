# a work item's directory is sorted by how long each part matters — questions for the planner

<!-- seal/specs/1791076835-a-work-items-directory-is-sorted-by-how-long-each-part-matters/questions.md
     The run is unattended: the owner answered the routing batch once
     (2026-10-04, `automation`) and nobody is asked anything during it. So no
     row here waits on a person. Each person-kind row is decided by this
     frame, with the answer written in and the grounds in `spec.md`, and a
     person may overturn it by opening what the frame opened. -->

**Judgments the ticket left open that the tree answered.** They are listed so nobody reopens them. Each one's grounds are in `spec.md`.

- **Which readers exist.** Enumerated by `grep` for every path segment, then opened: spec §*The readers, enumerated*. None reads a released item's process record after its release except the release seal at publish, and the survivor sweep, whose own docstrings say its input should already have expired.
- **Whether anything cites a round record by ledger anchor.** Measured: no ledger row anchors inside any work item's directory.
- **One file per run.** Rejected by the size target: 41 of 53 runs exceed 64 KB (D2).
- **Whether the paths move.** They do not (D1).
- **Whether `routing.md` leaves early.** It does not; `chain_check` keys retirement on it (D4).
- **Whether the ledger freeze is a precedent for leaving released items alone.** It is not; its grounds do not hold for round records (D5).
- **When the earliest safe removal is.** After the release reaches `main`, which is `settle`'s existing *released* test (D3).

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | Does the process record leave the tree before the fold, or only with the directory? | a person: decided by frame | **Before, by a mechanical arm**: 62% of the files and 67% of the bytes under `seal/specs/` leave at step 2b of every release, whether or not the fold runs. **Only with the directory**: no code changes, and the files wait for a judgment that has not run since 2026-09-24. The second is this plan's fallback cut | **Before**, by `settle --retire-process` (D3). Not tied to anything a person must be accountable for; overturned by taking the fallback cut in `plan.md` | decided by frame |
| Q2 | The flag's name | a person: decided by frame | `--retire-process` names the class with `docs/one-root-by-lifetime.md`'s own term (*the process record*) and keeps `settle`'s verb. `--drop-records` reads as the whole record. A subcommand would be the first in `settle` | **`--retire-process`**. A rename costs one string and its pins | decided by frame |
| Q3 | Are the 55 released directories exempt (frozen), or does the arm take them? And does this work item run it? | a person: decided by frame | **Exempt by a cutoff**: they stay until the fold, and only items after this one ever leave early. **Taken**: the arm treats every released item alike, as `--retire` does. **Run here**: a 525-file deletion inside a reviewed diff | **Taken, and not run here**: the first run is its own `[no-review]` pull request at 0.18.1's step 2b or later (D5) | decided by frame |
| Q4 | Does any test that reads the real corpus pin a file the arm would remove from a named released item? | a measurement | One run: copy the tree to a scratch directory, run the arm there against a local ref holding the 55 items, run the real-corpus test modules named in spec §*The readers, enumerated*. Each already accepts an empty `seal/specs/`; a pin on one named item's `phases/` or `rounds/` would go red | Assumed none. The build runs it in phase 2 and fixes a pin it finds the way a fold owes it (`docs/release-checklist.md` §2b: *an answer for every check … carrying a population floor over `seal/specs/`*) | ⬜ |
| Q5 | Did any shipped `survivors.md` quote row excuse a survivor in a range run after its own release? | a measurement | Run `survivor_check.py` over the merged ranges since 0.15.4 with and without the shipped `survivors.md` files and compare the `exempt` lists. A match means the arm removes an exemption a later run still used | Assumed none, on the module's own docstring (a `survivors.md` "lives until the release that ships it"). Not blocking: a lost exemption degrades to a reported survivor, the loud direction | ⬜ |
| Q6 | Where in `skills/settle/SKILL.md` the arm's section goes, and the exact wording of its output lines | the work | Phase 1 decides it against the existing sections and pins what it writes | — | ⬜ |
