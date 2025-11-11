# Figma 디자인 정보 가져오기 및 활용 가이드

이 문서는 Cursor에서 TalkToFigma MCP를 통해 Figma 디자인 정보를 가져와서 Flutter 코드로 변환하는 방법을 설명합니다.

## 📋 사전 준비

1. ✅ WebSocket 서버 실행 중 (`bunx cursor-talk-to-figma-socket`)
2. ✅ Figma 플러그인 연결 완료 (채널 연결됨)
3. ✅ Cursor에서 MCP 서버 연결 확인

## 🔍 Step 1: Figma 디자인 정보 가져오기

### 1-1. 문서 전체 구조 파악하기

**Cursor에서 요청:**
```
"Figma 문서의 전체 구조를 보여줘"
```

또는 직접적으로:
```
"get_document_info를 사용해서 현재 Figma 문서의 정보를 가져와줘"
```

**가져오는 정보:**
- 문서의 모든 페이지 목록
- 각 페이지의 프레임 및 컴포넌트 구조
- 문서의 메타데이터

**활용 예시:**
```markdown
문서 구조를 파악한 후:
- "로그인 페이지를 찾아줘"
- "메인 화면의 컴포넌트 목록을 보여줘"
```

### 1-2. 현재 선택된 요소 정보 가져오기

**Figma에서:**
1. 원하는 디자인 요소(프레임, 컴포넌트, 텍스트 등)를 선택

**Cursor에서 요청:**
```
"Figma에서 현재 선택한 요소의 정보를 가져와줘"
```

또는:
```
"get_selection을 사용해서 선택된 요소의 상세 정보를 보여줘"
```

**가져오는 정보:**
- 요소의 타입 (FRAME, COMPONENT, TEXT, RECTANGLE 등)
- 위치 (x, y 좌표)
- 크기 (width, height)
- 색상 정보 (fill, stroke)
- 텍스트 내용 (텍스트 요소인 경우)
- 폰트 정보 (fontFamily, fontSize, fontWeight 등)
- 자식 요소들 (children)
- 제약 조건 (constraints)
- 자동 레이아웃 정보 (layoutMode, padding 등)

### 1-3. 특정 노드의 상세 정보 가져오기

**Cursor에서 요청:**
```
"노드 ID [node_id]의 상세 정보를 가져와줘"
```

또는:
```
"get_node_info를 사용해서 특정 노드의 모든 속성을 보여줘"
```

**활용:**
- 특정 컴포넌트의 상세 스펙 확인
- 중첩된 요소의 정보 확인

### 1-4. 디자인 상세 정보 읽기

**Cursor에서 요청:**
```
"Figma에서 선택한 디자인의 상세 정보를 읽어서 Flutter 코드로 변환 가능한 형태로 보여줘"
```

또는:
```
"read_my_design을 사용해서 선택된 디자인의 모든 정보를 가져와줘"
```

## 🎨 Step 2: 디자인 정보 분석 및 구조화

가져온 정보를 바탕으로 다음과 같은 분석이 가능합니다:

### 2-1. 레이아웃 분석
- **Flex 레이아웃**: `layoutMode`가 "HORIZONTAL" 또는 "VERTICAL"인 경우
- **Stack 레이아웃**: 자식 요소들이 겹쳐있는 경우
- **Grid 레이아웃**: 자동 레이아웃이 설정된 경우

### 2-2. 스타일 분석
- **색상**: fill 색상, stroke 색상
- **타이포그래피**: 폰트, 크기, 두께, 줄 간격
- **모서리**: cornerRadius
- **그림자**: effects (shadow, blur)

### 2-3. 컴포넌트 분석
- **컴포넌트 인스턴스**: 컴포넌트로부터 생성된 인스턴스
- **오버라이드**: 인스턴스에서 변경된 속성
- **변형(Variants)**: 컴포넌트의 다른 상태

## 💻 Step 3: Flutter 코드로 변환

### 3-1. 기본 변환 예시

**Cursor에서 요청:**
```
"Figma에서 선택한 프레임을 Flutter 위젯 코드로 변환해줘.
프로젝트의 presentation/widgets/common 스타일을 참고해서 변환해줘."
```

**변환 과정:**
1. Figma 요소 → Flutter 위젯 매핑
   - FRAME → Container, Column, Row, Stack
   - TEXT → Text
   - RECTANGLE → Container
   - COMPONENT → Custom Widget

2. 스타일 변환
   - Figma 색상 → Flutter Color
   - Figma 폰트 → Flutter TextStyle
   - Figma 패딩 → Flutter EdgeInsets
   - Figma 모서리 → Flutter BorderRadius

3. 레이아웃 변환
   - HORIZONTAL layout → Row
   - VERTICAL layout → Column
   - 자동 레이아웃 → Flex 위젯들

### 3-2. 실제 변환 예시

**Figma 디자인:**
- 프레임: 375x812 (모바일 화면)
- 자동 레이아웃: VERTICAL, padding: 24
- 자식 요소:
  - 텍스트: "로그인" (H1, 24px, Bold)
  - 텍스트 필드 프레임
  - 버튼 프레임

