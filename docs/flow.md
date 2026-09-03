# 0.4.0 → 0.5.0 flow

A checklist for the tickets that carry `docs/one-root-by-lifetime.md`. Tick
a box when the ticket's pull request has merged into its release branch.
Delete this file when the last box is ticked; the design record and the
tickets are the durable copies, this is only the place to look each morning.

Each release branch is cut from `main`; each ticket is a branch cut from the
release branch and squashed back; the release branch merges into `main` as a
merge commit (`docs/branch-and-release.md`).

## 0.4.0 — `release/v0.4.0`

- [x] #78 the ledger fragments fold at release, and an open evidence-todo row refuses it (on today's paths) — merged as #87
- [x] #79 the root merge: `specs/` + `.specseal/` → `seal/`, opt-in is the root's presence, session-start hook moves once, CI and path references follow
- [x] release: gather the changelog, fold the ledger, move `plugin.json`, merge to `main`, tag `v0.4.0`

## 0.5.0 — `release/v0.5.0`

- [x] #80 local mode under `.git/seal/`, and the first-setup question (shared / local) — first, because the rest of 0.5.0 stands on it — merged as #95
- [x] #82 `seal/config.md`, first row the pull request language — merged as #99
- [x] #96 the release guard globs one place for `evidence-todo.md` and two work items keep it in another — before the release, because the release runs that guard — merged as #100
- [x] #81 `seal export` / `seal import` — merged as #102, after seven review rounds and a defect CI's windows leg caught
- [x] #104 the mode is two shell lines in a README, and a repository migrated from 0.3.x was never asked which it wanted — merged as #112, after five review rounds that each found the previous fix aimed at the coordinate rather than the class
- [x] #106 the language row governed the commits and pull requests and nothing else — merged as #113 with #105, four rounds
- [x] #105 `/specseal:config` — the front door to every row, routing the ones that have side effects — merged as #113
- [x] release preparation: sixteen changelog fragments gathered, six ledger fragments folded, `plugin.json` at 0.5.0 — merged as #114
- [ ] release: **the merge into `main` and the `v0.5.0` tag, which are the repository owner's.** `hooks/version-check.py` asks `git ls-remote --tags` and nothing else, so an untagged release is one no installed session is ever told about

**#106 arrived after this list was written.** It is in the 0.5.0 line above
because the row it renames ships in this release: widening it later renames a
key every repository that wrote the file already has, and a rename is the one
change a config file cannot absorb quietly.

**Why #104 and #105 arrived after the other four merged.** 0.5.0 is the release
that introduces the two modes, and it is also the release where every
repository coming from the 0.3.x layout lands in **shared** without being
asked — `hooks/root-migrate.py` moves the committed folders in-tree, which is
shared mode, and `tests/test_first_setup_asks_once.py` pins that the skill
says so rather than offering local beside a layout the hook is about to move.
A switch that exists only as two shell lines in a README leaves those
repositories a whole release cycle with nothing to run.

The two directions are not symmetric, which is what the command is for.

| | local → shared | shared → local |
|---|---|---|
| What moves | `<git-common-dir>/seal/` into the tree, staged | the tree's `seal/` out, `git rm -r --cached` staging the deletion |
| What it costs | the records enter the history, and going back removes them from the tree and not from the history | every other clone loses them on the next pull; `seal import` is how they get them back |
| What a `mv` leaves behind | the pull-request workflow is not installed | the workflow is not removed — **and with `seal/` no longer committed `unverified_check` exits 2 while `chain_check` exits 0 having read nothing**, measured 2026-09-03: a workflow red forever beside a check reporting a pass it did not earn. An earlier note here said both exit 0; that reading came from `$?` after a pipe, which reports the pipe's status and not the checker's — the mistake `seal/specs/1788395377-…/rounds/round-4.md` recorded once already |

## Later — not scheduled

- [ ] #83 `settle`: fold a released work item into `docs/` and the ledger, then remove it (fix the two readers first)
- [ ] #84 framer: the agent that writes the frame the smith fills
- [ ] #85 an orphan branch as the ledger's home, opt-in by ref

## 0.6.0 — what the measurements say to change

In this order. Each one stands on the one before it, and taking them the
other way round means undoing work.

- [ ] **#107 — the rules that go to every agent move out of the prompt and into a file.** First, because #30 adds a fifth agent: without that file the new one gets its own copy of the rules and #107 then has to take it back out. #107 also rewrites `agents/smith.md` and `agents/warden.md`, which #30 changes too.
- [ ] **#109 — measuring a segment and recording what it says becomes automatic.** Early, so the rest of 0.6.0 is the thing that tries it. Landing it last means finding out whether it works in 0.7.0. Its third part — a release opening the next version's log — is tried by 0.6.0's own release.
- [ ] **#97 and #110 — when a review run stops, and what one round's fixes may add.** One branch: both land in `skills/code-review/SKILL.md` and `docs/review-chain-spec.md`, and doing them apart means editing the same paragraphs twice. Different questions, same place — how many rounds to run, and how much new code a single fix pass may leave behind.
- [ ] **#103 — the two defect shapes only Windows has caught are made visible without Windows.** Half of it is a line in the file #97 and #110 have just settled; the other half is a sweep that stands alone.
- [ ] **#30 — the fifth agent, which owns the one full-suite run.** Largest, and last: today the smith and the warden are both forbidden that run and nobody is assigned it. It inherits everything above.
- [ ] #98 — three sentences say `-z` is what turns git's path quoting off. One line, and it rides whichever branch is open.
- [ ] #89 — the running log. It is read rather than done, and it closes at the release. Every agent segment of the flow is timed with `session-cost` and what the numbers say is written there as a comment; when this checklist reached here, that log became the list above.

## While the flow runs

After every smith or warden segment, measure its transcript and add the numbers and what they say to #89. The two changes already being trialled are per-phase smith spawns and scripted multi-file edits; compare each phase of #79 against #78's single segment.

## Order inside a ticket

1. Branch from the release branch; write `routing.md` before the first edit.
2. spec · plan (framer, once #84 exists; the session until then) → smith → warden rounds → sealer → pull request.
3. The pull request body carries `Closes #N`; the release workflow closes the ticket when the release reaches `main`.
