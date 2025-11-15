/// 앱에서 사용하는 이미지 assets 경로를 관리하는 상수 클래스
/// 
/// 사용 예시:
/// ```dart
/// Image.asset(AppAssets.logo)
/// ```
class AppAssets {
  AppAssets._();

  // Images
  static const String logo = 'assets/images/logo.png';
  static const String placeholder = 'assets/images/placeholder.png';
  
  // Icons
  static const String iconUser = 'assets/icons/user.png';
  static const String iconSettings = 'assets/icons/settings.png';
  
  // Illustrations
  static const String illustrationEmpty = 'assets/illustrations/empty.png';
  static const String illustrationError = 'assets/illustrations/error.png';
}

