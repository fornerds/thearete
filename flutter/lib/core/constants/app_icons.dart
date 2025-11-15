/// 앱에서 사용하는 SVG 아이콘 경로를 관리하는 상수 클래스
/// 
/// 사용 예시:
/// ```dart
/// CustomIcon(
///   icon: AppIcons.plus,
///   size: 16,
/// )
/// ```
class AppIcons {
  AppIcons._();

  // 기본 경로
  static const String _basePath = 'assets/icons';

  // Action Icons
  static const String plus = '$_basePath/plus.svg';
  static const String plusMedium = '$_basePath/plus_medium.svg';
  static const String close = '$_basePath/close.svg';
  static const String closeWhite = '$_basePath/close_white.svg';
  static const String edit = '$_basePath/edit.svg';
  static const String check = '$_basePath/check.svg';
  static const String pinActive = '$_basePath/pin_active.svg';
  static const String pinInactive = '$_basePath/pin_inactive.svg';

  // Communication Icons
  static const String chat = '$_basePath/chat.svg';
  static const String phone = '$_basePath/phone.svg';
  static const String announce = '$_basePath/announce.svg';

  // Navigation Icons
  static const String arrowRight = '$_basePath/arrow_right.svg';
  static const String arrowRightSmall = '$_basePath/arrow_right_small.svg';
  static const String arrowRightSmallLight = '$_basePath/arrow_right_small_light.svg';
  static const String arrowRightSmallDark = '$_basePath/arrow_right_small_dark.svg';
  static const String arrowDown = '$_basePath/arrow_down.svg';
  static const String arrowDownSmall = '$_basePath/arrow_down_small.svg';
  static const String arrowUp = '$_basePath/arrow_up.svg';
  static const String arrowUpSmall = '$_basePath/arrow_up_small.svg';
  static const String search = '$_basePath/search.svg';

  // UI Icons
  static const String moreVertical = '$_basePath/more_vertical.svg';
  static const String moreHorizontal = '$_basePath/more_horizontal.svg';
  static const String calendar = '$_basePath/calendar.svg';
  static const String camera = '$_basePath/camera.svg';
  static const String shop = '$_basePath/shop.svg';
  static const String dotLoading = '$_basePath/dot_loading.svg';

  // User Icons
  static const String userMen = '$_basePath/user_men.svg';
  static const String userMenLarge = '$_basePath/user_men_large.svg';
  static const String userWomen = '$_basePath/user_women.svg';
  static const String userWomenLarge = '$_basePath/user_women_large.svg';
}

