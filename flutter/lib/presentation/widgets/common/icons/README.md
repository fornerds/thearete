# 아이콘 사용 가이드

프로젝트에서 SVG 아이콘을 효율적으로 관리하고 사용하는 방법을 안내합니다.

## 구조

```
lib/
├── core/
│   └── constants/
│       └── app_icons.dart          # 아이콘 경로 상수 정의
└── presentation/
    └── widgets/
        └── common/
            └── icons/
                └── custom_icon.dart # CustomIcon 위젯 및 AppIconWidgets
```

## 사용 방법

### 1. CustomIcon 위젯 사용 (권장)

가장 유연한 방법으로, 모든 아이콘에 사용할 수 있습니다.

```dart
import 'package:thearete_clinic/presentation/widgets/common/icons/custom_icon.dart';
import 'package:thearete_clinic/core/constants/app_icons.dart';

// 기본 사용
CustomIcon(
  icon: AppIcons.plus,
  size: 16,
)

// 색상 변경
CustomIcon(
  icon: AppIcons.edit,
  size: 20,
  color: AppColors.keyColor3,
)

// 클릭 가능한 아이콘
CustomIcon(
  icon: AppIcons.close,
  size: 16,
  onTap: () {
    // 클릭 시 동작
  },
)

// width/height 개별 지정
CustomIcon(
  icon: AppIcons.calendar,
  width: 17,
  height: 19,
)
```

### 2. AppIconWidgets 편의 메서드 사용

자주 사용되는 아이콘들을 위한 편의 메서드입니다.

```dart
import 'package:thearete_clinic/presentation/widgets/common/icons/custom_icon.dart';

// Plus 아이콘
AppIconWidgets.plus(
  size: 16,
  color: AppColors.grayScaleSubText2,
  onTap: () => print('Plus clicked'),
)

// Close 아이콘
AppIconWidgets.close(
  size: 11,
  onTap: () => Navigator.pop(context),
)

// Edit 아이콘
AppIconWidgets.edit(
  size: 20,
  onTap: () => _handleEdit(),
)

// Arrow 아이콘들
AppIconWidgets.arrowRight(size: 8)
AppIconWidgets.arrowDown(size: 10)
AppIconWidgets.arrowUp(size: 10)
```

## 사용 가능한 아이콘 목록

### Action Icons
- `AppIcons.plus` - Plus 아이콘
- `AppIcons.close` - Close/X 아이콘 (작은 버전)
- `AppIcons.closeWhite` - Close/X 아이콘 (흰색)
- `AppIcons.edit` - Edit/Pencil 아이콘

### Communication Icons
- `AppIcons.chat` - Chat/Message 아이콘
- `AppIcons.phone` - Phone 아이콘

### Navigation Icons
- `AppIcons.arrowRight` - Arrow right 아이콘
- `AppIcons.arrowDown` - Arrow down 아이콘
- `AppIcons.arrowUp` - Arrow up 아이콘

### UI Icons
- `AppIcons.moreVertical` - More/Vertical dots 아이콘
- `AppIcons.calendar` - Calendar 아이콘

## 새 아이콘 추가하기

1. SVG 파일을 `assets/icons/` 폴더에 추가
2. `app_icons.dart`에 경로 상수 추가:
   ```dart
   static const String newIcon = '$_basePath/new_icon.svg';
   ```
3. 필요시 `AppIconWidgets`에 편의 메서드 추가

## 주의사항

- SVG 파일의 `stroke` 또는 `fill` 색상은 `CustomIcon`의 `color` 파라미터로 덮어쓸 수 있습니다.
- `size`를 지정하면 width와 height가 동일하게 적용됩니다.
- `width`와 `height`를 개별 지정하려면 `size` 대신 `width`와 `height`를 사용하세요.
- 클릭 가능한 아이콘은 `onTap` 콜백을 제공하거나 `isClickable: true`를 설정하세요.

