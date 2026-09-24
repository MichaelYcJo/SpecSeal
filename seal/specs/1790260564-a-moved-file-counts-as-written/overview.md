# 1790260564-a-moved-file-counts-as-written — overview

📋 implement applied
· spec:     `docs/review-chain-spec.md` §*The survivor sweep* and §*What the sweep reads, and what it counts as written*; `skills/agent-contract/SKILL.md` §12–§16; `CONTRIBUTING.md` §*What a change to a gate must carry*; this work item's `spec.md`, `plan.md`, `questions.md`; #563 (body and comment), #564
· evidence: `seal/ledger/1790260564-a-moved-file-counts-as-written.md` rows G7, G8, G10, M1, M6, O1, O4; rows re-read, or corrected in place, in `seal/releases/` 0.6.0, 0.8.1, 0.9.3, 0.9.5, 0.11.2, 0.12.0, 0.13.1, 0.14.0, 0.15.0, 0.15.1
· verified: executed — each new case seen red (at the base, at the previous phase's tip, or under a mutation), the survivor module whole, the modules that read an edited document, `evidence_check.py --strict .`; read — the three-OS behaviour of the CRLF, symlink and path cases

## Why this work exists

The survivor sweep wrote a moved file's text as the range's own and misread a gathered changelog fragment three ways, so a real survivor went unreported, and in local mode it refused every work item its own range row; after this, moved and gathered text are held, and a local range row holds on its own branch.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| S18's old assertion under phase 2 | `spec.md` M3: *the old assertion (`[1-9]` sentences) goes red under phase 2, and that red is the reason for the rewrite*. Executed on the old fixture after phase 2: `against 1 sentence(s)`, green — `moved_section` writes `# a` and then `# b`, a real removal | S18 rewritten on its own fixture with identical bytes, so it pins 0; `moved_section` untouched for S17 | the spec's intent (pin silence at 0) holds; its proof did not, and S17 had to stay unedited |
| The `not yours` line | `spec.md` §*Data & interfaces*: *No CLI flag, exit code or report line changes shape* | The shape stays; the reason clause is now the test that refused the row — in local mode the sentence `on_its_branch` returns for each of its five refusals (round 1's 🟡 2; at the build one sentence stood for all of them), in shared mode *this range touches nothing in it* (unchanged) | in local mode the old reason is true of every range and sends the reader to a diff that can never hold the file (`agent-contract` §14; pinned in O2, O4, O6 and the depth case) |
| The path-list case | `plan.md` names one more `ls-tree` and not the case that counts path lists | `test_every_path_list_this_module_derives_from_git_is_filtered_or_named` reclassified: `tracked` maps each caller to its filter; ledger row S2 (0.11.2) corrected | the case exists to go red on a new caller until it is classified; it did |
| Cases the spec did not list | `spec.md` scenarios end at M5, O3 | M6, M7 (the pairing's two counts), O1 through a symlink, O4 (missing / branchless `routing.md`), O5 (missing reader) | each is a mutation of a new unit that survived with the listed cases only |
| Sentences corrected beyond the two docs sentences | `spec.md` §*Docs sentences this work changes* names two | also `agents/smith.md` §Phases and `skills/code-review/orchestration.md` (*it never reaches a range that touches nothing in your own work item*), and the module docstring's second-anchor paragraph | the same sentence became false in local mode at each carrier (§12); the smith.md rider was re-measured (1, 1, True) and re-stamped |
| One record line | `spec.md` judgment 3 names S18 by its old name | the line carries `NAME NOT IN TREE` | `evidence_check.py --strict` refused it; the line means the old name |
| Note dates | the spawn: *corrected in place with a `Corrected 2026-09-24` note* | phases 1–2 notes read 2026-09-24; phase 3's read 2026-09-25 | the date turned during the run, and a note's date is the day it was read |

## Not verified

| Item | Who must answer |
|---|---|
| G10 on a runner whose git converts line endings, O1's symlink arm and the `normcase` comparison on Windows — only macOS was run | the three-OS matrix in `test.yml` at the pull request |
| The full suite | the sealer, once, after the review rounds settle |
| A local-mode repository end to end: `broad_gate.py#exemptions` handing a local `survivors.md` to the sweep at a seal | the sealer's run on a local-mode repository; the cases drive `survivor_check.py` directly |

## Not done

`questions.md` Q1 is built on its default: `.github/scripts/gather_changelog.py` and `publish_release_note.py` still end a section at any `## `, so a fragment carrying one breaks the second gather and the release note; filed as #586 for the owner. Narrowing `a_gathered_fragment` to an anchored path and a lone `\r` line ending stay out, per `spec.md` §*Out*. A local-mode declaration on a reused branch name reaches that branch's ranges, which `plan.md`'s failure scenario states and nothing measures. A parent branch's run from a detached HEAD, with no local head naming the parent, is still excused by a stacked child's row (round 2's ⬜ 4, executed by the reviewer): it is the same range as the child's own older-tip run, and it is the documented *no local branch* bound of `on_its_branch`.

## Fed back into the spec

Inferred during implementation: the pairing across paths is one for one in both directions (a copy removed beyond the ones that arrived is still removed; a copy written beyond them is written). A refused declaration's line names the test that refused it.
