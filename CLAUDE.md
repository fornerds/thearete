# Working ref.

## backend API 개발(신규 생성·수정) 기본 진행 순서

1. 요구사항을 확인하고, 구현에 필요한 추가 사항이 있으면 사용자에게 문의합니다.
2. 구현이 가능하다고 판단되면 실제 개발을 시작합니다.
3. 구현 후 backend container 로그에 문제 없는지 확인합니다. 이슈 발생 시 해결합니다.
4. 특별한 테스트 요구가 있을 때에만 curl 등으로 테스트를 수행하고, 필요 시 timeout과 docker 컨테이너 상태도 확인합니다.
5. 문제 확인이 필요하면 backend 컨테이너 로그를 docker 명령어로 확인합니다.
6. 테스트 계정이나 데이터가 필요할 경우 기존 API를 통해 생성하여 사용합니다.
   예시 테스트 계정:
   {
   "email": "skincare1@skin.com",
   "password": "qwer1234"
   }
7. Database나 model 변경 시에는 alembic 명령어로 migration 파일을 생성 및 적용합니다.
8. backend, database, nginx 등은 docker compose로 기동 및 관리합니다.
