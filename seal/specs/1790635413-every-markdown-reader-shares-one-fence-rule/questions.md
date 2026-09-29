# every markdown reader shares one fence rule (#584) — questions for the planner

<!-- seal/specs/1790635413-every-markdown-reader-shares-one-fence-rule/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

**No row here needs a person.** The routing batch sent this item with no
question, and judging from the tree left none. Every row below is a
measurement or the work's.

## Decided from the tree, so nobody reopens them

| # | What the ticket left open | The answer | Grounds |
|---|---|---|---|
| D1 | Which of the shared functions each reader adopts | Markers read through `live_lines`. Ledger rows read through `closed_fence_lines`. The heading walks and the meter use `fence_opener` / `fence_closes` directly or `fence_spans`. Riders use fence spans in `.md` files only | `docs/the-evidence-ledger.md` §*A marker counts only on a live line* for the markers. §*A retirement would break every ledger row…* for the rows. `rider_check.py`'s own direction for riders. `spec.md` §*The class* |
| D2 | How the hook reaches a function under `skills/` | It does not. `hooks/config.py` keeps its copy, gains the comment half, and the parity test holds that half to `comment_scan` over `blank_fences` | `fence_opener`'s docstring records the hook-path cost. D (#28) is changing what a hook's load failure does, in parallel. `plan.md` §*Alternatives considered* |
| D3 | Whether the config comment half is in | In, with closed comments only | The milestone assigns `hooks/config.py` to this item. `hooks/config.py`'s docstring: "Everything here fails toward nothing is declared". An unclosed comment hiding nothing means no file that reads today stops reading |
| D4 | Whether `evidence_check.py` is touched | No. Its stale "yet" is handed to C | The spawn prompt, and A editing the file in parallel. C edits it next in this release |
| D5 | Whether `close_issues_on_release.py` joins | No | `docs/issues-and-milestones.md` chose the wider fence for it on purpose |
| D6 | Whether `fold_ledger.py`'s other walks join beyond the three the issue names | The heading walks do. `--split`'s walks do not | `demote` copies a fenced `#` line verbatim into the file those walks read. `--split` is a migration this repository has taken |
| D7 | Readers with no fence or comment rule at all (`hooks/routing.py#table_rows` and others) | Out, as a different class | No in-scope reader reads their files. `routing.py` sits on the commit gate's path, which D is changing |

