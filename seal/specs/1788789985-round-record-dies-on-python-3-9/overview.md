# 1788789985-round-record-dies-on-python-3-9 — overview

📋 implement applied
· spec:     `CONTRIBUTING.md` §*Running the checks* (the floor sentence, and the fallback paragraph that already warns macOS ships 3.9 as `python3`) · `CLAUDE.md` §*The goal a design is chosen against*, §*Repo rule — a change writes fragments* · `skills/agent-contract/SKILL.md` §2 §3 §4 §9 §12 §13 §14 §15 · `skills/implement/SKILL.md` §1 §3 §4 · `seal/follow-up.md`'s own opening rules · `seal/config.md` (no `Record language` row → English) · `routing.md`, read and not rewritten
· evidence: three rows in `seal/ledger/1788789985-round-record-dies-on-python-3-9.md`, twelve coordinates, all resolved by `evidence_check --reverify`
· verified: **executed** — the new module's eleven cases, `tests/test_the_record_is_generated.py`'s 94, seven mutations of the guard, `python3 -m py_compile` at 3.9.6 over every shipped `.py`, the real script under 3.9.6 before and after, `ruff check` and `ruff format --check` on the two changed files. **Unverified** — the full suite, the repository-wide lint and the typecheck, which `agent-contract` §2 reserves for the orchestrator

## Why this work exists

A person whose `python3` is 3.9 got an interpreter traceback from deep inside
`round_record.py` and no way to learn that a newer interpreter was the fix;
they now get one sentence, before anything is read or written, naming the floor
and what they are running.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| How the floor number reaches the guard | The handoff: "**Reuse `FLOOR`, do not retype `(3, 12)`.** … Decide and argue in `spec.md` how a stdlib-only script under `skills/` reaches a constant under `.github/scripts/` — if it cannot, say so and say what you did instead" | The literal is retyped and pinned by a test | The handoff's own escape clause, taken with the argument it asks for. A read that can fail gives the guard a second way to die on the one machine with no other way of being told what is wrong; and a fallback-safe read still has to name a floor in its `except` branch, so **the second spelling survives the import anyway** — there is no version of the read that removes the second number. `CONTRIBUTING.md`'s sentence is itself a second spelling of `3.12`, held true by `tests/test_release_hygiene.py#test_the_python_floor_is_the_same_number_everywhere`; this is a sixth carrier under the rule the other five already live by |
| Where the class's property is drawn | The handoff: "*every script in this plugin that a documented command tells someone to invoke directly with `python3 <path>`*" | *a person **or the harness** invokes with whatever `python3` resolves to* | `hooks/hooks.json` runs every hook through `python3 "${CLAUDE_PLUGIN_ROOT}/hooks/dispatch.py"`, so `hooks/root-migrate.py:425`'s `zip(strict=True)` fails on the same machines for the same reason, with nobody watching. The narrower wording also excludes `round_record.py` itself, which no document names after a literal `python3 ` — so read strictly it excludes the member in the traceback |
| Where the deferrals go | The handoff: "write the finding into `seal/follow-up.md` with an answerer named" | Done, and `questions.md` Q1 records the tension | `seal/follow-up.md`'s own opening says a repository with a tracker "should normally hold none of those", and that anything tied to a coordinate is a `# RIDER:` at the line. A rider was weighed and rejected: the finding is about a class of five files, a rider at one line cannot say *and four others*, and nobody opens `gather_changelog.py` before running it. Q1 leaves the tracker-versus-file call to the owner, and it changes where the row lives rather than what it says |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide `ruff check`, and the typecheck. `agent-contract` §2 reserves the broad gate for the orchestrator, run once after the rounds settle. What was run instead: the new module and `tests/test_the_record_is_generated.py` together, 105 passed | the orchestrator |
| Any behaviour on an interpreter older than 3.9.6, which is the oldest one this machine had. The guard is deliberately written with no walrus and no f-string so that it parses much further back, and that is a design intent rather than a measured fact | the repository owner, if a report ever arrives from below 3.9 |
| The four deferred members of the class are **classified, not fixed**: `.github/scripts/gather_changelog.py:151`, `.github/scripts/fold_ledger.py:358`, `skills/implement/scripts/seal.py:324,436`, `hooks/root-migrate.py:425`. The construct in each was read, not run below the floor | the repository owner, via the row in `seal/follow-up.md` |
| Whether a 3.10+ construct nobody has thought of is present. The suite's class check matches two constructs by text, and the `python3 -m py_compile` sweep that covers syntax was run once by hand rather than wired in | the repository owner |

## Not done

**The four other members of the class were not fixed**, and the scope was drawn
that way in the handoff rather than by me: two of the five files are held by
other work items in this same release, and a conflict in them costs a second
run of the broad gate. The fix for each is the same fifteen lines, and
`spec.md` §*The guard is a block, not a shared helper* names
`skills/code-review/scripts/round_record.py#below_floor` as the spelling to
copy so that a third wording does not appear.

**No shared helper module was written.** Every candidate location for one is
further from `skills/code-review/scripts/` than `chain_check.py` is, and an
import is the fragility the whole design is arguing against. The cost of that
choice, stated: the sentence will exist in five files when the deferrals are
taken, and only one test currently reads it. A file adopting the block should
join that pin rather than write its own wording.

**`round_record.py:982`'s `removesuffix` was left alone.** It is 3.9 and the
handoff put it out of scope.

**The gap between the repository's two floor authorities was closed as a side
effect rather than as its own change.** `ruff.toml` and `run_tests.py` are now
compared, but only through the new case; neither of the two existing floor
tests was touched, because changing what an existing gate guards is something
`CONTRIBUTING.md` asks a separate argument for.

## Fed back into the spec

**None as a policy clause.** One sentence in `CONTRIBUTING.md` §*Running the
checks* — "Check `python3 -V` before using it, since nothing here holds the
floor for you: macOS ships 3.9 under that name" — turns out to describe this
ticket exactly, written before it was reported. It was not edited: the document
was right, and what was missing was the command saying the same thing at the
moment it matters. That is the inference this work rests on, recorded here
rather than added to the document as though it were new.
