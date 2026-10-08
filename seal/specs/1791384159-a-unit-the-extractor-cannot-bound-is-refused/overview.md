# 1791384159-a-unit-the-extractor-cannot-bound-is-refused — overview

`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens rather
than reconstructed at the end. Facts that must outlive this work item go to the
evidence ledger, not here.

📋 implement applied
· spec:     (filled when the work item closes)
· evidence: (filled when the work item closes)
· verified: (filled when the work item closes)

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
| `plan.md` §*Seams*, written before #867 landed | "`file_units`'s `.md` arm calls `heading_level`, and `resolve_unit`'s quoted arm calls `heading_path`; if #867 moves either, the arm follows the move" | #867's `markdown_lines`/`heading_rule` kept as they stand | the merged arms already called them; this work replaced only the suffix test in front of each |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and the typecheck | the sealer, once, after the review rounds settle |

## Not done

Nothing yet.

## Fed back into the spec

None yet.