## Rows

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | Does any shape this plugin produces or documents for `config.md` put a table row inside an HTML comment that closes, or a `<!--` inside a code span with a later `-->`? A yes means phase 6 changes a real file's reading. | a measurement: `seal.py`'s writer output, `templates/config.md`, `skills/config/SKILL.md`'s paste instructions, and this repository's `seal/config.md`, read through the new generator. Why the tree could not answer it: the writer's output is built at run time, and the frame reads text | (a) none: phase 6 ships as planned. (b) one: the phase names it in its record, and the changelog entry says which file changes reading | (a). The frame read `templates/config.md` and found `<!--` only on line 97, inside a code span that closes on the same line with `-->` beside it | ✅ measured 2026-09-29 at `e4bfd241`: (a). Old and new `config_rows` and `refusal` answer the same for all five shapes — `seal.py`'s `NEW_CONFIG` for a `Mode` and for a `Broad gate` row, `templates/config.md`, `skills/config/SKILL.md` and this repository's `seal/config.md`. The one closed comment among them is `NEW_CONFIG`'s header, which this repository's file carries too; it hides two prose lines above the table and no row (`phases/phase-6.md`) |
| Q2 | What does the shared rule change in `payload_meter.py`'s section report and in `test_a_section_marked_for_one_role_reaches_only_that_role.py`'s verdict over the shipped tree today? Line 443 of `skills/evidence-check/SKILL.md` opens a fence under the old rule only. `skills/evidence-ci/SKILL.md:55` and `skills/implement/orchestration.md:102` indent a fence five spaces under a list item, which the shared rule does not read as a fence | a measurement: both readers, old rule and new, over every file the test reads. Why the tree could not answer it: it is a diff of two walks over the corpus, and the frame runs nothing | (a) headings appear and the role test stays green: ship. (b) a marked section appears that reaches the wrong role: that is a finding the test was built for, fixed in the skill in the same phase | (a) | ✅ measured 2026-09-29 at `eeb4623e`, before the fix: (a). Over the 482 tracked `.md` files, the old walk and the shared rule differ in one file's heading set, `skills/evidence-check/SKILL.md`, whose line 443 hid `## Known limits`, `## Migrating a pre-anchor ledger` and `## CI` under the old rule. None carries the `Orchestrator:` marker, so the role check stays green. The two five-space fences change no heading (`phases/phase-5.md`) |
| Q3 | Where does the comment question live beside `broad_gate.py#fenced_row_at`, and what does its sentence say? | the work: phase 6. Why the tree could not answer it: the sentence is new, and its wording is decided where it is pinned | Any shape that keeps `fenced_row_at` a question about fences alone and names the comment. The sentence says the row is commented out and runs nothing | a sibling function beside `fenced_row_at` | ✅ decided 2026-09-29 at `e4bfd241`: `broad_gate.py#commented_row_at`, a sibling reading `hooks/config.py#commented`, and an arm of `missing_row` after the fence arm and before the absent-row one. It says the line is *written inside an HTML comment*, that it is commented out and not absent, to take it out of the comment or write the answer in the live table, and *Nothing ran.* Pinned by `test_a_broad_gate_line_only_inside_a_comment_is_named_and_not_called_absent` (`phases/phase-6.md`). NAME NOT IN TREE: the function, the arm and the case were reverted with phase 6's comment half after round 3, and the question goes with them to the new work item |
| Q4 | Do `fold_ledger.py`'s heading walks and `demote` share one helper over `fence_spans`, or does each call it? | the work: phase 1. Why the tree could not answer it: it is a factoring choice that changes no verdict | Either. One helper keeps them from drifting apart. Separate calls keep each unit's diff local | one helper | ✅ decided 2026-09-29 at `c3afabf8`: one helper, `fold_ledger.py#fenced_lines`, which `demote`, `version_headings`, `section_heading` and `insert` all ask (`phases/phase-1.md`) |
| Q5 | Round 1's 🟡 1 and 🟡 2: `gather_changelog.py` and `fold_ledger.py` write a fragment verbatim, so a fragment that leaves a fence or a comment open puts every marker written below it on a line their own `live_markers` cannot see — `--check` then asks for a second gather that writes the entry twice, or passes the fold with a wrong count. The only fix that closes it is a new refusal of such a fragment before anything is written, which is mechanism, and a fix pass may not add mechanism (`skills/code-review/orchestration.md` §*A fix pass adds the unit that pins it*). Does it land as a phase of this branch, as #658 did at the owner's request, or as an issue? | a person — the owner, who asked for #658 to be finished in this branch | (a) a phase of this plan: `leaves_open` in each script over `live_lines`, a refusal beside the #586 one in each `main`, one case each, and a sentence in `docs/branch-and-release.md`; round 1's report holds paste-ready drafts, executed in the reviewer's clone. (b) an issue in the 0.16.0 milestone: the defect ships in the release until it lands, and it is this branch's own | (a), on the #658 precedent. Nothing in today's tree has the shape: the gather and the fold both read their current corpus the same before and after (140/140, 125/125) | ✅ (a), answered 2026-09-29 by the orchestrating session from the owner's standing answer in this run: a defect found in a branch is fixed in that branch, not filed. Built as phase 9 |

**`Who can answer` takes one of three values and nothing else.** They were one
shape on the page before this, and #84's second comment measured all three
inside a single run's four rows.

- **a person** — what the product should be, or a value somebody has to be
  accountable for. This is the file's stated purpose, and the only kind of row
  that blocks the build.
- **a measurement** — a probe, a command or a count settles it, so asking a
  person is the wrong instrument and queueing it behind one wastes a round
  trip. Measured: six probes at about three seconds each answered a row that
  had been written into the human batch, and they showed the ticket's own
  instruction was wrong.
- **the work** — unknowable at framing time. The phase that meets it decides
  it there and records a divergence row; it does not travel back to the
  framer, which would spend the interruption the framing phase exists to spend
  once.

**The framer opens rows and does not own their answers.** A row is a question
put to somebody else, so opening one costs little and closes nothing — and the
`Status` column is ticked by whoever answered, never by whoever asked. Sorting
the rows this way is also what keeps the batch short enough to answer in one
sitting: two of the three kinds never needed a person at all.

Answered rows feed back into docs/ (policy clause or open-questions section)
before this directory's work merges.
