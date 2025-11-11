# MCP 서버 설정 가이드

이 문서는 Cursor IDE에서 MCP (Model Context Protocol) 서버를 설정하는 방법을 안내합니다.

## 🔍 MCP란 무엇인가?

MCP(Model Context Protocol)는 AI 시스템이 외부 데이터 소스와 상호작용할 수 있도록 하는 프로토콜입니다. 이를 통해 AI는 파일 시스템, 데이터베이스, 웹 API 등 다양한 데이터 소스와 직접 통신하여 필요한 정보를 얻거나 명령을 실행할 수 있습니다. 특히, MCP는 양방향 데이터 흐름을 지원하여 AI가 데이터를 읽고 수정하는 것을 가능하게 합니다.

**주요 특징**:
- 양방향 데이터 흐름 지원 (읽기/쓰기)
- 다양한 데이터 소스와 통합 가능
- 실시간 상호작용 지원
- 확장 가능한 아키텍처

## 📋 설정된 MCP 서버 목록

### 1. Talk to Figma MCP (고급)

**개요**: Cursor Talk to Figma MCP는 Cursor AI와 Figma를 통합하여 디자인을 프로그래밍적으로 읽고 수정할 수 있는 기능을 제공합니다. 이를 통해 디자인과 코드 간의 전환을 더욱 효율적으로 수행할 수 있으며, Figma 디자인에서 실제 코드로 퍼블리싱하는 과정이 MCP를 통해 자동화됩니다.

**용도**: 
- Figma 디자인 정보를 가져와 Flutter 코드로 변환
- 디자인 자동화 및 일괄 수정
- 텍스트 일괄 교체
- 컴포넌트 관리 및 오버라이드 전파
- 디자인에서 코드로의 자동 퍼블리싱

**특징**:
- WebSocket을 통한 실시간 Figma 플러그인 통신
- 양방향 데이터 흐름 (디자인 읽기/수정)
- 텍스트 일괄 교체 기능
- 컴포넌트 인스턴스 오버라이드 전파
- 주석 관리 및 프로토타입 연결 생성
- 자동 레이아웃 설정
- 요소 생성 및 스타일링 자동화

**프로젝트 구조**:
- `src/talk_to_figma_mcp/`: Figma 통합을 위한 TypeScript MCP 서버
- `src/cursor_mcp_plugin/`: Cursor와 통신하기 위한 Figma 플러그인
- `src/socket.ts`: MCP 서버와 Figma 플러그인 간의 통신을 중계하는 WebSocket 서버

**설정 방법**:
1. **Bun 설치** (필수)
   ```bash
   curl -fsSL https://bun.sh/install | bash
   ```

2. **WebSocket 서버 시작** (별도 터미널)
   ```bash
   bunx cursor-talk-to-figma-socket
   ```
   
   **참고**: 서버는 기본적으로 포트 3055에서 실행됩니다. 실행되면 다음과 같은 메시지가 표시됩니다:
   ```
   WebSocket server running on port 3055
   ```
   
   또는 로컬 개발 시:
   ```bash
   bun socket
   ```