**변환된 Flutter 코드:**
```dart
Column(
  mainAxisSize: MainAxisSize.min,
  crossAxisAlignment: CrossAxisAlignment.stretch,
  children: [
    Text(
      '로그인',
      style: TextStyle(
        fontSize: 24,
        fontWeight: FontWeight.bold,
      ),
    ),
    SizedBox(height: 24),
    // 텍스트 필드
    TextField(
      // ...
    ),
    SizedBox(height: 16),
    // 버튼
    ElevatedButton(
      // ...
    ),
  ],
)
```

## 🛠️ Step 4: 고급 활용

### 4-1. 컴포넌트 시스템 활용

**컴포넌트 정보 가져오기:**
```
"Figma에서 사용 가능한 모든 컴포넌트 목록을 가져와줘"
```

**컴포넌트 기반 코드 생성:**
```
"Figma의 Button 컴포넌트를 Flutter 위젯으로 변환해줘.
프로젝트의 primary_button.dart 스타일을 참고해서 만들어줘."
```

### 4-2. 텍스트 일괄 처리

**텍스트 노드 스캔:**
```
"Figma 문서의 모든 텍스트 노드를 스캔해서 목록을 보여줘"
```

**텍스트 일괄 교체:**
```
"Figma에서 'Old Text'를 'New Text'로 일괄 교체해줘"
```

### 4-3. 스타일 시스템 활용

**스타일 정보 가져오기:**
```
"Figma 문서의 모든 텍스트 스타일과 컬러 스타일을 가져와서 
Flutter의 theme.dart 파일로 변환해줘"
```

## 📝 실제 사용 워크플로우

### 시나리오 1: 로그인 화면 구현

1. **Figma에서 로그인 화면 프레임 선택**

2. **Cursor에서 요청:**
   ```
   "Figma에서 현재 선택한 로그인 화면 디자인을 가져와서 
   Flutter의 presentation/screens/auth/login_screen.dart 파일을 생성해줘.
   프로젝트의 Clean Architecture 패턴을 따르고,
   presentation/widgets/common의 기존 위젯들을 활용해줘."
   ```

3. **AI가 수행하는 작업:**
   - `get_selection`으로 디자인 정보 가져오기
   - 레이아웃 및 스타일 분석
   - 기존 프로젝트 구조 확인
   - Flutter 코드 생성
   - 적절한 디렉토리에 파일 생성

### 시나리오 2: 버튼 컴포넌트 생성

1. **Figma에서 버튼 컴포넌트 선택**

2. **Cursor에서 요청:**
   ```
   "Figma의 Primary Button 컴포넌트를 가져와서 
   presentation/widgets/common/buttons/primary_button.dart 파일을 만들어줘.
   Riverpod을 사용한 상태 관리와 함께 구현해줘."
   ```

3. **AI가 수행하는 작업:**
   - `get_node_info`로 컴포넌트 상세 정보 가져오기
   - 컴포넌트의 variants 확인
   - Flutter 버튼 위젯 생성
   - 프로젝트 스타일에 맞게 코드 작성

### 시나리오 3: 디자인 시스템 구축

1. **Figma에서 디자인 토큰 확인**

2. **Cursor에서 요청:**
   ```
   "Figma 문서의 모든 컬러 스타일과 텍스트 스타일을 가져와서 
   Flutter의 core/theme/app_theme.dart 파일을 업데이트해줘."
   ```

3. **AI가 수행하는 작업:**
   - `get_styles`로 모든 스타일 정보 가져오기
   - Flutter ThemeData로 변환
   - 기존 테마 파일 업데이트

## 🎯 유용한 명령어 모음

### 정보 가져오기
```
"Figma 문서 정보 가져오기"
"현재 선택한 요소 정보 보여줘"
"특정 노드 [node_id]의 정보 가져와줘"
"모든 컴포넌트 목록 보여줘"
"텍스트 스타일 목록 가져와줘"
```

### 코드 변환
```
"선택한 디자인을 Flutter 코드로 변환해줘"
"이 컴포넌트를 Flutter 위젯으로 만들어줘"
"프레임을 Flutter 화면 코드로 변환해줘"
```

### 프로젝트 통합
```
"Figma 디자인을 가져와서 [파일 경로]에 Flutter 코드로 저장해줘"
"기존 [위젯 파일] 스타일에 맞춰서 변환해줘"
"프로젝트의 Clean Architecture 패턴을 따라 코드 생성해줘"
```

## ⚠️ 주의사항

1. **채널 연결 확인**: 명령 전에 Figma 플러그인이 채널에 연결되어 있는지 확인
2. **요소 선택**: Figma에서 변환할 요소를 먼저 선택
3. **프로젝트 구조 이해**: AI가 프로젝트의 기존 구조를 참고하도록 명확히 지시
4. **스타일 일관성**: 기존 위젯 스타일을 참고하도록 요청

## 🔄 반복 작업 자동화

### 템플릿 활용
```
"Figma에서 선택한 디자인을 가져와서 
[기존 화면 파일]과 같은 구조로 새로운 화면을 만들어줘"
```

### 일괄 변환
```
"Figma의 모든 화면 프레임을 가져와서 
각각을 Flutter 화면 파일로 변환해줘"
```

## 📚 참고

- [MCP_SETUP.md](../MCP_SETUP.md) - MCP 서버 설정 방법
- [Flutter 프로젝트 컨벤션](../flutter/project_convention.md) - 프로젝트 구조 가이드


