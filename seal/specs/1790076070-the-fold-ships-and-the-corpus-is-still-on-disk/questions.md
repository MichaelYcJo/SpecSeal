# the fold ships, and the corpus is still on disk — questions for the planner

<!-- seal/specs/1790076070-the-fold-ships-and-the-corpus-is-still-on-disk/questions.md
— decisions only a human can make. The run is `automation`: nobody will be
asked, so every row below says why the tree could not settle it, and every
default continues. -->

## What the tickets left open and the tree answered — do not reopen

Each of these was a judgment the issue deliberately did not make. The framer
made it from the tree, and the grounds are where a reviewer can open them.

| Settled | Where the grounds are |
|---|---|
| where each of the 38 segments' prose goes, and which five `docs/` files are created | `plan.md` §*Destination map* |
| what happens to the 16 ungrouped — 5 folded, 11 kept, each named | `spec.md` §*The rule for the ungrouped* |
| that `1788184145-…` is kept rather than retired | `spec.md` G3 — one permanent ledger row anchors into its round record |
| which checks carry a population floor, and what each answer is | `spec.md` §*The population floors*, F1–F16, enumerated with `grep -rn "seal/specs" tests/` |
| that #368 is not repaired here and cannot bite this branch | `spec.md` O1 and `plan.md` phase 11 step 2 |
| that #101 takes only the measurement | `spec.md` O2 |
| that `seal/ledger.md` is byte-identical at the end | `spec.md` G3, A7 |
| that the issue's *fifteen carry no ledger row, one is tests only* is one off — it is fourteen and two | counted from `./bin/settle`'s own list |

## The rows that remain

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | Five new top-level `docs/` files — `the-evidence-ledger`, `the-gates-a-session-meets`, `the-broad-gate`, `measuring-a-run`, `the-agent-set` — become ratified norms. Is that the shape the repository wants, or should some of them merge into `docs/one-root-by-lifetime.md`? | **a person** — `docs/` holds norms a human ratifies, and `skills/implement/SKILL.md` says a work item does not create one on its own authority. The tree cannot answer what the owner wants their policy set to look like | five files, each for an area with no document · or fewer files with longer documents, at the cost of one file covering three areas | build the five as planned; each is a separate phase, so merging two afterwards is one edit and a marker move | ⬜ **shipped on the default, as FOUR** — phase 8 did not write `the-gates-a-session-meets.md`: `plan.md` forbids a new document for an area one already covers, and `docs/review-chain-spec.md` has a section per gate. Still the owner's at the merge |
| Q2 | Does `chain_check.py --baseline origin/main` stay green when 200+ committed round records leave the tree in one commit? Only `unverified_check` grew a folded-vs-deleted arm when `settle` shipped | **the work** — no tree has ever removed this many records, so the answer does not exist until phase 11 has removed them | green → nothing to do · red → the phase records the verdict and the repair is decided there, as a finding rather than as a silent edit | run it in phase 11 step 3 and record the exit code whatever it is | ✅ **answered: red.** Exit 1, 88 refusals, on `origin/main` and on the release base alike — `changed_routing` excludes a rename and not a retirement. Repaired at `4b81a25e` by reading the marker, the same signal `unverified_check.folded_items` reads; a deletion with no marker is still refused. `phases/phase-11.md` |
| Q3 | Does `assert teeth` (F6) still hold over the 7 surviving round records — is there still a record whose finding-id cell the rule refuses? | **a measurement** — one run of the case over the folded tree settles it, and asking a person is the wrong instrument | teeth survive → decline the floor · no teeth → re-point at a record built in `tmp_path`, which is F3's repair one case over | assume it does not survive and plan the fixture; phase 2 measures before writing it | ✅ **answered: the teeth survive.** Four of the seven remaining records carry cells `FINDING_ID_RE` refuses, so F6 is **declined** and no fixture was written. `phases/phase-1.md` |
| Q4 | `seal/ledger.md` line 78 anchors a work item directory, and its own grounds anticipate `settle` dropping the row. The frame keeps the directory instead | **a person** — the row is evidence for a rule that still stands, and whether the repository would rather lose the row than keep eight files is an owner's call, not a reading of policy | keep the directory (the frame's choice) · or remove the row, fold its claim into `docs/review-chain-spec.md` prose, and retire the directory | keep it. Nothing else in the branch depends on the choice, so overturning it later is one `settle --retire` away | ⬜ **kept, and the premise was wrong.** That row survived; FIVE others anchored at a retired `spec.md` broke, which G3 did not enumerate. Three removed, two lost a dead anchor. The multi-anchor rule is a second open row for the owner — `overview.md` §Not verified |
