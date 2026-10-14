# 플러그인이 관리하는 루트 하나, 수명 순으로 배치한다

*[English](./one-root-by-lifetime.md) · 한국어*

플러그인의 루트가 어디에 있는지, 저장소가 어떻게 옵트인하는지, 처음 설정에서
무엇을 묻는지, 그리고 루트의 각 부분이 얼마나 오래 사는지를 정합니다.

## 무엇이 바뀌는가, 네 줄로

<!-- specs/1788331011-two-roots-hold-three-lifetimes -->
**플러그인이 관리하는 루트 하나가 전부를 담고, 얼마나 오래 사는지에 따라
자리를 나눕니다.** `seal/specs/<id>/` 는 `settle` 이 `docs/` 로 접을 때까지
작업 항목을 담고, `seal/ledger/<id>.md` 는 릴리스가 접을 때까지 그 항목의
대조표 행을 담습니다. 영구히 남는 것은 `seal/` 바로 아래에 있습니다. 루트를
어디에 둘지는 저장소가 고릅니다. shared 는 커밋하고, local 은 공통 git
디렉터리 아래에 두어 커밋하지 않습니다. 그 자리에 루트가 있다는 것이 곧
옵트인입니다. 아직 0.3.x 배치인 저장소는 세션 시작 훅 `hooks/root-migrate.py`
가 한 번 옮기고, 커밋 안 된 파일 위에서는 옮기지 않습니다. 그 전까지 그
저장소에서 모든 게이트는 아무 말도 하지 않습니다. 어떤 표시가 그 배치를
이루는지는 `skills/implement/orchestration.md` §*Orchestrator: Bootstrap —
create what's missing* 에 있습니다. 그런 표시가 없는 `specs/` 는 프로젝트의
것입니다. 참고 루트(reference root)로 보고 이력으로 읽기만 하며, 쓰지
않습니다(`templates/config.md` §*Reference specs*).
Enforced by: tests/test_no_document_names_the_old_roots.py::test_no_shipped_document_names_the_old_roots, tests/test_optin_home.py::test_the_legacy_directory_is_not_an_opt_in

## 제안하는 트리

플러그인이 관리하는 루트 하나입니다. 플러그인이 만들고 옮기고 접으며, 그
검사기가 형식을 정합니다. `.github/` 가 GitHub 의 것인 것과 같습니다.

```
<repo>/
├── seal/                          플러그인이 만들고 옮기고 접는다. shared 모드에서는 커밋한다
│   ├── README.md                  이 폴더의 규칙: 옮기기 규칙, 무엇이 언제 어디로 가는지
│   ├── ledger.md                  합쳐진 근거 대조표. 영구
│   ├── ledger/<id>.md             진행 중인 작업 항목의 행. 릴리스 때 접고 치운다
│   ├── follow-up.md               영구
│   ├── parity.md                  이관 프로젝트에만. 영구
│   ├── pact.md                    pact 를 가진 저장소에만. 영구
│   ├── pact-changes/<id>.md       signer 의 pact change, --reverify 가 쓴다. 영구
│   ├── pact-reviews/<id>.md       pact 를 가진 저장소의 pact review. 영구
│   └── specs/<작업항목-id>/       작업 항목 전체. settle 이 접을 때까지 산다
│       ├── spec.md plan.md questions.md overview.md      작업의 기록: 무엇을 왜 만들기로 했는가
│       ├── changelog.md                                  릴리스 때 모은다
│       ├── routing.md rounds/round-N.md                  커밋 게이트와 CI 가 읽는 것
│       ├── tests-todo.md evidence-todo.md                무엇이든 접기 전에 evidence-todo 는 비어 있어야 한다
│       └── pr.ko.md
├── docs/                          정책서, 그리고 settle 이 작업의 기록을 접어 넣는 자리. 사람과 settle 이 쓴다
├── CHANGELOG.md
└── .git/                          커밋하지 않는다
    ├── seal/                      local 모드에서만. 위의 루트 전체가 <repo>/seal/ 대신 여기 산다
    ├── specseal-planner           framer 표시. 세션 상태
    ├── specseal-implementer       smith 표시. 세션 상태
    └── specseal-worktree-choice/  워크트리 질문의 답. 세션 상태
```

| 수명 | 사는 자리 | 끝나는 때 |
|---|---|---|
| 세션 | `.git/` | 세션이 끝날 때 |
| 릴리스와 릴리스 사이 | `seal/ledger/<id>.md` · `seal/specs/<id>/` | 릴리스 단계가 조각을 접고, `settle` 이 작업 항목을 접을 때 |
| 영구 | `seal/ledger.md` · `follow-up.md` · `parity.md` · `docs/` · `CHANGELOG.md` | 없음 |

