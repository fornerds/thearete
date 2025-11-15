import 'package:flutter/material.dart';
import '../../../../core/constants/app_colors.dart';

/// 텍스트 형태의 버튼 컴포넌트
/// Figma 디자인 시스템 기반으로 제작
class AppTextButton extends StatelessWidget {
  final String text;
  final VoidCallback? onPressed;
  final bool isLoading;
  final double? width;
  final Color? textColor;
  final double fontSize;
  final FontWeight fontWeight;

  const AppTextButton({
    super.key,
    required this.text,
    this.onPressed,
    this.isLoading = false,
    this.width,
    this.textColor,
    this.fontSize = 16,
    this.fontWeight = FontWeight.w600,
  });

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: width,
      child: TextButton(
        onPressed: isLoading ? null : onPressed,
        style: TextButton.styleFrom(
          foregroundColor: textColor ?? AppColors.medicalDarkBlue,
          disabledForegroundColor: AppColors.medicalLightBlueGray,
          padding: const EdgeInsets.symmetric(
            horizontal: 16,
            vertical: 12,
          ),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(8),
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
                style: TextStyle(
                  fontSize: fontSize,
                  fontWeight: fontWeight,
                ),
              ),
      ),
    );
  }
}

