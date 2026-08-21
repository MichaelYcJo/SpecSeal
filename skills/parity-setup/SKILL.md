---
name: parity-setup
description: Declare that this repo ports behavior from another codebase — find the original, record the baseline, write docs/parity.md.
disable-model-invocation: true
---

# /specseal:parity-setup — turn on parity mode

Writes `docs/parity.md`, whose presence is the declaration that this
repository ports behavior from another codebase. That turns on three-way
judgment (policy ↔ original ↔ new code, with the original preserved when the
policy is silent) and lets the `scribe` agent fetch what the original does.

The `implement` skill asks this question once, when it first bootstraps a
repo. Use this command when the answer was no at the time, when the layout
predates the question, or when the original repo changes.

## Procedure

1. **Stop if it already exists.** If `docs/parity.md` is present, show it and
   ask what should change instead of overwriting a declaration someone made.

2. **Find candidates for the original.** Do not ask the user to type a path
   from memory when the machine can propose one:
   - sibling directories of this repo that are git checkouts — a port usually
     sits beside its original
   - an upstream or fork relation in `git remote -v`
   - repos whose directory structure overlaps this one's

   Present what you found with what each one is, and let the user pick or give
   a path. **Never guess.** A comparison against a guessed original proves
   nothing, which is worse than having no parity mode at all.

3. **Read the baseline.** `git -C <original> rev-parse HEAD`. This is the
   commit the evidence ledger's coordinates will refer to, so record the SHA
   and the date you read it.

4. **Confirm the module.** A port often covers one directory of a larger
   original (`apps/foo`), not the whole repo. Ask when the original has an
   obvious multi-module layout.

5. **Policy root.** `docs/policies/` if present; otherwise propose it and say
   it will be created on first use.

6. **Write two files.**
   - `docs/parity.md` from `templates/parity.md`, committed. Coordinate-trust
     exceptions start empty.
   - `~/.claude/specseal/parity-paths.md` — the machine-local checkout path,
     keyed by this repo's origin remote URL so worktrees and second checkouts
     resolve to one entry. **This never goes in the committed file**: it is
     wrong for every other machine.

7. **Show the result and say what changes now.** Name the `legacy-parity`
   skill, the `scribe` agent, and that divergence from the original now needs
   grounds rather than preference.

## What this does not decide

Whether the port is a good idea, what to port, or in what order. It records
where the truth lives so that later disagreements have somewhere to appeal.
