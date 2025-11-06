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

## 📖 상세 문서

더 자세한 내용은 [backend/README.md](backend/README.md)를 참고하세요.
