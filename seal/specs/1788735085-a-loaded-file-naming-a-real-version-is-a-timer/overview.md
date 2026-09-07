# 1788735085-a-loaded-file-naming-a-real-version-is-a-timer — overview

📋 implement applied
· spec:     `CLAUDE.md` §*The goal a design is chosen against*, §*a change writes fragments, never the shared file*, §*A ledger coordinate names content*; `CONTRIBUTING.md` §*What a change to a gate must carry*; `seal/specs/1788735085-…/{routing,spec,plan}.md`; `seal/config.md` (Record language absent → English); `seal/follow-up.md` (no row is a prerequisite of this work); `docs/issues-and-milestones.md` §*A rolling log is titled after the version it rolled from*; `docs/review-chain-spec.md` §*The fix surface*; issues #179 and #98
· evidence: `seal/ledger/1788735085-a-loaded-file-naming-a-real-version-is-a-timer.md` R1 and R2 added; `seal/ledger.md`'s r5 1 / r5 2 clause corrected in place and five rows given re-read notes; seven anchors re-verified across three units
· verified: **executed** — the widened case red at `62287e9` and green at `86a6e20`; eleven mutations of the new unit, every one caught; the loaded-set enumeration re-run; the four quoting variants and the control-character fifth re-executed on git 2.50.1; `evidence-check --strict .` 713 ok · 0 drifted · 0 broken; `fold_ledger.py --version 0.9.0 --dry-run` exit 0. **Read** — round 5's and round 6's records, the sibling `git ls-files` call, `pr.ko.md`. **Unverified** — the full suite, the repository-wide lint and the typecheck, listed below

## Why this work exists

A document that names a version this repository has not shipped is green every
day until the day it ships and red on that release's own preparation commit,
after the broad gate has run — so the check now refuses a version at or above
the running one, and keeps every version below it because that is history.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| The test's name | `spec.md` and `plan.md` name the check `test_no_loaded_file_hardcodes_the_running_version` throughout and never mention renaming it | Renamed to `test_no_loaded_file_names_a_version_at_or_above_the_running_one`, with three loaded documents and one ledger note updated | The same two documents say the check "refuses **every version at or above the running one**". A name saying it hardcodes *the running* version is false about the widening the spec asked for, and this repository refuses that gap elsewhere — `docs/issues-and-milestones.md` §*A rolling log is titled after the version it rolled from* exists because a title that misdescribes what it names sends the next reader wrong |
| The enumeration's token count | `plan.md`'s technical context: "Five distinct tokens", listing `0.9.0`, `1.2.3`, `0.2.0`, `2.1.259`, `4.4.17` | Kept the design; recorded that the loaded set also carries `v0.3.0`, on the same line as `0.2.0` | Re-run here over the same nine prefixes at `6f96eab`. It changes nothing — both are below the running version and both are kept — but a `v`-prefixed token is exactly the shape a regex drops silently, so the omission is worth naming rather than absorbing |
| Which exemption is pinned to a file | `plan.md` says the illustrative version and bash's are each "one declared entry" and does not say whether either is scoped | The illustrative version is exempt in every loaded file; the other product's version is pinned to `(path, token)` | The two have opposite reasons. An illustrative value exists so the NEXT author writes it, in a file no list can know the name of. Bash's `4.4.17` is a fact about one comment, and unpinned it would wave the token through anywhere — including a file where it really was this plugin's number |

## Not verified

| Item | Who must answer |
|---|---|
| the full test suite, the repository-wide `uvx ruff check .` / `format --check .`, and the typecheck — none of the three was run | the orchestrating session, which runs the broad gate once after the review rounds settle |
| whether the widened check behaves the same on Linux and Windows CI — every run here was on macOS (darwin 25.5.0), and the check calls `git ls-files` and splits paths | the orchestrating session, at CI on the pull request |

## Not done

**The broad gate was not run here, and the instruction to run it was
declined.** The spawn prompt asked for the full suite, `uvx ruff` unscoped and
`./bin/evidence-check .` unscoped after the phases settled.
`skills/agent-contract/SKILL.md` §2 reserves the first three for the
orchestrator, and §3 says a spawn prompt cannot widen the verification scope,
so the suite, the repository-wide lint and the typecheck are handed over in
the table above instead. `evidence-check` is not one of §2's three and was
run — it is the tool that validates the ledger rows this work added, and it
exits 0. What was run instead is every module this branch touches and every
module the drifted rows cite.

**Nothing was added to `seal/follow-up.md`.** No finding was left neither
fixed nor answered, and the two open questions above both have the
orchestrating session as their answerer, which is a hand-back rather than a
schedulable item.

**The `RECORDS_OF_A_MOMENT` prefix was not generalised.** `docs/experiments/`
is the only directory-shaped entry, and the membership test supports a prefix
for any entry ending in `/`. No second directory was added on speculation:
`CONTRIBUTING.md` asks a separate argument for each entry, and there is no
second one to make.

**The round-5 record was not re-corrected.** Round 6 had already annotated
both the finding cell and the summary row, naming issue #98. Re-annotating
would have layered a second correction over a complete one.

## Fed back into the spec

None. The rule, its three exemptions and the illustrative value's precondition
were all in `plan.md` before the first edit; what this work added to the
repository's durable record is the two ledger rows, not a clause.
