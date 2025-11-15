import 'package:flutter/material.dart';
import '../../../../core/constants/app_colors.dart';

/// 보조 액션을 수행하는 Secondary 버튼 컴포넌트
/// Figma 디자인 시스템 기반으로 제작
class SecondaryButton extends StatelessWidget {
  final String text;
  final VoidCallback? onPressed;
  final bool isLoading;
  final double? width;
  final double? height;
  final EdgeInsetsGeometry? padding;
  final double borderRadius;

  const SecondaryButton({
    super.key,
    required this.text,
    this.onPressed,
    this.isLoading = false,
    this.width,
    this.height,
    this.padding,
    this.borderRadius = 8.0,
  });

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: width,
      height: height,
      child: OutlinedButton(
        onPressed: isLoading ? null : onPressed,
        style: OutlinedButton.styleFrom(
          foregroundColor: AppColors.medicalDarkBlue,
          disabledForegroundColor: AppColors.medicalLightBlueGray,
          side: BorderSide(
            color: onPressed == null
                ? AppColors.medicalLightBlueGray
                : AppColors.medicalDarkBlue,
            width: 1.5,
          ),
          padding: padding ?? const EdgeInsets.symmetric(
            horizontal: 24,
            vertical: 16,
          ),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(borderRadius),
          ),
        ),
        child: isLoading
            ? const SizedBox(
                height: 20,
                width: 20,
                child: CircularProgressIndicator(
                  strokeWidth: 2,
                  valueColor: AlwaysStoppedAnimation<Color>(
                    AppColors.medicalDarkBlue,
                  ),
                ),
              )
            : Text(
                text,
                style: const TextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.w600,
                ),
              ),
      ),
    );
  }
}