**모든 `seal/…` 경로는 `<repo>/seal/` 이 있으면 그것을, 없으면
`$(git rev-parse --git-common-dir)/seal/` 을 뜻합니다.** `implement` 스킬과
에이전트들이 이것을 한 문장으로 적고, 훅은 코드로 풉니다.

**이름이 말하는 것.** `seal/specs/<id>/` 에는 스펙과 그 과정 기록이
있습니다. `seal/ledger*` 는 스펙과 코드를 묶어 두고 코드가 움직이면 깨지는
그 묶음입니다. 제품 이름이 봉인하는 것이 이것이고, 에이전트가 찍는 seal 중
하나가 아닙니다(`skills/verify/SKILL.md` §*Every agent seals what it
verified, and one of them is final*).

## 릴리스 때 일어나는 일

1. **`seal/ledger/<id>.md` 를 그 릴리스의 대조표 파일로 접고** 조각을
   치웁니다. 아직 병합되지 않은 작업 항목의 조각은 그대로 둡니다. 삭제가
   아니라 이동이라 행은 전부 살아남고, 병합 뒤에는 조각이 막아 주던 파일 앞에
   줄 설 브랜치가 없습니다.
2. **`seal/specs/<id>/` 를 `docs/` 로 접고, 그 뒤 디렉터리를 지웁니다.**
   이것이 `settle` 입니다(`skills/settle/SKILL.md`). 릴리스된 작업 항목마다
   작업의 기록을 이미 있는 `docs/` 문서에 합치고, 새 영역일 때만 문서를
   만듭니다. 둘이 다르게 말하면 나중 작업 항목이 이깁니다. 접힌 문장마다
   작업 항목 id 를 HTML 주석으로 남기며, 그것이 접기 기록이고 다른 기록은
   없습니다.
3. **가드.** 릴리스보다 오래 살아야 하는 `spec.md` 의 문장은 병합 전에
   `docs/` 정책서나 대조표의 행에 있어야 합니다. 릴리스된 작업 항목의
   `evidence-todo.md` 에 열린 행이 있으면 릴리스 단계는 돌기를 거부하고,
   `settle` 은 그 항목을 건너뛰며 이름을 적습니다.

