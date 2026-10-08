# 1791384159-a-unit-the-extractor-cannot-bound-is-refused — overview

`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens rather
than reconstructed at the end. Facts that must outlive this work item go to the
evidence ledger, not here.

📋 implement applied
· spec:     this work item's `handoff.md`, `spec.md`, `plan.md`, `questions.md`, `routing.md`; `docs/the-evidence-ledger.md` §*A row is a content anchor, and it names no commit*, §*What the checker refuses, and what it says while refusing*; `skills/evidence-check/SKILL.md` §*Resolving a unit without a parser*, §*Verdicts and what to do*, §*What the region is*, §*Known limits*; #848's body; `seal/config.md` (`Ledger frozen from`, no `Record language` row)
· evidence: `seal/ledger/1791384159-a-unit-the-extractor-cannot-bound-is-refused.md` — U1–U8 for the new units, one `Corrected ·` row (0.4.0's "An anchor resolves"), fourteen `Re-read ·` rows written by `--reverify --into` after each cited claim was read; two rows of #867's fragment (K23 and its fenced-section `Corrected ·` row) re-stamped in place
· verified: executed — every new case seen red against d611c1a0 or the previous phase's head and green after, `bin/mutation-check` on every added unit (one mutation at a time; each survivor answered by a case or by removing the redundant unit), each phase's slice, the eight guard modules the spawn named, `bin/evidence-check --strict .` (0 broken; 8 drifted, all `agents/warden.md#"## Report"`, not this branch's), `survivor-check` and `correction-check` over `origin/release/v0.21.0...HEAD`, `uvx ruff check` and `uvx ruff format --check` on the changed Python files. Read — each drifted released row's claim. Unverified — the full suite (the sealer's)

## Why this work exists

A unit the checker could not bound — a brace-language body past a
multi-line signature, a `.py` the interpreter cannot parse, any suffix the
indentation rule was never written for — was hashed over a span that left
the body out and read `ok` through any rewrite of it; now each suffix has
one rule, and a unit no rule bounds is `BROKEN` with the anchor to use
instead.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| The shape `resolve_unit` returns | `questions.md` Q4 default (a): "a three-field namedtuple `(places, resurrected, refused)` and all three callers unpack it in one commit" / a tuple subclass, `Resolution`, that unpacks as the old pair and carries `refused` as an attribute | the pair with the attribute | Q4: "the constraint is one reading, not the tuple". The reason comes back from the same call. 21 call sites in six test modules and `resolve`'s "anything importing this module" unpack the pair, and a refused answer already has no places, so a caller that does not ask reads nothing rather than a span |
| How many production callers read the refusal | `spec.md` §*Data & interfaces*: "Its three callers are `judge`, `rider_check.py#region_lines` and `survivor_check.py`'s `resolves`" / `read_citation` is a fourth | all four, and `read_citation` prints it | it calls `resolve_unit` for a citing row's section; without the attribute a bare symbol there read "the section it names is gone" |
| A bare symbol in a `.md` file | `spec.md` *In* 1: `.md` refuses "zero or several matches, as today" / a bare symbol there ran the indentation rule over markdown | refused, naming the heading path | the table's rule for `.md` is the heading path, which a bare symbol does not name; measured, 1,964 `.md` coordinates in this repository's ledgers and none bare |
| `generic_units`' signature | `spec.md` §*Data & interfaces*: "`generic_units(lines, name, rule)` takes the rule that bounds the file" / `generic_units(lines, name, rule, family=None)` | the family beside the rule | the lexer cannot read `'` without knowing whether the language makes it a char, a string or a lifetime; `brace_family(path)` reads the same suffix table |
| What a refused candidate does to the reading | spec silent on several candidates / one refused candidate among those `generic_units` would choose from refuses the whole reading | refused | a span chosen beside a refused candidate is a choice among places nobody bounded; `skills/evidence-check/SKILL.md` §*Verdicts and what to do*: "An ambiguous MAJOR unit is BROKEN, loudly, and never a measurement" |
| What the fixtures hold inside each form | `spec.md` *In* 2 names a brace inside each form / opening brackets only | opening brackets | measured: with `}` in every form, eight form mutations survived, because a stray closer inside a body is carried past by the deeper-line clause; a stray opener always refuses (`phases/phase-2.md`) |
| `plan.md` §*Seams*, written before #867 landed | "`file_units`'s `.md` arm calls `heading_level`, and `resolve_unit`'s quoted arm calls `heading_path`; if #867 moves either, the arm follows the move" | #867's `markdown_lines`/`heading_rule` kept as they stand | the merged arms already called them; this work replaced only the suffix test in front of each |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and the typecheck | the sealer, once, after the review rounds settle |
| How many rows of a consuming repository's ledger change verdict on upgrade (`questions.md` Q3) | that repository's installer, by `evidence-check --strict .` at 0.21.0; the one known instance is #848's reporter |
| The walk against real code of each family beyond the fixtures — a large TypeScript or JSX codebase, C with preprocessor branches, Rust with macros | a consuming repository on its first run at 0.21.0; a misread there that re-balances by accident is the silent case `plan.md` names |

## Not done

- **Declaration shapes the opener never matched** — Go receiver methods
  `func (s *S) Name(`, generics `fn f<T>(`, typed constants. Out of scope by
  `spec.md` §*Out*: they read `BROKEN` today, the loud direction, and a
  quoted-line anchor works for each. Named in the hand-back as one issue to
  file.
- **JS regex literals and JSX text are not lexed.** A bracket they hold that
  stays open refuses the unit; JSX text with an apostrophe refuses it too.
  Lexing either is a grammar the walk does not have; the Known-limits bullet
  says so.
- **The eight `agents/warden.md#"## Report"` rows** that read `DRIFTED` at
  this branch's head came with `origin/release/v0.21.0` (#837 and #867), and
  this work neither changed nor read them. Named in the hand-back.

## Fed back into the spec

- *Inferred during implementation:* a bare symbol in a `.md` file is refused
  with the heading-path sentence (`docs/the-evidence-ledger.md`'s new
  paragraph states the table it follows from).
- *Inferred during implementation:* one refused candidate among those the
  declaration rule would choose from refuses the whole reading.
