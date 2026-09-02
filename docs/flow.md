# 0.4.0 → 0.5.0 flow

A checklist for the tickets that carry `docs/one-root-by-lifetime.md`. Tick
a box when the ticket's pull request has merged into its release branch.
Delete this file when the last box is ticked; the design record and the
tickets are the durable copies, this is only the place to look each morning.

Each release branch is cut from `main`; each ticket is a branch cut from the
release branch and squashed back; the release branch merges into `main` as a
merge commit (`docs/branch-and-release.md`).

## 0.4.0 — `release/v0.4.0`

- [ ] #78 the ledger fragments fold at release, and an open evidence-todo row refuses it (on today's paths)
- [ ] #30 the sealer: one agent takes the seal, once, after the rounds settle
- [ ] #79 the root merge: `specs/` + `.specseal/` → `seal/`, opt-in is the root's presence, session-start hook moves once, CI and path references follow
- [ ] release: gather the changelog, fold the ledger, move `plugin.json`, merge to `main`, tag `v0.4.0`

## 0.5.0 — `release/v0.5.0`

- [ ] #80 local mode under `.git/seal/`, and the first-setup question (shared / local)
- [ ] #82 `seal/config.md`, first row the pull request language
- [ ] #81 `seal export` / `seal import`
- [ ] release: gather, bump, merge, tag `v0.5.0`

## Later — not scheduled

- [ ] #83 `settle`: fold a released work item into `docs/` and the ledger, then remove it (fix the two readers first)
- [ ] #84 framer: the agent that writes the frame the smith fills
- [ ] #85 an orphan branch as the ledger's home, opt-in by ref

## Order inside a ticket

1. Branch from the release branch; write `routing.md` before the first edit.
2. spec · plan (framer, once #84 exists; the session until then) → smith → warden rounds → sealer → pull request.
3. The pull request body carries `Closes #N`; the release workflow closes the ticket when the release reaches `main`.
