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
- [ ] #104 the mode is two shell lines in a README, and a repository migrated from 0.3.x was never asked which it wanted — a `Mode` row in `seal/config.md` and `seal mode`
- [ ] #105 `/specseal:config` — the front door to every row, routing the ones that have side effects
- [ ] release: gather, bump, merge, tag `v0.5.0`

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
| What a `mv` leaves behind | the pull-request workflow is not installed | the workflow is not removed — **and with `seal/` no longer committed the checkers exit 0 having read nothing**, measured 2026-09-03, which is the silent-gate state this plugin exists to prevent |

## Later — not scheduled

- [ ] #83 `settle`: fold a released work item into `docs/` and the ledger, then remove it (fix the two readers first)
- [ ] #84 framer: the agent that writes the frame the smith fills
- [ ] #85 an orphan branch as the ledger's home, opt-in by ref

## 0.6.0 — what the measurements say to change

- [ ] #30 the sealer: one agent takes the seal, once, after the rounds settle — the orchestrator has held that role since #78, and 0.5.0 is cut after #82 and #81 rather than waiting for it
- [ ] #89 the running log: every agent segment of this flow is timed with `session-cost` and the improvement it points at is written there as a comment. Nothing on it is built during 0.4.0 or 0.5.0; when this checklist reaches here, the log becomes the tickets of 0.6.0.

## While the flow runs

After every smith or warden segment, measure its transcript and add the numbers and what they say to #89. The two changes already being trialled are per-phase smith spawns and scripted multi-file edits; compare each phase of #79 against #78's single segment.

## Order inside a ticket

1. Branch from the release branch; write `routing.md` before the first edit.
2. spec · plan (framer, once #84 exists; the session until then) → smith → warden rounds → sealer → pull request.
3. The pull request body carries `Closes #N`; the release workflow closes the ticket when the release reaches `main`.
