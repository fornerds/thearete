import 'package:flutter/material.dart';

import '../../../../core/constants/app_colors.dart';
import '../../../../core/constants/app_icons.dart';
import '../icons/custom_icon.dart';

/// 고객 카드 위젯
/// 
/// 사용 예시:
/// ```dart
/// CustomerCard(
///   name: '홍길동',
///   gender: 'M',
///   age: 30,
///   treatmentName: '리프팅',
///   additionalTreatments: 2,
///   isPinned: false,
///   onPinToggle: (pinned) { ... },
///   onTap: () { ... },
/// )
/// ```
class CustomerCard extends StatelessWidget {
  final String name;
  final String? gender; // 'M' or 'F'
  final int? age;
  final String? treatmentName;
  final int additionalTreatments;
  final bool isPinned;
  final ValueChanged<bool>? onPinToggle;
  final VoidCallback? onTap;

  const CustomerCard({
    super.key,
    required this.name,
    this.gender,
    this.age,
    this.treatmentName,
    this.additionalTreatments = 0,
    this.isPinned = false,
    this.onPinToggle,
    this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    // 성별에 따른 기본 이미지
    final userIcon = gender == 'F' 
        ? AppIcons.userWomenLarge 
        : AppIcons.userMenLarge;

    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(8),
      child: Container(
        constraints: const BoxConstraints(minHeight: 58),
        padding: const EdgeInsets.all(10),
        decoration: BoxDecoration(
          color: AppColors.grayScaleBackground,
          borderRadius: BorderRadius.circular(8),
          // 테두리 제거
        ),
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            // 프로필 이미지 (배경색이 SVG에 포함됨)
            CustomIcon(
              icon: userIcon,
              size: 38,
            ),
            const SizedBox(width: 18),
            // 고객 정보
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                mainAxisSize: MainAxisSize.min,
                children: [
                  // 고객 이름과 핀 버튼
                  Row(
                    crossAxisAlignment: CrossAxisAlignment.center,
                    children: [
                      Expanded(
                        flex: 1,
                        child: Text(
                          '$name님',
                          style: TextStyle(
                            fontSize: 16,
                            fontWeight: FontWeight.w700,
                            color: AppColors.grayScaleText,
                            height: 1.5,
                          ),
                          overflow: TextOverflow.ellipsis,
                          maxLines: 1,
                        ),
                      ),
                      const SizedBox(width: 2),
                      // 고정 토글 버튼
                      GestureDetector(
                        onTap: onPinToggle != null
                            ? () => onPinToggle!(!isPinned)
                            : null,
                        child: CustomIcon(
                          icon: isPinned ? AppIcons.pinActive : AppIcons.pinInactive,
                          size: 20,
                          color: isPinned 
                              ? AppColors.keyColor3 
                              : AppColors.grayScaleGuideText,
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 4),
                  // 성별, 나이, 시술 정보
                  SizedBox(
                    height: 20,
                    child: Row(
                      crossAxisAlignment: CrossAxisAlignment.baseline,
                      textBaseline: TextBaseline.alphabetic,
                      children: [
                        if (gender != null) ...[
                          Flexible(
                            child: Text(
                              gender == 'M' ? '남성' : '여성',
                              style: TextStyle(
                                fontSize: 14,
                                fontWeight: FontWeight.w600,
                                color: AppColors.grayScaleSubText2,
                                height: 1.35,
                              ),
                              overflow: TextOverflow.ellipsis,
                            ),
                          ),
                          if (age != null || treatmentName != null) ...[
                            Padding(
                              padding: const EdgeInsets.symmetric(horizontal: 4),
                              child: Text(
                                '·',
                                style: TextStyle(
                                  fontSize: 14,
                                  fontWeight: FontWeight.w600,
                                  color: AppColors.grayScaleSubText2,
                                  height: 1.0, // line-height를 1.0으로 조정
                                ),
                              ),
                            ),
                          ],
                        ],
                        if (age != null) ...[
                          Flexible(
                            child: Text(
                              '$age세',
                              style: TextStyle(
                                fontSize: 14,
                                fontWeight: FontWeight.w600,
                                color: AppColors.grayScaleSubText2,
                                height: 1.35,
                              ),
                              overflow: TextOverflow.ellipsis,
                            ),
                          ),
                          if (treatmentName != null) ...[
                            Padding(
                              padding: const EdgeInsets.symmetric(horizontal: 4),
                              child: Text(
                                '·',
                                style: TextStyle(
                                  fontSize: 14,
                                  fontWeight: FontWeight.w600,
                                  color: AppColors.grayScaleSubText2,
                                  height: 1.0, // line-height를 1.0으로 조정
                                ),
                              ),
                            ),
                          ],
                        ],
                        if (treatmentName != null) ...[
                          Flexible(
                            child: Text.rich(
                              TextSpan(
                                children: [
                                  TextSpan(
                                    text: treatmentName!,
                                    style: TextStyle(
                                      fontSize: 14,
                                      fontWeight: FontWeight.w600,
                                      color: AppColors.keyColor3,
                                      height: 1.35,
                                    ),
                                  ),
                                  if (additionalTreatments > 0)
                                    TextSpan(
                                      text: ' 외 ${additionalTreatments}건',
                                      style: TextStyle(
                                        fontSize: 14,
                                        fontWeight: FontWeight.w600,
                                        color: AppColors.keyColor3,
                                        height: 1.35,
                                      ),
                                    ),
                                ],
                              ),
                              overflow: TextOverflow.ellipsis,
                              maxLines: 1,
                            ),
                          ),
                        ],
                      ],
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

