# 1790076060-the-cap-is-read-as-bounding-fixes-and-the-pile-is-nobodys — questions for the planner

**What the tree answered, listed so nobody reopens it.** The tickets left these
open and the repository settled them; the grounds are in `spec.md`'s Grounding
table and `plan.md`'s Alternatives table, where the next party can overturn
them by opening what was opened here.

- **Which document owns each rule.** `docs/review-chain-spec.md`, for both. It
  already owns the cap and already carries the leftovers table that lists a
  finding's homes, and `tests/test_the_rules_have_one_owner.py` is the shape
  the repository uses for twelve rules already.
- **Whether a capped run's fixes may go unread.** No. `round_record.py seal`
  refuses to write `Broad gate` on a last record whose `Fixes checked by`
  reads anything but `no fixes to check`, and `chain_check` fails a ready pull
  request on `nobody`. So capped fixes owe one verifying round at their diff.
- **Whether the reopening bound's terminal record may write fixes too.** No.
  `chain_check.py`'s reopening walk refuses a second fix-closing record after
  a floor `no`. A sentence permitting it would name a state the checker
  refuses, which is #341.
- **Whether the two exits are one rule.** They are not. The round cap and the
  reopening bound both end a run `capped` and permit different things, and the
  repository's own rule about a word more than one party can have is what
  forces them to be named apart.
- **Whether a review run should open a new issue where one already owns the
  ground.** No — it comments on that one. Measured on the instance both
  tickets cite: round 7 of `1790039346-…` sent all seven of its findings to
  #491 rather than opening seven issues, and `docs/issues-and-milestones.md`
  §*An issue is its body and its comments together* already makes a comment
  the way a ticket grows here.
- **Whether `seal/follow-up.md` is a home for a finding that names nobody.**
  No. Its own opening rule is the same test, so a finding that fails the test
  fails it there too.
- **Whether the 0.8.x moratorium bars this work.** It does not — it names a
  release line far below the running one. The design respects it regardless,
  because its reason has not expired: every parsed field that ever arrived
  cost a checker arm, a template row, a protocol row and a cutoff, and this
  work needs none of the four.

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | Does the tracker make the trade `seal/follow-up.md` already made for its own file — that a real defect nobody will schedule stops being visible in the tracker, and lives in the round record and the pull request body instead? | a person | **Take the trade** (the ladder as specified): the pile stops growing by construction, and a defect nobody will schedule is visible only to whoever reads the work item's records, until `settle` retires the directory at a later release — after which the pull request body is what carries it. **Refuse it**: every finding is filed as today, and the gap stays the pile — 48% closed of 89, measured 2026-09-22 in round 1's fix pass, where this cell first read 47% — which is what the owner asked about. #493's body proposes the trade and says this is what the ticket decides | **Take the trade.** The run is `automation`, so nothing stops to ask; the ticket was raised by the repository owner and its body argues for it, and `seal/follow-up.md` already made the same trade on the grounds that an unowned row is not a plan. The cost is stated in `spec.md` and in the ladder's own prose, so a reader meets it rather than discovering it. **Where it is overturned is the rung-4 paragraph in `docs/review-chain-spec.md`, which names the repository owner and outlives this directory** — `settle` retires the work item at a later release and takes this row with it, which is the same disappearance rung 4 names for the findings, so a row that pointed at itself as the durable home was pointing at the wrong one (round 1's ⬜ 6). **Shipped on the default in phase 3** (`00b7b306`): the cost is the fourth rung's own paragraph in `docs/review-chain-spec.md`, a paragraph of `overview.md`, and a paragraph of `changelog.md`, each naming the repository owner as who overturns it. The row stays open because no person has answered it | ⬜ |
| Q2 | Which places still carrying the wording this branch removes are correct where they stand, and which should have moved with it? | a measurement | `survivor-check` against the base reports every one. Hits in `CHANGELOG.md` and in earlier work items' round records are durable copies by design and take a `survivors.md` range row; a hit in a live document or in a checker's comment is wording that should have moved | Run it in phase 4 and answer the report line by line. The phrase `every finding still open becomes an issue` alone stands in seven files today, three of them earlier work items' records | **None — measured in phase 4.** `survivor-check --range 6d410023..HEAD` examined 1,200 files against the 7 sentences the range removed and reported *no removed wording is still standing*, exit 0. No `survivors.md` was written, because a file with no rows records nothing. The seven standing copies of *every finding still open becomes an issue* are not in the class: the range removes that wording nowhere — every one of them is about the reopening bound, where the sentence is still true. The one place it has gone imprecise is `chain_check.py`'s `CAPPED_EXIT`, a runtime message this work item may not change; it is in `overview.md` §*Not verified* with the repository owner named, and `survivor-check` is structurally blind to it for the same reason | ✅ |
| Q3 | Does correcting the restating comment in `skills/code-review/scripts/chain_check.py` drift a ledger row anchored on that unit? | the work | A row is a content anchor, so a comment edit inside the anchored unit drifts it and `evidence-check --reverify` recomputes the hash. If no row is anchored there, nothing is owed | The phase that makes the edit runs `evidence-check`, and re-verifies what it drifted. The same class cost a finding in the instance both tickets cite — a docstring edit that drifted the row anchored on `comment_scan` | **No — measured in phase 4.** The edit landed in the MODULE docstring at line 230, and every `seal/ledger.md` row anchored in that file is anchored on a function, a constant or a comment block further down; none drifted. `evidence-check` named ten drifted anchors on this branch and not one of them is in `chain_check.py`. The positive proof is in this work item's own fragment: `stopping_floor` re-verified to `db4e9292`, byte-identical to the hash row F1 already carried, and `git diff 6d410023..HEAD` over that file is eight added docstring lines and nothing else. Ten drifted rows elsewhere were each re-read, judged still true, and re-verified | ✅ |
