# 리서치: Claude Code 기본 동작 분석

조사 날짜: 2026-02-26 (v2.1.58 기준)

## 출처

- [Anthropic Best Practices](https://code.claude.com/docs/en/best-practices)
- [HumanLayer - Writing a Good CLAUDE.md](https://www.humanlayer.dev/blog/writing-a-good-claude-md)
- [Piebald-AI/claude-code-system-prompts](https://github.com/Piebald-AI/claude-code-system-prompts) — v2.1.58, 225+ 파일
- [arxiv 2602.15228 - System Prompts in Code Generation](https://arxiv.org/abs/2602.15228)
- [arxiv 2509.14744 - Agentic Coding Manifests](https://arxiv.org/abs/2509.14744)
- [Arize - CLAUDE.md Optimization](https://arize.com/blog/claude-md-best-practices-learned-from-optimizing-claude-code-with-prompt-learning/)

---

## 1. Anthropic 공식 CLAUDE.md 가이드라인

### 포함할 것
- Claude가 추측 못 하는 Bash 명령어
- **기본값과 다른** 코드 스타일 규칙
- 테스트 러너, 빌드 명령
- 프로젝트 고유 아키텍처 결정
- 환경 quirks, 비직관적 동작

### 제외할 것
- 코드 읽으면 알 수 있는 것
- Claude가 이미 아는 언어 컨벤션
- 상세 API 문서 (링크로 대체)
- 자주 변하는 정보
- "write clean code" 같은 자명한 실천

### 핵심 인용
> "Claude가 지시 없이도 올바르게 수행하는 것이라면, 삭제하거나 hook으로 변환하세요."
> "비대한 CLAUDE.md 파일은 Claude가 실제 지시를 무시하게 만듭니다!"

---

## 2. Claude Code 시스템 프롬프트 상세 분석

출처: [Piebald-AI/claude-code-system-prompts](https://github.com/Piebald-AI/claude-code-system-prompts) v2.1.58

시스템 프롬프트는 단일 블록이 아니라 **225+ 조건부 파일**로 구성된 모듈 아키텍처:
- Agent Prompts 29개
- Data References 26개
- System Prompts 50+개
- System Reminders 40+개
- Tool Descriptions 50+개 (Bash만 47 fragments)

### 2.1 코드 품질 (5개 독립 프래그먼트)

| 프래그먼트 | 정확한 문구 (원문) |
|---|---|
| **Avoid over-engineering** | "Only make changes that are directly requested or clearly necessary. Keep solutions simple and focused." |
| **No unnecessary additions** | "Don't add features, refactor code, or make 'improvements' beyond what was asked. Don't add docstrings, comments, or type annotations to code you didn't change." |
| **No unnecessary error handling** | "Don't add error handling, fallbacks, or validation for scenarios that can't happen. Trust internal code and framework guarantees. Only validate at system boundaries." |
| **No premature abstractions** | "Don't create helpers, utilities, or abstractions for one-time operations. Don't design for hypothetical future requirements. Three similar lines of code is better than a premature abstraction." |
| **No compatibility hacks** | "If you are certain that something is unused, you can delete it completely." |

→ **결론**: KISS, YAGNI, "scope 유지"의 핵심이 이미 5개 프래그먼트에 분산 내장. CLAUDE.md에서 이것들을 상세히 반복할 필요 없음.

### 2.2 파일 작업

| 행동 | 내장 문구 |
|---|---|
| Read before Edit | "Do not propose changes to code you haven't read. Read it first." |
| Minimize file creation | "Do not create files unless they're absolutely necessary. Generally prefer editing an existing file." |
| No README auto-creation | "NEVER proactively create documentation files (*.md) or README files." |
| Software engineering context | "When given an unclear or generic instruction, consider it in the context of software engineering tasks." |

### 2.3 Git 워크플로우 (8+ 프래그먼트, 매우 상세)

| 행동 | 내장 문구 |
|---|---|
| Commit only when asked | "Only create commits when requested by the user. If unclear, ask first." |
| NEVER update git config | 명시적 금지 |
| No destructive ops | "NEVER run destructive git commands (push --force, reset --hard, checkout .) unless the user explicitly requests" |
| Never skip hooks | "NEVER skip hooks (--no-verify, --no-gpg-sign, etc)" + "If a hook fails, investigate and fix the underlying issue." |
| Prefer new commits | "ALWAYS create NEW commits rather than amending" |
| Specific files staging | "prefer adding specific files by name rather than 'git add -A'" |
| No force push to main | "NEVER run force push to main/master, warn the user" |
| Co-Authored-By | 조건부 변수 (`COMMIT_CO_AUTHORED_BY_CLAUDE_CODE`), 설정에 따라 포함/미포함 |
| PR creation | gh CLI 사용, HEREDOC 형식, 상세 워크플로우 포함 |

→ **결론**: Git 안전 규칙이 시스템 프롬프트에서 가장 상세한 영역 중 하나. CLAUDE.md에서 "Feature branches", "don't skip hooks" 등은 완전히 불필요. "No Co-Authored-By"만 오버라이드 가치 있음.

### 2.4 보안

| 행동 | 내장 문구 |
|---|---|
| OWASP Top 10 방지 | "Be careful not to introduce security vulnerabilities such as command injection, XSS, SQL injection" |
| 즉시 수정 | "If you notice that you wrote insecure code, immediately fix it" |
| Secrets 방지 | "Do not commit files that likely contain secrets (.env, credentials.json, etc)" |
| 보안 리뷰 | `/security-review` slash command 내장 (2610 tokens) |

### 2.5 커뮤니케이션 스타일

| 행동 | 내장 문구 |
|---|---|
| 간결함 | "Your responses should be short and concise." |
| Filler 금지 | "Avoid using filler words, repetition, or restating what the user has already said." |
| 이모지 금지 | "Only use emojis if the user explicitly requests it." |
| 코드 참조 | "Include the pattern file_path:line_number" |
| 시간 추정 금지 | "Avoid giving time estimates or predictions" |
| Inner monologue 숨김 | "Avoid sharing your thinking or inner monologue in your output" |

### 2.6 도구 사용

| 행동 | 내장 문구 |
|---|---|
| 전용 도구 우선 | "Do NOT use Bash to run commands when a relevant dedicated tool is provided" (Read > cat, Edit > sed, Grep > grep, Glob > find) |
| 병렬 호출 | "Make all independent tool calls in parallel" |
| Blocked 시 대안 | "Do not attempt to brute force. Consider alternative approaches." |
| 위험 작업 확인 | "Check with the user before proceeding" for destructive/irreversible actions |

### 2.7 에이전트/메모리 (내장)

| 행동 | 설명 |
|---|---|
| Task tool | Agent 스폰 가이드라인 내장 (294 tks) |
| Explore agent | 코드 탐색 전문 서브에이전트 (516 tks) |
| Plan mode | 계획 모드 전환 로직 (633 tks) |
| Agent memory | 도메인별 메모리 업데이트 가이드 (337 tks) |
| Session memory | 세션 메모리 템플릿 + 업데이트 지시 (756 tks) |
| Learning mode | 교육적 상호작용 모드 (1042 tks) |

→ **결론**: 기본 에이전트 동작은 내장. Orchestrator/Worker **분리 규칙**은 없으므로 오버라이드 가치 있음.

---

## 3. 기본값으로 안 되는 것 (오버라이드 필수)

| 행동 | 기본 동작 | 필요한 오버라이드 | 근거 |
|---|---|---|---|
| 한국어 응답 | 영어 | `ALWAYS respond in Korean` | 시스템 프롬프트에 없음 |
| uv 사용 | pip/poetry 경향 | `prefer uv` | 시스템 프롬프트에 없음 |
| pnpm 사용 | npm 경향 | `prefer pnpm` | 시스템 프롬프트에 없음 |
| ruff 자동 포맷 | 수동 | PostToolUse hook | 훅으로 강제 실행 |
| 3회 실패 후 중단 | 대안 탐색 권장하나 임계값 없음 | 3+ Fix Rule | 구체적 "3회" 기준 필요 |
| 완료 전 검증 | "should work" 주장 경향 | Verification Gate | IDENTIFY→RUN→READ→VERIFY 프로세스 |
| Co-Authored-By 제거 | 조건부 포함 (기본 ON) | `No Co-Authored-By` | 변수 오버라이드 |
| Agent 역할 분리 | 구분 없음 | Orchestrator/Worker 패턴 | 시스템 프롬프트에 없음 |
| 2단계 리뷰 | 없음 | Two-Stage Review | 시스템 프롬프트에 없음 |
| 스킬 자동 호출 | 없음 | Auto-trigger 규칙 | 커스텀 워크플로우 |
| Persistence | TODO 남기고 이동 가능 | Start = Finish | 시스템 프롬프트에 없음 |

---

## 4. 회색 지대: 알지만 일관성 없는 것

| 항목 | 시스템 프롬프트 커버리지 | 권장 |
|---|---|---|
| SOLID | 없음 (OCP, SRP 등 명시 없음) | 1줄 리마인더 유지 |
| DRY | "three similar lines > abstraction"으로 간접 커버 | 구체적 임계값 rules/에서 보강 |
| KISS | 5개 프래그먼트로 강하게 커버 | 1줄 리마인더 충분 |
| Scope 유지 | "only make directly requested changes"로 커버 | rules/에서 보강 |
| TODO 남기지 않기 | 없음 | "Start = Finish" 오버라이드 필요 |
| Root cause analysis | "consider alternatives" 수준 | rules/에서 상세화 |

---

## 5. 논문 핵심 발견

### arxiv 2602.15228
- "지시 구체성을 높인다고 정확도가 단조증가하지 않음"
- "Few-shot 예시가 대형 모델에서 오히려 성능 저하"
- Java가 Python보다 시스템 프롬프트 변동에 민감

### HumanLayer 분석
- **"지시 수가 늘수록 모든 지시의 준수율이 균일하게 감소"**
- 시스템 프롬프트 이미 ~50개 지시 포함
- CLAUDE.md는 150-200개 지시 이하 권장
- HumanLayer 자체 CLAUDE.md는 60줄 미만
- "Never send an LLM to do a linter's job" — 코드 스타일은 포맷터/린터로

### Arize 연구
- CLAUDE.md 최적화로 SWE Bench +10.87% 향상 (단일 레포)
- 핵심: 레포 특화 지시가 일반 지시보다 효과적

---

## 6. 커뮤니티 보고 (GitHub Issues)

- [#668](https://github.com/anthropics/claude-code/issues/668) — Claude가 CLAUDE.md 지시를 따르지 않는 버그
- [#7777](https://github.com/anthropics/claude-code/issues/7777) — Claude가 에이전트/CLAUDE.md 지시를 무시하는 문제
- 공통 원인: CLAUDE.md가 너무 길어서 지시가 "묻힘"

---

## 7. 결론: CLAUDE.md 작성 원칙

### 포함 기준 (하나라도 해당하면 포함)
1. **기본 동작을 바꾸는가?** (예: 한국어, uv, No Co-Authored-By)
2. **구체적 임계값/기준인가?** (예: "3회 실패 후 중단")
3. **고유한 워크플로우인가?** (예: Two-Stage Review, Orchestrator/Worker)

### 제외 기준 (하나라도 해당하면 제외)
1. **시스템 프롬프트에 이미 있는가?** — 225+개 프래그먼트 확인 필요
2. **언어/프레임워크 기본 컨벤션인가?** (예: snake_case, camelCase)
3. **"설명"인가 "지시"인가?** (설명 = 해로움, 지시 = 도움)
4. **린터/포맷터/훅이 할 수 있는가?** (예: ruff → hook으로)

### 적정 크기
- CLAUDE.md: **60줄 이하** (HumanLayer 기준)
- 총 지시 수: **100개 이하** (시스템 ~50 + CLAUDE.md ~50)
- 상세 규칙: `rules/` 디렉토리로 분리 (필요 시만 로드)

### 시스템 프롬프트와 중복되는 일반적 실수
| CLAUDE.md에 흔히 적는 것 | 이미 내장된 이유 |
|---|---|
| "Read before edit" | Edit 도구가 Read 없이 실패 + 별도 프래그먼트 |
| "Don't over-engineer" | 5개 독립 프래그먼트가 이미 커버 |
| "Use feature branches" | Git 안전 프로토콜에 포함 |
| "Don't skip hooks" | "NEVER skip hooks" 명시적 금지 |
| "Prefer dedicated tools" | 13개 도구 사용 정책 프래그먼트 |
| "Be concise" | Tone and style 프래그먼트 2개 |
| "Don't create unnecessary files" | Minimize file creation 프래그먼트 |
| "Security best practices" | OWASP Top 10 방지 프래그먼트 |
| "No emoji" | 명시적 금지 |
| "Git safety" | 8+ 프래그먼트, 가장 상세한 영역 |