**과정의 기록은 그 작업 항목을 실은 릴리스가 나간 뒤 떠납니다. 접기가
돌았든 안 돌았든 같습니다.** `settle --retire-process` 가 그것을 지웁니다.
그 릴리스가 `main` 에 병합된 뒤에는 이것을 읽는 검사가 없고, 작업의 기록이
그 안을 가리키는 자리는 릴리스 태그에서 읽습니다. 어느 파일이 과정의
기록인지는 `docs/the-record-layout.md` §*seal/specs/<work-item-id>/* 에
있습니다.

## 종속 규칙

**릴리스보다 오래 살아야 하는 것은 병합 뒤에 `seal/specs/<id>/` 를 읽어서는
안 됩니다.** `settle` 이 이 디렉터리를 지우므로, 영구적인 용도에서는 이미 없는
것으로 취급합니다.

- **안전한 것.** 대조표의 행은 좌표 옆에 조항 문장을 함께 적습니다. 라운드
  기록의 `Target SHA` 는 PR 이 열려 있는 동안만 읽습니다. 릴리스된 항목의
  HTML 주석은 작업 항목의 이름을 가리킬 뿐이고, git 이력에서 여전히 찾을 수
  있습니다.
- **지우기가 닿았던 두 독자.** `unverified_check.py --baseline` 은 작업 항목
  트리를 merge base 와 비교합니다. 브랜치를 체크아웃해서 돌리면 갈라진
  지점이고, CI 에서는 base 브랜치의 끝입니다. 그리고 접기 기록을 읽어서,
  접힌 디렉터리는 없어졌다고 하지 않고 접혔다고 이름을 댑니다.
  `gather_changelog.py --check` 는 릴리스 파일의 표시 주석을 세고, 조각도
  표시도 없는 묶음은 거부합니다. 그 묶음 위에서 개수 하한을 두는 검사가 세
  번째 종류이고, 접기가 그것에 무엇을 해 주어야 하는지는
  `skills/settle/SKILL.md` 에 있습니다.
- **일부러 남기는 것.** evidence-todo 가드, `seal/README.md` 의 옮기기 규칙,
  그리고 병합 뒤에 읽어도 되는 유일한 독자인 `settle` 자체입니다.

병합 뒤에 `seal/specs/<id>/` 를 새로 읽는 코드는 두 번째 갈래에 들어가고,
리뷰는 그렇게 말합니다.

**무엇이 움직일 때 다른 것을 찾아서 고쳐야 하는 관계를 만들지 않습니다.**
대조표의 행은 내용 앵커(`path#unit@hash`)라서 그 코드가 바뀔 때만 상태가
바뀌고, `settle` 은 릴리스마다 `docs/` 를 다시 쓰고 디렉터리를 지웁니다.
작업 항목 안의 경로나 위치에 묶인 것은 무엇이든 같은 식으로 깨집니다.

**`settle` 을 가볍게 유지하는 것**:

- 옮기기만 하고 검증하지 않습니다. 좌표가 맞는지는 `evidence-check` 의
  일입니다. 명령은 읽고 묶으며, 무엇이 아직 맞는지는 세션이 판단해 씁니다.
- 증분으로 돕니다. 지난번 접은 뒤 릴리스된 작업 항목만 읽으므로, 끊겨도 이어
  돌고 두 번 접히지 않습니다.
- 작업 항목의 주석이 붙은 문장은 더 새것으로 갈아 끼웁니다. 판단이 필요한
  자리는 어떤 영역이 첫 문서를 얻을 때뿐입니다.
- `evidence-todo.md` 에 열린 행이 있는 항목은 건너뛰고 이름을 적습니다.
- 접기는 작업 항목이 아닙니다. 어떻게 커밋하고 어디서 리뷰받는지는
  `skills/settle/SKILL.md` §*A fold is not a work item* 에 있습니다.

## 이 뒤로 "spec" 은 무엇을 뜻하는가

`spec.md` 는 변경 하나의 스펙입니다. 변경보다 오래 사는 것은 집이 둘입니다.
`docs/` 정책서(정책서 > SDD > 코드)와 대조표의 행이고, `settle` 이 그리로
옮깁니다. `docs/` 는 읽는 사람, 곧 사람으로 정의합니다. 사람이 쓰고,
`settle` 이 접어 넣는 유일한 쓰는 쪽입니다.

## 옵트인 신호는 루트 자체다, 모드가 정한 자리에 있는

<!-- specs/1788817289-local-mode-from-first-setup-to-the-gate -->
**저장소가 옵트인한 것은 그 모드의 자리에 `seal/` 이 있을 때입니다.** shared
모드면 `<repo>/seal/`, local 모드면 `.git/seal/` 입니다. 훅은 두 자리를 그
순서로 보고, 있는 쪽이 "켜졌다" 와 "어느 모드인가" 를 함께 말합니다. 그 밖에는
아무것도 읽지 않고 설정 키도 없습니다. local 모드에서는 폴더가 이미 클론 단위
신호이고, shared 모드에서는 플러그인을 깔지 않은 협업자에게 아무것도 돌지
않기 때문입니다. 버릴 픽스처는 공통 git 디렉터리 아래의 `.git/specseal-scratch`
파일로 빠지며, 이 파일은 커밋될 수 없습니다. 두 자리 어디에도 폴더가 없으면
옵트인하지 않은 것이고, 판단할 수 없는 훅은 아무것도 하지 않습니다.
Enforced by: tests/test_optin_home.py::test_new_home_opts_in, tests/test_optin_home.py::test_the_git_directory_is_the_second_place, tests/test_optin_home.py::test_the_shared_root_wins_when_both_exist

## 처음 설정에서 무엇을 묻는가

<!-- specs/1788354065-the-tree-that-must-stay-clean-has-no-way-to-opt-in -->
**이 프로젝트가 질문을 허용하는 유일한 순간이 처음 설정이고, 묻는 것은 하나,
shared 인가 local 인가입니다.** `AskUserQuestion` 하나에 선택지 둘을 두고,
**shared** 를 기본값으로 앞에 놓으며, 선택지마다 무엇을 하는지 적습니다.

- **shared** 는 트리에 `<repo>/seal/` 을 만들고, 경로를 정하는 커밋이 그것을
  싣습니다. `.github/workflows/hygiene.yml` 은 그 경로가 비어 있을 때만
  `templates/hygiene.yml` 에서 설치합니다.
- **local** 은 `$(git rev-parse --git-common-dir)/seal/` 을 만들고, 워크플로는
  설치하지 않으며, 트리에는 아무것도 손대지 않습니다.

두 자리 중 어디든 `seal/` 이 있거나 아직 0.3.x 배치인 저장소는 묻지 않습니다.
모드는 폴더가 있는 자리로 읽습니다. 이관 훅은 두 자리 중 어디든 루트가 있는
저장소에 옮겼다는 표시를 남기므로, local 모드 저장소가 옛 브랜치를 체크아웃해도
트리로 옮겨지지 않습니다.
Enforced by: tests/test_first_setup_asks_once.py::test_a_repository_with_the_root_at_either_place_is_never_asked, tests/test_first_setup_asks_once.py::test_the_two_options_are_named_in_order_with_shared_as_the_default

### shared 인가 local 인가

<!-- specs/1788411058-the-mode-is-two-shell-lines-in-a-readme -->
<!-- specs/1788398967-local-modes-records-never-leave-the-clone -->
**"폴더를 커밋할 것인가" 가 아니라 "CI 와 협업자가 이 워크플로를 보는가" 를
묻는 것입니다.** 어느 쪽이 맞는지는 대개 누구의 저장소인가로 정해집니다.

| | local 모드 | shared 모드 |
|---|---|---|
| 맞는 곳 | 저장소의 컨벤션 때문에 이 플러그인의 파일이 트리에 보이면 안 되는 곳. 회사 저장소, 남의 프로젝트에 기여할 때 | 자기 저장소, 또는 `seal/` 이 커밋돼도 아무에게도 지장이 없는 저장소 |
| `seal/` 이 사는 자리 | `.git/seal/`. 공통 git 디렉터리 안 | `<repo>/seal/`. 트리 안 |
| 커밋 | 하지 않는다. gitignore 에 적을 것도 없다 | 한다 |
| 연결된 워크트리와 병렬 세션 | 서로의 기록을 읽는다. git 디렉터리가 공통이다 | 서로의 기록을 읽는다. 파일이 커밋되어 있다 |
| 다른 기계와 재클론 | 비어 있는 채로 시작한다. `seal export` / `seal import` 로 손으로 사본을 옮긴다 | 전부 있다 |
| CI(대조표 검사와 체인 검사) | 돌 수 없다. hygiene 워크플로를 설치하지 않는다 | 돈다 |
| 나중에 바꾸기 | `seal mode shared` 가 `.git/seal/` 을 `<repo>/seal/` 로 옮기고 스테이지하고 워크플로를 넣는다. 커밋은 사람이 한다 | `seal mode local` 이 되돌려 옮기고 지운 것을 스테이지하고 워크플로를 뺀다. 커밋은 사람이 한다 |

**`seal/config.md` 의 `Mode` 줄은 키가 아니고, 누가 읽느냐가 다릅니다.** 그
줄은 루트가 *있어야 할* 자리를 말하고, 폴더가 있는 자리가 *실제* 자리입니다.
훅도 게이트도 검사도 그 줄로 루트를 정하지 않습니다. 읽는 것은
`hooks/optin.py#home_at` 하나뿐이고 위의 두 자리를 봅니다. 줄과 폴더가 어긋나면
검사가 짚고, 줄이 없으면 폴더가 있는 자리를 보고 채웁니다.

**local 모드는 hygiene 워크플로를 설치하지 않습니다. 거기 남은 워크플로는
영원히 빨간불이기 때문입니다.** 두 검사 모두 커밋된 파일을 읽는데 local 모드는
아무것도 커밋하지 않습니다. `unverified_check.py` 가 없는 경로에 2 로 끝나며 잡이
멈추므로, 돌았다면 아무것도 안 본 채 0 으로 끝났을 `chain_check.py` 는 돌지도
않습니다.

**local 모드는 gitignore 한 폴더가 아니라 `.git/` 아래에 삽니다.** 연결된
워크트리는 커밋된 파일만 체크아웃하므로, 무시한 `<repo>/seal/` 은 모든
워크트리에서 없습니다. `git rev-parse --git-common-dir` 은 그 클론의 모든
워크트리가 공유하고, 커밋 후보가 되지 않으며, `.gitignore` 줄도 필요
없습니다.

**local 의 기록은 그 기계의 그 클론을 떠나지 않습니다.** 새 기계나 재클론은
대조표도 작업 항목 기록도 없이 시작하고, CI 의 대조표 검사와 체인 검사는 돌 수
없습니다. 이것이 트레이드오프의 전부이고, 병렬 항목을 떼어 놓는 것은 브랜치
격리가 아니라 작업 항목마다 조각을 두는 배치입니다.

**local 의 기록은 손으로 옮길 수 있고, 복사는 동기화가 아닙니다.** 대조표의
행은 내용 앵커라서, 옮긴 대조표는 다른 트리에서 내용이 다른 자리만 DRIFTED 로
내려가고 깨지지 않습니다. 라운드 기록은 푸시된 커밋을 가리킵니다.
`.git/seal/` 은 옆의 세션 상태 없이 그것만 복사할 수 있게 자기 폴더입니다.
마지막 복사가 이기므로, 두 번 필요해지면 shared 로 바꾸라는 신호입니다.

**되돌릴 수 없는 것은 모드가 아니라 히스토리입니다.** shared 모드에서 커밋된
기록은 되돌아와도 저장소의 히스토리에 남습니다. 그래서 명령은 움직이기 전에
그것을 말하고, 커밋이 아니라 스테이지까지만 합니다.

**local 모드에는 export/import 한 쌍이 붙습니다.**

- `seal export` 는 `.git/seal/` 만 `seal-<repo>-<date>.zip` 으로 묶고,
  매니페스트에 원격 URL 과 export 시점의 HEAD SHA 를 적습니다.
- `seal import <zip>` 은 덮어쓰지 않습니다. 이미 있는 id 는 기존 파일 옆에
  `<id>.incoming.md` 로 내려놓고 알리며, 묻지 않습니다. 그 뒤
  `evidence-check` 가 이 트리 기준으로 어느 행이 어긋났는지 말합니다.
- 같은 쌍이 모드 전환입니다. export 하고 `<repo>/seal/` 에 풀고 커밋합니다.
- 알림은 하나뿐입니다. local 모드에서는 릴리스 준비 단계가 "마지막 export
  이후 작업 항목 N 개가 바뀌었습니다" 를 출력합니다. 어디에도 올리지 않습니다.

Enforced by: tests/test_first_setup_asks_once.py::test_each_option_says_what_it_creates_and_what_it_installs, tests/test_optin_home.py::test_the_local_root_is_never_a_commit_candidate_and_needs_no_gitignore

### 보존: 잰 것, 그리고 `settle` 이 답한 것

**처음 설정은 보존을 묻지 않습니다.** 작업 항목에서 남길 가치가 있는 작업의
기록은 `settle` 이 `docs/` 로 접고, 과정의 기록은 그 릴리스 뒤에
떠나므로(§*릴리스 때 일어나는 일*), 디렉터리에는 고를 것이 남지 않습니다.

## 이름

**제품명은 SpecSeal 이고, 안에서는 `seal` 한 단어를 어휘로 씁니다.** 루트
`seal/`, 명령 `seal export` / `seal import`, 기록을 가리키는 말 "the seal"
입니다.

| 이름 | 한 문장으로 | 왜 아닌가 |
|---|---|---|
| SpecSeal | 스펙을 그것을 구현한 코드에 봉인한다 | — 무엇을 어떻게 하는지 말한다. "spec 은 빌려 온 말, seal 은 우리 것" 이 드러난다 |
| Seal | 봉인한다 | 목적어가 없어 순환한다. 충돌이 심하다(Microsoft SEAL, kubeseal). 마켓플레이스에서 찾을 수 없는 이름이다 |
| AiSeal | AI 가 만든 것을 봉인한다 | 봉인되는 것이 아니라 만든 이를 이름에 넣는다. 접두어가 낡는다. 충돌한다 |

**루트 이름은 `.seal/` 이 아니라 보이는 `seal/` 입니다.** 진행 중인 항목은 PR
이 열려 있는 동안 사람이 읽는 것이고, 훅은 이름으로 폴더를 찾을 뿐 점이
있는지는 상관하지 않습니다.

**하위 디렉터리 이름은 `seal/specs/<id>/` 입니다.** 처음 여는 사람에게
디렉터리 이름이 안에 무엇이 있는지 말해야 합니다. smith 와 warden 은
에이전트 페르소나로 남고 디렉터리 이름에는 쓰지 않습니다.

**배포되는 산출물은 전부 영어입니다.** 저장소 자신의 커밋과 기록을 어떤
언어로 쓸지는 그 저장소의 설정이 정합니다(§*저장소가 스스로 정하는 것, 그리고
그것을 읽는 방법*).

## 저장소가 스스로 정하는 것, 그리고 그것을 읽는 방법

`seal/config.md` 는 저장소가 자기 자신에 대해 쓰는 단 하나의 파일입니다.
항목 하나에 행 하나를 두고, 검사기가 읽으며, 손으로 고칠 수 있습니다. 행은
`templates/config.md` 에 설명되어 있고, 행이 없을 때의 기본값도 거기에
적혀 있습니다.

<!-- specs/1788420761-the-settings-live-in-a-file-nobody-opens -->
**아무도 찾지 못하는 설정은 없는 설정과 같습니다.** 모든 행은 파일 전체를
보여 주고 변경을 알맞은 곳으로 보내는 명령 하나에서 닿을 수 있습니다. 처음
설정은 질문을 한 번에 묻고 다시 묻지 않기 때문입니다. 변경을 보내는 층은 자기
논리를 갖지 않습니다. 부수 효과가 있는 행은 그 일을 하는 스크립트로 보내고,
그냥 행일 뿐인 것은 바로 씁니다. 스킬 안의 논리는 스크립트처럼 변이 테스트를
할 수 없기 때문입니다.
Enforced by: tests/test_the_settings_have_a_front_door.py::test_the_skill_names_every_row_the_template_ships, tests/test_the_settings_have_a_front_door.py::test_the_skill_shows_rows_that_are_absent

<!-- specs/1788360817-the-pull-request-language-is-fixed-inside-a-skill -->
**이 플러그인이 어떤 언어로 쓰는지는 플러그인이 아니라 저장소가 답합니다.**
언어는 설정 행에 두고, 번역된 PR 본문이 들어가는 사본 파일의 이름은 그 안에
담긴 언어를 따릅니다.
Enforced by: tests/test_the_pull_request_language_is_the_repositorys.py::test_the_skill_names_the_file_and_the_row, tests/test_the_pull_request_language_is_the_repositorys.py::test_the_mirror_is_named_for_its_own_language

<!-- specs/1788420760-a-language-row-that-governs-four-things -->
**행이 둘인 이유는 행 하나로는 중간 답을 적을 수 없어서입니다.**
`Commit and pull request language` 는 바깥에서 읽는 것, 곧 커밋 제목과 본문,
PR 제목과 본문을 맡고, `Record language` 는 작업 항목이 쓰는 문서의 산문을
맡습니다. 하나를 정해도 다른 하나는 따라가지 않습니다. PR 은 그것을 여는
사람이 읽고, 기록은 여섯 달 뒤 그 결정으로 돌아오는 사람이 읽기 때문입니다.
어느 행이 무엇을 말하든 **검사기가 맞춰 보는 이름은 영어로 남습니다.** 필드
이름, 판정 낱말, 표시 주석, 근거 대조표의 앵커, 그리고 모든 코드가 그렇습니다.
Enforced by: tests/test_the_pull_request_language_is_the_repositorys.py::test_the_template_is_one_item_value_table_whose_first_row_is_the_language, tests/test_the_pull_request_language_is_the_repositorys.py::test_every_document_that_names_a_language_row_names_the_shipped_one

<!-- specs/1789598366-a-piped-broad-gate-row-takes-every-config-row-below-it -->
**칸에는 이스케이프한 파이프가 들어갈 수 있고, 해석되지 않는 줄 하나는 표의
끝으로 여기지 않고 이름을 대어 알립니다.** 읽는 쪽과 쓰는 쪽이 행 하나를
설명하는 상수를 함께 쓰므로, 어느 줄이 주어진 행인지 둘의 판단이 같습니다.
Enforced by: tests/test_the_mode_question_is_asked_once.py::test_an_escaped_pipe_is_one_row_and_the_rows_below_it_still_arrive, tests/test_the_mode_question_is_asked_once.py::test_a_line_that_will_not_parse_is_named_and_the_hook_still_says_nothing

<!-- specs/1788789329-a-git-call-that-fails-reads-as-no-remote -->
**실패한 git 호출은 "없음" 이라고 답한 git 호출이 아닙니다.** 그 구분이 필요한
호출자를 둔 호출 자리는 모두 그 구분을 돌려주고, 거부할 때는 원격이 없다,
다른 작업 트리가 없다, 추적되는 파일이 없다고 자신 있게 말하는 대신 어느
호출이 실패했는지를 밝힙니다.
Enforced by: tests/test_the_records_can_be_carried_out_and_in.py::test_the_export_omits_a_remote_it_could_not_read, tests/test_the_records_can_be_carried_out_and_in.py::test_an_unreadable_remote_here_refuses_the_import, tests/test_the_mode_is_a_row_and_a_command.py::test_a_git_that_cannot_answer_does_not_report_no_submodule
