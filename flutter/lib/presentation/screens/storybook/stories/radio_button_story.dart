import 'package:flutter/material.dart';
import '../../../../core/constants/app_colors.dart';
import '../../../widgets/common/radio/custom_radio_button.dart';
import 'base_story.dart';

/// 라디오 버튼 컴포넌트 스토리
class RadioButtonStory extends StatefulWidget {
  const RadioButtonStory({super.key});

  @override
  State<RadioButtonStory> createState() => _RadioButtonStoryState();
}

class _RadioButtonStoryState extends State<RadioButtonStory> {
  String? _selectedValue1;
  String? _selectedValue2;
  int? _selectedValue3;
  String? _selectedValue4;
  
  bool _enabled = true;

  @override
  Widget build(BuildContext context) {
    return BaseStory(
      title: 'Radio Button',
      description: '라디오 버튼 컴포넌트의 다양한 상태(default, hover, checked)를 테스트할 수 있습니다.',
      controls: Column(
        children: [
          ControlSection(
            title: 'General',
            children: [
              SwitchListTile(
                title: const Text('Enabled'),
                value: _enabled,
                onChanged: (value) {
                  setState(() => _enabled = value);
                },
              ),
            ],
          ),
        ],
      ),
      preview: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          CustomRadioGroup<String>(
            value: _selectedValue1,
            onChanged: _enabled
                ? (value) {
                    setState(() => _selectedValue1 = value);
                  }
                : null,
            enabled: _enabled,
            options: const [
              CustomRadioOption(value: 'option1', label: '옵션 1'),
              CustomRadioOption(value: 'option2', label: '옵션 2'),
              CustomRadioOption(value: 'option3', label: '옵션 3'),
            ],
          ),
        ],
      ),
      variants: [
        _buildVariantCard(
          'Horizontal Layout',
          CustomRadioGroup<String>(
            value: _selectedValue2,
            onChanged: (value) {
              setState(() => _selectedValue2 = value);
            },
            direction: Axis.horizontal,
            spacing: 24,
            options: const [
              CustomRadioOption(value: 'option1', label: '옵션 1'),
              CustomRadioOption(value: 'option2', label: '옵션 2'),
              CustomRadioOption(value: 'option3', label: '옵션 3'),
            ],
          ),
        ),
        const SizedBox(height: 16),
        _buildVariantCard(
          'With Disabled Option',
          CustomRadioGroup<String>(
            value: _selectedValue4,
            onChanged: (value) {
              setState(() => _selectedValue4 = value);
            },
            options: const [
              CustomRadioOption(value: 'option1', label: '옵션 1'),
              CustomRadioOption(value: 'option2', label: '옵션 2 (비활성화)', disabled: true),
              CustomRadioOption(value: 'option3', label: '옵션 3'),
            ],
          ),
        ),
        const SizedBox(height: 16),
        _buildVariantCard(
          'Integer Type',
          CustomRadioGroup<int>(
            value: _selectedValue3,
            onChanged: (value) {
              setState(() => _selectedValue3 = value);
            },
            options: const [
              CustomRadioOption(value: 1, label: '1번'),
              CustomRadioOption(value: 2, label: '2번'),
              CustomRadioOption(value: 3, label: '3번'),
            ],
          ),
        ),
        const SizedBox(height: 16),
        _buildVariantCard(
          'Disabled Group',
          CustomRadioGroup<String>(
            value: 'option2',
            onChanged: null,
            enabled: false,
            options: const [
              CustomRadioOption(value: 'option1', label: '옵션 1'),
              CustomRadioOption(value: 'option2', label: '옵션 2'),
              CustomRadioOption(value: 'option3', label: '옵션 3'),
            ],
          ),
        ),
        const SizedBox(height: 16),
        _buildVariantCard(
          'Different Sizes',
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              CustomRadioButton<String>(
                value: 'small',
                groupValue: 'small',
                onChanged: null,
                label: 'Small (16px)',
                size: 16,
              ),
              const SizedBox(height: 8),
              CustomRadioButton<String>(
                value: 'medium',
                groupValue: 'medium',
                onChanged: null,
                label: 'Medium (20px)',
                size: 20,
              ),
              const SizedBox(height: 8),
              CustomRadioButton<String>(
                value: 'large',
                groupValue: 'large',
                onChanged: null,
                label: 'Large (24px)',
                size: 24,
              ),
            ],
          ),
        ),
      ],
    );
  }

  Widget _buildVariantCard(String title, Widget content) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
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
            const SizedBox(height: 12),
            content,
          ],
        ),
      ),
    );
  }
}

