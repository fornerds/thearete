import 'package:flutter/material.dart';
import 'package:flutter_svg/flutter_svg.dart';

import '../../../../core/constants/app_colors.dart';
import '../../../../core/constants/app_icons.dart';

/// 커스텀 SVG 아이콘 위젯
/// 
/// 사용 예시:
/// ```dart
/// CustomIcon(
///   icon: AppIcons.plus,
///   size: 16,
///   color: AppColors.grayScaleText,
/// )
/// ```
class CustomIcon extends StatelessWidget {
  /// 아이콘 경로 (AppIcons에서 가져온 경로)
  final String icon;
  
  /// 아이콘 크기 (width와 height 모두 동일하게 적용)
  final double? size;
  
  /// 아이콘 너비 (size가 지정되지 않은 경우 사용)
  final double? width;
  
  /// 아이콘 높이 (size가 지정되지 않은 경우 사용)
  final double? height;
  
  /// 아이콘 색상 (SVG의 stroke/fill 색상을 덮어씀)
  final Color? color;
  
  /// 클릭 가능 여부
  final bool isClickable;
  
  /// 클릭 시 콜백
  final VoidCallback? onTap;

  const CustomIcon({
    super.key,
    required this.icon,
    this.size,
    this.width,
    this.height,
    this.color,
    this.isClickable = false,
    this.onTap,
  }) : assert(
          size != null || (width != null && height != null),
          'size 또는 width/height를 지정해야 합니다.',
        );

  @override
  Widget build(BuildContext context) {
    final effectiveWidth = size ?? width ?? 24;
    final effectiveHeight = size ?? height ?? 24;

    final iconWidget = SvgPicture.asset(
      icon,
      width: effectiveWidth,
      height: effectiveHeight,
      colorFilter: color != null
          ? ColorFilter.mode(color!, BlendMode.srcIn)
          : null,
      fit: BoxFit.contain,
      semanticsLabel: icon.split('/').last,
      placeholderBuilder: (context) => SizedBox(
        width: effectiveWidth,
        height: effectiveHeight,
      ),
    );

    if (isClickable || onTap != null) {
      return InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(4),
        child: Padding(
          padding: const EdgeInsets.all(4),
          child: iconWidget,
        ),
      );
    }

    return iconWidget;
  }
}

/// 자주 사용되는 아이콘들을 위한 편의 위젯들
class AppIconWidgets {
  AppIconWidgets._();

  /// Plus 아이콘
  static Widget plus({
    double? size,
    Color? color,
    VoidCallback? onTap,
  }) {
    return CustomIcon(
      icon: AppIcons.plus,
      size: size ?? 16,
      color: color ?? AppColors.grayScaleSubText2,
      isClickable: onTap != null,
      onTap: onTap,
    );
  }

  /// Close 아이콘
  static Widget close({
    double? size,
    Color? color,
    VoidCallback? onTap,
  }) {
    return CustomIcon(
      icon: AppIcons.close,
      size: size ?? 11,
      color: color ?? AppColors.grayScaleText,
      isClickable: onTap != null,
      onTap: onTap,
    );
  }

  /// Close (White) 아이콘
  static Widget closeWhite({
    double? size,
    VoidCallback? onTap,
  }) {
    return CustomIcon(
      icon: AppIcons.closeWhite,
      size: size ?? 16,
      color: Colors.white,
      isClickable: onTap != null,
      onTap: onTap,
    );
  }

  /// Edit 아이콘
  static Widget edit({
    double? size,
    Color? color,
    VoidCallback? onTap,
  }) {
    return CustomIcon(
      icon: AppIcons.edit,
      size: size ?? 16,
      color: color ?? AppColors.keyColor3,
      isClickable: onTap != null,
      onTap: onTap,
    );
  }

  /// Arrow Right 아이콘
  static Widget arrowRight({
    double? size,
    Color? color,
    VoidCallback? onTap,
  }) {
    return CustomIcon(
      icon: AppIcons.arrowRight,
      size: size ?? 8,
      color: color ?? AppColors.grayScaleText,
      isClickable: onTap != null,
      onTap: onTap,
    );
  }

  /// Arrow Down 아이콘
  static Widget arrowDown({
    double? size,
    Color? color,
    VoidCallback? onTap,
  }) {
    return CustomIcon(
      icon: AppIcons.arrowDown,
      size: size ?? 10,
      color: color ?? AppColors.grayScaleText,
      isClickable: onTap != null,
      onTap: onTap,
    );
  }

  /// Arrow Up 아이콘
  static Widget arrowUp({
    double? size,
    Color? color,
    VoidCallback? onTap,
  }) {
    return CustomIcon(
      icon: AppIcons.arrowUp,
      size: size ?? 10,
      color: color ?? AppColors.grayScaleText,
      isClickable: onTap != null,
      onTap: onTap,
    );
  }

  /// Search 아이콘
  static Widget search({
    double? size,
    Color? color,
    VoidCallback? onTap,
  }) {
    return CustomIcon(
      icon: AppIcons.search,
      size: size ?? 21,
      color: color ?? AppColors.grayScaleText,
      isClickable: onTap != null,
      onTap: onTap,
    );
  }
}

