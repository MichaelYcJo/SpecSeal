# claude_preset

리서치 기반의 최소주의 Claude Code 프리셋. 일반적인 프리셋 대비 **always-loaded 토큰 81% 절감**.

[English](./README.md)

## 왜 필요한가

[arxiv 2602.11988](https://arxiv.org/abs/2602.11988) 논문 기반:
- Context 파일이 태스크 성공률을 ~2% **감소**시킬 수 있음
- 불필요한 지시로 추론 비용 20-23% **증가**
- Claude는 이미 SOLID, DRY, "수정 전 읽기" 등을 알고 있음
- **Claude의 기본 동작을 바꾸는 것만 포함해야 함**

## 구성 요소

| 구성 | 수량 | 설명 |
|------|------|------|
| CLAUDE.md | 1 | 항상 로드 (~350 토큰). 언어, 도구, 안전 규칙 |
| Rules | 4 | 컨텍스트 기반 로드. 엔지니어링, 안전, 워크플로우, 오케스트레이션 |
| Skills | 10 | idle 시 0 토큰. 키워드 자동 트리거 |
| Commands | 20 | 특정 작업용 슬래시 커맨드 |
| Agents | 8 | 전문 워커 템플릿 |

### Always-Loaded (CLAUDE.md, ~350 토큰)

**Claude의 기본 동작을 바꾸는** 규칙만 포함:
- 한국어 응답
- `uv`/`pnpm` 선호
- 엔지니어링 기본 원칙 리마인더 (SOLID, DRY, KISS — 1줄)
- 3+ Fix Rule (동일 버그 3회 수정 실패 시 중단)
- Verification Gate (증거 없이 완료 주장 금지)
- Two-Stage Review (스펙 준수 → 코드 품질)
- Orchestrator/Worker 에이전트 패턴
- 스킬 자동 트리거 규칙

### Rules (컨텍스트 기반 로드, idle 시 0 토큰)

| 파일 | 용도 |
|------|------|
| `safety.md` | 3+ Fix Rule 상세, Verification Gate 상세, 보안 체크리스트 |
| `quality.md` | SOLID/DRY/KISS 상세, 구현 완전성, 스코프 규율 |
| `orchestration.md` | Orchestrator/Worker 역할 분리, 에이전트 템플릿, 모델 선택 |
| `workflow.md` | Two-Stage Review 상세, PDCA, 병렬 계획, Git 워크플로우 |

### Skills (자동 트리거)

| 스킬 | 트리거 | 용도 |
|------|--------|------|
| `/confidence-check` | implement, create, build | 구현 전 신뢰도 평가 |
| `/verify` | done, complete, PR | 완료 후 검증 |
| `/build-fix` | build errors | 빌드 에러 체계적 해결 |
| `/checkpoint` | refactor, delete, migrate | 위험 작업 전 안전 체크포인트 |
| `/debug` | test failures | 체계적 디버깅 |
| `/code-review` | review request | 심각도 기반 코드 리뷰 |
| `/learn` | problem solved | 문제 해결 인사이트 기록 |
| `/feature-planner` | new feature (>3 files) | 기능 구현 계획 |
| `/gap-analysis` | design vs implementation | 설계-구현 비교 분석 |
| `/audit` | commit, PR | 프로젝트 규칙 검증 |

### Commands

| 카테고리 | 커맨드 |
|----------|--------|
| 분석 | `/debug`, `/code-review`, `/code-smell` |
| 아키텍처 | `/architecture`, `/api-design`, `/db-design` |
| 품질 | `/testing`, `/refactoring`, `/clean-code` |
| 보안 | `/security-audit`, `/auth` |
| 프레임워크 | `/nextjs`, `/fastapi`, `/react-best-practices` |
| 인프라 | `/docker`, `/cicd`, `/monitoring` |
| 기타 | `/naming`, `/error-handling`, `/python-best-practices` |

### Agents

| 에이전트 | 역할 |
|---------|------|
| `backend-architect` | API, DB, 서버 설계 |
| `frontend-architect` | UI/UX, 컴포넌트 아키텍처 |
| `system-architect` | 시스템 수준 아키텍처 |
| `security-engineer` | 보안 검토 |
| `quality-engineer` | 테스트, QA |
| `python-expert` | Python 전문 |
| `performance-engineer` | 성능 최적화 |
| `technical-writer` | 기술 문서 |

## 설치

```bash
git clone https://github.com/USERNAME/claude_preset.git
cd claude_preset
bash install.sh
```

설치 프로그램 동작:
1. 기존 `~/.claude/` 설정 백업
2. CLAUDE.md, rules, skills, commands, agents 설치
3. `settings.json`에 훅 병합 (기존 설정 보존)

## 제거

```bash
bash uninstall.sh
```

현재 설정을 백업하고 이전 설정 복원을 제안합니다.

## 설계 철학

> "Claude가 이걸 기본으로 하나?"

CLAUDE.md의 모든 줄은 이 테스트를 통과합니다. Claude가 이미 아는 것(Python snake_case, "feature branch 사용" 등)은 포함하지 않습니다. Claude의 기본 동작을 바꾸는 행동 오버라이드만 남깁니다.

Claude가 "알지만 항상 적용하지는 않는" 원칙들(SOLID, DRY 등)은 CLAUDE.md에 1줄 리마인더로 유지하고, 상세 규칙은 `rules/` 디렉토리에서 컨텍스트에 따라 로드합니다. **설명은 빼고, 지시만 남기는** 접근입니다.

### 포함/제외 기준

| 포함 (하나라도 해당 시) | 제외 (하나라도 해당 시) |
|---|---|
| 기본 동작을 바꾸는 지시 | 시스템 프롬프트에 이미 내장 |
| 구체적 임계값/기준 | 언어/프레임워크 기본 컨벤션 |
| 고유한 워크플로우 | "설명"형 지시 (해로움) |
| | 린터/포맷터가 할 수 있는 것 |

근거 자료: [RESEARCH.ko.md](./RESEARCH.ko.md) | [English](./RESEARCH.md)

## 구조

```
claude_preset/
├── CLAUDE.md              # 매 세션 자동 로드되는 핵심 설정 (~350 토큰)
├── rules/                 # 상황에 따라 자동 로드되는 행동 규칙 (idle 시 0 토큰)
│   ├── safety.md          #   버그 수정 한계, 완료 검증, 보안 규칙
│   ├── quality.md         #   코드 품질 원칙 (SOLID, DRY 등), 스코프 관리
│   ├── orchestration.md   #   에이전트 역할 분리, 템플릿, 모델 선택 기준
│   └── workflow.md        #   리뷰 프로세스, PDCA 사이클, Git 워크플로우
├── skills/                # 키워드 감지 시 자동 실행되는 스킬 (idle 시 0 토큰)
│   ├── confidence-check/  #   구현 전 신뢰도 평가 (implement/create/build)
│   ├── verify/            #   완료 후 검증 게이트 (done/complete/PR)
│   ├── build-fix/         #   빌드 에러 체계적 해결
│   ├── checkpoint/        #   위험 작업 전 안전 체크포인트
│   ├── debug/             #   체계적 디버깅 (4단계 프로세스)
│   ├── code-review/       #   심각도 기반 코드 리뷰
│   ├── learn/             #   문제 해결 인사이트 기록
│   ├── feature-planner/   #   기능 구현 계획 (>3파일 시)
│   ├── gap-analysis/      #   설계 vs 구현 비교 분석
│   └── audit/             #   프로젝트 규칙 자동 검증
├── commands/              # /슬래시명령어로 실행하는 전문 도구 (20개)
│   ├── debug.md           #   분석: 디버깅, 코드리뷰, 코드스멜
│   ├── architecture.md    #   설계: 아키텍처, API, DB
│   ├── testing.md         #   품질: 테스트, 리팩토링, 클린코드
│   ├── security-audit.md  #   보안: 보안감사, 인증/인가
│   ├── nextjs.md          #   프레임워크: Next.js, FastAPI, React
│   └── ...                #   인프라: Docker, CI/CD, 모니터링 등
├── agents/                # Task tool로 스폰되는 전문 에이전트 (8개)
│   ├── backend-architect.md    # API/DB/서버 설계 전문
│   ├── frontend-architect.md   # UI/UX/컴포넌트 설계 전문
│   ├── system-architect.md     # 시스템 아키텍처 전문
│   ├── security-engineer.md    # 보안 검토 전문
│   ├── quality-engineer.md     # 테스트/QA 전문
│   ├── python-expert.md        # Python 개발 전문
│   ├── performance-engineer.md # 성능 최적화 전문
│   └── technical-writer.md     # 기술 문서 작성 전문
├── scripts/               # 훅에서 실행되는 자동화 스크립트
├── templates/             # settings.json 등 설정 템플릿
├── install.sh             # 설치 (백업 + 기존 @import 파일 정리 포함)
└── uninstall.sh           # 제거 (백업 + 이전 설정 복원 지원)
```

## 사용 예시

### 스킬 (자동 트리거 — 직접 호출 불필요)

```
> 로그인 기능 만들어줘

# Claude가 "만들어" 키워드를 감지 → /confidence-check 자동 실행
Confidence: 85%
✅ No duplicate exists
✅ Architecture compliant (Next.js App Router)
⚠️ Official docs — NextAuth v5 breaking changes 미확인
✅ Working reference found
Recommendation: NextAuth v5 마이그레이션 가이드 확인 후 진행
```

```
> 다 됐어, PR 올려줘

# Claude가 "됐어" + "PR" 감지 → /verify 자동 실행
Verification: PASS
Command: pnpm test && pnpm build
Evidence: Tests 23 passed, 0 failed. Build exit 0.
```

### 슬래시 커맨드 (직접 호출)

```
> /code-review src/auth/

## Review: src/auth/

**Critical** (1)
- src/auth/session.ts:42 — JWT secret hardcoded → use env var

**Important** (2)
- src/auth/login.ts:18 — missing rate limiting → add express-rate-limit
- src/auth/middleware.ts:7 — no token expiry check → verify exp claim

**Good**: Clean separation of auth logic from routes
**Verdict**: Request Changes
```

```
> /architecture 알림 시스템 설계해줘

## Architecture: 알림 시스템

**Requirements**: 실시간 알림, 이메일/푸시/인앱, 사용자별 설정

**Options**:
1. Polling — 단순, 실시간성 낮음 / 서버 부하
2. WebSocket — 실시간, 양방향 / 연결 관리 복잡
3. SSE + Queue — 실시간, 단방향 / 인프라 추가 필요

**Recommendation**: SSE + Redis Queue
```

```
> /debug 테스트 3개 실패하는데 원인 찾아줘

Bug: UserService.getProfile() returns null for OAuth users
Root cause: OAuth users have no `password` field → findOne query
  implicitly filters by password existence
Fix: Changed query to findOne({ id }) without password condition
Verification: 3 tests now passing
```

### 에이전트 (복잡한 작업 시 자동 스폰)

```
> 결제 시스템 보안 검토해줘

# Claude가 보안 + 검토 감지 → security-engineer 에이전트 스폰

## Security Review: 결제 시스템

**Critical** (2)
- src/payment/charge.ts:34 — SQL injection via orderId
- src/payment/webhook.ts:12 — Stripe signature 미검증

**High** (1)
- src/payment/refund.ts:8 — 금액 음수 검증 없음

**Recommendations**: Stripe webhook signature 검증 추가,
  parameterized queries 적용, 금액 범위 validation
```


## License

MIT
