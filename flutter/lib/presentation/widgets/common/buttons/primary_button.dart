import 'package:flutter/material.dart';
import '../../../../core/constants/app_colors.dart';

/// 주요 액션을 수행하는 Primary 버튼 컴포넌트
/// Figma 디자인 시스템 기반으로 제작
class PrimaryButton extends StatelessWidget {
  final String text;
  final VoidCallback? onPressed;
  final bool isLoading;
  final double? width;
  final double? height;
  final EdgeInsetsGeometry? padding;
  final double borderRadius;

  const PrimaryButton({
    super.key,
    required this.text,
    this.onPressed,
    this.isLoading = false,
    this.width,
    this.height,
    this.padding,
    this.borderRadius = 6.0,
  });

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: width,
      height: height ?? 48, // 기본 높이 48px
      child: ElevatedButton(
        onPressed: isLoading ? null : onPressed,
        style: ElevatedButton.styleFrom(
          backgroundColor: AppColors.keyColor4,
          foregroundColor: AppColors.box,
          disabledBackgroundColor: AppColors.medicalLightBlueGray,
          disabledForegroundColor: Colors.white70,
          padding: padding ?? const EdgeInsets.symmetric(
            horizontal: 16,
            vertical: 10,
          ),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(borderRadius),
          ),
          elevation: 0,
        ),
        child: isLoading
            ? const SizedBox(
                height: 20,
                width: 20,
                child: CircularProgressIndicator(
                  strokeWidth: 2,
                  valueColor: AlwaysStoppedAnimation<Color>(AppColors.box),
                ),
              )
            : Text(
                text,
                style: const TextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.w700,
                  height: 1.35, // line-height: 135% (21.6px / 16px)
                ),
              ),
      ),
    );
  }
}

