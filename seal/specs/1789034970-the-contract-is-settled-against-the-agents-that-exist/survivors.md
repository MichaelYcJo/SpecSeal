# 1789034970-the-contract-is-settled-against-the-agents-that-exist — survivor exemptions

## Over the whole branch — what CI reads

`survivor-check --range origin/release/v0.10.0...HEAD` reports fifteen places
against forty-three sentences this range removed. None of them is a stale copy
of a corrected claim standing where a reader would act on it.

**Four were corrected rather than exempted, and not one of the four was
reported.** They were found by enumerating the class instead — every live place
stating who the broad gate belongs to, or calling §6's mechanism an exception —
which is contract §12, and it is why this paragraph comes before the table
rather than after it:

- `.github/workflows/hygiene.yml` and
  `skills/code-review/scripts/survivor_check.py` both said *contract §2
  reserves the broad gate for the orchestrator*, in the present tense, as the
  reason a review round cannot run this very check. The conclusion is
  unchanged and the grounds are not: §2 now leaves the gate to whichever
  definition assigns it, and no reviewer's does.
- `tests/test_a_corrected_sentence_survives_elsewhere.py`'s module docstring
  carried the same sentence, describing #269.
- `tests/test_the_seal_is_taken_once_by_the_sealer.py`'s failure message read
  *the rule its one write excepts*; §6 excepts nothing now, so it names it.

The check saw none of the four, because each states the rule in words the
removed sentences do not share. That is the limit `survivor_check.py`'s own
docstring states, and the enumeration is what covers it.

### The records of the work item that created the contradiction

Seven of the fifteen. #30's `questions.md` Q4 weighed editing §2 inside a work
item that is not its own and chose instead to ship under a window with an
expiry written into it. This work item is that expiry arriving. Each of these
is a statement about a decision rather than about the tree, and rewriting one
would erase the reasoning that produced the paragraph #120 was filed to delete
— which is the one thing a reader comparing the two work items opens them for.

| Path | Quote | Grounds |
|---|---|---|
| `seal/specs/1789002694-two-agents-are-forbidden-the-seal-and-nobody-is-assigned-it/overview.md` | chose to ship under the contradiction rather than edit §2 here | **The closing memo's account of Q4.** It says what that work item decided and why, in the past tense of a decision, and the decision happened |
| `seal/specs/1789002694-two-agents-are-forbidden-the-seal-and-nobody-is-assigned-it/questions.md` | with the definition stating the exception and naming #120 | **The option list the owner was given.** Option (a) is the one that was taken; a question record that no longer shows the options is a record of an answer with nothing behind it |
| `seal/specs/1789002694-two-agents-are-forbidden-the-seal-and-nobody-is-assigned-it/spec.md` | named in the definition as its own exception to §6 | **That work item's specification of what it built**, and it is an accurate description of `agents/sealer.md` as #30 shipped it. This is the one to watch: it is a statement about a definition rather than about a decision, and it stands only because the sentences around it are explicitly about what that work item delivered |
| `seal/specs/1789002694-two-agents-are-forbidden-the-seal-and-nobody-is-assigned-it/plan.md` | the phase-4 record names that paragraph as the one #120 deletes | **The plan's hand-over to this work item**, naming where the paragraph to delete would be recorded. It was recorded there, and this work item found it there |
| `seal/specs/1789002694-two-agents-are-forbidden-the-seal-and-nobody-is-assigned-it/phases/phase-3.md` | name in this record the paragraph #120 deletes | **What phase 3 was asked**, which is what that section of a phase record is for |
| `seal/specs/1789002694-two-agents-are-forbidden-the-seal-and-nobody-is-assigned-it/phases/phase-3.md` | #120 settles §2 and §6 against the whole set of agents before this release ships | **Phase 3's quotation of the paragraph it wrote**, so a later reader can identify the section without opening the definition. Line 134 of the same file additionally carries `<!-- NAME NOT IN TREE -->`, because the case it names was renamed by this work item |
| `seal/specs/1789002694-two-agents-are-forbidden-the-seal-and-nobody-is-assigned-it/phases/phase-3.md` | has to remove the case in the same commit as the section | **The instruction phase 3 left for this work item, and it was followed** — the case and the section left in the same range. A record of a hand-over stays true after the hand-over happens |

### One record of the release that wrote the section

| Path | Quote | Grounds |
|---|---|---|
| `seal/specs/1788433011-every-spawn-prompt-is-retyped-from-memory/spec.md` | Do not run the full suite, repository-wide lint or a typecheck. | **#107's specification of the section as it shipped**, quoting what was then §2's heading in the table that lists which rules moved into the contract and why each was universal. It is dated by the work item it sits in, the way a shipped changelog section is dated by its release |

### Seven coincidences of ordinary wording

Each of these overlaps a removed sentence on three to five words that any two
sentences about the same kind of thing share, scoring between 1.84 and 2.69 —
the floor doing what it was calibrated to do at its edge. The check reports and
a reader judges, and this is the reading.

| Path | Quote | Grounds |
|---|---|---|
| `tests/test_broad_gate_rule.py` | the contract arrives through the same `skills:` frontmatter the definition does | **About how the contract REACHES an agent**, not about what any section of it says. The shared run is *the definition does* |
| `tests/test_broad_gate_rule.py` | it is reached for once an unexplained failure appears | **About when a baseline comparison is taken.** The shared runs are *rounds settle in* and *when it fires assert*, which are the words any two sentences about the gate's timing use |
| `tests/test_every_agent_reads_the_contract.py` | a listed skill the definition never mentions | **About the two halves of how a definition names its contract** — the `skills:` list and the opening paragraph. The shared run is *the definition does not* |
| `tests/test_the_seal_is_taken_once_by_the_sealer.py` | does not separate a coverage probe from a seal | **About the probe sentence in the two definitions**, which this range did not touch. The shared run is *definition does not* |
| `tests/test_the_seal_is_taken_once_by_the_sealer.py` | a second source that drifts from `broad_gate.py` | **About whether the sealer's definition re-describes the gate's checks.** Same three-word overlap, same reason |
| `tests/test_the_seal_is_taken_once_by_the_sealer.py` | dropping `verify` from the spawn is only correct | **About which skills the sealer's spawn carries**, which is #30's Q5 and not this work item's subject at all |
| `seal/ledger.md` | both tools measured rather than inherited from prose | **A ledger row about `uv` and the virtualenv `bin/test` builds.** The overlap is a date and a phase number — *2026 09 06 in phase* and *phase 3 both* |

## What would make these exemptions stop holding

Each quote is its own anchor, and the three groups fail differently.

A record in the first group stops being history the moment it asserts what the
tree holds TODAY rather than what its own work item decided. `spec.md`'s row is
the one to watch, and its grounds say why.

The second stops holding if `#107`'s spec is ever rewritten to describe the
contract as it stands rather than as that work item shipped it.

A coincidence in the third stops being one the moment the sentence carrying it
comes to name who takes the broad gate, or to call a named write an exception.
`tests/test_broad_gate_rule.py` is the file to watch, because it is the module
that pins the ownership sentence.
