# SpecSeal

[![tests](https://github.com/MichaelYcJo/SpecSeal/actions/workflows/test.yml/badge.svg)](https://github.com/MichaelYcJo/SpecSeal/actions/workflows/test.yml)

**Specs, sealed** — 스펙이 가리키는 코드가 바뀌면 CI 가 알려 줍니다.

![SpecSeal 데모: evidence-check 가 스펙-코드 드리프트를 잡는 모습](./assets/demo.gif)

코딩 에이전트는 다 됐다고 말합니다. SpecSeal 은 그 말이 열어 볼 수 있는 흔적을
남기게 합니다. 흔적은 셋입니다. smith 가 응답 끝에 적는 **증명 블록**(어떤 정책서를
읽었고 무엇을 실제로 실행했는지), 커밋 훅이 확인하는 **리뷰 표시**(`.git/specseal-reviewed`
에 적히는, 리뷰를 마친 시점의 HEAD sha), 그리고 정책 조항마다 근거가 되는 코드
위치를 짝지어 둔 **근거 대조표**(`docs/**/_evidence.md`)입니다.

리뷰 표시 없이 커밋하면 훅이 먼저 물어봅니다. 대조표가 가리키는 줄을 건드리면
검사 스크립트가 실패로 끝납니다. 둘 다 벽은 아니고, 알고 지나가게 만드는
기록입니다.

Claude Code **플러그인**으로 배포됩니다. 근거 대조표와 드리프트 검사기, 인계 규약은
git 이 있는 곳이면 어디서든 동작합니다.

## 상시 컨텍스트가 ~15줄인 이유

도장은 작아야 도장입니다. [arxiv 2602.11988](https://arxiv.org/abs/2602.11988) 에
따르면 컨텍스트 파일은 대체로 성공률을 높이지 못하면서 추론 비용만 20% 넘게
늘립니다. 모델은 SOLID 도 DRY 도 이미 알고 있습니다. SpecSeal 은 기본 동작을
실제로 바꾸는 것만 싣습니다. 나머지는 부를 때 로드되는 스킬이거나, 컨텍스트
밖에서 도는 훅입니다.

## 무엇이 들어 있나

| 누구/무엇 | 실제로 무엇인가 |
|---|---|
| **smith** (Claude Code 서브에이전트) | 스펙에 맞춰 구현한 뒤 증명 블록 세 줄을 적는다. 어떤 정책서를 열었는지, 어떤 대조표 행을 고쳤는지, 무엇을 실행하고 무엇을 읽기만 했는지. 훅이 검사하는 것이 아니라 스킬이 요구하는 공개이며, `none — <이유>` 로 채워진 줄은 사용자 눈에 그대로 보인다 |
| **warden** (서브에이전트) | 스펙 준수를 먼저 보고 그다음 품질을 본다. 통과하면 리뷰 시점의 HEAD sha 를 `.git/specseal-reviewed` 에 적고, 커밋 게이트는 그 파일을 확인한다 |
| **scribe** (서브에이전트) | 원본 코드가 실제로 하는 일을 `file:line` 좌표로 기록하고, 판정이 아니라 사실만 돌려준다. `docs/parity.md` 를 선언한 레포에서만 등장한다 |
| 스킬 | 각자가 따르는 방법론 (`implement`, `code-review`, `legacy-parity`, `evidence-check`, `writing-style` + 품질 유틸) |
| 훅 | 게이트 그 자체. 플러그인이 자동으로 등록하므로 설정을 따로 만질 필요가 없다 |
| CLAUDE.md 블록 | 늘 로드되는 12줄 — 툴링 선호, 안전 규칙 두 가지, git 규칙 하나. 응답 언어 규칙은 없다. 그것은 사용자 몫이다 |

## 체인

```
smith 가 벼린다 → verify → warden 이 시험한다 → 사용자에게 보고
      ↑                                            │
      └── 다시 벼리기 (사용자 지시) ← 사용자 판단
커밋   → .git/specseal-reviewed 가 HEAD 와 다르면 훅이 물어본다. 승인이 곧 면제다
```

smith 가 만들고 증명 블록을 적고, warden 이 리뷰 표시를 내주고, scribe 가 대조표를 채웁니다.

## 저장소에 남는 기억

세션이 끝나도 남아야 하는 것은 세션이 아니라 저장소에 적습니다.

| 루트 | 수명 | 담는 것 |
|---|---|---|
| `docs/` | 영구 | 정책서, 근거 대조표(정책 조항 ↔ 코드 좌표), 후속 목록 |
| `specs/` | 작업 한 건 | SDD 문서 한 벌 — spec · plan · questions · 마감 overview |
| `_ai/` | 세션 사이 | 리뷰 회차와 인계 목록. 커밋해 두었다가 다 옮기고 나면 PR 단위로 지운다 |

없는 파일은 `templates/` 에서 만들어집니다. 인계 규약은
[docs/review-handoff-protocol.md](./docs/review-handoff-protocol.md) 에 특정
도구를 전제하지 않고 적혀 있습니다. git 레포의 파일을 읽고 쓸 수 있는
에이전트라면 무엇이든 그대로 따를 수 있습니다.

대조표는 쌓아 두기만 하는 것이 아니라 **검사**받습니다. `evidence-check` 스킬의
CI 스크립트는 좌표가 더 이상 풀리지 않으면 2 로, 기준 커밋 이후 그 줄이 바뀌었으면
1 로 끝납니다. 기본 CI 설정에서는 둘 다 실패로 잡히고, `--strict` 를 주면 드리프트도
2 가 됩니다. 이 검사가 증명하는 범위는 좁습니다. 인용한 좌표가 아직 유효하다는
것이지, 그 좌표가 뒷받침하는 주장이 여전히 맞다는 뜻은 아닙니다. 다른 곳에서는
스펙이 조용히 낡아 가지만, 여기서는 낡는 순간 CI 에 드러납니다.

## 게이트

훅은 플러그인이 자동으로 등록하는 스크립트이며, 도구를 호출하는 시점에
사용자 컴퓨터에서 실행됩니다. 판정표 전문은 다음 두 문서에 있습니다.
[docs/worktree-guard-spec.md](./docs/worktree-guard-spec.md) ·
[docs/review-chain-spec.md](./docs/review-chain-spec.md)

| 게이트 | 언제 | 무엇을 | 어디서 |
|---|---|---|---|
| commit-review-gate | `git commit` 직전 | `.git/specseal-reviewed` 가 현재 HEAD 와 다르면 물어본다 (`[no-review]` 를 넣으면 건너뛰고, 그 표시가 명령에 그대로 남는다) | 루트에 `_ai/` 가 있는 레포에서만 동작하고, 그 밖에서는 아무것도 하지 않는다 |
| review-history-guard | `gh` 로 PR 리뷰 게시/조회 직후 | `_ai/review-history/PR-n/` 에 쓰거나 읽으라고 알린다 | 위와 같이 `_ai/` 가 있는 레포만 |
| worktree-guard | `git checkout`·`switch`·`worktree add` 와 `isolation: "worktree"` 로 부른 Agent 직전 | 한 규칙의 두 방향이다. 다른 세션이 이 트리에서 작업 중이면 전환을 막고, 반대로 혼자 작업 중이면 worktree 생성을 막는다(`[worktree-ok]` 를 넣으면 확인창으로 낮아진다). 멈춘 세션이거나 판정이 불가능한 환경이면 막지 않고 물어본다. 사유에는 상대 세션의 호스트 앱, 신호별 경과 시간, 마지막 메시지가 함께 나온다 | 모든 git 레포 |
| session-lease | 저장소를 건드리는 도구 호출(Bash·파일 편집) 직후 | `.git/specseal-leases/<세션id>` 에 시각을 적는다. 프로세스 이름이 `claude` 가 아닌 세션은 가드가 놓치는데, lease 는 어느 세션이 여기서 일하는지 그냥 밝혀 준다 | 모든 git 레포 |
| lint-python | `.py` 파일을 Write·Edit·NotebookEdit 한 직후 | 그 파일에 `ruff check --fix` 를 돌린 뒤 `ruff format` 을 돌린다. 린트 자동수정이 포함되므로 내용이 바뀔 수 있다 (uv → uvx → 전역 순으로 찾고, 없으면 건너뛴다) | 모든 프로젝트 |

어떤 게이트도 사용자의 코드나 프롬프트를 바깥으로 보내지 않습니다. 다만 두 가지
부수 효과는 밝혀 둡니다. session-lease 는 `.git/specseal-leases/` 아래에 시각
파일을 쓰고, lint-python 은 방금 저장한 `.py` 파일을 고쳐 씁니다. 네트워크를 탈
수 있는 훅도 lint-python 하나뿐입니다. `uvx ruff` 로 넘어가면 uv 가 처음 한 번
PyPI 에서 ruff 를 내려받습니다.

일부러 읽는 것도 하나 있습니다. worktree-guard 가 브랜치 전환을 막을 때, 지금 무엇을 보호하는지
사람이 알아볼 수 있게 다른 세션 기록에서 마지막 사용자 메시지 80자를 가져옵니다.
이 조각은 차단 사유에만 쓰이고 기기 밖으로 나가지 않습니다.

## 원본을 기준으로 삼기 (마이그레이션)

`docs/parity.md` 에 원본 저장소와 기준 커밋을 적어 두면 3자 판정을 쓸 수
있습니다. 정책서와 원본, 신규 코드를 나란히 놓고 판정하며, 판단이 갈리면
**원본을 보존하는 쪽**이 기본값입니다. 이때 scribe 가 원본이 실제로 어떻게
동작하는지 확인해 옵니다. 이 파일이 없는 레포에서는 이 기능이 아예
나타나지 않습니다.

## 치트시트

**저절로 도는 것** — 위 게이트는 전부 알아서 돌기 때문에 따로 부르지 않아도 됩니다.

**직접 부르는 것:**

| 명령 | 역할 |
|---|---|
| `python3 <플러그인>/skills/evidence-check/scripts/evidence_check.py . [--strict]` | 대조표의 좌표가 아직 살아 있는지 검사한다(데모 GIF 에 나오는 그 검사). 에이전트 없이 동작한다 |
| `/specseal:preset-setup` | CLAUDE.md 블록을 승인받아 뜻 단위로 병합한다 |
| `/specseal:security-audit` · `/specseal:testing` | 모델이 훑는 점검 목록 — OWASP 형태의 보안 점검과 테스트 전략 점검 |
| `bash install.sh [--project]` / `bash uninstall.sh` | CLAUDE.md 마커 블록을 넣거나 뺀다 |

**명령에 섞는 스위치:**

| 스위치 | 효과 |
|---|---|
| 커밋 명령의 `[no-review]` | 리뷰 게이트를 한 번 건너뛴다. 명령에 그대로 남아 흔적이 된다 |
| worktree 명령의 `[worktree-ok]` | 혼자 작업할 때 worktree 생성을 막던 것을 확인창으로 완화한다 |
| `WORKTREE_GUARD_IDLE_MIN=n` | 세션을 멈춘 것으로 볼 기준 시간, 분 단위 (기본 5) |
| `SPECSEAL_LANG=ko\|en` | worktree-guard 문구의 언어 (나머지 게이트는 영어만 나옵니다). 기본은 시스템 로케일을 따릅니다 |

## 설치

**요구사항**은 `git` 과 `python3` 두 가지이며, `python3` 은 PATH 에 잡혀
있어야 합니다. 게이트가 파이썬 스크립트이기 때문입니다. macOS 와 대부분의
Linux 배포판에는 이미 깔려 있습니다. Windows 라면 Python 3 을 설치한 뒤
`python3` 명령으로 실행되는지 확인하세요. `uv`/`uvx` 나 `ruff` 는 파이썬 자동
포맷 훅에만 쓰이고, 없으면 그 훅만 건너뜁니다.

```bash
# 1. 플러그인 (에이전트 + 스킬 + 게이트)
claude
> /plugin marketplace add MichaelYcJo/SpecSeal
> /plugin install specseal@specseal

# 2. CLAUDE.md 블록 — 범위는 하나만 선택
bash install.sh            # 대화형: 전역(~/.claude) 또는 프로젝트(./)
bash install.sh --project  # 비대화형 프로젝트 범위
```

`install.sh` 는 기존 파일을 `CLAUDE.md.bak` 으로 백업한 뒤 자기 마커 블록만
병합합니다. 여러 번 실행해도 결과가 같고, 다시 실행하면 블록만 갱신됩니다.
사용자가 직접 쓴 내용은 고치지 않으며, 겹치는 부분이 있으면 경고만 남긴 채
그대로 둡니다. 중복까지 정리하려면 Claude Code 안에서
`/specseal:preset-setup` 을 실행하세요. 무엇을 지우든 diff 를 보여 주고
승인을 받습니다.

## 처음 실행

켜야 도는 게이트는 둘입니다. 커밋 게이트와 리뷰 이력 알림은 레포 루트에 `_ai/`
디렉터리가 생기기 전까지 침묵합니다. 나머지 셋은 그렇지 않습니다. worktree-guard
와 session-lease 는 모든 git 레포에서 동작하고, lint-python 은 저장하는 모든 `.py`
파일을 고쳐 씁니다. 전역으로 설치하기 전에 위 표의 "어디서" 열을 먼저 보세요.

에이전트는 이름을 불러야 움직입니다.

```
> specseal:smith 에이전트로 <티켓> 구현해줘
```

smith 는 스펙 체인을 읽고 구현한 뒤 검증까지 마치고, 리뷰는 warden 에게
넘깁니다. 나온 리포트를 어떻게 할지는 사용자가 정합니다. 고칠 수도, 다시
리뷰를 돌릴 수도, 그대로 커밋할 수도 있습니다.

커밋 게이트와 리뷰 이력 알림을 켜려면 레포 루트에 `_ai/` 디렉터리를
만드세요(`mkdir _ai`). 나머지 문서 구조는 smith 가 처음 작업할 때
`templates/` 에서 만들어 둡니다.

에이전트를 쓰지 않아도 되는 기능이 두 가지 있습니다. 앞의 데모에서 보여 준
대조표 검사(`evidence_check.py`)와, 위 표에 적은 게이트 전부입니다.

## 언어 정책

기능 파일(스킬·에이전트·훅·커맨드)은 영어 하나로만 씁니다. 모델 컨텍스트에
로드되는 파일이라, 번역본을 따로 두면 반드시 원본과 어긋나기 때문입니다.
한국어는 사람이 읽는 문서에만 둡니다. 일부러 둔 예외가 하나 있습니다.
writing-style 스킬은 한국어 항목과 영어 항목을 따로 담는데, 이는 서로를 옮긴
번역본이 아니라 각 언어의 독립된 규범이라 앞의 어긋남 문제가 해당되지
않습니다. 응답 언어는 사용자 자신의 CLAUDE.md 설정을 따르며, 배포되는 블록은
언어를 강제하지 않습니다.

## 라이선스

MIT
