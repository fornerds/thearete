# TheArete Skin care application

## 🚀 빠른 시작 (Docker Compose)

### 1. 서비스 시작

```bash
# backend 디렉토리로 이동
cd backend

# Docker Compose로 모든 서비스 시작 (PostgreSQL + Backend)
docker compose up -d

# 또는 Makefile 사용
make docker-up
```

### 2. 서비스 상태 확인

```bash
# 실행 중인 컨테이너 확인
docker compose ps

# 로그 확인
docker compose logs -f backend

# 또는 Makefile 사용
make docker-logs
```

### 3. 데이터베이스 마이그레이션

```bash
# backend 컨테이너에서 마이그레이션 실행
docker compose exec backend alembic upgrade head

```

### 4. 서비스 중지

```bash
# 모든 서비스 중지
docker compose down

# 또는 Makefile 사용
make docker-down

# 볼륨까지 삭제하려면
docker compose down -v
```

## 📚 API 문서 접속

애플리케이션이 실행되면 다음 URL에서 API 문서를 확인할 수 있습니다:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json
- **Health Check**: http://localhost:8000/v1/health

## 🗄️ 데이터베이스 접속

### PostgreSQL 접속 정보

- **호스트**: localhost
- **포트**: 5432
- **데이터베이스**: mobile_backend
- **사용자**: postgres
- **비밀번호**: password

### DB Shell 접속

```bash
# Docker Compose를 통한 접속
docker compose exec postgres psql -U postgres -d mobile_backend

# 또는 Makefile 사용
make db-shell
```

## 🔧 유용한 명령어

```bash
# Backend 재빌드
docker compose build backend

# Backend만 재시작
docker compose restart backend

# 특정 서비스 로그만 확인
docker compose logs -f postgres
docker compose logs -f backend
```

## 🤖 MCP (Model Context Protocol) 설정

Cursor IDE에서 Figma 디자인을 Flutter 코드로 변환하고, 다양한 도구와 연동하기 위한 MCP 서버를 설정할 수 있습니다.

**주요 기능**:

- 🎨 **Talk to Figma MCP**: Figma 디자인을 Flutter 위젯 코드로 자동 변환, 텍스트 일괄 교체, 컴포넌트 오버라이드 전파 등
- 🔍 **GitHub MCP**: 코드 검색 및 이슈 관리
- 📁 **File System MCP**: 프로젝트 파일 탐색
- 🔎 **Brave Search MCP**: 웹 검색을 통한 최신 정보 조회
- 🗄️ **PostgreSQL/SQLite MCP**: 데이터베이스 쿼리 및 관리

**빠른 시작**:

```bash
# 1. Bun 설치 (Talk to Figma MCP 필수)
curl -fsSL https://bun.sh/install | bash

# 2. WebSocket 서버 시작 (별도 터미널)
bunx cursor-talk-to-figma-mcp@latest socket

# 3. Figma에서 플러그인 설치 및 연결
# 4. Cursor 재시작
```

**상세 설정 방법**: [MCP_SETUP.md](MCP_SETUP.md) 참고

## 📖 상세 문서

- Backend: [backend/README.md](backend/README.md)
- Flutter: [flutter/project_convention.md](flutter/project_convention.md)
- MCP 설정: [MCP_SETUP.md](MCP_SETUP.md)

