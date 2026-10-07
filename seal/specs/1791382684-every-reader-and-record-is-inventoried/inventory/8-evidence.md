# #834 inventory, part 8: EVIDENCE — issues since 0.18.0 by reader or record mechanism

Window: every issue created at or after 2026-10-03T16:59Z (v0.18.0 tag, 01:59 +0900), all states: **63 issues** (#754–#865).
PRs: every PR merged at or after that instant (47; the 0.18.0 release PR #753 merged at the boundary). Sources: `gh issue list --state all --search "created:>=2026-10-03"` (16 issues created before 16:59Z dropped), `gh pr list --state merged --search "merged:>=2026-10-03"` with `files` and `closingIssuesReferences`. Each issue body was read (English half).

Conventions:
- `Kind` lists the primary kind first; a second kind is added where the issue also carries it (for example a 🟡 reader defect plus ⬜ records that no longer match). Counts of reader-guess / record-drift below count an issue when either kind names it.
- `Fixed by PR` is the feature PR into a release branch. `(post-review)` means the fix landed on the same PR after its capped review run. Release PRs into `main` (#778, #799, #820, #840, #863) carry the closing keywords but fix nothing themselves.
- `Reopened-shape?` is `yes` when the issue is a new shape of a defect another issue (or its PR) had just fixed, named. Two point at pre-window issues (#761 → #747, #762 → #741); they are marked but still counted.
- `seal/specs/…` cells stand for files of different work items. Their PR count is 0 because no one path repeats.
- Units marked "removed since" are not in the tree at 5623d728 (`git grep`): `switch_kind`, `is_ref`, `_fetched_as`, `_refs` (by #850), `heredoc_data`, `_quoted_delimiter`, `_runs_what_it_reaches` (by #769), `cited_first`, `left_because` (by #829), `OWN_LISTING`, `proof_refused` (by #846). Still present: `FAILED_RE` (`broad_gate.py:340`, now `(.+?)::`), `generic_units` (`evidence_check.py:707`), `touched` (`round_record.py:3305`), `walk_tip` (`chain_check.py:4482`), `read_table` (`hooks/config.py:1326`), `pact_declaration` (`hooks/config.py:819`), `has_token` (`worktree-guard.py:381`), `has_marker` (`commit-review-gate.py:657`), `_rebase_names_a_branch` (`worktree-guard.py:2226`), `check_scale`/`SCALE_LADDER` (`seal_stamp.py`), `without_the_policy_span` (`tests/test_one_word_one_meaning.py:725`).

## Issues

| Issue | State | Filed from | File(s) | Unit(s) | Kind | Family | Fixed by PR | Reopened-shape? |
|---|---|---|---|---|---|---|---|---|
| #754 | closed | measurement | — | — | process | flow measurement log | release 0.18.1 (#778) | no |
| #755 | open | frame of #730 (O2) | rule documents (50 files) | verbatim-run ratchet baseline | record-other | rule restatement | — (open) | no |
| #759 | closed | review: fix pass of #756 r1 | `hooks/config.py` | `pact_declaration`, `config_rows` (stops at table end) | reader-other | pact markdown reader | #793 | no |
| #761 | closed | review: #758 r2 (deferred) | `skills/verify/scripts/broad_gate.py` | absence-at-base check under a `cd` row | reader-guess | broad-gate run attribution | #787 | yes: #747 class (pre-window, fixed by #758) |
| #762 | closed | review: #757 r3 (capped) | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py`, `seal/specs/…/spec.md` | `judge`, `OPENERS` row `zipfile.Path.open`, bare-name exclusion | reader-other + record-drift | encoding walker | #782 | yes: fix-of-fix of #741 r2 (pre-window) |
| #763 | closed | review: #760 r3 (capped) | `hooks/tokens.py`, `hooks/cmdline.py`, `docs/commit-review-gate-spec.md` | `heredoc_data`, `_quoted_delimiter`, `_runs_what_it_reaches` (all removed since) | reader-guess + record-drift | heredoc body as data | #769 | no |
| #764 | closed | frame of #750 (§Out) | `hooks/worktree-guard.py`, `hooks/cmdline_base.py` | `switch_kind`, frozen `classify` (`-b`/`-c` glued value) | reader-guess | worktree-guard shell prediction | #788 | no |
| #772 | closed | build of #746 / #771 r1 deferral | `skills/evidence-check/scripts/evidence_check.py` | unfrozen in-place `--reverify` re-stamp order | record-other | reverify judgment and order | #786 | no |
| #773 | closed | review: #769 r1 | `hooks/commit-review-gate.py`, `hooks/cmdline.py` | `has_marker` via `split_segments` (heredoc body read as command) | reader-guess + record-drift | heredoc body as data | #783 | yes: #763 (heredoc body vs command text, waiver reader) |
| #774 | closed | review: #771 r2 | `skills/evidence-check/scripts/evidence_check.py` | `record_pact_changes` (h1→h1 move) | record-other | reverify judgment and order | #786 | no (from #756 write path) |
| #775 | closed | review: #771 r3 (whites) | `templates/config.md`, `skills/evidence-check/scripts/evidence_check.py`, `docs/the-pact.md`, `skills/evidence-check/SKILL.md`, `seal/releases/0.18.0.md` | pact-change trigger sentences, 1-of-3 pins, `Enforced by:` line, `Re-read ·` row of 0.18.0:79 | record-drift | records sentence vs code | #786 | no |
| #779 | closed | measurement | — | — | process | flow measurement log | release 0.18.2 (#799) | no |
| #780 | closed | frame of #773 (Q1) | `hooks/worktree-guard.py`, `hooks/tokens.py` | `has_token` (consent token in heredoc body) | reader-guess | heredoc body as data | #803 | yes: #773 (same reading copied in the guard) |
| #781 | closed | frame of #774/#772/#775 | `docs/the-evidence-ledger.md`, `skills/evidence-check/scripts/evidence_check.py` | "dated note" sentence vs in-place writer | record-drift | records sentence vs code | #801 | no |
| #785 | closed | 0.18.1 release run + build probe of #786 | `skills/evidence-check/scripts/evidence_check.py` | in-place `--reverify` ignores families (outranked row re-stamped) | record-other | reverify judgment and order | #801 | no |
| #789 | closed | review: #787 r1 (🟡2, stated as limit) | `skills/verify/scripts/broad_gate.py`, `templates/config.md` | which runner prints the pytest summary first | reader-guess | broad-gate run attribution | #814 | yes: #761 (two directories instead of one cd) |
| #790 | closed | review: #788 r2 (deferred) | `hooks/worktree-guard.py`, `tests/test_guard_resolves_the_tree_it_judges.py` | `classify`/`is_ref` appends `^{commit}` to `:/msg` | reader-guess + record-drift | worktree-guard shell prediction | #803 | yes: #764 (another switch spelling missed) |
| #791 | closed | review: #786 r3 (capped) | `skills/evidence-check/scripts/evidence_check.py`, `docs/the-pact.md` | MOVES across repeated AGAIN walks | record-other + record-drift | reverify judgment and order | #786 (post-review) | yes: #772 (fix-of-fix: #786 r1 walk) |
| #792 | closed | post-review check of #786 | `skills/evidence-check/scripts/evidence_check.py` | `LEFT … run it without --ledger` remedy line | record-other | reverify judgment and order | #801 | no (released #743) |
| #794 | closed | review: #793 r4 (whites) | `tests/test_a_signatory_declares_its_pact.py`, `templates/config.md` | `DELIMITERS` build, `STRAY_WAYS` floor, template sentence | other + record-drift | pact markdown reader | #793 (post-review) | yes: #759 redesign residue |
| #797 | closed | 0.18.2 release prep (#795 by hand) | `seal/specs/*/changelog.md`, `skills/code-review/scripts/chain_check.py`, `agents/smith.md`, `skills/implement/SKILL.md` | changelog fragment vs fix range | record-drift | changelog fragment lag | #802 | no |
| #800 | closed | measurement | — | — | process | flow measurement log | release 0.18.3 (#820) | no |
| #805 | open | review: #802 r2 (⬜1) | `skills/code-review/scripts/chain_check.py` | `walk_tip` first-parent walk below a base-side merge | reader-other | fix-range walk over merges | — (open) | yes: #797 (its new notice) |
| #806 | closed | review: #801 r2 (⬜3) | `skills/evidence-check/scripts/evidence_check.py` | `cited_first` reads citations only | record-other | reverify judgment and order | #829 | yes: #772 (non-citation coordinate) |
| #807 | closed | review: #804 r1 (unmerged; stated as limit) | `skills/verify/scripts/broad_gate.py`, `templates/config.md` | runner count via collection pass; `-p no:junitxml` | reader-guess | broad-gate run attribution | #846 | yes: #761 (p1b shape) |
| #808 | closed | review: #801 r3 (capped) | `skills/evidence-check/scripts/evidence_check.py`, `seal/specs/…/overview.md`, `seal/releases/0.4.0.md` | `unplaced` loop vs `content_matches`; claim-tie rule at two sites | record-other + record-drift | reverify judgment and order | #801 (post-review) | yes: #785 (its new `unplaced` loop regressed) |
| #809 | closed | review: #801 r3 (⬜3, design) | `skills/evidence-check/scripts/evidence_check.py` | `classify` vs `reverify` on unsure place with claim | record-other | reverify judgment and order | #829 | yes: #808 (copies of one judgment) |
| #810 | closed | post-review check of #808 | `skills/evidence-check/scripts/evidence_check.py` | `left_because`, `classify` reason text on claim tie | record-other | reverify judgment and order | #801 | yes: #808 (fix-of-fix) |
| #811 | closed | review: #803 r3 (capped) | `hooks/worktree-guard.py`, `seal/specs/…/phases/phase-4.md` | `_fetched_as` `.strip()`, `_refs` `splitlines()` (removed since) | reader-guess + record-drift | worktree-guard shell prediction | #803 (post-review) | yes: #790 (its remote-tracking guess) |
| #812 | closed | review: #804 r3 (capped) | `skills/verify/scripts/broad_gate.py`, `templates/config.md`, `seal/specs/…/overview.md` | junitxml placement by dotted name; `git ls-files` tree | reader-guess + record-drift | broad-gate run attribution | #814 (post-review) | yes: #789 (P1, Q1 reopen) |
| #813 | closed | review: #804 r3 (outside) | `skills/verify/scripts/broad_gate.py` | `FAILED_RE` `\S+?` path group | reader-guess | broad-gate run attribution | #846 | no |
| #815 | closed | review: #814 r3 (capped) | `skills/verify/scripts/broad_gate.py`, `templates/config.md`, `seal/specs/…/overview.md` | collect-only proof accepts empty session | reader-guess + record-drift | broad-gate run attribution | #814 (post-review) | yes: #789/#812 (fix-of-fix of #814 r2) |
| #816 | closed | post-review check of #815 | `skills/verify/scripts/broad_gate.py`, `templates/config.md` | proof marks (`-o verbosity_test_cases=-1`) another runner can print | reader-guess | broad-gate run attribution | #846 | yes: #815 (fix-of-fix) |
| #818 | closed | Windows CI of #814 | `skills/verify/scripts/broad_gate.py` | failing-file listing separator | platform | platform path spelling | #846 | no |
| #821 | closed | measurement | — | — | process | flow measurement log | release 0.19.0 (#840) | no |
| #822 | closed | owner | `docs/the-pact.md`, `hooks/config.py`, `skills/evidence-check/scripts/pact_check.py`, `skills/code-review/scripts/chain_check.py`, `tests/test_one_word_one_meaning.py` | `Signatory`→`Signer`; compat header reader | other | pact vocabulary | #827 | no |
| #823 | closed | owner (review of capped chains) | `skills/code-review/scripts/chain_check.py`, `skills/code-review/scripts/round_record.py` | fix-of-fix count; finding `Location` → `.py` path | process | fix-of-fix rule | #828 | no |
| #824 | closed | owner (review of capped chains) | `skills/evidence-check/scripts/evidence_check.py` | four copies of one row judgment; write order | record-other | reverify judgment and order | #829 | no (umbrella of #772…#810) |
| #825 | closed | owner (review of capped chains) | `skills/verify/scripts/broad_gate.py`, `templates/config.md` | which pytest run printed a line | reader-guess | broad-gate run attribution | #846 | no (umbrella of #758, #787, #804, #814) |
| #826 | closed | owner (review of capped chains) | `hooks/worktree-guard.py`, `hooks/cmdline_base.py` | switch predicted from command text | reader-guess | worktree-guard shell prediction | #850 | no (umbrella of #733, #745, #788, #803) |
| #830 | closed | review: #827 r3 (capped) | `hooks/config.py`, `tests/test_one_word_one_meaning.py`, `seal/ledger/1791239490-….md` | `read_table` glued old header; `PACT_HEADER_WORD`; `without_the_policy_span`; R6 | reader-other + record-drift | pact markdown reader | #827 (post-review) | yes: #822 (its compat reader) |
| #831 | closed | post-review check 2 of #830 | `tests/test_one_word_one_meaning.py`, `tests/test_a_signer_declares_its_pact.py`, `hooks/config.py`, `seal/ledger/1791239490-….md` | `without_the_policy_span` end condition; glued-header quote; R1, R6 | reader-other + record-drift | pact markdown reader | #843 | yes: #830 (fix-of-fix) |
| #832 | closed | owner | `.github/scripts/release_seal.py`, `skills/verify/scripts/seal_stamp.py` | release image renderer | other | seal stamp | #859 | no |
| #833 | closed | review: #829 r3 (⬜1) | `seal/ledger/1791240748-….md` | ledger row E3 claim | record-drift | ledger row claim | #829 (post-review) | no |
| #834 | open | owner | — | — | process | #834 inventory theme | — (open) | no |
| #835 | closed (not planned) | owner | — | — | process | #834 inventory theme | not planned | no |
| #836 | closed (not planned) | owner | — | — | process | #834 inventory theme | not planned | no |
| #837 | closed (not planned) | owner | — | — | process | #834 inventory theme | not planned | no |
| #841 | closed | owner (CI wait) | `.github/workflows/test.yml`, `.github/scripts/run_tests.py` | Windows leg wall time | platform | CI test cost | #845 | no |
| #842 | closed | measurement | — | — | process | flow measurement log | release 0.20.0 (#863) | no |
| #844 | open | review: #843 r3 (capped) | `tests/test_one_word_one_meaning.py` | `without_the_policy_span` docstring wrap | record-other | pact markdown reader | — (open) | yes: #831 (its r2 fix) |
| #847 | closed | review: #845 r3 (capped) | `CONTRIBUTING.md` | `.test_durations` refresh recipe condition | record-drift | records sentence vs code | #845 (post-review) | yes: #841 (its r2 removed the only copy) |
| #848 | open | use (consuming repository, 0.18.3) | `skills/evidence-check/scripts/evidence_check.py` | `generic_units` indentation rule (multi-line TS signature) | reader-guess | evidence unit extent | — (open) | no |
| #849 | closed | review: #846 r6 (capped) | `skills/verify/scripts/broad_gate.py`, `skills/verify/scripts/pytest_record/specseal_pytest_record.py`, `seal/specs/…/spec.md` | `read_record`/`base_word` session with no `end` line; `Recorder` keyed on `id()` | reader-other + record-drift | broad-gate session end | #851 | yes: #825 r4 🟡2 again |
| #852 | open | review: #851 r2 (honest limits) | `skills/verify/scripts/broad_gate.py`, `skills/verify/scripts/pytest_record/specseal_pytest_record.py`, `templates/config.md` | `end` line exit 0/1/5 read as ran-to-end | reader-other | broad-gate session end | — (open) | yes: #849 (its new demotion) |
| #853 | open | reframe of #832 | `skills/verify/scripts/seal_stamp.py`, `skills/verify/scripts/broad_gate.py`, `hooks/sealer-stamp.py` | `check_scale`, `--scale`, values-file `scale`, `SCALE_LADDER` | record-drift | seal stamp | — (open) | yes: #832 (its reframe) |
| #854 | closed | review: #850 r3 (capped, 2nd fix-of-fix) | `hooks/worktree-guard.py`, `docs/worktree-guard-spec.md` | `_rebase_names_a_branch` (`--end-of-options`, long-option prefix) | reader-guess + record-drift | worktree-guard shell prediction | #855 | yes: #826 allow-list / #764 option spellings |
| #856 | open | review: #855 r1 | `hooks/worktree-guard.py` | words as frozen split sees them; brace expansion | reader-guess + record-drift | worktree-guard shell prediction | — (open) | yes: #854 (fix-of-fix) |
| #857 | open | owner | `skills/verify/scripts/seal_stamp.py` | placeholder mark | other | seal stamp | — (open) | no |
| #858 | open | owner (release checklist) | `.github/scripts/plugin_directory_check.py`, `docs/release-checklist.md` | "listed" inferred from two GitHub repos | reader-guess | plugin directory check | — (open) | no |
| #860 | open | review: #859 r2 (⬜4) | `skills/code-review/scripts/round_record.py` | `touched` diffs whole range incl. merge | reader-other | fix-range walk over merges | — (open) | no (same shape as #805, open) |
| #864 | open | owner (CI budget) | `.github/workflows/test.yml` | macOS leg wall time | platform | CI test cost | — (open) | no |
| #865 | open | measurement | — | — | process | flow measurement log | — (open) | no |

Totals over 63 issues. Primary kind: reader-guess 19, record-other 12, process 11, reader-other 8, record-drift 6, other 4, platform 3. With secondary kinds counted: record-drift 21, reader-guess 19.
Filed from: a review round or a post-review check 33, the owner 14, a frame 4, the measurement log 6, other 6 (a build #772, a release run #785, release prep #797, CI #818, use in another repository #848, a reframe #853).

## Counts by family

| Family | Issues | Of which reader-guess | Of which record-drift | Issues reopening a fixed shape | PRs that touched it |
|---|---|---|---|---|---|
| reverify judgment and order | 10 (#772, #774, #785, #791, #792, #806, #808, #809, #810, #824) | 0 | 2 | 5 (#791, #806, #808, #809, #810) | #756, #771, #786, #801, #829 |
| broad-gate run attribution | 8 (#761, #789, #807, #812, #813, #815, #816, #825) | 8 | 2 | 6 (#761, #789, #807, #812, #815, #816) | #758, #787, #814, #846, (#804 unmerged) |
| flow measurement log | 6 (#754, #779, #800, #821, #842, #865) | 0 | 0 | 0 | — |
| worktree-guard shell prediction | 6 (#764, #790, #811, #826, #854, #856) | 6 | 4 | 4 (#790, #811, #854, #856) | #765, #788, #803, #850, #855 |
| pact markdown reader | 5 (#759, #794, #830, #831, #844) | 0 | 3 | 4 (#794, #830, #831, #844) | #793, #827, #843 |
| #834 inventory theme | 4 (#834, #835, #836, #837) | 0 | 0 | 0 | — |
| heredoc body as data | 3 (#763, #773, #780) | 3 | 2 | 2 (#773, #780) | #769, #783, #803 |
| records sentence vs code | 3 (#775, #781, #847) | 0 | 3 | 1 (#847) | #786, #801, #845 |
| seal stamp | 3 (#832, #853, #857) | 0 | 1 | 1 (#853) | #859 |
| CI test cost | 2 (#841, #864) | 0 | 0 | 0 | #845 |
| broad-gate session end | 2 (#849, #852) | 0 | 1 | 2 (#849, #852) | #846, #851 |
| fix-range walk over merges | 2 (#805, #860) | 0 | 0 | 1 (#805) | #802 |
| changelog fragment lag | 1 (#797) | 0 | 1 | 0 | #795, #802 |
| encoding walker | 1 (#762) | 0 | 1 | 1 (#762) | #757, #782 |
| evidence unit extent | 1 (#848) | 1 | 0 | 0 | — |
| fix-of-fix rule | 1 (#823) | 0 | 0 | 0 | #828 |
| ledger row claim | 1 (#833) | 0 | 1 | 0 | #829 |
| pact vocabulary | 1 (#822) | 0 | 0 | 0 | #827 |
| platform path spelling | 1 (#818) | 0 | 0 | 0 | #846 |
| plugin directory check | 1 (#858) | 1 | 0 | 0 | — |
| rule restatement | 1 (#755) | 0 | 0 | 0 | — |

## Counts by file

An issue that names two files counts in both. PRs: feature PRs into a release branch merged in the window whose file list holds the path.

| File | Issues | Of which reader-guess | Of which record-drift | Issues reopening a fixed shape | PRs that touched it (into a release branch, in window) |
|---|---|---|---|---|---|
| `skills/evidence-check/scripts/evidence_check.py` | 13 (#772, #774, #775, #781, #785, #791, #792, #806, #808, #809, #810, #824, #848) | 1 | 4 | 5 | 7 (#756, #771, #786, #793, #801, #827, #829) |
| `skills/verify/scripts/broad_gate.py` | 12 (#761, #789, #807, #812, #813, #815, #816, #818, #825, #849, #852, #853) | 8 | 4 | 9 | 6 (#758, #787, #814, #846, #851, #859) |
| `templates/config.md` | 9 (#775, #789, #794, #807, #812, #815, #816, #825, #852) | 6 | 4 | 7 | 10 (#756, #758, #786, #787, #793, #814, #827, #828, #846, #851) |
| `hooks/worktree-guard.py` | 7 (#764, #780, #790, #811, #826, #854, #856) | 7 | 4 | 5 | 6 (#757, #765, #788, #803, #850, #855) |
| `hooks/config.py` | 4 (#759, #822, #830, #831) | 0 | 2 | 2 | 4 (#756, #793, #827, #843) |
| `skills/code-review/scripts/chain_check.py` | 4 (#797, #805, #822, #823) | 0 | 1 | 1 | 3 (#802, #827, #828) |
| `tests/test_one_word_one_meaning.py` | 4 (#822, #830, #831, #844) | 0 | 2 | 3 | 5 (#756, #770, #827, #838, #843) |
| `docs/the-pact.md` | 3 (#775, #791, #822) | 0 | 2 | 1 | 6 (#756, #771, #786, #793, #827, #829) |
| `seal/specs/…/overview.md` | 3 (#808, #812, #815) | 2 | 3 | 3 | 0 |
| `skills/verify/scripts/seal_stamp.py` | 3 (#832, #853, #857) | 0 | 1 | 1 | 1 (#859) |
| `.github/workflows/test.yml` | 2 (#841, #864) | 0 | 0 | 0 | 3 (#756, #845, #859) |
| `hooks/cmdline.py` | 2 (#763, #773) | 2 | 2 | 1 | 0 |
| `hooks/cmdline_base.py` | 2 (#764, #826) | 2 | 0 | 0 | 0 |
| `hooks/tokens.py` | 2 (#763, #780) | 2 | 1 | 1 | 2 (#783, #803) |
| `seal/ledger/1791239490-….md` | 2 (#830, #831) | 0 | 2 | 2 | 0 |
| `seal/specs/…/spec.md` | 2 (#762, #849) | 0 | 2 | 2 | 0 |
| `skills/code-review/scripts/round_record.py` | 2 (#823, #860) | 0 | 0 | 0 | 1 (#828) |
| `skills/verify/scripts/pytest_record/specseal_pytest_record.py` | 2 (#849, #852) | 0 | 1 | 2 | 2 (#846, #851) |
| `.github/scripts/plugin_directory_check.py` | 1 (#858) | 1 | 0 | 0 | 2 (#757, #767) |
| `.github/scripts/release_seal.py` | 1 (#832) | 0 | 0 | 0 | 2 (#757, #859) |
| `.github/scripts/run_tests.py` | 1 (#841) | 0 | 0 | 0 | 3 (#756, #845, #859) |
| `CONTRIBUTING.md` | 1 (#847) | 0 | 1 | 1 | 6 (#756, #757, #767, #770, #845, #859) |
| `agents/smith.md` | 1 (#797) | 0 | 1 | 0 | 2 (#758, #802) |
| `docs/commit-review-gate-spec.md` | 1 (#763) | 1 | 1 | 0 | 2 (#769, #783) |
| `docs/release-checklist.md` | 1 (#858) | 1 | 0 | 0 | 3 (#768, #770, #859) |
| `docs/the-evidence-ledger.md` | 1 (#781) | 0 | 1 | 0 | 4 (#771, #786, #801, #829) |
| `docs/worktree-guard-spec.md` | 1 (#854) | 1 | 1 | 1 | 5 (#765, #788, #803, #850, #855) |
| `hooks/commit-review-gate.py` | 1 (#773) | 1 | 1 | 1 | 3 (#757, #769, #783) |
| `hooks/sealer-stamp.py` | 1 (#853) | 0 | 1 | 1 | 1 (#859) |
| rule documents (50 files) | 1 (#755) | 0 | 0 | 0 | — |
| `seal/ledger/1791240748-….md` | 1 (#833) | 0 | 1 | 0 | 0 |
| `seal/releases/0.18.0.md` | 1 (#775) | 0 | 1 | 0 | 0 |
| `seal/releases/0.4.0.md` | 1 (#808) | 0 | 1 | 1 | 0 |
| `seal/specs/*/changelog.md` | 1 (#797) | 0 | 1 | 0 | 0 |
| `seal/specs/…/phases/phase-4.md` | 1 (#811) | 1 | 1 | 1 | 0 |
| `skills/evidence-check/SKILL.md` | 1 (#775) | 0 | 1 | 0 | 5 (#756, #771, #793, #801, #827) |
| `skills/evidence-check/scripts/pact_check.py` | 1 (#822) | 0 | 0 | 0 | 2 (#756, #827) |
| `skills/implement/SKILL.md` | 1 (#797) | 0 | 1 | 0 | 5 (#756, #768, #802, #827, #828) |
| `tests/test_a_signatory_declares_its_pact.py` | 1 (#794) | 0 | 1 | 1 | 2 (#756, #793) |
| `tests/test_a_signer_declares_its_pact.py` | 1 (#831) | 0 | 1 | 1 | 2 (#827, #843) |
| `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py` | 1 (#762) | 0 | 1 | 1 | 2 (#757, #782) |
| `tests/test_guard_resolves_the_tree_it_judges.py` | 1 (#790) | 1 | 1 | 1 | 7 (#757, #765, #788, #803, #845, #850, #855) |

## Observations

- Three families hold 24 of the 63 issues and 15 of the 27 reopenings: `reverify judgment and order` 10 (5 reopened), `broad-gate run attribution` 8 (6), `worktree-guard shell prediction` 6 (4). These 24 issues touched 3 files that grew in the window: `evidence_check.py` 4718→6128, `broad_gate.py` 3354→3849, `worktree-guard.py` 2616→3394 lines (v0.18.0→5623d728).
- Broad gate chain: #761 → #787 → #789 (r1) → #814 → #815 (r3) → #814 post-review → #816 (its check) → owner #825 → #846 → #849 (r6) → #851 → #852 (open). Between those, the unmerged #804 produced #807, #812 and #813. In the same chain, `templates/config.md` rule 3 is named in 9 issues (#789, #807, #812, #815, #816, #825, #852 among them), and 10 window PRs touched it.
- After #846 (2026-10-06T23:00) no new `run attribution` issue was filed. The defects moved to the new record, `broad-gate session end`: #849 (r6, "round 4's 🟡 2 again") → #851 → #852 (open). The reader-guess count there went to 0, but each issue still reopens a shape.
- Worktree guard chain: #764 → #788 → #790 (r2) → #803 → #811 (r3, `_refs`/`_fetched_as`) → owner #826 → #850 → #854 (r3, the second fix-of-fix) → #855 → #856 (r1, brace expansion; open). The family did not converge across the redesign: two new spellings were filed after #850's allow-list, both 🟡 on the silent side.
- Reverify chain: #772/#774/#775 → #786 → #791 (r3) → #792 (check) → #801 → #806, #808, #809 (r2–r3) → #810 (check) → owner #824 → #829 → #833 (a ledger row, ⬜). No reverify-judgment issue was filed after #829 (2026-10-06T04:03). The window after it is about 1.5 days.
- Heredoc family converged: #763 → #769 (one exact shape, `hooks/one_heredoc.py`) → #773 (waiver reader, r1) → #783 → #780 (the same reading copied in the guard) → #803. No heredoc issue was filed after 2026-10-04T13:17. Two of its three issues are one reading found in a second and third copy (`has_marker`, `has_token`).
- Pact markdown chain: #759 → #793 → #794 (r4). #822 → #827 → #830 (r3) → #831 (check 2, filed instead of fixed) → #843 → #844 (r3, docstring wrap; open). 4 of 5 issues reopen a shape. The `Pact` row reader (#759) did not recur after #793. The new defects came from the signer compatibility reader and the sweep's paragraph span.
- Record drift mostly rides along as a secondary kind: 21 issues carry it, but only 6 have it as the primary kind (#775, #781, #797, #833, #847, #853). Ledger-row-claim defects appear in 4 issues (#775 `Re-read ·` 0.18.0:79, #830 R6, #831 R1/R6, #833 E3). `seal/specs/…/overview.md` is in 3 (#808, #812, #815).
- Fix-range git walks: #797 → #802 added `walk_tip`, and #805 (r2) found that a merge from the base's side breaks it (open). #860 (`round_record.py#touched`, r2 of #859) is the same shape, a range that holds a merge, in a second reader (open). Both are reader-other over git history.
- `reader-guess` issues outside the three big families: #848 (`generic_units`, found in another repository, silent `ok` on a changed body; open) and #858 (`plugin_directory_check.py` infers "not listed" from two GitHub repositories; open).
- 18 of the 33 review-filed issues come from the last round of a capped run (14: #762, #763, #791, #808, #811, #812, #813, #815, #830, #833, #844, #847, #849, #854) or from the post-review check after one (4: #792, #810, #816, #831).
- Converged with no new issue after their fix in the window: heredoc (#803), the `Pact` row reader (#793), the encoding walker (#782), changelog fragment lag as a record (#802, though its walker reopened as #805), and reverify (#829, short window). Not converged: worktree guard (#856 open after #855), broad gate (#852 open after #851), pact markdown (#844 open after #843).
