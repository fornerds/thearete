import 'package:flutter/material.dart';
import '../../../../core/constants/app_colors.dart';

/// Storybook 스타일의 기본 스토리 위젯
/// 모든 스토리 페이지의 기본 레이아웃을 제공합니다
class BaseStory extends StatelessWidget {
  final String title;
  final String description;
  final Widget controls;
  final Widget preview;
  final List<Widget>? variants;

  const BaseStory({
    super.key,
    required this.title,
    required this.description,
    required this.controls,
    required this.preview,
    this.variants,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.medicalOffWhite,
      appBar: AppBar(
        title: Text(title),
        backgroundColor: AppColors.medicalDarkBlue,
        foregroundColor: Colors.white,
        elevation: 0,
      ),
      body: LayoutBuilder(
        builder: (context, constraints) {
          final isWide = constraints.maxWidth > 800;
          
          if (isWide) {
            // 와이드 화면: 좌우 분할
            return Row(
              children: [
                // 왼쪽: 컨트롤 패널
                Container(
                  width: 350,
                  color: Colors.white,
                  child: SingleChildScrollView(
                    padding: const EdgeInsets.all(16),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'Controls',
                          style: TextStyle(
                            fontSize: 18,
                            fontWeight: FontWeight.bold,
                            color: AppColors.medicalDarkBlue,
                          ),
                        ),
                        const SizedBox(height: 8),
                        Text(
                          description,
                          style: TextStyle(
                            fontSize: 14,
                            color: AppColors.medicalLightBlueGray,
                          ),
                        ),
                        const SizedBox(height: 16),
                        controls,
                      ],
                    ),
                  ),
                ),
                const VerticalDivider(width: 1),
                // 오른쪽: 미리보기
                Expanded(
                  child: SingleChildScrollView(
                    padding: const EdgeInsets.all(24),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'Preview',
                          style: TextStyle(
                            fontSize: 18,
                            fontWeight: FontWeight.bold,
                            color: AppColors.medicalDarkBlue,
                          ),
                        ),
                        const SizedBox(height: 16),
                        preview,
                        if (variants != null && variants!.isNotEmpty) ...[
                          const SizedBox(height: 32),
                          Text(
                            'Variants',
                            style: TextStyle(
                              fontSize: 18,
                              fontWeight: FontWeight.bold,
                              color: AppColors.medicalDarkBlue,
                            ),
                          ),
                          const SizedBox(height: 16),
                          ...variants!,
                        ],
                      ],
                    ),
                  ),
                ),
              ],
            );
          } else {
            // 좁은 화면: 세로 스크롤
            return SingleChildScrollView(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    title,
                    style: TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                      color: AppColors.medicalDarkBlue,
                    ),
                  ),
                  const SizedBox(height: 8),
                  Text(
                    description,
                    style: TextStyle(
                      fontSize: 14,
                      color: AppColors.medicalLightBlueGray,
                    ),
                  ),
                  const SizedBox(height: 24),
                  Card(
                    child: Padding(
                      padding: const EdgeInsets.all(16),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            'Controls',
                            style: TextStyle(
                              fontSize: 16,
                              fontWeight: FontWeight.bold,
                              color: AppColors.medicalDarkBlue,
                            ),
                          ),
                          const SizedBox(height: 16),
                          controls,
                        ],
                      ),
                    ),
                  ),
                  const SizedBox(height: 24),
                  Card(
                    child: Padding(
                      padding: const EdgeInsets.all(16),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            'Preview',
                            style: TextStyle(
                              fontSize: 16,
                              fontWeight: FontWeight.bold,
                              color: AppColors.medicalDarkBlue,
                            ),
                          ),
                          const SizedBox(height: 16),
                          preview,
                        ],
                      ),
                    ),
                  ),
                  if (variants != null && variants!.isNotEmpty) ...[
                    const SizedBox(height: 24),
                    Card(
                      child: Padding(
                        padding: const EdgeInsets.all(16),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              'Variants',
                              style: TextStyle(
                                fontSize: 16,
                                fontWeight: FontWeight.bold,
                                color: AppColors.medicalDarkBlue,
                              ),
                            ),
                            const SizedBox(height: 16),
                            ...variants!,
                          ],
                        ),
                      ),
                    ),
                  ],
                ],
              ),
            );
          }
        },
      ),
    );
  }
}

/// 컨트롤 섹션 위젯
class ControlSection extends StatelessWidget {
  final String title;
  final List<Widget> children;

  const ControlSection({
    super.key,
    required this.title,
    required this.children,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          title,
          style: TextStyle(
            fontSize: 14,
            fontWeight: FontWeight.w600,
            color: AppColors.medicalDarkBlue,
          ),
        ),
        const SizedBox(height: 8),
        ...children,
        const SizedBox(height: 16),
      ],
    );
  }
}

