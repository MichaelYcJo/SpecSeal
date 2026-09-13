# the record-before-the-fix sequence has no arm (#345) — questions for the planner

<!-- seal/specs/1789296200-the-record-before-the-fix-sequence-has-no-arm/questions.md —
decisions only a human can make, extracted so nothing ships on a silent
assumption. Before adding a row, check the inheritance rule: if policy is
silent but existing behavior answers it, inherit and record — only genuinely
NEW rules belong here. -->

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | In this repository's own correct runs, how often is the branch's HEAD **not** the `Target SHA` at the moment `new` runs? | **a measurement** — phase 1 takes it | Over every `rounds/round-N.md` under `seal/specs/`, compare the record's `Target SHA` against its adding commit's first parent. **0 or 1 differing → phase 2 refuses. 2 or more → phase 2 prints and continues.** The criterion is written here before the number is taken so the number cannot be read to suit the build | refuse | ⬜ |
| Q2 | Should a round record that says **why** it was written after its own fixes **pass** the pull request, where today it fails on a line no later commit can clear? | **a person** — the repository owner | **Yes** (plan's phases 3 and 4): the record carries a written reason, `written_late` prints instead of failing, and #120's missing fourth exit exists. It is a documented waiver on a gate, so `CONTRIBUTING.md` §*What a change to a gate must carry* is owed in the pull request. **No**: phase 2 ships alone, the refusal at `new` keeps no way past it, and a late record stays unmergeable without a history rewrite or an owner merging red — which is where work item 1789034970 ended | **yes** — build phases 3 and 4 | ✅ |
| Q3 | Where in the record does the reason live — a new `\| … \|` field row, or both SHAs plus the reason in the existing `Target SHA` cell? | **the work** — phase 3 decides against `close`'s field handling | `templates/sdd-round.md` already asks `Target SHA` for *both, if HEAD moved mid-review*, and `check_round` already reads that cell with `SHA_RE.findall`, so the second home half exists. A new row is cleaner to read and has to survive `close`, which acceptance A7 pins either way | the existing `Target SHA` cell, extended | ⬜ |
| Q4 | What is the flag and the field called? | **the work** — phase 3 | `tests/test_one_word_one_meaning.py` and `CLAUDE.md` §*a thing more than one party can have is named with whose* rule out two obvious candidates: **declaration** already means `routing.md`'s throughout `chain_check.py`, and **arm** already means a branch of a check a mutation should kill (`arm_check.py`) and the commit gate's review arm | none — the constraint is what is settled, not the word | ⬜ |

## What is not a question, and why

**Routing.** Answered by the owner in one batch before the first edit and
committed at `routing.md` beside this file: review through the review chain,
destination open the pull request, planning the framer, implementation `smith`.

**The record language.** `seal/config.md` carries a `Mode` row and a
`Broad gate` row and no `Record language` row, so these documents are in
English — every way of not naming one lands on English
(`skills/implement/SKILL.md` §*The language the records are written in*).

**Whether a new cutoff constant is owed.** No, and `spec.md` §Scope says why
for both directions: phase 2's refusal fires inside a live run and never
judges an existing record, and phase 4's new state is a relaxation.

**Whether `new` should commit the record itself.** Rejected on grounds a
reader can open — `plan.md`'s alternatives table — and deferred to an issue
rather than to a person, because the grounds do not turn on anybody's
preference.

**Q2 answered 2026-09-13 by the owner: yes — build phases 3 and 4.** A round
record that writes down WHY it was written after its own fixes passes the pull
request. This is a documented relaxation of a gate, so the pull request body
owes `CONTRIBUTING.md` §*What a change to a gate must carry* on both halves:
what the new refusal costs a correct run (phase 1's measurement is the
evidence), and what the new pass state lets through.

The alternative was to ship phase 2 alone and leave `new`'s refusal with no way
past it. Work item 1789034970 is where that ends: a pull request red on a line
no later commit could clear, and three bad exits.
