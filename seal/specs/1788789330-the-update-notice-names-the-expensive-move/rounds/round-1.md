# 1788789330-the-update-notice-names-the-expensive-move — review round 1

| Field | Value |
|---|---|
| Target SHA | 0a9dfc54adb12a2d8157be25d96c25a8f807bb28 |
| Ran by | warden on claude-opus-5 |
| PR | 233 |
| Broad gate | passed at e82ef31, under round 3 |
| Fixes checked by | round-2 |
| Contract changes | none — `hooks/version-check.py#notice(have, want)` keeps its signature and both call sites; what the fixes changed is the string it returns, and two cases now pin that string |
| New units | test_the_notice_agrees_with_the_docstring_about_what_a_reload_re_reads (depth 1) |
| Needs a fix | yes — findings 1 and 2. The notice tells a user the reload is the |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 1 of `1788789330-the-update-notice-names-the-expensive-move` (ticket #134, PR #233), at target `0a9dfc5`, base `86e140f`. No prior rounds.

Judged against the ticket's four *Done when* conditions in order. Two divergences the implementer recorded were named as the highest-value targets: whether run 6 of the preload experiment reaches one axis less than the ticket claims, and whether pulling `hooks/version-check.py:18` into the class widened the change past its ticket.

The class to re-derive, by the property rather than by reading the implementer's table: every place this repository tells a user what to do after an update lands — `restart`, `재시작`, `reload` minus `preload`, both languages. A row placed out of class counts as much as a line missed.

Shapes to try to break: a substring assertion over a multi-sentence message; the Korean and English texts contradicting each other; a user-facing sentence stating as fact something only run 6 supports, or the inverse; the banner's rendering.

The report was to be written to a file under the work item, and finding ids to be bare integers.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | The notice sells `/reload-plugins` as the way to load the new release; the same file's docstring says a reload re-reads the copy already in force | `hooks/version-check.py:154` | open | `hooks/version-check.py:19-21` says *out of that same copy*; `skills/update/SKILL.md:88` carries the qualifier and the three user-facing surfaces drop it. Siblings: `skills/update/SKILL.md:135`, `README.md:318`, `README.ko.md:310` |
| 2 | The pinned case passes wording, not meaning: a false reload claim and the deletion of the third unmeasured axis both survive it | `tests/test_version_check.py:96` | open | Executed. M1 and M2 of five mutations survived the case's own assertion body; controls M3/M4/M5 killed |
| 3 | The banner grew 391 → 707 characters and ships the long form `plan.md` chose against | `hooks/version-check.py:148` | open | Measured by calling `notice((0,7,1),(0,8,0))`. `plan.md` §Alternatives: *"The notice carries the short form"* |
| 4 | `spec.md`'s enumeration arithmetic: 2 reload hits not 3, 37 lines not 38, twelve coordinates under *Thirteen lines*, two mistyped work-item ids | `seal/specs/1788789330-the-update-notice-names-the-expensive-move/spec.md:47` | open | `git grep` at `86e140f` re-derived independently; membership itself is correct |
| 5 | `0.5.0` named as run 6's running version; the experiment record names no plugin version | `seal/specs/1788789330-the-update-notice-names-the-expensive-move/overview.md:21` | open | `docs/experiments/2026-09-03-skill-preload-and-the-copy-in-force.md` pins Claude Code 2.1.259 and a date, nothing else |
| 6 | `claude plugin update` named as the whole of what a user does, with no load step — the shape the branch pulled `version-check.py:18` in for | `hooks/ledger-migrate.py:4` | open | Docstring, pre-existing, no user-visible defect. Named rather than fixed |
| 7 | 하십시오체 in a 합니다체 document | `README.ko.md:310` | open | Only such form in the file |

## Paste-ready fixes

```python
        "data.\nEither way it still has to be loaded. /reload-plugins costs "
        "no session, and what was measured about it is a re-read of preloaded "
        "skill bodies out of the copy this session is already on. Nobody has "
        "measured whether it reaches hooks, agent definitions, or the version "
        "you just installed, so a restart is the move with no open question."
```
```
To load it: /reload-plugins re-reads the skill bodies a spawned agent is
handed, out of the copy this session is already on — that is what was
measured and all that was. Nobody has measured whether it reaches hooks,
agent definitions, or <new> itself, so restart for those. Either way this
session keeps running <old> until you do, so nothing is half-applied.
```
```
Then load it. `/reload-plugins` re-reads the preloaded skill bodies a spawned
agent is handed, out of the copy your session is already on — that is what
`docs/experiments/2026-09-03-skill-preload-and-the-copy-in-force.md` measured,
and it is the whole of it. Nobody has measured whether a reload reaches hooks,
agent definitions, or the newly installed version at all, so restart when you
want the update loaded for certain.
```
```
적용하는 방법은 두 가지이고 드는 값이 다릅니다. `/reload-plugins` 는 세션을
끝내지 않고, 하위 에이전트에게 넘어가는 스킬 본문을 다시 읽습니다. 다만 다시
읽는 대상은 지금 세션이 이미 쓰고 있는 복사본이며, 여기까지가
`docs/experiments/2026-09-03-skill-preload-and-the-copy-in-force.md` 에
적힌 측정 결과의 전부입니다. 훅과 에이전트 정의는 어떻게 되는지, 그리고 새로
설치된 버전을 집어 오기는 하는지는 아무도 측정한 적이 없습니다. 새 버전이
확실히 적용되게 하려면 재시작합니다.
```
```python
    # Per SENTENCE, not over the whole message: a bare `"measured" in msg` is
    # satisfied by the gap sentence alone. And per CLAIM, not per word — the
    # sentence has to name what was measured, or `a reload was measured to
    # install the new version` passes every assertion here.
    sentences = [s.strip() for s in msg.replace("\n", " ").split(". ")]

    reload_claim = next(s for s in sentences if "/reload-plugins" in s)
    assert "measured" in reload_claim, "the reload's reach is asserted, not sourced"
    assert "skill bodies" in reload_claim, (
        "the reload's claim names no subject, so it pins a word and not a fact"
    )
    assert any(
        scope in reload_claim
        for scope in ("already on", "in force", "already running")
    ), (
        "run 6's sentinel sat in the RUNNING version's directory, so what it "
        "measured is a re-read of the copy in force. Without that qualifier "
        "the notice sells the reload as the cheap way to load the new install, "
        "which nothing measured"
    )

    # All THREE unmeasured axes. The third — picking up a newly installed
    # version — is the one run 6's own sentinel placement rules out, and it is
    # the axis the ticket assumed, so it is the one most likely to be dropped.
    gap = next(s for s in sentences if "hooks" in s and "/reload-plugins" not in s)
    for axis in ("agent definitions", "installed"):
        assert axis in gap, f"the gap leaves {axis} to silence"
    assert any(
        negation in gap.lower()
        for negation in ("nobody", "not measured", "unmeasured", "no one")
    ), "the gap is stated as a fact rather than as an absence of measurement"
```
```python
        "data.\nThen load it. /reload-plugins costs no session; what was "
        "measured is a re-read of preloaded skill bodies out of the copy you "
        "are already on. Hooks, agent definitions, and picking up the new "
        "install are unmeasured — restart for those."
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_tmp_notice_mutations.py -q` — the pinned case's assertion body verbatim against five mutations of the notice | exit 1, `3 failed, 3 passed`. **M1 (reload claim replaced with *measured to install the new version into this session*) and M2 (third unmeasured axis deleted from the gap) SURVIVED.** Controls M3/M4/M5 killed; sanity case on the real notice green. Probe deleted |
| `bin/test tests/test_docs_line_wrap.py tests/test_one_word_one_meaning.py tests/test_no_real_identifiers.py -q` | exit 0, `30 passed` |
| `python3 -c` calling `notice((0,7,1),(0,8,0))` on the module at the target SHA | 707 characters, 4 lines; line 4 is 316 characters. Old text reconstructed at 391 |
| `git grep -ciI 'restart' 86e140f` · `git grep -cI '재시작' 86e140f` · `git grep -niI 'reload' 86e140f \| grep -vi preload` | 33 · 3 · 2 → 37 distinct after the `docs/flow.md:74` overlap |
| `git -C … rev-parse HEAD` · `git status --porcelain` | `0a9dfc54adb12a2d8157be25d96c25a8f807bb28`, tree clean. Target SHA did not move |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Whether `/reload-plugins` reaches hooks, agent definitions, or a newly installed version | `overview.md` §*Not verified*; the settling method is at `skills/update/SKILL.md:100-104` | the repository owner |
| How the multi-sentence `systemMessage` renders in a real session-start banner | `overview.md` §*Not verified* | the orchestrator, on the first session after this ships. Finding 3 is about its length, which is measurable and is not deferred |
