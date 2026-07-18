# SpecSeal

연구 근거 기반의 미니멀 Claude Code 프리셋 — **플러그인**으로 배포됩니다.
구현 → 리뷰 에이전트 체인, 세션을 넘어 살아남는 문서 레이아웃, 그 사이를
기계적으로 강제하는 훅으로 구성됩니다.

[English](./README.md)

## 상시 로드 컨텍스트를 최소로 두는 이유

[arxiv 2602.11988](https://arxiv.org/abs/2602.11988) 근거: 중복된 컨텍스트
파일은 오히려 작업 성공률을 낮추고 추론 비용을 늘립니다. SOLID·DRY·"수정 전
읽기"는 Claude 가 이미 아는 것입니다. 이 프리셋은 기본 동작을 실제로 바꾸는
것만 싣고, 나머지는 필요할 때만 로드되거나(스킬) 컨텍스트 밖에서 돕니다(훅).

## 구성

| 컴포넌트 | 역할 |
|---|---|
| **에이전트** — `developer` · `code-reviewer` · `parity-checker` | Who: 구현·리뷰·마이그레이션 사실 확인을 별도 컨텍스트로 분리, 각자 방법론 스킬을 사전 로드 |
| **스킬** — `implement` · `code-review` · `legacy-parity` · `evidence-check` + 품질 유틸(`verify`, `audit`, `debug`, …) | How: 트리거될 때만 로드되는 절차 |
| **훅** — commit-review-gate · review-history-guard · worktree-guard · lint-python | When: 기계적 강제. 플러그인이 자동 등록 (settings.json 배선 불필요) |
| **CLAUDE.md 블록** | 상시 로드가 불가피한 ~15줄 (언어·툴링·안전 규칙 둘·Git) |

### 체인

```
developer 구현 → verify → code-reviewer 리뷰 → 리포트 보고
       ↑                                          │
       └── 수정 (사용자 지시) ← 사용자 판단 ←──────┘
커밋   → 사이클에 리뷰 마크가 있어야 통과 (훅 강제, 승인으로 우회 가능)
```

세션 간 연속성은 세션이 아니라 저장소에 둡니다.

| 루트 | 수명 | 담는 것 |
|---|---|---|
| `docs/` | 영구 | 정책서, 근거 원장(스펙 조항 ↔ 코드 좌표), 후속 목록 |
| `specs/` | 작업 한 건 | SDD, overview |
| `_ai/` | 세션 사이 | 리뷰 회차 기록·인계 목록 — 커밋되고, 배출 후 PR 단위로 삭제 |

없는 파일은 `templates/` 에서 자동 생성됩니다. 인계 규약 자체는
[docs/review-handoff-protocol.md](./docs/review-handoff-protocol.md) 에 도구
중립적으로 명세되어 있어, git 레포에 파일을 읽고 쓸 수 있는 어떤 에이전트든
구현할 수 있습니다.

그리고 원장은 보관만 하는 것이 아니라 **검사**됩니다: `evidence-check` 스킬이
CI 용 스크립트를 동봉해, 스펙↔코드 좌표가 더 이상 해석되지 않으면 빌드를
실패시키고, 기준 커밋 이후 손댄 범위는 재검증 대상으로 표시합니다. 다른
곳에서는 스펙이 조용히 썩지만, 여기서는 썩으면 빌드가 빨개집니다.

### 훅이 하는 일

훅은 플러그인이 자동 등록하는 스크립트로, 특정 도구 이벤트 때 사용자의 머신에서
실행됩니다. 판정표 전체는 [docs/worktree-guard-spec.md](./docs/worktree-guard-spec.md)
와 [docs/review-chain-spec.md](./docs/review-chain-spec.md) 에 있습니다.

| 훅 | 언제 | 무엇을 | 적용 범위 |
|---|---|---|---|
| commit-review-gate | `git commit` 직전 | 사이클에 리뷰 마크가 없으면 확인창 (`[no-review]` 로 생략 가능) | 루트에 `_ai/` 가 있는 레포만 — 그 외에는 침묵 |
| review-history-guard | `gh` 로 PR 리뷰를 게시/조회한 직후 | `_ai/review-history/PR-n/` 쓰기/읽기 리마인드 | 같은 `_ai/` 옵트인 |
| worktree-guard | 브랜치 전환·worktree 생성 직전 | 다른 **활성** 세션이 있으면 전환 차단; 입력·출력·트랜스크립트가 모두 조용한 세션은 잊힌 탭으로 보고 확인창만 | 모든 git 레포 |
| lint-python | `.py` 파일 저장/수정 직후 | ruff 자동 포맷·수정 (uv → uvx → 전역 ruff, 없으면 조용히 스킵) | 모든 프로젝트 |

어떤 훅도 외부로 무언가를 보내지 않습니다 — 로컬 프로세스·git·파일 상태만 읽고
판정을 Claude Code 에 출력합니다.

### 마이그레이션

`docs/parity.md`(원본 저장소·기준 커밋)를 선언한 레포는 3자 판정(정책서 ↔
원본 ↔ 신규, 기본값은 **원본 보존**)과 원본 사실 확인 전담 `parity-checker`
를 얻습니다. 설정이 없는 레포에서는 존재 자체가 드러나지 않습니다.

## 설치

```bash
# 1. 플러그인 (스킬 + 에이전트 + 훅 + 커맨드)
claude
> /plugin marketplace add MichaelYcJo/specseal
> /plugin install specseal

# 2. CLAUDE.md 블록 — 범위는 하나만 선택
bash install.sh            # 대화형: 전역(~/.claude) 또는 프로젝트(./)
bash install.sh --project  # 비대화형 프로젝트 범위
```

`install.sh` 는 `CLAUDE.md.bak` 으로 백업하고, 자기 마커 블록만 병합하며
(멱등 — 다시 실행하면 갱신), 사용자 본인의 내용은 절대 고치지 않습니다 —
겹침은 경고만 합니다. 중복까지 정리하는 병합은 Claude Code 안에서
`/preset-setup` 을 실행하세요. 모든 삭제가 승인 diff 를 거칩니다.

## 언어 정책

기능 파일(스킬·에이전트·훅·커맨드)은 영어 단일본입니다 — 모델 컨텍스트에
로드되는 파일이고, 번역 미러는 반드시 어긋나기 때문입니다. 한국어는 사람이
읽는 문서(이 README)에만 둡니다. 의도된 예외 하나: writing-style 스킬은
언어별 문장 규칙(한국어·영어 절)을 담는데, 이는 번역 미러가 아니라 각 언어의
독립 규범이라 드리프트 논리가 적용되지 않습니다. 응답 언어는 CLAUDE.md
블록이 정하므로 지시문 언어와 무관합니다.

## 라이선스

MIT
