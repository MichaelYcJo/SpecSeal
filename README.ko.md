# SpecSeal

[![tests](https://github.com/MichaelYcJo/SpecSeal/actions/workflows/test.yml/badge.svg)](https://github.com/MichaelYcJo/SpecSeal/actions/workflows/test.yml)

**Specs, sealed** — 코드가 스펙에서 멀어지면 빌드가 빨개집니다.

![SpecSeal 데모: evidence-check 가 스펙-코드 드리프트를 잡는 모습](./assets/demo.gif)

코딩 에이전트는 주장을 합니다. SpecSeal 은 그 주장에 **도장**을 요구합니다 —
스펙을 실제로 읽지 않고는 찍을 수 없는 제작자 인장, 그것 없이는 어떤 커밋도
게이트를 못 넘는 warden 의 검인, 그리고 모든 조항이 근거 코드 좌표를 가리키는
원장. 코드는 움직였는데 원장이 그대로면, 빌드가 빨개집니다.

도장 없는 주장은 없다. 시험 없는 도장은 없다. 검인 없는 머지는 없다.

Claude Code **플러그인**으로 배포되며, 원장·드리프트 검사기·인계 규약은
git 이 있는 곳이면 어디서든 동작합니다.

## 상시 컨텍스트가 ~15줄인 이유

인장은 작아야 인장입니다. [arxiv 2602.11988](https://arxiv.org/abs/2602.11988)
에 따르면 컨텍스트 파일은 대체로 성공률을 높이지 못하면서 추론 비용만 20% 넘게
늘립니다. 모델은 SOLID 도 DRY 도 이미 알고 있습니다. SpecSeal 은 기본 동작을 실제로 바꾸는 것만 싣고,
나머지는 부를 때 로드되거나(스킬) 컨텍스트 밖에서 돕니다(훅).

## 문서청 사람들

| 누구/무엇 | 직무 |
|---|---|
| **smith** (에이전트) | 벼리는 자 — 만들고 다시 벼리고, 작업에 제작자 인장을 찍는다. 그 인장(증명 블록)은 스펙을 읽지 않고는 채울 수 없다 |
| **warden** (에이전트) | 검인관 — 스펙 준수부터 품질까지 시험하고, 통과해야만 커밋 게이트가 요구하는 검인을 내준다 |
| **scribe** (에이전트) | 필경사 — 판단 없이 충실히 옮긴다. 원본 코드가 실제로 하는 일을 좌표로 가져와 원장을 정직하게 지킨다 |
| 스킬 | 각 직무가 따르는 방법론 (`implement`, `code-review`, `legacy-parity`, `evidence-check`, `writing-style` + 품질 유틸) |
| 훅 | 게이트 그 자체 — 플러그인이 자동 등록, 설정 배선 불필요 |
| CLAUDE.md 블록 | 상시 로드가 불가피한 ~15줄 (언어·툴링·안전 규칙 둘·Git) |

## 체인

```
smith 가 벼린다 → verify → warden 이 시험한다 → 사용자에게 보고
      ↑                                            │
      └── 다시 벼리기 (사용자 지시) ← 사용자 판단
커밋   → 이번 사이클에 warden 의 검인이 있어야 통과 (훅 강제, 승인으로 우회 가능)
```

smith 가 벼려서 도장을 찍고, warden 이 검인을 내주고, scribe 가 원장을 지킵니다.

## 원장

세션을 넘는 기억은 세션이 아니라 저장소에 삽니다:

| 루트 | 수명 | 담는 것 |
|---|---|---|
| `docs/` | 영구 | 정책서, 근거 원장(스펙 조항 ↔ 코드 좌표), 후속 목록 |
| `specs/` | 작업 한 건 | SDD 세트: spec · plan · questions · 마감 overview |
| `_ai/` | 세션 사이 | 리뷰 회차·인계 목록 — 커밋되고, 배출 후 PR 단위로 삭제 |

없는 파일은 `templates/` 에서 부트스트랩됩니다. 인계 규약은
[docs/review-handoff-protocol.md](./docs/review-handoff-protocol.md) 에 도구
중립으로 명세되어 있어, git 레포에 파일을 읽고 쓸 수 있는 어떤 에이전트든
구현할 수 있습니다.

그리고 원장은 보관되는 것이 아니라 **검사**됩니다: `evidence-check` 스킬의
CI 스크립트가 스펙↔코드 좌표가 해석되지 않으면 빌드를 실패시키고, 기준 커밋
이후 손댄 범위는 재검증 대상으로 표시합니다. 다른 곳에서는 스펙이 조용히
썩지만, 여기서는 썩으면 빌드가 빨개집니다.

## 게이트

훅은 플러그인이 자동 등록하는 스크립트로, 도구 이벤트 때 사용자의 머신에서
실행됩니다. 판정표 전문:
[docs/worktree-guard-spec.md](./docs/worktree-guard-spec.md) ·
[docs/review-chain-spec.md](./docs/review-chain-spec.md)

| 게이트 | 언제 | 무엇을 | 어디서 |
|---|---|---|---|
| commit-review-gate | `git commit` 직전 | 사이클에 검인이 없으면 확인창 (`[no-review]` 로 흔적을 남기며 생략 가능) | 루트에 `_ai/` 있는 레포만 — 그 외 침묵 |
| review-history-guard | `gh` 로 PR 리뷰 게시/조회 직후 | `_ai/review-history/PR-n/` 쓰기/읽기 리마인드 | 같은 옵트인 |
| worktree-guard | 브랜치 전환·worktree 생성 직전 | 다른 **활성** 세션이 있으면 차단, 조용한 세션이면 벽 대신 질문 — 포렌식(호스트 앱·신호별 시각·마지막 메시지) 포함 | 모든 git 레포 |
| session-lease | 저장소를 건드리는 도구 호출(Bash·파일 편집) 직후 | "이 세션이 이 트리에서 일한다"를 `.git/specseal-leases/` 에 도장 — 추론 대신 선언 | 모든 git 레포 |
| lint-python | `.py` 저장 직후 | ruff 자동 포맷 (uv → uvx → 전역, 없으면 조용히 스킵) | 모든 프로젝트 |

어떤 게이트도 외부로 무언가를 보내지 않습니다 — 로컬 프로세스·git·파일
상태만 읽고 판정을 Claude Code 에 출력합니다. 다만 의도적으로 읽는 것이 하나
있습니다. worktree-guard 가 브랜치 전환을 막을 때, 지금 무엇을 보호하고 있는지
사람이 알아볼 수 있도록 다른 세션 기록에서 마지막 사용자 메시지 80자를 가져와
차단 사유에 함께 보여줍니다. 이 내용은 기기 안에만 머뭅니다.

## 원본에 대한 예우 (마이그레이션)

`docs/parity.md`(원본 저장소·기준 커밋)를 선언한 레포는 3자 판정 — 정책서 ↔
원본 ↔ 신규, 기본값은 **원본 보존** — 을 얻고, scribe 가 원본의 사실을
가져옵니다. 설정이 없는 레포에서는 존재 자체가 드러나지 않습니다.

## 치트시트

**저절로 도는 것: 위 게이트 전부 — 부를 필요 없음.**

**직접 부르는 것:**

| 명령 | 역할 |
|---|---|
| `python3 <플러그인>/skills/evidence-check/scripts/evidence_check.py . [--strict]` | 원장 드리프트 검사 (데모 GIF 의 그것) — 에이전트 없이 동작 |
| `/specseal:preset-setup` | CLAUDE.md 블록의 승인 기반 의미 병합 |
| `/specseal:security-audit` · `/specseal:testing` | 커버리지 체크리스트 |
| `bash install.sh [--project]` / `bash uninstall.sh` | CLAUDE.md 마커 블록 추가/제거 |

**명령에 섞는 스위치:**

| 스위치 | 효과 |
|---|---|
| 커밋 명령의 `[no-review]` | 리뷰 게이트 1회 생략 (흔적 남음) |
| worktree 명령의 `[worktree-ok]` | 단건 작업 worktree 거부를 확인창으로 완화 |
| `WORKTREE_GUARD_IDLE_MIN=n` | 유휴 판정 임계 분 (기본 5) |
| `SPECSEAL_LANG=ko\|en` | 게이트 문구 언어 (기본: 영어/시스템 로케일) |

## 설치

**요구사항**: `git`, 그리고 `python3`(PATH 에 잡혀 있어야 합니다). 게이트가
파이썬 스크립트라서 필요하며, macOS 와 대부분의 Linux 배포판에는 이미 깔려
있습니다. Windows 라면 Python 3 을 설치한 뒤 `python3` 명령으로 실행되는지
확인하세요. `uv`/`uvx` 나 `ruff` 는 파이썬 자동 포맷 훅에만 쓰이며, 없으면
그 훅만 건너뜁니다.

```bash
# 1. 플러그인 (에이전트 + 스킬 + 게이트)
claude
> /plugin marketplace add MichaelYcJo/SpecSeal
> /plugin install specseal@specseal

# 2. CLAUDE.md 블록 — 범위는 하나만 선택
bash install.sh            # 대화형: 전역(~/.claude) 또는 프로젝트(./)
bash install.sh --project  # 비대화형 프로젝트 범위
```

`install.sh` 는 `CLAUDE.md.bak` 으로 백업하고, 자기 마커 블록만 병합하며
(멱등 — 다시 실행하면 갱신), 사용자 본인의 내용은 절대 고치지 않습니다 —
겹침은 경고만 합니다. 중복까지 정리하는 병합은 Claude Code 안에서
`/specseal:preset-setup` 을 실행하세요. 모든 삭제가 승인 diff 를 거칩니다.

## 처음 실행

설치해도 당장은 아무 일도 일어나지 않습니다. 게이트는 옵트인한 레포에서만
깨어나고, 에이전트는 부를 때만 움직입니다.

```
> smith 에이전트로 <티켓> 구현해줘
```

smith 는 스펙 체인을 읽고 구현한 뒤 검증까지 마치고, 리뷰는 warden 에게
넘깁니다. 나온 리포트로 무엇을 할지 — 고칠지, 다시 리뷰할지, 커밋할지 — 는
사용자가 정합니다.

커밋 게이트와 리뷰 이력 리마인드를 켜려면 레포 루트에 `_ai/` 디렉터리를
만드세요(`mkdir _ai`). 나머지 문서 구조는 smith 가 처음 작업할 때
`templates/` 에서 만들어 둡니다.

에이전트가 없어도 쓸 수 있는 것이 둘 있습니다. 원장 드리프트
검사(`evidence_check.py`, 위 데모가 그것입니다)와 위 표의 게이트 전부입니다.

## 언어 정책

기능 파일(스킬·에이전트·훅·커맨드)은 영어 단일본입니다 — 모델 컨텍스트에
로드되는 파일이고, 번역 미러는 반드시 어긋나기 때문입니다. 한국어는 사람이
읽는 문서(이 README)에만 둡니다. 의도된 예외 하나: writing-style 스킬은
언어별 문장 규칙(한국어·영어 절)을 담는데, 이는 번역 미러가 아니라 각 언어의
독립 규범이라 드리프트 논리가 적용되지 않습니다. 응답 언어는 사용자 자신의 CLAUDE.md 설정을 따릅니다 — 배포되는 블록은
언어를 강제하지 않습니다.

## 라이선스

MIT
