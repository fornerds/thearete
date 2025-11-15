import 'package:flutter/material.dart';
import '../../../../core/constants/app_colors.dart';
import 'stories/button_story.dart';
import 'stories/text_field_story.dart';
import 'stories/text_area_story.dart';
import 'stories/number_field_story.dart';
import 'stories/select_field_story.dart';
import 'stories/radio_button_story.dart';
import 'stories/checkbox_story.dart';
import 'stories/filter_box_story.dart';
import 'stories/tag_story.dart';
import 'stories/pagination_story.dart';
import 'stories/email_verification_story.dart';

/// 컴포넌트 쇼케이스 메인 화면
/// Storybook 스타일로 모든 컴포넌트를 테스트할 수 있습니다
class ComponentShowcaseScreen extends StatelessWidget {
  const ComponentShowcaseScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.medicalOffWhite,
      appBar: AppBar(
        title: const Text('Component Showcase'),
        backgroundColor: AppColors.medicalDarkBlue,
        foregroundColor: Colors.white,
        elevation: 0,
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          _buildSectionHeader('Buttons'),
          _buildComponentCard(
            context,
            title: 'Primary Button',
            description: '주요 액션을 수행하는 Primary 버튼',
            icon: Icons.touch_app,
            onTap: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => const ButtonStory(),
                ),
              );
            },
          ),
          const SizedBox(height: 12),
          _buildSectionHeader('Inputs'),
          _buildComponentCard(
            context,
            title: 'Text Field',
            description: '커스텀 텍스트 입력 필드',
            icon: Icons.text_fields,
            onTap: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => const TextFieldStory(),
                ),
              );
            },
          ),
          const SizedBox(height: 12),
          _buildComponentCard(
            context,
            title: 'Text Area',
            description: '여러 줄 텍스트 입력 영역',
            icon: Icons.text_fields,
            onTap: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => const TextAreaStory(),
                ),
              );
            },
          ),
          const SizedBox(height: 12),
          _buildComponentCard(
            context,
            title: 'Number Field',
            description: '숫자 전용 입력 필드',
            icon: Icons.numbers,
            onTap: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => const NumberFieldStory(),
                ),
              );
            },
          ),
          const SizedBox(height: 12),
          _buildComponentCard(
            context,
            title: 'Select Field',
            description: '드롭다운 선택 컴포넌트',
            icon: Icons.arrow_drop_down_circle,
            onTap: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => const SelectFieldStory(),
                ),
              );
            },
          ),
          const SizedBox(height: 12),
          _buildSectionHeader('Selection'),
          _buildComponentCard(
            context,
            title: 'Radio Button',
            description: '라디오 버튼 컴포넌트',
            icon: Icons.radio_button_checked,
            onTap: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => const RadioButtonStory(),
                ),
              );
            },
          ),
          const SizedBox(height: 12),
          _buildComponentCard(
            context,
            title: 'Checkbox',
            description: '체크박스 컴포넌트',
            icon: Icons.check_box,
            onTap: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => const CheckboxStory(),
                ),
              );
            },
          ),
          const SizedBox(height: 12),
          _buildSectionHeader('Tags & Filters'),
          _buildComponentCard(
            context,
            title: 'Tag',
            description: '태그 컴포넌트',
            icon: Icons.label,
            onTap: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => const TagStory(),
                ),
              );
            },
          ),
          const SizedBox(height: 12),
          _buildComponentCard(
            context,
            title: 'Filter Box',
            description: '필터링 박스 컴포넌트',
            icon: Icons.filter_list,
            onTap: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => const FilterBoxStory(),
                ),
              );
            },
          ),
          const SizedBox(height: 12),
          _buildSectionHeader('Navigation'),
          _buildComponentCard(
            context,
            title: 'Pagination',
            description: '페이지네이션 컴포넌트',
            icon: Icons.pages,
            onTap: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => const PaginationStory(),
                ),
              );
            },
          ),
          const SizedBox(height: 12),
          _buildSectionHeader('Forms'),
          _buildComponentCard(
            context,
            title: 'Email Verification',
            description: '이메일 인증 컴포넌트',
            icon: Icons.email,
            onTap: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => const EmailVerificationStory(),
                ),
              );
            },
          ),
        ],
      ),
    );
  }

  Widget _buildSectionHeader(String title) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 12, top: 8),
      child: Text(
        title,
        style: TextStyle(
          fontSize: 20,
          fontWeight: FontWeight.bold,
          color: AppColors.medicalDarkBlue,
        ),
      ),
    );
  }

  Widget _buildComponentCard(
    BuildContext context, {
    required String title,
    required String description,
    required IconData icon,
    required VoidCallback onTap,
  }) {
    return Card(
      elevation: 2,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12),
      ),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(12),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Row(
            children: [
              Container(
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: AppColors.medicalPaleBlue.withOpacity(0.3),
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Icon(
                  icon,
                  color: AppColors.medicalDarkBlue,
                  size: 24,
                ),
              ),
              const SizedBox(width: 16),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      title,
                      style: TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.w600,
                        color: AppColors.medicalDarkBlue,
                      ),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      description,
                      style: TextStyle(
                        fontSize: 14,
                        color: AppColors.medicalLightBlueGray,
                      ),
                    ),
                  ],
                ),
              ),
              Icon(
                Icons.chevron_right,
                color: AppColors.medicalLightBlueGray,
              ),
            ],
          ),
        ),
      ),
    );
  }
}

