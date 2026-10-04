# 1791119073-a-pact-row-outside-the-config-table-is-refused — overview

📋 implement applied
· spec:     `spec.md`, `plan.md`, `questions.md` of this item; `docs/the-pact.md` §*How a signatory names the pact*, §*What this does not see*; `templates/config.md` §*Pact*; `hooks/config.py#config_rows`, `#unfenced`, `#hidden_lines`, `#pact_declaration`, `#declared_pacts`; `evidence_check.py#record_pact_changes`, `#NOTIFY_ROW_SHAPE`, `#gfm_lines`; `hooks/blocks.py#gfm_lines`; the census in `tests/test_every_reader_ends_a_line_where_gfm_does.py`
· evidence: `seal/ledger/1791119073-a-pact-row-outside-the-config-table-is-refused.md`, eight `Re-read ·` rows and N1–N4
· verified: executed — each phase's modules, the new cases red at the base or under `mutation-check`, `evidence-check .` and `--strict`, `survivor-check`; the full suite is not run here

## Why this work exists

A `Pact notify | always` row written where the table's reader does not reach
it was read as the default, and `--reverify` then lost a pact change for good.
Now such a row is refused, and every caller leaves the moved row or says so.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| The refusal sentence | Spec's shape: "… is shaped as a `Pact notify` row and is not read as one — it stands outside the `\| Item \| Value \|` table or spells the item another way; write it as a row of that table". Built: no dash or semicolon of its own, a third cause ("or holds a character that cuts the line"), the remedy as `\| <item> \| … \|`, and every whitespace character but a space shown as `<U+XXXX>` | built | `spec.md` §*Data & interfaces*: "The builder chooses the final text, and S16 pins it". The writer's `LEFT` line puts ` — ` and `; ` after the sentence, and W9 and W11 lines print as a correct row unless the invisible character is shown (`phases/phase-1.md`) |
| The shape's grammar | `spec.md` Scope 2: "a pipe, `Pact` or `Pact<\s+>notify`". Built after round 1 of PR #784: the leading pipe optional, the separator between the two words possibly empty, and each line read with its format characters (Unicode category Cf) removed, in both readers | built | Round 1's 🟡 1 and 🟡 2, executed by the warden: GFM renders a line with no leading pipe directly under the table as one of its rows, and renders a Cf character as nothing, so both were rows read as the default with no refusal |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and the typecheck at the branch head | the sealer, spawned by the orchestrator after the rounds settle |

## Not done

A misplaced `Ledger frozen from` row is the one other silent case among the
`seal/config.md` readers (`spec.md` §*Out*). Nothing is lost there, so it is
reported to the orchestrator as a candidate to file rather than built.

`skills/evidence-check/SKILL.md` carries a sentence parallel to the vendored
paragraph's pinned one. It stays true after phase 3 and was not edited, so
the region sibling E edits stays unmoved.

## Fed back into the spec

- *Inferred during implementation:* the refusal shows every whitespace
  character other than a space as its code point.
- *Inferred during implementation:* on GFM's cut a line is hidden only where
  every reader piece of it is hidden, which is the reading that refuses more.
- *Inferred during implementation:* the shape reads a line with every format
  character removed and needs no leading pipe (round 1 of PR #784).