```mermaid
erDiagram

    %% ───────────────────────────────
    %% 0. 피부샵 (회원)
    %% ───────────────────────────────
    SHOP {
        bigint id PK
        string name "상호명"
        string address "주소"
        string owner_name "대표자명"
        string phone "전화번호"
        string email "이메일 (로그인 ID)"
        string password "비밀번호 (암호화 저장)"
        string refresh_token "현재 로그인 중인 Refresh Token 저장"
        datetime refresh_token_expiry	"Refresh Token 만료 일시"
        datetime last_login_at "마지막 로그인 시간 (선택)"
        datetime created_at
        datetime updated_at
        boolean is_deleted
    }

    %% ───────────────────────────────
    %% 1. 고객 프로필
    %% ───────────────────────────────
    CUSTOMER {
        bigint id PK
        bigint shop_id FK
        string name "고객명"
        int age "나이"
        enum gender "성별 (M/F)"
        string phone "연락처"
        string skin_type "피부타입"
        text note "특이사항"
        tinyint marked "상단 고정 여부"
        datetime created_at
        datetime updated_at
        boolean is_deleted
    }

    %% ───────────────────────────────
    %% 2. 시술 (고객별 관리)
    %% ───────────────────────────────
    TREATMENT {
        bigint id PK
        bigint customer_id FK
        string type "시술 종류 (튼살-경, 튼살-중, 백반증, 흉터 등)"
        string area "시술 부위 (얼굴, 목, 팔, 다리, 입술 등)"
        boolean is_completed "시술 완료 여부"
        datetime created_at
        datetime updated_at
        boolean is_deleted
    }

    %% ───────────────────────────────
    %% 3. 시술 회차별 관리
    %% ───────────────────────────────
    TREATMENT_SESSION {
        bigint id PK
        bigint treatment_id FK
        date treatment_date "시술 날짜"
        int duration_minutes "소요시간(분)"
        int melanin "멜라닌 투입량 (0~9)"
        int white "화이트 투입량 (0~9)"
        int red "레드 투입량 (0~9)"
        int yellow "옐로우 투입량 (0~9)"
        boolean is_completed "시술 완료 여부"
        tinyint is_result_entered "시술 결과 입력 저장 여부"
        text note "특이사항"
        datetime first_recorded_at "최초 작성시간"
        datetime last_modified_at "최종 수정시간"
        datetime created_at
        datetime updated_at
        boolean is_deleted
    }

    %% ───────────────────────────────
    %% 4. 피부색 측정 데이터 (일반/병변)
    %% ───────────────────────────────
    SKIN_COLOR_MEASUREMENT {
        bigint id PK
        bigint session_id FK
        enum region_type "NORMAL | LESION"
        float l_value "L 값"
        float a_value "a 값"
        float b_value "b 값"
        string measurement_point "측정 위치(선택적)"
        datetime measured_at "측정 시각"
        datetime created_at
        datetime updated_at
        boolean is_deleted
    }

    %% ───────────────────────────────
    %% 6. 업로드된 이미지 원본
    %% ───────────────────────────────
    UPLOADED_IMAGE {
        bigint id PK
        string original_filename "원본 파일명"
        string storage_path "스토리지 내 저장 경로 (유니크)"
        string public_url "공개 접근 URL"
        string content_type "MIME 타입"
        int file_size "파일 크기 (바이트)"
        string storage_backend "저장소 구분 (local, s3 등)"
        datetime created_at
        boolean is_deleted
    }

    %% ───────────────────────────────
    %% 7. 시술 회차 이미지 매핑
    %% ───────────────────────────────
    TREATMENT_SESSION_IMAGE {
        bigint id PK
        bigint treatment_id FK
        bigint session_id FK
        bigint uploaded_image_id FK
        int sequence_no "표시 순서"
        string photo_type "BEFORE | AFTER 등 (선택)"
        datetime created_at
    }

    %% ───────────────────────────────
    %% 관계 설정
    %% ───────────────────────────────
    SHOP ||--o{ CUSTOMER : "has many"
    CUSTOMER ||--o{ TREATMENT : "has many"
    TREATMENT ||--o{ TREATMENT_SESSION : "has many"
    TREATMENT_SESSION ||--o{ SKIN_COLOR_MEASUREMENT : "has many"
    TREATMENT_SESSION ||--o{ TREATMENT_SESSION_IMAGE : "has many"
    TREATMENT ||--o{ TREATMENT_SESSION_IMAGE : "has many"
    UPLOADED_IMAGE ||--o{ TREATMENT_SESSION_IMAGE : "has many"
```
