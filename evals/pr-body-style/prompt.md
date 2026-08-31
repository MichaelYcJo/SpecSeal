다음 변경에 대한 PR 본문을 한국어로 작성해줘 (실제 파일은 없고, 본문 작성만):

- auth_service.py 에 login_with_email 함수 추가
- user.py 의 password_hash 컬럼을 bcrypt 에서 argon2id 로 변경
- 회원가입 통합 테스트 3개 파일 추가

이 변경으로 이메일+비밀번호 로그인이 도입되고, 기존 사용자는 다음 로그인 때
해시가 자동 이전된다. DB 마이그레이션이 하나 포함된다.
