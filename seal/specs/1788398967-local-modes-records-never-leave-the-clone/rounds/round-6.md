# 1788398967-local-modes-records-never-leave-the-clone — review round 6

<!-- The verifying round for round 5's fixes (target: the diff 3f2a7b1..7cc4fb3).
It exists because the chain checker refuses a `Pass` beside `Fixes checked by:
nobody`, and it names the way out itself: a round that opens nothing needing a
fix does not consume the cap. This one opened nothing needing a fix. Written by
the review orchestrator, which did not implement this work item. -->

| Field | Value |
|---|---|
| Target SHA | 7cc4fb3 (the fix diff from 3f2a7b1); dc79a57 and a1e7bf3 change only `rounds/*.md` cells |
| PR | none yet |
| Broad gate | at the tree this record is committed in — see the table below |
| Fixes checked by | round-7 |
| Contract changes | none |
| New units | none — one test case and two assertions |
| Needs a fix | no |

- [x] Pass

Round 5's seven were each re-derived rather than taken, and all seven hold.
The round opened two 🟡, both gradeable by the implementer on grounds, and
both were closed because each was smaller than the argument for deferring it.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| r5 🟡 1 | the manifest read for presence and not for type | `skills/implement/scripts/seal.py#normalise_remote`, `#import_` | answered — reproduced across twelve field shapes | reviewer executed `head` missing `exported_at`, and `head` as int, bool, None and list; `exported_at` as int and None; `remote` as int, list, dict, None and empty. **Twelve exit 0, zero tracebacks**, and all twelve reached the command's two closing lines with the records written. A correct manifest still prints the real timestamp and SHA |
| r5 🟡 2 | `manifest.json/` outside the size bound | `skills/implement/scripts/seal.py#unsafe`, `#import_` | answered — reproduced at three points | reviewer executed both spellings at the bound minus one, plus one, and 400 MB: six results, all as specified. The case's central-directory patch was checked to hit the entry exactly once, so it is not passing vacuously |
| r5 🟡 3 | the order comment | `skills/implement/scripts/seal.py:819-825` | answered — reproduced | reviewer read the comment against `:828`–`:903` |
| r5 🟡 4 | the READMEs said the import writes nothing | `README.md:474-479`, `README.ko.md:470-474` | answered — reproduced, and the two say the same thing | reviewer read both |
| r5 🟡 5 | the format refusal undocumented | `README.md:467`, `README.ko.md:464`, `spec.md:188` | answered — reproduced, and executed | reviewer ran a format-2 zip: the format message arrives before any name check |
| r5 🟡 6 | the ledger row wrong twice | `seal/ledger/…md:63` | answered — reproduced | reviewer read the row against the code |
| r5 🟡 7 | "Both limits" where there are three | `skills/implement/scripts/seal.py:109`, `overview.md:47` | answered — reproduced | reviewer read both |
| 🟡 1 | `7cc4fb3` created a line a person reads — `an unrecorded time` — and nothing pinned it. The reviewer deleted the whole closing block, then wrote a different phrase into it, and the suite stayed green both times. The three conditions pin that nothing raises, which was the finding's body; what the command says instead was chosen by that commit and kept by nobody | `skills/implement/scripts/seal.py:1005-1009` | fixed at the commit carrying this record — one assertion on the guarded line, and a case for the ordinary one | orchestrator reproduced both mutations: deleting the block reddens eight cases now, and changing the phrase reddens the one that names it. This is round 5's own §89 class — a fix that adds something a person sees — with the case missing as well as the document |
| 🟡 2 | round 5's `Contract changes` named `normalise_remote → import_`, and it is called from four places in the test file too. Round 2's cell had the same gap for `write_members`, while round 3's cell named the test file for that same function — the rule was applied two ways across the four cells rewritten at a1e7bf3 | `rounds/round-5.md:16`, `rounds/round-2.md:15` | fixed at the commit carrying this record | reviewer built an AST call graph and checked every call site all five cells name: **every one is real**. The gap is omission, not a wrong reach, and `chain_check.py` reads the shape rather than the completeness — so no gate would have caught it |

## What the reviewer checked and found clean

| What | Result |
|---|---|
| every caller of `normalise_remote` | two in `import_`, four in the test file; a genuinely different repository is still refused, `--allow-other-repo` still works, and two spellings of one repository still compare equal |
| `an unrecorded time` reachability | only when `head` is text and `exported_at` is not. With no `head` the line does not print at all, and the command still exits 0 |
| the four cases planted at 7cc4fb3, one mutation each | each reddens its own case: two for `normalise_remote`, two for the `head` guard, one for `exported_at`, one for `rstrip("/")` |
| every call site named in all five `Contract changes` cells | all real, checked against an AST call graph |

## Executed probes

| What was run | Result |
|---|---|
| reviewer: twelve manifest field shapes, a correct manifest, and a manifest with no `head` | 29 assertions, 0 failures |
| reviewer: both manifest spellings at the bound −1, +1 and 400 MB | six results as specified |
| reviewer: another repository, `--allow-other-repo`, two spellings of one repository, a format-2 zip | four as specified |
| reviewer: four mutations, one per condition 7cc4fb3 changed | each reddens its own case |
| reviewer: three mutations of the closing line against the whole test file | all three green — 🟡 1 |
| reviewer: an AST call graph against five records' `Contract changes` | every named site real; two omissions — 🟡 2 |
| reviewer: `chain_check.py --baseline origin/release/v0.5.0` at a1e7bf3 | exit 1 on round 5's unchecked `Pass` and its `Fixes checked by: round-6`, which this record is |
| orchestrator: the closing block deleted, then given a different phrase | eight cases red, then one — both green before this round's two assertions |
| orchestrator: the touched test file | 77 passed |

## Broad gate

Run at the tree this record is committed in. The code is identical to
`7cc4fb3`'s; what changed since is one test case, two assertions, and records.

| Check | Result |
|---|---|
| `pytest tests/ -q -n auto` | filled in at the gate's commit |
| `ruff check .` · `ruff format --check .` | filled in at the gate's commit |
| `evidence_check.py --strict .` | filled in at the gate's commit |
| `unverified_check.py --baseline` | filled in at the gate's commit |
| `chain_check.py --baseline` | filled in at the gate's commit |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| rounds 1–5 | `#place`, `#write_members`, `#import_`, `#write_zip`, `#unused`, `#blocked_path`, `#unsafe`, `#normalise_remote` | eight units, every one changed in at least two rounds |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| A clash on both sides takes two runs | round 5's record | the repository owner |
| The read-only-directory case skips as root | round 5's record | the repository owner |
| A root that is itself a symbolic link | `overview.md` §Not verified | the repository owner |
| Whether 32 MB, 512 MB and 20,000 are the right numbers | `overview.md` §Not verified | the repository owner, at the first root that meets one |
| The export accumulating unfolded work items | issue #101, after 0.5.0 | the repository owner |
| `evidence_check.py` drops a row with a non-hex hash silently | issue #97 | the repository owner |
| The reminder reading `1 work items changed` at N=1 | `questions.md` Q1, and the pull request body | the repository owner |
| A fix that adds a visible outcome should document AND pin it in the same commit | issue #89, on 0.6.0 | the repository owner |
