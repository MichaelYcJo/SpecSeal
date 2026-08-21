# public release hardening — overview

📋 implement applied
· spec:     README.md · README.ko.md · docs/review-chain-spec.md ·
            docs/worktree-guard-spec.md · skills/evidence-check/SKILL.md —
            each read against the code it describes, not trusted as written
· evidence: none added — this work fixed the checkers, it did not cite policy
· verified: every defect below was reproduced before the fix and is pinned by
            a regression test; suites run on macOS locally and on the
            ubuntu + macOS CI matrix

## What was done

Two review passes before first publication, run against the executable code
and against the documentation separately. The premise was that this plugin had
never been read by anyone but its author, and the reviews were told to assume
defects rather than confirm health.

They found that **three of the flagship behaviors did not do what the README
said they did**, each failing in the silent direction.

## What changed

```
hooks/commit-review-gate.py       changed  quote-aware tokenizer; unparseable
                                           git+commit asks instead of passing
skills/evidence-check/scripts/
  evidence_check.py               changed  deleted root-level citation is
                                           BROKEN, not EXTERNAL; URL ports
                                           stop matching the coordinate shape
hooks/worktree-guard.py           changed  /proc before lsof; bad idle-minutes
                                           override falls back instead of
                                           dying at import; undeterminable
                                           detection asks instead of denying
hooks/session-lease.py            changed  session id via basename; notebook
                                           edits lease their repo
hooks/lint-python.py              new      shell hook ported to Python
hooks/lint-python.sh              deleted  shebang + exec bit do not exist on
                                           Windows
hooks/hooks.json                  changed  every hook invoked through python3
CLAUDE.md                         changed  distributed block no longer sets a
                                           response language
install.sh / uninstall.sh         changed  refuse to edit a block whose end
                                           marker is missing
README.md / README.ko.md          changed  claims matched to behavior; Limits
                                           section; language switcher
tests/                            changed  +15 regression cases
```

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| Commit gate reach | README: "no commit passes the gate"; code emits `ask` and `[no-review]` skips it | Fix the README | `docs/review-chain-spec.md`: "Chosen `ask` over `deny` deliberately" — the code was right and the README oversold it |
| What the drift check proves | README: "when code moves away from its spec, the build turns red"; the script only checks that a coordinate resolves | Fix the README | `skills/evidence-check/SKILL.md`: "DRIFTED means someone must re-verify, not that the claim is wrong" |
| Deleted root-level citation | Spec silent; code classified it EXTERNAL, which `--strict` exempts | Fix the code | Cross-repo coordinates always carry a prefix directory, so a bare path with no file is a broken citation |
| Heredoc commit form | Spec silent; a regex split on `;`/`&&`/newline shredded quoted arguments | Fix the code | The gate's whole purpose is the commits Claude Code makes, and that is the form it is instructed to use |
| Session detection when unusable | Spec: deny conservatively | Change both | A deny that fires on every switch in extension-hosted environments is an outage, not a cost |
| Missing lsof | Spec silent; `proc_cwd` returned None and the tree read as single-stream | Fix the code | Fail-open in the direction that yanks another session's branch |

## Not verified

| Item | Who must answer |
|---|---|
| Hooks on real Windows — the `python3` invocation removes the shebang and exec-bit dependency, but nobody has run them there | a maintainer with a Windows machine, or the first user issue |
| `evals/` — authored against `claude plugin eval`, which is early access and has never been invoked | Anthropic-side enablement |
| Whether the demo GIF's recording exposes anything datable | reviewed frame by frame: it does not, but only the author knows what was on screen |

## Fed back into the spec

- `docs/worktree-guard-spec.md` — the undeterminable-detection row changed
  from deny to ask, with the reason recorded: a guard that fires on every
  invocation in an environment has stopped being a cost and become an outage.
- `docs/worktree-guard-spec.md` — lease coverage narrowed from "every tool
  call" to the repo-touching ones, matching what `hooks.json` registers.
- README gained a `Limits` section. Two of its entries (Windows untested,
  evals never run) had existed only in the author's head.
