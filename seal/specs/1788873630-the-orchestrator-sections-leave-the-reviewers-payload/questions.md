# 1788873630-the-orchestrator-sections-leave-the-reviewers-payload — questions

The design gate was answered by the repository owner in one batch before the
first edit (`routing.md`), and nothing below blocked the work. Each of these
arose after that batch, so it is written down rather than raised — every one
names its answerer, and none of them changes what was built.

## Q1 — the ledger's removal rule has no clause for a file split

**Who answers:** the repository owner.

`CLAUDE.md` and `CONTRIBUTING.md` say: *A row whose anchor a change removes is
REMOVED, not re-pointed. Its claim went with the code.* This change met that
rule three times and its rationale did not describe any of them — the claims
did not go anywhere, the prose moved to another file. Proof that it moved
unchanged is in the fragment: `--reverify` returned `b1368831`, `c0dc63a1`,
`21ad749e` and `98a430c2`, the same hashes the removed rows carried.

**Followed as written**, because the task instructed it explicitly and because
`evidence-check` reports such an anchor BROKEN, and BROKEN means go edit the
ledger.

What the owner may want to settle is whether a fourth state or a clause is
worth having. The trade, stated:

- **Leave it.** A removal-and-re-statement is honest, costs one row per
  anchor, and lands the claim in the branch that caused the move. What it
  costs is the verification history: three rows carrying between one and six
  dated re-reads became three rows dated 2026-09-08, and the history now
  lives only in the released sections of `seal/ledger.md`, findable by
  whoever thinks to look.
- **Add a move clause.** A row whose anchor's unit is found intact in another
  file could be re-pointed with its history intact. What it costs is a
  checker that searches for a heading across the tree — which
  `evidence-check` deliberately does not do at this scale; the BROKEN message
  already says *repo-wide scan skipped: over 200 files*.

This is recorded and not acted on, because a fourth ledger state is
mechanism and the moratorium on new parsed fields is a rule this session does
not get to weigh.

## Q2 — should the reference construction become a check?

**Who answers:** the repository owner.

Two enumerations in #265 were taken by grep and both were short, and the same
hole caught this session before a failing test exposed it. What found both was
a 40-line script, kept at
`/private/tmp/.../scratchpad/a4.py` for this session only and therefore gone
tomorrow. It asserts one property: **no live file names a moved heading beside
a file that does not hold it, and none names a heading that stayed beside the
file it left.**

It has the shape a check wants — it can fail, and it did, twice: once on the
two constants in `tests/test_the_rules_have_one_owner.py`, and once on its own
first version, which reported clean because Python adjacent-string
concatenation splits a pinned phrase across two literals and the flattening
did not account for it.

Not built, for one reason: it is mechanism the ticket did not ask for, and
scope is *only what was requested*. The judgment for the owner is whether the
class — *a document reference that survives a move by naming the wrong file* —
is worth a permanent case, given that the split it would guard happens rarely
and the next one is #120 growing the contract across five agents in 0.10.0.

## Q3 — a file's references are named in more than one form, and no check knows it

**Who answers:** the repository owner.

Related to Q2 and narrower. `skills/code-review/SKILL.md` is named as a path
in eleven test modules and as the tuple `("skills", "code-review",
"SKILL.md")` in ten more. Any future estimate of what touching a document
costs will be taken by grepping the path, and will be short by the same ten.

The cheap version is a one-line helper in `tests/` that yields every module
naming a given repository file in either form, used by whoever is estimating
rather than asserted in a case. The question is whether a helper nobody is
obliged to call is worth having — which is #180's shape again, and the reason
this is a question rather than a line already written.
