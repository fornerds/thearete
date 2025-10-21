# Mobile Backend

FastAPI 기반의 모바일 백엔드 API 서버입니다.

## 🚀 주요 기능

- **FastAPI**: 고성능 웹 프레임워크
- **SQLAlchemy 2.x**: ORM 및 데이터베이스 관리
- **Alembic**: 데이터베이스 마이그레이션
- **JWT 인증**: Bearer 토큰 기반 인증
- **PostgreSQL**: 프로덕션 데이터베이스
- **Pydantic**: 데이터 검증 및 직렬화
- **pytest**: 테스트 프레임워크
- **Docker**: 컨테이너화

## 📁 프로젝트 구조

```
backend/
├── app/
│   ├── main.py              # FastAPI 앱 진입점
│   ├── config.py             # 설정 관리
│   ├── deps.py               # 의존성 주입
│   ├── core/                 # 핵심 기능
│   │   ├── security.py       # JWT 및 비밀번호 해싱
│   │   ├── auth.py           # 인증 유틸리티
│   │   ├── exceptions.py     # 커스텀 예외
│   │   └── pagination.py     # 페이지네이션
│   ├── db/                   # 데이터베이스
│   │   ├── base.py           # SQLAlchemy Base
│   │   ├── session.py        # DB 세션 관리
│   │   ├── models/           # 데이터베이스 모델
│   │   └── repositories/     # 데이터 액세스 레이어
│   ├── schemas/              # Pydantic 스키마
│   ├── services/             # 비즈니스 로직
│   ├── api/v1/               # API 라우터
│   ├── ai/                   # AI 클라이언트
│   └── scripts/              # 유틸리티 스크립트
├── tests/                    # 테스트
├── alembic/                  # 마이그레이션
├── docker-compose.yml        # Docker Compose 설정
├── Dockerfile               # Docker 이미지
├── Makefile                 # 개발 도구
└── pyproject.toml           # 프로젝트 설정
```

## 🛠️ 설치 및 실행

### 1. 의존성 설치

```bash
# uv 사용 (권장)
uv sync

# 또는 pip 사용
pip install -e .
```

### 2. 환경변수 설정

```bash
cp .env.example .env
# .env 파일을 편집하여 설정값 수정
```

### 3. 데이터베이스 설정

```bash
# Docker Compose로 PostgreSQL 시작
docker compose up -d postgres

# 마이그레이션 실행
alembic upgrade head

# 샘플 데이터 시드
python -m app.scripts.seed
```

### 4. 애플리케이션 실행

```bash
# 개발 모드
uvicorn app.main:app --reload

# 또는 Makefile 사용
make run
```

## 🐳 Docker 사용

```bash
# 모든 서비스 시작
docker compose up -d

# 백엔드만 재빌드
docker compose up backend -d --build

# 로그 확인
docker compose logs -f backend
```

## 🧪 테스트

```bash
# 모든 테스트 실행
pytest

# 커버리지 포함
pytest --cov=app --cov-report=html

# 또는 Makefile 사용
make test
```

## 📚 API 문서

애플리케이션 실행 후 다음 URL에서 API 문서를 확인할 수 있습니다:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔧 개발 도구

```bash
# 코드 포맷팅
make fmt

# 린팅
make lint

# 마이그레이션 생성
make revision msg="Add new table"

# 데이터베이스 시드
make seed
```

## 🔐 인증

API는 JWT Bearer 토큰을 사용합니다:

1. `/v1/auth/login`에서 로그인하여 토큰 획득
2. 요청 헤더에 `Authorization: Bearer <token>` 추가
3. `/v1/auth/refresh`로 토큰 갱신

## 📝 주요 엔드포인트

- `GET /v1/health` - 헬스 체크
- `POST /v1/auth/login` - 로그인
- `POST /v1/auth/refresh` - 토큰 갱신
- `GET /v1/items/` - 아이템 목록
- `POST /v1/items/` - 아이템 생성
- `GET /v1/items/{id}` - 아이템 조회
- `PUT /v1/items/{id}` - 아이템 수정
- `DELETE /v1/items/{id}` - 아이템 삭제

## 🚀 배포

프로덕션 환경에서는 다음을 고려하세요:

1. 환경변수에서 `SECRET_KEY` 변경
2. 데이터베이스 URL 설정
3. CORS 설정 조정
4. 로깅 설정
5. 모니터링 도구 연동
