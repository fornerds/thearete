# Assets 폴더 구조

이 폴더는 앱에서 사용하는 정적 리소스(이미지, 아이콘 등)를 보관합니다.

## 폴더 구조

```
assets/
├── images/          # 일반 이미지 (로고, 배경, 사진 등)
├── icons/          # 아이콘 이미지
└── illustrations/  # 일러스트레이션
```

## 사용 방법

1. 이미지를 해당 폴더에 추가
2. `pubspec.yaml`에 assets 경로 등록
3. 코드에서 `AssetImage` 또는 `Image.asset()` 사용

## 예시

```dart
// 이미지 사용
Image.asset('assets/images/logo.png')

// 또는
AssetImage('assets/images/logo.png')
```