3. **Figma 플러그인 설치**
   - Figma → Plugins → Development → New Plugin
   - "Link existing plugin" 선택
   - 또는 [Figma Community](https://www.figma.com/community)에서 "Cursor Talk to Figma MCP" 검색

4. **MCP 서버 설정**
   - `.cursor/mcp.json`에 이미 설정되어 있음 (추가 토큰 불필요)

**사용 방법**:
1. WebSocket 서버 실행 (`bunx cursor-talk-to-figma-mcp@latest socket`)
2. Figma에서 "Cursor MCP Plugin" 실행
3. 플러그인에서 `join_channel` 명령으로 채널 참여
4. Cursor에서 Figma와 통신 시작

**주요 MCP 도구**:

#### 문서 및 선택
- `get_document_info` - 현재 Figma 문서의 정보를 가져옵니다
- `get_selection` - 현재 선택된 요소의 정보를 가져옵니다
- `get_node_info` - 특정 노드의 상세 정보를 가져옵니다
- `read_my_design` - 선택된 디자인의 상세 정보

#### 요소 생성
- `create_rectangle` - 위치, 크기, 이름을 지정하여 새로운 사각형을 생성합니다
- `create_frame` - 위치, 크기, 이름을 지정하여 새로운 프레임을 생성합니다
- `create_text` - 글꼴 속성을 지정하여 새로운 텍스트 노드를 생성합니다

#### 스타일링
- `set_fill_color` - 노드의 채우기 색상을 설정합니다
- `set_stroke_color` - 노드의 테두리 색상과 두께를 설정합니다
- `set_corner_radius` - 노드의 모서리 반경을 설정합니다

#### 레이아웃 및 조직
- `move_node` - 노드를 새로운 위치로 이동합니다
- `resize_node` - 노드의 크기를 조정합니다
- `delete_node` - 노드를 삭제합니다
- `set_layout_mode` - 자동 레이아웃 모드를 설정합니다
- `set_padding` - 패딩을 설정합니다

#### 컴포넌트 및 스타일
- `get_styles` - 로컬 스타일 정보를 가져옵니다
- `get_local_components` - 로컬 컴포넌트 정보를 가져옵니다
- `get_team_components` - 팀 컴포넌트 정보를 가져옵니다
- `create_component_instance` - 컴포넌트 인스턴스를 생성합니다
- `get_instance_overrides` - 컴포넌트 인스턴스 오버라이드 추출
- `set_instance_overrides` - 오버라이드를 다른 인스턴스에 전파합니다

#### 텍스트 관리
- `scan_text_nodes` - 텍스트 노드 스캔 (일괄 교체용)
- `set_multiple_text_contents` - 텍스트 일괄 교체

#### 내보내기 및 고급 기능
- `export_node_as_image` - 노드를 이미지(PNG, JPG, SVG, PDF)로 내보냅니다
- `execute_figma_code` - Figma에서 임의의 JavaScript 코드를 실행합니다
- `get_reactions` - 프로토타입 반응을 가져옵니다
- `create_connections` - FigJam 커넥터를 생성합니다

#### 연결 관리
- `join_channel` - 특정 채널에 연결하여 Figma와의 통신을 시작합니다

**사용 예시**:
- "Figma 파일에서 로그인 화면 디자인을 가져와서 Flutter 코드로 변환해줘"
- "Figma의 모든 텍스트 노드를 스캔해서 일괄 교체해줘"
- "선택한 컴포넌트 인스턴스의 오버라이드를 다른 인스턴스들에 전파해줘"
- "프로토타입 반응을 FigJam 커넥터로 변환해줘"
- "현재 선택한 프레임의 자동 레이아웃을 수직으로 설정해줘"

### 2. GitHub MCP
**용도**: GitHub 코드 검색, 이슈 관리, PR 생성

**설정 방법**:
1. GitHub Personal Access Token 생성
   - GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
   - "Generate new token (classic)" 클릭
   - 필요한 권한 선택: `repo`, `read:org` 등
   - 토큰 생성 후 복사
   
2. `.cursor/mcp.json` 파일에서 `GITHUB_PERSONAL_ACCESS_TOKEN` 값 업데이트

**사용 예시**:
- "GitHub에서 비슷한 Flutter 프로젝트 코드를 검색해줘"
- "이슈를 생성해줘"

### 3. File System MCP
**용도**: 프로젝트 파일 시스템 탐색 및 작업

**설정 방법**:
- 자동으로 프로젝트 루트 디렉토리로 설정됨
- 추가 설정 불필요

**사용 예시**:
- "프로젝트의 모든 Dart 파일을 찾아줘"
- "특정 패턴의 파일들을 검색해줘"

### 4. Brave Search MCP
**용도**: 웹 검색을 통한 최신 정보 조회

**설정 방법**:
1. Brave Search API 키 발급
   - [Brave Search API](https://brave.com/search/api/) 방문
   - API 키 발급 받기
   
2. `.cursor/mcp.json` 파일에서 `BRAVE_API_KEY` 값 업데이트

**사용 예시**:
- "Flutter 최신 버전의 변경사항을 검색해줘"
- "Riverpod 2.5 사용법을 검색해줘"

### 5. SQLite MCP
**용도**: 로컬 SQLite 데이터베이스 쿼리 및 관리

**설정 방법**:
- 자동으로 `backend/data.db` 경로로 설정됨
- 데이터베이스 파일이 없으면 생성됨

**사용 예시**:
- "데이터베이스 스키마를 확인해줘"
- "특정 테이블의 데이터를 조회해줘"

### 6. PostgreSQL MCP
**용도**: PostgreSQL 데이터베이스 쿼리 및 관리

**설정 방법**:
1. `.cursor/mcp.json` 파일에서 `POSTGRES_CONNECTION_STRING` 값 업데이트
   - 형식: `postgresql://username:password@host:port/database`
   - 프로젝트 기본값: `postgresql://postgres:password@localhost:5432/mobile_backend`
   - `docker-compose.yml`의 설정과 일치해야 함

**사용 예시**:
- "데이터베이스 테이블 목록을 보여줘"
- "특정 쿼리를 실행해줘"

## 🚀 빠른 시작 가이드

### 자동 설정 스크립트 사용 (권장)

```bash
# 프로젝트 루트에서 실행
./scripts/setup_mcp.sh
```

이 스크립트는 다음을 자동으로 수행합니다:
- Bun 설치 확인 및 설치 (필요시)
- MCP 설정 파일 생성 (예시 파일에서 복사)

### 수동 설정

### 1단계: 필수 토큰 발급

#### Bun 설치 (필수 - Talk to Figma MCP용)
```bash
curl -fsSL https://bun.sh/install | bash
```

설치 후 터미널을 재시작하거나:
```bash
source ~/.bashrc  # 또는 ~/.zshrc
```

#### Figma 플러그인 설치 (필수)
1. **방법 1: Figma Community에서 설치**
   - Figma → Plugins → Browse plugins
   - "Cursor Talk to Figma MCP" 검색 후 설치

2. **방법 2: 로컬 개발 플러그인으로 설치**
   - Figma → Plugins → Development → New Plugin
   - "Link existing plugin" 선택
   - 플러그인 manifest.json 파일 선택

#### GitHub 토큰 (선택 - 코드 검색용)
1. [GitHub Settings → Developer settings → Personal access tokens](https://github.com/settings/tokens)
2. "Generate new token (classic)" 클릭
3. 권한 선택: `repo`, `read:org`
4. 토큰 생성 후 복사

#### Brave Search API 키 (선택 - 웹 검색용)
1. [Brave Search API](https://brave.com/search/api/) 방문
2. API 키 발급

### 2단계: 설정 파일 업데이트

```bash
# 예시 파일을 복사
cp .cursor/mcp.json.example .cursor/mcp.json

# 설정 파일 열기
code .cursor/mcp.json
```

각 서버의 토큰/키 값을 실제 값으로 교체:
- `YOUR_GITHUB_TOKEN_HERE` → GitHub 토큰 (선택)
- `YOUR_BRAVE_API_KEY_HERE` → Brave API 키 (선택)

**참고**: Talk to Figma MCP는 토큰이 필요 없습니다 (WebSocket + 플러그인 방식)

### 3단계: WebSocket 서버 시작

별도 터미널에서 WebSocket 서버를 실행합니다:

```bash
# 프로젝트 루트에서
bunx cursor-talk-to-figma-mcp@latest socket
```

서버가 실행되면 다음과 같은 메시지가 표시됩니다:
```
WebSocket server running on port 3055
```

**참고**: 실제 서버는 포트 3055에서 실행됩니다. Figma 플러그인에서 연결할 때는 `ws://localhost:3055`를 사용합니다.

### 4단계: Figma 플러그인 연결

1. Figma 열기
2. Plugins → Cursor MCP Plugin 실행
3. 플러그인에서 `join_channel` 명령 실행하여 채널 참여

### 5단계: Cursor IDE 재시작

1. Cursor 완전 종료
2. Cursor 다시 시작
3. Cursor 설정 → MCP 서버 상태 확인

### 6단계: 테스트

Figma MCP 테스트:
```
"Figma에서 현재 선택한 디자인을 가져와서 Flutter 코드로 변환해줘"
```

**연결 확인**: Figma 플러그인에서 채널에 연결되면 다음과 같은 메시지가 표시됩니다:
```
Connected to server in channel: [채널ID]
```

## 💡 최적의 활용을 위한 팁

### 작업 전 확인사항
1. **채널 연결 확인**: 명령어를 보내기 전에 항상 채널에 연결되어 있는지 확인하세요
2. **문서 구조 파악**: `get_document_info`를 사용하여 문서의 전반적인 구조를 파악한 후 작업을 시작하는 것이 좋습니다
3. **선택 요소 확인**: 수정 전에 `get_selection`을 통해 현재 선택된 요소를 확인하세요

### 작업 흐름 권장사항
1. **요소 생성**: 프레임, 사각형, 텍스트 등 적절한 요소 생성 도구를 사용하여 디자인 요소를 추가하세요
2. **결과 검증**: 변경 사항을 적용한 후 `get_node_info`를 통해 결과를 검증하세요
3. **컴포넌트 활용**: 가능한 경우 컴포넌트 인스턴스를 사용하여 일관성을 유지하세요
4. **오류 처리**: 모든 명령어는 예외를 발생시킬 수 있으므로 오류 처리를 적절히 수행하세요

### 효율적인 워크플로우
- **디자인 → 코드**: Figma 디자인을 가져와서 Flutter 위젯 코드로 자동 변환
- **일괄 수정**: 텍스트나 스타일을 일괄적으로 변경하여 일관성 유지
- **컴포넌트 관리**: 컴포넌트 인스턴스의 오버라이드를 전파하여 디자인 시스템 유지
- **프로토타입 자동화**: 프로토타입 반응을 FigJam 커넥터로 변환하여 문서화

## 🎯 Flutter 프로젝트 활용 예시

### Figma 디자인을 Flutter 위젯으로 변환
```
"Figma에서 현재 선택한 로그인 화면 디자인을 가져와서 
presentation/widgets/common/buttons/primary_button.dart 
스타일에 맞춰 Flutter 코드로 변환해줘"
```

### 텍스트 일괄 교체
```
"Figma에서 모든 텍스트 노드를 스캔하고, 
'Old Text'를 'New Text'로 일괄 교체해줘"
```

### 컴포넌트 인스턴스 오버라이드 전파
```
"선택한 컴포넌트 인스턴스의 오버라이드를 
다른 모든 인스턴스에 전파해줘"
```

### GitHub에서 참고 코드 검색
```
"GitHub에서 Riverpod 2.5를 사용한 Flutter 인증 예제를 찾아줘"
```

### 프로젝트 파일 구조 분석
```
"프로젝트의 모든 Screen 파일을 찾아서 
Clean Architecture 패턴을 따르고 있는지 확인해줘"
```

### 데이터베이스 스키마 확인
```
"PostgreSQL 데이터베이스의 모든 테이블과 컬럼을 보여줘"
```

## ⚠️ 주의사항

1. **보안**
   - `.cursor/mcp.json` 파일은 `.gitignore`에 추가되어야 합니다
   - 토큰과 API 키는 절대 공개 저장소에 커밋하지 마세요

2. **토큰 권한**
   - GitHub: 필요한 최소 권한만 부여
   - Figma: 읽기 권한만 필요한 경우 읽기 전용 토큰 사용

3. **데이터베이스 연결**
   - PostgreSQL 연결 문자열에 민감한 정보가 포함되어 있으므로 주의

## 📝 .gitignore 추가

`.cursor/mcp.json` 파일을 Git에서 제외하려면:

```bash
echo ".cursor/mcp.json" >> .gitignore
```

또는 `.cursor/mcp.json.example` 파일을 생성하여 템플릿으로 사용:

```bash
cp .cursor/mcp.json .cursor/mcp.json.example
# .cursor/mcp.json.example에서 토큰 값들을 제거하고 커밋
```

## 🔧 문제 해결

### MCP 서버가 연결되지 않는 경우

1. **Node.js 버전 확인**
   ```bash
   node --version  # 18 이상이어야 함
   ```

2. **npx 명령어 확인**
   ```bash
   which npx
   ```

3. **토큰 유효성 확인**
   - 각 서비스의 토큰이 유효한지 확인
   - 토큰이 만료되었는지 확인

4. **Cursor 로그 확인**
   - Cursor 설정 → MCP 서버 로그 확인

## 🎨 디자인-코드 자동화 활용

Cursor Talk to Figma MCP를 통해 디자인과 개발의 경계를 허물어, 보다 효율적이고 통합된 워크플로우를 구축할 수 있습니다. 이를 통해 개발자는:

- **디자인을 코드로**: Figma 디자인을 자동으로 Flutter 위젯 코드로 변환
- **코드를 디자인으로**: 코드 변경사항을 Figma에 반영
- **일괄 작업 자동화**: 텍스트, 스타일, 컴포넌트 일괄 수정
- **디자인 시스템 유지**: 컴포넌트 오버라이드 전파로 일관성 유지

이를 통해 생산성을 크게 향상시킬 수 있습니다.

## 🔧 개발 및 확장

이 프로젝트는 오픈 소스로 제공되며, 개발자는 필요에 따라 기능을 확장하거나 수정할 수 있습니다. Figma 플러그인의 `code.js`와 `ui.html` 파일을 수정하여 사용자 인터페이스와 기능을 커스터마이즈할 수 있습니다.

## 📚 참고 자료

- [Model Context Protocol 공식 문서](https://modelcontextprotocol.io/)
- [Figma MCP 서버](https://www.figma.com/ko-kr/mcp-catalog/)
- [Cursor MCP 설정 가이드](https://docs.cursor.com/mcp)
- [Bun 공식 문서](https://bun.sh/docs)

