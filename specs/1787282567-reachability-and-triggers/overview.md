# reachability and triggers — overview

📋 implement applied
· spec:     skills/implement/SKILL.md (bootstrap rule) ·
            skills/legacy-parity/SKILL.md (config fields, path resolution) ·
            docs/review-chain-spec.md (cycle contract, mark convention) ·
            code.claude.com plugin manifest schema and bin/ semantics
· evidence: none added — no policy clause was settled by opening code here
· verified: executed — 110 local cases (111 on ubuntu, where the /proc probe
            runs instead of skipping), `claude plugin validate --strict`.
            Read only — whether narrowing the triggers actually lowers loaded
            context; that is an argument from the descriptions, not a
            measurement

## What was done

One theme, arrived at twice: **a capability that exists in code but cannot be
reached is not a capability.** The plugin had four of them.

1. **The drift check could not be typed.** The cheat sheet said
   `python3 <plugin>/skills/evidence-check/scripts/evidence_check.py` and no
   document ever said where `<plugin>` was — for the very check the demo GIF
   opens with.
2. **CI wiring had the same dead end**, which mattered more: the README's
   headline is that CI catches drift, and a check nobody manages to install
   catches nothing.
3. **Migration mode required a hand-written declaration.** `docs/parity.md`
   had no template, and its field list lived inside a skill that loads only
   once that file exists — a closed loop.
4. **Parity had no enforcement at all**, while every other promise had some.
   The review mark is one bit that cannot distinguish a review that compared
   against the original from one that did not.

Then a fifth, found while auditing the skills: triggers written before the
agent chain existed were firing on keywords, so a single request could open
three scope conversations and load three skills to hold them.

## What changed

```
bin/evidence-check                new      resolves the script from its own
                                           path, so the plugin's location
                                           never has to be known
skills/evidence-ci/SKILL.md       new      vendors the checker, writes the
                                           workflow, asks about --strict and
                                           path filters rather than guessing
skills/parity-setup/SKILL.md      new      declare a migration later
templates/parity.md               new      the declaration, with the local
                                           checkout path deliberately absent
skills/implement/SKILL.md         changed  bootstrap asks the migration
                                           question once, at _ai/README.md
hooks/commit-review-gate.py       changed  second arm: parity mark, its own
                                           opt-in, both reported at once
skills/legacy-parity/SKILL.md     changed  writes specseal-parity after a
                                           comparison actually happened
agents/smith.md                   changed  owns the design gate; calls the
                                           two planning skills
agents/warden.md                  changed  writes the parity mark, never early
skills/*/SKILL.md (9)             changed  each states where it does not belong
commands/                         deleted  moved into skills/, the documented
                                           layout; invocation names unchanged
.claude-plugin/plugin.json        changed  displayName, repository, keywords
```

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| Where the parity question belongs | Spec silent — it assumed the file existed | Ask at bootstrap, once | The only moment that is both once-per-repo and already a setup conversation. A session-start prompt would be the nagging this plugin exists to avoid |
| Who writes `docs/parity.md` | Spec silent | Derive three fields, ask for one | Which repo is the original is a fact the machine cannot hold; the rest it can. Guessing it is worse than having no parity mode, since a comparison against a guessed original proves nothing |
| Parity gate as a fifth hook | Spec silent | Fold into the commit gate | Both fire on `git commit`, and a third Python process on every Bash call is a real cost paid by every user, including those with neither opt-in |
| Gate scope | Spec silent | Silent on commits confined to `docs/`, `specs/`, `_ai/` | A gate that fires where no comparison was possible teaches people to click through it, which costs more than the check is worth |
| build-fix vs debug | Their descriptions overlapped | Keep both, cross-reference | Their bodies share no procedure: nothing runs during a compile error, so there is nothing to reproduce. Merging would load half-irrelevant content whichever fired |
| confidence-check / feature-planner | Looked redundant with the design gate | Keep content, narrow triggers | The gate decides *when to stop and ask*; these are *what to check* and *how to decompose*. The duplication was in the trigger, not the text |

## Not verified

| Item | Who must answer |
|---|---|
| Whether the narrowed triggers actually reduce loaded context — this is read, not executed | a session log measuring which skills load per request |
| Whether `/specseal:evidence-ci` produces a workflow that passes on a repo other than this one | the first user who runs it |
| Whether bootstrap's migration question reads as helpful or intrusive in practice | the first migration project that installs this |

## Fed back into the spec

- `docs/review-chain-spec.md` — the gate is now documented as two independent
  opt-ins with an arm each, and the marks section covers both. The reason for
  independence is recorded: nesting parity behind `_ai/` would hide it in
  every repo that declares `docs/parity.md` without the review workflow.
- `skills/legacy-parity/SKILL.md` — added the mark convention, with the one
  rule that makes it worth having: write it only after the comparison
  happened, because a mark for uncompared work converts "nobody checked" into
  "someone checked and it was fine".
- A test now fails the build when a model-invoked skill ships without a
  NOT-for boundary, so this cannot silently regress.
